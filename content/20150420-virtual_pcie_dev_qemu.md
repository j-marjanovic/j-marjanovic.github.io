Title: Virtual 
Date: 2015-04-20 19:00
Category: Projects
Tags: QEMU, Emulator, x86
Status: draft


Motivation
-----------
Why would anybody want to emulate a PCI express card in in an x86 emulator? Well,
there may be severl reasons for doing this. In my case, I want to see how 
(poorely documented) driver communicates with PCI express card. Another reason may
be to inpect how the closed source drivers work, but this may in some cases be
agains EULA. A third reasons which comes to my mind would be to simulate the system
with x86 (or some other arch) processor communicating with custom hardware. 
SystemVerilog (a languge to describe hardware) support the inclusion of functions,
written in C (this is called DPI). ALthough this will work, at least in my enviornment
would be easier and faster to buy a FPGA PCIe card and evalute the system in real world.



jan@jan-VirtualBox:~/QEMU/QEMU-src/qemu/bin/debug/native$ x86_64-softmmu/qemu-system-x86_64 -hda ../../../../../ubuntu.img -m 1024 -enable-kvm -device pci-mydev 
Could not access KVM kernel module: No such file or directory
failed to initialize KVM: No such file or directory


sudo apt-get install qemu-kvm

git://git.kiszka.org/kvm-kmod.git


Včeraj sem ostal:

jan@jan-VirtualBox:~/QEMU/QEMU-src/kvm-kmod$ less README 
jan@jan-VirtualBox:~/QEMU/QEMU-src/kvm-kmod$ git submodule init
Submodule 'linux' (http://git.kernel.org/pub/scm/virt/kvm/kvm.git) registered for path 'linux'
jan@jan-VirtualBox:~/QEMU/QEMU-src/kvm-kmod$ git submodule update
Cloning into 'linux'...
remote: Counting objects: 4138844, done.
remote: Compressing objects: 100% (767505/767505), done.
^Cceiving objects:   0% (15540/4138844), 6.88 MiB | 29.00 KiB/s
jan@jan-VirtualBox:~/QEMU/QEMU-src/kvm-kmod$ 





jan@jan-VirtualBox:~/QEMU/QEMU-src/kvm-kmod$ lsmod
Module                  Size  Used by
kvm                   452043  0 


Module opritons (Property)

http://lxr.free-electrons.com


 % ./x86_64-softmmu/qemu-system-x86_64 -hda ../../../../../images/ubuntu.img -m 1024 --enable-kvm -vga vmware -device pci-mydev,dev=0x1235


 % ./x86_64-softmmu/qemu-system-x86_64 -hda ../../../../../images/ubuntu.img -m 2048 --enable-kvm -vga vmware -smp 2 -device pci-mydev,bar=0:0x1000-2:0x100

