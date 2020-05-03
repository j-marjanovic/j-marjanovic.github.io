

# New layer
https://www.yoctoproject.org/docs/2.4/dev-manual/dev-manual.html#creating-a-general-layer-using-the-bitbake-layers-script

```
bitbake-layers create-layer gzip-acc
```

Add layer in `build/conf/bblayers.conf`


# Memory for DMA

https://forums.xilinx.com/t5/Embedded-Linux/User-space-drivers-and-contiguous-memory-buffers-for-PL/td-p/795836

https://github.com/ikwzm/udmabuf

https://github.com/ikwzm/ZynqMP-FPGA-Linux-Example-2-UltraZed

## compilation

https://www.yoctoproject.org/docs/2.4/kernel-dev/kernel-dev.html#working-with-out-of-tree-modules

> you might want to override the do_compile() step, or create a patch to the
> Makefile to work with the more typical KERNEL_SRC or KERNEL_PATH variables

since modules_install is missing, patching the Makefile is necessary


# HDF (hardware)

https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/59605045/Adding+an+HDF+to+a+Xilinx+Yocto+Layer

TODO: copy from HDF




# tftp server

$ cat /etc/default/atftpd
USE_INETD=false
# OPTIONS below are used only with init script
OPTIONS="--tftpd-timeout 300 --retry-timeout 5 --mcast-port 1758 --mcast-addr 239.239.239.0-255 --mcast-ttl 1 --maxthread 100 --verbose=5 --bind 192.168.1.149 /srv/tftp"

# initramfs

https://rocketboards.org/foswiki/Documentation/BuildingInitramfsForSimpleNetworkBoot

could not get initramfs embeeded in image, was getting the "dependency loop" error when
I set INITRAMFS_IMAGE

# NFS

as an option, easier with initramfs

https://www.denx.de/wiki/view/DULG/LinuxNfsRoot

https://community.nxp.com/docs/DOC-103717

>  untar the {IMAGE}.bz2 in an exported folder keeping using sudoand keeping the chmod of each file.

```
sudo mkdir -p /srv/nfs
sudo tar xvf tmp/deploy/images/zcu102-zynqmp/petalinux-image-minimal-zcu102-zynqmp.tar.gz -C /srv/nfs
```

https://help.ubuntu.com/stable/serverguide/network-file-system.html
https://help.ubuntu.com/community/SettingUpNFSHowTo

## client side testing

https://suneilrai.wordpress.com/2015/10/01/nfs-server-address-does-not-match-proto-option/

```
sudo apt install nfs common
```

## server side debugging

https://serverfault.com/a/107985

# build

```
bitbake petalinux-image-minimal
```

# deploy

## boot partition

scp tmp/deploy/images/zcu102-zynqmp/BOOT-zcu102-zynqmp.bin root@eval-kit-zcu102:/mnt/boot/BOOT.bin
scp tmp/deploy/images/zcu102-zynqmp/uEnv.txt root@eval-kit-zcu102:/mnt/boot/
ssh root@eval-kit-zcu102 -C "sync"


## TFTP

cp tmp/deploy/images/zcu102-zynqmp/zcu102-zynqmp-system.dtb /srv/tftp
cp tmp/deploy/images/zcu102-zynqmp/Image /srv/tftp

# run

machine_name=zcu102-zynqmp
ethaddr=00:0a:35:04:99:f3
kernel_image=Image
kernel_load_address=0x80000
devicetree_image=Image-zynqmp-zcu102-rev1.0.dtb
devicetree_load_address=0x4000000
bootargs=earlycon clk_ignore_unused root=/dev/nfs rw rootwait nfsroot=192.168.1.149:/srv/nfs ip=192.168.1.220:192.168.1.149::255.255.0.0:eval-kit-zcu102::off
loadkernel=fatload mmc 0 ${kernel_load_address} ${kernel_image}
loaddtb=fatload mmc 0 ${devicetree_load_address} ${devicetree_image}
bootkernel=run loadkernel && run loaddtb && booti ${kernel_load_address} - ${devicetree_load_address}
uenvcmd=run bootkernel

# u-boot configuration

false (not relevant anymore):
https://forums.xilinx.com/t5/Embedded-Linux/Yocto-getting-to-u-boot-menuconfig/td-p/758684

works:
bitbake u-boot-xlnx -c menuconfig

## terminal over SSH

https://unix.stackexchange.com/questions/297362/yocto-bitbake-does-not-start-menuconfig
xxxxxxxxxxxxx`x x`xxxx