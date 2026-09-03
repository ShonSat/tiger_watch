Jetson SDK: JetPack 5.1.6 | [https://developer.nvidia.com/embedded/jetpack-sdk-516] | 
| only available for host Ubuntu version 20.04 or less

1. Use SDK-manager on Host machine to flash Jetson device with JetPack 5.1.6 username: nvidia, password: nvidia
2. On device boot, add line in (sudo visudo) : 
```
nvidia ALL=(ALL) NOPASSWD:ALL
```
3. Create ssh key on Jetson and add key to your github account: 
```
ssh-keygen -t ed25519 -C $GITHUB_EMAIL
echo "Add content of ~/.ssh/id_ed25519.pub to SSH keys in your Github"
```
4. Verify Native TensorRT Installation and nvcc paths
```
# Verify the installed TensorRT version
dpkg -l | grep nvinfer

# Check that the trtexec utility is present in the standard system path
ls -la /usr/src/tensorrt/samples/trtexec

# Append alias in ~/.bashrc  to to run trtexec from any terminal location on jetson
echo "alias trtexec=/usr/src/tensorrt/bin/trtexec" >> ~/.bashrc

# Verify the alias is added and nvcc paths are present:
cat ~/.bashrc
...
export PATH=/usr/local/cuda-11.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
alias trtexec=/usr/src/tensorrt/bin/trtexec
```

5. System profiling tools.
```
# Update the system package manager and install pip
sudo apt-get update
sudo apt-get install -y python3-pip

# Install jetson-stats globally
sudo pip3 install -U jetson-stats

# Reboot the Jetson to initialize the jtop background system services
sudo reboot
```

6. External USB storage (EXT4 format) configuration (to store data, git repos):
```
lsblk                             # identify drive, i.e. /dev/sda
sudo umount /dev/sdX*
sudo fdisk /dev/sdX               # wipe and create single partition
# in fdisk prompt select options:
# g - creates new clean GPT partition table (wipes out old partition)
# n - creates new partition
# 1 - sets it as partition number 1.
# accept all default start and end sectors
# w - write the changes to the disk and exit 

sudo mkfs.ext4 -F /dev/sdX         # format new partition to EXT4 (linux) format

             
mkdir -p /mnt/usb                  # create directory to mount USB device X
sudo mount /dev/sdX /mnt/usb       # mount the drive, if mount fails due to missing/corrupt blocks, try fixing:  sudo e2fsck -y /dev/sdX
# sudo mount -t ext4  /dev/sdX /mnt/usb
sudo chown -R $USER:USER /mnt/usb  # change ownership to current jetson user

sudo blkid | grep sdX              # identify UUID of the device X:  
# example:  /dev/sda1: UUID="5e00f4cb-362a-4590-86ef-feaf3f3930cf" TYPE="ext4" PARTUUID="1132ab11-01"
# append line to /etc/fstab: UUID="5e00f4cb-362a-4590-86ef-feaf3f3930cf" /mnt/usb ext4 defaults,nofail  0 2 

sudo mount -a                      # mount all filesystems mentioned in fstab
```     
 
6. RealSense SDK install and D435 camera sanity with steps in RealSense_Jetson.md
    - Precompiled SDK librealsense2-utils and librealsense2-dev are installed.
    - Git repo cloned on your device ~/librealsense/  
    - Optional: Building from Source with V4L Native backend by applying the kernel patching

7. Clone tiger_watch repo
```
git clone git@github.com:ShonSat/tiger_watch.git 
```

9. Install Ultralytics software: 
- A) docker image from https://github.com/ultralytics/ultralytics#docker
```

```
- B) manually by hand or use script. 
```
~/tiger_watch/jetson_YOLO_setup.sh
```
    
