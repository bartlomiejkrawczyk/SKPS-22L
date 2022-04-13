# [SKPS] - Laboratorium 2

Przedmiot:
Systemy komputerowe w sterowaniu i pomiarach

Mateusz Brzozowski, Bartłomiej Krawczyk

# Plan laboratorium
1. [ ] Zbudowanie i uruchomienie pakietu dostarczonego w materiałach do wykładu.
2. [ ] Stworzenie pakietów OpenWRT na bazie dostarczonych kodów źródłowych.
3. [ ] Zdalne debugowanie programów za pomocą gdb.

## Przygotowanie SDK

1. `https://downloads.openwrt.org/releases/21.02.1/targets/bcm27xx/bcm2711/openwrt-sdk-21.02.1-bcm27xx-bcm2711_gcc-8.4.0_musl.Linux-x86_64.tar.xz` - pobranie SDK na RPi
2. `tar -xaf openwrt-sdk-21.02.1-bcm27xx-bcm2711_gcc-8.4.0_musl.Linux-x86_64.tar.xz`- wypakowanie sdk
3. `mv openwrt-sdk-21.02.1-bcm27xx-bcm2711_gcc-8.4.0_musl.Linux-x86_64/ openwrt-sdk/` - zmiana nazwy folderu
4. `cd openwrt-sdk`
5. `make menuconfig`:
    - Global Build Settings (wyłączamy opcje):
        - Select all target specific packages by default
        - Select all kernel module packages by default
        - Select all userspace packages by default
        - Cryptohraphically sign package lists
    - Advanced configuration options (wyłączamy opcje):
        - Automatic removal of build directories
6. `cd ..`

## 1. Pierwszy pakiet
1. `https://moodle.usos.pw.edu.pl/pluginfile.php/217384/mod_folder/content/0/WZ_W03_przyklady.tar.xz` - pobranie paczki z pakietem demo1
2. `tar -xaf WZ_W03_przyklady.tar.xz` - rozpakowanie paczki
3. `cd openwrt-sdk`
4. `export LANG=C`
5. `nano feeds.conf.default`- dodanie ścieżki do katalogu zawierającego katalogi z pakietami:
```
src-link skps /home/user/demo1_owrt_pkg
```
6. `./scripts/feeds update -a`
7. `./scripts/feeds install -p skps -a`
8. `make menuconfig`:
    - Examples (zaznaczamy):
        - demo1
        - demo1mak
9. `make package/feeds/skps/demo1/compile`
9. `make package/feeds/skps/demo1mak/compile`

10. `cd packages/architektura/skps`
11. `python3 -m http.server` - utworzenie servera http
12. `wget http://10.42.0.1`- przesłanie pliku na OpenWRT

Na OpenWRT:
1. `opkg install demo1.ipk` lub `opekg install --force-reintstall demo1.ipk`

instalować z opcją `--force-reintstall`

## 2. Pakiety "worms" i "buggy"

1. `https://moodle.usos.pw.edu.pl/pluginfile.php/217384/mod_folder/content/0/WZ_W03_przyklad_extbr.tar.xz` - pobranie paczki z pakietami worms i buggy
2. `tar -xaf WZ_W03_przyklad_extbr.tar.xz` - rozpakowanie paczki z pakietami
3. należy zainstalować ncurses w SDK: `./scripts/feeds install libncurses`
4. należy zaktualizować listy pakietów: `./scripts/feeds update -a`, `./scripts/feeds install -p skps -a`
4. Powtarzamy kroku z pierwszego etapu labolatorium


## 3. Debugowanie zdalne
1. `opkg update`
1. `opkg install gdb`- instalacja gdb za pomocą managera pakietów
2. `opkg install gdbserver`- instalacja gdbserver za pomocą managera pakietów
3. `gdbserver :9000 /usr/bin/bug3`

Na komputerze:
1. `./scripts/remote-gdb 10.42.0.230:9000 ./build_dir/target-aarch64_cortex-a72_musl/buggy-1.0/.pkgdir/buggy/usr/bin/bug1`

### Poszukiwanie błędów dla trzech programów z pakietu buggy za pomocą debuggera gdb

1. - uruchomienie gdbservera na RPi
2. - uruchomienie skryptu remote-gdb (zgodnie z instrukcją na stronie openwrt.org)

`set breakpoint auto-hw off` - breakpoint specific settings
`set can-use-hw-watchpoints 0` - set debugger's willingness to use watchpoint hardware

Przy pomocy gdb wykonaliśmy:
- ustawienie breakpointu

- pracę krokową

- podgląd wartości zmiennej (jednorazowy)

- podgląd wartości zmiennej (przy każdym kroku)

- podgląd stosu

- backtrace

- wykorzystanie watchpoint'ów w programie bug3, aby sprawdzić kiedy następuje zapisanie wartości pod niewłaściwym adresem np. w s1[10]

bug1:
w pętli for próbujemy się odwołac do table, jednakże wskaźnik "table" nie jest zainicjalizowany.

bug2:
próujemy odwołać się poza rozmiar tablicy

bug3:
zapisywaliśmy literę i w miejsce 0