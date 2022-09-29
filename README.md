# intLog: A Framework for Network-Centric ML-Systems Datasets

A software-agnostic logging framework that exposes hardware-level controls which can impact network-driven behavior. It is currently integrated with [Linux 5.5](https://github.com/handong32/linux/tree/intlog) and a baremetal library OS, [EbbRT](https://github.com/SESA/EbbRT). It instrumented fine-grained log collect at the network device interrupt layer and uses architecture specific performance monitoring units to store hardware metrics such as *instructions, cache-misses, energy use* and software metrics such as *bytes received and transmitted*. 

> So far, only tested and gathered experimental results for a machine with the following specifications: `Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB RAM, Intel(R) 10 Gigabit Network Connection`. Modifications for other architectures/network cards may be required to correctly read specific hardware counters.

## Overview
- `ebbrt`: Contains link to baremetal EbbRT and instructions for building EbbRT. EbbRT's ixgbe device driver already has `intLog` integrated with it.
- `linux`: Contains link to Linux 5.14 and instructions for building kernel and `ixgbe.ko` kernel module that has `intLog` integrated.
- `scripts`: Contains experimental scripts for four applications in our experimental study
  - `netpipe`: A simple ping-pong application for fixed sized messages
    - ebbrt: `EbbRT` implementation of `netpipe` and scripts to run
    - linux: `Linux` implementation of `netpipe` and scripts to run
  - `nodejs`: A HTTP web server running in NodeJS
    - ebbrt: `EbbRT` implementation of `nodejs` and scripts to run
    - linux: `Linux` implementation of `nodejs` and scripts to run
  - `mcd`: memcached
    - ebbrt: `EbbRT` implementation of `memached` and scripts to run
    - linux: `Linux` implementation of `memcached` and scripts to run
  - `mcdsilo`: memcached with a transcational database (Silo)
    - ebbrt: `EbbRT` implementation of `memcached-silo` and scripts to run
    - linux: `Linux` implementation of `memcached-silo` and scripts to run
- `tools`: Utilities and other guides for how to boot various OSes

## Dataset
We have collected over 4 TB of data from our experimental study, in the processof sanitizing and will post link to download
