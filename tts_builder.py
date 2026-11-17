# -*- coding: utf-8 -*-
"""
Independent TTS & Timeline Builder
Synthesizes speech using edge-tts with 3 Taiwan Neural Voices:
  - 黎光達: zh-TW-YunJheNeural
  - 阮氏英書: zh-TW-HsiaoChenNeural
  - 阮曰黃絨: zh-TW-HsiaoYuNeural
Generates millisecond-accurate subtitles.srt and synced narration track.
"""
import asyncio, glob, json, math, os, subprocess, sys
import edge_tts

ROOT = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(ROOT, "audio")
os.makedirs(AUD, exist_ok=True)

FFMPEG = "/Users/dat/Downloads/2ngay1d/bin/ffmpeg"
FFPROBE = "/Users/dat/Downloads/2ngay1d/bin/ffprobe"

with open(os.path.join(ROOT, "script.json"), "r", encoding="utf-8") as f:
    doc = json.load(f)

VOICE_MAP = {
    "le_quang_dat": "zh-TW-YunJheNeural",
    "nguyen_thi_anh_thu": "zh-TW-HsiaoChenNeural",
    "nguyen_viet_hoang_nhung": "zh-TW-HsiaoYuNeural"
}

def get_audio_duration(file_path):
    try:
        cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file_path]
        out = subprocess.check_output(cmd).decode().strip()
        return float(out)
    except Exception:
        return 0.0

async def synth_scene(scene, sem):
    sid = scene["scene_id"]
    spk = scene["speaker"]
    voice = VOICE_MAP.get(spk, "zh-TW-YunJheNeural")
    mp3_path = os.path.join(AUD, f"scene_{sid:02d}.mp3")
    meta_path = os.path.join(AUD, f"scene_{sid:02d}.json")

    async with sem:
        for attempt in range(4):
            try:
                com = edge_tts.Communicate(scene["text_zh"], voice)
                audio_data = bytearray()
                bounds = []
                async for ch in com.stream():
                    if ch["type"] == "audio":
                        audio_data += ch["data"]
                    elif ch["type"] in ("SentenceBoundary", "WordBoundary"):
                        bounds.append({
                            "start": ch["offset"] / 1e7,
                            "end": (ch["offset"] + ch["duration"]) / 1e7,
                            "text": ch["text"]
                        })
                if not audio_data:
                    raise RuntimeError("No audio data")
                with open(mp3_path, "wb") as f:
                    f.write(audio_data)
                dur = get_audio_duration(mp3_path)
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "scene_id": sid,
                        "voice": voice,
                        "duration": dur,
                        "sentences": bounds
                    }, f, ensure_ascii=False, indent=2)
                print(f"✓ Scene {sid:02d} [{voice}]: {dur:.2f}s ({len(bounds)} segments)")
                return sid, dur
            except Exception as e:
                print(f"Scene {sid:02d} attempt {attempt+1} err: {e}")
                await asyncio.sleep(2 + attempt * 2)
        raise RuntimeError(f"TTS failed for scene {sid}")

def build_timeline():
    FPS = 30
    LEAD = 0.40
    GAP = 1.20
    SLIDE_HOLD = 2.50
    CARD = 3.50
    END_HOLD = 2.0

    SECTION_NAMES = {
        "01 開場": ("第一部分", "開場｜品牌與行程介紹"),
        "02 目標客群": ("第二部分", "客群分析與核心主張"),
        "03 第一天行程": ("第三部分", "Day 1｜十分・九份・基隆夜市"),
        "04 第二天行程": ("第四部分", "Day 2｜野柳・淡水・西門町"),
        "05 財務分析": ("第五部分", "成本結構・定價與利潤"),
        "06 推薦理由": ("第六部分", "推薦理由與圓滿結語"),
    }

    def q(t):
        return math.ceil(t * FPS - 1e-6) / FPS

    items = []
    t = 0.0
    prev_section = None
    scenes = doc["scenes"]

    for s in scenes:
        if s["section"] != prev_section:
            no, name = SECTION_NAMES.get(s["section"], ("章節", s["section"]))
            spk_name = doc["voices"][s["speaker"]]["name_zh"]
            d = q(CARD)
            items.append({
                "type": "card",
                "section": s["section"],
                "label": no,
                "name": name,
                "presenter": spk_name,
                "start": round(t, 4),
                "dur": d
            })
            t += d
            prev_section = s["section"]

        sid = s["scene_id"]
        meta_file = os.path.join(AUD, f"scene_{sid:02d}.json")
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        speech_dur = meta.get("duration", 15.0)

        hold = SLIDE_HOLD if s.get("visual_type") == "slide" else 0.0
        if sid == len(scenes):
            hold += END_HOLD
        dur = q(LEAD + speech_dur + GAP + hold)

        items.append({
            "type": "scene",
            "scene_id": sid,
            "section": s["section"],
            "speaker": s["speaker"],
            "visual_type": s["visual_type"],
            "speech_dur": speech_dur,
            "start": round(t, 4),
            "dur": dur
        })
        t += dur

    total_dur = round(t, 4)
    print(f"\n==========================================")
    print(f"✓ TỔNG THỜI LƯỢNG DỰ KIẾN: {total_dur:.2f}s = {total_dur/60:.2f} phút")
    print(f"  (Đạt chuẩn 15 – 16 phút: {900 <= total_dur <= 960})")
    print(f"==========================================")

    tl_data = {
        "fps": FPS,
        "lead": LEAD,
        "gap": GAP,
        "slide_hold": SLIDE_HOLD,
        "card": CARD,
        "end_hold": END_HOLD,
        "total_dur": total_dur,
        "items": items
    }
    with open(os.path.join(ROOT, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(tl_data, f, ensure_ascii=False, indent=2)

    # Subtitles generator
    def srt_fmt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    srt_lines = []
    idx = 1
    for it in items:
        if it["type"] != "scene":
            continue
        sid = it["scene_id"]
        meta_file = os.path.join(AUD, f"scene_{sid:02d}.json")
        t_base = it["start"] + LEAD
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        sentences = meta.get("sentences", [])
        if not sentences:
            # Fallback to single sentence
            s_text = doc["scenes"][sid-1]["text_zh"]
            srt_lines.append(f"{idx}\n{srt_fmt(t_base)} --> {srt_fmt(t_base + meta['duration'])}\n{s_text}\n")
            idx += 1
        else:
            for sent in sentences:
                t1 = t_base + sent["start"]
                t2 = t_base + sent["end"]
                text = sent["text"].strip()
                if text:
                    srt_lines.append(f"{idx}\n{srt_fmt(t1)} --> {srt_fmt(t2)}\n{text}\n")
                    idx += 1

    srt_content = "\n".join(srt_lines)
    with open(os.path.join(ROOT, "subtitles.srt"), "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"✓ Đã xuất {idx-1} mốc phụ đề vào independent_tour/subtitles.srt")

    # Generate full narration.wav
    build_narration_audio(items)

def build_narration_audio(items):
    print("Đang tạo file âm thanh tổng narration.wav...")
    TMP = os.path.join(ROOT, "audio_segments")
    os.makedirs(TMP, exist_ok=True)
    seg_files = []
    for k, it in enumerate(items):
        seg_wav = os.path.join(TMP, f"seg_{k:03d}.wav")
        dur = it["dur"]
        if it["type"] == "card":
            # Silence
            cmd = [FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", str(dur), seg_wav]
            subprocess.run(cmd, check=True)
        else:
            sid = it["scene_id"]
            mp3_in = os.path.join(AUD, f"scene_{sid:02d}.mp3")
            lead = 0.40
            speech_dur = it["speech_dur"]
            tail = max(0.0, dur - lead - speech_dur)
            # Pad lead silence before, and tail silence after
            cmd = [
                FFMPEG, "-y", "-v", "error",
                "-i", mp3_in,
                "-af", f"adelay=400|400,apad=pad_dur={tail:.3f},aresample=48000",
                "-t", str(dur),
                seg_wav
            ]
            subprocess.run(cmd, check=True)
        seg_files.append(seg_wav)

    # Concat all wav segments
    concat_txt = os.path.join(TMP, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in seg_files:
            f.write(f"file '{p}'\n")

    out_wav = os.path.join(AUD, "narration.wav")
    cmd = [FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:a", "pcm_s16le", out_wav]
    subprocess.run(cmd, check=True)
    final_dur = get_audio_duration(out_wav)
    print(f"✓ File narration.wav hoàn tất: {final_dur:.2f}s ({final_dur/60:.2f} phút) tại {out_wav}")

async def run_all():
    sem = asyncio.Semaphore(4)
    tasks = [synth_scene(s, sem) for s in doc["scenes"]]
    await asyncio.gather(*tasks)

def main():
    print("=== [BƯỚC 3/6] TỔNG HỢP GIỌNG ĐỌC AI ĐỘC LẬP ===")
    asyncio.run(run_all())
    build_timeline()
    print("=== BƯỚC 3 HOÀN TẤT THÀNH CÔNG ===")

if __name__ == "__main__":
    main()
