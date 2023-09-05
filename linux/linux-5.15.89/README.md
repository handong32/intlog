# Steps to build intlog for cloudlab node c6220
## requires Intel processor and Intel ixgbe 10GbE NIC
Follows from: `https://davidaugustat.com/linux/how-to-compile-linux-kernel-on-ubuntu`

```
sudo apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev fakeroot dwarves

wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.89.tar.xz
tar -xf linux-5.15.89.tar.gz

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
sudo insmod drivers/net/ethernet/intel/ixgbe/ixgbe.ko
ip link set dev up
ip addr add ..
```
