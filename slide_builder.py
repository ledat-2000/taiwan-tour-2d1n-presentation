# -*- coding: utf-8 -*-
"""
Upgraded Slide Builder (1920x1080 Full HD with Real Photos)
Key Enhancements:
1. Authentic photographic inserts for every price and location.
2. Agoda/Booking real hotel room pricing screenshot + group discount negotiation note.
3. Clean modern luxury typography (macOS STHeiti Medium).
4. Full transparent data source footers.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "slides")
PHOTOS = os.path.join(ROOT, "real_photos")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(ROOT, "script.json"), "r", encoding="utf-8") as f:
    doc = json.load(f)

FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"

def font(size):
    return ImageFont.truetype(FONT_PATH, size)

W, H = 1920, 1080
BG = (248, 250, 252)         # Slate 50
NAVY = (15, 23, 42)          # Slate 900
DARK_TEAL = (13, 148, 136)   # Teal 600
LIGHT_TEAL = (204, 251, 241) # Teal 100
AMBER = (217, 119, 6)        # Amber 600
LIGHT_AMBER = (254, 243, 199)# Amber 100
WHITE = (255, 255, 255)
BORDER = (226, 232, 240)     # Slate 200
MUTED = (100, 116, 139)      # Slate 500

SRC_TEXT = "資料來源：台鐵官網、台灣好行官網、新北客運、野柳地質公園官網、Agoda 2026/11 實際查詢價格"

def draw_header(d, category, title):
    d.rectangle([0, 0, W, 14], fill=DARK_TEAL)
    d.text((100, 48), "越青旅行社｜山海海岸·青春北台灣 兩天一夜", fill=MUTED, font=font(26))
    if category:
        d.rounded_rectangle([100, 92, 260, 138], radius=8, fill=LIGHT_TEAL)
        d.text((118, 103), category, fill=DARK_TEAL, font=font(24))
        d.text((280, 88), title, fill=NAVY, font=font(48))
    else:
        d.text((100, 88), title, fill=NAVY, font=font(48))

def draw_footer(d):
    d.line([(100, 995), (1820, 995)], fill=BORDER, width=2)
    d.text((100, 1012), SRC_TEXT, fill=MUTED, font=font(21))

def paste_photo(base_im, photo_name, box, radius=12, label="", price=""):
    """Pastes a real photo thumbnail with rounded corners and optional price badge."""
    p_path = os.path.join(PHOTOS, photo_name)
    if not os.path.exists(p_path):
        return
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    try:
        raw_im = Image.open(p_path).convert("RGB")
        fitted = ImageOps.fit(raw_im, (w, h), Image.Resampling.LANCZOS)
        
        # Rounded mask
        mask = Image.new("L", (w, h), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
        
        base_im.paste(fitted, (x0, y0), mask)
        d = ImageDraw.Draw(base_im)
        # Outline
        d.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=BORDER, width=2)
        
        # Bottom label bar if provided
        if label or price:
            bar_h = 42
            d.rectangle([x0, y1 - bar_h, x1, y1], fill=(15, 23, 42))
            if label:
                d.text((x0 + 12, y1 - bar_h + 9), label, fill=WHITE, font=font(18))
            if price:
                d.text((x1 - 100, y1 - bar_h + 8), price, fill=AMBER, font=font(20))
    except Exception as e:
        print(f"Err pasting photo {photo_name}: {e}")

def render_cards():
    cards = [
        ("01", "第一部分", "品牌與行程總覽", "黎光達｜組長"),
        ("02", "第二部分", "客群分析與核心訴求", "黎光達｜組長"),
        ("03", "第三部分", "Day 1 經典山城鐵道與夜市", "阮氏英書｜組員"),
        ("04", "第四部分", "Day 2 北海岸奇岩·夕陽與商圈", "阮曰黃絨｜組員"),
        ("05", "第五部分", "成本結構·定價與利潤分析", "阮曰黃絨｜組員"),
        ("06", "第六部分", "推薦理由與圓滿結語", "黎光達｜組長"),
    ]
    for cid, no, title, presenter in cards:
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 16], fill=DARK_TEAL)
        d.text((120, 100), "越青旅行社·青春北台灣專題報告", fill=MUTED, font=font(32))
        
        # Center card container
        d.rounded_rectangle([200, 260, 1720, 820], radius=24, fill=WHITE, outline=BORDER, width=2)
        d.rounded_rectangle([260, 320, 420, 380], radius=12, fill=LIGHT_AMBER)
        d.text((285, 335), no, fill=AMBER, font=font(34))
        
        d.text((260, 420), title, fill=NAVY, font=font(72))
        d.text((260, 540), "山城鐵道 ✕ 奇岩地質 ✕ 浪漫夕陽 ✕ 流行商圈", fill=DARK_TEAL, font=font(38))
        
        d.rounded_rectangle([260, 660, 600, 740], radius=16, fill=LIGHT_TEAL)
        d.text((290, 685), f"主講人：{presenter}", fill=DARK_TEAL, font=font(34))
        draw_footer(d)
        im.save(os.path.join(OUT, f"card_{cid}.png"))
    print("✓ Đã render 6 thẻ phân đoạn card_01 -> card_06")

def render_slides():
    scenes = doc["scenes"]
    for s in scenes:
        if s.get("visual_type") != "slide":
            continue
        sid = s["scene_id"]
        sc = s.get("slide_content", {})
        layout = sc.get("layout", "card")
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)

        if layout == "hero_title":
            draw_header(d, "遊程企劃", sc.get("title", ""))
            d.rounded_rectangle([100, 170, 1820, 940], radius=24, fill=WHITE, outline=BORDER, width=2)
            d.text((150, 220), "山海海岸·青春北台灣 兩天一夜", fill=NAVY, font=font(64))
            d.text((150, 310), "專為第一次來台灣的越南年輕人量身打造：好玩、好拍、價格透明", fill=DARK_TEAL, font=font(34))
            
            # Photo strip preview
            paste_photo(im, "shifen_lantern.jpg", (150, 380, 640, 650), radius=16, label="十分鐵道天燈祈願")
            paste_photo(im, "amei_teahouse.jpg", (670, 380, 1160, 650), radius=16, label="九份山城阿妹茶樓夕照")
            paste_photo(im, "yehliu_queen.jpg", (1190, 380, 1680, 650), radius=16, label="野柳地質公園女王頭")
            
            # Summary bar
            d.rounded_rectangle([150, 680, 1680, 890], radius=16, fill=(241, 245, 249))
            d.text((180, 710), "【遊程三大核心保障】", fill=NAVY, font=font(30))
            d.text((180, 765), "• 交通全透明：台鐵區間車、平溪支線、台灣好行皇冠北海岸線全程串聯，絕無強迫購物站", fill=MUTED, font=font(26))
            d.text((180, 815), "• 雙語領隊隨行：合法旅宿、百萬保險與在地美食一應俱全，專案定價 NT$ 3,600 / 人", fill=MUTED, font=font(26))

        elif layout == "team_cards":
            draw_header(d, "團隊介紹", sc.get("title", ""))
            cards = sc.get("cards", [])
            cx = 100
            for c in cards:
                d.rounded_rectangle([cx, 200, cx + 520, 930], radius=20, fill=WHITE, outline=BORDER, width=2)
                d.rounded_rectangle([cx + 40, 240, cx + 220, 290], radius=8, fill=LIGHT_AMBER)
                d.text((cx + 55, 252), c["role"], fill=AMBER, font=font(24))
                d.text((cx + 40, 320), c["name"], fill=NAVY, font=font(46))
                d.line([(cx + 40, 395), (cx + 480, 395)], fill=BORDER, width=2)
                
                lines = c["desc"].split("·")
                ly = 430
                d.text((cx + 40, ly), "負責領域：", fill=DARK_TEAL, font=font(28))
                ly += 50
                for line in lines:
                    d.text((cx + 60, ly), f"• {line}", fill=MUTED, font=font(26))
                    ly += 50
                cx += 550

        elif layout in ("persona", "pillars"):
            draw_header(d, "市場分析", sc.get("title", ""))
            items = sc.get("items") or sc.get("pillars") or []
            iy = 200
            for it in items:
                d.rounded_rectangle([100, iy, 1820, iy + 215], radius=18, fill=WHITE, outline=BORDER, width=2)
                tag = it.get("tag") or it.get("name")
                desc = it.get("val") or it.get("desc")
                d.rounded_rectangle([140, iy + 40, 420, iy + 110], radius=12, fill=LIGHT_TEAL)
                d.text((160, iy + 55), tag, fill=DARK_TEAL, font=font(30))
                d.text((460, iy + 57), desc, fill=NAVY, font=font(32))
                iy += 245

        elif layout == "route_map":
            draw_header(d, "路網動線", sc.get("title", ""))
            d.rounded_rectangle([100, 200, 1820, 520], radius=20, fill=WHITE, outline=BORDER, width=2)
            d.rounded_rectangle([140, 240, 280, 295], radius=8, fill=LIGHT_AMBER)
            d.text((165, 252), "DAY 1", fill=AMBER, font=font(28))
            d.text((310, 250), "經典山城與港灣夜市", fill=NAVY, font=font(34))
            d.text((140, 350), sc.get("day1", ""), fill=DARK_TEAL, font=font(38))
            
            d.rounded_rectangle([100, 560, 1820, 880], radius=20, fill=WHITE, outline=BORDER, width=2)
            d.rounded_rectangle([140, 600, 280, 655], radius=8, fill=LIGHT_TEAL)
            d.text((165, 612), "DAY 2", fill=DARK_TEAL, font=font(28))
            d.text((310, 610), "地質奇觀·海景公路·歷史夕陽·潮流圈", fill=NAVY, font=font(34))
            d.text((140, 710), sc.get("day2", ""), fill=AMBER, font=font(38))

        elif layout == "day_table":
            # Day 1 & Day 2 Schedule Tables with Real Photos!
            draw_header(d, sc.get("day", "行程表"), sc.get("title", ""))
            rows = sc.get("rows", [])
            
            # Left side: Compact Table (100 to 1340)
            ty = 175
            d.rounded_rectangle([100, ty, 1340, ty + 50], radius=8, fill=(241, 245, 249))
            d.text((120, ty + 14), "時間", fill=MUTED, font=font(20))
            d.text((215, ty + 14), "目的地 / 站點", fill=MUTED, font=font(20))
            d.text((540, ty + 14), "交通路線", fill=MUTED, font=font(20))
            d.text((820, ty + 14), "費用", fill=MUTED, font=font(20))
            d.text((950, ty + 14), "亮點與活動", fill=MUTED, font=font(20))
            ty += 56

            for r in rows:
                d.rounded_rectangle([100, ty, 1340, ty + 52], radius=6, fill=WHITE, outline=BORDER, width=1)
                d.text((120, ty + 15), r["time"], fill=NAVY, font=font(19))
                d.text((215, ty + 15), r["dest"], fill=NAVY, font=font(19))
                
                # Transit badge
                d.rounded_rectangle([535, ty + 10, 790, ty + 42], radius=6, fill=LIGHT_TEAL)
                d.text((545, ty + 14), r["trans"], fill=DARK_TEAL, font=font(17))
                
                d.text((820, ty + 13), r["cost"], fill=AMBER, font=font(21))
                d.text((950, ty + 15), r["activity"], fill=MUTED, font=font(18))
                ty += 58

            # Right side: 3 Authentic Photos with price tags (1370 to 1820)
            if "DAY 1" in sc.get("day", "").upper():
                paste_photo(im, "shifen_lantern.jpg", (1380, 180, 1820, 420), label="十分天燈祈願", price="NT$ 200/4人")
                paste_photo(im, "amei_teahouse.jpg", (1380, 445, 1820, 685), label="九份芋圓與阿妹茶樓", price="NT$ 60")
                paste_photo(im, "keelung_nightmarket.jpg", (1380, 710, 1820, 950), label="基隆廟口鼎邊趖美食", price="NT$ 250")
            else:
                paste_photo(im, "yehliu_queen.jpg", (1380, 180, 1820, 420), label="野柳女王頭門票", price="NT$ 120")
                paste_photo(im, "tamsui_sunset.jpg", (1380, 445, 1820, 685), label="淡水情人橋夕陽渡輪", price="NT$ 60")
                paste_photo(im, "ximending_rainbow.jpg", (1380, 710, 1820, 950), label="西門町商圈與伴手禮", price="NT$ 250")

        elif layout in ("cost_table", "total_cost"):
            # Financial Cost Slides with Agoda Screenshot embedded!
            draw_header(d, "財務會計", sc.get("title", ""))
            items = sc.get("items") or sc.get("rows") or []
            
            # Left side: Cost table (100 to 920)
            ty = 190
            for it in items:
                d.rounded_rectangle([100, ty, 920, ty + 115], radius=14, fill=WHITE, outline=BORDER, width=2)
                cat = it.get("cat") or it.get("item")
                det = it.get("detail", "")
                amt = it.get("amount") or it.get("val")
                
                d.text((130, ty + 20), cat, fill=NAVY, font=font(30))
                if det:
                    d.text((130, ty + 65), det, fill=MUTED, font=font(20))
                d.rounded_rectangle([720, ty + 28, 890, ty + 85], radius=8, fill=LIGHT_AMBER)
                d.text((735, ty + 38), amt, fill=AMBER, font=font(28))
                ty += 130

            total_label = sc.get("subtotal") or sc.get("grand_total")
            if total_label:
                d.rounded_rectangle([100, ty + 10, 920, ty + 95], radius=14, fill=DARK_TEAL)
                d.text((130, ty + 32), total_label, fill=WHITE, font=font(32))

            # Right side: Agoda Hotel Screenshot with Group Discount note (960 to 1820)
            agoda_p = os.path.join(PHOTOS, "agoda_hotel_screenshot.png")
            if os.path.exists(agoda_p):
                raw_agoda = Image.open(agoda_p).convert("RGB")
                fitted_agoda = ImageOps.fit(raw_agoda, (860, 500), Image.Resampling.LANCZOS)
                mask = Image.new("L", (860, 500), 0)
                ImageDraw.Draw(mask).rounded_rectangle([0, 0, 860, 500], radius=16, fill=255)
                im.paste(fitted_agoda, (960, 190), mask)
                d.rounded_rectangle([960, 190, 1820, 690], radius=16, outline=BORDER, width=2)

            # Below Agoda screenshot: Real photos of food & entrance tickets
            paste_photo(im, "keelung_food.jpg", (960, 715, 1370, 935), label="野柳鮮魚合菜", price="NT$ 350")
            paste_photo(im, "shifen_waterfall.jpg", (1410, 715, 1820, 935), label="平溪線週遊券", price="NT$ 80")

        elif layout == "pricing_matrix":
            draw_header(d, "收益模型", sc.get("title", ""))
            metrics = sc.get("metrics", [])
            mx = 100
            for m in metrics:
                d.rounded_rectangle([mx, 190, mx + 390, 480], radius=18, fill=WHITE, outline=BORDER, width=2)
                d.rounded_rectangle([mx + 25, 220, mx + 180, 265], radius=6, fill=LIGHT_TEAL)
                d.text((mx + 40, 232), m["badge"], fill=DARK_TEAL, font=font(22))
                d.text((mx + 25, 300), m["label"], fill=MUTED, font=font(26))
                d.text((mx + 25, 370), m["num"], fill=NAVY, font=font(48))
                mx += 430

            # Formula card
            d.rounded_rectangle([100, 520, 1820, 660], radius=16, fill=LIGHT_AMBER, outline=AMBER, width=2)
            d.text((150, 565), sc.get("formula", ""), fill=AMBER, font=font(36))
            
            d.rounded_rectangle([100, 690, 1820, 810], radius=16, fill=WHITE, outline=BORDER, width=2)
            d.text((150, 735), sc.get("group_profit", ""), fill=DARK_TEAL, font=font(36))

            # Group discount note banner
            d.rounded_rectangle([100, 840, 1820, 940], radius=14, fill=LIGHT_TEAL)
            d.text((150, 872), "★ 團體洽談備忘：16人以上成團可享飯店住宿與餐廳 9 折優惠，每團可額外增加 NT$ 1,120 彈性利潤空間", fill=DARK_TEAL, font=font(24))

        elif layout == "comparison":
            draw_header(d, "價值優勢", sc.get("title", ""))
            comp = sc.get("compare", [])
            d.rounded_rectangle([100, 190, 1820, 250], radius=10, fill=(241, 245, 249))
            d.text((140, 210), "比較維度", fill=MUTED, font=font(24))
            d.text((450, 210), "旅客自行規劃自由行 (痛點與隱形成本)", fill=AMBER, font=font(24))
            d.text((1140, 210), "越青旅行社 青春北台灣遊程 (專屬價值)", fill=DARK_TEAL, font=font(24))
            
            cy = 270
            for c in comp:
                d.rounded_rectangle([100, cy, 1820, cy + 125], radius=12, fill=WHITE, outline=BORDER, width=1)
                d.rounded_rectangle([130, cy + 32, 340, cy + 88], radius=8, fill=LIGHT_TEAL)
                d.text((150, cy + 45), c["dim"], fill=DARK_TEAL, font=font(26))
                d.text((450, cy + 45), c["self"], fill=MUTED, font=font(26))
                d.text((1140, cy + 45), c["us"], fill=NAVY, font=font(26))
                cy += 140

        elif layout == "closing":
            draw_header(d, "結語", sc.get("title", ""))
            d.rounded_rectangle([100, 190, 1820, 930], radius=24, fill=WHITE, outline=BORDER, width=2)
            d.text((150, 250), "你會想參加這個行程嗎？", fill=NAVY, font=font(60))
            d.text((150, 345), "越青旅行社｜陪伴每一位青年探索最精彩、最道地的台灣", fill=DARK_TEAL, font=font(34))
            d.line([(150, 430), (1770, 430)], fill=BORDER, width=2)
            
            ax = 150
            for a in sc.get("authors", []):
                d.rounded_rectangle([ax, 470, ax + 480, 650], radius=16, fill=(248, 250, 252), outline=BORDER, width=1)
                d.text((ax + 40, 510), a["name"], fill=NAVY, font=font(40))
                d.text((ax + 40, 580), a["title"], fill=MUTED, font=font(26))
                ax += 540
                
            d.rounded_rectangle([150, 710, 1770, 870], radius=16, fill=LIGHT_AMBER)
            d.text((460, 765), sc.get("thank_you", "謝謝各位評審老師觀看·敬請批評指教"), fill=AMBER, font=font(38))

        draw_footer(d)
        out_p = os.path.join(OUT, f"scene_{sid:02d}.png")
        im.save(out_p)

    print("✓ Đã render toàn bộ slide độc lập với hình ảnh thật & Agoda screenshot!")

def render_location_tags():
    scenes = doc["scenes"]
    for s in scenes:
        if s.get("visual_type") != "video":
            continue
        sid = s["scene_id"]
        title = s.get("on_screen_title", "")
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        f_tag = font(32)
        b = d.textbbox((0, 0), title, font=f_tag)
        tw = b[2] - b[0]
        pad_x, pad_y = 26, 14
        box_w = tw + pad_x * 2
        box_h = 40 + pad_y * 2
        bx0, by0 = 80, 80
        d.rounded_rectangle([bx0, by0, bx0 + box_w, by0 + box_h], radius=14, fill=(15, 23, 42, 225), outline=(13, 148, 136, 255), width=2)
        d.text((bx0 + pad_x, by0 + pad_y), title, fill=(255, 255, 255, 255), font=f_tag)
        im.save(os.path.join(OUT, f"tag_{sid:02d}.png"))
    print("✓ Đã render nhãn địa điểm tag_XX.png cho các video clips")

def render_credits():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=DARK_TEAL)
    
    d.text((120, 95), "越青旅行社・感謝收看", fill=DARK_TEAL, font=font(32))
    d.text((120, 155), "專題致謝與官方資料來源聲明", fill=WHITE, font=font(56))
    d.line([(120, 240), (1800, 240)], fill=(51, 65, 85), width=2)
    
    # Left box: Course & Team
    d.rounded_rectangle([120, 280, 920, 880], radius=18, fill=(30, 41, 59))
    d.text((160, 320), "【專案策劃與匯報團隊】", fill=AMBER, font=font(30))
    d.text((160, 385), "主辦機構：越青旅行社 (Viet-Youth Travel)", fill=WHITE, font=font(26))
    d.text((160, 445), "專案組員：黎光達（組長）、阮氏英書、阮曰黃絨", fill=WHITE, font=font(26))
    d.text((160, 505), "遊程名稱：山海海岸・青春北台灣 兩天一夜", fill=WHITE, font=font(26))
    d.text((160, 565), "目標客群：18–25 歲首次訪台越南年輕人", fill=WHITE, font=font(26))
    d.text((160, 625), "產品定價：NT$ 3,600 / 人（16人成團）", fill=DARK_TEAL, font=font(28))
    d.text((160, 685), "直接成本：NT$ 2,523｜利潤：NT$ 597 (16.6%)", fill=MUTED, font=font(24))
    d.text((160, 745), "飯店優惠：16人以上成團可享專案約 9 折優惠", fill=AMBER, font=font(24))
    d.text((160, 805), "製作環境：macOS Apple Silicon (M4) 100% 自動化", fill=MUTED, font=font(22))

    # Right box: Official Data Sources
    d.rounded_rectangle([980, 280, 1800, 880], radius=18, fill=(30, 41, 59))
    d.text((1020, 320), "【官方資料查核與授權來源】", fill=DARK_TEAL, font=font(30))
    d.text((1020, 385), "1. 鐵道票價：國營台灣鐵路股份有限公司（台鐵新制票價）", fill=WHITE, font=font(24))
    d.text((1020, 445), "2. 支線票價：台鐵平溪線一日週遊券官方公告 (NT$80)", fill=WHITE, font=font(24))
    d.text((1020, 505), "3. 公車客運：基隆汽車客運 788、790 路線票價核准表", fill=WHITE, font=font(24))
    d.text((1020, 565), "4. 台灣好行：交通部觀光署北觀處 716 皇冠北海岸線", fill=WHITE, font=font(24))
    d.text((1020, 625), "5. 門票收費：新北市野柳地質公園官方售票標準 (NT$120)", fill=WHITE, font=font(24))
    d.text((1020, 685), "6. 飯店房價：Agoda / Booking 2026/11 基隆合法商旅牌價", fill=WHITE, font=font(24))
    d.text((1020, 745), "7. 影像素材：YouTube Creative Commons 4K 實景授權", fill=MUTED, font=font(22))

    d.line([(120, 925), (1800, 925)], fill=(51, 65, 85), width=2)
    d.text((120, 950), "© 2026 越青旅行社版權所有 All Rights Reserved. 專題期末成果發表", fill=MUTED, font=font(22))
    im.save(os.path.join(OUT, "credits.png"))
    print("✓ Đã render slide credits.png hoàn chỉnh!")

if __name__ == "__main__":
    render_cards()
    render_slides()
    render_location_tags()
    render_credits()
