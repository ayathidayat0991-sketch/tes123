 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..3aefea1e49db3e268ff639c98aa4050b5305f574
--- /dev/null
+++ b/README.md
@@ -0,0 +1,28 @@
+# Tools Termux YouTube Clipper + Auto Subtitle
+
+Script Python sederhana untuk:
+- Download video dari URL YouTube
+- Ambil subtitle otomatis YouTube (prioritas Bahasa Indonesia, fallback Inggris)
+- Buat clip 60 detik pertama
+- Burn subtitle ke video
+- Simpan hasil ke folder `Hasil/`
+
+## Install (Termux)
+
+```bash
+pkg update && pkg install python ffmpeg
+pip install yt-dlp
+```
+
+## Jalankan
+
+```bash
+python clipper_termux.py
+```
+
+Lalu tinggal paste URL YouTube target.
+
+## Output
+
+- File hasil: `Hasil/<judul_video>_clip_sub.mp4`
+- Folder sementara: `Hasil/_temp/`
 
EOF
)
