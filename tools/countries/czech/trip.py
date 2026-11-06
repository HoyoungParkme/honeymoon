"""체코(+오스트리아) 신혼여행 2027.05.09–05.18 (2인) 세 코스. build_country.py czech 가 읽는다.

근거 (2026-11-06 조사)
- 여행사: 모두투어 허니문 세미팩 '프라하2/체스키/할슈타트1/잘츠부르크1/비엔나2', 이오스여행사 체코&오스트리아 8일(체스키 1박),
  하나투어 '체코 일주 9일'(쿠트나호라·플젠 양조장·카를로비바리), 참좋은여행 '보헤미안 랩소디 체코 일주'(카를로비바리·체스키 1박)
- 명소·요금: 프라하성 메인 서킷 450 CZK, 구시청사 탑 350 CZK(온라인), 세들레츠 시간 지정 220 CZK, 체스키 성 1코스 300 CZK·탑 280 CZK,
  필스너 우르켈 투어 430 CZK, 할슈타트 푸니쿨라 €29·소금광산 €49, 쇤브룬 €30–42, 벨베데레 €23
- 항공: 구글 항공 2026-11-06 조회 (아시아나 직항 왕복 1인 ₩1,369,500)
- 교통: RegioJet·FlixBus 프라하↔체스키 €6–15, CK Shuttle 990 CZK, 쿠트나호라 열차 166 CZK, 빈→프라하 레일젯 €14.90~
- 행사: 프라하의 봄 국제음악축제 2027 개막 5/12 20:00 시민회관 (서울시향 5/12–13 출연)
- 식당: cz_restaurants.py (트립어드바이저·구글 평점, 미슐랭 빕 구르망)
환율 1€ ≈ 25 CZK. 하루 비용 합산이 유로 기준이라 요금은 '€ (CZK)' 순서로 적는다."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))  # tools/ (tripkit)
sys.path.insert(0, HERE)
from cz_places import PLACES  # noqa: E402,F401
from cz_restaurants import RESTAURANTS  # noqa: E402,F401
from tripkit import mv, st  # noqa: E402

COURSE_META = {
    1: ("코스 1 · 프라하 + 체스키크룸로프 (느린 허니문)", "#1E7FA8"),
    2: ("코스 2 · 체코 + 오스트리아 (할슈타트·잘츠부르크·빈)", "#2F7A57"),
    3: ("코스 3 · 체코 일주 (플젠·카를로비바리·체스키·쿠트나호라)", "#B8432A"),
}

# 이름, 요금 보기 링크, 1박 2인 1실 요금 (2027년 5월 요금 미오픈 → 2026년 시세 기준 추정)
HOTELS = {
    "h_prg_bohemia": ("Grand Hotel Bohemia (프라하 5성)", "https://www.kayak.co.kr/hotels/Grand-Hotel-Bohemia-Prague", "€180–240 (추정)"),
    "h_prg_987": ("987 Design Prague (4성)", "https://www.kayak.co.kr/hotels/987-Design-Prague", "€110–150 (추정)"),
    "h_prg_majestic": ("Grand Majestic Plaza (프라하 4성)", "https://www.kayak.co.kr/hotels/Grand-Majestic-Plaza-Prague", "€110–150 (추정)"),
    "h_ck_ruze": ("Hotel Růže (체스키크룸로프 4성)", "https://www.kayak.co.kr/hotels/Hotel-Ruze-Cesky-Krumlov", "€130–180 (추정)"),
    "h_ck_oldinn": ("Hotel Old Inn (스보르노스티 광장)", "https://www.kayak.co.kr/hotels/Hotel-Old-Inn-Cesky-Krumlov", "€110–160 (추정)"),
    "h_kv_pupp": ("Grandhotel Pupp (카를로비바리 5성)", "https://www.kayak.co.kr/hotels/Grandhotel-Pupp-Karlovy-Vary", "€200–280 (추정)"),
    "h_hall_heritage": ("Heritage Hotel Hallstatt (4성)", "https://www.kayak.co.kr/hotels/Heritage-Hotel-Hallstatt", "€250–350 (추정)"),
    "h_salz_europa": ("Austria Trend Hotel Europa (잘츠부르크)", "https://www.kayak.co.kr/hotels/Austria-Trend-Hotel-Europa-Salzburg", "€140–190 (추정)"),
    "h_wien_nh": ("NH Wien City (빈 4성)", "https://www.kayak.co.kr/hotels/NH-Wien-City", "€150–200 (추정)"),
}

HOTEL_META = {
    "h_prg_bohemia": {"city": "프라하 · 화약탑 옆", "search": "Grand Hotel Bohemia Prague", "official": "",
                      "alt": "이오스여행사 업그레이드 선택지(5성). 구시가 광장 도보 6분, 중앙역 도보 10분. 더 싸게는 987 Design·Grand Majestic(4성) €110~150"},
    "h_prg_987": {"city": "프라하 · 신시가 (중앙역 도보 6분)", "search": "987 Design Prague", "official": "",
                  "alt": "모두투어 체코·오스트리아 허니문 상품의 프라하 호텔. 5성을 원하면 Grand Hotel Bohemia"},
    "h_prg_majestic": {"city": "프라하 · 공화국 광장", "search": "Grand Majestic Plaza Prague", "official": "",
                       "alt": "하나투어 체코 일주 상품의 프라하 호텔. 프라하를 세 번 들르므로 같은 호텔로 잡고 큰 짐은 맡겨 두기"},
    "h_ck_ruze": {"city": "체스키크룸로프 구시가", "search": "Hotel Ruze Cesky Krumlov", "official": "",
                  "when": "체스키 구시가 숙소는 방이 적어 5월 주말이 먼저 참. 무료 취소로 지금",
                  "alt": "이오스여행사 상품의 체스키 호텔(옛 예수회 건물, 성 전망). 광장 정면을 원하면 Hotel Old Inn"},
    "h_ck_oldinn": {"city": "체스키크룸로프 · 스보르노스티 광장", "search": "Hotel Old Inn Cesky Krumlov", "official": "",
                    "when": "체스키 구시가 숙소는 방이 적음. 무료 취소로 지금",
                    "alt": "가야투어 상품의 체스키 호텔(광장 한가운데). 단체 상품 대부분은 체스키에서 자지 않음"},
    "h_kv_pupp": {"city": "카를로비바리 · 테플라 강변", "search": "Grandhotel Pupp Karlovy Vary", "official": "",
                  "alt": "1701년 문을 연 온천 도시의 상징 호텔(영화 '카지노 로얄' 촬영지). 더 싸게는 콜로나다 근처 4성 €100~140"},
    "h_hall_heritage": {"city": "할슈타트 · 선착장 앞", "search": "Heritage Hotel Hallstatt", "official": "",
                        "when": "할슈타트 마을 안 숙소는 몇 곳뿐이라 가장 먼저 매진",
                        "alt": "이오스여행사 상품의 할슈타트 호텔. 모두투어 허니문은 페닉스 홀 부티크. 마을 밖(오버트라운)은 €150~200대"},
    "h_salz_europa": {"city": "잘츠부르크 · 중앙역 앞", "search": "Austria Trend Hotel Europa Salzburg", "official": "",
                      "alt": "모두투어 허니문 상품의 잘츠부르크 호텔. 역 앞이라 짐 끌기 편함, 구시가까지 도보 20분"},
    "h_wien_nh": {"city": "빈 · 마리아힐퍼 거리", "search": "NH Wien City", "official": "",
                  "alt": "모두투어 허니문 상품의 빈 호텔. 링 안쪽을 원하면 Hotel Royal·Austria Trend Europa Wien"},
}

BREAKFAST = {
    "h_prg_bohemia": "호텔 조식 (아르데코 홀) — 보통 포함 요금이 €15~20 더 비쌈",
    "h_prg_987": "호텔 뷔페 조식",
    "h_prg_majestic": "호텔 뷔페 조식",
    "h_ck_ruze": "호텔 조식 (성 전망 홀)",
    "h_ck_oldinn": "호텔 조식 (광장 쪽 창가)",
    "h_kv_pupp": "그랜드 홀 조식 (포함)",
    "h_hall_heritage": "호텔 조식 (호수 전망)",
    "h_salz_europa": "호텔 뷔페 조식",
    "h_wien_nh": "호텔 뷔페 조식",
}
CAFES = {
    "h_prg_bohemia": "Café Imperial 아침 메뉴 (도보 7분) — €10–15",
    "h_prg_987": "Café Imperial 아침 메뉴 (도보 6분) — €10–15",
    "h_prg_majestic": "Café Imperial 아침 메뉴 (도보 4분) — €10–15",
    "h_ck_ruze": "광장 주변 카페 — 체코식 팬케이크·커피 €5–8",
    "h_ck_oldinn": "광장 주변 카페 — €5–8",
    "h_kv_pupp": "콜로나다 앞 카페 — 온천 웨이퍼(오플라트키) + 커피 €4–7",
    "h_hall_heritage": "Seecafé 호숫가 커피·케이크 — €6–10",
    "h_salz_europa": "역 앞 베이커리 — €5–8",
    "h_wien_nh": "마리아힐퍼 거리 카페 — 멜랑쥬 + 크루아상 €6–10",
}

ARRIVAL = {"wake": "집", "sleepAt": "5/9 10:45 인천 출발 (아시아나 직항, 약 13시간)",
           "bfA": "집 또는 인천공항 식당", "bfB": "기내식 2회", "startNote": "프라하 공항 도착 시각부터 시작"}

PHOTOS = {
    "old_town": ("프라하 구시가 광장과 틴 성당", ["Old Town Square Prague Tyn Church", "Prague Old Town Square"]),
    "castle": ("카를교와 프라하성", ["Charles Bridge Prague Castle", "Prague Castle from Charles Bridge"]),
    "sedlec": ("세들레츠 해골 성당", ["Sedlec Ossuary chandelier", "Sedlec Ossuary"]),
    "obecni": ("시민회관 스메타나 홀", ["Obecní dům Praha", "Municipal House Prague facade"]),
    "cesky": ("체스키크룸로프 전경", ["Český Krumlov panorama", "Cesky Krumlov castle town"]),
    "ck_castle": ("체스키크룸로프 성 탑", ["Český Krumlov Castle tower", "Cesky Krumlov castle"]),
    "vltava": ("블타바강 야경", ["Prague Vltava night", "Prague at night Vltava"]),
    "letna": ("레트나 공원에서 본 프라하 다리들", ["Prague bridges from Letná", "Letna park view Prague"]),
    "vysehrad": ("비셰흐라드 성 베드로·바울 성당", ["Vyšehrad Basilica Saints Peter and Paul", "Vysehrad Prague"]),
    "hallstatt": ("할슈타트 호수 마을", ["Hallstatt village lake", "Hallstatt Austria"]),
    "salzburg": ("호엔잘츠부르크 성과 잘츠부르크", ["Hohensalzburg Fortress Salzburg", "Salzburg old town"]),
    "schonbrunn": ("쇤브룬 궁전", ["Schloss Schönbrunn Gartenseite", "Schönbrunn Palace garden facade"]),
    "belvedere": ("벨베데레 궁전", ["Upper Belvedere Vienna", "Belvedere Palace Vienna"]),
    "karlovy": ("카를로비바리 믈린스카 콜로나다", ["Mlýnská kolonáda Karlovy Vary", "Karlovy Vary colonnade"]),
    "plzen": ("필스너 우르켈 양조장 정문", ["Pilsner Urquell brewery gate", "Pilsner Urquell Plzeň"]),
    "kutna": ("쿠트나호라 성 바르바라 대성당", ["Chrám svaté Barbory exterior", "Kutná Hora - View SW on Chrám Svaté Barbory"]),
}

# ── 자주 쓰는 문구 ──
PRG_TAXI = "€22–28 (550–700 CZK, 차량당)"
PRG_TAXI_NOTE = "Bolt 앱 또는 도착층 공식 택시 부스. AE 공항버스는 1인 200 CZK → 중앙역"
PID = "24시간권 €6 (150 CZK)"
SUNSET_PRG = "5월 중순 프라하 일몰 약 20:35"
SUNSET_CK = "5월 중순 체스키 일몰 약 20:35"


def prague_arrival(hotel, walk_ots, date="5/9", dow="일"):
    """1일차: 16:45 도착 → 체크인 → 구시가 광장·천문시계 → 로칼 → 카를교 야경."""
    return {"date": date, "dow": dow, "city": "프라하", "title": "직항 도착, 구시가 광장 첫 야경", "photo": "old_town", "sleep": hotel, "start": "16:45", "items": [
        st("prg_airport", "아시아나 직항 도착 (16:45). 입국심사 — EES 얼굴·지문 등록 → 수하물", 50),
        mv("prg_airport", hotel, "taxi", 35, "", "도착층 택시 부스 또는 Bolt 픽업 존", PRG_TAXI, PRG_TAXI_NOTE),
        st(hotel, "체크인 · 짐 풀기", 45),
        mv(hotel, "old_town_sq", "walk", walk_ots),
        st("old_town_sq", "구시가 광장 — 틴 성당·구시청사, 노을 지는 광장", 40, "무료", "소매치기 주의"),
        mv("old_town_sq", "astro_clock", "walk", 2),
        st("astro_clock", "천문시계 정각 인형극 (매시 정각, 09~23시)", 15, "무료", at="20:00"),
        mv("astro_clock", "r_lokal", "walk", 8),
        st("r_lokal", "첫 저녁: Lokál Dlouhááá — 필스너 탱크 맥주 + 튀긴 치즈·굴라시", 80, "€16–20", "전화 예약 가능, 저녁은 대기"),
        mv("r_lokal", "charles_bridge", "walk", 15),
        st("charles_bridge", "카를교 야경 — 불 켜진 프라하성", 30, "무료"),
        mv("charles_bridge", hotel, "walk", 15),
    ]}


def prague_castle(hotel, date, dow, evening="pinkasu"):
    """프라하성 09:00 → 황금소로 → 쿠흐냐 점심 → 말라 스트라나·캄파 → 휴식 → 교탑 일몰 → 저녁."""
    items = [
        mv(hotel, "castle", "tram", 30, "트램 22번 (말로스트란스카 → 프라시스키 흐라트)", "", PID, "걸어서 카를교·네루도바 거리로 올라가면 40분"),
        st("castle", "프라하성 — 성 비투스 대성당·구왕궁·성 이르지 바실리카 (메인 서킷)", 120, "€18 (450 CZK)", "09:00 개장 직후. 정오 정문 근위병 교대", at="09:00",
           link="https://www.hrad.cz/en"),
        mv("castle", "golden_lane", "walk", 5),
        st("golden_lane", "황금소로 — 카프카가 머문 파란 집(22번)", 30, "서킷 포함"),
        mv("golden_lane", "r_kuchyn", "walk", 8),
        st("r_kuchyn", "점심: Kuchyň 테라스 — 시내를 내려다보며 체코 가정식 (냄비에서 직접 고름)", 75, "€20–30", "테라스석 예약 필수", at="12:00"),
        mv("r_kuchyn", "mala_strana", "walk", 15, note="네루도바 거리 내리막"),
        st("mala_strana", "말라 스트라나 — 성 미쿨라시 성당, 바로크 골목", 30, "무료"),
        mv("mala_strana", "kampa", "walk", 8),
        st("kampa", "캄파 섬 · 존 레논 벽", 40, "무료"),
        mv("kampa", hotel, "walk", 25, note="카를교 건너기"),
        st(hotel, "호텔 휴식", 120),
    ]
    if evening == "pinkasu":
        items += [
            mv(hotel, "bridge_tower_old", "walk", 15),
            st("bridge_tower_old", "카를교 구시가 쪽 교탑 — 카를교와 프라하성 일몰 (" + SUNSET_PRG + ")", 45, "€8 (190 CZK)", at="20:00"),
            mv("bridge_tower_old", "r_pinkasu", "walk", 15),
            st("r_pinkasu", "저녁: U Pinkasů (1843년) — 콜레뇨(돼지 무릎) 하나 나눠 먹기 + 필스너", 90, "€18–24"),
            mv("r_pinkasu", hotel, "walk", 10),
        ]
    else:  # 'imperial'
        items += [
            mv(hotel, "bridge_tower_old", "walk", 15),
            st("bridge_tower_old", "카를교 교탑 일몰 (" + SUNSET_PRG + ")", 45, "€8 (190 CZK)", at="20:00"),
            mv("bridge_tower_old", "r_imperial", "taxi", 10, "", "Bolt", "€6–8 (차량당)"),
            st("r_imperial", "저녁: Café Imperial — 아르누보 모자이크 홀, 고급 스비치코바", 90, "€25–40", "예약 권장"),
            mv("r_imperial", hotel, "walk", 7),
        ]
    return {"date": date, "dow": dow, "city": "프라하", "title": "프라하성과 말라 스트라나", "photo": "castle", "sleep": hotel, "start": "08:30", "items": items}


def old_town(hotel, date, dow, evening):
    """요제포프 → 구시청사 탑 → 루브르 점심 → 국립극장·댄싱 하우스 → 휴식 → 저녁(evening: 'spring' | 'cruise' | 'pinkasu')."""
    items = [
        mv(hotel, "josefov", "walk", 12),
        st("josefov", "유대인 지구 — 시나고그·옛 유대인 묘지 (토요일 휴관)", 90, "", "통합권은 현장·온라인 (요금 확인)"),
        mv("josefov", "rudolfinum", "walk", 5),
        st("rudolfinum", "루돌피눔 · 블타바 강변 산책", 15, "무료"),
        mv("rudolfinum", "astro_clock", "walk", 10),
        st("astro_clock", "구시청사 탑 — 구시가 광장 360° 전망", 40, "€14 (350 CZK, 온라인)", "현장은 450 CZK"),
        mv("astro_clock", "r_louvre", "walk", 12, note="나로드니 거리"),
        st("r_louvre", "점심: Café Louvre (1902년) — 스비치코바 + 홈메이드 케이크", 75, "€18–22", "온라인 예약 가능", at="12:30"),
        mv("r_louvre", "national_theatre", "walk", 4),
        st("national_theatre", "국립극장 · 레기교 강변", 15, "무료"),
        mv("national_theatre", "dancing_house", "walk", 12),
        st("dancing_house", "댄싱 하우스 (외관) · 나플라브카 강변", 30, "무료"),
        mv("dancing_house", hotel, "tram", 20, "트램 (나로드니 → 공화국 광장)", "", "24시간권"),
        st(hotel, "호텔 휴식", 120),
    ]
    if evening == "spring":
        items += [
            mv(hotel, "r_imperial", "walk", 7),
            st("r_imperial", "이른 저녁: Café Imperial — 아르누보 타일 홀, 스비치코바", 90, "€25–40", "예약 권장", at="17:45"),
            mv("r_imperial", "obecni_dum", "walk", 6),
            st("obecni_dum", "프라하의 봄 국제음악축제 개막 공연 — 시민회관 스메타나 홀 (2027년은 서울시향이 5/12~13 출연)", 130, "",
               "festival.cz 티켓 오픈 즉시 (개막 공연은 빨리 매진). 정장 차림", at="20:00", link="https://festival.cz/en/"),
            mv("obecni_dum", hotel, "walk", 7),
        ]
    elif evening == "cruise":
        items += [
            mv(hotel, "vltava_pier", "walk", 15),
            st("vltava_pier", "블타바강 디너 크루즈 — 뷔페 + 프라하성·카를교 야경 (약 3시간)", 180, "€62–69 (1,557–1,730 CZK)", "클룩·마이리얼트립. 재즈 보트는 €49+식사 €31", at="19:00"),
            mv("vltava_pier", hotel, "walk", 15),
        ]
    else:
        items += [
            mv(hotel, "r_uprince", "walk", 10),
            st("r_uprince", "Terasa U Prince 옥상 — 구시가 광장 일몰 음료 (" + SUNSET_PRG + ")", 60, "€8–12", "식사는 다른 곳에서 (전망값)", at="19:45"),
            mv("r_uprince", "r_pinkasu", "walk", 8),
            st("r_pinkasu", "저녁: U Pinkasů — 콜레뇨 + 필스너", 90, "€18–24"),
            mv("r_pinkasu", hotel, "walk", 10),
        ]
    return {"date": date, "dow": dow, "city": "프라하", "title": "구시가·유대인 지구, 그리고 " + {"spring": "프라하의 봄 개막 공연", "cruise": "블타바 디너 크루즈", "pinkasu": "옥상 일몰"}[evening],
            "photo": "obecni" if evening == "spring" else "vltava" if evening == "cruise" else "old_town", "sleep": hotel, "start": "09:00", "items": items}


def kutna_hora(hotel, walk_station, date, dow, dinner="kantyna"):
    """쿠트나호라 당일: 열차 → 세들레츠 10:00 → 구시가 → 다치츠키 점심 → 성 바르바라 → 프라하 복귀 → 저녁."""
    items = [
        mv(hotel, "praha_hlavni", "walk", walk_station),
        mv("praha_hlavni", "kutna_hora_station", "train", 55, "체코철도 열차 (시간당 1~2편)", "프라하 중앙역 → 쿠트나호라 중앙역", "€7 (166 CZK, 1인)", "ČD 앱으로 예매, 좌석 지정 없음"),
        mv("kutna_hora_station", "sedlec", "walk", 12),
        st("sedlec", "세들레츠 해골 성당 — 유골 약 4만 구로 꾸민 납골당", 40, "€9 (220 CZK)", "시간 지정 예약 필수", at="10:00", link="https://www.sedlec.info/en/"),
        mv("sedlec", "kutna_centre", "bus", 15, "시내버스 (세들레츠 → 구시가)", "", "현금 (요금 확인)", "또는 연결 열차로 시내역까지 7분"),
        st("kutna_centre", "쿠트나호라 구시가 — 중세 은광 도시, 유네스코 세계유산", 40, "무료"),
        mv("kutna_centre", "r_dacicky", "walk", 3),
        st("r_dacicky", "점심: Dačický — 멧돼지 굴라시 + 지역 탱크 맥주 (쿠트나호라 1위)", 75, "€15–25", "온라인 예약", at="12:00"),
        mv("r_dacicky", "st_barbara", "walk", 10, note="예수회 거리 조각상 길"),
        st("st_barbara", "성 바르바라 대성당 — 광부들이 지은 고딕 대성당, 계곡 전망", 60, "", "입장료 현장"),
        mv("st_barbara", "kutna_mesto", "walk", 15),
        mv("kutna_mesto", "kutna_hora_station", "train", 7, "연결 열차", "시내역 → 중앙역", "왕복권에 포함되는지 확인"),
        mv("kutna_hora_station", "praha_hlavni", "train", 55, "체코철도 열차", "", "€7 (166 CZK, 1인)"),
        mv("praha_hlavni", hotel, "walk", walk_station),
        st(hotel, "호텔 휴식", 100),
    ]
    if dinner == "kantyna":
        items += [
            mv(hotel, "r_kantyna", "walk", 12),
            st("r_kantyna", "저녁: Kantýna — 정육점 겸 고기집, 타타라크(소고기 육회)·스테이크", 80, "€20–30", "예약 없음 (입구 티켓 → 카운터 주문)", at="19:00"),
            mv("r_kantyna", hotel, "walk", 12),
        ]
    else:
        items += [
            mv(hotel, "r_vycep", "tram", 20, "트램 (비노흐라디 방면)", "", "24시간권"),
            st("r_vycep", "마지막 만찬: Výčep — 미슐랭 빕 구르망, 현대 체코 요리", 100, "€25–35", "예약 권장", at="19:30"),
            mv("r_vycep", hotel, "taxi", 15, "", "Bolt", "€8–10 (차량당)"),
        ]
    return {"date": date, "dow": dow, "city": "쿠트나호라 (당일)", "title": "해골 성당과 은광 도시 쿠트나호라", "photo": "sedlec", "sleep": hotel, "start": "08:30", "items": items}


def ck_arrival(prev_hotel, ck_hotel, date, dow):
    """프라하 → 체스키 버스 → 파파스 점심 → 성 탑 → 망토 다리·정원 → 세미나리 정원 일몰 → 샤틀라바."""
    return {"date": date, "dow": dow, "city": "프라하 → 체스키크룸로프", "title": "동화 마을 체스키크룸로프", "photo": "cesky", "sleep": ck_hotel, "start": "07:45", "items": [
        st(prev_hotel, "체크아웃 (큰 짐은 프라하 호텔에 맡겨도 됨)", 15),
        mv(prev_hotel, "na_knizeci", "metro", 25, "메트로 B선 → 안델", "", "30분권 (요금 확인)"),
        st("na_knizeci", "RegioJet 버스 탑승 (08:30경)", 10, "", "좌석 지정, 1~2주 전 예매", at="08:20"),
        mv("na_knizeci", "ck_bus", "bus", 175, "RegioJet / FlixBus", "나 크니제치(안델) → 체스키크룸로프", "€8–15 (1인)", "CK Shuttle(호텔 앞→호텔 앞)은 1인 990 CZK"),
        mv("ck_bus", ck_hotel, "walk", 12, note="구시가까지 내리막 자갈길"),
        st(ck_hotel, "짐 맡기기", 10),
        mv(ck_hotel, "r_papas", "walk", 5),
        st("r_papas", "점심: Papa's Living — 블타바 강변 테라스, 립 + 스비치코바", 75, "€18–36", "며칠 전 온라인 예약 (테라스 요청)"),
        mv("r_papas", "ck_castle", "walk", 6),
        st("ck_castle", "성 탑 오르기 — 붉은 지붕 마을과 강 굽이 전체", 50, "€11 (280 CZK, 박물관+탑)"),
        mv("ck_castle", "ck_garden", "walk", 10),
        st("ck_garden", "망토 다리 · 바로크 성 정원", 60, "무료"),
        mv("ck_garden", ck_hotel, "walk", 12),
        st(ck_hotel, "체크인 · 휴식", 90),
        mv(ck_hotel, "ck_view", "walk", 5),
        st("ck_view", "세미나리 정원 — 성과 마을 일몰 (" + SUNSET_CK + ")", 40, "무료", at="19:50"),
        mv("ck_view", "r_satlava", "walk", 5),
        st("r_satlava", "저녁: Krčma v Šatlavské — 중세 동굴 선술집, 장작불 그릴 꼬치", 90, "€20–30", "예약 필수 (론리플래닛 Top choice)"),
        mv("r_satlava", ck_hotel, "walk", 5),
    ]}


def ck_full_day(ck_hotel, date, dow):
    """체스키 둘째 날: 성 내부 1코스 → 광장 → 점심 → 블타바 카누 → 휴식 → 슈베이크."""
    return {"date": date, "dow": dow, "city": "체스키크룸로프", "title": "성 내부 투어와 블타바강 카누", "photo": "ck_castle", "sleep": ck_hotel, "start": "09:00", "items": [
        mv(ck_hotel, "ck_castle", "walk", 8),
        st("ck_castle", "성 내부 1코스 — 르네상스 홀·황금 마차 (가이드 동반)", 60, "€12 (300 CZK)", "시간 지정, 5월 주말은 매진 빠름", at="09:30",
           link="https://www.zamek-ceskykrumlov.cz/en"),
        mv("ck_castle", "ck_square", "walk", 5),
        st("ck_square", "스보르노스티 광장 · 골목 산책 · 에곤 실레 아트센터", 70, ""),
        st("ck_square", "점심: 광장 주변에서 가볍게", 50, "€10–15"),
        mv("ck_square", "ck_rafting", "walk", 8),
        st("ck_rafting", "블타바강 카누·래프팅 1시간 — 마을을 둥글게 도는 짧은 코스 (5월 물이 차가워 선택)", 90, "", "강변 대여소 현장 (요금 확인)"),
        mv("ck_rafting", ck_hotel, "walk", 8),
        st(ck_hotel, "호텔 휴식", 120),
        mv(ck_hotel, "ck_square", "walk", 3),
        st("ck_square", "광장 · 성 야경 산책", 30, "무료"),
        mv("ck_square", "r_svejk", "walk", 5),
        st("r_svejk", "저녁: Švejk — 체코 전통 요리 + 필스너", 80, "€15–25", at="19:00"),
        mv("r_svejk", ck_hotel, "walk", 5),
    ]}


def ck_to_prague(ck_hotel, hotel, date, dow, evening):
    """체스키 → 프라하 버스 → 레트나 전망 → 저녁(evening: 'cruise' | 'pinkasu')."""
    items = [
        st(ck_hotel, "아침 마을 산책 · 체크아웃", 60),
        mv(ck_hotel, "ck_bus", "walk", 12),
        mv("ck_bus", "na_knizeci", "bus", 175, "RegioJet / FlixBus", "체스키크룸로프 → 프라하 안델", "€8–15 (1인)"),
        mv("na_knizeci", hotel, "metro", 25, "메트로 B선", "", "30분권"),
        st(hotel, "체크인 · 휴식", 90),
        mv(hotel, "letna", "tram", 20, "트램 (레트나 방면)", "", PID),
        st("letna", "레트나 공원 — 블타바강 다리들이 겹쳐 보이는 전망, 비어가든", 60, "맥주 €3–4"),
        mv("letna", hotel, "tram", 20, fare="24시간권"),
    ]
    if evening == "cruise":
        items += [
            mv(hotel, "vltava_pier", "walk", 15),
            st("vltava_pier", "블타바강 디너 크루즈 — 뷔페 + 야경 (약 3시간)", 180, "€62–69 (1,557–1,730 CZK)", "클룩·마이리얼트립 예약", at="19:00"),
            mv("vltava_pier", hotel, "walk", 15),
        ]
    else:
        items += [
            mv(hotel, "r_lokal", "walk", 10),
            st("r_lokal", "저녁: Lokál Dlouhááá — 세게딘 굴라시·슈니첼", 80, "€16–20"),
            mv("r_lokal", hotel, "walk", 10),
        ]
    return {"date": date, "dow": dow, "city": "체스키크룸로프 → 프라하", "title": "프라하로 돌아와 " + ("블타바 디너 크루즈" if evening == "cruise" else "레트나 전망"),
            "photo": "vltava" if evening == "cruise" else "letna", "sleep": hotel, "start": "08:30", "items": items}


def prague_slow(hotel, date, dow):
    """프라하 여유 일: 비셰흐라드 → 나플라브카 → 페트르진 → 말라 스트라나 → 레트나 일몰 → 비체프."""
    return {"date": date, "dow": dow, "city": "프라하", "title": "비셰흐라드와 페트르진, 현지인의 프라하", "photo": "vysehrad", "sleep": hotel, "start": "09:30", "items": [
        mv(hotel, "vysehrad", "metro", 20, "메트로 C선 → 비셰흐라드", "", PID),
        st("vysehrad", "비셰흐라드 성채 — 성 베드로·바울 성당, 스메타나·드보르자크 묘지, 강 전망", 90, "무료"),
        mv("vysehrad", "naplavka", "walk", 15, note="강변 계단으로"),
        st("naplavka", "나플라브카 강변 산책 (토요일 오전엔 농산물 시장)", 30, "무료"),
        mv("naplavka", "r_louvre", "walk", 15),
        st("r_louvre", "점심: Café Louvre — 스비치코바·케이크", 70, "€18–22"),
        mv("r_louvre", "petrin", "tram", 20, "트램 + 걸어서 페트르진 언덕", "", "24시간권", "푸니쿨라 운행 여부는 현지 확인"),
        st("petrin", "페트르진 전망대 — 작은 에펠탑에서 프라하성과 구시가", 60, "€10 (250 CZK)"),
        mv("petrin", "mala_strana", "walk", 25, note="장미정원 → 내리막"),
        st("mala_strana", "말라 스트라나 카페 휴식", 50, "€8–12"),
        mv("mala_strana", hotel, "tram", 15, fare="24시간권"),
        st(hotel, "호텔 휴식", 60),
        mv(hotel, "letna", "tram", 20, fare="24시간권"),
        st("letna", "레트나 메트로놈 — 다리들 위로 지는 해 (" + SUNSET_PRG + ")", 50, "무료", at="19:50"),
        mv("letna", "r_vycep", "taxi", 15, "", "Bolt", "€8–10 (차량당)"),
        st("r_vycep", "저녁: Výčep — 미슐랭 빕 구르망, 현대 체코 요리", 100, "€25–35", "예약 권장"),
        mv("r_vycep", hotel, "taxi", 15, "", "Bolt", "€8–10 (차량당)"),
    ]}


def prague_last(hotel, walk_ots):
    """10일차(화): 바츨라프 광장·쇼핑 → 칸티나 점심 → 18:50 아시아나."""
    return {"date": "5/18", "dow": "화", "city": "프라하 → 인천", "title": "마지막 산책, 저녁 직항으로 귀국", "photo": "old_town", "sleep": None, "start": "09:30", "items": [
        mv(hotel, "old_town_sq", "walk", walk_ots),
        st("old_town_sq", "아침의 구시가 광장 — 사람 없는 시간 사진", 30, "무료"),
        mv("old_town_sq", "powder_tower", "walk", 6),
        st("powder_tower", "화약탑 · 기념품 (보헤미안 크리스털, 마리오네트, 꿀 케이크)", 60, "€20–60"),
        mv("powder_tower", "wenceslas", "walk", 10),
        st("wenceslas", "바츨라프 광장 — 1989 벨벳 혁명의 광장, 국립박물관 외관", 30, "무료"),
        mv("wenceslas", "r_kantyna", "walk", 5),
        st("r_kantyna", "점심: Kantýna — 타타라크·스테이크", 70, "€20–30", at="12:00"),
        mv("r_kantyna", hotel, "walk", 12),
        st(hotel, "맡긴 짐 찾기", 10),
        mv(hotel, "prg_airport", "taxi", 40, "", "호텔에서 Bolt 호출", PRG_TAXI, "오후 정체 대비 45분"),
        st("prg_airport", "체크인 · 택스리펀 · 출국 (아시아나 18:50 → 인천 5/19 13:10)", 60, "", "택스리펀은 출국 심사 전 세관 도장", at="16:00"),
    ]}


# ───────────────────────── 코스 1: 프라하 + 체스키 (느린 허니문) ─────────────────────────
H1 = "h_prg_bohemia"
C1 = [
    prague_arrival(H1, 6),
    prague_castle(H1, "5/10", "월", "pinkasu"),
    kutna_hora(H1, 10, "5/11", "화", "kantyna"),
    old_town(H1, "5/12", "수", "spring"),
    ck_arrival(H1, "h_ck_ruze", "5/13", "목"),
    ck_full_day("h_ck_ruze", "5/14", "금"),
    ck_to_prague("h_ck_ruze", H1, "5/15", "토", "cruise"),
    prague_slow(H1, "5/16", "일"),
    {"date": "5/17", "dow": "월", "city": "프라하", "title": "느린 하루, 옥상 일몰과 마지막 만찬", "photo": "letna", "sleep": H1, "start": "10:00", "items": [
        st(H1, "늦잠 · 호텔 조식", 60),
        mv(H1, "strahov", "tram", 30, "트램 22번 (포호젤레츠 방면)", "", PID),
        st("strahov", "스트라호프 수도원 — 언덕 위 수도원 정원과 시내 전망 (도서관은 복도에서 관람, 요금 현장)", 60, ""),
        mv("strahov", "r_kuchyn", "walk", 12),
        st("r_kuchyn", "점심: Kuchyň 테라스 — 다시 한 번 프라하 전망", 75, "€20–30", "테라스석 예약", at="13:00"),
        mv("r_kuchyn", "kampa", "walk", 20),
        st("kampa", "캄파 공원 낮잠 · 강변 벤치", 60, "무료"),
        mv("kampa", H1, "walk", 25),
        st(H1, "호텔 휴식 · 짐 정리", 120),
        mv(H1, "r_uprince", "walk", 8),
        st("r_uprince", "Terasa U Prince 옥상 — 구시가 광장 일몰 음료 (" + SUNSET_PRG + ")", 60, "€8–12", "음료만 (전망값)", at="19:45"),
        mv("r_uprince", "r_imperial", "taxi", 8, "", "Bolt", "€6–8 (차량당)"),
        st("r_imperial", "마지막 만찬: Café Imperial — 아르누보 타일 홀", 90, "€25–40", "예약"),
        mv("r_imperial", H1, "walk", 7),
    ]},
    prague_last(H1, 6),
]

# ───────────────────────── 코스 2: 체코 + 오스트리아 ─────────────────────────
H2 = "h_prg_987"
C2 = [
    prague_arrival(H2, 12),
    prague_castle(H2, "5/10", "월", "imperial"),
    old_town(H2, "5/11", "화", "cruise"),
    ck_arrival(H2, "h_ck_oldinn", "5/12", "수"),
    {"date": "5/13", "dow": "목", "city": "체스키크룸로프 → 할슈타트", "title": "셔틀로 국경 넘어 할슈타트", "photo": "hallstatt", "sleep": "h_hall_heritage", "start": "07:30", "items": [
        mv("h_ck_oldinn", "ck_garden", "walk", 10),
        st("ck_garden", "아침 망토 다리 · 성 안뜰 산책 (관광객 오기 전)", 40, "무료"),
        mv("ck_garden", "h_ck_oldinn", "walk", 10),
        st("h_ck_oldinn", "조식 · 체크아웃", 60),
        st("h_ck_oldinn", "CK Shuttle 호텔 앞 픽업", 5, "", at="09:50"),
        mv("h_ck_oldinn", "hallstatt", "bus", 180, "CK Shuttle 미니밴 (호텔 → 할슈타트 주차장)", "체스키크룸로프 → 할슈타트", "€40 (990 CZK, 1인)", "3~4일 전 예약. 이오스여행사 일정과 같은 09:50 출발"),
        mv("hallstatt", "h_hall_heritage", "walk", 8),
        st("h_hall_heritage", "짐 맡기기", 10),
        mv("h_hall_heritage", "r_seecafe", "walk", 3),
        st("r_seecafe", "점심: Seecafé — 호숫가 테라스 (마을 안에서 드물게 평이 좋은 곳)", 60, "€10–18"),
        mv("r_seecafe", "hallstatt_skywalk", "funicular", 8, "잘츠베르크반 푸니쿨라", "마을 → 소금광산 언덕", "왕복 €29", "소금광산 투어 포함 €49"),
        st("hallstatt_skywalk", "스카이워크 '세계유산 전망대' — 호수와 마을을 350m 위에서", 60, ""),
        mv("hallstatt_skywalk", "hallstatt", "funicular", 8, fare="왕복권"),
        st("hallstatt", "마을 골목 · 마르크트 광장 · 납골당(바인하우스)", 60, ""),
        mv("hallstatt", "h_hall_heritage", "walk", 5),
        st("h_hall_heritage", "체크인 · 휴식", 80),
        mv("h_hall_heritage", "hallstatt_view", "walk", 8),
        st("hallstatt_view", "엽서 뷰포인트 — 단체 관광객이 빠진 저녁 (일몰 약 20:35)", 40, "무료", "주민 사유지·드론 금지", at="19:40"),
        mv("hallstatt_view", "h_hall_heritage", "walk", 8),
        st("h_hall_heritage", "저녁: 호텔 레스토랑 — 호수 송어 요리 (마을 식당은 평이 대체로 낮음)", 90, "€30–45"),
    ]},
    {"date": "5/14", "dow": "금", "city": "할슈타트 → 잘츠부르크", "title": "모차르트의 도시 잘츠부르크", "photo": "salzburg", "sleep": "h_salz_europa", "start": "07:00", "items": [
        st("hallstatt", "새벽 호숫가 — 관광버스 오기 전 거울 같은 호수", 50, "무료"),
        st("h_hall_heritage", "조식 · 체크아웃", 50),
        mv("h_hall_heritage", "hallstatt_station", "ferry", 10, "할슈타트 페리 (기차 시간에 맞춰 운항)", "선착장 → 할슈타트역", "€3–4"),
        mv("hallstatt_station", "salzburg_hbf", "train", 150, "ÖBB 지역열차 → 아트낭푸하임 환승 → 잘츠부르크", "", "€25–35 (1인, 추정)", "또는 버스 543·150번 바트이슐 경유"),
        mv("salzburg_hbf", "h_salz_europa", "walk", 3),
        st("h_salz_europa", "짐 맡기기", 10),
        mv("h_salz_europa", "mirabell", "walk", 12),
        st("mirabell", "미라벨 정원 — '사운드 오브 뮤직' 도레미 계단, 호엔잘츠부르크 성 정면", 40, "무료"),
        mv("mirabell", "getreidegasse", "walk", 10, note="마카르트 다리 (사랑의 자물쇠)"),
        st("getreidegasse", "게트라이데 거리 철제 간판 · 모차르트 생가 (외관) · 점심", 90, "€15–25"),
        mv("getreidegasse", "hohensalzburg", "funicular", 12, "페스퉁스반 푸니쿨라", "구시가 → 성", "€18–22 (성 입장 포함, 추정)"),
        st("hohensalzburg", "호엔잘츠부르크 성 — 구시가 지붕과 알프스 전망", 90, "푸니쿨라 요금에 포함"),
        mv("hohensalzburg", "h_salz_europa", "taxi", 15, "", "", "€12–15 (차량당)"),
        st("h_salz_europa", "체크인 · 휴식", 60),
        mv("h_salz_europa", "r_augustiner", "walk", 20),
        st("r_augustiner", "저녁: Augustiner Bräustübl — 1621년 수도원 맥주홀, 돌잔에 직접 따르는 맥주 + 노점 학세", 100, "€15–25", "평일 15시 오픈, 현금만", at="18:00"),
        mv("r_augustiner", "h_salz_europa", "taxi", 10, "", "", "€10–12 (차량당)"),
    ]},
    {"date": "5/15", "dow": "토", "city": "잘츠부르크 → 빈", "title": "빈, 나슈마르크트와 클림트 '키스'", "photo": "belvedere", "sleep": "h_wien_nh", "start": "08:30", "items": [
        mv("h_salz_europa", "salzburg_hbf", "walk", 3),
        mv("salzburg_hbf", "wien_hbf", "train", 150, "ÖBB 레일젯 (30분~1시간 간격)", "잘츠부르크 → 빈 중앙역", "€20–40 (1인, 조기 할인 요금, 추정)", "ÖBB 앱 스파쉬네 요금이 가장 쌈"),
        mv("wien_hbf", "h_wien_nh", "taxi", 15, "", "", "€15–18 (차량당)"),
        st("h_wien_nh", "짐 맡기기", 10),
        mv("h_wien_nh", "naschmarkt", "walk", 12),
        st("naschmarkt", "나슈마르크트 — 토요일 벼룩시장 + 노점 점심 (일요일 휴무)", 80, "€15–25"),
        mv("naschmarkt", "belvedere", "tram", 20, "트램 D (벨베데레 방면)", "", "24시간권 (요금 확인)"),
        st("belvedere", "벨베데레 상궁 — 클림트 '키스', 정원 너머 빈 시내", 100, "€23", "시간 지정 온라인 예매", link="https://www.belvedere.at/en"),
        mv("belvedere", "h_wien_nh", "tram", 25, fare="24시간권"),
        st("h_wien_nh", "체크인 · 휴식", 90),
        mv("h_wien_nh", "r_meierei", "taxi", 15, "", "", "€12–15 (차량당)"),
        st("r_meierei", "저녁: Meierei im Stadtpark — 미슐랭 빕, 비너 슈니첼 + 치즈", 100, "€30–45", "예약 권장", at="19:30"),
        mv("r_meierei", "h_wien_nh", "taxi", 15, "", "", "€12–15 (차량당)"),
    ]},
    {"date": "5/16", "dow": "일", "city": "빈", "title": "쇤브룬 궁전과 슈테판 대성당, 오페라의 밤", "photo": "schonbrunn", "sleep": "h_wien_nh", "start": "08:30", "items": [
        mv("h_wien_nh", "schonbrunn", "metro", 25, "U3 → U4 쇤브룬역", "", "24시간권"),
        st("schonbrunn", "쇤브룬 궁전 그랜드 투어 + 정원 · 글로리에테 언덕", 180, "€30–42", "시간 지정 온라인 예매", at="09:00", link="https://www.schoenbrunn.at/en"),
        mv("schonbrunn", "r_figlmuller", "metro", 25, "U4 → U1 슈테판스플라츠", "", "24시간권"),
        st("r_figlmuller", "점심: Figlmüller — 접시보다 큰 비너 슈니첼 (1905년)", 75, "€20–30", "예약 필수. 슈니첼 하나를 둘이 나눠도 충분"),
        mv("r_figlmuller", "stephansdom", "walk", 3),
        st("stephansdom", "슈테판 대성당 — 남탑 계단 (일요일 미사 시간엔 관람 제한)", 60, ""),
        mv("stephansdom", "hofburg", "walk", 10, note="그라벤 거리 · 콜마르크트"),
        st("hofburg", "호프부르크 왕궁 · 미하엘러 광장 · 왕궁 정원", 60, "무료 (외관·정원)"),
        mv("hofburg", "h_wien_nh", "walk", 20),
        st("h_wien_nh", "호텔 휴식 · 옷 갈아입기", 90),
        mv("h_wien_nh", "staatsoper", "walk", 15),
        st("staatsoper", "빈 국립오페라극장 — 오페라·발레 공연 (5월 시즌 중)", 180, "", "공식 사이트 좌석 예매 (입석은 당일)", at="19:00", link="https://www.wiener-staatsoper.at/en/"),
        mv("staatsoper", "h_wien_nh", "walk", 15),
    ]},
    {"date": "5/17", "dow": "월", "city": "빈 → 프라하", "title": "프라하로 돌아와 성 테라스 마지막 만찬", "photo": "letna",
     "note": "5/17은 오스트리아 성령강림 월요일(공휴일) — 빈 상점 대부분 휴무라 아침에 바로 이동", "sleep": H2, "start": "08:30", "items": [
        mv("h_wien_nh", "wien_hbf", "taxi", 15, "", "", "€15–18 (차량당)"),
        mv("wien_hbf", "praha_hlavni", "train", 240, "ÖBB 레일젯 / RegioJet", "빈 중앙역 → 프라하 중앙역", "€15–30 (1인, 조기 요금 €14.90~)", "1~2달 전 예매"),
        mv("praha_hlavni", H2, "walk", 6),
        st(H2, "체크인 · 휴식", 90),
        mv(H2, "letna", "tram", 20, "트램 (레트나 방면)", "", PID),
        st("letna", "레트나 공원 비어가든 — 블타바강 다리 전망", 60, "맥주 €3–4"),
        mv("letna", "r_kuchyn", "walk", 25, note="공원 → 프라하성 북쪽 정원"),
        st("r_kuchyn", "마지막 만찬: Kuchyň 테라스 — 프라하 일몰 (" + SUNSET_PRG + ")", 100, "€20–30", "테라스석 예약 필수", at="19:15"),
        mv("r_kuchyn", "charles_bridge", "walk", 20, note="네루도바 거리 내리막"),
        st("charles_bridge", "카를교 마지막 야경", 20, "무료"),
        mv("charles_bridge", H2, "taxi", 10, "", "Bolt", "€6–8 (차량당)"),
    ]},
    prague_last(H2, 12),
]

# ───────────────────────── 코스 3: 체코 일주 ─────────────────────────
H3 = "h_prg_majestic"
C3 = [
    prague_arrival(H3, 10),
    prague_castle(H3, "5/10", "월", "pinkasu"),
    {"date": "5/11", "dow": "화", "city": "프라하 → 플젠 → 카를로비바리", "title": "필스너 양조장 지나 온천 도시로", "photo": "plzen", "sleep": "h_kv_pupp", "start": "08:00", "items": [
        st(H3, "체크아웃 (큰 짐은 호텔에 맡김, 1박 가방만)", 15),
        mv(H3, "praha_hlavni", "walk", 12),
        mv("praha_hlavni", "plzen_station", "train", 90, "체코철도 열차 (시간당 1~2편)", "프라하 중앙역 → 플젠 중앙역", "€6–10 (1인, 추정)"),
        mv("plzen_station", "pilsner", "walk", 10),
        st("pilsner", "필스너 우르켈 양조장 투어 — 지하 저장고에서 여과 안 한 맥주 시음", 100, "€17 (430 CZK)", "영어 투어 시간 지정 예약", at="11:00", link="https://www.prazdrojvisit.cz/en/"),
        st("pilsner", "점심: 양조장 펍 Na Spilce — 굴라시 + 탱크 맥주", 70, "€15–20"),
        mv("pilsner", "plzen_bus", "taxi", 10, "", "", "€6–8 (차량당)"),
        mv("plzen_bus", "kv_bus", "bus", 90, "시외버스", "플젠 → 카를로비바리", "€5–8 (1인, 추정)"),
        mv("kv_bus", "h_kv_pupp", "taxi", 10, "", "터미널 택시", "€6–8 (차량당)"),
        st("h_kv_pupp", "체크인 · 그랜드호텔 푸프 산책", 60),
        mv("h_kv_pupp", "kv_colonnade", "walk", 15, note="테플라 강변 산책로"),
        st("kv_colonnade", "믈린스카 콜로나다 — 온천수 컵으로 시음 (12개 샘)", 40, "컵 €5–10"),
        mv("kv_colonnade", "r_sklipek", "walk", 10),
        st("r_sklipek", "저녁: Restaurace Sklípek — 푸짐한 체코 고기 요리", 80, "€12–20", "현금 준비 (일요일 휴무라는 후기)", at="18:30"),
        mv("r_sklipek", "h_kv_pupp", "taxi", 10, "", "", "€6–8 (차량당)"),
    ]},
    {"date": "5/12", "dow": "수", "city": "카를로비바리 → 프라하", "title": "온천 도시 아침, 밤엔 프라하의 봄 개막", "photo": "karlovy", "sleep": H3, "start": "08:30", "items": [
        st("h_kv_pupp", "조식 · 호텔 스파", 90),
        mv("h_kv_pupp", "kv_diana", "funicular", 10, "디아나 푸니쿨라", "그랜드호텔 푸프 뒤 → 전망대", "요금 현장"),
        st("kv_diana", "디아나 전망대 — 숲속 온천 도시 전경", 40, ""),
        mv("kv_diana", "kv_vridlo", "walk", 25, note="숲길 내리막"),
        st("kv_vridlo", "브르지들로 — 12m 솟는 72°C 간헐천", 30, "무료"),
        st("kv_vridlo", "점심: 콜로나다 주변 카페 (온천 웨이퍼 오플라트키)", 50, "€10–15"),
        mv("kv_vridlo", "kv_bus", "taxi", 10, "", "", "€6–8 (차량당)"),
        mv("kv_bus", "florenc", "bus", 135, "RegioJet / FlixBus", "카를로비바리 → 프라하 플로렌츠", "€7–16 (1인)"),
        mv("florenc", H3, "walk", 12),
        st(H3, "체크인 · 휴식", 75),
        mv(H3, "r_imperial", "walk", 4),
        st("r_imperial", "이른 저녁: Café Imperial — 아르누보 타일 홀, 스비치코바", 90, "€25–40", "예약 권장", at="17:45"),
        mv("r_imperial", "obecni_dum", "walk", 6),
        st("obecni_dum", "프라하의 봄 국제음악축제 개막 공연 — 시민회관 스메타나 홀 (2027년은 서울시향이 5/12~13 출연)", 130, "",
           "festival.cz 티켓 오픈 즉시 (개막 공연은 빨리 매진)", at="20:00", link="https://festival.cz/en/"),
        mv("obecni_dum", H3, "walk", 5),
    ]},
    ck_arrival(H3, "h_ck_oldinn", "5/13", "목"),
    ck_full_day("h_ck_oldinn", "5/14", "금"),
    ck_to_prague("h_ck_oldinn", H3, "5/15", "토", "cruise"),
    old_town(H3, "5/16", "일", "pinkasu"),
    kutna_hora(H3, 12, "5/17", "월", "vycep"),
    prague_last(H3, 10),
]

COURSES = {1: C1, 2: C2, 3: C3}

# ───────────────────────── 코스 선택 페이지 예산 (만 원, 2인, 1€ ≈ 1,500원) ─────────────────────────
# 항공: 아시아나 직항 왕복 1인 136.95만 × 2. 숙소: HOTELS 요금 중간값 × 박수. 현지 교통: 공항 택시·버스·열차·셔틀·대중교통.
# 입장권·체험: 프라하성·크루즈·프라하의 봄(좌석 €40~100 가정)·성 투어 등. 식비: 1인 하루 €40~50. 기타: 숙박세 + 예비비.
BUDGET = {
    "budgetTotal": 1000,
    "categories": [
        {"label": "국제선 항공", "color": "#5B8DEF"},
        {"label": "숙소 9박", "color": "#E8B04B"},
        {"label": "현지 교통", "color": "#7FD1A8"},
        {"label": "입장권·체험", "color": "#C9A4F2"},
        {"label": "식비", "color": "#F0907A"},
        {"label": "숙박세·예비비", "color": "#6F7D97"},
    ],
    "courses": {
        "course1": {"no": "COURSE 1", "accent": "#1E7FA8", "title": "프라하 + 체스키크룸로프, 느린 허니문", "tag": "프라하 5성 7박 · 체스키 구시가 2박 · 프라하의 봄 개막 공연",
                    "total": 784, "parts": [273.9, 267, 22, 76, 125, 20],
                    "photo": "photos/czech/cesky.jpg", "alt": "체스키크룸로프 전경",
                    "flightShort": "아시아나 직항", "stayShort": "5성 + 구시가",
                    "flight": "아시아나 직항 왕복 · 1인 136.95만 원 (2026-11-06 구글 항공) · 인천 10:45 → 프라하 16:45 / 프라하 18:50 → 인천 13:10",
                    "stay": "Grand Hotel Bohemia (프라하 5성) 7박 · Hotel Růže (체스키 구시가) 2박",
                    "good": "예산 안(약 784만 원). 직항이라 첫날·마지막 날이 넉넉하고, 이동은 체스키 왕복 두 번뿐",
                    "watch": "오스트리아는 빠짐. 프라하 5박째부터는 동네 산책 위주라 볼거리가 많은 걸 원하면 코스 2"},
        "course2": {"no": "COURSE 2", "accent": "#2F7A57", "title": "체코 + 오스트리아, 할슈타트·잘츠부르크·빈", "tag": "여행사 허니문 동선 · 할슈타트 1박 · 빈 오페라",
                    "total": 800, "parts": [273.9, 222, 56, 70, 150, 28],
                    "photo": "photos/czech/hallstatt.jpg", "alt": "할슈타트 호수 마을",
                    "flightShort": "아시아나 직항", "stayShort": "4성 + 할슈타트",
                    "flight": "아시아나 직항 왕복 · 1인 136.95만 원 · 빈 → 프라하는 레일젯 4시간 (프라하 왕복이라 마지막 밤은 프라하)",
                    "stay": "987 Design (프라하) 4박 · Hotel Old Inn (체스키) · Heritage (할슈타트) · Austria Trend Europa (잘츠부르크) · NH Wien City 2박",
                    "good": "모두투어 체코·오스트리아 허니문(약 480만 원/1인)과 같은 동선을 자유여행으로 약 800만 원(2인)",
                    "watch": "1~2박마다 짐을 옮김. 빈 → 프라하 기차 4시간. 5/17 오스트리아 공휴일"},
        "course3": {"no": "COURSE 3", "accent": "#B8432A", "title": "체코 일주, 플젠·카를로비바리·체스키·쿠트나호라", "tag": "여행사 체코 일주 동선 · 온천 호텔 1박 · 프라하의 봄",
                    "total": 707, "parts": [273.9, 194, 30, 72, 120, 17],
                    "photo": "photos/czech/karlovy.jpg", "alt": "카를로비바리 콜로나다",
                    "flightShort": "아시아나 직항", "stayShort": "4성 + 온천 5성",
                    "flight": "아시아나 직항 왕복 · 1인 136.95만 원 · 국내는 열차·버스",
                    "stay": "Grand Majestic Plaza (프라하) 6박 · Grandhotel Pupp (카를로비바리) · Hotel Old Inn (체스키) 2박",
                    "good": "가장 쌈(약 707만 원). 하나투어·참좋은여행 체코 일주의 핵심 도시를 기차·버스로, 체스키는 2박",
                    "watch": "프라하 호텔을 세 번 들락날락 (같은 호텔로 잡고 큰 짐 맡기기). 맥주·고기 위주 식사"},
    },
}

# ───────────────────────── 예약할 것 ─────────────────────────
ASIANA = {"what": "아시아나 직항 왕복: 인천 5/9 10:45 → 프라하 16:45 / 프라하 5/18 18:50 → 인천 5/19 13:10", "where": "인천 ↔ 프라하",
          "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 136.95만 원 (2026-11-06 구글 항공)", "when": "코스를 고르면 바로. 직항 좌석은 일찍 빠짐",
          "alt": "카타르(도하 경유) 125.2만 원, 에티하드 116.5만 원(5/10 아침 도착). 대한항공 직항은 2027 하계 운항 요일 확인",
          "links": [{"name": "네이버 항공", "tag": "한국어", "url": "https://flight.naver.com/flights/international/ICN-PRG-20270509/PRG-ICN-20270518?adult=2&fareType=Y"},
                    {"name": "아시아나 공식", "tag": "공식", "url": "https://flyasiana.com/"},
                    {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}
KLOOK = lambda kw: {"name": "클룩", "tag": "한국어", "url": "https://www.klook.com/ko/search/?query=" + kw}
MRT = lambda kw: {"name": "마이리얼트립", "tag": "한국어", "url": "https://www.myrealtrip.com/search?q=" + kw}
REGIO = {"name": "RegioJet 공식", "tag": "공식", "url": "https://www.regiojet.com/"}
FLIX = {"name": "FlixBus", "tag": "비교", "url": "https://global.flixbus.com/"}
OBB = {"name": "ÖBB 공식", "tag": "공식", "url": "https://www.oebb.at/en/"}
CD = {"name": "체코철도 ČD", "tag": "공식", "url": "https://www.cd.cz/en/"}

T_CASTLE = {"what": "프라하성 메인 서킷 (대성당·구왕궁·성 이르지·황금소로)", "where": "프라하", "dates": "5/10 09:00", "price": "€18 (450 CZK, 1인)", "when": "1~2주 전 온라인 (현장 구매도 가능)",
            "alt": "한국어 가이드 투어는 마이리얼트립", "links": [{"name": "프라하성 공식", "tag": "공식", "url": "https://www.hrad.cz/en"}, MRT("프라하성")]}
T_TOWER = {"what": "구시청사 탑 (천문시계)", "where": "프라하", "dates": None, "price": "€14 (350 CZK 온라인, 1인)", "when": "며칠 전 온라인 (현장 450 CZK)", "alt": "",
           "links": [KLOOK("프라하 구시청사")]}
T_CRUISE = {"what": "블타바강 디너 크루즈 (뷔페, 약 3시간)", "where": "프라하", "dates": None, "price": "€62–69 (1,557–1,730 CZK, 1인)", "when": "1~2주 전 (창가석 요청)",
            "alt": "재즈 보트 €49 + 식사 €31", "links": [KLOOK("블타바 디너 크루즈"), MRT("프라하 크루즈")]}
T_SPRING = {"what": "프라하의 봄 국제음악축제 개막 공연 (시민회관 스메타나 홀)", "where": "프라하", "dates": "5/12 20:00", "price": "좌석 등급별 (2027 판매가 열리면 확인)",
            "when": "판매 시작 즉시. 개막 공연은 가장 먼저 매진", "alt": "5/13 서울시향 공연, 축제 기간 다른 공연(루돌피눔 등)",
            "links": [{"name": "Prague Spring 공식", "tag": "공식", "url": "https://festival.cz/en/"}]}
T_SEDLEC = {"what": "세들레츠 해골 성당 시간 지정 입장", "where": "쿠트나호라", "dates": None, "price": "€9 (220 CZK, 1인)", "when": "1~2주 전 (시간 지정 필수)",
            "alt": "성 바르바라 대성당 통합권은 현장", "links": [{"name": "세들레츠 공식", "tag": "공식", "url": "https://www.sedlec.info/en/"}]}
T_CK = {"what": "체스키크룸로프 성 내부 1코스 (가이드 투어)", "where": "체스키크룸로프", "dates": None, "price": "€12 (300 CZK, 1인) + 탑·박물관 280 CZK", "when": "2~3주 전 시간 지정",
        "alt": "바로크 극장 투어 400 CZK (요일 한정)", "links": [{"name": "체스키 성 공식", "tag": "공식", "url": "https://www.zamek-ceskykrumlov.cz/en"}]}
T_BUS_CK = {"what": "프라하 ↔ 체스키크룸로프 버스 (왕복)", "where": "프라하 안델 ↔ 체스키 터미널", "dates": None, "price": "€8–15 (편도 1인)", "when": "1~2주 전 (좌석 지정, 주말 매진 잦음)",
            "alt": "CK Shuttle 호텔 앞→호텔 앞 990 CZK (1인)", "links": [REGIO, FLIX, {"name": "CK Shuttle", "tag": "공식", "url": "https://www.ckshuttle.cz/"}]}
T_KH_TRAIN = {"what": "프라하 ↔ 쿠트나호라 열차", "where": "프라하 중앙역 ↔ 쿠트나호라 중앙역", "dates": None, "price": "€7 (166 CZK, 편도 1인)", "when": "당일 앱·역 창구 (좌석 지정 없음)",
              "alt": "", "links": [CD]}


def rest(key, when, alt=""):
    r = RESTAURANTS[key]
    links = [{"name": "공식·예약", "tag": "공식", "url": r["url"]}] if r.get("url") else []
    links.append({"name": "트립어드바이저", "tag": "비교", "url": r["rating"]["url"]})
    return {"what": r["name"], "where": r["city"], "dates": "", "price": r["price"], "when": when, "alt": alt, "links": links}


def with_date(item, dates):
    return dict(item, dates=dates)


SITES = [
    {"name": "아고다", "url": "https://www.agoda.com/ko-kr/", "for": "숙소", "note": "한국어·원화 결제. 현지 통화(CZK·EUR)로 결제하면 수수료가 덜 붙음"},
    {"name": "트립닷컴", "url": "https://kr.trip.com/", "for": "숙소·항공·열차", "note": "한국어 고객센터. 유럽 열차도 한국어로"},
    {"name": "부킹닷컴", "url": "https://www.booking.com/index.ko.html", "for": "숙소", "note": "체스키·할슈타트 소형 숙소 재고가 가장 많음"},
    {"name": "네이버 항공", "url": "https://flight.naver.com/", "for": "국제선", "note": "아시아나·대한항공 직항과 경유편 비교"},
    {"name": "RegioJet", "url": "https://www.regiojet.com/", "for": "버스·열차", "note": "프라하↔체스키·카를로비바리·빈. 좌석 지정, 한국 카드 결제 가능"},
    {"name": "ÖBB", "url": "https://www.oebb.at/en/", "for": "오스트리아 열차", "note": "잘츠부르크→빈, 빈→프라하 레일젯. 스파쉬네 조기 요금"},
    {"name": "클룩", "url": "https://www.klook.com/ko/", "for": "투어·입장권", "note": "한국어. 블타바 크루즈·프라하성 투어"},
    {"name": "마이리얼트립", "url": "https://www.myrealtrip.com/", "for": "한국어 가이드·스냅", "note": "프라하 한국어 야경 투어·스냅 촬영 후기 많음"},
]
TAXI = [
    {"what": "프라하 공항 ↔ 시내", "note": "Bolt·Uber 550~700 CZK(€22~28, 차량당). AE 공항버스 1인 200 CZK → 중앙역. 119번 버스 + 메트로는 1인 46 CZK", "links": [{"name": "Bolt", "url": "https://bolt.eu/"}]},
    {"what": "프라하 대중교통 (PID)", "note": "24시간권 150 CZK, 72시간권 350 CZK. 트램·메트로·버스·페트르진 푸니쿨라 공통. 'PID Lítačka' 앱으로 구매", "links": [{"name": "PID", "url": "https://pid.cz/en/"}]},
    {"what": "길거리 택시 주의", "note": "구시가 광장 앞 대기 택시는 바가지가 잦음 → Bolt·Uber 앱으로 호출", "links": []},
    {"what": "체스키크룸로프", "note": "구시가는 걸어서. 버스 터미널 → 구시가 도보 10~15분 (자갈길이라 캐리어 바퀴 주의)", "links": []},
    {"what": "오스트리아 이동", "note": "할슈타트역은 호수 건너편 → 기차 시간에 맞춘 페리(€3~4). 잘츠부르크·빈은 ÖBB 앱", "links": [{"name": "ÖBB", "url": "https://www.oebb.at/en/"}]},
    {"what": "데이터", "note": "eSIM(유럽 10일 10GB) 출국 전 설치. 체코·오스트리아 모두 EU 로밍 범위", "links": []},
]

BOOKING = {
    "country": {"kicker": "ČESKO · 2027.05.09 – 05.18", "page": "czech.html"},
    "sites": SITES, "taxi": TAXI,
    "courses": {
        1: {"name": "코스 1 · 프라하 + 체스키크룸로프", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저. 코스가 정해지면 당일", "items": [ASIANA]},
            {"cat": "공연", "hint": "프라하의 봄 개막 공연은 판매 시작 즉시", "items": [T_SPRING]},
            {"cat": "숙소", "hint": "체스키 구시가 숙소부터. 무료 취소로 먼저 잡기", "auto": "hotels"},
            {"cat": "버스·열차", "hint": "", "items": [with_date(T_BUS_CK, "5/13 · 5/15"), with_date(T_KH_TRAIN, "5/11")]},
            {"cat": "입장권·투어", "hint": "세들레츠와 체스키 성은 시간 지정", "items": [T_CASTLE, with_date(T_SEDLEC, "5/11 10:00"), with_date(T_TOWER, "5/12"), with_date(T_CK, "5/14 09:30"), with_date(T_CRUISE, "5/15 19:00")]},
            {"cat": "식당", "hint": "테라스·저녁 자리 예약", "items": [
                rest("kuchyn", "1~2주 전 테라스석"), rest("satlava", "1~2주 전 (필수)"), rest("papas", "며칠 전 온라인, 테라스 요청"), rest("dacicky", "1주 전 온라인"),
                rest("imperial", "1주 전"), rest("vycep", "1주 전"), rest("louvre", "며칠 전 온라인"), rest("lokal", "당일 전화 또는 대기"), rest("kantyna", "예약 불가 — 이른 시간에")]},
        ]},
        2: {"name": "코스 2 · 체코 + 오스트리아", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [ASIANA]},
            {"cat": "숙소", "hint": "할슈타트·체스키부터 (방이 적음)", "auto": "hotels"},
            {"cat": "버스·셔틀·열차", "hint": "국경 넘는 구간은 1~2달 전이 가장 쌈", "items": [
                with_date(dict(T_BUS_CK, what="프라하 → 체스키크룸로프 버스 (편도)"), "5/12"),
                {"what": "CK Shuttle 체스키 → 할슈타트 (09:50)", "where": "체스키 호텔 앞 → 할슈타트", "dates": "5/13 09:50", "price": "€40 (990 CZK, 1인)", "when": "3~4일 전까지 (일찍 할수록 시간 선택)",
                 "alt": "Bean Shuttle 등 다른 셔틀사도 비슷한 요금", "links": [{"name": "CK Shuttle", "tag": "공식", "url": "https://www.ckshuttle.cz/"}]},
                {"what": "할슈타트 → 잘츠부르크 (페리 + ÖBB 열차)", "where": "할슈타트 → 잘츠부르크", "dates": "5/14 오전", "price": "€25–35 + 페리 €3–4 (1인, 추정)", "when": "당일 ÖBB 앱", "alt": "버스 543·150번 바트이슐 경유", "links": [OBB]},
                {"what": "ÖBB 레일젯 잘츠부르크 → 빈", "where": "잘츠부르크 → 빈 중앙역", "dates": "5/15 오전", "price": "€20–40 (1인, 조기 요금, 추정)", "when": "1~2달 전 스파쉬네", "alt": "WESTbahn", "links": [OBB, {"name": "트립닷컴 열차", "tag": "한국어", "url": "https://kr.trip.com/trains/"}]},
                {"what": "빈 → 프라하 레일젯 / RegioJet", "where": "빈 중앙역 → 프라하 중앙역", "dates": "5/17 오전", "price": "€15–30 (1인, 조기 €14.90~)", "when": "1~2달 전", "alt": "", "links": [OBB, REGIO]},
            ]},
            {"cat": "입장권·공연", "hint": "쇤브룬·벨베데레는 시간 지정", "items": [
                T_CASTLE, with_date(T_TOWER, "5/11"), with_date(T_CRUISE, "5/11 19:00"),
                {"what": "할슈타트 소금광산 푸니쿨라 · 스카이워크", "where": "할슈타트", "dates": "5/13 오후", "price": "푸니쿨라 왕복 €29 (소금광산 포함 €49, 1인)", "when": "현장 또는 며칠 전 온라인", "alt": "",
                 "links": [{"name": "Salzwelten 공식", "tag": "공식", "url": "https://www.salzwelten.at/en/hallstatt"}]},
                {"what": "쇤브룬 궁전 그랜드 투어", "where": "빈", "dates": "5/16 09:00", "price": "€30–42 (1인)", "when": "1~2주 전 시간 지정", "alt": "",
                 "links": [{"name": "쇤브룬 공식", "tag": "공식", "url": "https://www.schoenbrunn.at/en"}]},
                {"what": "벨베데레 상궁 (클림트 '키스')", "where": "빈", "dates": "5/15 오후", "price": "€23 (1인)", "when": "며칠 전 시간 지정", "alt": "",
                 "links": [{"name": "벨베데레 공식", "tag": "공식", "url": "https://www.belvedere.at/en"}]},
                {"what": "빈 국립오페라극장 공연", "where": "빈", "dates": "5/16 19:00", "price": "좌석 등급별 (공식 사이트)", "when": "판매가 열리면 바로 (보통 2~3달 전)", "alt": "입석은 공연 당일 현장",
                 "links": [{"name": "Wiener Staatsoper 공식", "tag": "공식", "url": "https://www.wiener-staatsoper.at/en/"}]},
            ]},
            {"cat": "식당", "hint": "", "items": [
                rest("kuchyn", "1~2주 전 테라스석 (마지막 만찬)"), rest("satlava", "1~2주 전"), rest("papas", "며칠 전 온라인"), rest("figlmuller", "1~2주 전 (필수)"),
                rest("meierei", "1주 전"), rest("augustiner", "예약 불가 — 현금"), rest("imperial", "1주 전"), rest("lokal", "당일")]},
        ]},
        3: {"name": "코스 3 · 체코 일주", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [ASIANA]},
            {"cat": "공연", "hint": "판매 시작 즉시", "items": [T_SPRING]},
            {"cat": "숙소", "hint": "체스키 광장 호텔·카를로비바리 푸프부터", "auto": "hotels"},
            {"cat": "버스·열차", "hint": "", "items": [
                {"what": "프라하 → 플젠 열차 / 플젠 → 카를로비바리 버스", "where": "프라하 → 플젠 → 카를로비바리", "dates": "5/11", "price": "열차 €6–10 + 버스 €5–8 (1인, 추정)", "when": "1주 전 앱", "alt": "", "links": [CD, REGIO]},
                {"what": "카를로비바리 → 프라하 버스", "where": "카를로비바리 → 프라하 플로렌츠", "dates": "5/12 오후", "price": "€7–16 (1인)", "when": "1~2주 전", "alt": "", "links": [REGIO, FLIX]},
                with_date(T_BUS_CK, "5/13 · 5/15"), with_date(T_KH_TRAIN, "5/17")]},
            {"cat": "입장권·투어", "hint": "", "items": [
                T_CASTLE,
                {"what": "필스너 우르켈 양조장 투어 (영어)", "where": "플젠", "dates": "5/11 11:00", "price": "€17 (430 CZK, 1인)", "when": "1~2주 전 시간 지정", "alt": "",
                 "links": [{"name": "Pilsner Urquell 공식", "tag": "공식", "url": "https://www.prazdrojvisit.cz/en/"}]},
                with_date(T_CK, "5/14 09:30"), with_date(T_CRUISE, "5/15 19:00"), with_date(T_TOWER, "5/16"), with_date(T_SEDLEC, "5/17 10:00")]},
            {"cat": "식당", "hint": "", "items": [
                rest("kuchyn", "1~2주 전 테라스석"), rest("sklipek", "며칠 전 (현금)"), rest("imperial", "1주 전"), rest("satlava", "1~2주 전"), rest("papas", "며칠 전"),
                rest("dacicky", "1주 전"), rest("vycep", "1주 전 (마지막 만찬)"), rest("pinkasu", "당일 가능")]},
        ]},
    },
}
for c in BOOKING["courses"].values():
    for g in c["groups"]:
        for it in g.get("items", []):
            it["dates"] = it.get("dates") or "코스 일정 참고"
