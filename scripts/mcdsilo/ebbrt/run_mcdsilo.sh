#! /bin/bash

export NITERS=${NITERS:='1'}
export BEGIN_ITER=${BEGIN_ITER:="0"}
export MDVFS=${MDVFS:="0x1d00 0x1b00 0x1900 0x1700 0x1500 0x1300 0x1100 0xf00 0xd00"}
export MQPS=${MQPS:='50000 100000 200000'}
export ITRS=${ITRS:-"25 50 100 150 200"}
export MRAPL=${MRAPL:-"135 95 75 55"}
export MSLEEP=${MSLEEP:='c7'}

currdate=`date +%m_%d_%Y_%H_%M_%S`

function runMutilateBench
{
    timeout 300 python3 -u mutilate_bench.py "$@"
}

function reboot
{
    echo "reboot"
    ssh 192.168.1.11 pkill mutilate
    ssh 192.168.1.37 pkill mutilate
    ssh 192.168.1.38 pkill mutilate
    sleep 600
    success=1
    if alive; then
	success=0
    fi
    return $success
}

function alive
{
    output=$(ping -c 3 192.168.1.9 | grep "3 received")
    if [[ ${#output} -ge 1 ]]; then
	return 0
    else
	return 1
    fi
}

function runEbbRT
{
    echo "runEbbRT"
    echo "DVFS ${MDVFS}"
    echo "ITRS ${ITRS}"
    echo "MRAPL ${MRAPL}"
    echo "NITERS ${NITERS}"
    echo "MQPS ${MQPS}"
    echo "mkdir ${currdate}"
    echo "sleep_states:  ${MSLEEP}"    
    mkdir ${currdate}
    mkdir "${currdate}_sla_violations"

    for dvfs in ${MDVFS}; do
	for itr in $ITRS; do
	    for qps in ${MQPS}; do
		for r in ${MRAPL}; do
		    for sleep_state in ${MSLEEP}; do
			for nrepeat in `seq $BEGIN_ITER 1 $NITERS`; do
			    # try 3 times
			    for rerun in `seq 0 1 2`; do
				sleep 1
				runBench=1
				benchSuccess=1
				
				if alive; then
				    echo "alive ${rerun}"
				    runBench=0
				else
				    echo "dead ${rerun}"

				    if reboot; then
					if alive; then	    
					    ## warmup run
					    runMutilateBench --qps 10000 --time 5 --itr 50 --rapl 135 --dvfs 0x1d00 --nrepeat 0
					    
					    if alive; then
						ssh 192.168.1.11 pkill mutilate
						ssh 192.168.1.37 pkill mutilate
						ssh 192.168.1.38 pkill mutilate
						runBench=0
					    fi
					fi
				    	
					echo "reboot success ${rerun}"
				    fi
				fi
				
				if [[ ${runBench} -eq 0  ]]; then		
				    echo "runMutilateBench --qps ${qps} --time 20 --itr ${itr} --rapl ${r} --dvfs ${dvfs} --nrepeat ${nrepeat} --sleep_state ${sleep_state}"
				    runMutilateBench --qps ${qps} --time 20 --itr ${itr} --rapl ${r} --dvfs ${dvfs} --nrepeat ${nrepeat} --sleep_state ${sleep_state}
				    sleep 1
				    if alive; then
					rritr=$(( ${itr}*2 ))
					output=$(wc -c "ebbrt_out.${nrepeat}_${rritr}_${dvfs}_${r}_${qps}_${sleep_state}" | awk '{print $1}')
					if (( $output > 100)); then
					    echo "filesize == ${output} good"
					    read_99th=$(sed -n 2p "ebbrt_out.${nrepeat}_${rritr}_${dvfs}_${r}_${qps}_${sleep_state}" | awk '{ print $10 }')
				            read_99th_int=${read_99th%.*}

					    if (( $read_99th_int <= 500 )); then
						benchSuccess=0
					    else
						echo "ebbrt_out.${nrepeat}_${rritr}_${dvfs}_${r}_${qps}_${sleep_state} read_99=${read_99th_int} > 500, skipping log data"
						mv "ebbrt_out.${nrepeat}_${rritr}_${dvfs}_${r}_${qps}_${sleep_state}" "${currdate}_sla_violations/"
						pkill socat
						break
					    fi					
					else
					    echo "filesize == ${output} bad, rebooting"
					    rm "ebbrt_out.${nrepeat}_${rritr}_${dvfs}_${r}_${qps}_${sleep_state}"
					    reboot
					fi
					
				    fi
				fi

				## made it to this point, get log data
				ritr=$(( ${itr}*2 ))
				if [[ ${benchSuccess} -eq 0  ]]; then
				    echo "rdtsc,0" | socat - TCP4:192.168.1.9:5002 > ebbrt_rdtsc.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}
				    echo "ebbrt_rdtsc.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}"
				    sleep 1
				    echo "getcounters,0" | socat - TCP4:192.168.1.9:5002 > ebbrt_counters.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}
				    echo "ebbrt_counters.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}"
				    
				    for c in `seq 0 1 14`; do
					echo "get,$c" | socat - TCP4:192.168.1.9:5002 > ebbrt_dmesg.${nrepeat}_${c}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}
					sleep 1
					./parse_ebbrt_mcd ebbrt_dmesg.${nrepeat}_${c}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state} > "ebbrt_dmesg.${nrepeat}_${c}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}"
					sleep 1
					rm -f ebbrt_dmesg.${nrepeat}_${c}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}
					echo "ebbrt_dmesg.${nrepeat}_${c}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state}"
					mv ebbrt_* ${currdate}/
					sleep 1
				    done
				    
				    if alive; then
					pkill socat
					break
				    else
					pkill socat
					echo "**** ebbrt_dmesg.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state} get log error"
				    fi				
				else
				    echo "**** ebbrt_dmesg.${nrepeat}_${ritr}_${dvfs}_${r}_${qps}_${sleep_state} ran out of memory error"
				fi

				echo "rerun == ${rerun}"
			    done
    			done
		    done
		done
	    done
	done
    done
}

"$@"

