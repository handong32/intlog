# Scripts for running NetPIPE in Linux

## Hardware Setup
We assume the following IP address mappings, connected together via VLAN:
```
NetPIPE Server -> 192.168.1.9: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
NetPIPE Client -> 192.168.1.11: Intel(R) Xeon(R) CPU E5-2690 0 @ 2.90GHz, 126 GB, Intel(R) 10 Gigabit Network Connection
```

## Software Setup
NetPIPE 3.7.1: https://github.com/handong32/NetPIPE-3.7.1

## Example run_netpipe_tuned.sh run:
```
#example server: MSGSIZES='8192' ITR='8 4' MDVFS='0x1d00 0x1c00' REPEAT=1 WRITEBACK_DIR="/mnt/netpipe/linux/9_27" MYIP="192.168.1.9" ./run_netpipe_tuned.sh
#example client: MSGSIZES='8192' ITR='8 4' MDVFS='0x1d00 0x1c00' REPEAT=1 WRITEBACK_DIR="/mnt/netpipe/linux/9_27" ROLE="CLIENT" MYIP="192.168.1.11" NP_SERVER_IP="192.168.1.9" ./run_netpipe_tuned.sh
```

##### Requirements
```
Numpy
Pandas
Python3
```

##### Example: run_netpipe_tuned.sh will automatically create a <data_folder> to store all trace logs
```
python clean_netpipe_linux.py <data_folder>
```
