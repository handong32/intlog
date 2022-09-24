set -x

#example server: MSGSIZES='8192' ITR='8 4' MDVFS='0x1d00 0x1c00' REPEAT=1 WRITEBACK_DIR="/mnt/netpipe/linux/9_27" MYIP="192.168.1.9" ./run_netpipe_tuned.sh
#example client: MSGSIZES='8192' ITR='8 4' MDVFS='0x1d00 0x1c00' REPEAT=1 WRITEBACK_DIR="/mnt/netpipe/linux/9_27" ROLE="CLIENT" MYIP="192.168.1.11" NP_SERVER_IP="192.168.1.9" ./run_netpipe_tuned.sh
# tshark -i eth0 -w t.pcap -F pcap host 192.168.1.9 &

TS=$(date +"%m.%d.%y-%H.%M.%S")

INSMOD=insmod
RMMOD=rmmod
IP=ip
TASKSET=taskset
DMESG=dmesg
CAT=cat
SLEEP=sleep
IXGBE=ixgbe
RDMSR=rdmsr
WRMSR=wrmsr
SSH=ssh
SCP=scp
TSHARK=tshark
PKILL=pkill
ETHTOOL=/app/ethtool-4.5/ethtool
SETAFFINITY=/app/perf/set_irq_affinity_ixgbe.sh
DISABLE_HT=/app/perf/disable_ht.sh
ENABLE_IDLE=/app/perf/enable_cstates.sh
MSR_MAX_FREQ=/app/perf/msr_max_freq.sh
NETPIPE=/app/NetPIPE-3.7.1/NPtcp_joules
RAPL_POW_MOD=/app/uarch-configure/rapl-read/rapl-power-mod
ETHMODULE_NOLOG=/app/ixgbe/ixgbe_orig.ko
ETHMODULE_YESLOG=/app/ixgbe/ixgbe_log.ko
SET_IP=/app/perf/set_ip.sh
IXGBE_STATS_CORE=/proc/ixgbe_stats/core
DVFS="0x199"
TURBOBOOST="0x1a0"

export ROLE=${ROLE:-"SERVER"}
export DEVICE=${DEVICE:-"eth0"}
export MYIP=${MYIP:-"192.168.1.9"}
export NP_SERVER_IP=${NP_SERVER_IP:-"192.168.1.9"}
export ITR=${ITR:-"10"}
export MSGSIZES=${MSGSIZES:-"64 8192 65536 524288"}
export LOOP=${LOOP:-"5000"}
export TASKSETCPU=${TASKSETCPU:-"1"}
export MDVFS=${MDVFS:="0x1d00"}
export MRAPL=${MRAPL:-"135"}
export REPEAT=${REPEAT:-1}
export BEGINI=${BEGINI:-0}
export PERF_INIT=${PERF_INIT:-0}
export CAPSHARK=${CAPSHARK:-0}
export WRITEBACK_DIR=${WRITEBACK_DIR:-"/tmp/"}
export SCREEN_PRESLEEP=${SCREEN_PRESLEEP:-1}

echo "Sleeping ${SCREEN_PRESLEEP} seconds for screen"
sleep ${SCREEN_PRESLEEP}

if [[ ${PERF_INIT} == 1 ]]; then
    ## apply performance scripts
    ${DISABLE_HT}
    ${SLEEP} 1
    ${ENABLE_IDLE}
    ${SLEEP} 1
    ${MSR_MAX_FREQ}
    ${SLEEP} 1
    ${RAPL_POW_MOD} 135
    ${SLEEP} 1

    ## apply ixgbe module with logging
    if [[ ${ROLE} == "SERVER" ]]; then    
	${SLEEP} 1
	#rmmod ixgbe && insmod /app/ixgbe/ixgbe_movnti.ko && /app/perf/set_ip.sh eth0 192.168.1.9
        ${RMMOD} ${IXGBE} && ${INSMOD} ${ETHMODULE_YESLOG} && ${SET_IP} ${DEVICE} ${MYIP}
	${SLEEP} 1
    fi

    ## set ITR to statically tuned
    ${ETHTOOL} -C ${DEVICE} rx-usecs 10
    ${SLEEP} 1
    ${IP} link set ${DEVICE} down && ${IP} link set ${DEVICE} up
    ${SLEEP} 1
fi

## dump results from setting PERF_INIT
${SETAFFINITY} -x all ${DEVICE}
${ETHTOOL} -c ${DEVICE}
${SLEEP} 1
${RDMSR} -a ${DVFS}
${RDMSR} -a ${TURBOBOOST}

for ((i=$BEGINI;i<$REPEAT; i++)); do
    for msg in $MSGSIZES; do
    	for itr in $ITR; do
	    #echo "${ETHTOOL} -C ${DEVICE} rx-usecs ${itr}"
	    ${ETHTOOL} -C ${DEVICE} rx-usecs ${itr}
	    for dvfs in ${MDVFS}; do
	    	if [[ ${ROLE} == "SERVER" ]]; then
		    ${WRMSR} -p ${TASKSETCPU} ${DVFS} ${dvfs}
		    #echo "${WRMSR} -p ${TASKSETCPU} ${DVFS} ${dvfs}"
		    ${SLEEP} 1
		fi
	    	
	    	for r in ${MRAPL}; do
		    if [[ ${ROLE} == "SERVER" ]]; then
			#echo "${RAPL_POW_MOD} ${r}"
			${RAPL_POW_MOD} ${r}
			${SLEEP} 1
		    fi
		    
		    if [[ ${ROLE} == "SERVER" ]]; then
			## clean up previous trace logs just incase
			${CAT} ${IXGBE_STATS_CORE}/${TASKSETCPU} &> /dev/null

			## start wireshark
			if [[ ${CAPSHARK} == 1 ]]; then
			    ${SLEEP} 1
			    ${TASKSET} -c 0 ${TSHARK} -i ${DEVICE} -w /app/tshark.pcap.${i}_${TASKSETCPU}_${msg}_${LOOP}_${itr}_${dvfs}_${r} -F pcap host ${MYIP} &
			    ${SLEEP} 1
			fi

			## start np server
		        ${TASKSET} -c ${TASKSETCPU} ${NETPIPE} -l ${msg} -u ${msg} -n ${LOOP} -p 0 -r -I &> /app/linux.np.server.${i}_${TASKSETCPU}_${msg}_${LOOP}_${itr}_${dvfs}_${r}

			if [[ ${CAPSHARK} == 1 ]]; then
			    ${SLEEP} 1
			    ${PKILL} ${TSHARK}
			    ${SLEEP} 1
			fi			
			
			# dumps logs
			${CAT} ${IXGBE_STATS_CORE}/${TASKSETCPU} &> /app/linux.np.log.${i}_${TASKSETCPU}_${msg}_${LOOP}_${itr}_${dvfs}_${r}
			${SLEEP} 5
		    else
			#echo "CLIENT"
		        while ! ${TASKSET} -c ${TASKSETCPU} ${NETPIPE} -h ${NP_SERVER_IP} -l ${msg} -u ${msg} -n ${LOOP} -p 0 -r -I; do
			    echo "FAILED: Server not ready trying again ..."
			    ${SLEEP} 5
			done
		        ${CAT} np.out &> /app/linux.np.client.${i}_${TASKSETCPU}_${msg}_${LOOP}_${itr}_${dvfs}_${r}
			${SLEEP} 5
		    fi		    
		    ${SLEEP} 1
		    ${SCP} /app/*.${i}_${TASKSETCPU}_${msg}_${LOOP}_${itr}_${dvfs}_${r} 192.168.1.153:${WRITEBACK_DIR}
	    	done
            done
        done	
    done
done
