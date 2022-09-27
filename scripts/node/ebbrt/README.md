# Scripts for running nodejs webserver in EbbRT

## Hardware Setup
We assume the following IP address mappings in `nodejs_bench.py`, connected together via VLAN:
```
NodeJS Webserver -> 192.168.1.200: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
wrk client -> 192.168.1.11: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
```

## Software Setup
NodeJS Webserver: `https://github.com/handong32/EbbRT-node`

wrk client: `https://github.com/wg/wrk`

## Details of files

`nodejs_bench.py`: Python wrapper to run `wrk` benchmark against EbbRT-nodejs Webserver

`run_nodejs.sh`: shell script wrapper to automate configurations of ITR, DVFS, RAPL for `nodejs_bench.py` 

`parse_ebbrt_nodejs.c`: converts trace log from EbbRT binary into readable format

`clean_nodejs_ebbrt.py`: cleans up trace log to reveal energy and timestamp information
