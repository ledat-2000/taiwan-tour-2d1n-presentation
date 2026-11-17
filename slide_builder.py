# -*- coding: utf-8 -*-
"""
Independent Slide Builder (1920x1080 Full HD)
Features:
- Modern Emerald & Deep Slate luxury travel visual identity
- 100% Traditional Chinese typography using macOS native STHeiti Medium
- Structured tables for Day 1 and Day 2 schedules with badges
- Complete Cost & Profit Breakdown Matrix
- Transparent Data Source Footer on every slide
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "slides")
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

SRC_TEXT = "資料來源：台鐵官網、台灣好行官網、野柳地質公園官網、Agoda 2026 實際查詢價格"

def draw_header(d, category, title):
    # Top color stripe
    d.rectangle([0, 0, W, 14], fill=DARK_TEAL)
    # Brand tag
    d.text((100, 50), "越青旅行社｜山海海岸·青春北台灣 兩天一夜", fill=MUTED, font=font(28))
    # Category badge
    if category:
        d.rounded_rectangle([100, 95, 240, 140], radius=8, fill=LIGHT_TEAL)
        d.text((118, 105), category, fill=DARK_TEAL, font=font(26))
        d.text((260, 90), title, fill=NAVY, font=font(52))
    else:
        d.text((100, 90), title, fill=NAVY, font=font(52))

def draw_footer(d):
    d.line([(100, 990), (1820, 990)], fill=BORDER, width=2)
    d.text((100, 1008), SRC_TEXT, fill=MUTED, font=font(22))

def render_cards():
    cards = [
        ("01", "第一部分", "品牌與行程總覽", "黎光達｜組長"),
        ("02", "第二部分", "目標客群與核心訴求", "黎光達｜組長"),
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
            # Main banner
            d.rounded_rectangle([100, 180, 1820, 940], radius=24, fill=WHITE, outline=BORDER, width=2)
            d.text((160, 260), "山海海岸·青春北台灣 兩天一夜", fill=NAVY, font=font(70))
            d.text((160, 370), "專為第一次來台灣的越南年輕人（18–25歲）量身打造", fill=DARK_TEAL, font=font(40))
            
            # 3 badges
            bx = 160
            for b_text in ["好玩 (Fun)", "好拍 (Photogenic)", "價格合理 (Affordable)"]:
                d.rounded_rectangle([bx, 480, bx + 360, 580], radius=16, fill=LIGHT_TEAL, outline=DARK_TEAL, width=2)
                d.text((bx + 35, 510), b_text, fill=DARK_TEAL, font=font(34))
                bx += 400
                
            d.rounded_rectangle([160, 640, 1760, 880], radius=16, fill=(241, 245, 249))
            d.text((200, 680), "【行程精華亮點】", fill=NAVY, font=font(34))
            d.text((200, 740), "• 台北出發 → 平溪支線鐵道 → 十分天燈 → 九份阿妹茶樓燈籠夜景 → 基隆廟口夜市", fill=MUTED, font=font(30))
            d.text((200, 800), "• 野柳地質公園女王頭 → 皇冠北海岸無敵海景 → 淡水老街與漁人碼頭夕照 → 西門町潮流圈", fill=MUTED, font=font(30))

        elif layout == "team_cards":
            draw_header(d, "團隊介紹", sc.get("title", ""))
            cards = sc.get("cards", [])
            cx = 100
            for c in cards:
                d.rounded_rectangle([cx, 220, cx + 520, 920], radius=20, fill=WHITE, outline=BORDER, width=2)
                d.rounded_rectangle([cx + 40, 260, cx + 220, 310], radius=8, fill=LIGHT_AMBER)
                d.text((cx + 55, 272), c["role"], fill=AMBER, font=font(24))
                d.text((cx + 40, 340), c["name"], fill=NAVY, font=font(48))
                d.line([(cx + 40, 420), (cx + 480, 420)], fill=BORDER, width=2)
                
                # Description
                lines = c["desc"].split("·")
                ly = 460
                d.text((cx + 40, ly), "負責領域：", fill=DARK_TEAL, font=font(30))
                ly += 50
                for line in lines:
                    d.text((cx + 60, ly), f"• {line}", fill=MUTED, font=font(28))
                    ly += 50
                cx += 550

        elif layout in ("persona", "pillars"):
            draw_header(d, "市場分析", sc.get("title", ""))
            items = sc.get("items") or sc.get("pillars") or []
            iy = 220
            for it in items:
                d.rounded_rectangle([100, iy, 1820, iy + 210], radius=18, fill=WHITE, outline=BORDER, width=2)
                tag = it.get("tag") or it.get("name")
                desc = it.get("val") or it.get("desc")
                d.rounded_rectangle([140, iy + 35, 420, iy + 105], radius=12, fill=LIGHT_TEAL)
                d.text((160, iy + 50), tag, fill=DARK_TEAL, font=font(32))
                d.text((460, iy + 52), desc, fill=NAVY, font=font(34))
                iy += 240

        elif layout == "route_map":
            draw_header(d, "路網動線", sc.get("title", ""))
            d.rounded_rectangle([100, 220, 1820, 540], radius=20, fill=WHITE, outline=BORDER, width=2)
            d.rounded_rectangle([140, 260, 280, 315], radius=8, fill=LIGHT_AMBER)
            d.text((165, 272), "DAY 1", fill=AMBER, font=font(28))
            d.text((310, 270), "經典山城與港灣夜市", fill=NAVY, font=font(36))
            d.text((140, 370), sc.get("day1", ""), fill=DARK_TEAL, font=font(42))
            
            d.rounded_rectangle([100, 580, 1820, 900], radius=20, fill=WHITE, outline=BORDER, width=2)
            d.rounded_rectangle([140, 620, 280, 675], radius=8, fill=LIGHT_TEAL)
            d.text((165, 632), "DAY 2", fill=DARK_TEAL, font=font(28))
            d.text((310, 630), "地質奇觀·海景公路·歷史夕陽·潮流圈", fill=NAVY, font=font(36))
            d.text((140, 730), sc.get("day2", ""), fill=AMBER, font=font(40))

        elif layout == "day_table":
            draw_header(d, sc.get("day", "行程表"), sc.get("title", ""))
            rows = sc.get("rows", [])
            # Table header
            ty = 190
            d.rounded_rectangle([100, ty, 1820, ty + 60], radius=8, fill=(241, 245, 249))
            d.text((130, ty + 16), "時間", fill=MUTED, font=font(24))
            d.text((250, ty + 16), "目的地 / 站點", fill=MUTED, font=font(24))
            d.text((640, ty + 16), "交通工具 / 路線", fill=MUTED, font=font(24))
            d.text((1060, ty + 16), "費用 (NT$)", fill=MUTED, font=font(24))
            d.text((1260, ty + 16), "活動內容與亮點", fill=MUTED, font=font(24))
            ty += 70

            for r in rows:
                d.rounded_rectangle([100, ty, 1820, ty + 60], radius=8, fill=WHITE, outline=BORDER, width=1)
                d.text((130, ty + 16), r["time"], fill=NAVY, font=font(24))
                d.text((250, ty + 16), r["dest"], fill=NAVY, font=font(24))
                
                # Transit badge
                d.rounded_rectangle([640, ty + 10, 980, ty + 50], radius=6, fill=LIGHT_TEAL)
                d.text((655, ty + 16), r["trans"], fill=DARK_TEAL, font=font(22))
                
                # Cost badge
                d.text((1060, ty + 16), r["cost"], fill=AMBER, font=font(26))
                d.text((1260, ty + 16), r["activity"], fill=MUTED, font=font(23))
                ty += 68

        elif layout in ("cost_table", "total_cost"):
            draw_header(d, "財務會計", sc.get("title", ""))
            items = sc.get("items") or sc.get("rows") or []
            ty = 220
            for it in items:
                d.rounded_rectangle([100, ty, 1820, ty + 120], radius=16, fill=WHITE, outline=BORDER, width=2)
                cat = it.get("cat") or it.get("item")
                det = it.get("detail", "")
                amt = it.get("amount") or it.get("val")
                
                d.text((140, ty + 25), cat, fill=NAVY, font=font(34))
                if det:
                    d.text((140, ty + 72), det, fill=MUTED, font=font(24))
                d.rounded_rectangle([1520, ty + 30, 1780, ty + 90], radius=10, fill=LIGHT_AMBER)
                d.text((1545, ty + 42), amt, fill=AMBER, font=font(32))
                ty += 140

            total_label = sc.get("subtotal") or sc.get("grand_total")
            if total_label:
                d.rounded_rectangle([100, ty + 10, 1820, ty + 100], radius=16, fill=DARK_TEAL)
                d.text((140, ty + 35), total_label, fill=WHITE, font=font(38))

        elif layout == "pricing_matrix":
            draw_header(d, "收益模型", sc.get("title", ""))
            metrics = sc.get("metrics", [])
            mx = 100
            for m in metrics:
                d.rounded_rectangle([mx, 220, mx + 390, 520], radius=20, fill=WHITE, outline=BORDER, width=2)
                d.rounded_rectangle([mx + 30, 250, mx + 180, 295], radius=6, fill=LIGHT_TEAL)
                d.text((mx + 45, 260), m["badge"], fill=DARK_TEAL, font=font(22))
                d.text((mx + 30, 330), m["label"], fill=MUTED, font=font(28))
                d.text((mx + 30, 410), m["num"], fill=NAVY, font=font(52))
                mx += 430

            # Formula card
            d.rounded_rectangle([100, 570, 1820, 720], radius=18, fill=LIGHT_AMBER, outline=AMBER, width=2)
            d.text((160, 620), sc.get("formula", ""), fill=AMBER, font=font(40))
            
            d.rounded_rectangle([100, 760, 1820, 890], radius=18, fill=WHITE, outline=BORDER, width=2)
            d.text((160, 805), sc.get("group_profit", ""), fill=DARK_TEAL, font=font(40))

        elif layout == "comparison":
            draw_header(d, "價值優勢", sc.get("title", ""))
            comp = sc.get("compare", [])
            # Header
            d.rounded_rectangle([100, 200, 1820, 260], radius=10, fill=(241, 245, 249))
            d.text((140, 218), "比較維度", fill=MUTED, font=font(26))
            d.text((450, 218), "旅客自行規劃自由行 (痛點與隱形成本)", fill=AMBER, font=font(26))
            d.text((1140, 218), "越青旅行社 青春北台灣遊程 (專屬價值)", fill=DARK_TEAL, font=font(26))
            
            cy = 280
            for c in comp:
                d.rounded_rectangle([100, cy, 1820, cy + 130], radius=14, fill=WHITE, outline=BORDER, width=1)
                d.rounded_rectangle([130, cy + 35, 340, cy + 95], radius=8, fill=LIGHT_TEAL)
                d.text((150, cy + 48), c["dim"], fill=DARK_TEAL, font=font(28))
                d.text((450, cy + 50), c["self"], fill=MUTED, font=font(28))
                d.text((1140, cy + 50), c["us"], fill=NAVY, font=font(28))
                cy += 150

        elif layout == "closing":
            draw_header(d, "結語", sc.get("title", ""))
            d.rounded_rectangle([100, 200, 1820, 920], radius=24, fill=WHITE, outline=BORDER, width=2)
            d.text((160, 270), "你會想參加這個行程嗎？", fill=NAVY, font=font(64))
            d.text((160, 370), "越青旅行社｜陪伴每一位青年探索最精彩的台灣", fill=DARK_TEAL, font=font(36))
            d.line([(160, 460), (1760, 460)], fill=BORDER, width=2)
            
            # Author cards
            ax = 160
            for a in sc.get("authors", []):
                d.rounded_rectangle([ax, 500, ax + 460, 680], radius=16, fill=(248, 250, 252), outline=BORDER, width=1)
                d.text((ax + 40, 540), a["name"], fill=NAVY, font=font(44))
                d.text((ax + 40, 610), a["title"], fill=MUTED, font=font(28))
                ax += 520
                
            d.rounded_rectangle([160, 740, 1760, 860], radius=16, fill=LIGHT_AMBER)
            d.text((480, 780), sc.get("thank_you", "謝謝各位評審老師觀看·敬請批評指教"), fill=AMBER, font=font(40))

        draw_footer(d)
        out_p = os.path.join(OUT, f"scene_{sid:02d}.png")
        im.save(out_p)

    print("✓ Đã render toàn bộ slide độc lập vào independent_tour/slides/")

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
        # Pill
        d.rounded_rectangle([bx0, by0, bx0 + box_w, by0 + box_h], radius=14, fill=(15, 23, 42, 225), outline=(13, 148, 136, 255), width=2)
        d.text((bx0 + pad_x, by0 + pad_y), title, fill=(255, 255, 255, 255), font=f_tag)
        im.save(os.path.join(OUT, f"tag_{sid:02d}.png"))
    print("✓ Đã render nhãn địa điểm tag_XX.png cho các video clips")

if __name__ == "__main__":
    render_cards()
    render_slides()
    render_location_tags()

def render_credits():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=DARK_TEAL)
    
    d.text((120, 100), "越青旅行社・感謝收看", fill=DARK_TEAL, font=font(34))
    d.text((120, 160), "專題致謝與資料來源聲明", fill=WHITE, font=font(60))
    d.line([(120, 250), (1800, 250)], fill=(51, 65, 85), width=2)
    
    # Left box: Course & Team
    d.rounded_rectangle([120, 300, 920, 880], radius=18, fill=(30, 41, 59))
    d.text((160, 340), "【專案策劃與匯報團隊】", fill=AMBER, font=font(32))
    d.text((160, 410), "主辦機構：越青旅行社 (Viet-Youth Travel)", fill=WHITE, font=font(28))
    d.text((160, 470), "專案組員：黎光達（組長）、阮氏英書、阮曰黃絨", fill=WHITE, font=font(28))
    d.text((160, 530), "遊程名稱：山海海岸・青春北台灣 兩天一夜", fill=WHITE, font=font(28))
    d.text((160, 590), "目標客群：18–25 歲首次訪台越南年輕人", fill=WHITE, font=font(28))
    d.text((160, 650), "產品定價：NT$ 3,600 / 人（16人成團）", fill=DARK_TEAL, font=font(30))
    d.text((160, 710), "總成本：NT$ 3,003｜預估單客利潤：NT$ 597 (16.6%)", fill=MUTED, font=font(26))
    d.text((160, 780), "製作環境：macOS Apple Silicon (M4) 100% 自動化", fill=MUTED, font=font(24))

    # Right box: Official Data Sources
    d.rounded_rectangle([980, 300, 1800, 880], radius=18, fill=(30, 41, 59))
    d.text((1020, 340), "【官方資料查核與授權來源】", fill=DARK_TEAL, font=font(32))
    d.text((1020, 410), "1. 鐵道票價：國營台灣鐵路股份有限公司（台鐵新制票價）", fill=WHITE, font=font(26))
    d.text((1020, 470), "2. 支線票價：台鐵平溪線一日週遊券官方公告 (NT$80)", fill=WHITE, font=font(26))
    d.text((1020, 530), "3. 公車客運：基隆汽車客運 788、790 路線票價核准表", fill=WHITE, font=font(26))
    d.text((1020, 590), "4. 台灣好行：交通部觀光署北觀處 716 皇冠北海岸線", fill=WHITE, font=font(26))
    d.text((1020, 650), "5. 門票收費：新北市野柳地質公園官方售票標準 (NT$120)", fill=WHITE, font=font(26))
    d.text((1020, 710), "6. 飯店房價：Agoda / Hotels.com 2026/11 華國飯店牌價", fill=WHITE, font=font(26))
    d.text((1020, 770), "7. 影像素材：YouTube Creative Commons 4K 實景授權", fill=MUTED, font=font(24))

    d.line([(120, 930), (1800, 930)], fill=(51, 65, 85), width=2)
    d.text((120, 955), "© 2026 越青旅行社版權所有 All Rights Reserved. 專題期末成果發表", fill=MUTED, font=font(24))
    im.save(os.path.join(OUT, "credits.png"))
    print("✓ Đã render slide credits.png hoàn chỉnh!")

if __name__ == "__main__":
    render_credits()
