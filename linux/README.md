# Building Linux kernel 5.5

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

Use insmod to dynamically load ixgbe.ko into the kernel OR configure kernel to automatically load ixgbe
$ insmod drivers/net/ethernet/intel/ixgbe/ixgbe.ko
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

## Accessing trace logs
Once the `ixgbe` kernel module has been inserted, it creates entries in `procfs`:

```
$ cat /proc/ixgbe_stats/core/0
$ cat /proc/ixgbe_stats/core/1
....
....
$ cat /proc/ixgbe_stats/core/N
```
