## Uruchomienie i skonfigurowanie OpenWRT dla maszyny wirtualnej i uruchomienie na qemu


1. Pobieramy obraz systemu operacyjnego:

`wget https://downloads.openwrt.org/releases/21.02.1/targets/armvirt/64/openwrt-21.02.1-armvirt-64-Image -O Image`

2. Pobiramy obraz systemu plików:

`wget https://downloads.openwrt.org/releases/21.02.1/targets/armvirt/64/openwrt-21.02.1-armvirt-64-rootfs-ext4.img.gz -O rootfs.ext4.gz`

3. Wypakowujemy obraz systemu plików:

`gzip -d rootfs.ext4.gz`

4. Uruchamiamy system:

```sh
qemu-system-aarch64 \
    -M virt -cpu cortex-a57 -nographic -smp 4 \
    -kernel Image -append "root=/dev/vda console=ttyAMA0" \
    -drive file=rootfs.ext4,if=none,format=raw,id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -nic user,hostfwd=tcp::8889-:80,hostfwd=tcp::8888-:22
```

5. Edytujemy plik konfiguracyjny sieci, tak aby umożliwić przesyłanie plików na OpenWRT:

`vi /etc/config/network`
```
#config device
#       option name 'br-lan'
#       option type 'bridge'
#       list ports 'eth0'

config interface 'lan'
        option device 'br-lan'
        option proto 'dhcp'
#       option ipaddr '192.168.1.1'
#       option netmask '255.255.255.0'
#       option ip6assign '60'
```
6. Uruchamiamy ponownie kartę sieciową:

`/etc/init.d/network reload`

## Implementacja w języku Python oraz uruchomienie w OpenWRT / qemu dwóch programów generujących sygnał PWM

1. Aktualizujemy pakiety na OpenWRT:

`opkg update`

2. Instalujemy na OpenWRT Pythona3:

`opkg install python3`

### Generacja sygnałów o zmiennej częstotliwości

### Generacja sygnałów o zmiennym wypełnieniu