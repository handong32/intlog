# Scripts for running memcached-silo in Linux

## Hardware Setup
We assume the following IP address mappings in `silo_bench.py`, connected together via VLAN:
```
mcdsilo server -> 192.168.1.9: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate client -> 192.168.1.11: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
mutilate agent -> 192.168.1.37: Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz, 126 GB, Intel(R) 10 Gigabit Network Connectio
mutilate agent -> 192.168.1.38: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connectio
```

## Software Setup
mcdsilo linux server: `https://github.com/ix-project/servers`

mutilate: `https://github.com/ix-project/mutilate`

## Example silo_bench.py run:
```
$ python3 -u silo --help
usage: silo_bench.py [-h] [--rapl RAPL] [--itr ITR] [--dvfs DVFS]
                         [--nrepeat NREPEAT] [--qps QPS] [--time TIME]
                         [--ring RING] [--dtxmx DTXMX] [--dca DCA]
                         [--thresh THRESH] [--type TYPE] [--verbose VERBOSE]

optional arguments:
  -h, --help         show this help message and exit
  --rapl RAPL        Rapl power limit [35, 135]
  --itr ITR          Static interrupt delay [10, 500]
  --dvfs DVFS        DVFS value [0xc00 - 0x1d00]
  --nrepeat NREPEAT  repeat value
  --qps QPS          RPS rate
  --time TIME        Time in seconds to run
  --ring RING        TX and RX ring
  --dtxmx DTXMX      DTXMXSZRQ
  --dca DCA          DCA
  --thresh THRESH    PTHRESH, HTHRESH, WTHRESH
  --type TYPE        Workload type [etc, usr]
  --verbose VERBOSE  Print mcdsilo raw stats
  
$ python3 -u silo_bench.py --qps 100000 --time 20 --itr 2 --rapl 135 --dvfs 0x1d00 --nrepeat 0
```

## Use run_silo.sh to automate multi-configuration runs
```
MQPS="200000 400000 600000" MDVFS="0x1d00 0x1b00 0x1900 0x1700 0x1500 0x1300 0x1100 0xf00 0xd00" ITRS="50 100 200 250 300 350 400" MRAPl="135 75 55" NITERS="1"  ./run_silo.sh run
```

## Generate summary dataset from detailed log traces

##### Requirements
```
Numpy
Pandas
Python3
```

##### Example: run_silo.sh will automatically create a <data_folder> to store all trace logs
```
python clean_mcdsilo_linux.py <data_folder>
```
