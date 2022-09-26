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
