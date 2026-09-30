// realSense_3d_perception.cpp
// A real-time C++ 3D perception system on Jetson, fusing RealSense D435 depth with TensorRT detections to
// filter point clouds and estimate physical object dimensions.
// RealSense D435 → Point Cloud → Bounding Box Dimensions
// 
//
// Prerequisites:
//   - librealsense2 (https://github.com/realsenseai/librealsense.git)
//   - PCL (Point Cloud Library), example code: https://github.com/realsenseai/librealsense/blob/master/examples/pointcloud/rs-pointcloud.cpp 
//
// Build CMD (Linux):
//   g++ -std=c++17 realSense_3d_perception.cpp -o perception \
//       -lrealsense2 -lpcl_common -lpcl_io -lpcl_filters -lpcl_segmentation

#include <librealsense2/rs.hpp>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/common/common.h>
#include <pcl/filters/passthrough.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/kdtree/kdtree.h>

#include <iostream>
#include <vector>
#include <cmath>
#include <limits>

// #######################################
// Configuration
// #######################################
constexpr int   FRAME_WIDTH   = 640;
constexpr int   FRAME_HEIGHT  = 480;
constexpr int   FRAME_FPS     = 30;
constexpr float MIN_DEPTH_M   = 0.1f;   // 10 cm minimum
constexpr float MAX_DEPTH_M   = 10.0f;  // 10 m maximum
constexpr float GROUND_FILTER_M = 0.2f; // Remove points within 20cm of ground plane

// #######################################
// Data structure for a detection bounding box (from YOLO/TensorRT)
// #######################################
struct Detection {
    int   x1, y1, x2, y2;  // 2D pixel coordinates
    float confidence;
    int   class_id;
};

// #######################################
// Filter point cloud to a 2D bounding box region
// #######################################
pcl::PointCloud<pcl::PointXYZ>::Ptr filterCloudToBBox(
    const rs2::points& points,
    const Detection&   det,
    int                width,
    int                height)
{
    auto cloud = pcl::PointCloud<pcl::PointXYZ>::Ptr(new pcl::PointCloud<pcl::PointXYZ>());
    const rs2::vertex* vertices = points.get_vertices();

    // Clamp bounding box to valid image bounds
    int x1 = std::max(0, std::min(det.x1, width  - 1));
    int y1 = std::max(0, std::min(det.y1, height - 1));
    int x2 = std::max(0, std::min(det.x2, width  - 1));
    int y2 = std::max(0, std::min(det.y2, height - 1));

    cloud->reserve((x2 - x1 + 1) * (y2 - y1 + 1));

    for (int y = y1; y <= y2; ++y) {
        for (int x = x1; x <= x2; ++x) {
            const rs2::vertex& v = vertices[y * width + x];

            // Skip invalid depth (0 or non-finite)
            if (v.z <= MIN_DEPTH_M || v.z > MAX_DEPTH_M || !std::isfinite(v.z))
                continue;

            pcl::PointXYZ pt;
            pt.x = v.x;
            pt.y = v.y;
            pt.z = v.z;
            cloud->push_back(pt);
        }
    }

    return cloud;
}

// #######################################
// Remove ground plane (assumes Y is vertical)
// 
pcl::PointCloud<pcl::PointXYZ>::Ptr removeGround(
    const pcl::PointCloud<pcl::PointXYZ>::Ptr& input)
{
    // Find the minimum Y value (lowest point)
    float min_y = std::numeric_limits<float>::max();
    for (const auto& pt : input->points) {
        if (pt.y < min_y) min_y = pt.y;
    }

    // Filter out points near the ground plane
    auto filtered = pcl::PointCloud<pcl::PointXYZ>::Ptr(new pcl::PointCloud<pcl::PointXYZ>());
    for (const auto& pt : input->points) {
        if (std::abs(pt.y - min_y) > GROUND_FILTER_M) {
            filtered->push_back(pt);
        }
    }

    return filtered;
}

// #######################################
// Compute AABB dimensions from a point cloud
// #######################################
struct Dimensions {
    float width;
    float height;
    float depth;
    float volume;
    bool  valid;
};

Dimensions computeDimensions(const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud)
{
    Dimensions dims{0, 0, 0, 0, false};

    if (cloud->empty() || cloud->size() < 10) {
        return dims;  // Not enough points
    }

    pcl::PointXYZ min_pt, max_pt;
    pcl::getMinMax3d(*cloud, min_pt, max_pt);

    dims.width  = max_pt.x - min_pt.x;
    dims.height = max_pt.y - min_pt.y;
    dims.depth  = max_pt.z - min_pt.z;
    dims.volume = dims.width * dims.height * dims.depth;
    dims.valid  = true;

    return dims;
}

// #######################################
// Main
// #######################################
int main() try
{
    // ── 1. Configure RealSense pipeline ──────────────────────
    rs2::pipeline pipe;
    rs2::config   cfg;

    cfg.enable_stream(RS2_STREAM_DEPTH, FRAME_WIDTH, FRAME_HEIGHT, RS2_FORMAT_Z16, FRAME_FPS);
    cfg.enable_stream(RS2_STREAM_COLOR, FRAME_WIDTH, FRAME_HEIGHT, RS2_FORMAT_BGR8, FRAME_FPS);

    rs2::pipeline_profile profile = pipe.start(cfg);

    // Set the camera to High Accuracy preset for better depth quality
    auto depth_sensor = profile.get_device().first<rs2::depth_sensor>();
    if (depth_sensor.supports(RS2_OPTION_VISUAL_PRESET)) {
        depth_sensor.set_option(RS2_OPTION_VISUAL_PRESET,
                                RS2_RS400_VISUAL_PRESET_HIGH_ACCURACY);
    }

    // ── 2. Create point cloud object ─────────────────────────
    rs2::pointcloud pc;
    rs2::points     points;

    // ── 3. Main loop ─────────────────────────────────────────
    std::cout << "Tiger Watch 3D Perception — Press Ctrl+C to exit\n";

    while (true) {
        // Wait for a new frameset
        rs2::frameset frames = pipe.wait_for_frames();

        // Get depth and color frames
        rs2::depth_frame depth = frames.get_depth_frame();
        rs2::video_frame color = frames.get_color_frame();

        if (!depth || !color) continue;

        // Map color texture onto the point cloud
        pc.map_to(color);

        // Generate the point cloud from the depth frame
        points = pc.calculate(depth);

        // ── Simulated YOLO detection (replace with your TensorRT output) ──
        // For this example, we assume an object is detected at the center
        // of the image. In your Tiger Watch project, replace this with
        // the actual bounding box from your TensorRT inference.
        Detection det;
        det.x1 = FRAME_WIDTH  / 2 - 80;
        det.y1 = FRAME_HEIGHT / 2 - 80;
        det.x2 = FRAME_WIDTH  / 2 + 80;
        det.y2 = FRAME_HEIGHT / 2 + 80;
        det.confidence = 0.95f;
        det.class_id   = 0;  // e.g., "tiger"

        // ── Filter point cloud to the detection region ───────
        auto object_cloud = filterCloudToBBox(points, det, FRAME_WIDTH, FRAME_HEIGHT);

        if (object_cloud->empty()) {
            std::cout << "[Frame] No valid depth points in detection region.\n";
            continue;
        }

        // ── Remove ground plane ──────────────────────────────
        auto object_no_ground = removeGround(object_cloud);

        // ── Compute dimensions ───────────────────────────────
        Dimensions dims = computeDimensions(object_no_ground);

        if (dims.valid) {
            std::cout << "[Detection] class=" << det.class_id
                      << " conf=" << det.confidence
                      << " points=" << object_no_ground->size()
                      << " | W=" << dims.width  << "m"
                      << " H=" << dims.height << "m"
                      << " D=" << dims.depth  << "m"
                      << " V=" << dims.volume << "m³\n";
        }
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error& e) {
    std::cerr << "RealSense error: " << e.what() << "\n";
    return EXIT_FAILURE;
}
catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << "\n";
    return EXIT_FAILURE;
}
