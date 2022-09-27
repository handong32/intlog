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
WTHRESH = 0
PTHRESH = 0
HTHRESH = 0
THRESHC = 0
DTXMXSZRQ = 0
DCA = 0
RSC_DELAY = 0
MAX_DESC = 0
BSIZEPKT = 0
BSIZEHDR = 0
RXRING = 0
TXRING = 0
RAPL = 135
DVFS = '0xffff'
ITRC = []
TYPE = 'etc'
TIME = 120
SEARCH = 0
VERBOSE = 0
TARGET_QPS=100000
NREPEAT = 0
SLEEP = "c7"

WORKLOADS = {
    'etc': '--keysize=fb_key --valuesize=fb_value --iadist=fb_ia --update=0.0',
}

def runLocalCommandOut(com):
    #print(com)
    p1 = Popen(list(filter(None, com.strip().split(' '))), stdout=PIPE)
    p1.communicate()
    #print("\t"+com, "->\n", p1.communicate()[0].strip())
    
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
    
def setITR(v):
    global ITR

    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rx_usecs,"+v)

    time.sleep(0.5)
    ITR = int(v)

def setRAPL(v):
    global RAPL

    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rapl,"+v)

    time.sleep(0.5)
    RAPL = int(v)

def setDVFS(v):
    global DVFS

    runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "dvfs,"+str(int(v, 0)))
    
    time.sleep(0.5)
    DVFS = v    
    
def runBenchEbbRT(mqps):
    runRemoteCommandGet("pkill mutilate", "192.168.1.38")
    runRemoteCommandGet("pkill mutilate", "192.168.1.37")
    runRemoteCommandGet("pkill mutilate", "192.168.1.11")
    time.sleep(1)
    print("pkill mutilate done")
    
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.37")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.38")    
    time.sleep(2)    
    print("mutilate agentmode done")    

    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "clear,0")
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "start,0")
    
    output = runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --noload --agent=192.168.1.38,192.168.1.37 --threads=1 "+WORKLOADS[TYPE]+" --depth=4 --measure_depth=1 --connections=16 --measure_connections=32 --measure_qps=2000 --qps="+str(mqps)+" --time="+str(TIME), "192.168.1.11")
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "stop,0")
    
    ## normalize settings for retrieving logs
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rx_usecs,10")
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "dvfs,"+str(int('0x1d00', 0)))
    localout = runLocalCommandGet("socat - TCP4:192.168.1.9:5002", "rapl,135")
        
    f = open("ebbrt_out."+str(NREPEAT)+"_"+str(int(ITR)*2)+"_"+DVFS+"_"+str(RAPL)+"_"+str(TARGET_QPS)+"_"+str(SLEEP), "w")
    for line in str(output).strip().split("\\n"):
        f.write(line.strip()+"\n")
    f.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", help="Type of benchmark [mcd, zygos]")
    parser.add_argument("--rapl", help="Rapl power limit [35, 135]")
    parser.add_argument("--itr", help="Static interrupt delay [10, 500]")
    parser.add_argument("--dvfs", help="DVFS value [0xc00 - 0x1d00]")
    parser.add_argument("--nrepeat", help="repeat value")
    parser.add_argument("--qps", type=int, help="RPS rate")
    parser.add_argument("--time", type=int, help="Time in seconds to run")
    parser.add_argument("--ring", type=int, help="TX and RX ring")
    parser.add_argument("--dtxmx", type=int, help="DTXMXSZRQ")
    parser.add_argument("--dca", type=int, help="DCA")
    parser.add_argument("--thresh", type=int, help="PTHRESH, HTHRESH, WTHRESH")
    parser.add_argument("--restartnic", type=int, help="restart nic")
    parser.add_argument("--type", help="Workload type [etc, usr]")
    parser.add_argument("--pow_search_enable", help="Limit printf for search power limit")
    parser.add_argument("--verbose", help="Print mcd raw stats")
    parser.add_argument("--sleep_state", help="sleep states: c1, c1e, c3, c6, c7")

    args = parser.parse_args()
    if args.rapl:
        #print("RAPL = ", args.rapl)
        setRAPL(args.rapl)
    if args.itr:
        #print("ITR = ", args.itr)
        setITR(args.itr)
    if args.qps:
        TARGET_QPS = args.qps
        #print("TARGET_QPS = ", TARGET_QPS)
    if args.dvfs:
        setDVFS(args.dvfs)
    if args.nrepeat:
        NREPEAT = args.nrepeat
    if args.time:
        TIME = args.time
        #print("TIME = ", TIME)
    if args.type:
        TYPE = args.type
        print("TYPE = ", TYPE)
    if args.pow_search_enable:
        SEARCH = 1
    if args.verbose:
        VERBOSE = 1
    if args.sleep_state:
        setSLEEP(args.sleep_state)

    runBenchEbbRT(TARGET_QPS)            
