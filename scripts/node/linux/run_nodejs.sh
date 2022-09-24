#! /bin/bash

currdate=`date +%m_%d_%Y_%H_%M_%S`

export MRAPL=${MRAPL:-"135 75 55"}
export NITERS=${NITERS:='2'}
export MDVFS=${MDVFS:="0x1d00 0x1b00 0x1900 0x1700 0x1500 0x1300 0x1100 0xf00 0xd00"}
export ITRS=${ITRS:-"2 4 6 8 12 16 20 24 28 32 36 40 50 60 70 80"}
export COM=${COM:-"com1"}

#set -x
#ghzs="2.9 2.8 2.7 2.6 2.5 2.4 2.3 2.2 2.1 2.0 1.9 1.8 1.7 1.6 1.5 1.4 1.3 1.2"
#coms="com1 com512"
#taskset -c 1 ./wrk -t1 -c1 -d1s -H "Host: example.com \n Host: test.go Host: example.com \n  Host: example.com \n  Host: example.com \n  Host: example.com \n Host: example.com \n Host: example.com Host: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.com Host: example.comHost: example.com Host: example.com \n Host: test.go Host: example.com \n  Host: example.com \n  Host: example.com \n  Host: example.com \n Host: example.com \n Host: example.com Host: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.comHost: example.com Host: example.comHost: " http://192.168.1.230:6666/index.html --latency
#
function run
{
    echo "DVFS ${MDVFS}"
    echo "ITRS ${ITRS}"
    echo "MRAPL ${MRAPL}"
    echo "NITERS ${NITERS}"
    echo "COM ${COM}"

    for c in ${COM}; do
	ssh 192.168.1.9 pkill node
	echo "mkdir ${currdate}_${c}"
	mkdir ${currdate}_${c}
	
	for r in ${MRAPL}; do
	    for itr in $ITRS; do	    
		for dvfs in ${MDVFS}; do
		    for i in `seq 0 1 ${NITERS}`; do
			echo "timeout 300 python3 -u nodejs_bench.py --rapl ${r} --dvfs ${dvfs} --itr ${itr} --com ${c} --nrepeat ${i}"
			timeout 300 python3 -u nodejs_bench.py --rapl ${r} --dvfs ${dvfs} --itr ${itr} --com ${c} --nrepeat ${i}
			sleep 1
			## get wireshark
			#scp -r 192.168.1.9:/app/tshark.pcap "linux.node.tshark.${i}_${itr}_${dvfs}_${r}"
			#sleep 1
			mv linux.node* ${currdate}_${c}/
		    done
		done
	    done
	done
    done
}

$1
