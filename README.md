# intLog: A Framework for Network-Centric ML-Systems Datasets

A software-agnostic logging framework that exposes hardware-level controls which can impact network-driven behavior. It is currently integrated with [Linux 5.14](https://github.com/handong32/linux/tree/intlog) and a baremetal library OS, [EbbRT](https://github.com/SESA/EbbRT). It instrumented fine-grained log collect at the network device interrupt layer and uses architecture specific performance monitoring units to store hardware metrics such as *instructions, cache-misses, energy use* and software metrics such as *bytes received and transmitted*. 

> So far, only tested and gathered experimental results for a machine with the following specifications: `Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB RAM, Intel(R) 10 Gigabit Network Connection`. Modifications for other architectures/network cards may be required to correctly read specific hardware counters.
