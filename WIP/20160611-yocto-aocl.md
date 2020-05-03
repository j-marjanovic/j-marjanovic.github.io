

copied the files from here:
/home/jan/altera/16.0/hld/host/arm32


root@cyclone5:~/bin# strace ./aocl

returns:

lstat64("/home/root/bin/aocl", {st_mode=S_IFREG|0755, st_size=28522, ...}) = 0
stat64("/home/root/bin/share", 0xbea94a70) = -1 ENOENT (No such file or directory)
stat64("/home/root/share", 0xbea94a70)  = -1 ENOENT (No such file or directory)
stat64("/home/share", 0xbea94a70)       = -1 ENOENT (No such file or directory)
stat64("/share", 0xbea94a70)            = -1 ENOENT (No such file or directory)
fstat64(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(4, 64), ...}) = 0
ioctl(1, TCGETS, {B115200 opost isig icanon echo ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb6fd9000
write(1, "aocl: Unable to determine the ex"..., 98aocl: Unable to determine the execution environment of the Altera Runtime Environment for OpenCL.
) = 98
write(1, "aocl:     Detailed error: Could "..., 107aocl:     Detailed error: Could not find root directory for the SDK:  could not find the 'share' directory
) = 107
exit_group(1)                           = ?
+++ exited with 1 +++


Terasic proviedes rootfs, lets investiaget what is in there


➜  share pwd                                                                   
/media/jan/eb671067-6070-409c-88e5-68908046e7b4/usr/share
➜  share l                                                                     
total 404K
drwxr-xr-x 13 root root 4,0K apr 16  2014 .
drwxr-xr-x 12 root root 4,0K apr 16  2014 ..
drwxr-xr-x  7 root root 4,0K apr 16  2014 autoconf
drwxr-xr-x  2 root root 4,0K apr 16  2014 awk
drwxr-xr-x  2 root root 4,0K apr 16  2014 dict
drwxr-xr-x  4 root root 4,0K apr 16  2014 gdb
drwxr-xr-x  2 root root 4,0K apr 16  2014 gnu-config
drwxr-xr-x  2 root root 4,0K apr 16  2014 info
drwxr-xr-x  2 root root 4,0K apr 16  2014 man
drwxr-xr-x  2 root root 4,0K apr 16  2014 misc
drwxr-xr-x 12 root root 4,0K apr 16  2014 oprofile
-rw-r--r--  1 root root 190K apr 16  2014 pci.ids.gz
drwxr-xr-x  2 root root 4,0K apr 16  2014 readline
drwxr-xr-x  2 root root 4,0K apr 16  2014 udhcpc
-rw-r--r--  1 root root 160K apr 16  2014 usb.ids.gz


Ok, create share directory in home dir


final:
root@cyclone5:~/host/arm32# ls
bin    lib    share



root@cyclone5:~# aocl diagnose /dev/acl0 
aocl diagnose: Running diagnostic from /home/root/opencl_arm32_rte/board/c5soc/arm32/bin

Verified that the kernel mode driver is installed on the host machine.


MMD ERROR: Kernel driver version is 16.0.. Expected version 14.0
Using platform: Altera SDK for OpenCL


