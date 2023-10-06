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
sudo insmod drivers/net/ethernet/intel/ixgbe/ixgbe.ko
ip link set dev up
ip addr add ..
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
