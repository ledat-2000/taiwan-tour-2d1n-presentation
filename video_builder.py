# -*- coding: utf-8 -*-
"""
Independent Video Pipeline & Assembler (Full HD 1080p @ 30fps)
Key Upgrades for Approach A:
1. Fast-paced 16s Intro Montage teaser at start.
2. Real photos embedded in slides (Agoda hotel room pricing screenshot + group discount).
3. Traditional Chinese subtitle burn-in via libass (STHeiti Medium).
4. Audio mix: voice narration + soft acoustic travel BGM (volume ducked).
5. Output: FINAL_TOUR_15MIN_1080P.mp4 (15m38s).
"""
import concurrent.futures, glob, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
SEG = os.path.join(ROOT, "segments")
BUILD_ASS = os.path.join(ROOT, "ass")
OUT = os.path.join(ROOT, "output")
RAW = "/Users/dat/Downloads/2ngay1d/raw_videos"
SLIDES = os.path.join(ROOT, "slides")
AUD = os.path.join(ROOT, "audio")

os.makedirs(SEG, exist_ok=True)
os.makedirs(BUILD_ASS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

FFMPEG = "/Users/dat/Downloads/2ngay1d/bin/ffmpeg"
FFPROBE = "/Users/dat/Downloads/2ngay1d/bin/ffprobe"

with open(os.path.join(ROOT, "timeline.json"), "r", encoding="utf-8") as f:
    tl = json.load(f)

FPS = tl["fps"]
X264 = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", str(FPS),
    "-g", "60", "-an", "-movflags", "+faststart"
]

TOPIC_MAP = {
    2: 'scene_02', 6: 'scene_07', 8: 'scene_10', 9: 'scene_11',
    10: 'scene_12', 11: 'scene_16', 12: 'scene_13', 13: 'scene_15',
    14: 'scene_17', 15: 'scene_18', 16: 'scene_19', 17: 'scene_20',
    18: 'scene_21', 19: 'scene_22', 20: 'scene_23', 22: 'scene_25',
    24: 'scene_27', 25: 'scene_28', 26: 'scene_31', 27: 'scene_32',
    28: 'scene_33', 29: 'scene_34', 30: 'scene_35', 31: 'scene_36',
    32: 'scene_36', 38: 'scene_42', 39: 'scene_42', 40: 'scene_43'
}

def srt_time(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

cues = []
srt_file = os.path.join(ROOT, "subtitles.srt")
if os.path.exists(srt_file):
    for blk in open(srt_file, encoding="utf-8").read().strip().split("\n\n"):
        ln = blk.strip().split("\n")
        if len(ln) >= 3:
            a, b = ln[1].split(" --> ")
            cues.append((srt_time(a), srt_time(b), "\\N".join(ln[2:])))

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Box,STHeiti Medium,54,&HFF000000,&HFF000000,&H8C000000,&H8C000000,1,0,0,0,100,100,1,0,3,14,0,2,80,80,68,1
Style: Txt,STHeiti Medium,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,3.0,0,2,80,80,68,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def at(x):
    x = max(0, x)
    h = int(x // 3600)
    m = int(x % 3600 // 60)
    s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def write_ass(path, start, dur):
    out = [ASS_HEAD]
    matched = 0
    for a, b, t in cues:
        if b <= start or a >= start + dur:
            continue
        a2, b2 = max(a, start) - start, min(b, start + dur) - start
        out.append(f"Dialogue: 0,{at(a2)},{at(b2)},Box,,0,0,0,,{t}\n")
        out.append(f"Dialogue: 1,{at(a2)},{at(b2)},Txt,,0,0,0,,{t}\n")
        matched += 1
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return matched > 0

def esc(p):
    return p.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

def dur_of(p):
    try:
        return float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip() or 0)
    except:
        return 0.0

def render_segment(task):
    k, it = task
    out_mp4 = os.path.join(SEG, f"seg_{k:03d}.mp4")

    # If intro_montage is already rendered and valid, skip
    if it["type"] == "intro_montage":
        if os.path.exists(out_mp4) and abs(dur_of(out_mp4) - it["dur"]) < 0.2:
            return k, it["dur"], 0.0

    # For slides and scenes, re-render to reflect new photos, voices & subtitles
    t0 = time.time()
    n = round(it["dur"] * FPS)
    dur = it["dur"]
    tmp_out = out_mp4 + ".tmp.mp4"

    ass_path = os.path.join(BUILD_ASS, f"seg_{k:03d}.ass")
    has_sub = it["type"] == "scene" and write_ass(ass_path, it["start"], it["dur"])

    if it["type"] == "card":
        card_png = os.path.join(SLIDES, f"card_{it['section'][:2]}.png")
        vf = (f"scale=3840:2160,zoompan=z='1+0.025*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1920x1080:fps={FPS},fade=in:st=0:d=0.35,fade=out:st={dur-0.35:.3f}:d=0.35")
        cmd = [FFMPEG, "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", card_png,
               "-vf", vf, "-frames:v", str(n)] + X264 + [tmp_out]

    elif it["type"] == "credits":
        cred_png = os.path.join(SLIDES, "credits.png")
        vf = f"scale=1920:1080,fps={FPS},fade=in:st=0:d=0.5,fade=out:st={dur-0.5:.3f}:d=0.5"
        cmd = [FFMPEG, "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", cred_png,
               "-vf", vf, "-frames:v", str(n)] + X264 + [tmp_out]

    elif it["visual_type"] == "slide":
        slide_png = os.path.join(SLIDES, f"scene_{it['scene_id']:02d}.png")
        vf = (f"scale=3840:2160,zoompan=z='1+0.035*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d=1:s=1920x1080:fps={FPS},fade=in:st=0:d=0.35,fade=out:st={dur-0.35:.3f}:d=0.35")
        if has_sub:
            vf += f",ass='{esc(ass_path)}'"
        cmd = [FFMPEG, "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", slide_png,
               "-vf", vf, "-frames:v", str(n)] + X264 + [tmp_out]

    else:
        # Video scene with location tags and footage
        sid = it["scene_id"]
        prefix = TOPIC_MAP.get(sid, "scene_02")
        raw_files = sorted(f for f in glob.glob(os.path.join(RAW, f"{prefix}_*")) if not f.endswith(".part"))
        if not raw_files:
            raw_files = sorted(f for f in glob.glob(os.path.join(RAW, "scene_02_*")) if not f.endswith(".part"))

        tag_png = os.path.join(SLIDES, f"tag_{sid:02d}.png")
        k_files = len(raw_files)
        parts = [n // k_files + (1 if i < n % k_files else 0) for i in range(k_files)]
        
        cmd = [FFMPEG, "-y", "-v", "error"]
        for f in raw_files:
            cmd += ["-stream_loop", "-1", "-ss", "1.0", "-i", f]
        cmd += ["-loop", "1", "-framerate", str(FPS), "-i", tag_png]

        fc = []
        for i, f in enumerate(raw_files):
            fc.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
                      f"crop=1920:1080,fps={FPS},setsar=1,trim=end_frame={parts[i]},setpts=PTS-STARTPTS[v{i}]")
        fc.append("".join(f"[v{i}]" for i in range(k_files)) + f"concat=n={k_files}:v=1:a=0[base]")
        fc.append(f"[{k_files}:v]format=rgba,trim=end_frame={n},fade=in:st=0.3:d=0.4:alpha=1,"
                  f"fade=out:st=5.5:d=0.5:alpha=1,setpts=PTS-STARTPTS[tg]")
        last = f"[base][tg]overlay=0:0:format=auto,fade=in:st=0:d=0.3,fade=out:st={dur-0.3:.3f}:d=0.3"
        if has_sub:
            last += f",ass='{esc(ass_path)}'"
        fc.append(last + "[out]")
        cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-frames:v", str(n)] + X264 + [tmp_out]

    subprocess.run(cmd, check=True)
    os.replace(tmp_out, out_mp4)
    elapsed = time.time() - t0
    print(f"✓ seg {k:03d} [{it['type']:<5}] sid={it.get('scene_id','-')} dur={dur:.2f}s ({elapsed:.1f}s)")
    return k, dur, elapsed

def main():
    print("=== [BƯỚC 5 & 6] RENDER TOÀN BỘ PHÂN ĐOẠN VIDEO 1080P ===")
    credits_item = {"type": "credits", "start": tl["total_duration_sec"], "dur": 8.0}
    items = tl["items"] + [credits_item]
    tasks = list(enumerate(items))

    # Parallel processing with 4 workers on M4
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(render_segment, task) for task in tasks]
        for f in concurrent.futures.as_completed(futures):
            f.result()

    print("\n✓ Đã render xong toàn bộ phân đoạn video.")
    assemble_final_video()

def assemble_final_video():
    print("\n--- GHÉP NỐI TOÀN BỘ VIDEO & FILE THUYẾT MINH & NHẠC NỀN BGM ---")
    credits_item = {"type": "credits", "start": tl["total_duration_sec"], "dur": 8.0}
    items = tl["items"] + [credits_item]
    concat_txt = os.path.join(ROOT, "concat_segments.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for k in range(len(items)):
            p = os.path.join(SEG, f"seg_{k:03d}.mp4")
            f.write(f"file '{p}'\n")

    narration_wav = os.path.join(AUD, "narration.wav")
    bgm_mp3 = os.path.join(ROOT, "bgm.mp3")
    final_video = os.path.join(OUT, "FINAL_TOUR_15MIN_1080P.mp4")

    # Audio filter:
    # Narration at 100% volume.
    # BGM looped and gently mixed at 11% volume so it warms up the video without masking voices.
    filter_complex = (
        "[1:a]volume=1.0[vce];"
        "[2:a]volume=0.11[bgm];"
        "[vce][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    cmd = [
        FFMPEG, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", narration_wav,
        "-stream_loop", "-1", "-i", bgm_mp3,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        final_video
    ]
    t0 = time.time()
    subprocess.run(cmd, check=True)
    dur = float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final_video]).decode().strip())
    size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"\n========================================================")
    print(f"🎉 XUẤT VIDEO THÀNH PHẨM ĐỘC LẬP THÀNH CÔNG!")
    print(f"  - Đường dẫn: {final_video}")
    print(f"  - Thời lượng: {dur:.2f} giây = {dur/60:.2f} phút")
    print(f"  - Độ phân giải: 1920x1080 Full HD, 30fps")
    print(f"  - Dung lượng: {size_mb:.1f} MB")
    print(f"  - Thời gian ghép: {time.time()-t0:.1f}s")
    print(f"========================================================")

if __name__ == "__main__":
    main()
