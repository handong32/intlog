After successfully compiling any of the four applications, you should have an *.elf32 to boot on a single hardware node. 

e.g. for an EbbRT-memcached binary:
```
$ file mcd.elf32 
mcd.elf32: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped
```

In order to boot this physically on another machine, we use the [pxeboot](https://docs.fedoraproject.org/en-US/Fedora/7/html/Installation_Guide/ap-pxe-server.html) protocol.

While that is mostly a guide for Linux based kernels, there are slight modifications to do for booting baremetal EbbRT. The following are steps I have successfully used to pxeboot EbbRT:

```
[root@localhost ~]# yum -y update
[root@localhost ~]# yum -y install dhcp
[root@localhost ~]# yum -y install syslinux xinetd
[root@localhost ~]# yum -y install tftp-server

[root@localhost ~]# cd /var/lib/tftpboot/
[root@localhost ~]# grub2-mknetdir --net-directory=./
[root@localhost ~]# grub2-mkimage -d /usr/lib/grub/i386-pc/ -O i386-pc-pxe --output=./boot/grub2/i386-pc/core.0 --prefix=./boot/grub2/ pxe tftp
[root@localhost ~]# cd boot/grub2/i386-pc/

## create this file
[root@localhost ~]# cat /var/lib/tftpboot/boot/grub2/grub.cfg
set default=0
set timeout=0

menuentry "EbbRT" {
	multiboot /mcd.elf32
	boot
}

[root@localhost ~]# cd ..
[root@localhost ~]# chmod a+x grub.cfg

[root@localhost ~]# cat /etc/dhcp/dhcpd.conf 
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
ddns-update-style none;

default-lease-time 604800;
max-lease-time 604800;
authoritative;

allow booting;
allow bootp;

## NOTE: 192.168.1.153 is on the local VLAN such that pxeboot can communicate with to get the required mcd.elf32 to boot
subnet 192.168.1.0 netmask 255.255.255.0 {
       range dynamic-bootp 192.168.1.200 192.168.1.254;
       option broadcast-address 192.168.1.255;
       next-server 192.168.1.153;
       filename                         "pxelinux.0";
}

## MAC addr matching to prioritize EbbRT elf
host ebbrt_server {
      hardware ethernet        90:e2:ba:ad:8c:00;
      fixed-address            192.168.1.9;   # netpipe, mcd, mcdsilo
      #fixed-address            192.168.1.200;   # nodejs
      max-lease-time           604800;
      next-server              192.168.1.153;
      filename "/boot/grub2/i386-pc/core.0";
}


[root@localhost ~]# cat /etc/xinetd.d/tftp 
# default: off
# description: The tftp server serves files using the trivial file transfer \
#	protocol.  The tftp protocol is often used to boot diskless \
#	workstations, download configuration files to network-aware printers, \
#	and to start the installation process for some operating systems.
service tftp
{
	socket_type		= dgram
	protocol		= udp
	wait			= yes
	user			= root
	server			= /usr/sbin/in.tftpd
	server_args		= -s /var/lib/tftpboot
	disable			= no
	per_source		= 11
	cps			= 100 2
	flags			= IPv4
}

[root@localhost ~]# systemctl start dhcpd
[root@localhost ~]# systemctl start xinetd
```
