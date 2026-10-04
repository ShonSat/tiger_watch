Jetson SDK: JetPack 5.1.7 | [https://developer.nvidia.com/embedded/jetpack-sdk-517] | 
| only available for host Ubuntu version 20.04 or less
Jetson Xavier AGX HW specs: https://docs.nvidia.com/jetson/archives/r35.1/DeveloperGuide/text/HR/JetsonModuleAdaptationAndBringUp/JetsonAgxXavierSeries.html 

https://docs.nvidia.com/jetson/archives/r35.6.5/DeveloperGuide/AT/JetsonLinuxToolchain.html

0. Check the release file: 
• Run cat /etc/nv_tegra_release to see the exact L4T release and build information.
• Query the core package: Run dpkg-query --show nvidia-l4t-core for newer JetPack/L4T versions to see the exact package version installed.
• Check  UEFI boot screen: Read the Jetson System firmware version displayed on the connected monitor during device bootup.
• Check jtop


1. Use SDK Manager on the host machine to flash the Jetson with JetPack 5.1.7. Create a unique user account and password during first boot; do not record credentials in this document.
2. Use `sudo` with the account password for administrative tasks. Avoid blanket `NOPASSWD:ALL` sudo rules. If automation requires elevated access, grant only the specific required commands through a reviewed sudoers policy.
3. Create ssh key on Jetson and add key to your github account: 
```
ssh-keygen -t ed25519 -C $GITHUB_EMAIL
echo "Add content of ~/.ssh/id_ed25519.pub to SSH keys in your Github"
```

## Host-to-Jetson SSH Access

This section configures the host as the SSH client and the Jetson as the SSH server. SSH provides an encrypted management and file-transfer channel; it is not a Layer 2 network bridge. The host and Jetson need IP connectivity over the same LAN or through a permitted routed network. A host on Wi-Fi can reach a Jetson on Ethernet when both are on a network that allows client-to-client traffic.

### Network and service

Use a DHCP reservation or a local DNS name for the Jetson rather than relying on an address that may change. On the Jetson, find its current address and install/enable the OpenSSH server:
```bash
hostname -I
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager
```

OpenSSH listens on TCP port 22 by default. Permit inbound TCP/22 only from the trusted management network in the Jetson firewall or network policy. Do not forward SSH from the public internet through the router. If the host cannot connect, check the Jetson's address, routing, firewall rules, and whether Wi-Fi client isolation or VLAN policy blocks wired-to-wireless traffic. From the host, `ip route get <jetson-host>` can confirm the selected route.

### Verify server identity

Before the first connection, retrieve the Jetson's SSH host-key fingerprint from a trusted Jetson console:
```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Connect from the host using the Jetson account and a DNS name or address obtained from the trusted network configuration:
```bash
ssh <jetson-user>@<jetson-host>
```

Compare the fingerprint shown on first connection with the value obtained from the Jetson console before accepting it. The SSH client records the server host key in the host user's `~/.ssh/known_hosts`. Do not disable host-key checking to bypass a mismatch; verify unexpected host-key changes through a trusted console or administrator.

### Configure key-based authentication

On the host, create an Ed25519 key if an appropriate key does not already exist. Protect the private key with a passphrase and keep it on the host; only its `.pub` public-key file is installed on the Jetson.
```bash
ssh-keygen -t ed25519 -a 64 -C "host-to-jetson"
ssh-copy-id -i ~/.ssh/id_ed25519.pub <jetson-user>@<jetson-host>
```

`ssh-copy-id` prompts for the Jetson account password once and adds the public key to that account's `~/.ssh/authorized_keys`. Verify key-only login from the host:
```bash
ssh -o BatchMode=yes -o PasswordAuthentication=no \
	<jetson-user>@<jetson-host> 'hostname; id -un'
```

For a passphrase-protected key, use the host's SSH agent to avoid re-entering the key passphrase during a login session. `known_hosts` verifies the server; `authorized_keys` grants a client key access. They serve different purposes. The Jetson does not need the host in its `known_hosts` unless the Jetson itself will initiate SSH connections to the host.

### Optional SSH client alias and file transfer

The host can define a local alias in `~/.ssh/config` to avoid repeating the user, host, and key settings. Use placeholders, not device-specific addresses, in shared documentation:
```sshconfig
Host jetson
		HostName <jetson-host>
		User <jetson-user>
		IdentityFile ~/.ssh/id_ed25519
		IdentitiesOnly yes
```

Then connect or transfer files from the host:
```bash
ssh jetson
scp ./artifact jetson:<target-directory>/
rsync -av --progress ./build/ jetson:<target-directory>/build/
```

If SSH is intentionally configured on a non-default port, specify it with `ssh -p <port>`, `scp -P <port>`, or `rsync -e 'ssh -p <port>'`. Keep the selected port restricted to the trusted management network.

## C++ Development Libraries for Host Cross-Compilation

The default CMake targets need ARM64 RealSense, OpenGL/GLX, GLU, GLFW, and OpenCV development files. Install the Ubuntu and NVIDIA Jetson packages on the Jetson; keep the JetPack NVIDIA repositories enabled so `libopencv-dev` resolves to the Jetson build rather than Ubuntu's older generic build.

```bash
sudo apt update
apt-cache policy libopencv-dev
sudo apt install -y \
	libgl-dev \
	libglx-dev \
	libopengl-dev \
	libglu1-mesa-dev \
	libglfw3-dev \
	libopencv-dev
```

Install or build librealsense on the Jetson using [RealSense_Jetson.md](RealSense_Jetson.md), then verify the installed target files:
```bash
dpkg-query -W libgl-dev libglx-dev libopengl-dev libglu1-mesa-dev libglfw3-dev libopencv-dev
pkg-config --modversion glfw3 opencv4 realsense2
readlink -e /usr/local/lib/librealsense2.so
file "$(readlink -e /usr/local/lib/librealsense2.so)"
```

CUDA 11.4 and TensorRT 8.5.2 are JetPack components, not host `pip` dependencies. They are needed only for the optional TensorRT inference target. Verify them on the Jetson with:
```bash
/usr/local/cuda-11.4/bin/nvcc --version
dpkg-query -W libnvinfer-dev libnvinfer-plugin-dev
test -f /usr/include/aarch64-linux-gnu/NvInfer.h
test -e /usr/lib/aarch64-linux-gnu/libnvinfer.so
test -e /usr/local/cuda-11.4/targets/aarch64-linux/lib/libcudart.so
```

The CMake toolchain in this repository cross-builds the default RealSense targets using the ARM64 sysroot. The optional TensorRT target also requires matching CUDA 11.4/TensorRT 8.5.2 development files in that sysroot and a target-aware CUDA runtime configuration; the host's CUDA installation is not a substitute.

4. Verify Native TensorRT Installation and nvcc paths
```
# Verify the installed TensorRT version
dpkg -l | grep nvinfer

# Check that the trtexec utility is present in the standard system path
ls -la /usr/src/tensorrt/samples/trtexec

# Append alias in ~/.bashrc  to to run trtexec and cuda from any terminal location on jetson
echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH" >> ~/.bashrc
echo "alias trtexec=/usr/src/tensorrt/bin/trtexec" >> ~/.bashrc

# Verify the alias is added and nvcc paths are present:
cat ~/.bashrc
...
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH 
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

6. External USB storage (EXT4 format) configuration (to store data, logs, git repos, python edge_env):
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
sudo chown -R $USER:$USER /mnt/usb  # change ownership to current jetson user

sudo blkid | grep sdX              # identify UUID of the device X:  
# example:  /dev/sda1: UUID="5e00f4cb-362a-4590-86ef-feaf3f3930cf" TYPE="ext4" PARTUUID="1132ab11-01"
# append line to /etc/fstab: UUID="5e00f4cb-362a-4590-86ef-feaf3f3930cf" /mnt/usb ext4 defaults,nofail  0 2 

sudo mount -a                      # mount all filesystems mentioned in fstab
```     
 
6. RealSense_Jetson.md:  RealSense SDK install and D435 camera sanity with steps in  
- A) Precompiled SDK librealsense2-utils and librealsense2-dev are installed.
- B) Building from Source  (needed for running inference on GPU, using opencv2, etc. ).

8. Clone tiger_watch repo
```
git clone git@github.com:ShonSat/tiger_watch.git 
```

9. Install Ultralytics software last. Or if you want to go without Ultralitics bloatware, skip to step 10.

- A) Jetson_Docker.md: docker image from https://github.com/ultralytics/ultralytics#docker

- B) manually by hand or use script. Note: takes 4GB space 
```
~/tiger_watch/jetson_YOLO_setup.sh
```

10.    
