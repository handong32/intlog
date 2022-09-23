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

SERVER = "192.168.1.9"
CLIENT = "192.168.1.11"
ITR = 1
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
VERBOSE = 0
TARGET_QPS=100000
NREPEAT = 0

WORKLOADS = {
    #ETC = 75% GET, 25% SET
    'etc': '--keysize=fb_key --valuesize=fb_value --iadist=fb_ia --update=0.25',

    #USR = 99% GET, 1% SET
    'usr': '--keysize=19 --valuesize=2 --update=0.01',

    'etc2': '--keysize=fb_key --valuesize=fb_value --iadist=fb_ia --update=0.033'
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

####################################################
# Use ethtool to set ITR on all cores/queues
###################################################
def setITR(v):
    global ITR
    p1 = Popen(["ssh", SERVER, "/app/ethtool-4.5/ethtool -C eth0 rx-usecs", v], stdout=PIPE, stderr=PIPE)
    p1.communicate()    
    time.sleep(0.5)
    ITR = int(v)

##################################################
# Set RAPL power limit, modified from (https://web.eece.maine.edu/~vweaver/projects/rapl/)
#################################################
def setRAPL(v):
    global RAPL
    p1 = Popen(["ssh", SERVER, "/app/uarch-configure/rapl-read/rapl-power-mod", v], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    time.sleep(0.5)
    RAPL = int(v)

####################################################
# Use msrtools to write directly and update all
# CPU frequencies (DVFS)
###################################################
def setDVFS(v):
    global DVFS
    ## last core runs a polling loop, set to use lowest energy for DVFS
    p1 = Popen(["ssh", SERVER, "wrmsr -p 15 0x199", "0xc00"], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    
    for i in range(0, 15):
        wcom=f'wrmsr -p {i} 0x199'
        p1 = Popen(["ssh", SERVER, wcom, v], stdout=PIPE, stderr=PIPE)
        p1.communicate()
    DVFS = v
                                                    
def cleanLogs():
    for i in range(0, 15):
        runRemoteCommandGet("cat /proc/ixgbe_stats/core/"+str(i)+" &> /dev/null", SERVER)
        if VERBOSE:
            print("cleanLogs", i)
            
def printLogs():
    for i in range(0, 15):
        runRemoteCommandGet("cat /proc/ixgbe_stats/core/"+str(i)+" &> /app/mcdsilo_dmesg."+str(i), SERVER)
        if VERBOSE:
            print("printLogs", i)

def getLogs():
    for i in range(0, 15):
        runLocalCommandOut("scp -r "+SERVER+":/app/mcd_dmesg."+str(i)+" linux.mcdsilo.dmesg."+str(NREPEAT)+"_"+str(i)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS))        
        #runLocalCommandOut("gzip -f9 mcdsilo_dmesg."+str(NREPEAT)+"_"+str(i-1)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS))
        if VERBOSE:
            print("getLogs", i)

def runBench(mqps):
    ########### init client load generators 
    runRemoteCommandGet("pkill mutilate", "192.168.1.38")
    runRemoteCommandGet("pkill mutilate", "192.168.1.37")
    runRemoteCommandGet("pkill mutilate", "192.168.1.11")
    time.sleep(1)        

    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.37")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.38")
    time.sleep(1)
    #########################

    # check if memcached server is already running
    is_running_mcd = runRemoteCommandGet("pgrep silotpcc-linux", SERVER)
    if is_running_mcd:
        print("already running mcdsilo")
    else:
        ## launch mcd server - listens on 192.168.1.9 by default
        runRemoteCommands("taskset -c 0-15 /app/zygos-bench/servers/silotpcc-linux", SERVER)
        ## requires some time to set up DB
        time.sleep(60)                

    ## reset logs
    cleanLogs()

    ## run benchmark
    output = runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --noload --agent=192.168.1.37,192.168.1.38 --threads=1 "+WORKLOADS[TYPE]+" --depth=4 --measure_depth=1 --connections=16 --measure_connections=32 --measure_qps=2000 --qps="+str(mqps)+" --time="+str(TIME), CLIENT)

    # dumps rdtsc timestamps of mcd server -- helps to parse log for timestamps that only impact application runtime
    runRemoteCommands("killall -USR2 silotpcc-linux", SERVER)
    
    if VERBOSE:
        print("Finished executing mcdsilo")

    ## store output file
    f = open("linux.mcdsilo.out."+str(NREPEAT)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS), "w")
    for line in str(output).strip().split("\\n"):
        f.write(line.strip()+"\n")
    f.close()

    ## get logs
    printLogs()
    getLogs()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--type", help="Workload type [etc, usr]")
    parser.add_argument("--verbose", help="Print mcdsilo raw stats")
    
    args = parser.parse_args()
    if args.rapl:
        setRAPL(args.rapl)
    if args.itr:
        setITR(args.itr)
    if args.qps:
        TARGET_QPS = args.qps
    if args.dvfs:
        setDVFS(args.dvfs)
    if args.nrepeat:
        NREPEAT = args.nrepeat
    if args.time:
        TIME = args.time
    if args.type:
        TYPE = args.type
        print("TYPE = ", TYPE)
    if args.verbose:
        VERBOSE = 1

    runBench(TARGET_QPS)            
