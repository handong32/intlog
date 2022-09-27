# Scripts for running memcached in EbbRT

## Hardware Setup
We assume the following IP address mappings in `mutilate_bench.py`, connected together via VLAN:
```
memcached server -> 192.168.1.9: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate client -> 192.168.1.11: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate agent -> 192.168.1.37: Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz, 126 GB, Intel(R) 10 Gigabit Network Connectio
mutilate agent -> 192.168.1.38: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connectio
mutilate agent -> 192.168.1.104: Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate agent -> 192.168.1.106: Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate agent -> 192.168.1.107: Intel(R) Xeon(R) CPU E5-2650 v2 @ 2.60GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
```

## Software Setup
memccached server: `https://github.com/handong32/EbbRT-memcached`

mutilate: `https://github.com/ix-project/mutilate`


## Details of files

`mutilate_bench.py`: Python wrapper to run `mutilate` benchmark against EbbRT-memcached

`run_mcd.sh`: shell script wrapper to automate configurations of ITR, DVFS, RAPL for `mutilate_bench.py` 

`parse_ebbrt_mcd.c`: converts trace log from EbbRT binary into readable format

`clean_mcd_ebbrt.py`: cleans up trace log to reveal energy and timestamp information

## Use run_mcd.sh to automate multi-configuration runs
```
MQPS="200000 400000 600000" MDVFS="0x1d00 0x1b00 0x1900" ITRS="50 100 200 250 300 350 400" MRAPl="135" NITERS="1"  ./run_mcd.sh runEbbRT
```
