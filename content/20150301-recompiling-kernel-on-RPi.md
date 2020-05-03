Title: Compilation of Linux kernel for Raspberry Pi
Date: 2015-03-01 19:00
Category: Projects
Tags: Linux, Raspberry Pi


Yesterday I got my Raspberry Pi 2, the evolution of the legendary Raspberry Pi. 
The evolution is the right word to describe what has changed compared to 
the previous version. The processor it is now a quad-core, it runs faster,
it has got a newer instruction set (ARMv7) and the board now incorporates 1GB
of RAM and 4 USB connector. The RCA jack is no longer present, the additional
place is being occupied by a larger extension header instead. A welcomed update
of already great hardware, in my opinion (for people complaining that it
can't play 4K video, run desktop version of the Windows, ..., well, consider
buying proper computer, RPi was meant to be cheep enough to tinker with
without fear of breaking something).

I am the kind of the person which thinks that compiling Linux kernel would be 
great a way to spend the Sunday. Since one of my projects with RPi includes
custom driver for communication with FPGA, I needed Linux headers and _kbuild_
system for building kernel modules (those who are not familiar with the procedure,
imagine that you are building a program linked with libraries; in this case a 
program is a kernel module and kernel and its modules represent the libraries).

On the Ubuntu (and I think on other Debian systems but I am not 100% sure) you
can get kernel headers and source directly from the Debian repository, something
like:

	:::bash
	apt-get install linux-headers-$(uname -r)

The above command will install the headers the headers for the currently running 
kernel. It copies the header files to /usr/src and creates link in /lib/modules/,
this gives the user tools needed to compile kernel modules.


The hard way
-------------------

Before you continue reading I would just like to inform you that the procedure 
described in this section did not yield desired result. Although I managed to 
get a kernel image, the _kbuild_ system did not work. In Thomas Alva Edison style
 I want to present a method which does not work, but at least we know it does not work. The working (and easier) procedure is described in the next section.

Initially I wanted to get the headers in the same way as I would on Ubuntu, by
using apt (Advanced Packaging Tool). Searching for available packages did not
show the package needed (the Raspbian was running the 3.18.7-v7+ kernel).

	:::console
	pi@raspberrypi ~ $ sudo aptitude search linux-headers
	v   linux-headers                                   -                                                           
	p   linux-headers-3.10-3-all                        - All header files for Linux 3.10 (meta-package)            
	p   linux-headers-3.10-3-all-armhf                  - All header files for Linux 3.10 (meta-package)            
	p   linux-headers-3.10-3-common                     - Common header files for Linux 3.10-3                      
	p   linux-headers-3.10-3-rpi                        - Header files for Linux 3.10-3-rpi                         
	p   linux-headers-3.12-1-all                        - All header files for Linux 3.12 (meta-package)            
	p   linux-headers-3.12-1-all-armhf                  - All header files for Linux 3.12 (meta-package)            
	p   linux-headers-3.12-1-common                     - Common header files for Linux 3.12-1                      
	p   linux-headers-3.12-1-rpi                        - Header files for Linux 3.12-1-rpi                         
	p   linux-headers-3.18.0-trunk-all                  - All header files for Linux 3.18 (meta-package)            
	p   linux-headers-3.18.0-trunk-all-armhf            - All header files for Linux 3.18 (meta-package)            
	p   linux-headers-3.18.0-trunk-common               - Common header files for Linux 3.18.0-trunk                
	p   linux-headers-3.18.0-trunk-rpi                  - Header files for Linux 3.18.0-trunk-rpi                   
	p   linux-headers-3.18.0-trunk-rpi2                 - Header files for Linux 3.18.0-trunk-rpi2                  
	p   linux-headers-3.2.0-4-all                       - All header files for Linux 3.2 (meta-package)             
	p   linux-headers-3.2.0-4-all-armhf                 - All header files for Linux 3.2 (meta-package)             
	p   linux-headers-3.2.0-4-common                    - Common header files for Linux 3.2.0-4                     
	p   linux-headers-3.2.0-4-rpi                       - Header files for Linux 3.2.0-4-rpi                        
	p   linux-headers-3.6-trunk-all                     - All header files for Linux 3.6 (meta-package)             
	p   linux-headers-3.6-trunk-all-armhf               - All header files for Linux 3.6 (meta-package)             
	p   linux-headers-3.6-trunk-common                  - Common header files for Linux 3.6-trunk                   
	p   linux-headers-3.6-trunk-rpi                     - Header files for Linux 3.6-trunk-rpi                      
	p   linux-headers-rpi                               - Header files for Linux rpi configuration (meta-package)   
	p   linux-headers-rpi-rpfv                          - This metapackage will pull in the headers for the raspbian
	p   linux-headers-rpi2-rpfv                         - This metapackage will pull in the headers for the raspbian


I tried my luck with _linux-headers-rpi2-rpfv_ which installed headers for
kernel 3.18.0. That might sound close enough, but Linux refuses modules which
have not been compiled with exactly the same same kernel. 


So I decided to recompile the kernel on my laptop running Ubuntu. The procedure
of compiling on one type of machine (in this case Intel x86_64 processor) for
another (in this case ARM processor) is called cross-compilation.

The process of cross-compilation is described here: [Raspberry Pi Kernel Compilation](http://elinux.org/Raspberry_Pi_Kernel_Compilation)

Everything went fine, I got the kernel image and /lib/modules directory. The only
thing that the guide does not mention is that _make modules_install_ creates 
symbolic links to the original directory. I copied the entire kernel directory
to /usr/src and recreated symbolic links, so everything should be fine.

At this point if everything went OK we would have a working kernel and its 
_kbuild_ system which gives us the tools to compile the kernel modules out of the
tree (in a separate directory). The RPi boots up, which is a good sign, meaning
that there is nothing wrong with the kernel image. 

However, when I try to compile the kernel module, I get the error saying that 
there is a syntax error in script in kernel module 
(the same problem as described [here](http://stackoverflow.com/questions/17282461/scripts-recordmcount-syntax-error-when-i-try-to-build-a-linux-kernel-module-o). The answer by Joe C states:

>Anyway, if you cross compile you don't get a /usr/src/linux-header-x.x.x/scripts dir that's usable on your target system.


Since I previously downloaded another kernel headers from Debian repository,
I tired copying the scripts directory from there:

pi@raspberrypi /usr/src/linux-headers-3.18.0-trunk-rpi2 $ sudo cp -rv scripts/ ../linux-sources-3.18.8-v7+/

This fixed the compilation problem just to cause complete disaster when I
tried inserting the module. The following kernel message (_dmesg_ command)
shows nothing promising:

    :::
    [ 4246.164155] Unable to handle kernel paging request at virtual address fe220b30
	[ 4246.176292] pgd = b5dd8000
	[ 4246.183812] [fe220b30] *pgd=00000000
	[ 4246.192196] Internal error: Oops: 5 [#1] PREEMPT SMP ARM
	[ 4246.202324] Modules linked in: pi64_dev(O+) snd_bcm2835 snd_soc_pcm512x_i2c snd_soc_wm8804 snd_soc_pcm512x snd_soc_tas5713 regmap_spi regmap_i2c snd_soc_bcm2708_i2s regmap_mmio snd_soc_core snd_compress snd_pcm_dmaengine snd_pcm snd_seq snd_seq_device snd_timer r8712u(C) snd spi_bcm2708 i2c_bcm2708
	[ 4246.239611] CPU: 3 PID: 3468 Comm: insmod Tainted: G         C O   3.18.8-v7+ #1
	[ 4246.252306] task: b87aa840 ti: b760a000 task.ti: b760a000
	[ 4246.262985] PC is at load_module+0x1a64/0x1f0c
	[ 4246.272699] LR is at load_module+0x1a50/0x1f0c
	[ 4246.282373] pc : [<800940d4>]    lr : [<800940c0>]    psr: 90000013
	[ 4246.282373] sp : b760be88  ip : 7f110770  fp : b760bf44
	[ 4246.304401] r10: 00000000  r9 : 7f110600  r8 : 80536d44
	[ 4246.314883] r7 : b86dc8c4  r6 : fe220b1c  r5 : 7f11060c  r4 : b760bf48
	[ 4246.326685] r3 : 00000000  r2 : b760be70  r1 : b7555280  r0 : 807f2a3c
	[ 4246.338495] Flags: NzcV  IRQs on  FIQs on  Mode SVC_32  ISA ARM  Segment user
	[ 4246.350916] Control: 10c5387d  Table: 35dd806a  DAC: 00000015
	[ 4246.361932] Process insmod (pid: 3468, stack limit = 0xb760a238)
	[ 4246.373206] Stack: (0xb760be88 to 0xb760c000)
	[ 4246.382808] be80:                   7f11060c 00007fff 8009168c ffffffff b760bee4 bd949000
	[ 4246.396352] bea0: 00000000 7f11060c 00000000 b760bedc 807e4d78 7f110648 b760a000 7f110770
	[ 4246.409938] bec0: 00001f4b 806c9bdc ba7b961c b760a000 b9330000 808ab8fc 76fd3000 00000000
	[ 4246.423538] bee0: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
	[ 4246.437137] bf00: 00000000 00000000 00000000 00000000 00000000 00000000 00000080 00001f4b
	[ 4246.450707] bf20: 76fd3000 76f91948 00000080 8000f0a4 b760a000 00000000 b760bfa4 b760bf48
	[ 4246.464292] bf40: 80094664 8009267c bd949000 00001f4b bd949f3c bd949de3 bd94acc4 00000850
	[ 4246.477932] bf60: 00000940 00000000 00000000 00000000 0000001f 00000020 00000017 00000014
	[ 4246.491605] bf80: 00000010 00000000 00000000 7eb7861c 00000000 7768b038 00000000 b760bfa8
	[ 4246.505297] bfa0: 8000ee20 80094588 7eb7861c 00000000 76fd3000 00001f4b 76f91948 76fd3000
	[ 4246.519052] bfc0: 7eb7861c 00000000 7768b038 00000080 7768af80 00001f4b 76f91948 00000000
	[ 4246.532810] bfe0: 00000000 7eb785c4 76f88fb4 76ef3ab4 60000010 76fd3000 d466662e d5f7abd0
	[ 4246.546635] [<800940d4>] (load_module) from [<80094664>] (SyS_init_module+0xe8/0xfc)
	[ 4246.560087] [<80094664>] (SyS_init_module) from [<8000ee20>] (ret_fast_syscall+0x0/0x48)
	[ 4246.573935] Code: e51bc088 e15c0006 e2466008 0a000009 (e5963014) 
	[ 4246.604593] ---[ end trace 8e4bd0982f9f1fd0 ]---

It basically says that there was an error trying to access the wrong part of the
memory from the _insmod_ process.

At this point I decided to stop experimenting with this approach. I was getting
frustrated with constant fighting with all kind of errors. When I initially started
writing this blog post I wanted to describe the method to cross-compile Linux
kernel image and _kbuild_ build system. Unfortunately, although it may sound
appealing to speed up the process by cross compiling on x86 machine, the 
complication with various stuff make it more time consuming that compiling directly
on Raspberry Pi. I know myself good enough that I know I wont quit this easy.
I will probably return to this problem on some other occasion and tried again,
be assured that I will write a blog post If I succeed.


The easy way
-------------------

At the end I dropped the cross-compilation idea and resorted to compiling kernel
on the RPi itself. This can also serve as a performance test of the new RPi. 
I overclocked it to 1000MHz (using raspi-config I selected the RPi2 setting).

The compilation of kernel took something less than 2 hours, quite decent result
compared to 17 minutes it takes on my laptop with not-so-new i3 and 6GB of RAM.

The following figure shows the temperature during the compilation. The temperature
was captured every minute with a Cron job which read from 
**/sys/class/thermal/thermal_zone0/temp**

![RPi temperature]({static}/images/pi_temp_during_compile.png)
{: style="width:90%; display: block; margin-left: auto; margin-right: auto;"}


Finally, using freshly compiled kernel on RPi, I managed to get compile my 
module and to load it in kernel (debug message from kernel):

	:::console
	[   38.324756] ============================================
	[   38.324786]        Pi64 driver by Jan Marjanovic        
	[   38.324796] 
	[   38.324808]   built: Mar  1 2015 11:38:10
	[   38.324818] ============================================



