import os
import subprocess
import sys
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, USLT

def convert_file(input_path, output_path):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-codec:a", "libmp3lame",
        "-b:a", "128k",  # 128k bitrate for fast reading on old players
        "-ar", "44100",
        "-ac", "2",
        output_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Copy lyrics from M4A (©lyr) to MP3 (USLT) if present
        try:
            m4a = MP4(input_path)
            lyrics = m4a.get('\xa9lyr')
            if lyrics and lyrics[0]:
                try:
                    tags = ID3(output_path)
                except Exception:
                    tags = ID3()
                tags.add(USLT(encoding=3, lang='eng', desc='', text=lyrics[0]))
                tags.save(output_path)
        except Exception as e:
            # Silently ignore tag copying errors, but print warning
            print(f"  Peringatan: Gagal menyalin lirik: {e}")
            
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("Error: ffmpeg tidak terinstal atau tidak ditemukan di PATH.")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python3 convert.py <path_file_atau_folder>")
        sys.exit(1)

    target = os.path.abspath(sys.argv[1])
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_base_dir = os.path.join(project_root, "mp3_output")

    if not os.path.exists(target):
        print(f"Error: Path '{target}' tidak ditemukan.")
        sys.exit(1)

    # Determine base directory to preserve Artist/Album structure
    if os.path.isdir(target):
        has_direct_m4a = any(f.lower().endswith('.m4a') for f in os.listdir(target) if os.path.isfile(os.path.join(target, f)))
        if has_direct_m4a:
            # Target is Album folder. Artist is parent, base is grandparent
            base_dir = os.path.dirname(os.path.dirname(target))
        else:
            # Target is Artist folder (or higher). Base is parent
            base_dir = os.path.dirname(target)
            
        print(f"Mencari file .m4a di dalam folder '{target}' secara rekursif...")
        m4a_files = []
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.lower().endswith('.m4a'):
                    m4a_files.append(os.path.join(root, file))

        if not m4a_files:
            print(f"Tidak ditemukan file .m4a di folder '{target}'.")
            return

        print(f"Ditemukan {len(m4a_files)} file .m4a. Mulai konversi...")
        for input_path in m4a_files:
            rel_path = os.path.relpath(input_path, base_dir)
            output_rel_path = os.path.splitext(rel_path)[0] + ".mp3"
            output_path = os.path.join(output_base_dir, output_rel_path)

            print(f"Mengonversi: {rel_path}")
            if convert_file(input_path, output_path):
                print(f"Sukses -> {output_rel_path}")
            else:
                print(f"Gagal -> {rel_path}")

        print(f"\nKonversi selesai! File disimpan di '{output_base_dir}'.")

    elif os.path.isfile(target):
        if not target.lower().endswith('.m4a'):
            print("Error: File harus memiliki ekstensi .m4a")
            sys.exit(1)

        target_dir = os.path.dirname(target)
        has_direct_m4a = any(f.lower().endswith('.m4a') for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f)))
        if has_direct_m4a:
            base_dir = os.path.dirname(os.path.dirname(target_dir))
        else:
            base_dir = os.path.dirname(target_dir)

        rel_path = os.path.relpath(target, base_dir)
        output_rel_path = os.path.splitext(rel_path)[0] + ".mp3"
        output_path = os.path.join(output_base_dir, output_rel_path)

        print(f"Mengonversi file: {rel_path}")
        if convert_file(target, output_path):
            print(f"Konversi sukses -> {output_rel_path}")
        else:
            print("Konversi gagal.")

if __name__ == "__main__":
    main()
