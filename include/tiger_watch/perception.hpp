#pragma once
#include <string>


namespace tiger_watch {

class PerceptionPipeline {
public:
    PerceptionPipeline(const std::string& engine_path);
    void run();
private:
    RealSenseCapture capture_;
    TensorRTEngine engine_;
    DetectionFusion fusion_;
    Alerting alerting_;
};

} // namespace tiger_watch
