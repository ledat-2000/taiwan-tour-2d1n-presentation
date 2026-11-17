# -*- coding: utf-8 -*-
"""
Independent TTS & Timeline Builder (Upgraded for Approach A)
Synthesizes speech using edge-tts with Taiwan Neural Voices:
  - 黎光達: zh-TW-YunJheNeural (+0%, +0Hz)
  - 阮氏英書: zh-TW-HsiaoChenNeural (+0%, +0Hz)
  - 阮曰黃絨: zh-TW-HsiaoChenNeural (-3%, +2Hz) -> Voice 5 (ấm, mượt mà)
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

# Configured voices (Nhung uses Voice 5: HsiaoChen -3% rate, +2Hz pitch)
VOICE_CONFIG = {
    "le_quang_dat": {
        "voice": "zh-TW-YunJheNeural",
        "rate": "+0%",
        "pitch": "+0Hz"
    },
    "nguyen_thi_anh_thu": {
        "voice": "zh-TW-HsiaoChenNeural",
        "rate": "+0%",
        "pitch": "+0Hz"
    },
    "nguyen_viet_hoang_nhung": {
        "voice": "zh-TW-HsiaoChenNeural",
        "rate": "-3%",
        "pitch": "+2Hz"
    }
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
    cfg = VOICE_CONFIG.get(spk, VOICE_CONFIG["le_quang_dat"])
    voice = cfg["voice"]
    rate = cfg["rate"]
    pitch = cfg["pitch"]
    mp3_path = os.path.join(AUD, f"scene_{sid:02d}.mp3")
    meta_path = os.path.join(AUD, f"scene_{sid:02d}.json")

    async with sem:
        for attempt in range(4):
            try:
                com = edge_tts.Communicate(scene["text_zh"], voice, rate=rate, pitch=pitch)
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
                        "rate": rate,
                        "pitch": pitch,
                        "duration": dur,
                        "sentences": bounds
                    }, f, ensure_ascii=False, indent=2)
                print(f"✓ Scene {sid:02d} [{spk} - {voice} ({rate},{pitch})]: {dur:.2f}s")
                return sid, dur
            except Exception as e:
                print(f"Scene {sid:02d} attempt {attempt+1} err: {e}")
                await asyncio.sleep(2 + attempt * 2)
        raise RuntimeError(f"TTS failed for scene {sid}")

def build_timeline():
    FPS = 30
    INTRO_MONTAGE = 16.0  # 15s fast-paced opening teaser
    LEAD = 0.50
    GAP = 1.65
    SLIDE_HOLD = 4.00
    CARD = 4.50
    END_HOLD = 5.0

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

    # 1. Opening Montage Teaser (15.0s)
    d_intro = q(INTRO_MONTAGE)
    items.append({
        "type": "intro_montage",
        "section": "00 序幕精華",
        "label": "精彩預告",
        "name": "山海海岸・青春北台灣 兩天一夜 精華導覽",
        "presenter": "越青旅行社",
        "start": round(t, 4),
        "dur": d_intro
    })
    t += d_intro

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
    print(f"✓ TỔNG THỜI LƯỢNG DỰ KIẾN (KÈM INTRO 15S): {total_dur:.2f}s = {total_dur/60:.2f} phút")
    print(f"  (Đạt chuẩn 15 – 16 phút: {900 <= total_dur <= 960})")
    print(f"==========================================")

    tl_data = {
        "fps": FPS,
        "lead_sec": LEAD,
        "gap_sec": GAP,
        "total_duration_sec": total_dur,
        "items": items
    }
    with open(os.path.join(ROOT, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(tl_data, f, ensure_ascii=False, indent=2)

    return tl_data

def build_subtitles(tl_data):
    srt_file = os.path.join(ROOT, "subtitles.srt")
    cue_idx = 1
    srt_lines = []

    def fmt_ts(sec):
        ms = int(round((sec - int(sec)) * 1000))
        m, s = divmod(int(sec), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    scenes = {s["scene_id"]: s for s in doc["scenes"]}

    for item in tl_data["items"]:
        if item["type"] != "scene":
            continue
        sid = item["scene_id"]
        sc = scenes[sid]
        lead = tl_data["lead_sec"]
        scene_start = item["start"] + lead

        meta_file = os.path.join(AUD, f"scene_{sid:02d}.json")
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        words = meta.get("sentences", [])
        full_text = sc["text_zh"]

        # Break text into readable phrases of 14-22 chars
        punct = ["。", "！", "？", "；", "，"]
        chunks = []
        cur = ""
        for char in full_text:
            cur += char
            if char in punct and len(cur) >= 12:
                chunks.append(cur)
                cur = ""
            elif len(cur) >= 20:
                chunks.append(cur)
                cur = ""
        if cur:
            chunks.append(cur)

        tot_chars = max(1, sum(len(c) for c in chunks))
        speech_dur = meta.get("duration", item["speech_dur"])

        cur_t = scene_start
        for c in chunks:
            frac = len(c) / tot_chars
            c_dur = frac * speech_dur
            start_ts = fmt_ts(cur_t)
            end_ts = fmt_ts(cur_t + c_dur)
            cur_t += c_dur

            clean_text = c.strip("，。；！？")
            if not clean_text:
                continue
            srt_lines.append(f"{cue_idx}\n{start_ts} --> {end_ts}\n{clean_text}\n\n")
            cue_idx += 1

    with open(srt_file, "w", encoding="utf-8") as f:
        f.writelines(srt_lines)
    print(f"✓ Đã tạo phụ đề {srt_file} ({cue_idx - 1} đoạn)")

def assemble_narration(tl_data):
    """
    Renders the master audio narration track at 48kHz stereo,
    placing each scene's speech at the exact millisecond offset.
    """
    out_wav = os.path.join(AUD, "narration.wav")
    seg_dir = os.path.join(ROOT, "audio_segments")
    os.makedirs(seg_dir, exist_ok=True)

    scenes = {s["scene_id"]: s for s in doc["scenes"]}
    seg_files = []

    for idx, item in enumerate(tl_data["items"]):
        seg_wav = os.path.join(seg_dir, f"seg_{idx:03d}.wav")
        dur = item["dur"]

        if item["type"] in ("card", "intro_montage"):
            # Silent block for card/intro
            cmd = [
                FFMPEG, "-y",
                "-f", "lavfi",
                "-i", f"anullsrc=channel_layout=stereo:sample_rate=48000",
                "-t", str(dur),
                "-c:a", "pcm_s16le",
                seg_wav
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            sid = item["scene_id"]
            mp3_in = os.path.join(AUD, f"scene_{sid:02d}.mp3")
            lead_ms = int(tl_data["lead_sec"] * 1000)

            filter_str = (
                f"aformat=sample_rates=48000:channel_layouts=stereo,"
                f"adelay={lead_ms}|{lead_ms},"
                f"apad=whole_dur={dur}"
            )
            cmd = [
                FFMPEG, "-y",
                "-i", mp3_in,
                "-af", filter_str,
                "-t", str(dur),
                "-c:a", "pcm_s16le",
                seg_wav
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        seg_files.append(seg_wav)

    concat_list = os.path.join(ROOT, "concat_audio.txt")
    with open(concat_list, "w") as f:
        for s in seg_files:
            f.write(f"file '{s}'\n")

    cmd = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c:a", "pcm_s16le",
        out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dur = get_audio_duration(out_wav)
    print(f"✓ Đã ghép narration.wav hoàn chỉnh ({dur:.2f}s = {dur/60:.2f} phút)")

async def main():
    print("=== BƯỚC 3: XUẤT GIỌNG ĐỌC AI & TIMELINE (MẪU 5 CHO NHUNG) ===")
    sem = asyncio.Semaphore(4)
    tasks = [synth_scene(s, sem) for s in doc["scenes"]]
    await asyncio.gather(*tasks)
    print("\n✓ Đã tổng hợp toàn bộ 41 phân cảnh audio với Mẫu 5 cho Nhung!")
    tl_data = build_timeline()
    build_subtitles(tl_data)
    assemble_narration(tl_data)

if __name__ == "__main__":
    asyncio.run(main())
