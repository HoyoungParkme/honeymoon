"""포르투갈 신혼여행 2027.05.09–05.18 (2인) 세 코스. build_country.py portugal 이 읽는다.

근거 (2026-11-06 조사)
- 여행사: 하나투어 자유허니문 '리스본2+알부페이라2+포르투3'·'리스본+포르투', 하나투어·노랑풍선·모두투어·참좋은여행 '포르투갈 일주 9일'
  (신트라 페나성·오비두스·나자레·코임브라·아베이루·포르투·라고스, 전용버스로 1박씩 이동)
- 명소·요금: 제로니무스 €18·벨렝탑 €15 (둘 다 월요일 휴관 — 5/10·5/17이 월요일), 상 조르즈 €17, 페나 궁전 €20 + 셔틀 €4.5,
  헤갈레이라 €20(30분 단위), 무어인의 성 €12, 렐루 서점 €15.95, 테일러스 €25, 도우루 열차 €12.45·하벨루 보트 €12.50
- 교통: CP 알파 펜둘라르 리스본↔포르투 €35.70 (2시간 50분), 호시우→신트라 €2.30, 리스본 공항 택시 약 €16
- 항공: 구글 항공 2026-11-06 조회 (카타르 왕복 1인 ₩1,433,300, 귀국편이 5/18 08:25라 마지막 밤은 리스본)
- 주의: 글로리아 푸니쿨라 2025-09부터 운행 중단, 베나길 동굴은 2025년부터 상륙 금지(배에서만)
- 식당: pt_restaurants.py (트립어드바이저·구글 평점, 미슐랭 빕 구르망)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))  # tools/ (tripkit)
sys.path.insert(0, HERE)
from pt_places import PLACES  # noqa: E402,F401
from pt_restaurants import RESTAURANTS  # noqa: E402,F401
from tripkit import mv, st  # noqa: E402

COURSE_META = {
    1: ("코스 1 · 리스본 + 포르투·도우루 (허니문 정석)", "#1E7FA8"),
    2: ("코스 2 · 포르투갈 일주 (오비두스·나자레·코임브라, 렌터카)", "#2F7A57"),
    3: ("코스 3 · 리스본 + 알가르브 라고스 (절벽 해안)", "#B8432A"),
}

# 이름, 요금 보기 링크, 1박 2인 1실 요금 (2027년 5월 요금 미오픈 → 2026년 시세 기준 추정)
HOTELS = {
    "h_lis_avani": ("Avani Avenida Liberdade (리스본)", "https://www.kayak.co.kr/hotels/Avani-Avenida-Liberdade-Lisbon", "€200–280 (추정)"),
    "h_lis_mundial": ("Hotel Mundial (리스본 4성, 루프탑)", "https://www.kayak.co.kr/hotels/Hotel-Mundial-Lisbon", "€150–220 (추정)"),
    "h_opo_descobertas": ("Descobertas Boutique Hotel (포르투)", "https://www.kayak.co.kr/hotels/Descobertas-Boutique-Hotel-Porto", "€140–190 (추정)"),
    "h_opo_acta": ("Hotel Acta The Avenue (포르투 4성)", "https://www.kayak.co.kr/hotels/Hotel-Acta-The-Avenue-Porto", "€120–170 (추정)"),
    "h_naz_marbravo": ("Hotel Mar Bravo (나자레)", "https://www.kayak.co.kr/hotels/Hotel-Mar-Bravo-Nazare", "€110–160 (추정)"),
    "h_lagos_casamae": ("Casa Mãe (라고스 부티크)", "https://www.kayak.co.kr/hotels/Casa-Mae-Lagos", "€200–280 (추정)"),
}

HOTEL_META = {
    "h_lis_avani": {"city": "리스본 · 리베르다드 거리", "search": "Avani Avenida Liberdade Lisbon", "official": "",
                    "alt": "하나투어 일주 상품의 '리스본 시내 1박' 선택지. 더 싸게는 Hotel Mundial(4성, 루프탑) €150~220"},
    "h_lis_mundial": {"city": "리스본 · 마르팅 모니즈 (28번 트램 출발점)", "search": "Hotel Mundial Lisbon", "official": "",
                      "alt": "하나투어 허니문·모두투어 세미팩의 리스본 호텔. 루프탑 바에서 상 조르즈 성 정면"},
    "h_opo_descobertas": {"city": "포르투 · 히베이라 근처", "search": "Descobertas Boutique Hotel Porto", "official": "",
                          "alt": "하나투어 자유허니문의 포르투 호텔. 강변까지 걸어서. 더 싸게는 Hotel Acta The Avenue"},
    "h_opo_acta": {"city": "포르투 · 알리아도스 거리", "search": "Hotel Acta The Avenue Porto", "official": "",
                   "alt": "하나투어 자유허니문 포르투 호텔 중 하나. 상 벤투역 도보 5분, 렌터카 반납 후 걸어서"},
    "h_naz_marbravo": {"city": "나자레 · 해변 광장", "search": "Hotel Mar Bravo Nazare", "official": "",
                       "alt": "해변 바로 앞. 주차는 호텔에 문의 (여름엔 해변 주차가 어려움)"},
    "h_lagos_casamae": {"city": "라고스 구시가 성벽 안", "search": "Casa Mae Lagos", "official": "",
                        "when": "알가르브 부티크는 5월부터 성수기 요금. 무료 취소로 지금",
                        "alt": "정원·수영장 있는 부티크. 더 싸게는 구시가 게스트하우스 €100~150, 리조트를 원하면 알부페이라(하나투어 허니문)"},
}

BREAKFAST = {
    "h_lis_avani": "호텔 조식", "h_lis_mundial": "호텔 조식 (루프탑 층 뷔페)", "h_opo_descobertas": "호텔 조식",
    "h_opo_acta": "호텔 뷔페 조식", "h_naz_marbravo": "호텔 조식 (해변 뷰)", "h_lagos_casamae": "정원 조식 (로컬 재료)",
}
CAFES = {
    "h_lis_avani": "Manteigaria (시아두, 도보 15분) — 나타 + 비카(에스프레소) €3",
    "h_lis_mundial": "Manteigaria (시아두, 도보 12분) — 나타 + 비카 €3",
    "h_opo_descobertas": "히베이라 카페 — 나타 + 갈랑(라테) €3–5",
    "h_opo_acta": "볼량 시장 카페 — €3–5",
    "h_naz_marbravo": "해변 카페 — 나타 + 커피 €3",
    "h_lagos_casamae": "구시가 카페 — €4–6",
}

ARRIVAL = {"wake": "기내", "sleepAt": "5/9 01:20 인천 출발 (카타르항공, 도하 경유), 비행기 안에서 아침",
           "bfA": "기내식", "bfB": "도하 공항 환승 중 카페 (€5–10)", "startNote": "리스본 공항 도착 시각부터 시작"}

PHOTOS = {
    "lisbon_tram": ("리스본 28번 트램", ["Lisbon tram 28 Alfama", "Eléctrico 28 Lisboa"]),
    "alfama": ("알파마 지붕과 테주강", ["Alfama rooftops Lisbon", "Miradouro de Santa Luzia"]),
    "pena": ("신트라 페나 궁전", ["Pena Palace Sintra", "Palácio da Pena"]),
    "belem": ("벨렝탑", ["Belém Tower Lisbon", "Torre de Belém"]),
    "porto_ribeira": ("포르투 히베이라와 동 루이스 다리", ["Porto Ribeira Dom Luís bridge", "Ribeira Porto"]),
    "lello": ("렐루 서점 계단", ["Livraria Lello staircase", "Livraria Lello"]),
    "douro": ("도우루 밸리 포도밭", ["Douro Valley vineyards Pinhão", "Douro valley terraces"]),
    "obidos": ("오비두스 성곽 마을", ["Óbidos walls Portugal", "Óbidos village"]),
    "coimbra": ("코임브라 대학교", ["University of Coimbra tower", "Coimbra university"]),
    "lagos": ("라고스 폰타 다 피에다드", ["Ponta da Piedade Lagos", "Ponta da Piedade"]),
    "benagil": ("베나길 동굴", ["Benagil cave", "Algar de Benagil"]),
    "lisbon_view": ("상 페드루 드 알칸타라 전망대에서 본 리스본", ["Miradouro de São Pedro de Alcântara", "Lisbon view castle"]),
    "cabo_roca": ("호카곶", ["Cabo da Roca", "Cabo da Roca lighthouse"]),
}

# ── 자주 쓰는 문구 ──
LIS_TAXI = "€15–20 (차량당)"
LIS_TAXI_NOTE = "Uber·Bolt. 메트로 빨간선은 1인 €1.90 + 카드 €0.50"
SUNSET_LIS = "5월 중순 리스본 일몰 약 20:40"
SUNSET_OPO = "5월 중순 포르투 일몰 약 20:50"
SUNSET_LAG = "5월 중순 라고스 일몰 약 20:35"


def lisbon_arrival(hotel, walk_rossio):
    """1일차: 13:30 도착 → 체크인·낮잠 → 호시우·시아두·나타 → 하미루 → 세뇨라 두 몬트 일몰."""
    return {"date": "5/9", "dow": "일", "city": "리스본", "title": "도하 경유 도착, 첫 저녁은 하미루", "photo": "lisbon_tram", "sleep": hotel, "start": "13:30", "items": [
        st("lis_airport", "카타르항공 도착 (13:30). 입국심사 — EES 얼굴·지문 등록 → 수하물", 60),
        mv("lis_airport", hotel, "taxi", 25, "", "도착층 Uber·Bolt 픽업 존", LIS_TAXI, LIS_TAXI_NOTE),
        st(hotel, "체크인 · 샤워 · 낮잠 (도하 경유 약 18시간 비행 후)", 120),
        mv(hotel, "rossio", "walk", walk_rossio),
        st("rossio", "호시우 광장 — 물결무늬 칼사다 포석", 15, "무료"),
        mv("rossio", "santa_justa", "walk", 3),
        st("santa_justa", "산타 주스타 엘리베이터 (아래에서 구경, 줄이 길어 타지 않음)", 10, "무료"),
        mv("santa_justa", "chiado", "walk", 8, note="카르무 수녀원 쪽 계단으로 올라감"),
        st("chiado", "시아두 산책 · 카페 브라질레이라 앞 페소아 동상", 30, "무료"),
        mv("chiado", "r_manteigaria", "walk", 2),
        st("r_manteigaria", "간식: Manteigaria — 갓 구운 나타 (종이 울리면 새 판)", 20, "€1.50 (1개)"),
        mv("r_manteigaria", "r_ramiro", "taxi", 12, "", "Uber·Bolt", "€7–9 (차량당)"),
        st("r_ramiro", "첫 저녁: Cervejaria Ramiro — 타이거새우·조개찜, 마지막엔 프레구 샌드위치", 90, "€30–45",
           "웹 예약 (19:30 이후 예약 불가, 월요일 휴무)", at="18:45", link="https://www.cervejariaramiro.com/"),
        mv("r_ramiro", "senhora_monte", "taxi", 10, "", "", "€6–8 (차량당)"),
        st("senhora_monte", "세뇨라 두 몬트 전망대 — 리스본에서 가장 높은 전망대, 노을과 야경 (" + SUNSET_LIS + ")", 40, "무료"),
        mv("senhora_monte", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
    ]}


def alfama_fado(hotel, walk_mm, date="5/10", dow="월"):
    """28번 트램 → 그라사 → 상 조르즈 성 → 산타 루치아 → 알파마 → 해물밥 → 코메르시우 → 파두 디너."""
    return {"date": date, "dow": dow, "city": "리스본", "title": "28번 트램, 알파마 골목과 파두의 밤", "photo": "alfama",
            "note": "월요일은 제로니무스 수도원·벨렝탑 휴관 → 벨렝은 수요일에", "sleep": hotel, "start": "08:15", "items": [
        mv(hotel, "martim_moniz", "walk", walk_mm),
        st("martim_moniz", "28번 트램 출발점 — 이른 시간에 타야 앉아감", 15, "", "차내 1회권 또는 나베간트 카드"),
        mv("martim_moniz", "graca", "tram", 15, "28번 트램", "마르팅 모니즈 → 그라사", "€3 내외 (차내, 추정)"),
        st("graca", "그라사 전망대 — 성과 테주강", 20, "무료"),
        mv("graca", "sao_jorge", "walk", 12),
        st("sao_jorge", "상 조르즈 성 — 리스본 전체가 내려다보이는 무어인 성채", 90, "€17", "09:00 개장, 온라인 예매로 줄 건너뛰기", at="09:30"),
        mv("sao_jorge", "santa_luzia", "walk", 10),
        st("santa_luzia", "산타 루치아 · 포르타스 두 솔 전망대 — 알파마 지붕과 테주강, 아줄레주 벽", 25, "무료"),
        mv("santa_luzia", "alfama", "walk", 5),
        st("alfama", "알파마 골목 미로 산책 (빨래 걸린 계단길)", 50, "무료"),
        mv("alfama", "se_lisboa", "walk", 8),
        st("se_lisboa", "리스본 대성당 (12세기 로마네스크)", 20, ""),
        mv("se_lisboa", "r_uma", "walk", 10),
        st("r_uma", "점심: Uma Marisqueira — 한국인이 줄 서는 해물밥(아호스 드 마리스쿠) 2인분", 80, "€15–20", "예약 없음, 조리 20~40분"),
        mv("r_uma", "comercio", "walk", 8),
        st("comercio", "코메르시우 광장 · 아우구스타 개선문 — 테주강 앞 노란 광장", 30, "무료"),
        mv("comercio", hotel, "walk", 12),
        st(hotel, "호텔 휴식 (시에스타)", 150),
        mv(hotel, "clube_fado", "taxi", 10, "", "Uber·Bolt", "€6–8 (차량당)"),
        st("clube_fado", "파두 디너 — Clube de Fado (알파마). 기타 소리와 '사우다드'", 150, "€78 (1인, 식사+공연)", "1~2주 전 예약. 더 싸게는 O Faia 커버 €20",
           at="20:00", link="https://www.clube-de-fado.com/"),
        mv("clube_fado", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
    ]}


def sintra_cascais(hotel, walk_rossio, date="5/11", dow="화"):
    """신트라: 피리키타 → 페나 09:30 → 무어인의 성 → 점심 → 헤갈레이라 → 호카곶 → 카스카이스 일몰 디너."""
    return {"date": date, "dow": dow, "city": "신트라 · 카스카이스 (당일)", "title": "페나 궁전, 땅끝 호카곶, 카스카이스 일몰", "photo": "pena", "sleep": hotel, "start": "07:30", "items": [
        mv(hotel, "rossio_station", "walk", walk_rossio),
        mv("rossio_station", "sintra_station", "train", 40, "CP 신트라선 (20분 간격)", "호시우역 → 신트라역", "€2.30 (1인)", "나베간트 카드 충전"),
        mv("sintra_station", "r_piriquita", "walk", 12),
        st("r_piriquita", "아침: Casa Piriquita — 트라베세이루·케이자다 (11시 넘으면 줄)", 20, "€5", "08:30 오픈"),
        mv("r_piriquita", "pena", "bus", 20, "페나 셔틀 / 434번 순환버스", "신트라 시내 → 페나 궁전", "셔틀 €4.5 (1인)", "434 버스 1일권 €13.55"),
        st("pena", "페나 궁전 — 언덕 위 노랑·빨강 궁전 (시간 지정 입장) + 공원", 120, "€20", "parquesdesintra.pt 09:30 슬롯 예매", at="09:30",
           link="https://www.parquesdesintra.pt/en/"),
        mv("pena", "mouros", "walk", 15),
        st("mouros", "무어인의 성 — 성벽 위로 대서양과 페나 궁전", 60, "€12"),
        mv("mouros", "r_tascantiga", "walk", 25, note="숲길 내리막으로 구시가"),
        st("r_tascantiga", "점심: Tascantiga — 대구튀김·돼지 볼살 등 작은 접시", 70, "€15–25", "점심 예약 불가"),
        mv("r_tascantiga", "regaleira", "walk", 10),
        st("regaleira", "헤갈레이라 별장 — 이니시에이션 우물 나선 계단, 지하 동굴", 90, "€20", "30분 단위 시간 지정", at="14:30"),
        mv("regaleira", "cabo_roca", "bus", 40, "Scotturb 403번", "신트라 → 호카곶", "차내 구매 (요금 확인)"),
        st("cabo_roca", "호카곶 — '땅이 끝나고 바다가 시작되는 곳', 유라시아 서쪽 끝 절벽", 40, "무료"),
        mv("cabo_roca", "cascais", "bus", 30, "Scotturb 403번", "호카곶 → 카스카이스"),
        st("cascais", "카스카이스 구시가 · 해변 산책", 60, "무료"),
        mv("cascais", "r_mardoinferno", "walk", 20, note="해안 산책로"),
        st("r_mardoinferno", "저녁: Mar do Inferno — 절벽 앞 해산물, 일몰 테라스 (" + SUNSET_LIS + ")", 120, "€40–70", "테라스 예약, 수요일 휴무, 출발 전 영업 확인", at="19:30"),
        mv("r_mardoinferno", "cascais_station", "taxi", 8, "", "", "€8–10 (차량당)"),
        mv("cascais_station", "cais_sodre", "train", 40, "CP 카스카이스선", "카스카이스 → 카이스 두 소드레", "€2.30 (1인)"),
        mv("cais_sodre", hotel, "taxi", 10, "", "Uber·Bolt", "€7–9 (차량당)"),
    ]}


def belem_items(hotel):
    """벨렝 오전(수요일): 원조 나타 → 제로니무스 09:30 → 발견기념비 → 벨렝탑."""
    return [
        mv(hotel, "r_pasteisbelem", "taxi", 20, "", "Uber·Bolt (15E 트램도 가능)", "€12–15 (차량당)"),
        st("r_pasteisbelem", "아침: Pastéis de Belém — 1837년 원조 에그타르트 (안쪽 홀로)", 30, "€1.50 (1개)", "08:00 오픈"),
        mv("r_pasteisbelem", "jeronimos", "walk", 3),
        st("jeronimos", "제로니무스 수도원 — 마누엘 양식 회랑, 바스쿠 다 가마 무덤", 75, "€18", "온라인 시간 지정 (월요일 휴관)", at="09:30"),
        mv("jeronimos", "padrao", "walk", 8),
        st("padrao", "발견기념비 · 바닥의 세계지도", 15, "무료"),
        mv("padrao", "belem_tower", "walk", 12),
        st("belem_tower", "벨렝탑 — 테주강 위 16세기 요새", 45, "€15", "시간 지정 (월요일 휴관)"),
    ]


def porto_day(hotel, date, dow):
    """포르투: 렐루 09:00 → 알마스·볼량 → 카자 게드스 → 대성당 → 히베이라 → 다리 위층 → 테일러스 → 모루 정원 일몰 → 타파벤투."""
    return {"date": date, "dow": dow, "city": "포르투", "title": "렐루 서점, 히베이라, 가이아 일몰", "photo": "porto_ribeira", "sleep": hotel, "start": "08:30", "items": [
        mv(hotel, "lello", "walk", 10),
        st("lello", "렐루 서점 — 붉은 나선 계단 (시간 지정 입장)", 40, "€15.95", "첫 타임 예매, 책을 사면 입장료 차감", at="09:00", link="https://www.livrarialello.pt/en/"),
        mv("lello", "clerigos", "walk", 3),
        st("clerigos", "클레리구스 탑 (외관) · 대학가", 15, "무료"),
        mv("clerigos", "sao_bento", "walk", 7),
        st("sao_bento", "상 벤투역 — 아줄레주 2만 장의 역사 그림", 20, "무료"),
        mv("sao_bento", "almas", "walk", 8),
        st("almas", "알마스 성당 — 파란 타일로 덮인 외벽", 15, "무료"),
        mv("almas", "bolhao", "walk", 3),
        st("bolhao", "볼량 시장 — 2022년 새 단장한 전통 시장", 40, "무료"),
        mv("bolhao", "r_guedes", "walk", 8),
        st("r_guedes", "점심: Casa Guedes — 천천히 구운 돼지 뒷다리살 샌드위치 + 세하 치즈", 45, "€5–10"),
        mv("r_guedes", "se_porto", "walk", 10),
        st("se_porto", "포르투 대성당 앞 광장 — 지붕들 너머 강", 20, "무료"),
        mv("se_porto", "ribeira", "walk", 10, note="골목 계단 내리막"),
        st("ribeira", "히베이라 강변 — 알록달록한 집들, 하벨루 배", 40, "무료"),
        mv("ribeira", "gaia", "walk", 10, note="동 루이스 다리 아래층"),
        mv("gaia", "taylors", "walk", 12, note="가파른 오르막"),
        st("taylors", "테일러스 포트와인 셀러 — 오디오 투어 + 시음 3잔", 75, "€25", "온라인 예약", at="15:30"),
        mv("taylors", "gaia", "walk", 10),
        st("gaia", "가이아 강변 카페 휴식", 60, "€5–10"),
        mv("gaia", "jardim_morro", "walk", 15, note="케이블카(편도 €7, 추정) 또는 언덕길"),
        st("jardim_morro", "모루 정원 · 세하 두 필라르 — 포르투 일몰 명당 (" + SUNSET_OPO + ")", 60, "무료", at="20:00"),
        mv("jardim_morro", "dom_luis", "walk", 3),
        st("dom_luis", "동 루이스 1세 다리 위층 건너기 — 야경", 15, "무료"),
        mv("dom_luis", "r_tapabento", "walk", 8),
        st("r_tapabento", "저녁: Tapabento — 문어 샐러드·오리밥 (트립어드바이저 4.7)", 90, "€35–50", "구글 지도로 예약"),
        mv("r_tapabento", hotel, "walk", 10),
    ]}


def douro_day(hotel, walk_sb, date, dow):
    """도우루: 상 벤투 → 피냥 열차(강변 노선) → 하벨루 보트 → 퀸타 시음 → 복귀 → 카페 산티아구."""
    return {"date": date, "dow": dow, "city": "도우루 밸리 (당일)", "title": "강 따라 달리는 열차로 도우루 와인 마을", "photo": "douro", "sleep": hotel, "start": "08:30",
            "note": "여행사 단체 상품엔 없는 도우루. 열차가 싫으면 와이너리 점심 포함 투어($60~120)", "items": [
        mv(hotel, "sao_bento", "walk", walk_sb),
        st("sao_bento", "도우루선 열차 탑승 (09:10경) — 오른쪽 창가가 강 쪽", 10, "", at="09:00"),
        mv("sao_bento", "pinhao", "train", 140, "CP 도우루선 지역열차", "상 벤투 → 피냥", "€12.45 (1인)", "레구아 이후 강 옆을 달림"),
        st("pinhao", "피냥역 아줄레주 · 강변 마을", 20, "무료"),
        mv("pinhao", "pinhao_pier", "walk", 5),
        st("pinhao_pier", "하벨루 보트 1시간 — 계단식 포도밭 사이 강 위", 60, "€12.50", "선착장 현장"),
        st("pinhao", "점심: 피냥 강변 식당 (생선구이·도우루 와인)", 75, "€20–30"),
        st("pinhao", "걸어서 가는 퀸타 와인 시음 (마을 안 와이너리, 현장)", 90, "€15–25"),
        mv("pinhao", "sao_bento", "train", 140, "CP 도우루선", "피냥 → 상 벤투", "€12.45 (1인)"),
        mv("sao_bento", hotel, "walk", walk_sb),
        st(hotel, "호텔 휴식", 40),
        mv(hotel, "r_santiago", "walk", 12),
        st("r_santiago", "저녁: Café Santiago — 원조급 프란세지냐 (하나를 둘이)", 70, "€11–15", "일요일 휴무, 예약 없음"),
        mv("r_santiago", hotel, "walk", 12),
    ]}


def lisbon_free(hotel, date, dow):
    """리스본 자유일(일요일): LX 팩토리 → 타임아웃 마켓 → 휴식 → 바이후 알투 → 상 페드루 일몰 → 벨류 에우리쿠."""
    return {"date": date, "dow": dow, "city": "리스본", "title": "LX 팩토리와 타임아웃 마켓, 전망대 일몰", "photo": "lisbon_view", "sleep": hotel, "start": "10:00", "items": [
        mv(hotel, "lx_factory", "taxi", 20, "", "Uber·Bolt", "€10–12 (차량당)"),
        st("lx_factory", "LX 팩토리 — 옛 공장 단지의 서점·편집숍 (일요일 마켓)", 90, "무료"),
        mv("lx_factory", "time_out_market", "taxi", 12, "", "", "€8–10 (차량당)"),
        st("time_out_market", "점심: 타임아웃 마켓 — 각자 한 가게씩 골라 나눠 먹기", 75, "€15–30", "13시 피크 피하기"),
        mv("time_out_market", "cais_sodre", "walk", 3),
        st("cais_sodre", "핑크 스트리트 · 테주강 리베이라 다스 나우스 산책", 40, "무료"),
        mv("cais_sodre", hotel, "taxi", 10, "", "", "€7–9 (차량당)"),
        st(hotel, "호텔 휴식", 120),
        mv(hotel, "bairro_alto", "taxi", 10, "", "", "€6–8 (차량당)"),
        st("bairro_alto", "바이후 알투 골목 · 기념품 (정어리 통조림, 아줄레주 타일, 코르크)", 50, "€20–40"),
        mv("bairro_alto", "sao_pedro", "walk", 5),
        st("sao_pedro", "상 페드루 드 알칸타라 전망대 — 상 조르즈 성 정면 일몰 (" + SUNSET_LIS + ")", 45, "무료", "글로리아 푸니쿨라는 2025-09부터 운행 중단", at="20:00"),
        mv("sao_pedro", "r_eurico", "taxi", 12, "", "", "€7–9 (차량당)"),
        st("r_eurico", "저녁: O Velho Eurico — 전통 타스카, 직원 추천 요리 나눠 먹기", 100, "€20–30", "몇 달 전 전화 예약 (당일 대기 리스트)", at="21:00"),
        mv("r_eurico", hotel, "walk", 8),
    ]}


def lisbon_last(hotel):
    """9일차(월): 오세아나리우 → 시아두 쇼핑 → 휴식·짐 → 프라드 두스 마르스 마지막 만찬."""
    return {"date": "5/17", "dow": "월", "city": "리스본", "title": "오세아나리우, 쇼핑, 문어구이 마지막 만찬", "photo": "belem",
            "note": "월요일이라 벨렝 수도원·탑은 휴관. 내일 08:25 비행기 → 오늘 밤 짐 정리", "sleep": hotel, "start": "09:30", "items": [
        mv(hotel, "oceanario", "metro", 30, "메트로 빨간선 → 오리엔트", "", "€1.90 (1인)"),
        st("oceanario", "리스본 오세아나리우 — 유럽 최대급 수족관 (개복치·해달)", 120, "", "온라인 예매 (요금 확인)"),
        st("oriente", "점심: 오리엔트 쇼핑센터 · 강변", 60, "€15–20"),
        mv("oriente", "chiado", "metro", 25, "메트로", "", "€1.90 (1인)"),
        st("chiado", "시아두 쇼핑 · 마지막 나타", 90, "€20–50"),
        mv("chiado", hotel, "taxi", 10, "", "", "€6–8 (차량당)"),
        st(hotel, "짐 정리 · 휴식 (내일 05:30 출발)", 120),
        mv(hotel, "r_frade", "taxi", 15, "", "Uber·Bolt", "€8–10 (차량당)"),
        st("r_frade", "마지막 만찬: Frade dos Mares — 문어구이·생선수프 (트립어드바이저 4.8)", 100, "€30–45", "예약 필수", at="19:30"),
        mv("r_frade", hotel, "taxi", 15, "", "", "€8–10 (차량당)"),
    ]}


def lisbon_depart(hotel):
    return {"date": "5/18", "dow": "화", "city": "리스본 → 인천", "title": "새벽 공항, 도하 경유 귀국", "photo": "lisbon_tram", "sleep": None, "start": "05:30",
            "note": "카타르항공 08:25 출발 → 도하 → 인천 5/19 17:05", "items": [
        st(hotel, "체크아웃 (조식 대신 호텔 테이크아웃 박스 요청)", 15),
        mv(hotel, "lis_airport", "taxi", 20, "", "전날 Uber 예약 또는 호텔 택시", LIS_TAXI),
        st("lis_airport", "체크인 · 택스리펀 · 출국 (카타르항공 08:25)", 120, "", "택스리펀은 출국 심사 전 키오스크", at="06:10"),
    ]}


def porto_to_lisbon(porto_hotel, lis_hotel, date, dow, dinner):
    """포르투 오전 마토지뉴스 생선구이 → 알파 펜둘라르 → 리스본 저녁."""
    items = [
        st(porto_hotel, "체크아웃 · 짐 맡기기", 15),
        mv(porto_hotel, "foz", "bus", 30, "STCP 500번 버스 (강변 → 바다)", "", "€2 내외 (추정)"),
        st("foz", "포스 두 도우루 — 도우루강이 대서양을 만나는 등대 산책", 60, "무료"),
        mv("foz", "r_saltamuro", "taxi", 15, "", "", "€8–10 (차량당)"),
        st("r_saltamuro", "점심: Salta o Muro — 마토지뉴스 숯불 생선구이", 90, "€30–40", at="12:30"),
        mv("r_saltamuro", porto_hotel, "metro", 30, "메트로 A선 Matosinhos → 시내", "", "€2 내외"),
        st(porto_hotel, "짐 찾기", 10),
        mv(porto_hotel, "campanha", "taxi", 12, "", "", "€8–10 (차량당)"),
        st("campanha", "알파 펜둘라르 탑승", 10, "", at="15:45"),
        mv("campanha", "santa_apolonia", "train", 170, "CP 알파 펜둘라르", "포르투 캄파냥 → 리스본 산타 아폴로니아", "€35.70 (1인)", "인터시다드 €28.05. cp.pt 조기 할인"),
        mv("santa_apolonia", lis_hotel, "taxi", 10, "", "", "€7–9 (차량당)"),
        st(lis_hotel, "체크인", 30),
    ]
    if dinner == "salgrosso":
        items += [mv(lis_hotel, "r_salgrosso", "taxi", 10, "", "", "€6–8 (차량당)"),
                  st("r_salgrosso", "저녁: Taberna Sal Grosso — 알파마 작은 타스카, 바칼라우 아 브라스", 90, "€20–30", "영업일·예약 방식 전화로 확인", at="20:00"),
                  mv("r_salgrosso", lis_hotel, "taxi", 10, "", "", "€6–8 (차량당)")]
    else:
        items += [mv(lis_hotel, "r_ramiro", "taxi", 10, "", "", "€6–8 (차량당)"),
                  st("r_ramiro", "저녁: Cervejaria Ramiro — 해산물 한 번 더 (일요일 영업)", 90, "€30–45", "19:30 이후는 번호표 대기", at="19:30"),
                  mv("r_ramiro", lis_hotel, "taxi", 10, "", "", "€6–8 (차량당)")]
    return {"date": date, "dow": dow, "city": "포르투 → 리스본", "title": "대서양 하구와 생선구이, 기차로 리스본", "photo": "porto_ribeira", "sleep": lis_hotel, "start": "09:00", "items": items}


# ───────────────────────── 코스 1: 리스본 + 포르투·도우루 ─────────────────────────
L1, P1 = "h_lis_avani", "h_opo_descobertas"
C1 = [
    lisbon_arrival(L1, 10),
    alfama_fado(L1, 15),
    sintra_cascais(L1, 15),
    {"date": "5/12", "dow": "수", "city": "리스본 → 포르투", "title": "벨렝 원조 나타, 알파 펜둘라르로 포르투", "photo": "belem", "sleep": P1, "start": "08:15", "items":
        belem_items(L1) + [
            mv("belem_tower", "r_canalha", "taxi", 8, "", "", "€6–8 (차량당)"),
            st("r_canalha", "점심: Canalha — 미슐랭 빕 구르망, 제철 해산물", 90, "€40–60", "예약 필수", at="12:30"),
            mv("r_canalha", L1, "taxi", 20, "", "", "€12–15 (차량당)"),
            st(L1, "짐 찾기", 10),
            mv(L1, "santa_apolonia", "taxi", 15, "", "", "€8–10 (차량당)"),
            st("santa_apolonia", "알파 펜둘라르 탑승 (오후 편)", 10, "", at="15:30"),
            mv("santa_apolonia", "campanha", "train", 170, "CP 알파 펜둘라르", "리스본 산타 아폴로니아 → 포르투 캄파냥", "€35.70 (1인)", "인터시다드 €28.05. cp.pt 조기 할인"),
            mv("campanha", "sao_bento", "train", 5, "도시 연결 열차 (같은 표로 환승)"),
            mv("sao_bento", P1, "walk", 10),
            st(P1, "체크인", 30),
            mv(P1, "r_brasao", "walk", 12),
            st("r_brasao", "저녁: Brasão Aliados — 프란세지냐 + 오리밥", 80, "€15–25", "구글로 예약", at="20:00"),
            mv("r_brasao", "dom_luis", "walk", 12),
            st("dom_luis", "동 루이스 다리 위층 야경", 20, "무료"),
            mv("dom_luis", P1, "walk", 10),
        ]},
    porto_day(P1, "5/13", "목"),
    douro_day(P1, 10, "5/14", "금"),
    porto_to_lisbon(P1, L1, "5/15", "토", "salgrosso"),
    lisbon_free(L1, "5/16", "일"),
    lisbon_last(L1),
    lisbon_depart(L1),
]

# ───────────────────────── 코스 2: 포르투갈 일주 (렌터카) ─────────────────────────
L2, P2 = "h_lis_mundial", "h_opo_acta"
CAR = "렌터카 3일 €180–250 (편도 반납료 포함, 추정)"
C2 = [
    lisbon_arrival(L2, 4),
    alfama_fado(L2, 2),
    sintra_cascais(L2, 4),
    {"date": "5/12", "dow": "수", "city": "리스본 → 오비두스 → 나자레", "title": "벨렝, 성곽 마을 오비두스, 거대 파도의 나자레", "photo": "obidos", "sleep": "h_naz_marbravo", "start": "08:15",
     "note": "여행사 일주의 '전용버스' 구간을 렌터카로 (국제운전면허 필요, 고속도로 통행료는 전자 단말기 렌트)", "items":
        belem_items(L2) + [
            mv("belem_tower", L2, "taxi", 20, "", "", "€12–15 (차량당)"),
            st(L2, "체크아웃 · 짐 찾기", 15),
            mv(L2, "car_lisbon", "taxi", 10, "", "", "€6–8 (차량당)"),
            st("car_lisbon", "렌터카 픽업 (오토, 완전자차) · 점심 간단히", 50, CAR),
            mv("car_lisbon", "obidos", "car", 70, "A8 고속도로", "리스본 → 오비두스", "통행료·기름 €15–20 (추정)"),
            st("obidos", "오비두스 — 성벽 위 한 바퀴 + 진지냐(체리주) 초콜릿 잔", 100, "€2 (진지냐)", "성벽 위는 난간 없음"),
            mv("obidos", "nazare", "car", 40, "A8 → N242", "오비두스 → 나자레"),
            st("h_naz_marbravo", "체크인 · 해변 산책", 60),
            mv("h_naz_marbravo", "nazare", "funicular", 5, "나자레 푸니쿨라", "해변 → 시티우 전망대", "€2–3 (추정)"),
            st("nazare", "시티우 전망대 일몰 — 세계 최대 파도 서핑 등대 (" + SUNSET_LIS + ")", 60, "", at="20:00"),
            mv("nazare", "h_naz_marbravo", "funicular", 5),
            st("h_naz_marbravo", "저녁: 해변 식당 생선구이·정어리 (나자레는 검증된 맛집 데이터 없음)", 80, "€20–30"),
        ]},
    {"date": "5/13", "dow": "목", "city": "나자레 → 코임브라 → 아베이루 → 포르투", "title": "대학 도시 코임브라, 운하 도시 아베이루", "photo": "coimbra", "sleep": P2, "start": "08:30", "items": [
        st("h_naz_marbravo", "아침 해변 · 체크아웃", 40),
        mv("h_naz_marbravo", "coimbra", "car", 80, "A8 → A1", "나자레 → 코임브라"),
        st("coimbra", "코임브라 대학교 — 조아니나 도서관(시간 지정)·탑·학생 망토", 120, "", "온라인 예매 (요금 확인)"),
        st("coimbra", "점심: 구시가 식당 (새끼돼지 통구이 레이탕은 근처 메알랴다 명물)", 60, "€15–25"),
        mv("coimbra", "aveiro", "car", 50, "A1", "코임브라 → 아베이루"),
        st("aveiro", "아베이루 — 몰리세이루 보트로 운하 한 바퀴 + 오보스 몰레스(달걀 과자)", 90, "€15 (보트, 추정)"),
        mv("aveiro", "car_porto", "car", 60, "A1 / A29", "아베이루 → 포르투"),
        st("car_porto", "렌터카 반납", 20),
        mv("car_porto", P2, "metro", 15, "메트로 (캄파냥 → 트린다드)", "", "€2 내외"),
        st(P2, "체크인 · 휴식", 60),
        mv(P2, "r_brasao", "walk", 5),
        st("r_brasao", "저녁: Brasão Aliados — 프란세지냐 + 오리밥", 80, "€15–25", "구글로 예약", at="20:15"),
        mv("r_brasao", P2, "walk", 5),
    ]},
    porto_day(P2, "5/14", "금"),
    douro_day(P2, 6, "5/15", "토"),
    porto_to_lisbon(P2, L2, "5/16", "일", "ramiro"),
    lisbon_last(L2),
    lisbon_depart(L2),
]

# ───────────────────────── 코스 3: 리스본 + 라고스 ─────────────────────────
L3, G3 = "h_lis_mundial", "h_lagos_casamae"
C3 = [
    lisbon_arrival(L3, 4),
    alfama_fado(L3, 2),
    sintra_cascais(L3, 4),
    {"date": "5/12", "dow": "수", "city": "리스본 → 라고스", "title": "벨렝 아침, 버스로 남쪽 알가르브", "photo": "belem", "sleep": G3, "start": "08:15", "items":
        belem_items(L3) + [
            mv("belem_tower", L3, "taxi", 20, "", "", "€12–15 (차량당)"),
            st(L3, "체크아웃 · 짐 찾기 · 점심 간단히", 45),
            mv(L3, "oriente", "metro", 25, "메트로 빨간선", "", "€1.90 (1인)"),
            st("oriente", "Rede Expressos 버스 탑승", 10, "", "rede-expressos.pt 좌석 지정", at="13:45"),
            mv("oriente", "lagos_bus", "bus", 225, "Rede Expressos 고속버스", "리스본 오리엔트 → 라고스", "€20–25 (1인, 추정)", "기차는 투네스 환승 약 4시간"),
            mv("lagos_bus", G3, "walk", 10),
            st(G3, "체크인 · 정원 휴식", 50),
            mv(G3, "lagos", "walk", 5),
            st("lagos", "라고스 구시가 골목 · 성벽 · 노예시장 터 광장", 40, "무료"),
            mv("lagos", "r_casinha", "walk", 5),
            st("r_casinha", "저녁: Casinha do Petisco — 구리 냄비 해산물 카타플라나 2인", 90, "€20–30", "자리가 아주 적음 → 이른 시간", at="19:30"),
            mv("r_casinha", G3, "walk", 8),
        ]},
    {"date": "5/13", "dow": "목", "city": "라고스", "title": "폰타 다 피에다드 동굴 보트와 절벽 해변", "photo": "lagos", "sleep": G3, "start": "09:00", "items": [
        mv(G3, "lagos_marina", "walk", 10),
        st("lagos_marina", "폰타 다 피에다드 동굴 보트 (작은 배로 해식 동굴 사이)", 75, "€25–35 (1인, 추정)", "마리나 부스·현장, 파도 높으면 취소", at="09:30"),
        mv("lagos_marina", "ponta_piedade", "taxi", 10, "", "", "€8–10 (차량당)"),
        st("ponta_piedade", "폰타 다 피에다드 절벽 산책로 · 등대 — 위에서 본 동굴과 바위 기둥", 60, "무료"),
        mv("ponta_piedade", "camilo", "walk", 20, note="절벽 위 나무 데크길"),
        st("camilo", "카밀루 해변 — 200계단 아래 작은 만 (바다는 16~18°C)", 60, "무료"),
        mv("camilo", "r_forja", "taxi", 10, "", "", "€8–10 (차량당)"),
        st("r_forja", "점심: A Forja — 보드에 적힌 오늘의 생선 (현금)", 70, "€15", "약 30분 대기"),
        mv("r_forja", G3, "walk", 8),
        st(G3, "수영장 · 낮잠", 150),
        mv(G3, "dona_ana", "walk", 15),
        st("dona_ana", "도나 아나 해변 — 황금 절벽 해변 일몰 산책 (" + SUNSET_LAG + ")", 60, "무료", at="19:30"),
        mv("dona_ana", "r_artistas", "taxi", 8, "", "", "€6–8 (차량당)"),
        st("r_artistas", "기념 디너: Restaurante dos Artistas — 미슐랭 가이드 등재 테이스팅 메뉴", 120, "€40–80", "예약, 일요일 휴무"),
        mv("r_artistas", G3, "walk", 5),
    ]},
    {"date": "5/14", "dow": "금", "city": "라고스", "title": "베나길 동굴 보트, 메이아 프라이아 해산물", "photo": "benagil", "sleep": G3, "start": "09:00", "items": [
        mv(G3, "lagos_marina", "walk", 10),
        st("lagos_marina", "베나길 동굴 보트 투어 (해안 동굴 여러 곳, 2025년부터 동굴 상륙 금지 — 배에서만)", 150, "€35–45 (1인, 추정)", "2~3일 전 예약, 파도 상황 따라 취소", at="09:30"),
        mv("lagos_marina", "r_barrigada", "taxi", 12, "", "", "€8–10 (차량당)"),
        st("r_barrigada", "점심: A Barrigada — 메이아 프라이아 해변 앞 생선구이", 90, "€25–40"),
        st("r_barrigada", "메이아 프라이아 — 4km 모래 해변 산책·선베드", 90, "선베드 €15–20"),
        mv("r_barrigada", G3, "taxi", 12, "", "", "€8–10 (차량당)"),
        st(G3, "호텔 휴식", 120),
        mv(G3, "ponta_piedade", "taxi", 10, "", "", "€8–10 (차량당)"),
        st("ponta_piedade", "폰타 다 피에다드 등대 일몰 (" + SUNSET_LAG + ")", 50, "무료", at="19:50"),
        mv("ponta_piedade", "r_casinha", "taxi", 10, "", "", "€8–10 (차량당)"),
        st("r_casinha", "저녁: Casinha do Petisco — 생선구이 (또는 구시가 다른 식당)", 80, "€20–30"),
        mv("r_casinha", G3, "walk", 8),
    ]},
    {"date": "5/15", "dow": "토", "city": "라고스 → 리스본", "title": "리스본으로 돌아와 타임아웃 마켓과 타스카", "photo": "lisbon_view", "sleep": L3, "start": "08:30", "items": [
        st(G3, "조식 · 체크아웃", 40),
        mv(G3, "lagos_bus", "walk", 10),
        st("lagos_bus", "Rede Expressos 버스 탑승", 10, "", at="09:30"),
        mv("lagos_bus", "oriente", "bus", 225, "Rede Expressos 고속버스", "라고스 → 리스본 오리엔트", "€20–25 (1인, 추정)"),
        mv("oriente", L3, "metro", 25, "메트로 빨간선", "", "€1.90 (1인)"),
        st(L3, "체크인", 20),
        mv(L3, "time_out_market", "taxi", 10, "", "", "€7–9 (차량당)"),
        st("time_out_market", "늦은 점심: 타임아웃 마켓", 60, "€15–30"),
        mv("time_out_market", "cais_sodre", "walk", 3),
        st("cais_sodre", "핑크 스트리트 · 테주강 산책", 40, "무료"),
        mv("cais_sodre", L3, "taxi", 10, "", "", "€7–9 (차량당)"),
        st(L3, "호텔 휴식 · 루프탑 바", 90),
        mv(L3, "r_salgrosso", "taxi", 10, "", "", "€6–8 (차량당)"),
        st("r_salgrosso", "저녁: Taberna Sal Grosso — 알파마 작은 타스카, 바칼라우 아 브라스", 90, "€20–30", "영업일·예약 방식 전화로 확인", at="20:00"),
        mv("r_salgrosso", L3, "taxi", 10, "", "", "€6–8 (차량당)"),
    ]},
    lisbon_free(L3, "5/16", "일"),
    lisbon_last(L3),
    lisbon_depart(L3),
]

COURSES = {1: C1, 2: C2, 3: C3}

# ───────────────────────── 코스 선택 페이지 예산 (만 원, 2인, 1€ ≈ 1,500원) ─────────────────────────
# 항공: 카타르 왕복 1인 143.33만 × 2. 숙소: HOTELS 요금 중간값 × 박수. 현지 교통: 열차·버스·택시·렌터카.
# 입장권·체험: 수도원·궁전·파두·와이너리·보트. 식비: 1인 하루 €45. 기타: 리스본·포르투 숙박세(1박 €2~4) + 예비비.
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
        "course1": {"no": "COURSE 1", "accent": "#1E7FA8", "title": "리스본 + 포르투·도우루, 허니문 정석", "tag": "하나투어 자유허니문 동선 · 도우루 강변 열차 · 파두 디너",
                    "total": 0, "parts": [286.7, 0, 45, 72, 140, 15],
                    "photo": "photos/portugal/porto_ribeira.jpg", "alt": "포르투 히베이라",
                    "flightShort": "카타르 도하 경유", "stayShort": "리스본 시내 + 포르투 강변",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 143.3만 원 (2026-11-06 구글 항공) · 리스본 13:30 도착 / 08:25 출발",
                    "stay": "Avani Avenida Liberdade (리스본) 6박 · Descobertas Boutique (포르투) 3박",
                    "good": "", "watch": "귀국편이 5/18 08:25라 마지막 날은 새벽 공항. 리스본↔포르투 기차 왕복 약 6시간"},
        "course2": {"no": "COURSE 2", "accent": "#2F7A57", "title": "포르투갈 일주, 오비두스·나자레·코임브라", "tag": "여행사 일주 동선을 렌터카로 · 나자레 1박 · 도우루",
                    "total": 0, "parts": [286.7, 0, 80, 70, 135, 15],
                    "photo": "photos/portugal/obidos.jpg", "alt": "오비두스 성곽 마을",
                    "flightShort": "카타르 도하 경유", "stayShort": "4성 가성비",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 143.3만 원 · 렌터카 리스본 픽업 → 포르투 반납",
                    "stay": "Hotel Mundial (리스본) 5박 · Hotel Mar Bravo (나자레) · Hotel Acta The Avenue (포르투) 3박",
                    "good": "", "watch": "렌터카 이틀 운전 (국제운전면허). 나자레·코임브라는 검증된 맛집 데이터가 없음"},
        "course3": {"no": "COURSE 3", "accent": "#B8432A", "title": "리스본 + 알가르브 라고스, 절벽 해안", "tag": "하나투어 허니문의 남부 휴양 · 동굴 보트 두 번 · 포르투 없음",
                    "total": 0, "parts": [286.7, 0, 27, 75, 140, 15],
                    "photo": "photos/portugal/lagos.jpg", "alt": "라고스 폰타 다 피에다드",
                    "flightShort": "카타르 도하 경유", "stayShort": "리스본 + 라고스 부티크",
                    "flight": "카타르항공 도하 1회 경유 왕복 · 1인 143.3만 원 · 리스본↔라고스 고속버스",
                    "stay": "Hotel Mundial (리스본) 6박 · Casa Mãe (라고스) 3박",
                    "good": "", "watch": "포르투를 뺌. 5월 바다는 16~18°C라 수영보다는 보트·절벽 산책. 버스 편도 약 4시간"},
    },
}
NIGHTS = {"course1": {"h_lis_avani": 6, "h_opo_descobertas": 3}, "course2": {"h_lis_mundial": 5, "h_naz_marbravo": 1, "h_opo_acta": 3},
          "course3": {"h_lis_mundial": 6, "h_lagos_casamae": 3}}
GOOD = {"course1": "예산 안(약 {t}만 원). 하나투어 '리스본+포르투' 자유허니문(1인 406만 원~)과 같은 두 도시에 신트라·도우루까지",
        "course2": "예산 안(약 {t}만 원). 노랑풍선·하나투어 일주(1인 504만~560만 원)의 오비두스·나자레·코임브라·포르투를 자유여행으로",
        "course3": "예산 안(약 {t}만 원). 리스본 + 알가르브 절벽 해안, 이동이 가장 적고 느긋함"}
for _c, _n in NIGHTS.items():
    _eur = sum((lambda lo, hi: (lo + hi) / 2)(*map(float, HOTELS[h][2].split(" ")[0].strip("€").split("–"))) * n for h, n in _n.items())
    _b = BUDGET["courses"][_c]
    _b["parts"][1] = round(_eur * 0.15, 1)
    _b["total"] = round(sum(_b["parts"]))
    _b["good"] = GOOD[_c].format(t=_b["total"])

# ───────────────────────── 예약할 것 ─────────────────────────
QATAR = {"what": "카타르항공 왕복: 인천 5/9 01:20 → 도하 → 리스본 13:30 / 리스본 5/18 08:25 → 도하 → 인천 5/19 17:05", "where": "인천 ↔ 리스본",
         "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 143.3만 원 (2026-11-06 구글 항공)", "when": "코스를 고르면 바로. 5월은 2~3월부터 오름",
         "alt": "대한항공 직항(KE921 12:45 → 리스본 20:20 / KE922 22:30 귀국)은 여행사 상품에 쓰이는 편 — 직항을 원하면 2027 운항 요일 확인. 리스본 IN·포르투 OUT 루프트한자 149.3만 원",
         "links": [{"name": "네이버 항공", "tag": "한국어", "url": "https://flight.naver.com/flights/international/ICN-LIS-20270509/LIS-ICN-20270518?adult=2&fareType=Y"},
                   {"name": "카타르항공 공식", "tag": "공식", "url": "https://www.qatarairways.com/ko-kr/homepage.html"},
                   {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}
KLOOK = lambda kw: {"name": "클룩", "tag": "한국어", "url": "https://www.klook.com/ko/search/?query=" + kw}
MRT = lambda kw: {"name": "마이리얼트립", "tag": "한국어", "url": "https://www.myrealtrip.com/search?q=" + kw}
CP = {"name": "CP 포르투갈 철도", "tag": "공식", "url": "https://www.cp.pt/passageiros/en"}
PSINTRA = {"name": "Parques de Sintra 공식", "tag": "공식", "url": "https://www.parquesdesintra.pt/en/"}

T_PENA = {"what": "페나 궁전 09:30 시간 지정 (+ 셔틀)", "where": "신트라", "dates": "5/11 09:30", "price": "€20 + 셔틀 €4.5 (1인)", "when": "2~3주 전. 오전 슬롯부터 매진",
          "alt": "무어인의 성 €12도 같은 사이트", "links": [PSINTRA, KLOOK("페나 궁전")]}
T_REGALEIRA = {"what": "헤갈레이라 별장 14:30 (30분 단위)", "where": "신트라", "dates": "5/11 14:30", "price": "€20 (1인)", "when": "1~2주 전", "alt": "",
               "links": [{"name": "Quinta da Regaleira 공식", "tag": "공식", "url": "https://www.regaleira.pt/en/"}]}
T_JERONIMOS = {"what": "제로니무스 수도원 + 벨렝탑", "where": "리스본 · 벨렝", "dates": "5/12 09:30", "price": "€18 + €15 (1인)", "when": "1~2주 전 시간 지정 (둘 다 월요일 휴관)", "alt": "",
               "links": [{"name": "공식 e-티켓", "tag": "공식", "url": "https://www.museusemonumentos.pt/en"}, KLOOK("제로니무스")]}
T_CASTLE = {"what": "상 조르즈 성", "where": "리스본", "dates": "5/10 09:30", "price": "€17 (1인)", "when": "며칠 전 온라인 (줄 건너뛰기)", "alt": "",
            "links": [{"name": "상 조르즈 성 공식", "tag": "공식", "url": "https://castelodesaojorge.pt/en/"}]}
T_FADO = {"what": "파두 디너 — Clube de Fado", "where": "리스본 · 알파마", "dates": "5/10 20:00", "price": "€78 (1인, 식사+공연)", "when": "1~2주 전", "alt": "O Faia 커버 €20, 한국어 파두 투어는 마이리얼트립",
          "links": [{"name": "Clube de Fado 공식", "tag": "공식", "url": "https://www.clube-de-fado.com/"}, MRT("리스본 파두")]}
T_LELLO = {"what": "렐루 서점 시간 지정 입장", "where": "포르투", "dates": None, "price": "€15.95 (1인, 책 구매 시 차감)", "when": "1~2주 전 첫 타임", "alt": "",
           "links": [{"name": "Livraria Lello 공식", "tag": "공식", "url": "https://www.livrarialello.pt/en/"}]}
T_TAYLOR = {"what": "테일러스 포트와인 셀러 투어 + 시음", "where": "빌라 노바 드 가이아", "dates": None, "price": "€25 (1인)", "when": "1주 전 온라인", "alt": "칼렘 €22, 그레이엄스 €40~",
            "links": [{"name": "Taylor's 공식", "tag": "공식", "url": "https://www.taylor.pt/en/visit-taylors"}]}
T_ALFA = {"what": "CP 알파 펜둘라르 리스본 ↔ 포르투", "where": "산타 아폴로니아 ↔ 캄파냥", "dates": None, "price": "€35.70 (편도 1인, 인터시다드 €28.05)", "when": "1~2달 전 조기 할인",
          "alt": "", "links": [CP, {"name": "트립닷컴 열차", "tag": "한국어", "url": "https://kr.trip.com/trains/"}]}
T_DOURO = {"what": "도우루선 열차 상 벤투 ↔ 피냥", "where": "포르투 → 도우루", "dates": None, "price": "€12.45 (편도 1인) + 하벨루 보트 €12.50", "when": "당일 역 창구·앱 (좌석 지정 없음)",
           "alt": "와이너리 점심 포함 투어 $60~120", "links": [CP, KLOOK("도우루"), MRT("도우루 밸리")]}


def rest(key, when, alt=""):
    r = RESTAURANTS[key]
    links = [{"name": "공식·예약", "tag": "공식", "url": r["url"]}] if r.get("url") else []
    links.append({"name": "트립어드바이저", "tag": "비교", "url": r["rating"]["url"]})
    return {"what": r["name"], "where": r["city"], "dates": "", "price": r["price"], "when": when, "alt": alt, "links": links}


def with_date(item, dates):
    return dict(item, dates=dates)


SITES = [
    {"name": "아고다", "url": "https://www.agoda.com/ko-kr/", "for": "숙소", "note": "한국어·원화 결제. 유로로 결제하면 수수료가 덜 붙음"},
    {"name": "트립닷컴", "url": "https://kr.trip.com/", "for": "숙소·항공·열차·렌터카", "note": "한국어 고객센터. CP 열차·렌터카도 한국어로"},
    {"name": "부킹닷컴", "url": "https://www.booking.com/index.ko.html", "for": "숙소", "note": "라고스·나자레 소형 숙소 재고가 가장 많음"},
    {"name": "네이버 항공", "url": "https://flight.naver.com/", "for": "국제선", "note": "카타르·대한항공 직항·루프트한자 비교"},
    {"name": "CP", "url": "https://www.cp.pt/passageiros/en", "for": "열차", "note": "알파 펜둘라르 조기 할인, 도우루선·신트라선"},
    {"name": "클룩", "url": "https://www.klook.com/ko/", "for": "투어·입장권", "note": "한국어. 신트라·도우루 투어, 파두"},
    {"name": "마이리얼트립", "url": "https://www.myrealtrip.com/", "for": "한국어 가이드·스냅", "note": "리스본·포르투 한국어 워킹투어·스냅"},
]
TAXI = [
    {"what": "리스본 공항 ↔ 시내", "note": "Uber·Bolt 약 €16. 메트로 빨간선 1인 €1.90 + 카드 €0.50", "links": [{"name": "Bolt", "url": "https://bolt.eu/"}]},
    {"what": "포르투 공항 ↔ 시내", "note": "메트로 E선 1인 €2.30 + 카드 €0.60, 택시 €25~35", "links": []},
    {"what": "리스본 대중교통", "note": "나베간트(Navegante) 충전식 카드 하나로 메트로·트램·CP 근교선. 28번 트램은 아침 일찍", "links": []},
    {"what": "언덕 도시 이동", "note": "리스본·포르투는 언덕과 미끄러운 돌길 → 굽 없는 운동화. 오르막은 Uber·Bolt가 싸고 빠름", "links": []},
    {"what": "렌터카 (코스 2)", "note": "국제운전면허증 + 한국 면허증. 고속도로는 전자 통행료라 '비아 베르드' 단말기 렌트 필수", "links": []},
    {"what": "데이터", "note": "eSIM(유럽 10일 10GB) 출국 전 설치", "links": []},
]

BOOKING = {
    "country": {"kicker": "PORTUGAL · 2027.05.09 – 05.18", "page": "portugal.html"},
    "sites": SITES, "taxi": TAXI,
    "courses": {
        1: {"name": "코스 1 · 리스본 + 포르투·도우루", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저. 코스가 정해지면 당일", "items": [QATAR]},
            {"cat": "숙소", "hint": "무료 취소 요금으로 먼저", "auto": "hotels"},
            {"cat": "열차", "hint": "알파 펜둘라르는 일찍 살수록 쌈", "items": [with_date(T_ALFA, "5/12 · 5/15"), with_date(T_DOURO, "5/14")]},
            {"cat": "입장권·공연", "hint": "페나 09:30 슬롯과 렐루 첫 타임이 먼저", "items": [
                with_date(T_CASTLE, "5/10 09:30"), T_FADO, T_PENA, T_REGALEIRA, T_JERONIMOS, with_date(T_LELLO, "5/13 09:00"), with_date(T_TAYLOR, "5/13 15:30")]},
            {"cat": "식당", "hint": "", "items": [
                rest("eurico", "지금 (몇 달 치 예약이 참)"), rest("ramiro", "1~2주 전 웹 예약"), rest("frade", "1~2주 전 전화"), rest("canalha", "1~2주 전"),
                rest("tapabento", "1주 전 구글"), rest("brasao", "며칠 전 구글"), rest("mardoinferno", "1주 전 테라스 (영업 확인)"), rest("salgrosso", "1주 전 전화"), rest("uma", "예약 불가 — 오픈 전 도착")]},
        ]},
        2: {"name": "코스 2 · 포르투갈 일주", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [QATAR]},
            {"cat": "숙소", "hint": "", "auto": "hotels"},
            {"cat": "렌터카·열차", "hint": "", "items": [
                {"what": "렌터카 3일 (리스본 시내 픽업 → 포르투 반납, 오토)", "where": "리스본 → 포르투", "dates": "5/12–5/13", "price": "€180–250 (편도 반납료·완전자차 포함, 추정)",
                 "when": "1~2달 전. 오토는 수량이 적음", "alt": "통행료 단말기(비아 베르드) 함께 렌트", "links": [{"name": "트립닷컴 렌터카", "tag": "한국어", "url": "https://kr.trip.com/carhire/"},
                                                                                           {"name": "Rentalcars", "tag": "비교", "url": "https://www.rentalcars.com/"}]},
                with_date(T_DOURO, "5/15"), with_date(dict(T_ALFA, what="CP 알파 펜둘라르 포르투 → 리스본"), "5/16")]},
            {"cat": "입장권·공연", "hint": "", "items": [
                with_date(T_CASTLE, "5/10 09:30"), T_FADO, T_PENA, T_REGALEIRA, T_JERONIMOS,
                {"what": "코임브라 대학교 (조아니나 도서관 시간 지정)", "where": "코임브라", "dates": "5/13 오전", "price": "요금 공식 사이트 확인", "when": "1~2주 전", "alt": "",
                 "links": [{"name": "코임브라 대학교 방문", "tag": "공식", "url": "https://visit.uc.pt/en/"}]},
                with_date(T_LELLO, "5/14 09:00"), with_date(T_TAYLOR, "5/14 15:30")]},
            {"cat": "식당", "hint": "", "items": [
                rest("eurico", "지금 (참고: 코스 2는 일정에 없음, 원하면 5/17 저녁과 교체)"), rest("ramiro", "1~2주 전 웹 예약"), rest("frade", "1~2주 전 전화"),
                rest("tapabento", "1주 전 구글"), rest("brasao", "며칠 전 구글"), rest("mardoinferno", "1주 전 (영업 확인)"), rest("saltamuro", "며칠 전")]},
        ]},
        3: {"name": "코스 3 · 리스본 + 라고스", "groups": [
            {"cat": "국제선 항공", "hint": "가장 먼저", "items": [QATAR]},
            {"cat": "숙소", "hint": "라고스 부티크부터", "auto": "hotels"},
            {"cat": "버스", "hint": "", "items": [
                {"what": "Rede Expressos 리스본 ↔ 라고스 고속버스", "where": "리스본 오리엔트 ↔ 라고스", "dates": "5/12 · 5/15", "price": "€20–25 (편도 1인, 추정)", "when": "1~2주 전 좌석 지정",
                 "alt": "CP 열차 투네스 환승 약 4시간", "links": [{"name": "Rede Expressos 공식", "tag": "공식", "url": "https://rede-expressos.pt/en"}, CP]}]},
            {"cat": "입장권·보트·공연", "hint": "보트는 파도 따라 취소 → 무료 취소 상품", "items": [
                with_date(T_CASTLE, "5/10 09:30"), T_FADO, T_PENA, T_REGALEIRA, T_JERONIMOS,
                {"what": "폰타 다 피에다드 동굴 보트", "where": "라고스 마리나", "dates": "5/13 09:30", "price": "€25–35 (1인, 추정)", "when": "현장 또는 1~2일 전", "alt": "카약 투어", "links": [KLOOK("라고스 보트")]},
                {"what": "베나길 동굴 보트 투어 (라고스 출발)", "where": "라고스 마리나", "dates": "5/14 09:30", "price": "€35–45 (1인, 추정)", "when": "2~3일 전", "alt": "2025년부터 동굴 상륙 금지 — 배에서만 관람",
                 "links": [KLOOK("베나길"), MRT("베나길")]}]},
            {"cat": "식당", "hint": "", "items": [
                rest("eurico", "지금 (몇 달 치 예약이 참)"), rest("ramiro", "1~2주 전 웹 예약"), rest("frade", "1~2주 전 전화"), rest("artistas", "1~2주 전 전화"),
                rest("casinha", "이른 시간 방문"), rest("mardoinferno", "1주 전 (영업 확인)"), rest("salgrosso", "1주 전 전화"), rest("forja", "현금, 대기")]},
        ]},
    },
}
for c in BOOKING["courses"].values():
    for g in c["groups"]:
        for it in g.get("items", []):
            it["dates"] = it.get("dates") or "코스 일정 참고"
