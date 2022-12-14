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

################################
# TODO: Other NIC params to explore
################################
def updateNIC():
    global ITR
    global WTHRESH
    global HTHRESH
    global PTHRESH
    global DTXMXSZRQ
    global DCA
    global RSC_DELAY
    global MAX_DESC
    global BSIZEPKT
    global BSIZEHDR
    global RXRING
    global TXRING
    global THRESHC
    
    ### fix syntax highlighting in emacs???
    bs = 0
    
    '''
    Receive Side Scaling (RSC)
    '''
    # RSC Delay: The delay = (RSC Delay + 1) x 4 us = 4, 8, 12... 32 us.
    # 3 bits, so [0 - 7]
    # select 4: 4, 8, 16, 32 | 1, 2, 4, 8
    RSC_DELAY = np.random.randint(1, 5)
    if RSC_DELAY == 3:
        RSC_DELAY=4
    elif RSC_DELAY == 4:
        RSC_DELAY = 8
    
    '''
    MAXDESC * SRRCTL.BSIZEPKT must not exceed 64 KB minus one, which is the
    maximum total length in the IP header and must be larger than the expected
    received MSS.

    Maximum descriptors per Large receive as follow:
    00b = Maximum of 1 descriptor per large receive.
    01b = Maximum of 4 descriptors per large receive.
    10b = Maximum of 8 descriptors per large receive.
    11b = Maximum of 16 descriptors per large receive
    '''
    # select 3: 1, 2, 3
    MAX_DESC = np.random.randint(1, 4)

    '''
    SRRCTL.BSIZEPKT
    Receive Buffer Size for Packet Buffer.
    The value is in 1 KB resolution. Value can be from 1 KB to 16 KB. Default buffer size is
    2 KB. This field should not be set to 0x0. This field should be greater or equal to 0x2
    in queues where RSC is enabled.

    *** Linux default is at 3072
    
    MAXDESC * SRRCTL.BSIZEPKT must not exceed 64 KB minus one

    if MAX_DESC == 1:
        BSIZEPKT = 12 * 1024 #np.random.randint(3, 16) * 1024
    elif MAX_DESC == 2:
        BSIZEPKT = 6 * 1024#np.random.randint(3, 8) * 1024
    else:
        BSIZEPKT = 3 * 1024 #np.random.randint(3, 4) * 1024
    '''
    BSIZEPKT = 3 * 1024
    
    '''
    BSIZEHEADER

    Receive Buffer Size for Header Buffer.
    The value is in 64 bytes resolution. Value can be from 64 bytes to 1024 bytes

    *** Linux default is set at 0x4 * 64 Bytes = 256 Bytes
    '''
    # select 3: [4, 8, 12] * 64 Bytes
    BSIZEHDR = np.random.randint(1, 4) * 4 * 64

    '''
    ITR Interval
    '''
    # ITR: (RSC_DELAY+2) us to 200 us in increments of 10
    #ITR = np.random.randint((((RSC_DELAY+1) * 4)/2)+1, 101) * 2
    itr_delay_us = RSC_DELAY*4
    itr_start = (itr_delay_us/10) + 1
    #print("itr_start", itr_start)
    ITR = np.random.randint(itr_start, 16) * 10
    
    '''
    RDLEN
    '''
    c = np.random.randint(0, 2)
    if c == 0:
        RXRING = 512
        TXRING = 512
    else:
        RXRING = 4092
        TXRING = 4092

    '''
    TDLEN
    '''
    #c = np.random.randint(0, 2)
    #if c == 0:
    #    TXRING = 512
    #else:
    #    TXRING = 4092
    
    '''
    ** Linux: PTHRESH=32 HTHRESH=1 WTHRESH=1
    Notes about THRESH, PTHRESH, WTHRESH

    Transmit descriptor fetch setting is programmed in the TXDCTL[n] register per
    In order to reduce transmission latency, it is recommended to set the PTHRESH value
    as high as possible while the HTHRESH and WTHRESH as low as possible (down to
    zero).

    In order to minimize PCIe overhead the PTHRESH should be set as low as possible
    while HTHRESH and WTHRESH should be set as high as possible.

    The sum of PTHRESH plus WTHRESH must not be greater than the onchip descriptor
    buffer size (40)

    When the WTHRESH equals zero, descriptors are written back for those
    descriptors with the RS bit set. When the WTHRESH value is greater than
    zero, descriptors are accumulated until the number of accumulated descriptors equals
    the WTHRESH value, then these descriptors are written back. Accumulated
    descriptor write back enables better use of the PCIe bus and memory bandwidth.

    PTHRESH: Pre Fetch Threshold The on chip descriptor buffer becomes almost empty while there are enough
    descriptors in the host memory.
         - The on-chip descriptor buffer is defined as almost empty if it contains less descriptors
           then the threshold defined by PTHRESH
         - The transmit descriptor contains enough descriptors if it includes more ready
           descriptors than the threshold defined by TXDCTL[n].HTHRESH

    Controls when a prefetch of descriptors is considered. This threshold refers to the
    number of valid, unprocessed transmit descriptors the 82599 has in its on-chip buffer. If
    this number drops below PTHRESH, the algorithm considers pre-fetching descriptors from
    host memory. However, this fetch does not happen unless there are at least HTHRESH
    valid descriptors in host memory to fetch. HTHRESH should be given a non-zero value each time PTHRESH is used.
    '''

    # [2, 40) in increments of 2
    # WTHRESH: Should not be higher than 1 when ITR == 0, else device basically crashes
    '''
    WTHRESH = np.random.randint(1, 20)
    
    #PTHRESH: WTHRESH + PTHRESH < 40
    PTHRESH = np.random.randint(1, (20 - WTHRESH)+1)
    
    # HTHRESH
    HTHRESH = np.random.randint(1, 20)

    WTHRESH *= 2
    PTHRESH *= 2
    HTHRESH *= 2
    '''
    '''
    In order to reduce transmission latency, it is recommended to set the PTHRESH value
    as high as possible while the HTHRESH and WTHRESH as low as possible (down to
    zero).

    In order to minimize PCIe overhead the PTHRESH should be set as low as possible
    while HTHRESH and WTHRESH should be set as high as possible.

    The sum of PTHRESH plus WTHRESH must not be greater than the on chip descriptor
    buffer size (40)
    '''
    THRESHC = np.random.randint(0, 3)

    if THRESHC == 0:
        '''
        CPU cache line optimization Assume  N equals the CPU cache line divided by 16 descriptor size.
        Then in order to align descriptors prefetch to CPU cache line in most cases it is advised to
        set PTHRESH to the onchip descriptor buffer size minus N and HTHRESH to N. In order to align 
        descriptor write back to the CPU cache line it is advised to set WTHRESH to either N or even 2 times N.
        Note that partial cache line writes might significantly degrade performance. Therefore, it is highly recommended to follow this advice.
        
        getconf LEVEL1_DCACHE_LINESIZE == CPU cache line size 64
        on chip descriptor size == 16
        
        N = 64 / 16 = 4
        PTHRESH = 16 4 == 12
        HTHRESH == 4
        WTHRESH == 4 or 8
        '''

        PTHRESH = 12
        HTHRESH = 4
        WTHRESH = 4
    elif THRESHC == 1:
        '''
        Minimizing PCIe overhead: As an example, setting PTHRESH to the on-chip descriptor buffer size minus 16 and HTHRESH to 16 
        minimizes the PCIe request and header overhead to 20% of the bandwidth required for the descriptor fetch.
        '''
        PTHRESH = 0
        HTHRESH = 16
        WTHRESH = 16
    elif THRESHC == 2:
        '''
        Minimizing transmission latency from tail update: Setting PTHRESH to the on chip 
        descriptor buffer size minus N, previously defined, while HTHRESH and WTHRESH to zero.
        '''
        PTHRESH = 12
        HTHRESH = 0
        WTHRESH = 0
    
    '''
    DTXMXSZRQ
    The maximum allowed amount of 256 bytes outstanding requests. If the total
    size request is higher than the amount in the field no arbitration is done and no
    new packet is requested
    
    min: 0x10 * 256 = 4 KB
    max: 0xFFF * 256 = 1 MB
    '''
    c = np.random.randint(0, 3)
    if c == 0:
        # default
        DTXMXSZRQ = 16
    elif c == 1:
        DTXMXSZRQ = 2046
    elif c == 2:
        # 0xFFF
        DTXMXSZRQ = 4095

    '''
    DCA == 1, RX_DCA = OFF, TX_DCA = OFF
    DCA == 2, RX_DCA = ON, TX_DCA = OFF
    DCA == 3, RX_DCA = OFF, TX_DCA = ON
    DCA == 4, RX_DCA = ON, TX_DCA = ON
    '''
    dcac = np.random.randint(0, 2)
    if dcac == 0:
        DCA = 1
    else:
        DCA = 4

    #print("RSC_DELAY=%d MAX_DESC=%d BSIZEPKT=%d BSIZEHDR=%d RXRING=%d TXRING=%d ITR=%d DTXMXSZRQ=%d WTHRESH=%d PTHRESH=%d HTHRESH=%d DCA=%d\n" % (RSC_DELAY, MAX_DESC, BSIZEPKT, BSIZEHDR, RXRING, TXRING, ITR, DTXMXSZRQ, WTHRESH, PTHRESH, HTHRESH, DCA))
    #return

    # RSC_DELAY
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 RSCDELAY", str(RSC_DELAY)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # MAXDESC
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 MAXDESC", str(MAX_DESC)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # BSIZEPKT
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 BSIZEPACKET", str(BSIZEPKT)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # BSIZEHDR
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 BSIZEHEADER", str(BSIZEHDR)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # RXRING
    p1 = Popen(["ssh", SERVER, "ethtool -G enp4s0f1 rx", str(RXRING)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # TXRING
    p1 = Popen(["ssh", SERVER, "ethtool -G enp4s0f1 tx", str(TXRING)], stdout=PIPE, stderr=PIPE)
    p1.communicate()
        
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 WTHRESH", str(WTHRESH)], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 PTHRESH", str(PTHRESH)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 HTHRESH", str(HTHRESH)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # DTXMXSZRQ 
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 DTXMXSZRQ", str(DTXMXSZRQ)], stdout=PIPE, stderr=PIPE)
    p1.communicate()

    # DCA
    p1 = Popen(["ssh", SERVER, "ethtool -C enp4s0f1 DCA", str(DCA)], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    
    p1 = Popen(["ssh", SERVER, "ifdown enp4s0f1"], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    time.sleep(1)
    
    p1 = Popen(["ssh", SERVER, "ifup enp4s0f1"], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    time.sleep(1)

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
    p1 = Popen(["ssh", SERVER, "wrmsr -a 0x199", v], stdout=PIPE, stderr=PIPE)
    p1.communicate()
    time.sleep(0.5)
    DVFS = v

def cleanLogs():
    for i in range(0, 16):                    
        runRemoteCommandGet("cat /proc/ixgbe_stats/core/"+str(i)+" &> /dev/null", SERVER)
        if VERBOSE:
            print("cleanLogs", i)
            
def printLogs():
    for i in range(0, 16):
        runRemoteCommandGet("cat /proc/ixgbe_stats/core/"+str(i)+" &> /app/mcd_dmesg."+str(i), SERVER)
        if VERBOSE:
            print("printLogs", i)

def getLogs():
    for i in range(0, 16):
        runLocalCommandOut("scp -r "+SERVER+":/app/mcd_dmesg."+str(i)+" linux.mcd.dmesg."+str(NREPEAT)+"_"+str(i)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS))        
        #runLocalCommandOut("gzip -f9 mcd_dmesg."+str(NREPEAT)+"_"+str(i-1)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS))
        if VERBOSE:
            print("getLogs", i)

def runBench(mqps):
    ########### init client load generators 
    runRemoteCommandGet("pkill mutilate", "192.168.1.106")
    runRemoteCommandGet("pkill mutilate", "192.168.1.107")            
    runRemoteCommandGet("pkill mutilate", "192.168.1.38")
    runRemoteCommandGet("pkill mutilate", "192.168.1.37")
    runRemoteCommandGet("pkill mutilate", "192.168.1.11")
    time.sleep(1)        

    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.37")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.38")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.106")
    runRemoteCommands("/app/mutilate/mutilate --agentmode --threads=16", "192.168.1.107")    
    time.sleep(1)
    #########################

    # check if memcached server is already running
    is_running_mcd = runRemoteCommandGet("pgrep memcached", SERVER)
    if is_running_mcd:
        print("already running mcd")
    else:
        ## launch mcd server
        runRemoteCommands("taskset -c 0-15 /app/memcached/memcached -u nobody -t 16 -m 32G -c 8192 -b 8192 -l 192.168.1.9 -B binary", SERVER)
        time.sleep(1)
        
        # init mcd server with prelim data
        runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --loadonly -K fb_key -V fb_value", CLIENT)
        runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --loadonly -K fb_key -V fb_value", CLIENT)
        runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --loadonly -K fb_key -V fb_value", CLIENT)
        runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --loadonly -K fb_key -V fb_value", CLIENT)
        time.sleep(1)

    ## reset logs
    cleanLogs()

    ## run benchmark
    output = runRemoteCommandGet("taskset -c 0 /app/mutilate/mutilate --binary -s 192.168.1.9 --noload --agent=192.168.1.106,192.168.1.107,192.168.1.37,192.168.1.38 --threads=1 "+WORKLOADS[TYPE]+" --depth=4 --measure_depth=1 --connections=16 --measure_connections=32 --measure_qps=2000 --qps="+str(mqps)+" --time="+str(TIME), CLIENT)

    # dumps rdtsc timestamps of mcd server -- helps to parse log for timestamps that only impact application runtime
    runRemoteCommands("killall -USR2 memcached", SERVER)
    
    if VERBOSE:
        print("Finished executing memcached")

    ## store output file
    read_5th = ''
    read_10th = ''
    read_50th = ''
    read_90th = ''
    read_95th = ''
    read_99th = ''
    totalQPS = ''
    f = open("linux.mcd.out."+str(NREPEAT)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS), "w")
    for line in str(output).strip().split("\\n"):
        if "read" in line:
            alla = list(filter(None, line.strip().split(' ')))
            read_5th = alla[4]
            read_10th = alla[5]
            read_50th = alla[6]
            read_90th = alla[7]
            read_95th = alla[8]
            read_99th = alla[9]
        if "Total QPS" in line:
            alla = list(filter(None, line.strip().split(' ')))
            totalQPS = alla[3]
        f.write(line.strip()+"\n")
    f.close()
    
    printLogs()
    getLogs()

    ### creating summary files 
    numeles=0
    f = open("linux.mcd.dmesg."+str(NREPEAT)+"_0_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS), "r")
    for l in f:
        alla = l.strip().split(' ')
        numeles = len(alla)
        break
    f.close()

    arras = []
    for i in range(0, numeles):
        arras.append(0)
        
    for i in range(0, 16):
        f = open("linux.mcd.dmesg."+str(NREPEAT)+"_"+str(i)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS), "r")
        for l in f:
            alla = l.strip().split(' ')
            for j in range(0, numeles):
                arras[j] += int(alla[j])
            break

    f = open("linux.mcd.stats."+str(NREPEAT)+"_"+str(ITR)+"_"+str(DVFS)+"_"+str(RAPL)+"_"+str(TARGET_QPS), "w")
    for i in range(0, len(arras)):
        f.write(str(arras[i])+' ')
    f.write(read_99th+' '+totalQPS+'\n')
    f.close()
    time.sleep(1)

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
    parser.add_argument("--verbose", help="Print mcd raw stats")
    
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
