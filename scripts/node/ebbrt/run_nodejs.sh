#! /bin/bash

currdate=`date +%m_%d_%Y_%H_%M_%S`

export MRAPL=${MRAPL:-"135 75 55"}
export NITERS=${NITERS:='2'}
export MDVFS=${MDVFS:="0x1d00 0x1b00 0x1900 0x1700 0x1500 0x1300 0x1100 0xf00 0xd00"}
#export ITRS=${ITRS:-"2 4 6 8 12 16 20 24 28 32 36 40 50 60 70 80"}
export RITRS=${RITRS:-"1 2 3 4 6 8 10 12 14 16 18 20 25 30 35 40"}
export MSLEEP=${MSLEEP:='c1'}

#set -x
#ghzs="2.9 2.8 2.7 2.6 2.5 2.4 2.3 2.2 2.1 2.0 1.9 1.8 1.7 1.6 1.5 1.4 1.3 1.2"
#coms="com1 com512"
#taskset -c 1 ./wrk -t1 -c1 -d1s -H "Host: example.com \n Host: test.go Host: example.com \n  Host: example.com \n  Host: example.com \n  Host: example.com \n Host: example.com \n Host: example.com Host: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.com Host: example.comHost: example.com Host: example.com \n Host: test.go Host: example.com \n  Host: example.com \n  Host: example.com \n  Host: example.com \n Host: example.com \n Host: example.com Host: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.com Host: example.comHost: " http://192.168.1.230:6666/index.html --latency
#
function alive
{
    output=$(ping -c 3 192.168.1.200 | grep "3 received")
    if [[ ${#output} -ge 1 ]]; then
	return 0
    else
	return 1
    fi
}

function reboot
{
    echo "reboot"
    #TODO trigger node reboot
    sleep 1
    success=1
    for iwait in `seq 0 1 10`;
    do
        echo "reboot waiting ${iwait}"
	if alive; then
	    success=0
	    break	    
        fi
	sleep 120
    done

    sleep 60
    return $success
}

function runEbbRT
{
    echo "rapl:   ${MRAPL}"
    echo "niters: ${NITERS}"
    echo "mdvs:   ${MDVFS}"
    echo "ritrs:  ${RITRS}"
    echo "sleep_states:  ${MSLEEP}"
    echo "mkdir ${currdate}"

    mkdir ${currdate}

    for r in ${MRAPL}; do
	for itr in ${RITRS}; do	    
	    for dvfs in ${MDVFS}; do
		for sleep_state in ${MSLEEP}; do
		    for nrepeat in `seq 0 1 ${NITERS}`; do		    
			# try two times
			for rerun in `seq 0 1 2`; do
			    sleep 1
			    runBench=1
			    benchSuccess=1
			    
			    if alive; then
				echo "alive"
				runBench=0
			    else
				echo "dead"

				if reboot; then	    
				    #runBench=0
				    echo "reboot success"
				    timeout 300 python3 -u nodejs_bench.py --os ebbrt --rapl 135 --dvfs 0x1d00 --itr 4 --nrepeat 0 --sleep_state 'c7'
				    echo "warmup run success"

				    ## check alive again
				    if alive; then
				        runBench=0
				    fi
				fi
			    fi
			    
			    if [[ ${runBench} -eq 0  ]]; then				
				echo "timeout 300 python3 -u nodejs_bench.py --os ebbrt --rapl ${r} --dvfs ${dvfs} --itr ${itr} --nrepeat ${nrepeat} --sleep_state ${sleep_state}"
				timeout 300 python3 -u nodejs_bench.py --os ebbrt --rapl ${r} --dvfs ${dvfs} --itr ${itr} --nrepeat ${nrepeat} --sleep_state ${sleep_state}
				if alive; then
				    benchSuccess=0
				fi
			    fi

			    ritr=$(( ${itr}*2 ))
			    if [[ ${benchSuccess} -eq 0  ]]; then
				echo "ebbrt_dmesg.${nrepeat}_${ritr}_${dvfs}_${r}_${sleep_state} success"
				echo "get,1" | socat - TCP4:192.168.1.200:5002 > "ebbrt_dmesg.${nrepeat}_1_${ritr}_${dvfs}_${r}_${sleep_state}"
				sleep 1
				
				echo "rdtsc,0" | socat - TCP4:192.168.1.200:5002 > "ebbrt_rdtsc.${nrepeat}_${ritr}_${dvfs}_${r}_${sleep_state}"
				sleep 1
				
				#echo "getcounters,0" | socat - TCP4:192.168.1.200:5002 > "ebbrt_counters.${nrepeat}_${ritr}_${dvfs}_${r}_${sleep_state}"
				
				## get wireshark
				#scp -r 192.168.1.11:/app/tshark.pcap "ebbrt_tshark.${nrepeat}_1_${ritr}_${dvfs}_${r}"
				#sleep 1
				
				if alive; then
				    ./parse_ebbrt_mcd "ebbrt_dmesg.${nrepeat}_1_${ritr}_${dvfs}_${r}_${sleep_state}" > "ebbrt_dmesg.${nrepeat}_1_${ritr}_${dvfs}_${r}_${sleep_state}.csv"
				    rm -f "ebbrt_dmesg.${nrepeat}_1_${ritr}_${dvfs}_${r}_${sleep_state}"
				    mv ebbrt_* ${currdate}/
				    break
				else
				    echo "**** ebbrt_dmesg.${nrepeat}_${ritr}_${dvfs}_${r}_${sleep_state} get log error"
				fi				
			    else
				echo "**** ebbrt_dmesg.${nrepeat}_${ritr}_${dvfs}_${r}_${sleep_state} ran out of memory error"
			    fi

			    echo "rerun == ${rerun}"
			done
		    done
		done
	    done
	done
    done
}

$1
