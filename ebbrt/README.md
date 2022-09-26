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
