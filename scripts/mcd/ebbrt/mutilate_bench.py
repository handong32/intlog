import math
import random
import subprocess
from subprocess import Popen, PIPE, call
import time
from datetime import datetime
import sys
import os
import getopt
import numpy as np
import itertools
import argparse
import shutil

CLIENT = "192.168.1.11"
SERVER = "192.168.1.9"
ITR = 333
RAPL = 135
DVFS = '0x1d00'
TYPE = 'etc'
TIME = 120
TARGET_QPS=100000
NREPEAT = 0
SLEEP = "c7"
SEND="SINGLE"
DCA = "OFF"
RSC = "OFF"
TWB = "OFF"

WORKLOADS = {
    #ETC = 75% GET, 25% SET
    'etc': '--keysize=fb_key --valuesize=fb_value --iadist=fb_ia --update=0.25',

    #USR = 99% GET, 1% SET
    'usr': '--keysize=19 --valuesize=2 --update=0.01',

    'etc2': '--keysize=fb_key --valuesize=fb_value --iadist=fb_ia --update=0.033',

    'large': '--keysize=normal:400,2 -V --valuesize=normal:8000,2 --update=0.25'
}

def runLocalCommandOut(com):
    p1 = Popen(list(filter(None, com.strip().split(' '))), stdout=PIPE)
    p1.communicate()

def runLocalCommand(com):
    #print(com)
    p1 = Popen(list(filter(None, com.strip().split(' '))), stdout=PIPE)

def runRemoteCommands(com, server):
    #print(com)
    p1 = Popen(["ssh", server, com])

def runRemoteCommandGet(com, server):
    #print(com)
    p1 = Popen(["ssh", server, com], stdout=PIPE)
    return p1.communicate()[0].strip()

def runLocalCommandGet(com, sin):
    p1 = Popen(list(filter(None, com.strip().split(' '))), stdout=PIPE, stdin=PIPE)
    sout = p1.communicate(input=sin.encode())[0]
    return sout.decode()

sleep_dict = {
    "c1"  : "0",      # 0x00
    "c1e" : "1",      # 0x01
    "c3"  : "16",     # 0x10
#    "c6"  : "32",     # 0x20
    "c7"  : "48"      # 0x30
}
def setSLEEP(v):
    global SLEEP
    SLEEP = v
    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "sleep_state,"+sleep_dict[SLEEP])
    
def setITR(v, s):    
    global ITR

    if s == "linux":
        p1 = Popen(["ssh", CSERVER2, "/app/ethtool-4.5/ethtool -C eth0 rx-usecs", v], stdout=PIPE, stderr=PIPE)
        p1.communicate()    
        time.sleep(0.5)
    else:
        runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rx_usecs,"+v)
    
    ITR = int(v)

def setRAPL(v, s):
    global RAPL

    if s == "linux":
        p1 = Popen(["ssh", CSERVER2, "/app/uarch-configure/rapl-read/rapl-power-mod", v], stdout=PIPE, stderr=PIPE)
        p1.communicate()
        time.sleep(0.5)
    else:
        runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rapl,"+v)
        
    RAPL = int(v)

def setDVFS(v, s):
    global DVFS

    if s == "linux":
        p1 = Popen(["ssh", CSERVER2, "wrmsr -a 0x199", v], stdout=PIPE, stderr=PIPE)
        p1.communicate()
        time.sleep(0.5)
    else:
        runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "dvfs,"+str(int(v, 0)))

    DVFS = v

def setSend(s):
    global SEND
    if s == 2:
        SEND="MULTIPLE"
    else:
        SEND="SINGLE"
        
    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "ixgbe_switch_send,"+str(s))

def setMAXTXD(s):
    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "IXGBE_MAX_DATA_PER_TXD,"+str(s))
    
def runBench(mqps):
    runRemoteCommandGet("pkill mutilate", "192.168.1.106")
    runRemoteCommandGet("pkill mutilate", "192.168.1.107")    
    runRemoteCommandGet("pkill mutilate", "192.168.1.38")
    runRemoteCommandGet("pkill mutilate", "192.168.1.37")
    runRemoteCommandGet("pkill mutilate", "192.168.1.11")
    time.sleep(1)
    print("pkill mutilate done")
    
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.37")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.38")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.106")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.107")
    
    time.sleep(5)    
    print("mutilate agentmode done")

    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "start,0")    
    output = runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --noload --agent=192.168.1.106,192.168.1.107,192.168.1.37,192.168.1.38 --threads=1 "+WORKLOADS[TYPE]+" --depth=4 --measure_depth=1 --connections=16 --measure_connections=32 --measure_qps=2000 --qps="+str(mqps)+" --time="+str(TIME), "192.168.1.11")
    
    #--keysize=fb_key --valuesize=fb_value
    #normal:400,2 -V normal:8000,2
    #output = runRemoteCommandGet('taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --noload --agent=192.168.1.106,192.168.1.107,192.168.1.37,192.168.1.38 --threads=1 --keysize=normal:400,2 -V --valuesize=normal:8000,2 --update=0.25 --depth=4 --measure_depth=1 --connections=16 --measure_connections=32 --measure_qps=2000 --qps='+str(mqps)+' --time='+str(TIME), '192.168.1.11')
    
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "stop,0")
    read_5th = ''
    read_10th = ''
    read_50th = ''
    read_90th = ''
    read_95th = ''
    read_99th = ''
    f = open("ebbrt_out."+str(NREPEAT)+"_"+str(int(ITR)*2)+"_"+DVFS+"_"+str(RAPL)+"_"+str(TARGET_QPS)+"_"+str(SLEEP)+"_"+TYPE+"_"+SEND+"_DCA"+DCA+"_RSC"+RSC+"_TWB"+TWB, "w")
    for line in str(output).strip().split("\\n"):
        if "read" in line:
            alla = list(filter(None, line.strip().split(' ')))
            read_5th = alla[4]
            read_10th = alla[5]
            read_50th = alla[6]
            read_90th = alla[7]
            read_95th = alla[8]
            read_99th = alla[9]
        f.write(line.strip()+"\n")
    f.close()

    countersout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "getcounters,0")
    f = open("ebbrt_counters."+str(NREPEAT)+"_"+str(int(ITR)*2)+"_"+DVFS+"_"+str(RAPL)+"_"+str(TARGET_QPS)+"_"+str(SLEEP)+"_"+TYPE+"_"+SEND+"_DCA"+DCA+"_RSC"+RSC+"_TWB"+TWB, "w")
    f.write(str(countersout))
    f.close()
            
    x1 = np.zeros(72)
    tjoules=0.0
    trdtsc=0.0
    for line in str(countersout).strip().split("\n"):
        alla = list(filter(None, line.strip().split(' ')))
        core = int(alla[0])
        if core < 2:
            ## sum up joules for package 0 & 1
            tjoules += float(alla[10])
            trdtsc += float(alla[11])
        xalla = [float(x) for x in alla]
        x1 = np.add(x1, xalla)
    ## average time
    trdtsc = trdtsc / 2.0

    ## 16 cores
    x1[0] = 16
    x1[10] = tjoules
    x1[11] = trdtsc    
    f = open("ebbrt_mcd_stats."+str(NREPEAT)+"_"+str(int(ITR)*2)+"_"+DVFS+"_"+str(RAPL)+"_"+str(TARGET_QPS)+"_"+str(SLEEP)+"_"+TYPE+"_"+SEND+"_DCA"+DCA+"_RSC"+RSC+"_TWB"+TWB, "w")
    salla = [str(x) for x in x1]
    f.write('ncores rx_desc rsc_desc rx_bytes tx_desc tx_bytes instructions cycles ref_cycles llc_miss joules time')
    for i in np.arange(40):
        f.write(' tx_desc_'+str(i))
    f.write(' read_5th read_10th read_50th read_90th read_95th read_99th\n')
    f.write((' '.join(salla[:52]))+' '+read_5th+' '+read_10th+' '+read_50th+' '+read_90th+' '+read_95th+' '+read_99th)
    f.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--os", help="linux or ebbrt")
    parser.add_argument("--rapl", help="Rapl power limit [35, 135]")
    parser.add_argument("--itr", help="Static interrupt delay [10, 500]")
    parser.add_argument("--dvfs", help="DVFS value [0xc00 - 0x1d00]")
    parser.add_argument("--nrepeat", help="repeat value")
    parser.add_argument("--qps", type=int, help="RPS rate")
    parser.add_argument("--time", type=int, help="Time in seconds to run")    
    parser.add_argument("--type", help="Workload type [etc, usr]")
    parser.add_argument("--send", type=int, help="Send using SINGLE [1] TX descriptor or MULTIPLE [2]")
    parser.add_argument("--maxtxd", type=int, help="IXGBE_MAX_DATA_PER_TXD [>1500]")
    parser.add_argument("--dca", type=int, help="DCA")
    parser.add_argument("--rsc", type=int, help="Receive Side Coalescing")
    parser.add_argument("--twb", type=int, help="TX_HEAD_WB")
    parser.add_argument("--sleep_state", help="sleep states: c1, c1e, c3, c6, c7")
    
    args = parser.parse_args()
    if args.rapl:
        #print("RAPL = ", args.rapl)
        setRAPL(args.rapl, args.os)
    if args.itr:
        #print("ITR = ", args.itr)
        setITR(args.itr, args.os)
    if args.qps:
        TARGET_QPS = args.qps
        #print("TARGET_QPS = ", TARGET_QPS)
    if args.dvfs:
        setDVFS(args.dvfs, args.os)
    if args.nrepeat:
        NREPEAT = args.nrepeat
    if args.time:
        TIME = args.time
        #print("TIME = ", TIME)
    if args.type:
        TYPE = args.type
        #print("TYPE = ", TYPE)
    if args.sleep_state:
        setSLEEP(args.sleep_state)
    if args.send:
        setSend(args.send)
    if args.maxtxd:
        setMAXTXD(args.maxtxd)
    if args.dca:
        DCA="ON"
    if args.rsc:
        RSC="ON"
    if args.twb:
        TWB="ON"

    runBench(TARGET_QPS)        
