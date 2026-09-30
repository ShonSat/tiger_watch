The ultralytics/ultralytics:latest-jetson-jetpack5 image requires a substantial amount of disk space. The compressed download payload size is roughly 6 GB, and it expands to an uncompressed footprint of approximately 13 GB on your storage drive. [1, 2] 
## ⚠️ The eMMC Storage Trap on AGX Xavier
Because the native internal storage on a standard NVIDIA Jetson AGX Xavier developer kit is only 32 GB of eMMC flash memory, pulling this image directly to your default root path will almost certainly trigger a "No space left on device" error. The baseline JetPack operating system files already occupy most of that internal allocation. [3, 4] 
## 🛠️ Step-by-Step Fixes to Handle the Size

## Option A: Check Your Extant Storage Limits
Before trying to run the pull loop, execute a system space check:

df -h /

If your remaining available space reads under 15 GB, do not initiate the download yet.
## Option A: Clean Your Docker Environment
Free up cached blocks by purging historical dangling container configurations:

sudo docker system prune -a --volumes

## Option B: Re-route Docker Storage Target to an SSD (Best Practice)
If you have mounted an external NVMe SSD or SATA drive to your Xavier developer board, you must configure Docker to store its images there instead of hitting the internal eMMC drive: [4] 

1. Edit  the global Docker daemon settings file:
   
   sudo vim /etc/docker/daemon.json
   
2. Inject a configuration pointer tracking your external drive storage mount path (add a comma if appending to existing parameters):
   
   {
     "data-root": "/media/nvidia/your_ssd_name/docker-data"
   }
   
3. Restart the core background daemon service engine to apply the storage mapping:
   
   sudo systemctl restart docker
   
 

 
# 1. Pull the official Ultralytics image tailored for JetPack 5.x
sudo docker pull ultralytics/ultralytics:latest-jetson-jetpack5

# 2. Run the Docker container with native hardware access mapped
sudo docker run -it --ipc=host --runtime=nvidia \
    --net=host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/bus/usb \
    -v /home/nvidia/tiger_watch:/workspace/tiger_watch \
    ultralytics/ultralytics:latest-jetson-jetpack5
 