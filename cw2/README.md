# [SKPS] - Laboratorium 1

## Zadania
1. [X] Uruchomienie OpenWRT na RPI 4B
2. [X] Zadanie 1
3. [X] Zadanie 2
4. [X] Zadanie 3
5. [X] Zadanie 4
6. [] Zadanie 5

## Przygotowanie stanowiska

Podłączyliśmy urządnie RPi zgodnie ze schematem dołączonym do skryptu laboratoryjnego.

<img src="images/1.0.jpg" width="75%"/>

Prowadzący zweryfikował poprawność połączenia.

## Pierwsze uruchomienie RPi

Uruchomiliśmy terminal UART za pomocą programu tio `tio /dev/ttyUSB0`.

Następnie włączyliśmy zasilanie i zalogowaliśmy się do urządenia.

![](images/1.1.png)


## Instalacja OpenWRT z wykorzystaniem systemu ratunkowego

Skonfigurowaliśmy server DNS, w pliku `/etc/resolv.conf` dodaliśmy linijkę `nameserver 8.8.8.8`

Pobraliśmy obraz systemu:

`wget https://downloads.openwrt.org/releases/21.02.1/targets/bcm27xx/bcm2711/openwrt-21.02.1-bcm27xx-bcm2711-rpi-4-ext4-factory.img.gz`

Rozpakowaliśmy obraz systemu:

`gzip -d openwrt-21.02.1-bcm27xx-bcm2711-rpi-4-ext4-factory.img.gz`

Zamontowaliśmy obraz systemu:

`losetup -P -f openwrt-21.02.1-bcm27xx-bcm2711-rpi-4-ext4-factory.img`

Przekopiowujemy obraz na drugą partycję:

`dd if=/dev/loop0p2 of=/dev/mmcblk0p2 bs=4096`

Tworzymy katalogi na partycje:

`mkdir /mnt/boot /mnt/owrt`

Montujemy partycję pierwszą obrazu OpenWRT

`mount /dev/loop0p1 /mnt/owrt`

Montujemy partycję pierwszą karty SD

`mount /dev/mmcblk0p1 /mnt/boot`

Kopiujemy pliki obrazu systemu:

- `cp /mnt/owrt/cmdline.txt /mnt/boot/user/`
- `cp /mnt/owrt/kernel8.img /mnt/boot/user/`
- `cp /mnt/owrt/bcm2711-rpi-4-b.dtb /mnt/boot/user/`

Powiększyliśmy system plików:

`resize2fs /dev/mmcblk0p2`

Na koniec restartowaliśmy system:

`reboot`

Po po uruchomieniu systemu skonfigurowaliśmy interfejs sieciowy:

`vi /etc/config/network`

Napotkaliśmy problemy z dns, tak więc dodaliśmy linijkę `nameserver 8.8.8.8` do pliku `/etc/resolv.conf`

Następnie pobraliśmy wymagane do pracy pakiety `opkg install [package]`:

- `nano`
- `python3`
- `python3-pip`
- `libgpiod`
- `gpiod-tools`
- `kmod-pwm-bcm2835`

`pip install python-periphery`

Włączyliśmy sprzętową obsługę PWM. W pliku `/boot/config.txt` dodaliśmy linijkę `dtoverlay=pwm-2chan`

## Obsługa GPIO przez sysfs

Przetestowaliśmy działanie diody LED za pomocą sysfs

`echo 27 > /sys/class/gpio/export`
`echo out > /sys/class/gpio/gpio27/direction`
`echo 1 > /sys/class/gpio/gpio27/value`

## Zadanie 1: GPIO - wyjście dla LED

Napisaliśmy program który uruchamiał diodę LED 10 razy.

## Zadanie 2: GPIO - wyjście dla LED z płynną zmianą jasności

Napisaliśmy kod w pythonie który uruchamiał diodę LED 10 razy.


## Zadanie 3: GPIO - wyjście PWM, buzzer pasywny

Napisaliśmy kod w pythonie który uruchamiał diodę LED 10 razy.


## Zadanie 4: GPIO - wejście

Napisaliśmy kod w pythonie który uruchamiał diodę LED 10 razy.


## Zadanie 5: Akcesoria do wyboru
