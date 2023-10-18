# Steps to build intlog for cloudlab node c6220
## requires Intel processor and Intel ixgbe 10GbE NIC
Follows from: `https://davidaugustat.com/linux/how-to-compile-linux-kernel-on-ubuntu`

```
sudo apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev fakeroot dwarves

wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.89.tar.xz
tar -xf linux-5.15.89.tar.xz

cd linux-5.15.89
cp -v /boot/config-$(uname -r) .config
make localmodconfig

scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS
scripts/config --set-str CONFIG_SYSTEM_TRUSTED_KEYS ""
scripts/config --set-str CONFIG_SYSTEM_REVOCATION_KEYS ""

fakeroot make -j8

sudo make modules_install
sudo make install
sudo reboot
```

after rebooting
```
# need to rerun setup.sh and msr_setup.sh from experiment-scripts for flink
# turns off hyperthreads because intlog only has 16 queues/cores
echo off | sudo tee /sys/devices/system/cpu/smt/control
# turns off turboboost
echo "1" | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
# remmove mlx4 module
sudo rmmod mlx4_core

# gets the modified intlog
git clone https://github.com/handong32/intlog.git
cp -r ~/intlog/linux/linux-5.15.89/drivers/net/ ~/linux-5.15.89/drivers/

# build ixgbe.ko
cd linux-5.15.89
fakeroot make -j8

hand32@Mapper10-2:~/linux-5.15.89$ lsmod | grep ixgbe
ixgbe                 372736  0
mdio                   16384  1 ixgbe
dca                    16384  3 igb,ioatdma,ixgbe
hand32@Mapper10-2:~/linux-5.15.89$ lsmod | grep igb
igb                   266240  0
i2c_algo_bit           16384  2 igb,ast
dca                    16384  3 igb,ioatdma,ixgbe
hand32@Mapper10-2:~/linux-5.15.89$ sudo rmmod ixgbe
hand32@Mapper10-2:~/linux-5.15.89$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether f0:4d:a2:73:fb:7b brd ff:ff:ff:ff:ff:ff
    altname enp2s0f0
    inet 128.110.96.38/22 metric 1024 brd 128.110.99.255 scope global eno1
       valid_lft forever preferred_lft forever
    inet6 fe80::f24d:a2ff:fe73:fb7b/64 scope link 
       valid_lft forever preferred_lft forever
3: eno2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether f0:4d:a2:73:fb:7c brd ff:ff:ff:ff:ff:ff
    altname enp2s0f3
hand32@Mapper10-2:~/linux-5.15.89$ sudo insmod ~/linux-5.15.89/drivers/net/ethernet/intel/ixgbe/ixgbe.ko
hand32@Mapper10-2:~/linux-5.15.89$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether f0:4d:a2:73:fb:7b brd ff:ff:ff:ff:ff:ff
    altname enp2s0f0
    inet 128.110.96.38/22 metric 1024 brd 128.110.99.255 scope global eno1
       valid_lft forever preferred_lft forever
    inet6 fe80::f24d:a2ff:fe73:fb7b/64 scope link 
       valid_lft forever preferred_lft forever
3: eno2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether f0:4d:a2:73:fb:7c brd ff:ff:ff:ff:ff:ff
    altname enp2s0f3
6: enp3s0f0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether a0:36:9f:28:fa:78 brd ff:ff:ff:ff:ff:ff
7: enp3s0f1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether a0:36:9f:28:fa:7a brd ff:ff:ff:ff:ff:ff

hand32@Mapper10-2:~/linux-5.15.89$ sudo ip link set dev enp3s0f0 up
hand32@Mapper10-2:~/linux-5.15.89$ sudo ip addr add 10.10.1.2/24 dev enp3s0f0
hand32@Mapper10-2:~/linux-5.15.89$ cat /proc/ixgbe_stats/core/1
```

## Changes when moving from Linux 5.14 to Linux 5.15
```
## file_operations was deprecated?
static const struct file_operations ct_file_ops =
{
 .owner   = THIS_MODULE,
 .open    = ct_open,
 .read    = seq_read,
 .llseek  = seq_lseek,
 .release = seq_release
};

->

static const struct proc_ops ct_file_ops =
{
 .proc_open    = ct_open,
 .proc_read    = seq_read,
 .proc_lseek  = seq_lseek,
 .proc_release = seq_release
};

## api changes
proc_create(name, 0444, ixgbe_core_dir, &ct_file_ops, (void*)i) -> proc_create_data(name, 0444, ixgbe_core_dir, &ct_file_ops, (void*)i)
```
