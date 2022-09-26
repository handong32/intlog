# Building Linux kernel 5.5

## Configuration file
Modified for performance based off study [here](https://github.com/LinuxPerfStudy/LEBench)

## Build the bootable `bzImage`
`
$ make -j bzImage
`
## GRUB configuration
To boot linux with its DVFS frequency governor disabled in order to *static* set DVFS, append the following line to your grub: `intel_pstate=disable cpufreq.off=1`

Note: Depending on your kernel version and Linux flavor, DVFS may be disabled from userspace

## NIC level logging
The `ixgbe` device driver changes to instrument logging in the NIC can be found at:
```
linux/drivers/net/ethernet/intel/ixgbe/ixgbe_main.c
linux/drivers/net/ethernet/intel/ixgbe/ixgbe.h
```

`IXGBE_LOG_SIZE` is hard-coded to limit amount of memory is used to store the traces. The function for collecting traces is found at `ixgbe_msix_clean_rings`.

