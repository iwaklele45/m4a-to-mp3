# M4A to MP3 Converter (Compatibility Mode)

Script sederhana untuk mengubah file `.m4a` menjadi `.mp3` dengan opsi yang kompatibel untuk pemutar musik (MP3 Player) lama / jadul agar dapat memuat lagu lebih cepat.

## Fitur
- Konversi satu file `.m4a` atau satu folder berisi banyak file `.m4a` secara rekursif.
- Kompresi tinggi untuk performa player lama: **MP3 Constant Bitrate 128kbps, Stereo, 44.1kHz**.
- Struktur subfolder (misal: Artist/Album) tetap terjaga saat dikonversi.
- **Salin Lirik Otomatis:** Mempertahankan lirik lagu dari file `.m4a` (tag `©lyr`) ke `.mp3` (tag ID3v2 `USLT`).
- Semua output disimpan di dalam folder `mp3_output` pada root project ini (mencegah file dobel di flashdisk asal).

## Prasyarat
Pastikan sudah menginstal:
1. **Python 3**
2. **FFmpeg** (harus ada di PATH sistem).
3. **Mutagen** (library Python untuk memproses metadata).
   ```bash
   pip install mutagen
   ```
   *(Catatan untuk macOS: Jika muncul error externally-managed-environment, gunakan perintah: `pip install --break-system-packages mutagen`)*

## Cara Penggunaan

Jalankan script dengan memberikan parameter path folder atau path file:

### 1. Konversi satu folder secara rekursif (Batch)
```bash
python3 convert.py /Volumes/MY_FD/Iwan_Fals
```
File hasil konversi beserta struktur foldernya akan disimpan di `<folder_project>/mp3_output/`.
Contoh: `/Volumes/MY_FD/Iwan_Fals/Koleksi_Akustik/03. Galang Rambu Anarki.m4a` akan dikonversi menjadi `<folder_project>/mp3_output/Iwan_Fals/Koleksi_Akustik/03. Galang Rambu Anarki.mp3`.

### 2. Konversi satu file
```bash
python3 convert.py "/Volumes/MY_FD/Iwan_Fals/Koleksi_Akustik/03. Galang Rambu Anarki.m4a"
```
File hasil konversi akan disimpan di `<folder_project>/mp3_output/Iwan_Fals/Koleksi_Akustik/03. Galang Rambu Anarki.mp3`.

---

## Solusi Masalah (Troubleshooting)

### Flashdisk Tidak Terbaca oleh Player Lama
Jika USB Flashdisk Anda tidak terdeteksi sama sekali oleh pemutar musik (misalnya muncul tulisan "Read USB" yang sangat lama atau tidak ada respons):
1. **Penyebab:** Player lama umumnya tidak mendukung skema partisi **GPT (GUID Partition Table)** yang sering digunakan oleh OS modern.
2. **Solusi:** Format ulang USB Flashdisk Anda menggunakan skema partisi **MBR (Master Boot Record)** dan sistem file **FAT32**.

*Peringatan: Proses format akan menghapus semua file di dalam USB. Amankan (backup) data Anda terlebih dahulu.*

#### Cara Format di macOS via Terminal:
1. Cari nama disk USB Anda dengan perintah:
   ```bash
   diskutil list
   ```
2. Format ulang disk tersebut (misal identifier-nya adalah `disk13`):
   ```bash
   diskutil eraseDisk FAT32 "NAMA_FD" MBR disk13
   ```
   *(Ganti `disk13` dengan identifier USB Anda yang sebenarnya)*
