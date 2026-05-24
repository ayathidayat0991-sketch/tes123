 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/clipper_termux.py b/clipper_termux.py
new file mode 100755
index 0000000000000000000000000000000000000000..b1425e64c31c79a0a5f90e6cc389bbc5ae51cfb4
--- /dev/null
+++ b/clipper_termux.py
@@ -0,0 +1,153 @@
+#!/usr/bin/env python3
+"""
+Tools Termux: YouTube Clipper + Auto Subtitle
+UI simple: cukup masukkan URL YouTube.
+Output akan disimpan ke folder ./Hasil
+"""
+
+from __future__ import annotations
+
+import re
+import shutil
+import subprocess
+import sys
+from pathlib import Path
+
+HASIL_DIR = Path("Hasil")
+TEMP_DIR = HASIL_DIR / "_temp"
+CLIP_DURATION = 60  # detik
+
+
+def run_cmd(cmd: list[str], desc: str) -> None:
+    print(f"\n[+] {desc}...")
+    try:
+        subprocess.run(cmd, check=True)
+    except subprocess.CalledProcessError:
+        print(f"[!] Gagal saat proses: {desc}")
+        sys.exit(1)
+
+
+def sanitize_filename(name: str) -> str:
+    safe = re.sub(r"[^\w\-. ]+", "_", name).strip()
+    return safe or "video"
+
+
+def require_binary(binary: str) -> None:
+    if not shutil.which(binary):
+        print(f"[!] '{binary}' belum terpasang.")
+        print("    Install dulu di Termux, contoh:")
+        print("    pkg update && pkg install ffmpeg python")
+        print("    pip install yt-dlp")
+        sys.exit(1)
+
+
+def choose_subtitle_file(base_stem: str) -> Path | None:
+    candidates = sorted(TEMP_DIR.glob(f"{base_stem}*.vtt"))
+    if not candidates:
+        return None
+
+    id_candidates = [p for p in candidates if p.name.endswith(".id.vtt")]
+    if id_candidates:
+        return id_candidates[0]
+    return candidates[0]
+
+
+def get_video_title(url: str) -> str:
+    result = subprocess.run(
+        ["yt-dlp", "--print", "title", url],
+        check=False,
+        text=True,
+        capture_output=True,
+    )
+    title = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "video"
+    return sanitize_filename(title)
+
+
+def main() -> None:
+    print("=" * 54)
+    print(" YouTube Clipper Termux + Subtitle Otomatis")
+    print("=" * 54)
+
+    url = input("Masukkan URL YouTube target: ").strip()
+    if not url:
+        print("[!] URL tidak boleh kosong.")
+        return
+
+    require_binary("yt-dlp")
+    require_binary("ffmpeg")
+
+    HASIL_DIR.mkdir(exist_ok=True)
+    TEMP_DIR.mkdir(parents=True, exist_ok=True)
+
+    title = get_video_title(url)
+    video_file = TEMP_DIR / f"{title}.mp4"
+    srt_file = TEMP_DIR / f"{title}.srt"
+    clip_file = HASIL_DIR / f"{title}_clip_sub.mp4"
+
+    download_cmd = [
+        "yt-dlp",
+        "-f",
+        "mp4/best",
+        "--write-auto-sub",
+        "--sub-lang",
+        "id,en",
+        "--skip-download",
+        "-o",
+        str(TEMP_DIR / "%(title)s.%(ext)s"),
+        url,
+    ]
+    run_cmd(download_cmd, "Ambil subtitle otomatis YouTube")
+
+    run_cmd(
+        [
+            "yt-dlp",
+            "-f",
+            "mp4/best",
+            "-o",
+            str(video_file),
+            url,
+        ],
+        "Download video",
+    )
+
+    subtitle_vtt = choose_subtitle_file(title)
+    if subtitle_vtt:
+        run_cmd(
+            ["ffmpeg", "-y", "-i", str(subtitle_vtt), str(srt_file)],
+            "Konversi subtitle ke .srt",
+        )
+    else:
+        print("[!] Subtitle otomatis tidak ditemukan. Lanjut tanpa subtitle.")
+
+    ffmpeg_cmd = [
+        "ffmpeg",
+        "-y",
+        "-ss",
+        "0",
+        "-t",
+        str(CLIP_DURATION),
+        "-i",
+        str(video_file),
+    ]
+
+    if srt_file.exists():
+        ffmpeg_cmd += ["-vf", f"subtitles={srt_file.as_posix()}"]
+
+    ffmpeg_cmd += [
+        "-c:v",
+        "libx264",
+        "-c:a",
+        "aac",
+        "-movflags",
+        "+faststart",
+        str(clip_file),
+    ]
+
+    run_cmd(ffmpeg_cmd, "Buat clip 60 detik + burn subtitle")
+
+    print("\n[✓] Selesai!")
+    print(f"    Hasil tersimpan di: {clip_file}")
+
+
+if __name__ == "__main__":
+    main()
 
EOF
)
