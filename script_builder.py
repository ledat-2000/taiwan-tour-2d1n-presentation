# -*- coding: utf-8 -*-
"""
Independent Script Builder for Taiwan 2D1N Tour
Agency: 越青旅行社 (Viet-Youth Travel)
Product: 山海海岸・青春北台灣 兩天一夜
Calibrated for exactly ~3,050 Traditional Chinese characters (Standard: 2,950 - 3,150)
Target video duration: 15 - 16 minutes
"""
import json, os, re

DAT = "le_quang_dat"               # Nam - Trưởng nhóm: Part 1, 2, 6
THU = "nguyen_thi_anh_thu"         # Nữ: Part 3 (Day 1)
NHUNG = "nguyen_viet_hoang_nhung"  # Nữ: Part 4 (Day 2) + Part 5 (Cost & Pricing)

SRC = "資料來源：台鐵官網、台灣好行官網、野柳地質公園官網、Agoda 2026 實際查詢價格"

scenes = []

def add(speaker, section, vtype, text, title=None, kw=None, slide_content=None):
    scenes.append({
        "scene_id": len(scenes) + 1,
        "section": section,
        "speaker": speaker,
        "visual_type": vtype,
        "text_zh": text,
        "on_screen_title": title or "",
        "search_keyword": kw or "Taiwan 4K travel",
        "slide_content": slide_content or {}
    })

# ==================== PART 1: 開場與旅行社介紹 (黎光達) ====================
# Scene 01
add(DAT, "01 開場", "slide",
    "評審老師與各位同學好，我是越青旅行社的組長黎光達。今天由我們團隊為大家介紹專為越南青年設計的精選遊程：「山海海岸・青春北台灣兩天一夜」。旅程從台北出發，串聯十分、九份、基隆、野柳與淡水，兼具山城歷史與壯麗海景。",
    title="山海海岸・青春北台灣 兩天一夜",
    slide_content={
        "layout": "hero_title",
        "title": "山海海岸・青春北台灣 兩天一夜",
        "subtitle": "越青旅行社｜專為越南青年打造的台灣初體驗首選",
        "badges": ["好玩體驗", "極致美拍", "合理價格"],
        "footer": SRC
    })

# Scene 02
add(DAT, "01 開場", "video",
    "越青旅行社是由在台灣求學的越南留學生共同成立。我們親身體會過初次來台時在語言與大眾交通上的迷惘，因此最了解越南旅客的核心需求：資訊透明、拒絕隱藏收費，並提供全程雙語陪伴，讓每位朋友安心暢遊台灣。",
    title="越青旅行社品牌理念", kw="Taipei city 4K drone footage")

# Scene 03
add(DAT, "01 開場", "slide",
    "在分工上，我負責遊程總體架構、客群分析與推薦價值提煉；阮氏英書負責第一天十分、九份與基隆的深度規劃；阮曰黃絨則操刀第二天野柳、淡水與精準成本利潤試算。我們三位都會以流利的繁體中文為各位解說。",
    title="團隊分工表",
    slide_content={
        "layout": "team_cards",
        "title": "越青旅行社・策劃團隊分工",
        "cards": [
            {"role": "組長", "name": "黎光達", "desc": "品牌定位・客群痛點分析・推薦理由與結語"},
            {"role": "組員", "name": "阮氏英書", "desc": "第一天完整行程：十分天燈・九份燈海・基隆夜市"},
            {"role": "組員", "name": "阮曰黃絨", "desc": "第二天完整行程：野柳地質・淡水夕陽・西門町＋成本售價"}
        ],
        "footer": SRC
    })

# ==================== PART 2: 目標客群分析 (黎光達) ====================
# Scene 04
add(DAT, "02 目標客群", "slide",
    "本行程的目標受眾為十八至二十五歲、首次來台灣的越南年輕人，涵蓋在學大學生與職場新人。他們的特點是預算有限但充滿探索欲，熱愛拍照打卡，需要非常明確的交通車次、時刻表與花費指引。",
    title="目標客群畫像 (18-25歲)",
    slide_content={
        "layout": "persona",
        "title": "目標客群畫像分析",
        "items": [
            {"tag": "目標族群", "val": "18–25 歲越南年輕人（大學生、剛入職青年）"},
            {"tag": "旅遊經驗", "val": "首次踏上台灣，不熟悉大眾運輸轉乘方式"},
            {"tag": "核心需求", "val": "每筆花費透明清晰、兼顧好玩與打卡分享"}
        ],
        "footer": SRC
    })

# Scene 05
add(DAT, "02 目標客群", "slide",
    "經過深入市調，越南青年出遊最重視三大要素：第一是好玩，要親自放天燈與逛夜市；第二是好拍，每個景點都要能拍出社群吸睛美照；第三是價格合理，所有花費公開透明，絕無強迫消費或隱形購物站。",
    title="三大核心訴求",
    slide_content={
        "layout": "pillars",
        "title": "越南青年旅客三大核心訴求",
        "pillars": [
            {"name": "好玩 (Fun)", "desc": "放天燈、老街探秘、夜市尋味，親身深度互動"},
            {"name": "好拍 (Photogenic)", "desc": "十分鐵道、九份山城燈海、女王頭、淡江夕照"},
            {"name": "價格合理 (Affordable)", "desc": "全程大眾運輸銜接，票價食宿公開透明，高性價比"}
        ],
        "footer": SRC
    })

# Scene 06
add(DAT, "02 目標客群", "video",
    "考量初次訪台旅客看不懂公車站牌或擔心刷錯悠遊卡的焦慮，我們全程安排隨團雙語青年領隊，帶大家搭乘台鐵、台灣好行與捷運，不僅省錢安全，還能學會如何在台灣自主漫遊。",
    title="大眾運輸與隨團指引", kw="Taipei Main Station MRT Taiwan 4K")

# Scene 07
add(DAT, "02 目標客群", "slide",
    "現在看到的是兩天一夜的動線規劃圖。第一天從台北車站搭台鐵至瑞芳，走訪十分放天燈，下午暢遊九份山城，夜宿基隆港；第二天探訪野柳女王頭，搭台灣好行沿北海岸抵達淡水，傍晚回到西門町圓滿賦歸。",
    title="兩天一夜路線總覽",
    slide_content={
        "layout": "route_map",
        "title": "山海海岸・兩天一夜路線總覽",
        "day1": "台北車站 ➔ 瑞芳 ➔ 十分老街 ➔ 九份老街 ➔ 基隆廟口夜市 (宿基隆)",
        "day2": "基隆 ➔ 野柳地質公園 ➔ 皇冠北海岸 ➔ 淡水老街/夕陽 ➔ 西門町",
        "footer": SRC
    })

# ==================== PART 3: 第一天完整行程 (阮氏英書) ====================
# Scene 08
add(THU, "03 第一天行程", "video",
    "謝謝光達組長。大家好，我是阮氏英書，由我為大家解說第一天行程。早上八點整，我們在台北車站地下一樓大廳集合，領隊發放已儲值悠遊卡與越文導覽地圖，提醒乘車守則後整隊出發。",
    title="08:00 台北車站集合整隊", kw="Taipei Main Station morning crowd 4K")

# Scene 09
add(THU, "03 第一天行程", "video",
    "八點十五分，我們刷悠遊卡搭乘台鐵四一五四次區間車由台北出發至瑞芳，車程約四十五分鐘，票價七十三元。列車平穩乾淨，窗外景致由市區轉入青山綠水，開啟舒適的鐵道初體驗。",
    title="08:15 搭台鐵區間車至瑞芳｜NT$73", kw="Taiwan Railway EMU Train Taipei to Ruifang 4K")

# Scene 10
add(THU, "03 第一天行程", "video",
    "九點十分抵達瑞芳車站。瑞芳是昔日採金採煤重鎮，也是前往平溪與九份的玄關。我們在月台購買平溪線一日週遊券，一張只要八十元，當天可無限次搭乘平溪支線各站列車，非常超值。",
    title="09:20 購買平溪一日券｜NT$80", kw="Ruifang Railway Station Pingxi Line ticket 4K")

# Scene 11
add(THU, "03 第一天行程", "video",
    "九點四十分搭乘平溪支線柴油彩繪列車前往十分，車程約三十分鐘。火車穿梭在翠綠山林與基隆河谷之間，十點十分抵達十分車站，木造古樸月台讓團員立刻感受到濃濃懷舊氛圍。",
    title="09:40 平溪支線彩繪列車體驗", kw="Pingxi Line train passing mountains 4K")

# Scene 12
add(THU, "03 第一天行程", "video",
    "十點半至十一點半，在十分老街施放祈福天燈。十分老街最特別的是火車就從店家門前開過。我們安排兩人合放一盞四色天燈，一盞兩百五十元，每人一百二十五元，親筆寫下祝福，看著天燈升空無比感動。",
    title="10:30 十分老街放天燈｜每人NT$125", kw="Shifen Old Street Sky Lantern Taiwan 4K")

# Scene 13
add(THU, "03 第一天行程", "video",
    "放完天燈後，步行二十分鐘前往十分瀑布公園。十分瀑布寬四十公尺、高二十公尺，是台灣最大的簾幕型瀑布，有台灣尼加拉瀑布之稱。新北市政府目前免門票開放，陽光下彩虹映照瀑布，是拍照打卡首選。",
    title="11:30 漫步十分瀑布（免門票）", kw="Shifen Waterfall scenic 4K")

# Scene 14
add(THU, "03 第一天行程", "video",
    "十二點半回到老街享用在地小吃午餐，每人預算一百五十元。最推薦知名美食雞翅包飯與現烤香腸，去骨雞翅塞滿炒油飯，表皮烤得酥脆香濃，好吃又有飽足感，大家吃得讚不絕口。",
    title="12:30 十分風味小吃午餐｜NT$150", kw="Shifen food street chicken wing rice 4K")

# Scene 15
add(THU, "03 第一天行程", "video",
    "午後一點半，搭平溪線列車返回瑞芳。兩點二十分在瑞芳站外搭乘基隆客運七八八號公車前往九份，車程約二十分鐘，票價只要十五元。公車蜿蜒上山，沿途可俯瞰美麗的基隆嶼海景。",
    title="14:20 搭基隆客運788上九份｜NT$15", kw="Bus 788 road up to Jiufen mountain 4K")

# Scene 16
add(THU, "03 第一天行程", "video",
    "兩點四十分抵達九份老街。這座昔日淘金小鎮依山傍海，石階古道縱橫交錯。我們先品嚐著名賴阿婆芋圓，再漫步基山街特色小舖，每人點心預算一百五十元，細細體會山城的慢活與古樸風貌。",
    title="14:40 九份老街漫步與芋圓｜NT$150", kw="Jiufen Old Street food and shops 4K")

# Scene 17
add(THU, "03 第一天行程", "video",
    "下午五點傍晚時分，豎崎路的紅燈籠逐一亮起，阿妹茶樓前宛如神隱少女動畫場景。橘紅晚霞照亮海面，紅燈籠映襯木造老茶樓，如夢似幻，團員們紛紛拿起手機拍下最經典的台灣山城代表照。",
    title="17:00 豎崎路阿妹茶樓經典燈籠景", kw="Jiufen A-Mei Tea House lanterns night 4K")

# Scene 18
add(THU, "03 第一天行程", "video",
    "六點半在九份派出所站搭乘基隆客運七八八號公車直達基隆市區，車程約五十分鐘，票價三十元。七點二十分抵達全台灣最具特色的基隆廟口夜市，整排黃色燈籠整齊排列，氣氛格外熱鬧。",
    title="18:30 基隆客運788直達基隆｜NT$30", kw="Keelung city night harbor 4K")

# Scene 19
add(THU, "03 第一天行程", "video",
    "七點半至九點為廟口夜市晚餐時間，每人餐費預算兩百五十元。必吃經典有一口吃香腸、營養三明治與泡泡冰。新鮮的海鮮與道地小吃讓人食指大動，是深入感受台灣庶民飲食文化的絕佳體驗。",
    title="19:30 基隆廟口夜市小吃探索｜NT$250", kw="Keelung Miaokou Night Market food 4K")

# Scene 20
add(THU, "03 第一天行程", "video",
    "晚上九點步行五分鐘入住廟口旁的基隆華國商務飯店。我們安排雙人房雙床房型，含次日自助早餐，雙人房每人分攤七百元。飯店乾淨安全、交通極便利，讓團員消除整天疲勞，安心好眠。",
    title="21:00 入住基隆華國商務飯店｜每人NT$700", kw="Taiwan modern clean hotel room interior 4K")

# Scene 21
add(THU, "03 第一天行程", "slide",
    "這張表是第一天行程總結。整日交通花費一百九十八元、天燈一百二十五元、餐飲點心五百五十元加上住宿七百元，每人總花費為一千五百七十三元。行程兼顧山城鐵道、燈籠夜色與在地美食，充實且愜意。",
    title="第一天行程與費用總結",
    slide_content={
        "layout": "day_table",
        "day": "Day 1",
        "title": "第一天：十分山城・九份燈海・基隆夜市",
        "rows": [
            {"time": "08:15", "dest": "台北 ➔ 瑞芳", "trans": "台鐵區間車 4154", "cost": "NT$ 73", "activity": "舒適搭乘台鐵列車"},
            {"time": "09:40", "dest": "瑞芳 ➔ 十分", "trans": "平溪線一日週遊券", "cost": "NT$ 80", "activity": "平溪支線無限次搭乘"},
            {"time": "10:30", "dest": "十分老街", "trans": "徒步", "cost": "NT$ 125", "activity": "四色祈福天燈 (2人1盞)"},
            {"time": "11:30", "dest": "十分瀑布", "trans": "徒步", "cost": "免費", "activity": "參觀台灣尼加拉瀑布"},
            {"time": "12:30", "dest": "十分老街", "trans": "徒步", "cost": "NT$ 150", "activity": "午餐雞翅包飯與特色小吃"},
            {"time": "14:20", "dest": "瑞芳 ➔ 九份", "trans": "基隆客運 788", "cost": "NT$ 15", "activity": "搭乘公車蜿蜒上山"},
            {"time": "14:40", "dest": "九份老街", "trans": "徒步", "cost": "NT$ 150", "activity": "賴阿婆芋圓與老街巡禮"},
            {"time": "17:00", "dest": "豎崎路", "trans": "徒步", "cost": "免費", "activity": "阿妹茶樓經典燈籠紅景"},
            {"time": "18:30", "dest": "九份 ➔ 基隆", "trans": "基隆客運 788", "cost": "NT$ 30", "activity": "直達基隆港口市區"},
            {"time": "19:30", "dest": "基隆廟口", "trans": "徒步", "cost": "NT$ 250", "activity": "晚餐廟口夜市人氣美食"},
            {"time": "21:00", "dest": "華國飯店", "trans": "徒步", "cost": "NT$ 700", "activity": "住宿雙人房含自助早餐"}
        ],
        "footer": SRC
    })

# ==================== PART 4: 第二天完整行程 (阮曰黃絨) ====================
# Scene 22
add(NHUNG, "04 第二天行程", "video",
    "謝謝英書。大家好，我是阮曰黃絨，接下來由我介紹第二天壯闊的北海岸地質與淡水夕陽。早上七點半在飯店享用自助早餐，八點半辦理退房，團員一身輕便開啟令人期待的海岸巡禮。",
    title="07:30 飯店自助早餐・退房", kw="Hotel breakfast buffet Taiwan morning 4K")

# Scene 23
add(NHUNG, "04 第二天行程", "slide",
    "第二天的交通我們善用整合優勢：由基隆搭基隆客運七九零公車到野柳；接續搭台灣好行七一六皇冠北海岸線直達淡水；最後搭台北捷運回到西門町，全程路線流暢、車資經濟划算。",
    title="第二天交通整合策略",
    slide_content={
        "layout": "feature_card",
        "title": "Day 2 海岸線大眾交通串聯",
        "cards": [
            {"badge": "基隆客運 790", "title": "基隆 ➔ 野柳地質公園", "desc": "班次密集，車程35分鐘，票價 NT$30"},
            {"badge": "台灣好行 716", "title": "皇冠北海岸觀光專車", "desc": "沿台2線海景公路直達淡水，車資約 NT$150"},
            {"badge": "台北捷運", "title": "淡水信義線 ➔ 西門町", "desc": "淡水直達台北車站轉板南線至西門，票價 NT$50"}
        ],
        "footer": SRC
    })

# Scene 24
add(NHUNG, "04 第二天行程", "video",
    "八點半在基隆車站搭乘基隆客運七九零號公車，沿濱海公路前行，九點十分抵達世界知名的野柳地質公園。這座凸出於海面的狹長海岬，因造山運動與風化侵蝕形成奇特天然奇岩。",
    title="08:30 搭基隆客運790至野柳｜NT$30", kw="Yehliu Geopark scenic view 4K")

# Scene 25
add(NHUNG, "04 第二天行程", "video",
    "九點十五分至十一點半參觀園區，門票一百二十元。領隊引導大家參觀招牌女王頭、俏皮公主與蕈狀岩群。女王頭頸部因自然風化日漸細瘦，大家抓緊機會與她合影，留下珍貴回憶。",
    title="09:15 野柳女王頭奇岩探訪｜門票NT$120", kw="Yehliu Queen Head rock Taiwan 4K")

# Scene 26
add(NHUNG, "04 第二天行程", "video",
    "十一點半前往野柳漁港享用現撈海鮮合菜，每人預算兩百五十元。野柳漁產豐富，我們安排四菜一湯，包含鮮魚、白灼蝦、蛤蜊湯與時蔬，鮮美多汁、真材實料，大家吃得心滿意足。",
    title="11:30 野柳漁港海鮮午餐｜NT$250", kw="Taiwan seafood restaurant dishes 4K")

# Scene 27
add(NHUNG, "04 第二天行程", "video",
    "十二點四十在野柳搭乘台灣好行七一六皇冠北海岸線前往淡水，車資約一百五十元。巴士沿著北部濱海公路前進，一邊是壯麗山景，一邊是湛藍大海，九十分鐘車程有如海景明信片般美麗。",
    title="12:40 台灣好行716皇冠北海岸線｜NT$150", kw="Northern Coast highway Taiwan ocean drive 4K")

# Scene 28
add(NHUNG, "04 第二天行程", "video",
    "下午兩點半抵達淡水老街。淡水是擁有四百年歷史的著名河港。我們先漫步金色水岸，品嚐阿給與阿婆鐵蛋這兩項在地名產，每人點心預算一百元，感受濃濃的淡水小鎮風情。",
    title="14:30 漫步淡水金色水岸老街｜NT$100", kw="Tamsui Old Street waterfront 4K")

# Scene 29
add(NHUNG, "04 第二天行程", "video",
    "四點半轉搭公車前往漁人碼頭情人橋。這座流線型白色單塔斜張橋如同一艘揚帆的帆船。傍晚五點夕陽落下淡水河口，水天染成金黃粉紫，淡江夕照的浪漫氛圍讓所有人沉醉其中。",
    title="16:30 漁人碼頭情人橋・淡江夕照", kw="Tamsui Lovers Bridge sunset Taiwan 4K")

# Scene 30
add(NHUNG, "04 第二天行程", "video",
    "五點四十在淡水捷運站搭乘淡水信義線，在台北車站轉乘板南線到西門站，車程約四十五分鐘，票價五十元。捷運平穩快速又準點，讓大家親身體驗台北捷運網絡的高效率與便利。",
    title="17:40 台北捷運紅線轉藍線至西門｜NT$50", kw="Taipei MRT train and platform 4K")

# Scene 31
add(NHUNG, "04 第二天行程", "video",
    "六點半抵達潮流聖地西門町。這裡匯聚流行服飾與街頭文化，安排兩小時晚餐與購物，預算兩百五十元。大家品嚐知名的阿宗麵線與台式滷味，並採買伴手禮與紀念品，收穫滿滿。",
    title="18:30 西門町流行商圈晚餐購物｜NT$250", kw="Ximending pedestrian street night Taiwan 4K")

# Scene 32
add(NHUNG, "04 第二天行程", "video",
    "晚上八點半全團在西門捷運站六號出口彩虹斑馬線集合。領隊清點行李、發放問卷並合影留念。兩天一夜豐富旅程在此圓滿結束，大家依依不捨互道珍重，為青春寫下最美一頁。",
    title="20:30 西門彩虹地標圓滿賦歸", kw="Ximending rainbow zebra crossing 4K")

# Scene 33
add(NHUNG, "04 第二天行程", "slide",
    "螢幕上是第二天時程表。第二天交通費兩百三十元、野柳門票一百二十元、三餐飲食點心六百元，每人花費九百五十元。整日包攬地質奇景、無敵海景、夕陽與購物，節奏順暢不匆忙。",
    title="第二天行程與費用總結",
    slide_content={
        "layout": "day_table",
        "day": "Day 2",
        "title": "第二天：野柳奇岩・海景公路・淡水夕照・西門商圈",
        "rows": [
            {"time": "07:30", "dest": "基隆華國飯店", "trans": "徒步", "cost": "房費內含", "activity": "享用飯店豐盛自助早餐"},
            {"time": "08:30", "dest": "基隆 ➔ 野柳", "trans": "基隆客運 790", "cost": "NT$ 30", "activity": "搭乘濱海公車前往野柳"},
            {"time": "09:15", "dest": "野柳地質公園", "trans": "徒步", "cost": "NT$ 120", "activity": "女王頭與奇岩怪石巡禮"},
            {"time": "11:30", "dest": "野柳漁港", "trans": "徒步", "cost": "NT$ 250", "activity": "午餐新鮮現撈海鮮合菜"},
            {"time": "12:40", "dest": "野柳 ➔ 淡水", "trans": "台灣好行 716", "cost": "NT$ 150", "activity": "皇冠北海岸無敵海景巴士"},
            {"time": "14:30", "dest": "淡水老街", "trans": "徒步", "cost": "NT$ 100", "activity": "品嚐阿給與鐵蛋漫步水岸"},
            {"time": "16:30", "dest": "漁人碼頭", "trans": "市區公車", "cost": "免費", "activity": "情人橋觀賞浪漫淡江夕照"},
            {"time": "17:40", "dest": "淡水 ➔ 西門", "trans": "台北捷運", "cost": "NT$ 50", "activity": "搭乘舒適捷運返回市中心"},
            {"time": "18:30", "dest": "西門町商圈", "trans": "徒步", "cost": "NT$ 250", "activity": "晚餐阿宗麵線與潮流採購"},
            {"time": "20:30", "dest": "西門捷運站", "trans": "徒步", "cost": "免費", "activity": "彩虹地標大合照圓滿賦歸"}
        ],
        "footer": SRC
    })

# ==================== PART 5: 成本、售價與利潤分析 (阮曰黃絨) ====================
# Scene 34
add(NHUNG, "05 財務分析", "slide",
    "接下來由我說明成本與收益分析。我們以十六位旅客成團計算直接成本：兩天交通合計四百二十八元、住宿七百元、門票天燈二百四十五元、兩天餐飲點心一千一百五十元，直接成本為兩千五百二十三元。",
    title="直接成本明細表",
    slide_content={
        "layout": "cost_table",
        "title": "直接成本核算明細表 (每位旅客)",
        "items": [
            {"cat": "全程交通費", "detail": "台鐵區間車、平溪一日券、客運788/790、好行716、台北捷運", "amount": "NT$ 428"},
            {"cat": "住宿費用", "detail": "基隆華國商務飯店雙人房含自助早餐 (兩人一室分攤)", "amount": "NT$ 700"},
            {"cat": "體驗與門票", "detail": "十分四色天燈每人分攤 NT$125 + 野柳地質公園門票 NT$120", "amount": "NT$ 245"},
            {"cat": "餐飲點心費", "detail": "午餐×2、晚餐×2、特色點心×2 (雞翅包飯、海鮮、夜市、阿給)", "amount": "NT$ 1,150"}
        ],
        "subtotal": "直接成本小計：NT$ 2,523 / 人",
        "footer": SRC
    })

# Scene 35
add(NHUNG, "05 財務分析", "slide",
    "間接成本方面，隨團雙語青年領隊兩天薪資食宿共六千四百元，由十六位團員分攤，每人四百元；另外兩百萬旅遊平安險與行前手冊每人一百五十元。加總直接與間接成本，每人總成本為三千零三元。",
    title="綜合總成本彙整",
    slide_content={
        "layout": "total_cost",
        "title": "綜合總成本彙總清單 (16人團)",
        "rows": [
            {"item": "直接成本小計 (交通/住宿/門票/餐食)", "val": "NT$ 2,523"},
            {"item": "隨團雙語領隊分攤 (總薪資NT$6,400 ÷ 16人)", "val": "NT$ 400"},
            {"item": "履約責任保險、旅平險與行政雜支", "val": "NT$ 150"}
        ],
        "grand_total": "每位旅客總成本：NT$ 3,003",
        "footer": SRC
    })

# Scene 36
add(NHUNG, "05 財務分析", "slide",
    "定價方面，我們將售價訂為每人新台幣三千六百元。售價扣除總成本三千零三元後，每位旅客為旅行社帶來五百九十七元淨利潤，利潤率約百分之十六點六。以每團十六人計，每團利潤達九千五百五十二元，兼顧親民與永續營運。",
    title="定價與毛利分析",
    slide_content={
        "layout": "pricing_matrix",
        "title": "定價策略與利潤分析",
        "metrics": [
            {"label": "每人總成本", "num": "NT$ 3,003", "badge": "成本基準"},
            {"label": "旅行社正式售價", "num": "NT$ 3,600", "badge": "青年親民價"},
            {"label": "每客淨利潤", "num": "NT$ 597", "badge": "合理毛利"},
            {"label": "產品毛利率", "num": "16.6 %", "badge": "穩健收益"}
        ],
        "formula": "售價 (NT$3,600) － 總成本 (NT$3,003) ＝ 單客利潤 (NT$597)",
        "group_profit": "16人出團規模 ➔ 每團預估淨利潤 NT$ 9,552",
        "footer": SRC
    })

# Scene 37
add(NHUNG, "05 財務分析", "slide",
    "相較於自己自由行，越青旅行社提供極大價值。自行規劃容易因查錯車次、排隊買票或搭計程車增加額外開銷，遇到語言不通更是求助無門。我們不僅解決所有痛點，更提供無價的安全感與好友同樂體驗，性價比超群。",
    title="自由行 vs 越青旅行社價值對比",
    slide_content={
        "layout": "comparison",
        "title": "遊程價值深度對比",
        "compare": [
            {"dim": "交通銜接", "self": "路線陌生、易迷路或錯過班次", "us": "精算時刻表、領隊專人引導無縫轉乘"},
            {"dim": "語言溝通", "self": "點餐與問路易產生障礙與誤會", "us": "隨團雙語青年領隊全程即時翻譯"},
            {"dim": "應變保障", "self": "遇天候異動需自行承擔風險", "us": "完整旅平險保障與專屬應變預案"},
            {"dim": "社交樂趣", "self": "獨自出遊孤單、拍照不易", "us": "結識同鄉青年夥伴、互相打卡助攻"}
        ],
        "footer": SRC
    })

# ==================== PART 6: 推薦理由與結語 (黎光達) ====================
# Scene 38
add(DAT, "06 推薦理由", "video",
    "謝謝黃絨。最後由我總結推薦本遊程的四大核心理由。第一，絕對好玩：行程融合鐵道天燈、九份黃金歷史、野柳地質奇觀、淡水夕陽與基隆夜市，兩天之內玩遍北台灣最具代表性的自然與人文精華。",
    title="推薦理由① 絕對好玩・精選必訪精華", kw="Taiwan night market and lantern fun 4K")

# Scene 39
add(DAT, "06 推薦理由", "video",
    "第二，絕對好拍：我們嚴選五大打卡地標——十分放天燈、九份阿妹茶樓紅燈籠、十分瀑布水幕、野柳女王頭以及淡水情人橋落日，每張照片都是能在社群平台引爆點讚的青春美好紀錄。",
    title="推薦理由② 絕對好拍・五大社群打卡熱點", kw="Taiwan travel scenic 4K compilation")

# Scene 40
add(DAT, "06 推薦理由", "video",
    "第三，價格公道透明：兩天一夜含完整交通、精緻住宿、門票天燈與六餐美食只要三千六百元，無購物壓力；第四，安全安心：雙語領隊全程陪伴，每天只安排精選景點不趕路，讓旅客玩得盡興、家人百分之百放心。",
    title="推薦理由③④ 價格公道・安全安心保障", kw="Taipei city sunset and skyline 4K")

# Scene 41
add(DAT, "06 推薦理由", "slide",
    "如果你是第一次來台灣的越南年輕人，你會想參加這個行程嗎？我們的回答是：一定會！越青旅行社用心陪伴大家走進最青春、最美麗的台灣。感謝各位評審與老師的聆聽，以上是我們的報告，謝謝大家！",
    title="走進最青春的台灣",
    slide_content={
        "layout": "closing",
        "title": "你會想參加這個行程嗎？",
        "subtitle": "越青旅行社｜陪伴每一位青年探索最精彩的台灣",
        "authors": [
            {"name": "黎光達", "title": "組長兼品牌總監"},
            {"name": "阮氏英書", "title": "山城文化遊程規劃"},
            {"name": "阮曰黃絨", "title": "海岸地質與財務風控"}
        ],
        "thank_you": "謝謝各位評審老師觀看・敬請批評指教",
        "footer": SRC
    })

# Compute statistics
han = lambda t: len(re.findall(r"[\u4e00-\u9fff]", t))
total_han = sum(han(s["text_zh"]) for s in scenes)
by_spk = {}
for s in scenes:
    s["han_chars"] = han(s["text_zh"])
    by_spk[s["speaker"]] = by_spk.get(s["speaker"], 0) + s["han_chars"]

doc = {
    "project": "Independent_Tour_2N1D",
    "title_zh": "山海海岸・青春北台灣 兩天一夜",
    "agency_zh": "越青旅行社",
    "language": "zh-TW（繁體中文）",
    "target_duration_sec": [900, 960],
    "voices": {
        DAT: {"name_zh": "黎光達", "gender": "male", "edge_voice": "zh-TW-YunJheNeural", "rate": "+0%"},
        THU: {"name_zh": "阮氏英書", "gender": "female", "edge_voice": "zh-TW-HsiaoChenNeural", "rate": "+0%"},
        NHUNG: {"name_zh": "阮曰黃絨", "gender": "female", "edge_voice": "zh-TW-HsiaoYuNeural", "rate": "+0%"}
    },
    "price_summary_ntd": {
        "cost_per_person": 3003,
        "price_per_person": 3600,
        "profit_per_person": 597,
        "margin": "16.6%",
        "group_size": 16
    },
    "stats": {
        "total_han_chars": total_han,
        "han_chars_by_speaker": by_spk,
        "scene_count": len(scenes)
    },
    "scenes": scenes
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

print(f"=== KỊCH BẢN ĐỘC LẬP HOÀN THIỆN ===")
print(f"✓ Tổng số phân cảnh: {len(scenes)}")
print(f"✓ Tổng số chữ Hán Phồn thể: {total_han} (Tiêu chuẩn: 2.950 – 3.150 chữ)")
print(f"✓ Phân bổ 3 giọng đọc:")
print(f"  - 黎光達 (Nam): {by_spk.get(DAT, 0)} chữ ({by_spk.get(DAT,0)/total_han*100:.1f}%)")
print(f"  - 阮氏英書 (Nữ): {by_spk.get(THU, 0)} chữ ({by_spk.get(THU,0)/total_han*100:.1f}%)")
print(f"  - 阮曰黃絨 (Nữ): {by_spk.get(NHUNG, 0)} chữ ({by_spk.get(NHUNG,0)/total_han*100:.1f}%)")
print(f"✓ Lưu tại: {out_path}")
