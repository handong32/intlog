# Building Linux kernel 5.5 and instrumenting `intLog` tracing framework

## Linux configuration file
We use a specially modified `.config` to build Linux kernel that was optimized for performance, details based off study [here](https://github.com/LinuxPerfStudy/LEBench).

## First, build the Linux kernel image `bzImage` (can be booted with pxeboot/grub), sample output of successful build below:
```
$ cd linux/ 
$ make -j bzImage
...
..
.
Setup is 16220 bytes (padded to 16384 bytes).
System is 8901 kB
CRC 66a5975b
Kernel: arch/x86/boot/bzImage is ready  (#24)
```

## Build ixgbe device driver with `intLog` instrumented to capture fine-grained logs:
```
$ make drivers/net/ethernet/intel/ixgbe/ixgbe.ko
  CALL    scripts/checksyscalls.sh
  CALL    scripts/atomic/check-atomics.sh
  DESCEND  objtool
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_main.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_common.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_ethtool.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_82599.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_82598.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_phy.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_sriov.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_mbx.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_x540.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_x550.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_lib.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_ptp.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_xsk.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_sysfs.o
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe_debugfs.o
  LD [M]  drivers/net/ethernet/intel/ixgbe/ixgbe.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC [M]  drivers/net/ethernet/intel/ixgbe/ixgbe.mod.o
  LD [M]  drivers/net/ethernet/intel/ixgbe/ixgbe.ko

$ modinfo drivers/net/ethernet/intel/ixgbe/ixgbe.ko
filename:       /root/linux/drivers/net/ethernet/intel/ixgbe/ixgbe.ko
version:        5.1.0-k
license:        GPL v2
description:    Intel(R) 10 Gigabit PCI Express Network Driver
author:         Intel Corporation, <linux.nics@intel.com>
srcversion:     209765DB761432A694DEA13
alias:          pci:v00008086d000015E5sv*sd*bc*sc*i*
alias:          pci:v00008086d000015E4sv*sd*bc*sc*i*
alias:          pci:v00008086d000015CEsv*sd*bc*sc*i*
alias:          pci:v00008086d000015C8sv*sd*bc*sc*i*
alias:          pci:v00008086d000015C7sv*sd*bc*sc*i*
alias:          pci:v00008086d000015C6sv*sd*bc*sc*i*
alias:          pci:v00008086d000015C4sv*sd*bc*sc*i*
alias:          pci:v00008086d000015C3sv*sd*bc*sc*i*
alias:          pci:v00008086d000015C2sv*sd*bc*sc*i*
alias:          pci:v00008086d000015AEsv*sd*bc*sc*i*
alias:          pci:v00008086d000015ACsv*sd*bc*sc*i*
alias:          pci:v00008086d000015ADsv*sd*bc*sc*i*
alias:          pci:v00008086d000015ABsv*sd*bc*sc*i*
alias:          pci:v00008086d000015B0sv*sd*bc*sc*i*
alias:          pci:v00008086d000015AAsv*sd*bc*sc*i*
alias:          pci:v00008086d000015D1sv*sd*bc*sc*i*
alias:          pci:v00008086d00001563sv*sd*bc*sc*i*
alias:          pci:v00008086d00001560sv*sd*bc*sc*i*
alias:          pci:v00008086d0000154Asv*sd*bc*sc*i*
alias:          pci:v00008086d00001557sv*sd*bc*sc*i*
alias:          pci:v00008086d00001558sv*sd*bc*sc*i*
alias:          pci:v00008086d0000154Fsv*sd*bc*sc*i*
alias:          pci:v00008086d0000154Dsv*sd*bc*sc*i*
alias:          pci:v00008086d00001528sv*sd*bc*sc*i*
alias:          pci:v00008086d000010F8sv*sd*bc*sc*i*
alias:          pci:v00008086d0000151Csv*sd*bc*sc*i*
alias:          pci:v00008086d00001529sv*sd*bc*sc*i*
alias:          pci:v00008086d0000152Asv*sd*bc*sc*i*
alias:          pci:v00008086d000010F9sv*sd*bc*sc*i*
alias:          pci:v00008086d00001514sv*sd*bc*sc*i*
alias:          pci:v00008086d00001507sv*sd*bc*sc*i*
alias:          pci:v00008086d000010FBsv*sd*bc*sc*i*
alias:          pci:v00008086d00001517sv*sd*bc*sc*i*
alias:          pci:v00008086d000010FCsv*sd*bc*sc*i*
alias:          pci:v00008086d000010F7sv*sd*bc*sc*i*
alias:          pci:v00008086d00001508sv*sd*bc*sc*i*
alias:          pci:v00008086d000010DBsv*sd*bc*sc*i*
alias:          pci:v00008086d000010F4sv*sd*bc*sc*i*
alias:          pci:v00008086d000010E1sv*sd*bc*sc*i*
alias:          pci:v00008086d000010F1sv*sd*bc*sc*i*
alias:          pci:v00008086d000010ECsv*sd*bc*sc*i*
alias:          pci:v00008086d000010DDsv*sd*bc*sc*i*
alias:          pci:v00008086d0000150Bsv*sd*bc*sc*i*
alias:          pci:v00008086d000010C8sv*sd*bc*sc*i*
alias:          pci:v00008086d000010C7sv*sd*bc*sc*i*
alias:          pci:v00008086d000010C6sv*sd*bc*sc*i*
alias:          pci:v00008086d000010B6sv*sd*bc*sc*i*
depends:
intree:         Y
name:           ixgbe
vermagic:       5.5.0+ SMP mod_unload
parm:           allow_unsupported_sfp:Allow unsupported and untested SFP+ modules on 82599-based adapters (uint)
parm:           debug:Debug level (0=none,...,16=all) (int)


```

## Loading `ixgbe.ko` kernel module
Can use `insmod` to dynamically load `ixgbe.ko` into the kernel OR configure kernel to automatically load `ixgbe.ko`: `$insmod drivers/net/ethernet/intel/ixgbe/ixgbe.ko`. After loading, use `dmesg` to check output:

```
$ dmesg
[   18.235902] Successfully loaded /proc/ixgbe_stats/
[   18.246126] ip (253) used greatest stack depth: 13928 bytes left
[   18.292983] ip (273) used greatest stack depth: 13816 bytes left
[   18.301130] ixgbe_open()
[   18.303935] cpuidle stats state_count=6
[   18.308316] i=0 name=POLL exit_latency=0 target_residency=0
[   18.314642] i=1 name=C1 exit_latency=2 target_residency=2
[   18.320768] i=2 name=C1E exit_latency=10 target_residency=20
[   18.327185] i=3 name=C3 exit_latency=80 target_residency=211
[   18.333606] i=4 name=C6 exit_latency=104 target_residency=345
[   18.340123] i=5 name=C7 exit_latency=109 target_residency=345
[   18.348473] 0 vmalloc size=112000000 addr=(____ptrval____)
[   18.383078] 1 vmalloc size=112000000 addr=(____ptrval____)
[   18.417171] 2 vmalloc size=112000000 addr=(____ptrval____)
[   18.451308] 3 vmalloc size=112000000 addr=(____ptrval____)
[   18.485445] 4 vmalloc size=112000000 addr=(____ptrval____)
[   18.519611] 5 vmalloc size=112000000 addr=(____ptrval____)
[   18.553886] 6 vmalloc size=112000000 addr=(____ptrval____)
[   18.587973] 7 vmalloc size=112000000 addr=(____ptrval____)
[   18.622258] 8 vmalloc size=112000000 addr=(____ptrval____)
[   18.656346] 9 vmalloc size=112000000 addr=(____ptrval____)
[   18.690673] 10 vmalloc size=112000000 addr=(____ptrval____)
[   18.724730] 11 vmalloc size=112000000 addr=(____ptrval____)
[   18.758962] 12 vmalloc size=112000000 addr=(____ptrval____)
[   18.792864] 13 vmalloc size=112000000 addr=(____ptrval____)
[   18.826813] 14 vmalloc size=112000000 addr=(____ptrval____)
[   18.860441] 15 vmalloc size=112000000 addr=(____ptrval____)
[   18.892230] +++++ ixgbe_open tsc_khz = 2899999 now=727940214204 tsc=727940214204 ++++++
[   18.967656] ixgbe_request_msix_irqs vector=0
[   18.971122] ixgbe_request_msix_irqs vector=1
[   18.974556] ixgbe_request_msix_irqs vector=2
[   18.977985] ixgbe_request_msix_irqs vector=3
[   18.981418] ixgbe_request_msix_irqs vector=4
[   18.984857] ixgbe_request_msix_irqs vector=5
[   18.988289] ixgbe_request_msix_irqs vector=6
[   18.991719] ixgbe_request_msix_irqs vector=7
[   18.995147] ixgbe_request_msix_irqs vector=8
[   18.998584] ixgbe_request_msix_irqs vector=9
[   19.002015] ixgbe_request_msix_irqs vector=10
[   19.005541] ixgbe_request_msix_irqs vector=11
[   19.009068] ixgbe_request_msix_irqs vector=12
[   19.012594] ixgbe_request_msix_irqs vector=13
[   19.016126] ixgbe_request_msix_irqs vector=14
[   19.019652] ixgbe_request_msix_irqs vector=15
```

## Accessing `/proc/ixgbe_stats` logs
Once the `ixgbe.ko` kernel module has been inserted, it creates entries in `procfs`. Example:

```
$ cat /proc/ixgbe_stats/core/0
0 0 0 2 66 796328503066 4659393906693 11244259868274 10094371629 0 0 0 0 0 0 3647352166 7422520693157768
1 0 0 2 66 796627595348 4659805444067 11245254416981 10094909064 0 0 0 0 0 0 3647834313 7422521693656626
2 0 0 2 66 796857485218 4660153788936 11246096250615 10095275010 0 0 0 0 0 0 3648218489 7422522541532334
3 1 60 0 0 796999664261 4660356185023 11246585374475 10095525176 0 0 0 0 0 0 3648448786 7422523030886744
....
....

$ cat /proc/ixgbe_stats/core/1
0 0 0 3 102 812503139713 3802899911944 9180714539673 7965524108 0 0 0 0 0 0 3648448786 7422523030895618
1 0 0 0 0 812762435450 3803093056564 9181181306418 7965788938 0 0 0 0 0 0 3648960690 7422524144156965
2 0 0 2 66 813012948163 3803257639823 9181579049306 7966048208 0 0 0 0 0 0 3649147982 7422524541899688
3 1 74 0 0 0 0 0 0 0 0 0 0 0 0 0 7422524542104961
4 0 0 2 74 0 0 0 0 0 0 0 0 0 0 0 7422524542288230
5 1 66 0 0 0 0 0 0 0 0 0 0 0 0 0 7422524544546915
6 1 87 0 0 0 0 0 0 0 0 0 0 0 0 0 7422524544631238
7 0 0 2 66 813039044911 3803274442994 9181619656962 7966076424 0 0 0 0 0 0 3649167883 7422524582507828
8 1 66 0 0 0 0 0 0 0 0 0 0 0 0 0 7422524584107323
9 1 1458 0 0 0 0 0 0 0 0 0 0 0 0 0 7422524584176923
```
##### `ixgbe_stats` data layout:

**num**|RXdescriptor|RXbytes|TXdescriptor|TXbytes|Instructions|Cycles|Ref\_Cycles|LLC\_miss|c1|c1e|c3|c6|c7|Joules|RdtscTimestamp
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
```
num: current line entry in trace log
RXdescriptor (Receive Descriptor): A data structure that points to memory location of received packet and other packet info such as length, etc.
RXbytes (Receive Bytes): Number of bytes received
TXdescriptor (Transmit Descriptor): A data structure that points to memory location of transmitted packet and other packet info such as length, etc.
RXbytes (Transmit Bytes): Number of bytes transmitted
Instructions: number of instructions used
Cycles: number of CPU cycles, is impacted by different CPU frequency changes
Ref_Cycles: number of CPU cycles, is NOT impacted by different CPU frequency changes, counts at fixed rate
LLC_Miss: last-level cache miss
c1, c1e, c3, c6, c7: number of different sleep states
Joules: energy used from reading RAPL MSR
RdtscTimestamp: per-core timestamp of when log entry was taken
```

## GRUB configuration
To boot linux with its DVFS frequency governor disabled in order to *static* set DVFS, append the following line to your grub: `intel_pstate=disable cpufreq.off=1`

Note: Depending on your kernel version and Linux flavor, DVFS may be disabled from userspace

## NIC level logging and kernel module
The `ixgbe` device driver changes to instrument logging in the NIC can be found at:
```
linux/drivers/net/ethernet/intel/ixgbe/ixgbe_main.c
linux/drivers/net/ethernet/intel/ixgbe/ixgbe.h
```

`IXGBE_LOG_SIZE` in `ixgbe.h` is hard-coded to limit amount of memory is used to store the traces. The function for collecting traces is found at `ixgbe_msix_clean_rings` in `ixgbe_main.c`.


