"""그리스 신혼여행 2027.05.09–05.18 (2인) 세 코스. build_country.py greece 가 읽는다.

근거 (2026-11-04 조사)
- 여행사: 하나투어·모두투어·참좋은여행·노랑풍선 '그리스 일주'(아테네 + 델피·메테오라 + 산토리니 2박),
  이오스여행사 허니문(아테네 1 + 산토리니 2~3 + 미코노스 2, 이아 동굴 호텔)
- 명소·요금: hhticket.gr(아크로폴리스 €30 시간 지정), 키클라데스 문화재청 2026 시간표, delostours.gr, 트립어드바이저 랭킹
- 항공: 구글 항공 2026-11-04 조회 (카타르 왕복 1인 ₩1,260,800, 국내선 ₩67,000~138,000)
- 페리: Ferryhopper·SeaJets (미코노스→산토리니 약 2시간, 이라클리온→산토리니 08:00경 출발)
- 식당: restaurants.py (트립어드바이저 평점·리뷰 수, 미슐랭 2027, 현지 매체)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))  # tools/ (tripkit)
sys.path.insert(0, HERE)
from gr_places import PLACES  # noqa: E402,F401
from gr_restaurants import RESTAURANTS  # noqa: E402,F401
from tripkit import mv, st  # noqa: E402

COURSE_META = {
    1: ("코스 1 · 섬 허니문 (미코노스 + 산토리니)", "#1E7FA8"),
    2: ("코스 2 · 그리스 일주 (델피·메테오라 + 산토리니)", "#2F7A57"),
    3: ("코스 3 · 크레타 + 산토리니", "#B8432A"),
}

# 이름, 요금 보기 링크, 1박 2인 1실 요금 (2027년 5월 요금 미오픈 → 2026년 시세 기준 추정)
HOTELS = {
    "h_ath_electra": ("Electra Palace Athens (5성)", "https://www.kayak.co.kr/hotels/Electra-Palace-Athens", "€250–330 (추정)"),
    "h_ath_plaka": ("Hotel Plaka (3성)", "https://www.kayak.co.kr/hotels/Plaka-Hotel-Athens", "€150–200 (추정)"),
    "h_ath_herodion": ("Herodion Hotel (4성)", "https://www.kayak.co.kr/hotels/Herodion-Hotel-Athens", "€200–260 (추정)"),
    "h_myk_harmony": ("Harmony Boutique Hotel (4성)", "https://www.kayak.co.kr/hotels/Harmony-Boutique-Hotel-Mykonos", "€220–320 (추정)"),
    "h_oia_andronis": ("Andronis Boutique Hotel (이아, 핫텁 스위트)", "https://www.andronis.com/", "€650–900 (추정)"),
    "h_fira_elgreco": ("El Greco Resort (피라, 4성)", "https://www.kayak.co.kr/hotels/El-Greco-Resort-Santorini", "€150–220 (추정)"),
    "h_imero_astra": ("Astra Suites (이메로비글리, 칼데라 뷰)", "https://www.astra-suites.com/", "€450–650 (추정)"),
    "h_kal_doupiani": ("Doupiani House (카스트라키, 메테오라 뷰)", "https://www.doupianihouse.gr/", "투어 요금에 포함"),
    "h_cha_delfino": ("Casa Delfino (하니아 구항, 부티크)", "https://www.casadelfino.com/", "€220–320 (추정)"),
    "h_her_lato": ("Lato Boutique Hotel (이라클리온)", "https://www.lato.gr/", "€120–160 (추정)"),
}

HOTEL_META = {
    "h_ath_electra": {"city": "아테네 · 플라카", "search": "Electra Palace Athens", "official": "https://www.electrahotels.gr/hotels/electra-palace-athens/", "alt": "루프탑 수영장에서 아크로폴리스가 보임. 더 싸게는 Hotel Plaka(3성, 루프탑 뷰) 1박 €150~200"},
    "h_ath_plaka": {"city": "아테네 · 플라카", "search": "Plaka Hotel Athens", "official": "https://www.plakahotel.gr/", "alt": "루프탑 바에서 아크로폴리스 정면. 수영장이 원하면 Electra Palace(5성)"},
    "h_ath_herodion": {"city": "아테네 · 아크로폴리스 박물관 앞", "search": "Herodion Hotel Athens", "official": "https://www.herodion.gr/", "alt": "아크로폴리스 남쪽 입구까지 도보 5분, 루프탑 정원 뷰"},
    "h_myk_harmony": {"city": "미코노스 타운 (구항 언덕)", "search": "Harmony Boutique Hotel Mykonos", "official": "", "alt": "이오스여행사 허니문 상품의 4성 선택지. 5성은 Kouros·Katikies Mykonos"},
    "h_oia_andronis": {"city": "산토리니 · 이아", "search": "Andronis Boutique Hotel Oia", "official": "https://www.andronis.com/", "when": "이아 동굴 호텔은 가장 먼저 매진. 무료 취소 요금으로 지금 잡기",
                       "alt": "이오스 허니문 상품 선택지(Petite Suite 핫텁). 예산을 줄이려면 아고다에서 '이아 동굴 스위트 핫텁' 1박 €300~450대를 찾기"},
    "h_fira_elgreco": {"city": "산토리니 · 피라 외곽", "search": "El Greco Resort Santorini", "official": "", "alt": "하나투어 그리스 일주 상품의 산토리니 호텔(수영장). 칼데라 뷰는 아님"},
    "h_imero_astra": {"city": "산토리니 · 이메로비글리", "search": "Astra Suites Santorini", "official": "https://www.astra-suites.com/", "when": "칼데라 뷰 스위트는 일찍 매진. 지금 무료 취소로",
                      "alt": "이아보다 조용한 칼데라 정면, 스카로스 바위가 바로 앞. 더 싸게는 피로스테파니 칼데라 뷰 3성 €250~350"},
    "h_kal_doupiani": {"city": "메테오라 · 카스트라키", "search": "Doupiani House Kastraki", "official": "https://www.doupianihouse.gr/", "when": "델피·메테오라 1박 2일 투어를 예약하면 투어사가 배정 (투어별로 호텔 다름)",
                       "alt": "투어 대신 직접 가면 1박 €90~130"},
    "h_cha_delfino": {"city": "크레타 · 하니아 구항", "search": "Casa Delfino Chania", "official": "https://www.casadelfino.com/", "alt": "구항 골목 17세기 저택 호텔. 주차는 구시가 밖 공영주차장"},
    "h_her_lato": {"city": "크레타 · 이라클리온", "search": "Lato Boutique Hotel Heraklion", "official": "https://www.lato.gr/", "alt": "항구 바로 위라 다음 날 08:00 페리에 걸어서 감 (트립어드바이저 4.4, 리뷰 2,579)"},
}

BREAKFAST = {
    "h_ath_electra": "호텔 조식 (루프탑 아크로폴리스 뷰) — 보통 객실 요금에 포함",
    "h_ath_plaka": "호텔 조식 — 포함 요금이 €10~15 더 비쌈",
    "h_ath_herodion": "호텔 조식 (정원 테라스)",
    "h_myk_harmony": "호텔 조식 (구항 뷰 테라스)",
    "h_oia_andronis": "객실 테라스로 가져다주는 조식 (포함)",
    "h_fira_elgreco": "호텔 뷔페 조식",
    "h_imero_astra": "칼데라 뷰 테라스 조식 (포함)",
    "h_kal_doupiani": "호텔 조식 (메테오라 바위 뷰 정원)",
    "h_cha_delfino": "호텔 조식 (안뜰)",
    "h_her_lato": "호텔 조식 (루프탑 항구 뷰)",
}
CAFES = {
    "h_ath_electra": "Ariston (1910년) 부가차·티로피타 — 신타그마, 일요일 휴무, €3–6",
    "h_ath_plaka": "Ariston (1910년) 부가차·티로피타 — 도보 8분, 일요일 휴무, €3–6",
    "h_ath_herodion": "아크로폴리스 박물관 카페 (아크로폴리스 뷰) — €6–12",
    "h_myk_harmony": "Gioras 장작 화덕 빵집 — 아몬드 쿠키·파이, €4–8",
    "h_oia_andronis": "이아 메인 거리 카페 — €8–15",
    "h_fira_elgreco": "Bakery Svoronos (24시간) — 부가차·쿨루리, €3–6",
    "h_imero_astra": "Bakery Svoronos (피라, 24시간) — €3–6",
    "h_kal_doupiani": "카스트라키 광장 카페 — €5–8",
    "h_cha_delfino": "Bougatsa Iordanis (1924년) — 치즈 부가차, €4–6",
    "h_her_lato": "사자 광장 Kirkor 부가차 — €4–6",
}

ARRIVAL = {"wake": "기내", "sleepAt": "5/9 01:20 인천 출발 (카타르항공, 도하 경유), 비행기 안에서 아침",
           "bfA": "기내식", "bfB": "도하 공항 환승 중 카페 (€5–10)", "startNote": "아테네 공항 도착 시각부터 시작"}

# 날짜 사진: 키 → (설명, 커먼즈 검색어 후보)
PHOTOS = {
    "plaka": ("아테네 아나피오티카 골목", ["Anafiotika Athens", "Plaka Athens street"]),
    "parthenon": ("아크로폴리스 파르테논", ["Parthenon Acropolis Athens", "Acropolis of Athens"]),
    "lycabettus": ("리카비토스 언덕에서 본 아테네", ["Lycabettus hill view Athens", "Athens from Lycabettus"]),
    "sounion": ("수니온 곶 포세이돈 신전", ["Temple of Poseidon Sounion", "Cape Sounion"]),
    "little_venice": ("미코노스 리틀 베니스", ["Little Venice Mykonos", "Mykonos Little Venice sunset"]),
    "delos": ("델로스 사자 테라스", ["Terrace of the Lions Delos", "Delos lions"]),
    "oia": ("산토리니 이아 마을", ["Oia Santorini", "Oia blue domes"]),
    "catamaran": ("산토리니 칼데라 바다", ["Santorini caldera sea", "Santorini caldera boat"]),
    "skaros": ("이메로비글리 스카로스 바위", ["Skaros rock Imerovigli", "Imerovigli Santorini"]),
    "pyrgos": ("산토리니 피르고스 마을", ["Pyrgos Kallistis", "Pyrgos Santorini village"]),
    "nea_kameni": ("네아 카메니 화산섬", ["Nea Kameni", "Nea Kameni volcano Santorini"]),
    "nat_museum": ("국립고고학박물관 아가멤논 황금 가면", ["Mask of Agamemnon", "National Archaeological Museum Athens"]),
    "syntagma": ("국회의사당 근위병 에브조네스", ["Evzones Syntagma", "Changing of the guard Athens"]),
    "delphi": ("델피 아폴론 신전·원형 극장", ["Delphi theatre", "Delphi Temple of Apollo"]),
    "meteora": ("메테오라 수도원", ["Meteora monasteries", "Varlaam Monastery Meteora"]),
    "chania": ("하니아 베네치아 구항 등대", ["Chania lighthouse harbour", "Chania Venetian harbour"]),
    "elafonisi": ("엘라포니시 핑크 비치", ["Elafonisi beach", "Elafonissi Crete"]),
    "knossos": ("크노소스 궁전", ["Knossos palace", "Knossos north entrance"]),
}

# ── 자주 쓰는 문구 ──
ATH_TAXI = "€40 (차량당 정액, 05~24시 · 밤 €55)"
ATH_TAXI_NOTE = "지하철 3호선은 1인 €9, 신타그마까지 40분"
ACRO = "https://www.hhticket.gr"
SUNSET_ATH = "5월 중순 아테네 일몰 약 20:25"
SUNSET_SAN = "5월 중순 산토리니 일몰 약 20:20"


def athens_arrival(hotel, walk_to_plaka, evening):
    """1일차: 12:25 도착 → 체크인 → 플라카·아나피오티카 → 저녁(evening: 'lycabettus' | 'strofi')."""
    items = [
        st("ath_airport", "카타르항공 도착 (12:25). 입국심사 — EES 얼굴·지문 등록 → 수하물", 50),
        mv("ath_airport", hotel, "taxi", 40, "", "도착층 공식 택시 승강장 (노란 택시, 정액)", ATH_TAXI, ATH_TAXI_NOTE),
        st(hotel, "체크인 · 샤워 · 낮잠 (도하 경유 17시간 비행 후)", 150),
        mv(hotel, "r_lukumades", "walk", walk_to_plaka, note="모나스티라키 쪽으로"),
        st("r_lukumades", "간식: Lukumades — 갓 튀긴 그리스식 꿀 도넛", 25, "€4–8", link="https://www.tripadvisor.com/Restaurant_Review-g189400-d5993987-Reviews-Lukumades-Athens_Attica.html"),
        mv("r_lukumades", "monastiraki", "walk", 3),
        st("monastiraki", "모나스티라키 광장 — 아크로폴리스를 처음 올려다보는 곳", 20, "무료", "소매치기 주의"),
        mv("monastiraki", "plaka", "walk", 8, note="아드리아누 거리"),
        st("plaka", "플라카 골목 산책 · 기념품 거리", 40, "무료"),
        mv("plaka", "anafiotika", "walk", 6, note="스트라토노스 거리 계단"),
        st("anafiotika", "아나피오티카 — 아크로폴리스 바로 아래 섬마을 같은 흰 골목", 30, "무료"),
    ]
    if evening == "lycabettus":
        items += [
            mv("anafiotika", "lycabettus_funicular", "taxi", 15, "", "플라카 아래 큰길에서", "€8–10 (차량당)", "걸으면 오르막 35분"),
            mv("lycabettus_funicular", "lycabettus", "funicular", 4, "리카비토스 푸니쿨라 (30분 간격)", "", "왕복 €10"),
            st("lycabettus", "리카비토스 정상 일몰 · 아크로폴리스 야경 (" + SUNSET_ATH + ")", 70, "무료", "일몰 30분 전 도착", at="19:50"),
            mv("lycabettus", "lycabettus_funicular", "funicular", 4, fare="왕복권"),
            mv("lycabettus_funicular", "r_karamanlidika", "taxi", 15, "", "", "€8–10 (차량당)"),
            st("r_karamanlidika", "첫 저녁: Ta Karamanlidika tou Fani — 파스투르마·수주키 메제 플래터", 80, "€20–30", "공식 사이트 예약 (트립어드바이저 4.7, 리뷰 7,101)", link="https://www.karamanlidika.gr/en/reservations/"),
            mv("r_karamanlidika", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        ]
    else:
        items += [
            mv("anafiotika", "acropolis_museum", "walk", 12, note="아크로폴리스 북쪽 산책로 → 디오니시우 아레오파기투 보행로"),
            st("acropolis_museum", "디오니시우 아레오파기투 보행로 — 아크로폴리스 남쪽 산책", 30, "무료"),
            mv("acropolis_museum", "r_strofi", "walk", 8),
            st("r_strofi", "첫 저녁: Strofi 루프탑 — 파르테논 정면 일몰·야경 디너 (" + SUNSET_ATH + ")", 120, "€30–45", "루프탑 자리 지정 예약, 월요일 휴무", at="19:45", link="https://strofi.gr/en/"),
            mv("r_strofi", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        ]
    return {"date": "5/9", "dow": "일", "city": "아테네", "title": "도하 경유 도착, 플라카 첫 산책", "photo": "plaka", "sleep": hotel, "start": "12:25", "items": items}


def athens_acropolis(hotel, walk_to_acro, evening):
    """2일차(월): 아크로폴리스 08:00 → 박물관 → 수블라키 → 아고라 → 근위병 → 저녁(evening: 'sounion' | 'lycabettus' | 'thes')."""
    items = [
        mv(hotel, "acropolis", "walk", walk_to_acro, note="남쪽 입구(디오니소스 극장 쪽)가 덜 붐빔"),
        st("acropolis", "아크로폴리스 08:00 첫 슬롯 — 파르테논·에렉테이온·니케 신전·헤로데스 아티쿠스 음악당", 120, "€30",
           "hhticket.gr 1시간 단위 시간 지정 예매(하루 2만 명 상한). 물·모자", at="08:00", link=ACRO),
        mv("acropolis", "acropolis_museum", "walk", 5),
        st("acropolis_museum", "아크로폴리스 박물관 — 파르테논 원본 조각, 유리 바닥 아래 유적 (월 09~17시)", 100, "€20", "시간 지정 e-티켓 (아크로폴리스와 별도)",
           link="https://etickets.theacropolismuseum.gr"),
        mv("acropolis_museum", "r_kostas", "walk", 18, note="플라카 → 에르무 거리 → 아기아스 이리니스 광장"),
        st("r_kostas", "점심: Kosta's Souvlaki — 서서 먹는 수블라키 피타 (Culinary Backstreets 선정)", 30, "€4–8", "점심 한정, 재료 떨어지면 닫음",
           link="https://www.tripadvisor.com/Restaurant_Review-g189400-d3518811-Reviews-Kosta_s_Souvlaki-Athens_Attica.html"),
        mv("r_kostas", "ancient_agora", "walk", 8, note="모나스티라키 → 아드리아누 거리"),
        st("ancient_agora", "고대 아고라 — 헤파이스토스 신전(가장 온전한 도리스식 신전), 민주주의 발상지", 70, "€20", "2025년 통합권 폐지로 별도 티켓"),
        mv("ancient_agora", "syntagma_guard", "walk", 18, note="에르무 쇼핑 거리"),
        st("syntagma_guard", "국회의사당 앞 근위병(에브조네스) 교대 — 매시 정각", 20, "무료"),
        mv("syntagma_guard", hotel, "walk", 8),
        st(hotel, "호텔 휴식 (시에스타)", 90),
    ]
    if evening == "sounion":
        items += [
            mv(hotel, "syntagma", "walk", 6),
            mv("syntagma", "sounion", "bus", 100, "수니온 선셋 반일 투어 버스 (해안도로)", "신타그마 출발 → 수니온 곶", "투어 €45–65", "입장료 포함 여부 확인 (트립어드바이저 반일투어 4.7, 리뷰 1,418)"),
            st("sounion", "포세이돈 신전 일몰 — 에게해 절벽 위 (" + SUNSET_ATH + ")", 100, "€20", "마지막 입장은 일몰 20분 전", at="19:15"),
            mv("sounion", "syntagma", "bus", 100, fare="투어 포함"),
            mv("syntagma", "r_atlantikos", "taxi", 10, "", "", "€6–8 (차량당)"),
            st("r_atlantikos", "늦은 저녁: Atlantikos — 멸치·오징어 튀김 해산물 타베르나", 60, "€15–25", "예약 안 받음, 22시 넘으면 한산",
               link="https://www.tripadvisor.com/Restaurant_Review-g189400-d7176555-Reviews-Atlantikos-Athens_Attica.html"),
            mv("r_atlantikos", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        ]
    elif evening == "lycabettus":
        items += [
            mv(hotel, "lycabettus_funicular", "taxi", 15, "", "", "€8–10 (차량당)"),
            mv("lycabettus_funicular", "lycabettus", "funicular", 4, "리카비토스 푸니쿨라", "", "왕복 €10"),
            st("lycabettus", "리카비토스 정상 일몰 · 아크로폴리스 야경 (" + SUNSET_ATH + ")", 70, "무료", at="19:50"),
            mv("lycabettus", "lycabettus_funicular", "funicular", 4, fare="왕복권"),
            mv("lycabettus_funicular", "r_karamanlidika", "taxi", 15, "", "", "€8–10 (차량당)"),
            st("r_karamanlidika", "저녁: Ta Karamanlidika tou Fani — 햄·소시지 메제 플래터", 80, "€20–30", "공식 사이트 예약", link="https://www.karamanlidika.gr/en/reservations/"),
            mv("r_karamanlidika", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        ]
    else:
        items += [
            mv(hotel, "philopappos", "walk", 15, note="아크로폴리스 남서쪽 산책로"),
            st("philopappos", "필로파포스 언덕 일몰 — 정면에서 보는 파르테논 (" + SUNSET_ATH + ")", 50, "무료", at="19:45"),
            mv("philopappos", "r_thes", "taxi", 12, "", "", "€8–10 (차량당)"),
            st("r_thes", "저녁: Thes — 트립어드바이저 아테네 1위 현대 그리스 요리", 100, "€30–45", "이메일 thespsirri@gmail.com 예약 필수",
               link="https://www.instagram.com/thesgreekcreativecuisine/"),
            mv("r_thes", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        ]
    return {"date": "5/10", "dow": "월", "city": "아테네", "title": "아크로폴리스와 고대 아테네", "photo": "parthenon", "sleep": hotel, "start": "07:40", "items": items}


def athens_last_day(prev_hotel, acro_museum_free=False):
    """10일차(화, 국제박물관의 날): 근위병·국립정원 → 점심 → 20:00 카타르항공."""
    return {"date": "5/18", "dow": "화", "city": "아테네 → 인천", "title": "마지막 산책, 밤 비행기로 귀국", "photo": "syntagma", "sleep": None, "start": "09:30",
            "note": "5/18은 국제박물관의 날 — 국립 박물관·유적 무료지만 매우 붐빔",
            "items": [
                mv(prev_hotel, "r_ariston", "walk", 8),
                st("r_ariston", "아침: Ariston (1910년) — 부가차·티로피타", 30, "€3–6", "07:30 오픈", link="https://culinarybackstreets.com/stories/athens/ariston"),
                mv("r_ariston", "syntagma_guard", "walk", 5),
                st("syntagma_guard", "근위병 교대 (매시 정각)", 20, "무료", at="11:00"),
                mv("syntagma_guard", "national_garden", "walk", 3),
                st("national_garden", "국립정원 산책", 40, "무료"),
                mv("national_garden", "panathenaic", "walk", 12),
                st("panathenaic", "파나티나이코 스타디움 — 1896년 첫 근대올림픽 대리석 경기장, 트랙 뛰어보기", 45, "€12", "오디오가이드 포함"),
                mv("panathenaic", "zeus_temple", "walk", 10),
                st("zeus_temple", "제우스 신전 · 하드리아누스 문 (울타리 밖에서)", 15, "무료"),
                mv("zeus_temple", "plaka", "walk", 8),
                st("plaka", "늦은 점심 · 기념품 (올리브오일 비누, 꿀, 피스타치오)", 90, "€20–30"),
                mv("plaka", prev_hotel, "walk", 10),
                st(prev_hotel, "맡긴 짐 찾기", 10),
                mv(prev_hotel, "ath_airport", "taxi", 45, "", "호텔 프런트에서 호출", ATH_TAXI, "퇴근 시간이라 50분 잡기"),
                st("ath_airport", "체크인 · 출국 (카타르항공 20:00 → 도하 → 인천 5/19 17:05)", 60, "", "택스리펀 서류는 출국 심사 전 세관", at="17:00"),
            ]}


# ───────────────────────── 코스 1: 섬 허니문 ─────────────────────────
C1 = [
    athens_arrival("h_ath_electra", 12, "lycabettus"),
    athens_acropolis("h_ath_electra", 15, "sounion"),
    {"date": "5/11", "dow": "화", "city": "아테네 → 미코노스", "title": "미코노스, 리틀 베니스 일몰", "photo": "little_venice", "sleep": "h_myk_harmony", "start": "09:00",
     "items": [
         mv("h_ath_electra", "r_ariston", "walk", 6),
         st("r_ariston", "아침: Ariston (1910년) — 부가차", 25, "€3–6"),
         mv("r_ariston", "h_ath_electra", "walk", 6),
         st("h_ath_electra", "체크아웃 · 수영장", 60),
         mv("h_ath_electra", "ath_airport", "taxi", 40, "", "", ATH_TAXI),
         st("ath_airport", "체크인 (SKY express 13:10 출발, 국내선 1시간 전)", 70, "", "위탁 수하물은 요금제에 따라 별도", at="12:00"),
         mv("ath_airport", "jmk_airport", "plane", 45, "SKY express 13:10 → 13:55", "아테네 → 미코노스", "€66", "구글 항공 ₩98,782 (2026-11-04). Aegean 07:35편 ₩88,244"),
         st("jmk_airport", "도착 · 수하물", 20),
         mv("jmk_airport", "h_myk_harmony", "taxi", 15, "", "공항 택시 승강장", "€20–25 (차량당)"),
         st("h_myk_harmony", "체크인 · 휴식", 90),
         mv("h_myk_harmony", "paraportiani", "walk", 10),
         st("paraportiani", "파라포르티아니 교회 — 미코노스 상징 흰 교회", 15, "무료"),
         mv("paraportiani", "matoyianni", "walk", 5),
         st("matoyianni", "마토얀니 거리 · 호라 미로 골목 쇼핑", 50, "무료"),
         mv("matoyianni", "r_katerinas", "walk", 5),
         st("r_katerinas", "Katerina's 발코니 일몰 칵테일 — 리틀 베니스 (일몰 약 20:15)", 90, "€15–20", "일몰 1시간 전 발코니 자리", at="19:15", link="https://katerinaslittlevenicemykonos.com/"),
         mv("r_katerinas", "windmills", "walk", 4),
         st("windmills", "카토 밀리 풍차 — 일몰 직후 블루아워", 15, "무료"),
         mv("windmills", "r_sakis", "walk", 8),
         st("r_sakis", "저녁: Sakis Grill House — 2인 기로스 플레이트", 50, "€6–14", "21~23시 줄"),
         mv("r_sakis", "h_myk_harmony", "walk", 10),
     ]},
    {"date": "5/12", "dow": "수", "city": "미코노스", "title": "델로스 유적과 키키스 타베르나", "photo": "delos", "sleep": "h_myk_harmony", "start": "09:30",
     "items": [
         mv("h_myk_harmony", "mykonos_oldport", "walk", 8),
         st("mykonos_oldport", "델로스행 보트 탑승 (Delos Tours 10:00)", 15, "왕복 €25", "delostours.gr 예매 또는 부두 매표소", at="09:45", link="https://www.delostours.gr/en/"),
         mv("mykonos_oldport", "delos", "boat", 30, "Delos Tours 보트", "구항 → 델로스"),
         st("delos", "델로스 유적 — 아폴론 탄생지, 사자 테라스, 유네스코 (그늘 없음: 모자·물)", 150, "€20", "섬 입장료는 현장 결제"),
         st("delos", "13:30 복귀 보트 탑승", 5, at="13:25"),
         mv("delos", "mykonos_oldport", "boat", 30, fare="왕복권"),
         mv("mykonos_oldport", "r_kikis", "taxi", 20, "", "구항 택시 승강장", "€25–30 (차량당)"),
         st("r_kikis", "점심: Kiki's Tavern — 전기 없는 숯불 타베르나, 숯불 돼지 목살 (대기 중 무료 와인)", 150, "€25–40", "예약 불가·점심만(12:30~19:00), 5월 영업 출발 전 확인, 현금"),
         mv("r_kikis", "agios_sostis", "walk", 3),
         st("agios_sostis", "아기오스 소스티스 해변 — 선베드 없는 자연 해변 (바다는 18~20°C로 차가움)", 60, "무료"),
         mv("agios_sostis", "armenistis", "taxi", 15, "", "타베르나에 택시 부탁", "€20 (차량당)"),
         st("armenistis", "아르메니스티스 등대 — 한적한 일몰", 45, "무료", at="19:40"),
         mv("armenistis", "r_baboulas", "taxi", 15, "", "", "€20 (차량당)"),
         st("r_baboulas", "저녁: Baboulas Ouzeri — 홍합 사가나키·문어 + 우조 (트립어드바이저 4.8)", 90, "€25–40", "공식 사이트 예약", link="https://www.baboulasmykonos.gr/"),
         mv("r_baboulas", "h_myk_harmony", "walk", 6),
     ]},
    {"date": "5/13", "dow": "목", "city": "미코노스 → 산토리니", "title": "고속선으로 산토리니, 아무디 일몰 디너", "photo": "oia", "sleep": "h_oia_andronis", "start": "08:30",
     "items": [
         mv("h_myk_harmony", "r_gioras", "walk", 6),
         st("r_gioras", "아침: Gioras 화덕 빵집 — 아몬드 쿠키·파이 (BBC Travel 소개)", 25, "€4–8"),
         mv("r_gioras", "h_myk_harmony", "walk", 6),
         st("h_myk_harmony", "체크아웃", 10),
         mv("h_myk_harmony", "mykonos_newport", "taxi", 10, "", "", "€15–20 (차량당)"),
         st("mykonos_newport", "SeaJets 체크인 (10:10 출발, 30분 전 도착)", 40, "", "금·일은 매진이 잦아 1~2주 전 예매", at="09:30"),
         mv("mykonos_newport", "athinios", "ferry", 140, "SeaJets 고속선 10:10 → 12:30", "미코노스 신항 → 산토리니 아티니오스", "€60–90", "Ferryhopper 수수료 없음. 멀미하면 대형선(WorldChampion Jet)"),
         st("athinios", "하선 · 미리 예약한 픽업 차량 (항구 택시는 부족)", 15),
         mv("athinios", "h_oia_andronis", "taxi", 40, "", "호텔 픽업 또는 사전 예약 차량", "€50–60 (차량당)"),
         st("h_oia_andronis", "체크인 · 동굴 스위트 핫텁", 100),
         mv("h_oia_andronis", "r_pitogyros", "walk", 4),
         st("r_pitogyros", "늦은 점심: PitoGyros — 이아에서 가장 싼 기로스 피타 (트립어드바이저 4.7)", 40, "€8–15"),
         mv("r_pitogyros", "oia", "walk", 3),
         st("oia", "이아 골목 · 파란 돔 교회 · 갤러리 산책", 60, "무료"),
         mv("oia", "ammoudi", "walk", 15, note="이아 끝에서 계단 약 300개 내려감"),
         st("r_dimitris", "일몰 디너: Dimitris Ammoudi Taverna — 바다 바로 옆 랍스터 파스타·문어 (" + SUNSET_SAN + ")", 150, "€40–70", "일몰 시간 바다쪽 자리 예약, 1.5시간 전 착석", at="18:50"),
         mv("r_dimitris", "h_oia_andronis", "taxi", 10, "", "식당에서 택시 호출 (계단 대신)", "€15 (차량당)"),
     ]},
    {"date": "5/14", "dow": "금", "city": "산토리니", "title": "카타마란 선셋 크루즈", "photo": "catamaran", "sleep": "h_oia_andronis", "start": "07:00",
     "items": [
         mv("h_oia_andronis", "oia", "walk", 3),
         st("oia", "새벽 이아 — 사람 없는 골목 사진 산책", 50, "무료"),
         mv("oia", "h_oia_andronis", "walk", 3),
         st("h_oia_andronis", "조식 · 핫텁 · 낮잠", 330),
         mv("h_oia_andronis", "vlychada", "bus", 45, "크루즈사 픽업 버스", "호텔 앞 → 블리하다 마리나", "투어 포함"),
         st("vlychada", "카타마란 선셋 크루즈 5시간 — 레드·화이트 비치, 온천, 선상 BBQ·무제한 음료, 바다 위 일몰", 330, "€110–130",
            "1~2주 전 예약. 5월 바다는 차가워 수영은 선택 (대표 상품 트립어드바이저 4.9)", at="15:00", link="https://sailing-santorini.com/"),
         mv("vlychada", "h_oia_andronis", "bus", 45, fare="투어 포함"),
     ]},
    {"date": "5/15", "dow": "토", "city": "산토리니", "title": "스카로스 바위, 아크로티리, 와이너리 일몰", "photo": "skaros", "sleep": "h_fira_elgreco", "start": "09:30",
     "items": [
         mv("h_oia_andronis", "h_fira_elgreco", "taxi", 25, "", "호텔에서 호출", "€30–35 (차량당)", "짐을 먼저 맡김"),
         st("h_fira_elgreco", "짐 맡기기", 10),
         mv("h_fira_elgreco", "imerovigli", "taxi", 10, "", "", "€12–15 (차량당)"),
         mv("imerovigli", "skaros", "walk", 20, note="칼데라 쪽 계단 내려갔다 올라옴"),
         st("skaros", "스카로스 바위 — 칼데라 한가운데 옛 성채 터", 40, "무료"),
         mv("skaros", "firostefani", "walk", 30, note="칼데라 절벽 산책로 (피라-이아 트레킹 남쪽 구간)"),
         st("r_aktaion", "점심: Aktaion (1922년) — 파바·토마토케프테데스", 75, "€25–35", "공식 사이트 폼 예약", at="13:00", link="https://www.aktaionsantorini.com"),
         mv("firostefani", "h_fira_elgreco", "walk", 15),
         st("h_fira_elgreco", "체크인 · 수영장", 90),
         mv("h_fira_elgreco", "akrotiri", "taxi", 25, "", "", "€25–30 (차량당)"),
         st("akrotiri", "아크로티리 유적 — 기원전 17세기 화산재에 덮인 '그리스의 폼페이' (토 08~18시)", 75, "€20", "실내 지붕이 있어 더운 날 좋음"),
         mv("akrotiri", "red_beach", "walk", 10),
         st("red_beach", "레드 비치 전망대 (낙석으로 해변 접근 폐쇄, 위에서만)", 20, "무료"),
         mv("red_beach", "santo_wines", "taxi", 20, "", "", "€25 (차량당)"),
         st("santo_wines", "Santo Wines 절벽 테라스 — 아시르티코 테이스팅 + 칼데라 일몰 (" + SUNSET_SAN + ")", 110, "€18–38", "일몰 테라스석은 수 주 전 예약(€40 선결제)", at="19:00", link="https://santowines.gr"),
         mv("santo_wines", "r_metaxi", "taxi", 15, "", "", "€15–20 (차량당)"),
         st("r_metaxi", "저녁: Metaxi Mas — 섬 최고 가성비 로컬 타베르나 (트립어드바이저 4.6, 리뷰 4,730)", 100, "€25–35", "전화 예약만, 10일 전 예약·전날 재확인", link="https://santorini-metaximas.gr/en"),
         mv("r_metaxi", "h_fira_elgreco", "taxi", 15, "", "식당에서 택시 호출", "€20 (차량당)"),
     ]},
    {"date": "5/16", "dow": "일", "city": "산토리니", "title": "화산섬·온천 보트, 피르고스 일몰 디너", "photo": "nea_kameni", "sleep": "h_fira_elgreco", "start": "09:00",
     "items": [
         mv("h_fira_elgreco", "r_svoronos", "walk", 10),
         st("r_svoronos", "아침: Bakery Svoronos — 부가차·쿨루리", 20, "€3–6"),
         mv("r_svoronos", "fira", "walk", 3),
         mv("fira", "fira_oldport", "funicular", 5, "피라 케이블카", "피라 → 구항 (또는 계단 588개)", "편도 €6"),
         st("fira_oldport", "화산섬·온천 보트 탑승 (10:00경)", 10, "€25–45", "보트 투어는 부두 매표소나 전날 여행사", at="09:50"),
         mv("fira_oldport", "nea_kameni", "boat", 20, "전통 보트", "구항 → 네아 카메니"),
         st("nea_kameni", "네아 카메니 화산 분화구 하이킹 + 팔레아 카메니 유황 온천 (수영복 변색 주의)", 210, "€5 (화산공원 현금)", "운항 여부 당일 확인"),
         mv("nea_kameni", "fira_oldport", "boat", 20, fare="투어 포함"),
         mv("fira_oldport", "fira", "funicular", 5, fare="편도 €6"),
         st("fira", "피라 칼데라 카페 · 쇼핑", 60, "€10–15"),
         mv("fira", "h_fira_elgreco", "walk", 10),
         st("h_fira_elgreco", "호텔 휴식", 90),
         mv("h_fira_elgreco", "pyrgos", "taxi", 15, "", "", "€15–20 (차량당)"),
         st("pyrgos", "피르고스 마을 골목 — 이아보다 한적한 중세 마을", 40, "무료"),
         mv("pyrgos", "pyrgos_castle", "walk", 8),
         st("pyrgos_castle", "카스텔리 정상 일몰 — 섬 전체 파노라마 (" + SUNSET_SAN + ")", 40, "무료", at="19:50"),
         mv("pyrgos_castle", "r_selene", "walk", 5),
         st("r_selene", "기념 디너: Selene — 2027 미슐랭 1스타 (선드라이 토마토 타르트)", 150, "€120–200", "공식 사이트 예약 필수", link="https://selene.gr/"),
         mv("r_selene", "h_fira_elgreco", "taxi", 15, "", "", "€20 (차량당)"),
     ]},
    {"date": "5/17", "dow": "월", "city": "산토리니 → 아테네", "title": "아테네로 돌아와 고고학박물관, 마지막 만찬", "photo": "nat_museum", "sleep": "h_ath_electra", "start": "09:30",
     "items": [
         st("h_fira_elgreco", "느긋한 조식 · 수영장 · 체크아웃", 150),
         mv("h_fira_elgreco", "r_luckys", "walk", 10),
         st("r_luckys", "점심: Lucky's Souvlakis — 섬에서 가장 싸고 푸짐한 기로스", 40, "€5–12"),
         mv("r_luckys", "h_fira_elgreco", "walk", 10),
         mv("h_fira_elgreco", "jtr_airport", "taxi", 15, "", "", "€20–25 (차량당)"),
         st("jtr_airport", "체크인 (Aegean 15:05 출발)", 60, at="14:00"),
         mv("jtr_airport", "ath_airport", "plane", 50, "Aegean 15:05 → 15:55", "산토리니 → 아테네", "€73", "구글 항공 ₩109,289 (2026-11-04)"),
         st("ath_airport", "도착 · 수하물", 20),
         mv("ath_airport", "h_ath_electra", "taxi", 40, "", "", ATH_TAXI),
         st("h_ath_electra", "체크인", 20),
         mv("h_ath_electra", "nat_arch_museum", "taxi", 15, "", "", "€8–10 (차량당)"),
         st("nat_arch_museum", "국립고고학박물관 — 아가멤논 황금 가면, 안티키테라 기계 (월 08~20시)", 100, "€20", "시간 지정 입장 예약 권장", link="https://www.namuseum.gr/en/episkepsi"),
         mv("nat_arch_museum", "r_thes", "taxi", 15, "", "", "€8–10 (차량당)"),
         st("r_thes", "마지막 만찬: Thes — 아테네 1위 현대 그리스 요리 (트립어드바이저 4.9, 리뷰 5,592)", 100, "€30–45", "이메일 예약 필수", at="20:30"),
         mv("r_thes", "h_ath_electra", "taxi", 10, "", "", "€6–8 (차량당)"),
     ]},
    athens_last_day("h_ath_electra"),
]

# ───────────────────────── 코스 2: 그리스 일주 ─────────────────────────
C2 = [
    athens_arrival("h_ath_plaka", 6, "strofi"),
    athens_acropolis("h_ath_plaka", 12, "lycabettus"),
    {"date": "5/11", "dow": "화", "city": "델피 → 메테오라", "title": "델피 신탁과 메테오라 일몰", "photo": "delphi", "sleep": "h_kal_doupiani", "start": "07:30",
     "note": "델피·메테오라 1박 2일 소그룹 투어 기준 (여행사 '그리스 일주' 동선을 자유여행으로). 투어사마다 시간·호텔이 다름",
     "items": [
         mv("h_ath_plaka", "syntagma", "walk", 6, note="투어 미팅 장소 (호텔 픽업이면 생략)"),
         mv("syntagma", "delphi", "bus", 180, "델피·메테오라 1박 2일 투어 차량", "아테네 → 델피", "투어 €280–350", "교통·가이드·호텔·조식 포함, 입장료 별도. GetYourGuide/클룩 '델피 메테오라 2일'"),
         st("delphi", "델피 유적·박물관 — 아폴론 신전, 원형 극장, 세상의 배꼽 옴팔로스", 150, "€20", "여름 08~20시"),
         mv("delphi", "arachova", "bus", 15, fare="투어 포함"),
         st("arachova", "점심: 아라호바 산마을 (파르나소스산 아래)", 60, "€15–25"),
         mv("arachova", "h_kal_doupiani", "bus", 210, "투어 차량", "아라호바 → 카스트라키", "투어 포함"),
         st("h_kal_doupiani", "체크인 — 창밖으로 메테오라 바위", 40),
         mv("h_kal_doupiani", "meteora_sunset", "bus", 15, "투어 차량 (일몰 투어 포함 상품)", fare="투어 포함"),
         st("meteora_sunset", "메테오라 일몰 — 바위 기둥 위 수도원들", 50, "무료", at="19:40"),
         mv("meteora_sunset", "kastraki", "bus", 10, fare="투어 포함"),
         st("kastraki", "저녁: 카스트라키 마을 타베르나 (가이드 추천)", 80, "€15–25"),
         mv("kastraki", "h_kal_doupiani", "walk", 5),
     ]},
    {"date": "5/12", "dow": "수", "city": "메테오라 → 아테네", "title": "하늘 위 수도원, 아테네로", "photo": "meteora", "sleep": "h_ath_plaka", "start": "08:30",
     "items": [
         mv("h_kal_doupiani", "great_meteoron", "bus", 15, "투어 차량", fare="투어 포함"),
         st("great_meteoron", "대 메테오론 수도원 — 가장 크고 높은 수도원 (화요일 휴무라 수요일에)", 70, "€5 (현금)", "복장: 무릎·어깨 가림 (입구에서 숄 대여)"),
         mv("great_meteoron", "varlaam", "walk", 10),
         st("varlaam", "바를라암 수도원 — 도르래 바구니, 프레스코", 50, "€5 (현금)"),
         mv("varlaam", "kalambaka", "bus", 15, fare="투어 포함"),
         st("kalambaka", "점심: 칼람바카 시내", 60, "€15–20"),
         mv("kalambaka", "syntagma", "bus", 300, "투어 차량 복귀 (약 5시간)", "칼람바카 → 아테네", "투어 포함", "일부 투어는 기차 복귀"),
         mv("syntagma", "h_ath_plaka", "walk", 6),
         st("h_ath_plaka", "체크인 · 휴식", 40),
         mv("h_ath_plaka", "r_atlantikos", "walk", 10),
         st("r_atlantikos", "저녁: Atlantikos — 멸치·오징어 튀김", 60, "€15–25", "예약 안 받음"),
         mv("r_atlantikos", "h_ath_plaka", "walk", 10),
     ]},
    {"date": "5/13", "dow": "목", "city": "아테네 → 산토리니", "title": "산토리니 도착, 칼데라 절벽 산책", "photo": "skaros", "sleep": "h_fira_elgreco", "start": "07:45",
     "items": [
         mv("h_ath_plaka", "ath_airport", "taxi", 40, "", "", ATH_TAXI),
         st("ath_airport", "체크인 (Aegean 10:05 출발)", 70, at="08:55"),
         mv("ath_airport", "jtr_airport", "plane", 50, "Aegean 10:05 → 10:55", "아테네 → 산토리니", "€68", "구글 항공 ₩101,792 (5/11 조회 기준). 위탁 수하물은 요금제 확인"),
         st("jtr_airport", "도착 · 수하물", 20),
         mv("jtr_airport", "h_fira_elgreco", "taxi", 15, "", "공항 택시 (부족하면 사전 예약 픽업)", "€20–25 (차량당)"),
         st("h_fira_elgreco", "체크인 · 수영장", 90),
         mv("h_fira_elgreco", "r_luckys", "walk", 10),
         st("r_luckys", "점심: Lucky's Souvlakis — 기로스 피타", 40, "€5–12"),
         mv("r_luckys", "fira", "walk", 3),
         st("fira", "피라 칼데라 산책로", 40, "무료"),
         mv("fira", "firostefani", "walk", 15),
         mv("firostefani", "imerovigli", "walk", 25, note="칼데라 절벽 산책로"),
         mv("imerovigli", "skaros", "walk", 20),
         st("skaros", "스카로스 바위 일몰 — 이아보다 조용한 칼데라 정면 (" + SUNSET_SAN + ")", 60, "무료", at="19:30"),
         mv("skaros", "r_aktaion", "walk", 35, note="피로스테파니로 돌아옴 (밤길은 휴대폰 손전등)"),
         st("r_aktaion", "저녁: Aktaion (1922년) — 파바·토마토케프테데스", 80, "€25–35", "공식 사이트 폼 예약", link="https://www.aktaionsantorini.com"),
         mv("r_aktaion", "h_fira_elgreco", "walk", 15),
     ]},
    {"date": "5/14", "dow": "금", "city": "산토리니", "title": "아크로티리, 그리고 피라→이아 트레킹", "photo": "oia", "sleep": "h_fira_elgreco", "start": "08:30",
     "items": [
         mv("h_fira_elgreco", "akrotiri", "taxi", 25, "", "", "€25–30 (차량당)", "버스는 피라 터미널에서 €2.40"),
         st("akrotiri", "아크로티리 유적 — 화산재에 덮인 미노아 도시 (금 08~18시)", 75, "€20"),
         mv("akrotiri", "red_beach", "walk", 10),
         st("red_beach", "레드 비치 전망대 (해변 접근 폐쇄)", 20, "무료"),
         mv("red_beach", "perissa", "taxi", 20, "", "", "€20–25 (차량당)"),
         st("perissa", "페리사 검은 모래 해변 · 비치 타베르나 점심", 120, "€20–30"),
         mv("perissa", "h_fira_elgreco", "bus", 25, "KTEL 버스", "페리사 → 피라", "€2.40"),
         st("h_fira_elgreco", "호텔 휴식 · 운동화 갈아신기", 60),
         mv("h_fira_elgreco", "fira", "walk", 10),
         st("fira", "피라→이아 칼데라 트레킹 출발 (약 10km, 3~4시간)", 5, "무료", "이메로비글리 이후 물·상점 없음 → 물 1L씩", at="16:00"),
         mv("fira", "imerovigli", "walk", 45, note="피로스테파니 → 이메로비글리 (포장길)"),
         mv("imerovigli", "oia", "walk", 150, note="무인 흙길 구간 → 이아 (운동화 필수)"),
         mv("oia", "oia_castle", "walk", 5),
         st("oia_castle", "이아 성채 일몰 (" + SUNSET_SAN + ")", 45, "무료", "트레킹 1위(트립어드바이저 4.8) 마무리. 성채는 1.5시간 전 만석", at="19:45"),
         mv("oia_castle", "r_pitogyros", "walk", 5),
         st("r_pitogyros", "저녁: PitoGyros — 기로스 피타", 40, "€8–15"),
         mv("r_pitogyros", "h_fira_elgreco", "taxi", 25, "", "일몰 직후 버스는 극심 혼잡 → 택시 예약", "€35 (차량당)", "버스 €2"),
     ]},
    {"date": "5/15", "dow": "토", "city": "산토리니", "title": "화산섬·온천, 와이너리 일몰", "photo": "nea_kameni", "sleep": "h_fira_elgreco", "start": "09:00",
     "items": [
         mv("h_fira_elgreco", "r_svoronos", "walk", 10),
         st("r_svoronos", "아침: Bakery Svoronos", 20, "€3–6"),
         mv("r_svoronos", "fira", "walk", 3),
         mv("fira", "fira_oldport", "funicular", 5, "피라 케이블카", "", "편도 €6"),
         st("fira_oldport", "화산섬·온천 보트 탑승 (10:00경)", 10, "€25–45", at="09:50"),
         mv("fira_oldport", "nea_kameni", "boat", 20, "전통 보트"),
         st("nea_kameni", "네아 카메니 분화구 하이킹 + 유황 온천 (여행사 선택관광 단골)", 210, "€5 (현금)"),
         mv("nea_kameni", "fira_oldport", "boat", 20, fare="투어 포함"),
         mv("fira_oldport", "fira", "funicular", 5, fare="편도 €6"),
         mv("fira", "h_fira_elgreco", "walk", 10),
         st("h_fira_elgreco", "호텔 휴식", 120),
         mv("h_fira_elgreco", "pyrgos", "taxi", 15, "", "", "€15–20 (차량당)"),
         st("pyrgos", "피르고스 마을 골목", 40, "무료"),
         mv("pyrgos", "santo_wines", "taxi", 10, "", "", "€12–15 (차량당)"),
         st("santo_wines", "Santo Wines 테라스 테이스팅 + 칼데라 일몰 (" + SUNSET_SAN + ")", 110, "€18–38", "테라스석 예약", at="19:00", link="https://santowines.gr"),
         mv("santo_wines", "r_metaxi", "taxi", 15, "", "", "€15–20 (차량당)"),
         st("r_metaxi", "저녁: Metaxi Mas — 토마토케프테데스·크라소티가니아", 100, "€25–35", "전화 예약만"),
         mv("r_metaxi", "h_fira_elgreco", "taxi", 15, "", "", "€20 (차량당)"),
     ]},
    {"date": "5/16", "dow": "일", "city": "산토리니", "title": "고대 티라, 카마리 해변, 아무디 일몰", "photo": "catamaran", "sleep": "h_fira_elgreco", "start": "08:30",
     "items": [
         mv("h_fira_elgreco", "ancient_thera", "taxi", 25, "", "메사 부노 산길 (마지막은 걸어서)", "€30 (차량당)"),
         st("ancient_thera", "고대 티라 유적 — 산꼭대기 도시, 양쪽 바다 전망 (수요일 휴무)", 90, "€10"),
         mv("ancient_thera", "kamari", "taxi", 15, "", "", "€15–20 (차량당)"),
         st("kamari", "카마리 해변 산책 · 비치 카페 점심", 120, "€20–30"),
         mv("kamari", "h_fira_elgreco", "bus", 20, "KTEL 버스", "카마리 → 피라", "€2"),
         st("h_fira_elgreco", "호텔 휴식", 120),
         mv("h_fira_elgreco", "ammoudi", "taxi", 30, "", "", "€35 (차량당)"),
         st("r_dimitris", "일몰 디너: Dimitris Ammoudi Taverna — 포구 해산물 (" + SUNSET_SAN + ")", 150, "€40–70", "바다쪽 자리 예약", at="18:50"),
         mv("r_dimitris", "h_fira_elgreco", "taxi", 30, "", "식당에서 호출", "€35 (차량당)"),
     ]},
    {"date": "5/17", "dow": "월", "city": "산토리니 → 아테네", "title": "고고학박물관과 수니온 일몰", "photo": "sounion", "sleep": "h_ath_plaka", "start": "06:50",
     "items": [
         mv("h_fira_elgreco", "jtr_airport", "taxi", 15, "", "전날 예약", "€20–25 (차량당)"),
         st("jtr_airport", "체크인 (Aegean 08:25 출발)", 60, at="07:20"),
         mv("jtr_airport", "ath_airport", "plane", 50, "Aegean 08:25 → 09:15", "산토리니 → 아테네", "€73", "구글 항공 ₩109,289 (2026-11-04)"),
         st("ath_airport", "도착 · 수하물", 20),
         mv("ath_airport", "h_ath_plaka", "taxi", 40, "", "", ATH_TAXI),
         st("h_ath_plaka", "짐 맡기기", 10),
         mv("h_ath_plaka", "nat_arch_museum", "taxi", 15, "", "", "€8–10 (차량당)"),
         st("nat_arch_museum", "국립고고학박물관 — 아가멤논 황금 가면 (월 08~20시)", 100, "€20", link="https://www.namuseum.gr/en/episkepsi"),
         mv("nat_arch_museum", "r_kostas", "taxi", 15, "", "", "€8–10 (차량당)"),
         st("r_kostas", "점심: Kosta's Souvlaki", 30, "€4–8"),
         mv("r_kostas", "h_ath_plaka", "walk", 8),
         st("h_ath_plaka", "체크인 · 휴식", 120),
         mv("h_ath_plaka", "syntagma", "walk", 6),
         mv("syntagma", "sounion", "bus", 100, "수니온 선셋 반일 투어 버스", "신타그마 → 수니온 곶", "투어 €45–65"),
         st("sounion", "포세이돈 신전 일몰 (" + SUNSET_ATH + ")", 100, "€20", at="19:15"),
         mv("sounion", "syntagma", "bus", 100, fare="투어 포함"),
         mv("syntagma", "r_lukumades", "walk", 12),
         st("r_lukumades", "늦은 디저트: Lukumades", 25, "€4–8"),
         mv("r_lukumades", "h_ath_plaka", "walk", 5),
     ]},
    athens_last_day("h_ath_plaka"),
]

# ───────────────────────── 코스 3: 크레타 + 산토리니 ─────────────────────────
C3 = [
    athens_arrival("h_ath_herodion", 15, "lycabettus"),
    athens_acropolis("h_ath_herodion", 5, "thes"),
    {"date": "5/11", "dow": "화", "city": "아테네 → 크레타 하니아", "title": "크레타 하니아, 구항 일몰", "photo": "chania", "sleep": "h_cha_delfino", "start": "08:45",
     "items": [
         st("h_ath_herodion", "조식 · 체크아웃", 40),
         mv("h_ath_herodion", "ath_airport", "taxi", 40, "", "", ATH_TAXI),
         st("ath_airport", "체크인 (Aegean 11:25 출발)", 70, at="10:15"),
         mv("ath_airport", "chq_airport", "plane", 50, "Aegean 11:25 → 12:15", "아테네 → 하니아", "€92", "구글 항공 ₩137,921 (2026-11-04). SKY express 06:45편 ₩73,191"),
         st("chq_airport", "렌터카 픽업 (3일, 이라클리온 항구 반납)", 40, "€180–240 (3일 + 편도 반납료)", "국제운전면허증 필수"),
         mv("chq_airport", "seitan_limania", "taxi", 15, "렌터카", "공항 → 아크로티리 반도", "기름값"),
         st("seitan_limania", "세이탄 리마니아 — 절벽 사이 에메랄드 협만 해변 (급경사 15분)", 80, "무료", "운동화"),
         mv("seitan_limania", "h_cha_delfino", "taxi", 30, "렌터카", "구시가 밖 공영주차장 → 도보", "주차 €5–10/일"),
         st("h_cha_delfino", "체크인 · 휴식", 90),
         mv("h_cha_delfino", "chania_harbour", "walk", 3),
         st("chania_harbour", "베네치아 구항 산책", 40, "무료"),
         mv("chania_harbour", "chania_lighthouse", "walk", 12, note="방파제 따라"),
         st("chania_lighthouse", "하니아 등대 일몰 (트립어드바이저 구항 4.6, 리뷰 6,692)", 50, "무료", at="19:50"),
         mv("chania_lighthouse", "r_tamam", "walk", 15),
         st("r_tamam", "저녁: Tamam — 옛 터키 목욕탕 건물의 크레타 요리 (트립어드바이저 4.3, 리뷰 5,442)", 90, "€20–30", "예약 권장"),
         mv("r_tamam", "h_cha_delfino", "walk", 5),
     ]},
    {"date": "5/12", "dow": "수", "city": "크레타 서부", "title": "엘라포니시 핑크 비치, 산마을 슬로푸드", "photo": "elafonisi", "sleep": "h_cha_delfino", "start": "08:00",
     "items": [
         mv("h_cha_delfino", "r_iordanis", "walk", 8),
         st("r_iordanis", "아침: Bougatsa Iordanis (1924년) — 양젖 치즈 부가차", 25, "€4–6"),
         mv("r_iordanis", "elafonisi", "taxi", 110, "렌터카", "하니아 → 엘라포니시 (산길 75km)", "기름값", "커브 많음, 멀미약"),
         st("elafonisi", "엘라포니시 — 분홍 모래·얕은 라군 (트립어드바이저 4.4, 리뷰 16,838, 크레타 1위)", 210, "주차 €3–5", "5월 바다 18~20°C"),
         mv("elafonisi", "r_dounias", "taxi", 110, "렌터카", "엘라포니시 → 드라코나 산마을", "기름값"),
         st("r_dounias", "이른 저녁: Dounias — 장작불 슬로푸드, 주방 냄비 보고 고르기 (리뷰 1,348)", 100, "€20–30", at="18:00"),
         mv("r_dounias", "h_cha_delfino", "taxi", 30, "렌터카", "드라코나 → 하니아", "기름값"),
         st("chania_harbour", "구항 야경 산책", 30, "무료"),
         mv("chania_harbour", "h_cha_delfino", "walk", 3),
     ]},
    {"date": "5/13", "dow": "목", "city": "하니아 → 이라클리온", "title": "레팀노, 크노소스 궁전, 페스케시 저녁", "photo": "knossos", "sleep": "h_her_lato", "start": "09:00",
     "items": [
         st("h_cha_delfino", "조식 · 체크아웃", 30),
         mv("h_cha_delfino", "rethymno", "taxi", 60, "렌터카", "북부 해안 고속도로", "기름값"),
         st("rethymno", "레팀노 구시가 — 베네치아 항구·포르테차 (트립어드바이저 4.6, 리뷰 8,502)", 90, "무료"),
         st("rethymno", "점심: 레팀노 구항 타베르나", 60, "€15–25"),
         mv("rethymno", "knossos", "taxi", 80, "렌터카", "레팀노 → 이라클리온 남쪽", "기름값"),
         st("knossos", "크노소스 궁전 — 미노아 문명 궁전 (복원이 과하다는 평도)", 90, "€20", "hhticket.gr", link=ACRO),
         mv("knossos", "h_her_lato", "taxi", 20, "렌터카", "", "기름값"),
         st("h_her_lato", "체크인 · 렌터카 반납 위치 확인 (내일 07:30 항구)", 60),
         mv("h_her_lato", "heraklion_lions", "walk", 8),
         st("heraklion_lions", "사자 광장 · 구시가 산책", 40, "무료"),
         mv("heraklion_lions", "r_peskesi", "walk", 5),
         st("r_peskesi", "저녁: Peskesi — 농장 재료 크레타 요리 (리뷰 6,051)", 100, "€25–35", "예약 권장", at="20:00"),
         mv("r_peskesi", "h_her_lato", "walk", 10),
     ]},
    {"date": "5/14", "dow": "금", "city": "크레타 → 산토리니", "title": "고속선으로 산토리니, 스카로스 일몰", "photo": "skaros", "sleep": "h_imero_astra", "start": "07:00",
     "items": [
         mv("h_her_lato", "heraklion_port", "taxi", 5, "렌터카", "", "", "항구에서 렌터카 반납"),
         st("heraklion_port", "렌터카 반납 · SeaJets 체크인 (08:00경 출발)", 40, "", at="07:20"),
         mv("heraklion_port", "athinios", "ferry", 110, "SeaJets 고속선 08:00경 → 10:00경", "이라클리온 → 산토리니 아티니오스", "€68–93", "Ferryhopper에서 시각 확인. 블루스타는 3시간 50분 €31"),
         st("athinios", "하선 · 사전 예약 픽업", 15),
         mv("athinios", "h_imero_astra", "taxi", 30, "", "호텔 픽업", "€40–50 (차량당)"),
         st("h_imero_astra", "체크인 · 칼데라 뷰 테라스 · 휴식", 150),
         mv("h_imero_astra", "fira", "walk", 30, note="칼데라 절벽 산책로"),
         st("r_luckys", "늦은 점심: Lucky's Souvlakis", 40, "€5–12"),
         mv("fira", "h_imero_astra", "walk", 30),
         st("h_imero_astra", "호텔 수영장", 90),
         mv("h_imero_astra", "skaros", "walk", 15),
         st("skaros", "스카로스 바위 일몰 — 호텔 바로 앞 (" + SUNSET_SAN + ")", 60, "무료", at="19:30"),
         mv("skaros", "r_aktaion", "walk", 25),
         st("r_aktaion", "저녁: Aktaion — 파바·토마토케프테데스", 80, "€25–35", "공식 사이트 폼 예약"),
         mv("r_aktaion", "h_imero_astra", "taxi", 8, "", "", "€12 (차량당)"),
     ]},
    {"date": "5/15", "dow": "토", "city": "산토리니", "title": "피르고스, 해산물 점심, 카타마란 선셋 크루즈", "photo": "catamaran", "sleep": "h_imero_astra", "start": "09:30",
     "items": [
         mv("h_imero_astra", "pyrgos", "taxi", 20, "", "", "€20 (차량당)"),
         st("pyrgos", "피르고스 마을 · 카스텔리 정상 (아침이라 한적)", 60, "무료"),
         mv("pyrgos", "r_psaraki", "taxi", 15, "", "", "€20 (차량당)"),
         st("r_psaraki", "점심: To Psaraki — 마리나 뷰 해산물 (구글 4.7, 리뷰 2,630+)", 90, "€35–55", "예약 권장", at="12:30", link="https://topsaraki.gr/"),
         mv("r_psaraki", "vlychada", "walk", 3),
         st("vlychada", "카타마란 선셋 크루즈 5시간 — 레드·화이트 비치, 온천, 선상 BBQ, 바다 위 일몰", 330, "€110–130", "1~2주 전 예약", at="15:00", link="https://sailing-santorini.com/"),
         mv("vlychada", "h_imero_astra", "bus", 45, "크루즈사 픽업 버스", fare="투어 포함"),
     ]},
    {"date": "5/16", "dow": "일", "city": "산토리니", "title": "아크로티리, 이메로비글리→이아 트레킹", "photo": "oia", "sleep": "h_imero_astra", "start": "09:00",
     "items": [
         mv("h_imero_astra", "akrotiri", "taxi", 30, "", "", "€30 (차량당)"),
         st("akrotiri", "아크로티리 유적 (일 08~18시)", 75, "€20"),
         mv("akrotiri", "red_beach", "walk", 10),
         st("red_beach", "레드 비치 전망대", 20, "무료"),
         mv("red_beach", "h_imero_astra", "taxi", 30, "", "", "€30 (차량당)"),
         st("h_imero_astra", "점심 · 휴식 · 운동화", 180),
         mv("h_imero_astra", "imerovigli", "walk", 3),
         st("imerovigli", "이메로비글리→이아 트레킹 출발 (약 7.5km, 2.5~3시간)", 5, "무료", "물 1L씩", at="16:30"),
         mv("imerovigli", "oia", "walk", 150, note="무인 흙길 구간 → 이아"),
         mv("oia", "ammoudi", "walk", 15, note="계단 300개"),
         st("r_dimitris", "일몰 디너: Dimitris Ammoudi Taverna (" + SUNSET_SAN + ")", 150, "€40–70", "바다쪽 자리 예약", at="19:20"),
         mv("r_dimitris", "h_imero_astra", "taxi", 25, "", "식당에서 호출", "€35 (차량당)"),
     ]},
    {"date": "5/17", "dow": "월", "city": "산토리니 → 아테네", "title": "아테네 고고학박물관, 수니온 일몰", "photo": "sounion", "sleep": "h_ath_herodion", "start": "06:50",
     "items": [
         mv("h_imero_astra", "jtr_airport", "taxi", 20, "", "전날 예약", "€25 (차량당)"),
         st("jtr_airport", "체크인 (Aegean 08:25 출발)", 55, at="07:20"),
         mv("jtr_airport", "ath_airport", "plane", 50, "Aegean 08:25 → 09:15", "산토리니 → 아테네", "€73", "구글 항공 ₩109,289 (2026-11-04)"),
         st("ath_airport", "도착 · 수하물", 20),
         mv("ath_airport", "h_ath_herodion", "taxi", 40, "", "", ATH_TAXI),
         st("h_ath_herodion", "짐 맡기기", 10),
         mv("h_ath_herodion", "nat_arch_museum", "taxi", 20, "", "", "€10 (차량당)"),
         st("nat_arch_museum", "국립고고학박물관 (월 08~20시)", 100, "€20", link="https://www.namuseum.gr/en/episkepsi"),
         mv("nat_arch_museum", "r_kostas", "taxi", 15, "", "", "€8–10 (차량당)"),
         st("r_kostas", "점심: Kosta's Souvlaki", 30, "€4–8"),
         mv("r_kostas", "h_ath_herodion", "taxi", 10, "", "", "€6–8 (차량당)"),
         st("h_ath_herodion", "체크인 · 휴식", 120),
         mv("h_ath_herodion", "syntagma", "taxi", 10, "", "", "€6–8 (차량당)"),
         mv("syntagma", "sounion", "bus", 100, "수니온 선셋 반일 투어 버스", "신타그마 → 수니온 곶", "투어 €45–65"),
         st("sounion", "포세이돈 신전 일몰 (" + SUNSET_ATH + ")", 100, "€20", at="19:15"),
         mv("sounion", "syntagma", "bus", 100, fare="투어 포함"),
         mv("syntagma", "r_atlantikos", "taxi", 10, "", "", "€6–8 (차량당)"),
         st("r_atlantikos", "늦은 저녁: Atlantikos", 60, "€15–25"),
         mv("r_atlantikos", "h_ath_herodion", "taxi", 10, "", "", "€6–8 (차량당)"),
     ]},
    athens_last_day("h_ath_herodion"),
]

COURSES = {1: C1, 2: C2, 3: C3}

# ───────────────────────── 코스 선택 페이지 예산 (만 원, 2인) ─────────────────────────
# 항공: 카타르 왕복 1인 126.1만 × 2. 숙소: 위 HOTELS 요금 중간값 × 박수. 현지 교통: 국내선·페리·택시·렌터카.
# 입장권·체험: 아크로폴리스 €30·박물관·투어·크루즈 등. 식비: 1인 하루 €45~55. 기타: 기후회복세(1박 €2~10) + 예비비.
BUDGET = {
    "budgetTotal": 1000,
    "categories": [
        {"label": "국제선 항공", "color": "#5B8DEF"},
        {"label": "숙소 9박", "color": "#E8B04B"},
        {"label": "현지 교통", "color": "#7FD1A8"},
        {"label": "입장권·체험", "color": "#C9A4F2"},
        {"label": "식비", "color": "#F0907A"},
        {"label": "관광세·예비비", "color": "#6F7D97"},
    ],
    "courses": {
        "course1": {"no": "COURSE 1", "accent": "#1E7FA8", "title": "섬 허니문, 미코노스 + 산토리니", "tag": "이아 동굴 스위트 2박 · 델로스 · 카타마란",
                    "total": 1124, "parts": [252.2, 468, 114, 111, 150, 28.8],
                    "photo": "photos/greece/oia.jpg", "alt": "산토리니 이아 마을",
                    "flightShort": "카타르 도하 경유", "stayShort": "이아 동굴 호텔",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 126.1만 원 (2026-11-04 구글 항공) · 국내선 2회 + 고속선 1회",
                    "stay": "Electra Palace (아테네 5성) · Harmony Boutique (미코노스) · Andronis Boutique 이아 2박 · El Greco (피라) 2박",
                    "good": "허니문 전문 여행사 동선 그대로, 이아 동굴 스위트와 섬 두 곳",
                    "watch": "예산을 약 124만 원 넘음 (이아 호텔이 절반). 섬 이동이 많아 짐 정리가 잦음"},
        "course2": {"no": "COURSE 2", "accent": "#2F7A57", "title": "그리스 일주, 델피·메테오라 + 산토리니", "tag": "여행사 일주 동선 · 메테오라 1박 · 산토리니 4박",
                    "total": 877, "parts": [252.2, 210, 80, 170, 135, 29.8],
                    "photo": "photos/greece/meteora.jpg", "alt": "메테오라 수도원",
                    "flightShort": "카타르 도하 경유", "stayShort": "3~4성 가성비",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 126.1만 원 · 국내선 2회",
                    "stay": "Hotel Plaka (아테네 3성) · Doupiani House (메테오라, 투어 포함) · El Greco Resort (피라) 4박",
                    "good": "예산 안(약 877만 원). 하나·모두투어 그리스 일주의 핵심(델피·메테오라·산토리니)을 자유여행으로",
                    "watch": "델피→메테오라→아테네 차량 이동이 하루 8시간 넘음. 산토리니 호텔은 칼데라 뷰 아님"},
        "course3": {"no": "COURSE 3", "accent": "#B8432A", "title": "크레타 + 산토리니, 한국인 덜 가는 섬", "tag": "렌터카 크레타 3일 · 칼데라 뷰 스위트 3박",
                    "total": 1119, "parts": [252.2, 450, 154, 82.5, 150, 30.3],
                    "photo": "photos/greece/elafonisi.jpg", "alt": "크레타 엘라포니시 해변",
                    "flightShort": "카타르 도하 경유", "stayShort": "칼데라 뷰 스위트",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 126.1만 원 · 국내선 2회 + 이라클리온→산토리니 고속선",
                    "stay": "Herodion (아테네 4성) · Casa Delfino (하니아) · Lato (이라클리온) · Astra Suites (이메로비글리) 3박",
                    "good": "한국 신혼 블로그 언급 1위 섬 크레타 + 칼데라 정면 스위트. 해변·자연·음식",
                    "watch": "예산을 약 119만 원 넘음. 렌터카(국제운전면허) 필요, 크레타 산길 운전이 김"},
    },
}

# ───────────────────────── 예약할 것 ─────────────────────────
QATAR = {"what": "카타르항공 왕복: 인천 5/9 01:20 → 도하 → 아테네 12:25 / 아테네 5/18 20:00 → 도하 → 인천 5/19 17:05", "where": "인천 ↔ 아테네",
         "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 126.1만 원 (2026-11-04 구글 항공)", "when": "코스를 고르면 바로. 5월은 2~3월부터 오름",
         "alt": "에미레이트(두바이 경유)는 110.8만 원이지만 아테네 도착이 5/10 밤. 터키항공은 157.1만 원, 5/10 아침 도착",
         "links": [{"name": "네이버 항공", "tag": "한국어", "url": "https://flight.naver.com/flights/international/ICN-ATH-20270509/ATH-ICN-20270518?adult=2&fareType=Y"},
                   {"name": "카타르항공 공식", "tag": "공식", "url": "https://www.qatarairways.com/ko-kr/homepage.html"},
                   {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}
AEGEAN = {"name": "Aegean 공식", "tag": "공식", "url": "https://www.aegeanair.com/"}
SKYX = {"name": "SKY express 공식", "tag": "공식", "url": "https://www.skyexpress.gr/en"}
TRIPF = {"name": "트립닷컴 항공", "tag": "한국어", "url": "https://kr.trip.com/flights/"}
FERRYH = {"name": "Ferryhopper", "tag": "비교", "url": "https://www.ferryhopper.com/"}
SEAJ = {"name": "SeaJets 공식", "tag": "공식", "url": "https://www.seajets.com/"}
KLOOK = lambda kw: {"name": "클룩", "tag": "한국어", "url": "https://www.klook.com/ko/search/?query=" + kw}
MRT = lambda kw: {"name": "마이리얼트립", "tag": "한국어", "url": "https://www.myrealtrip.com/search?q=" + kw}


def flight(what, dates, price, alt, links):
    return {"what": what, "where": "그리스 국내선", "dates": dates, "price": price, "when": "국제선 다음으로 바로. 저가 요금은 3~4개월 전이 가장 쌈. 위탁 수하물은 예매 때 같이",
            "alt": alt, "links": links}


T_ACRO = {"what": "아크로폴리스 08:00 시간 지정 입장권", "where": "아테네", "dates": "5/10 08:00", "price": "€30 (1인)", "when": "1~2달 전. 인기 슬롯(08:00, 17:00 이후)은 며칠 전 매진",
          "alt": "매진이면 클룩·마이리얼트립 가이드 투어(입장권 포함)", "links": [{"name": "hhticket.gr 공식", "tag": "공식", "url": ACRO}, KLOOK("아크로폴리스"), MRT("아크로폴리스")]}
T_AMUS = {"what": "아크로폴리스 박물관 시간 지정 입장권", "where": "아테네", "dates": "5/10 10:15경", "price": "€20 (1인)", "when": "2~3주 전", "alt": "",
          "links": [{"name": "공식 e-티켓", "tag": "공식", "url": "https://etickets.theacropolismuseum.gr"}]}
T_SOUNION = {"what": "수니온 선셋 반일 투어", "where": "아테네 근교", "dates": "5/10 또는 5/17 오후", "price": "€45–65 (1인, 입장료 €20 별도 여부 확인)", "when": "1~2주 전",
             "alt": "택시 왕복(대기 포함) €150~200", "links": [KLOOK("수니온"), MRT("수니온"), {"name": "GetYourGuide", "tag": "비교", "url": "https://www.getyourguide.com/s/?q=sounion%20sunset"}]}
T_NAM = {"what": "국립고고학박물관", "where": "아테네", "dates": "5/17 오후", "price": "€20 (1인)", "when": "1~2주 전 시간 지정", "alt": "",
         "links": [{"name": "공식", "tag": "공식", "url": "https://www.namuseum.gr/en/episkepsi"}]}
T_DELOS = {"what": "델로스 섬 보트 (10:00)", "where": "미코노스", "dates": "5/12 10:00", "price": "왕복 €25 + 섬 입장 €20 (1인)", "when": "1~2주 전 (현장 구매도 가능)",
           "alt": "영어 가이드 반일 투어 €79 (보트·입장·가이드)", "links": [{"name": "Delos Tours 공식", "tag": "공식", "url": "https://www.delostours.gr/en/"}, KLOOK("델로스")]}
T_CAT = {"what": "산토리니 카타마란 선셋 크루즈 (5시간, BBQ·음료)", "where": "산토리니", "dates": None, "price": "€110–130 (1인, 공유)", "when": "1~2주 전",
         "alt": "세미프라이빗 €180~300, 프라이빗 4인 €800~", "links": [{"name": "Sunset Oia 공식", "tag": "공식", "url": "https://sailing-santorini.com/"}, KLOOK("산토리니 선셋 크루즈"), MRT("산토리니 요트")]}
T_SANTO = {"what": "Santo Wines 일몰 테라스 테이스팅", "where": "산토리니 · 피르고스", "dates": None, "price": "€18–38 (1인, 예약 시 €40 선결제)", "when": "수 주 전 (일몰석)",
           "alt": "Venetsanos(메갈로호리) 칼데라 뷰", "links": [{"name": "Santo Wines 공식", "tag": "공식", "url": "https://santowines.gr"}]}
T_AKRO = {"what": "아크로티리 유적", "where": "산토리니", "dates": None, "price": "€20 (1인)", "when": "현장 구매 가능 (월·목은 15:30 마감)", "alt": "",
          "links": [{"name": "hhticket.gr 공식", "tag": "공식", "url": ACRO}]}
T_VOLC = {"what": "화산섬·온천 보트", "where": "산토리니 · 피라 구항", "dates": None, "price": "€25–45 + 화산공원 €5 현금 (1인)", "when": "전날 부두·여행사 (현장 구매)", "alt": "카타마란 크루즈에 온천 포함된 상품으로 대체 가능",
          "links": [KLOOK("산토리니 화산섬")]}
T_DM = {"what": "델피·메테오라 1박 2일 소그룹 투어 (호텔 포함)", "where": "아테네 출발", "dates": "5/11–5/12", "price": "€280–350 (1인, 입장료 별도: 델피 €20 · 수도원 €5×2)",
        "when": "1~2달 전", "alt": "기차로 직접 가면 아테네→칼람바카 약 5.5시간 €28~31 (2026 기준)", "links": [KLOOK("메테오라 델피"), MRT("메테오라"), {"name": "GetYourGuide", "tag": "비교", "url": "https://www.getyourguide.com/s/?q=delphi%20meteora%202%20day"}]}
T_KNOSSOS = {"what": "크노소스 궁전", "where": "크레타 · 이라클리온", "dates": "5/13 오후", "price": "€20 (1인)", "when": "1주 전 또는 현장", "alt": "",
             "links": [{"name": "hhticket.gr 공식", "tag": "공식", "url": ACRO}]}
T_CAR = {"what": "크레타 렌터카 3일 (하니아 공항 픽업 → 이라클리온 항구 반납)", "where": "크레타", "dates": "5/11–5/14", "price": "€180–240 (편도 반납료 포함, 완전자차 추천)",
         "when": "1~2달 전. 수동이 기본이라 오토는 일찍", "alt": "국제운전면허증 필수", "links": [{"name": "트립닷컴 렌터카", "tag": "한국어", "url": "https://kr.trip.com/carhire/"},
                                                                                {"name": "Rentalcars", "tag": "비교", "url": "https://www.rentalcars.com/"}]}


def rest(key, when, alt=""):
    r = RESTAURANTS[key]
    links = [{"name": "공식·예약", "tag": "공식", "url": r["url"]}] if r.get("url") else []
    links.append({"name": "트립어드바이저", "tag": "비교", "url": r["rating"]["url"]})
    return {"what": r["name"], "where": r["city"], "dates": "", "price": r["price"], "when": when, "alt": alt, "links": links}


def with_date(item, dates):
    return dict(item, dates=dates)


SITES = [
    {"name": "아고다", "url": "https://www.agoda.com/ko-kr/", "for": "숙소", "note": "한국어·원화 결제. 유로로 결제하면 수수료가 덜 붙음. 산토리니 동굴 호텔은 공식 사이트가 더 쌀 때가 있으니 비교"},
    {"name": "트립닷컴", "url": "https://kr.trip.com/", "for": "숙소·항공·렌터카", "note": "한국어 고객센터. 그리스 국내선·렌터카도 한국어로"},
    {"name": "부킹닷컴", "url": "https://www.booking.com/index.ko.html", "for": "숙소", "note": "그리스 섬 소형 숙소 재고가 가장 많음"},
    {"name": "네이버 항공", "url": "https://flight.naver.com/", "for": "국제선", "note": "카타르·에미레이트·터키항공 비교. 결제 직전 금액 확인"},
    {"name": "Ferryhopper", "url": "https://www.ferryhopper.com/", "for": "페리", "note": "수수료 없음, 한국 카드 결제 가능. SeaJets·Blue Star 한 화면 비교"},
    {"name": "클룩", "url": "https://www.klook.com/ko/", "for": "투어·입장권", "note": "한국어. 아크로폴리스 가이드·산토리니 크루즈·메테오라 투어"},
    {"name": "마이리얼트립", "url": "https://www.myrealtrip.com/", "for": "한국어 가이드·요트", "note": "산토리니 요트투어·아테네 한국어 가이드 후기 많음"},
    {"name": "hhticket.gr", "url": ACRO, "for": "유적 공식 입장권", "note": "아크로폴리스·아크로티리·크노소스·델로스 등 국영 유적 공식 e-티켓"},
]
TAXI = [
    {"what": "아테네 공항 ↔ 시내 택시", "note": "정액 €40 (05~24시), 밤 €55. 2인·짐 포함, 카드 가능. 지하철 3호선은 1인 €9", "links": []},
    {"what": "택시 앱", "note": "FREE NOW(아테네 택시 호출), Uber(아테네에서는 일반 택시 호출로 연결). 섬은 앱이 거의 안 되니 호텔 픽업이나 사전 예약", "links": [{"name": "FREE NOW", "url": "https://www.free-now.com/"}]},
    {"what": "산토리니 이동", "note": "택시가 아주 부족 (섬 전체 수십 대). 공항·항구 픽업은 호텔에 미리 요청(€40~60). 일몰 직후 이아 버스는 극심 혼잡. KTEL 버스는 피라 터미널 중심, €2~2.40", "links": [{"name": "KTEL 산토리니", "url": "https://ktel-santorini.gr/"}]},
    {"what": "미코노스 이동", "note": "파브리카 터미널에서 해변 버스 €2. 택시는 줄이 길어 저녁엔 미리 호출", "links": []},
    {"what": "크레타 렌터카", "note": "국제운전면허증 + 한국 면허증. 산길이 많아 소형 오토 + 완전자차. 하니아 구시가는 차량 진입 금지 → 공영주차장", "links": []},
    {"what": "데이터", "note": "eSIM(유럽 10일 10GB) 출국 전 설치. 섬 사이 바다 위에서는 끊김", "links": []},
]

BOOKING = {
    "country": {"kicker": "ΕΛΛΆΔΑ · 2027.05.09 – 05.18", "page": "greece.html"},
    "sites": SITES, "taxi": TAXI,
    "courses": {
        1: {"name": "코스 1 · 섬 허니문", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저. 코스가 정해지면 당일", "items": [QATAR]},
            {"cat": "숙소", "hint": "이아 동굴 호텔부터. 무료 취소로 먼저 잡고 갈아타기", "auto": "hotels"},
            {"cat": "국내선·페리", "hint": "섬 사이 이동은 결항 대비 오전 편", "items": [
                flight("SKY express 아테네 → 미코노스 13:10", "5/11 13:10", "€66 (₩98,782, 1인)", "Aegean 07:35편 ₩88,244", [SKYX, AEGEAN, TRIPF]),
                {"what": "SeaJets 미코노스 → 산토리니 10:10", "where": "미코노스 신항 → 아티니오스", "dates": "5/13 10:10", "price": "€60–90 (1인)", "when": "1~2주 전 (금·일 매진 잦음)", "alt": "일반선 3시간+ 약 €42", "links": [FERRYH, SEAJ]},
                flight("Aegean 산토리니 → 아테네 15:05", "5/17 15:05", "€73 (₩109,289, 1인)", "Ryanair 17:10편 ₩85,038", [AEGEAN, TRIPF]),
            ]},
            {"cat": "입장권·투어", "hint": "아크로폴리스 08:00 슬롯과 크루즈가 먼저", "items": [
                T_ACRO, T_AMUS, with_date(T_SOUNION, "5/10 오후"), T_DELOS, with_date(T_CAT, "5/14 15:00"), with_date(T_AKRO, "5/15"), with_date(T_SANTO, "5/15 19:00"), with_date(T_VOLC, "5/16 10:00"), T_NAM]},
            {"cat": "식당", "hint": "전화·이메일 예약이 필요한 곳 위주", "items": [
                rest("metaxi", "10일 전 전화 예약, 전날 재확인"), rest("dimitris", "2~3주 전, 일몰 시간 바다쪽 자리"), rest("selene", "1~2달 전 (미슐랭 1스타)"),
                rest("thes", "2~3주 전 이메일"), rest("karamanlidika", "1~2주 전 공식 사이트"), rest("baboulas", "1주 전"), rest("katerinas", "1주 전 발코니"), rest("aktaion", "1~2주 전 폼"), rest("kikis", "예약 불가 — 12시 전 도착")]},
        ]},
        2: {"name": "코스 2 · 그리스 일주", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [QATAR]},
            {"cat": "델피·메테오라 투어", "hint": "투어가 호텔·교통을 같이 잡아 줌", "items": [T_DM]},
            {"cat": "숙소", "hint": "무료 취소 요금으로 먼저", "auto": "hotels"},
            {"cat": "국내선", "hint": "", "items": [
                flight("Aegean 아테네 → 산토리니 10:05", "5/13 10:05", "€68 (₩101,792, 1인)", "SKY express 10:00편 ₩88,245", [AEGEAN, SKYX, TRIPF]),
                flight("Aegean 산토리니 → 아테네 08:25", "5/17 08:25", "€73 (₩109,289, 1인)", "SKY express 08:30편 ₩125,848", [AEGEAN, TRIPF]),
            ]},
            {"cat": "입장권·투어", "hint": "", "items": [T_ACRO, T_AMUS, with_date(T_AKRO, "5/14"), with_date(T_VOLC, "5/15 10:00"), with_date(T_SANTO, "5/15 19:00"), with_date(T_SOUNION, "5/17 오후"), T_NAM]},
            {"cat": "식당", "hint": "", "items": [
                rest("strofi", "1~2주 전 루프탑 지정"), rest("karamanlidika", "1~2주 전"), rest("metaxi", "10일 전 전화"), rest("dimitris", "2~3주 전 일몰석"), rest("aktaion", "1~2주 전 폼")]},
        ]},
        3: {"name": "코스 3 · 크레타 + 산토리니", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [QATAR]},
            {"cat": "숙소", "hint": "Astra Suites(칼데라 뷰)부터", "auto": "hotels"},
            {"cat": "국내선·페리·렌터카", "hint": "", "items": [
                flight("Aegean 아테네 → 하니아 11:25", "5/11 11:25", "€92 (₩137,921, 1인)", "SKY express 06:45편 ₩73,191", [AEGEAN, SKYX, TRIPF]),
                T_CAR,
                {"what": "SeaJets 이라클리온 → 산토리니 (08:00경)", "where": "이라클리온 → 아티니오스", "dates": "5/14 08:00경", "price": "€68–93 (1인)", "when": "2027 시간표가 열리면 바로 (판매 시작 시점 확인)", "alt": "Blue Star 3시간 50분 약 €31, SKY express 이라클리온→산토리니 항공 €69~", "links": [FERRYH, SEAJ]},
                flight("Aegean 산토리니 → 아테네 08:25", "5/17 08:25", "€73 (₩109,289, 1인)", "", [AEGEAN, TRIPF]),
            ]},
            {"cat": "입장권·투어", "hint": "", "items": [T_ACRO, T_AMUS, T_KNOSSOS, with_date(T_CAT, "5/15 15:00"), with_date(T_AKRO, "5/16"), with_date(T_SOUNION, "5/17 오후"), T_NAM]},
            {"cat": "식당", "hint": "", "items": [
                rest("thes", "2~3주 전 이메일"), rest("karamanlidika", "1~2주 전"), rest("tamam", "1주 전"), rest("peskesi", "1~2주 전"), rest("psaraki", "1주 전"), rest("dimitris", "2~3주 전 일몰석"), rest("aktaion", "1~2주 전")]},
        ]},
    },
}
for c in BOOKING["courses"].values():
    for g in c["groups"]:
        for it in g.get("items", []):
            it["dates"] = it.get("dates") or "코스 일정 참고"
