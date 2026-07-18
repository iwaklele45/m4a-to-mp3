# Agent Guide for m4a-to-mp3

High-signal repository facts and commands.

## Setup & Execution
- **Prerequisites:** Python 3, `ffmpeg` (with `libmp3lame` encoder), Python library `mutagen`.
- **Execution:** `python3 convert.py <path_file_atau_folder>`
  - If directory: scans recursively and replicates `Artist/Album` structure under `mp3_output/`.
  - If single file: converts and outputs directly to `mp3_output/<Artist>/<Album>/file.mp3` depending on file location.

## Output Target Quality
- **Audio Output:** Constant Bitrate (CBR) **128 kbps**, **44.1 kHz**, **Stereo**. 
- **Album Art:** Stripped (audio-only) for fast loading on old devices.
- **Lyrics Tagging:** Copies embedded lyrics (`©lyr` tag in M4A) to MP3 ID3v2 Unsychronized Lyrics (`USLT` frame).

## Troubleshooting USB Player Lama
- Old media players require USB drive with **MBR (Master Boot Record)** partition table and **FAT32** filesystem.
- macOS disk format command:
  ```bash
  diskutil eraseDisk FAT32 "NAMA_FD" MBR <disk_identifier>
  ```
