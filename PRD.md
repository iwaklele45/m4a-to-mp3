# Product Requirement Document (PRD) - M4A to MP3 Converter for Legacy Players

## 1. Latar Belakang & Tujuan
Banyak pemutar musik (MP3 player) atau head unit mobil lama memiliki keterbatasan dalam membaca format audio modern (.m4a) serta keterbatasan memori/prosesor untuk memuat file berukuran besar. Proyek ini bertujuan untuk menyediakan alat konversi batch otomatis dari format `.m4a` ke `.mp3` dengan konfigurasi optimal untuk player jadul (kompatibilitas tinggi, loading cepat, dan mempertahankan lirik lagu).

## 2. Kebutuhan Pengguna (User Stories)
*   **Konversi Batch & Rekursif:** Pengguna dapat mengonversi satu folder yang berisi banyak subfolder musik (contoh: `Artist/Album/`) sekaligus secara rekursif.
*   **Replikasi Struktur Folder:** Folder output harus mempertahankan struktur folder input (`Artist/Album`) agar tidak merusak pengelompokan lagu saat disalin kembali ke USB.
*   **Penyalinan Lirik (Lyrics Sync):** Lirik yang tertanam di file `.m4a` harus tetap ada di file `.mp3` hasil konversi.
*   **Loading Cepat:** File MP3 hasil konversi harus dikompresi agar berukuran kecil sehingga player lama dapat membaca daftar putar dengan cepat tanpa macet/lemot.
*   **Panduan USB Drive:** Pengguna membutuhkan panduan pemecahan masalah jika USB flashdisk mereka tidak terbaca oleh player lama (masalah skema partisi GPT vs MBR).

## 3. Spesifikasi Teknis & Fitur Utama
*   **Bahasa & Framework:** Python 3 (menggunakan standard library `subprocess` & `os`).
*   **Dependencies:**
    *   `FFmpeg` dengan encoder `libmp3lame`.
    *   Library Python `mutagen` untuk membaca dan menulis metadata lirik.
*   **Kualitas & Format Output:**
    *   Codec: MP3 (MPEG audio layer 3).
    *   Bitrate: Constant Bitrate (CBR) **128 kbps** (standar kompatibilitas optimal & hemat memori).
    *   Sample Rate: **44.1 kHz**.
    *   Saluran (Channels): **Stereo (2 channels)**.
    *   Album Art / Cover: **Dihapus (Audio-only)** untuk meningkatkan kecepatan loading lagu pada pemutar lama.
*   **Transfer Metadata:**
    *   Membaca tag lirik `©lyr` dari file `.m4a` asal.
    *   Menulis lirik tersebut ke tag ID3v2 `USLT` (Unsynchronized Lyrics) pada file `.mp3` hasil.
*   **Struktur Output:**
    *   Seluruh hasil konversi disimpan di folder `mp3_output` pada root proyek.
    *   Struktur folder direplikasi berdasarkan relasi direktori target input.

## 4. Kriteria Sukses (Definition of Done)
1.  Script dapat dijalankan melalui CLI dengan format: `python3 convert.py <path_file_atau_folder>`.
2.  File `.mp3` yang dihasilkan berukuran lebih kecil dengan bitrate 128 kbps (CBR).
3.  Lirik lagu dari berkas `.m4a` dapat dibaca dan muncul dengan benar di berkas `.mp3` saat diuji menggunakan ID3 parser.
4.  Struktur folder `Artist/Album` terbentuk dengan benar di dalam folder `mp3_output/`.
5.  Dokumentasi menyertakan cara format USB ke MBR FAT32 untuk mengatasi masalah kompabilitas drive.
