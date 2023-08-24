# Load firmware to ONT Nokia G-010S-P

## Generic steps
### Introduction
- Either telnet, ssh or TTL is fine but TTL requires special device and sometimes [physical connection via internal pins](https://hack-gpon.org/ont-nokia-g-010s-p/)
- Default IP address of the ONT is 192.168.1.10
- There are 02 main partitions for firmware, mtd2 (image0) and mtd5 (image1), one of them is active at a time.

### Tools
With the assumption that operator uses Windows, the tools listed below
- [Teraterm](http://www.teraterm.org/)
- [MobaXterm](https://mobaxterm.mobatek.net/)

### Detail steps
- Copy the image into ONT via scp (if you can use this connection) or kermit (if you use TTL connection). The image file should be copied in /tmp since flash capacity (size) while /tmp mounted to RAM.
- Check the current active partition
```sh
# fw_printenv committed_image
```
If the result is 0 (image0 - mtd2 current active partition) then you can only write the fw to the other (image1 - mtd5).
```sh
# mtd -e image1 write /tmp/sys.bin image1
# fw_setenv committed_image 1
```

## Using Carlitoxx v1 firmware

### Replace firmware
> IP. 192.168.1.10 \
  user. root \
  password. admin

```sh
$ssh -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10
```
Backup all partitions with dd
```sh
$dd if=/dev/mtd0 of=/tmp/mtd0.backup
$dd if=/dev/mtd1 of=/tmp/mtd1.backup
$dd if=/dev/mtd2 of=/tmp/mtd2.backup
$dd if=/dev/mtd3 of=/tmp/mtd3.backup
$dd if=/dev/mtd4 of=/tmp/mtd4.backup
$dd if=/dev/mtd5 of=/tmp/mtd5.backup
```
Transfer backups via scp
```sh
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd0.backup mtd0.backup
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd1.backup mtd1.backup
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd2.backup mtd2.backup
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd3.backup mtd3.backup
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd4.backup mtd4.backup
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 admin@192.168.1.10:/tmp/mtd5.backup mtd5.backup
```

Send `Carlitoxx v1` firmware to sfp via scp
```sh
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 mtd2.bin admin@192.168.1.10:/tmp/
$scp -o KexAlgorithms=diffie-hellman-group1-sha1 mtd5.bin admin@192.168.1.10:/tmp/
```

Write the image to mtd2 and mtd5 partition
```sh
$mtd -e image0 write /tmp/mtd2.bin image0
$mtd -e image1 write /tmp/mtd5.bin image1
```

Set env vars before reboot
```sh
$fw_setenv ont_serial XXXXXXXX
$fw_setenv target oem-generic
$fw_setenv committed_image 0
$reboot
```


### ONU setup
Update / verify parameters via `/etc/init.d/sys.sh`
```sh
$vi /etc/init.d/sys.sh

....
oem-generic)
  uci set sys.mib.vendor_id='VTGR'
  uci set sys.mib.ont_version='vG-421WD-v2\0\0'
  uci set sys.mib.equipment_id='XXXXXXXX\0\0\0\0'
....
```

Config / set env variables (then reboot)
```sh
$fw_setenv target oem-generic
$fw_setenv ont_serial XXXXXXXX
$fw_setenv image0_version V2106220222
$fw_setenv image1_version V2106220222
$reboot
```
### Verify ONU state
Login via ssh after reboot
```sh
$onu ploamsg
# expect to have 5
$onu gtcsng
# ont_serial XXXXXXXX should be here
$gtop # then c then v
# or
$gtop # then c then y
# you should see VLANs (35, ...)
```

## References
- [ONU online status](https://forum.huawei.com/carrier/en/thread/769933660095848448)