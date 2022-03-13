# Zadanie domowe

Pobranie oraz wstępna konfiguracja obrazu systemu Linux dla 64-bitowej maszyny Virt:
1. `wget https://buildroot.org/downloads/buildroot-2022.02.tar.xz` - pobranie najnowszej stabilnej wersji buildroota
2. `tar -xaf buildroot-2022.02.tar.xz` - wypakowanie skompresowanych plików
3. `cd buildroot-2022.02/` - wejście do folderu z plikami buildroot
4. `make qemu_aarch64_virt_defconfig` - wybranie domyślnej konfiguracji dla 64-bitowej maszyny Virt
5. `make menuconfig`
    - Toolchain -> Toolchain Type -> External

Ustawienie nazwy systemu na Brzozowski_Krawczyk:
1. `make menuconfig`
    - System configuration -> System hostname -> Brzozowski_Krawczyk

Wersja używająca ramdysku startowego:
1. `make menuconfig`
    - Filesystem images -> cpio the root filesystem -> Compression method -> gzip [x]
    - Filesystem images -> initial RAM filesystem linked into linux kernel [x]
    - Filesystem images -> ext2/3/4 root filesystem [ ]
2. `make clean all` - pełna rekompilacja systemu
3. `qemu-system-aarch64 -M virt -cpu cortex-a57 -nographic -smp 4 -kernel output/images/Image -append "console=ttyAMA0"` - uruchomienie QEMU z Initramfs

Wersja używająca rzeczywistego systemu plików ext4:
1. `make linux-dirclean` - usunięcie poprzedniego obrazu
2. `make menuconfig`
    - Filesystem images -> initial RAM filesystem linked into linux kernel [ ]
    - Filesystem images -> ext2/3/4 root filesystem [x] -> ext4
3. `make` - częściowa rekompilacja systemu
4. `qemu-system-aarch64 -M virt -cpu cortex-a57 -nographic -smp 4 -kernel output/images/Image -append "root=/dev/vda console=ttyAMA0" -drive file=output/images/rootfs.ext4,if=none,format=raw,id=hd0 -device virtio-blk-device,drive=hd0` - uruchomienie QEMU z systemem plików ext4