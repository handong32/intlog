## Building EbbRT

##### Follow steps from: https://github.com/SESA/EbbRT/wiki/Build-Tutorial-(DRAFT)

1) Build `sysroot_ebbrt`
```
## setup directories
$ mkdir ~\sysroot_ebbrt\
$ mkdir ~\sysroot_ebbrt\build
$ mkdir ~\sysroot_ebbrt\native

## build ebbrt sysroot
$ cd ~\sysroot_ebbrt\build && make -j16 -f ~/EbbRT/toolchain/Makefile SYSROOT=~/sysroot_ebbrt/native/
```

## Hardware (9/27/2022)
For historical purposes, the following OS and hardware was used to build EbbRT:
```
32-Core AMD Opteron(TM) Processor 6272, 62 GB RAM

$ uname -a
Linux 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

$ gcc --version
gcc (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609
Copyright (C) 2015 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.2 LTS"

$ lspci
00:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD/ATI] RD890 Northbridge only dual slot (2x16) PCI-e GFX Hydra part (rev 02)
00:03.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] RD890 PCI to PCI bridge (PCI express gpp port C)
00:04.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] RD890 PCI to PCI bridge (PCI express gpp port D)
00:0d.0 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] RD890 PCI to PCI bridge (external gfx1 port B)
00:11.0 SATA controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 SATA Controller [IDE mode]
00:12.0 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 USB OHCI0 Controller
00:12.1 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0 USB OHCI1 Controller
00:12.2 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 USB EHCI Controller
00:13.0 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 USB OHCI0 Controller
00:13.1 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0 USB OHCI1 Controller
00:13.2 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 USB EHCI Controller
00:14.0 SMBus: Advanced Micro Devices, Inc. [AMD/ATI] SBx00 SMBus Controller (rev 3d)
00:14.1 IDE interface: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 IDE Controller
00:14.3 ISA bridge: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 LPC host controller
00:14.4 PCI bridge: Advanced Micro Devices, Inc. [AMD/ATI] SBx00 PCI to PCI Bridge
00:14.5 USB controller: Advanced Micro Devices, Inc. [AMD/ATI] SB7x0/SB8x0/SB9x0 USB OHCI2 Controller
00:18.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 0
00:18.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 1
00:18.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 2
00:18.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 3
00:18.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 4
00:18.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 5
00:19.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 0
00:19.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 1
00:19.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 2
00:19.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 3
00:19.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 4
00:19.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 5
00:1a.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 0
00:1a.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 1
00:1a.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 2
00:1a.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 3
00:1a.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 4
00:1a.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 5
00:1b.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 0
00:1b.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 1
00:1b.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 2
00:1b.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 3
00:1b.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 4
00:1b.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Family 15h Processor Function 5
02:00.0 Ethernet controller: Intel Corporation 82576 Gigabit Network Connection (rev 01)
02:00.1 Ethernet controller: Intel Corporation 82576 Gigabit Network Connection (rev 01)
03:00.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
03:00.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
04:00.0 VGA compatible controller: NVIDIA Corporation GT218 [GeForce 210] (rev a2)
04:00.1 Audio device: NVIDIA Corporation High Definition Audio Controller (rev a1)
40:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD/ATI] RD890 Northbridge only dual slot (2x16) PCI-e GFX Hydra part (rev 02)
```
