# Building Linux kernel 5.5

## Configuration file
Modified for performance based off study [here](https://github.com/LinuxPerfStudy/LEBench)

## Build the bootable `bzImage`
```
$ make -j bzImage
$ ...
$ ...
$ ...
Setup is 16220 bytes (padded to 16384 bytes).
System is 8901 kB
CRC 66a5975b
Kernel: arch/x86/boot/bzImage is ready  (#24)
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
