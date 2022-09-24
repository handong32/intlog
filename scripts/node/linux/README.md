# Scripts for running nodejs webserver in Linux

## Hardware Setup
We assume the following IP address mappings in `nodejs_bench.py`, connected together via VLAN:
```
NodeJS Webserver -> 192.168.1.9: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
wrk client -> 192.168.1.11: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
```

## Software Setup
NodeJS Webserver: `https://nodejs.org/ko/blog/release/v0.10.26/`

wrk client: `https://github.com/wg/wrk`

## Example nodejs_bench.py run:
```
$ python nodejs_bench.py --help
usage: nodejs_bench.py [-h] [--rapl RAPL] [--dvfs DVFS] [--com COM] [--itr ITR] [--nrepeat NREPEAT]

optional arguments:
  -h, --help         show this help message and exit
  --rapl RAPL        Rapl power limit [46, 136]
  --dvfs DVFS        Cpu frequency [0x1D00 ... 0xC00]
  --com COM          com1 == -t1 -c1, com512 == -t16 -c512, com1_1024 == 1024 bytes
  --itr ITR          Static interrupt delay [10, 1000]
  --nrepeat NREPEAT  repeat value

```

## Use run_nodejs.sh to automate multi-configuration runs
```
MDVFS="0x1d00 0x1b00 0x1900 0x1700 0x1500 0x1300 0x1100 0xf00 0xd00" ITRS="2 4" MRAPl="135" NITERS="1"  ./run_nodejs.sh run
```

## Generate summary dataset from detailed log traces

##### Requirements
```
Numpy
Pandas
Python3
```

##### Example: run_nodejs.sh will automatically create a <data_folder> to store all trace logs
```
python clean_linux.py <data_folder>
```
