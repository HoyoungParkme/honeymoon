"""코스별 '예약할 것' 목록을 만든다 → data/booking.json. booking.html이 읽는다.
숙소는 data/courses.json의 잠자리(sleep)에서 자동으로, 나머지(항공·열차·입장권·식당·현지 교통)는 아래 표에서.
사용: python -I tools/build_booking.py"""
import json
import os
import urllib.parse
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
courses = json.load(open(os.path.join(ROOT, "data", "courses.json"), encoding="utf-8"))

YEAR = 2027


def iso(md):  # '5/9' → '2027-05-09'
    m, d = md.split("/")
    return "%d-%02d-%02d" % (YEAR, int(m), int(d))


def q(s):
    return urllib.parse.quote(s)


# ---------- 한국에서 쓰기 좋은 예약처 (공통 안내) ----------
SITES = [
    {"name": "아고다", "url": "https://www.agoda.com/ko-kr/", "for": "숙소", "note": "한국어·원화 결제, 무료 취소 요금 필터. 호텔 공식가보다 비쌀 때가 있으니 공식 사이트와 한 번 비교"},
    {"name": "트립닷컴", "url": "https://kr.trip.com/", "for": "숙소·항공·열차·입장권", "note": "한국어 고객센터. 스페인 열차(Renfe)·알함브라 같은 입장권도 한국어로 살 수 있음"},
    {"name": "부킹닷컴", "url": "https://www.booking.com/index.ko.html", "for": "숙소", "note": "유럽 호텔 재고가 가장 많음. 한국어 지원, 카드 결제는 현지 통화(EUR) 선택이 수수료 덜 나감"},
    {"name": "네이버 항공", "url": "https://flight.naver.com/", "for": "항공", "note": "다구간(마드리드 IN·바르셀로나 OUT) 비교에 편함. 표시가는 카드 조건가일 수 있어 결제 직전 금액 확인"},
    {"name": "클룩", "url": "https://www.klook.com/ko/", "for": "입장권·투어", "note": "한국어. 사그라다·알함브라·플라멩코 등. 공식 사이트보다 €3–10 비싸지만 매진 뒤 구할 때 유용"},
    {"name": "마이리얼트립", "url": "https://www.myrealtrip.com/", "for": "입장권·한인 가이드", "note": "한국어 가이드 투어(알함브라·톨레도 등). 공연·입장권도 일부"},
    {"name": "Renfe 공식", "url": "https://www.renfe.com/es/en", "for": "열차", "note": "영어. 가장 싸고 'Combinado Cercanías'(세르카니아스 무료)는 공식 예매에만 딸려 옴. 한국 카드 결제 가능"},
    {"name": "Omio", "url": "https://www.omio.co.kr/", "for": "열차·버스", "note": "한국어. Renfe·Iryo·OUIGO·ALSA를 한 화면에서 비교. 수수료 €1–3"},
    {"name": "TheFork", "url": "https://www.thefork.com/", "for": "식당", "note": "유럽 식당 예약 앱(영어). 보틴·7 Portes 등 예약 가능. 예약 안 되는 집은 식당 홈페이지나 전화"},
]

# ---------- 택시·현지 이동 (공통) ----------
TAXI = [
    {"what": "택시 앱 미리 설치", "note": "FREE NOW(마드리드·세비야·바르셀로나 택시 호출), Cabify(스페인 전역, 정액 요금), Uber(마드리드·바르셀로나). 셋 다 한국 카드 등록 가능. 공항·역 앞은 줄 서서 타도 됨", "links": [{"name": "FREE NOW", "url": "https://www.free-now.com/"}, {"name": "Cabify", "url": "https://cabify.com/es"}, {"name": "Uber", "url": "https://www.uber.com/kr/ko/"}]},
    {"what": "마드리드 공항 ↔ 시내 택시", "note": "M-30 안쪽(솔·레티로 쪽) ↔ 공항은 정액 €33 (2인·캐리어 포함, 카드 가능). 미터 요금 아님", "links": [{"name": "마드리드시 요금 안내", "url": "https://www.madrid.es/portales/munimadrid/es/Inicio/Movilidad-y-transporte/Taxi"}]},
    {"what": "바르셀로나 공항 → 시내", "note": "택시 약 €35–45 (공항 할증 €4.5 포함). 2인이면 아에로부스 왕복 €12.85가 더 싸고 15분 간격이라 일정은 아에로부스 기준", "links": [{"name": "아에로부스", "url": "https://aerobusbarcelona.es/"}]},
    {"what": "그라나다 택시", "note": "역·버스터미널 ↔ 시내 €7–11. 알함브라 언덕 숙소(Alixares·파라도르)는 밤에 버스가 끊기니 식당에서 택시 불러 달라고 하면 됨(Cabify도 됨)", "links": []},
    {"what": "교통카드", "note": "마드리드 Multi 카드(€2.50, 공항 자판기) + 10회권 / 바르셀로나 T-casual(10회) / 세비야·톨레도·코르도바는 기사에게 현금 또는 컨택리스. 한국 비자·마스터 컨택리스 카드 그대로 됨", "links": [{"name": "마드리드 Multi 카드", "url": "https://www.crtm.es/billetes-y-tarifas/tarjeta-multi"}, {"name": "바르셀로나 T-casual", "url": "https://www.tmb.cat/en/barcelona-fares-metro-bus/single-and-integrated/t-casual"}]},
    {"what": "데이터", "note": "eSIM(유심사·에어알로 등 스페인/유럽 10일 10GB 1~2만 원) 출국 전 설치. 택시 앱·지도·예약 확인에 필수", "links": []},
]

# ---------- 숙소 메타 (잠자리 이름 앞부분 → 도시·공식 사이트·다른 선택지) ----------
HOTELS = {
    "Room Mate Alba": {"city": "마드리드", "search": "Room Mate Alba Madrid", "official": "https://room-matehotels.com/", "alt": "Hotel Regente(3성, 솔 광장 옆, 1박 €150–200 추정)로 바꾸면 3박 약 €150 절약"},
    "Hotel Regente": {"city": "마드리드", "search": "Hotel Regente Madrid", "official": "https://www.hotelregente.com/", "alt": "4성으로 올리고 싶으면 Room Mate Alba(1박 €195–270)"},
    "Las Casas de la Judería": {"city": "세비야", "search": "Las Casas de la Juderia Sevilla", "official": "https://www.lascasasdelajuderiasevilla.com/", "alt": "Hotel Rey Alfonso X(4성, 같은 산타크루스 지구)도 비슷한 가격"},
    "Hotel Rey Alfonso X": {"city": "세비야", "search": "Hotel Rey Alfonso X Sevilla", "official": "https://www.hotelreyalfonsox.com/", "alt": "분위기를 원하면 Las Casas de la Judería(파티오 27개짜리 저택 호텔)"},
    "Hotel Porcel Alixares": {"city": "그라나다", "search": "Hotel Porcel Alixares Granada", "official": "https://www.hotelesporcel.com/", "alt": "시내 쪽이 좋으면 Casa del Capitel Nazarí(알바이신 입구, 1박 €110–150 추정)"},
    "Casa del Capitel Nazarí": {"city": "그라나다", "search": "Casa del Capitel Nazari Granada", "official": "https://www.hotelcasacapitel.com/", "alt": "알함브라 바로 옆이 좋으면 Porcel Alixares(5/14 1박 €90, 조식 포함 확인)"},
    "Parador de Granada": {"city": "그라나다 (알함브라 안)", "search": "Parador de Granada", "official": "https://www.paradores.es/en/parador-de-granada", "alt": "객실 40개뿐이라 못 잡으면 Alixares 1박 더 + 알함브라 야간 입장(€11.27)으로 대체"},
    "Catalonia Catedral": {"city": "바르셀로나", "search": "Catalonia Catedral Barcelona", "official": "https://www.cataloniahotels.com/en/hotel/catalonia-catedral", "alt": "Hotel Lleó(3성, 람블라스 옆, 1박 €180–220 추정)로 바꾸면 3박 약 €400 절약"},
    "Hotel Lleó": {"city": "바르셀로나", "search": "Hotel Lleo Barcelona", "official": "https://www.hotel-lleo.com/", "alt": "루프탑 수영장이 있는 Catalonia Catedral(4성, 1박 €330–360)"},
}


def hotel_links(meta, checkin, nights):
    co = (date.fromisoformat(checkin) + timedelta(days=nights)).isoformat()
    s = meta["search"]
    return [
        {"name": "아고다", "tag": "한국어", "url": "https://www.agoda.com/ko-kr/search?textToSearch=%s&checkIn=%s&los=%d&rooms=1&adults=2&children=0" % (q(s), checkin, nights)},
        {"name": "부킹닷컴", "tag": "한국어", "url": "https://www.booking.com/searchresults.ko.html?ss=%s&checkin=%s&checkout=%s&group_adults=2&no_rooms=1&group_children=0" % (q(s), checkin, co)},
        {"name": "트립닷컴", "tag": "한국어", "url": "https://kr.trip.com/hotels/list?keyword=%s&checkin=%s&checkout=%s&adult=2" % (q(s), checkin.replace("-", "/"), co.replace("-", "/"))},
        {"name": "공식 사이트", "tag": "공식", "url": meta["official"]},
    ]


def hotel_items(course):
    """같은 숙소가 이어지는 밤을 묶어 체크인 날짜·박수를 계산한다."""
    runs = []
    for d in courses[course]["days"]:
        name = d.get("sleepName") or ""
        if name.startswith("기내"):
            continue
        if runs and runs[-1]["name"] == name and runs[-1]["last"] == d["n"] - 1:
            runs[-1]["nights"] += 1
            runs[-1]["last"] = d["n"]
        else:
            runs.append({"name": name, "checkin": iso(d["date"]), "nights": 1, "last": d["n"], "price": d.get("sleepPrice", ""), "kayak": d.get("sleepUrl", "")})
    out = []
    for r in runs:
        key = next(k for k in HOTELS if r["name"].startswith(k))
        m = HOTELS[key]
        co = (date.fromisoformat(r["checkin"]) + timedelta(days=r["nights"])).isoformat()
        when = "2027년 5월 재고가 열리는 대로 (2026-11-04 기준 미오픈). 무료 취소 요금으로 먼저 잡기" if key != "Hotel Porcel Alixares" else "지금 가능 (2026-11-04 Booking에서 €90·조식 포함·무료 취소 확인)"
        if key == "Parador de Granada":
            when = "객실 40개. 파라도르 공식 사이트에 2027.5가 열리는 즉시 (보통 12개월 전). 이 코스의 1순위 예약"
        out.append({
            "what": r["name"], "where": m["city"],
            "dates": "%s 체크인 · %d박 (%s 체크아웃)" % (r["checkin"][5:].replace("-", "/"), r["nights"], co[5:].replace("-", "/")),
            "price": r["price"].replace(" (2인 1실, 카약 검색가)", "") + " · 1박 2인 1실",
            "when": when, "alt": m["alt"],
            "links": hotel_links(m, r["checkin"], r["nights"]) + [{"name": "카약 비교", "tag": "비교", "url": r["kayak"]}],
        })
    return out


# ---------- 항공 ----------
NAVER_MULTI = "https://flight.naver.com/flights/international/SEL:city-MAD:airport-20270509/BCN:airport-SEL:city-20270518"
NAVER_RT = "https://flight.naver.com/flights/international/ICN-MAD-20270509/MAD-ICN-20270518?adult=2&fareType=Y"
FLIGHTS = {
    "course1": [{"what": "카타르항공 다구간: 인천 → 마드리드 (5/9 01:20 → 14:15) / 바르셀로나 → 인천 (5/18 오후)", "where": "인천 ↔ 마드리드·바르셀로나", "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 121.1만 원 (2026-11-04 구글 항공 최저가)", "when": "코스를 고르면 바로. 5월은 성수기 초입이라 2~3월부터 오름",
                 "alt": "같은 도하 경유 에미레이트(두바이)는 약 137만, 직항 대한항공·아시아나는 213만", "links": [{"name": "네이버 항공 (다구간)", "tag": "한국어", "url": NAVER_MULTI}, {"name": "카타르항공 공식", "tag": "공식", "url": "https://www.qatarairways.com/ko-kr/homepage.html"}, {"name": "트립닷컴 항공", "tag": "한국어", "url": "https://kr.trip.com/flights/"}, {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}],
    "course2": [{"what": "대한항공·아시아나 직항 다구간: 인천 → 마드리드 (5/9 09:55 → 18:00) / 바르셀로나 → 인천 (5/18 저녁)", "where": "인천 ↔ 마드리드·바르셀로나", "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 213.4만 원 (2026-11-04 구글 항공 최저가)", "when": "코스를 고르면 바로. 직항은 좌석이 적어 늦을수록 비쌈",
                 "alt": "귀국편만 경유(에어프랑스·루프트한자)로 바꾸면 1인 약 150~165만. 가는 편 직항 + 귀국 경유 조합도 네이버 다구간에서 비교 가능", "links": [{"name": "네이버 항공 (다구간)", "tag": "한국어", "url": NAVER_MULTI}, {"name": "대한항공", "tag": "공식", "url": "https://www.koreanair.com/"}, {"name": "아시아나항공", "tag": "공식", "url": "https://flyasiana.com/"}, {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}],
    "course3": [{"what": "대한항공 마드리드 왕복 직항: 인천 → 마드리드 (5/9 09:55 → 18:00) / 마드리드 → 인천 (5/18 20:00 → 5/19 16:00)", "where": "인천 ↔ 마드리드", "dates": "5/9 출발 · 5/18 귀국", "price": "1인 약 195.3만 원 (2026-11-04 구글 항공 최저가)", "when": "코스를 고르면 바로. 왕복 직항은 대한항공 하루 1편뿐",
                 "alt": "카타르항공 경유 왕복은 1인 약 119만 (편도 20시간)", "links": [{"name": "네이버 항공 (왕복)", "tag": "한국어", "url": NAVER_RT}, {"name": "대한항공", "tag": "공식", "url": "https://www.koreanair.com/"}, {"name": "트립닷컴 항공", "tag": "한국어", "url": "https://kr.trip.com/flights/"}, {"name": "구글 항공", "tag": "비교", "url": "https://www.google.com/travel/flights?hl=ko&curr=KRW"}]}],
}

# ---------- 열차·버스·국내선 ----------
RENFE = {"name": "Renfe 공식", "tag": "공식", "url": "https://www.renfe.com/es/en"}
OMIO = {"name": "Omio", "tag": "한국어", "url": "https://www.omio.co.kr/"}
TRIP_TRAIN = {"name": "트립닷컴 열차", "tag": "한국어", "url": "https://kr.trip.com/trains/"}
T_TOLEDO = {"what": "마드리드 ↔ 톨레도 Avant 왕복", "where": "아토차 ↔ 톨레도", "dates": "5/11 08:45 출발 · 17:25 귀환", "price": "편도 €11–13, 왕복 약 €22 (1인)", "when": "출발 2달 전쯤 (Avant는 정액이라 서두를 필요 없음, 좌석만 확보)", "alt": "버스(ALSA, 플라사 엘립티카 출발 50분 €6)도 있지만 열차가 빠름", "links": [RENFE, OMIO, TRIP_TRAIN]}
T_CORDOBA = {"what": "마드리드 → 코르도바 → 세비야 고속열차", "where": "아토차 → 코르도바 → 산타 후스타", "dates": "5/12 07:20 마드리드 출발 · 15:50 코르도바 출발", "price": "마드리드→코르도바 €9–45, 코르도바→세비야 €7–37 (조기 예매가, 1인)", "when": "판매 시작(보통 3~4개월 전)하면 바로. 저가(Iryo·OUIGO·Renfe Básico)는 먼저 팔림. 환불 가능 요금으로", "alt": "Iryo·OUIGO가 Renfe보다 싸지만 캐리어 추가요금(OUIGO €5). Renfe로 사면 솔↔아토차 세르카니아스 무료", "links": [RENFE, {"name": "Iryo", "tag": "공식", "url": "https://iryo.eu/en/home"}, {"name": "OUIGO", "tag": "공식", "url": "https://www.ouigo.com/es/en"}, OMIO, TRIP_TRAIN]}
T_SEV_GRA_TRAIN = {"what": "세비야 → 그라나다 열차", "where": "산타 후스타 → 그라나다역", "dates": "5/14 07:30 출발 (2시간 40분)", "price": "€30–48 (1인)", "when": "판매 시작하면 바로 (하루 4편뿐)", "alt": "ALSA 버스 3시간 €21–29 (코스 2 방식)", "links": [RENFE, OMIO, TRIP_TRAIN]}
T_SEV_GRA_BUS = {"what": "세비야 → 그라나다 ALSA 버스", "where": "플라사 데 아르마스 → 그라나다 버스터미널", "dates": "5/14 07:55 출발 (3시간)", "price": "€21–29 (1인)", "when": "한 달 전이면 충분. 온라인이 창구보다 쌈", "alt": "열차 2시간 40분 €30–48 (코스 1·3 방식)", "links": [{"name": "ALSA 공식", "tag": "공식", "url": "https://www.alsa.com/en/"}, OMIO]}
T_GRX_BCN = {"what": "부엘링 그라나다 → 바르셀로나 국내선", "where": "GRX → BCN", "dates": "5/15 오후 (16:30 전후 편)", "price": "편도 €41부터 + 위탁수하물 25kg 웹 €18–99 (1인)", "when": "국제선 다음으로 바로. 저가항공은 3~4개월 전이 가장 쌈. 수하물은 예매 때 같이(공항에서 추가하면 2~3배)", "alt": "열차는 7시간 이상이라 비추. Optima 요금에 수하물 포함", "links": [{"name": "부엘링 공식", "tag": "공식", "url": "https://www.vueling.com/en"}, {"name": "트립닷컴 항공", "tag": "한국어", "url": "https://kr.trip.com/flights/"}, {"name": "스카이스캐너", "tag": "한국어", "url": "https://www.skyscanner.co.kr/"}]}
T_GRA_MAD = {"what": "그라나다 → 마드리드 AVE", "where": "그라나다역 → 아토차", "dates": "5/16 10:50 출발 (3시간 20분)", "price": "€23–30 조기 예매 (1인)", "when": "판매 시작하면 바로. 2026-02 운행 재개 확인됨, 예매 전 운행 여부 다시 확인", "alt": "운행이 멈추면 그라나다 → 마드리드 국내선(이베리아·부엘링 1시간)", "links": [RENFE, OMIO, TRIP_TRAIN]}
T_SEGOVIA = {"what": "마드리드 ↔ 세고비아 Avant 왕복", "where": "차마르틴 ↔ 세고비아-기오마르", "dates": "5/17 08:55 출발 · 18:25 귀환", "price": "편도 €19.70부터 (1인)", "when": "출발 2달 전쯤", "alt": "버스(Avanza, 몽클로아 출발 1시간 15분 €5)가 싸지만 열차 27분", "links": [RENFE, OMIO]}
T_MONTSERRAT = {"what": "몬세라트 Trans Montserrat 통합권", "where": "에스파냐 광장 FGC역", "dates": "5/17 당일", "price": "€50 (메트로 왕복 + R5 + 산악열차 + 푸니쿨라 2개, 1인)", "when": "현장 자판기에서 당일 구매 (예약 불필요)", "alt": "FGC 온라인 구매도 가능. 산악열차 대신 케이블카(Aeri)는 별도 요금", "links": [{"name": "FGC 공식", "tag": "공식", "url": "https://www.fgc.cat/en/"}, {"name": "클룩 (몬세라트 투어)", "tag": "한국어", "url": "https://www.klook.com/ko/search/?query=%EB%AA%AC%EC%84%B8%EB%9D%BC%ED%8A%B8"}]}
T_AEROBUS = {"what": "바르셀로나 아에로부스 왕복권", "where": "엘 프라트 T1 ↔ 카탈루냐 광장", "dates": "5/15 도착 · 5/18 출국", "price": "왕복 €12.85 (90일 유효, 1인)", "when": "도착해서 정류장 자판기나 앱에서. 왕복권이 편도 두 장보다 €2 쌈", "alt": "택시 €35–45", "links": [{"name": "아에로부스 공식", "tag": "공식", "url": "https://aerobusbarcelona.es/"}]}
TRANSPORT = {
    "course1": [T_TOLEDO, T_CORDOBA, T_SEV_GRA_TRAIN, T_GRX_BCN, T_AEROBUS, T_MONTSERRAT],
    "course2": [T_TOLEDO, T_CORDOBA, T_SEV_GRA_BUS, T_GRX_BCN, T_AEROBUS, T_MONTSERRAT],
    "course3": [T_TOLEDO, T_CORDOBA, T_SEV_GRA_BUS, T_GRA_MAD, T_SEGOVIA],
}

# ---------- 입장권·공연·체험 ----------
KLOOK = lambda kw: {"name": "클룩", "tag": "한국어", "url": "https://www.klook.com/ko/search/?query=" + q(kw)}
MRT = lambda kw: {"name": "마이리얼트립", "tag": "한국어", "url": "https://www.myrealtrip.com/search?q=" + q(kw)}
K_PALACIO = {"what": "마드리드 왕궁 입장권 (09:30 슬롯)", "where": "마드리드", "dates": "5/10 09:30", "price": "€18.77 (1인, 온라인)", "when": "약 1~2달 전 (패트리모니오 나시오날 공식). 슬롯 15분 단위", "alt": "매진이면 클룩 가이드 투어로", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://tickets.patrimonionacional.es/en/tickets/palacio-real-de-madrid"}, KLOOK("마드리드 왕궁")]}
K_PRADO = {"what": "프라도 미술관 무료 시간 (18:00–20:00)", "where": "마드리드", "dates": "5/10 18:00", "price": "무료 (예약 불필요, 줄 30분)", "when": "예약 없음. 줄 서기 싫으면 일반권 €15 온라인", "alt": "일반권 €15로 오후 내내", "links": [{"name": "공식", "tag": "공식", "url": "https://www.museodelprado.es/en/visit/opening-times-and-prices"}]}
K_BOTIN_ETC = None
K_MEZQUITA = {"what": "메스키타 입장권", "where": "코르도바", "dates": "5/12 09:43", "price": "€15 (1인)", "when": "2~3주 전이면 됨 (공식 사이트)", "alt": "현장 구매도 보통 가능", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.mezquita-catedraldecordoba.es/en/organiza-tu-visita/"}, KLOOK("메스키타")]}
K_ALCAZAR = {"what": "세비야 알카사르 (09:30 입장)", "where": "세비야", "dates": "5/13 09:30", "price": "€15.50 (1인, 온라인)", "when": "약 2달 전 공식 예매. 5월은 빨리 매진", "alt": "매진이면 클룩·마이리얼트립 가이드 투어(€40~)", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.alcazarsevilla.org/en/"}, KLOOK("세비야 알카사르"), MRT("세비야 알카사르")]}
K_CATEDRAL_SEV = {"what": "세비야 대성당 + 히랄다 탑", "where": "세비야", "dates": "5/13 11:33", "price": "€13 (1인, 온라인)", "when": "1달 전", "alt": "", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.catedraldesevilla.es/en/cultural-visit/"}]}
K_FLAMENCO_SEV = {"what": "Casa de la Memoria 플라멩코 19:30", "where": "세비야", "dates": "5/13 19:30", "price": "€24 (1인)", "when": "1달 전 (100석, 주말은 매진)", "alt": "Museo del Baile Flamenco 공연 €25", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.casadelamemoria.es/"}, KLOOK("세비야 플라멩코")]}
K_SETAS = {"what": "세타스 데 세비야 전망대 야경", "where": "세비야", "dates": "5/13 22:00", "price": "약 €15 (1인, 미확인)", "when": "당일 현장", "alt": "", "links": [{"name": "공식", "tag": "공식", "url": "https://setasdesevilla.com/en/"}]}
K_HAMMAM = {"what": "Hammam Al Ándalus 아랍 목욕탕 (목욕 + 마사지 15분)", "where": "그라나다", "dates": "5/14 낮", "price": "€65 (1인)", "when": "2~3주 전 공식 사이트. 2인 동시 슬롯으로", "alt": "마사지 없이 목욕만 €45", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://granada.hammamalandalus.com/en/"}, KLOOK("그라나다 하맘")]}
K_ALHAMBRA = {"what": "알함브라 일반권 (나스르 궁전 시간 지정)", "where": "그라나다", "dates": "5/15 08:30 입장", "price": "€22.27 + 수수료 (1인)", "when": "가장 먼저. 공식 사이트에 2027.5 날짜가 열리는지 수시 확인(여행사는 3개월 전 안내, 5월은 매진 잦음). 여권 영문 이름 그대로, 환불 불가", "alt": "매진이면 클룩·마이리얼트립 가이드 투어(€50~70, 입장권 포함)가 현실적 대안", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://tickets.alhambra-patronato.es/en/"}, KLOOK("알함브라"), MRT("알함브라"), {"name": "트립닷컴", "tag": "한국어", "url": "https://kr.trip.com/travel-guide/attraction/granada/alhambra-10521581/"}]}
K_SACROMONTE = {"what": "Venta El Gallo 사크로몬테 동굴 플라멩코 21:00", "where": "그라나다", "dates": "5/15 21:00", "price": "공연 €25, 저녁 포함 €55 (1인)", "when": "2~3주 전 공식 사이트", "alt": "Cuevas Los Tarantos (같은 골목, €30)", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.ventaelgallo.es/"}, KLOOK("사크로몬테 플라멩코")]}
K_SAGRADA = {"what": "사그라다 파밀리아 (09:00 입장, 탑 없이)", "where": "바르셀로나", "dates": "5/16 09:00", "price": "€26 기본 (탑 포함 €36, 1인)", "when": "2~3달 전 공식. 오전 슬롯 먼저 매진", "alt": "매진이면 클룩(€30~) 또는 가이드 투어", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://sagradafamilia.org/en/tickets"}, KLOOK("사그라다 파밀리아"), MRT("사그라다 파밀리아")]}
K_BATLLO = {"what": "카사 바트요 (12:00)", "where": "바르셀로나", "dates": "5/16 12:00", "price": "€35~ (다이내믹, 1인)", "when": "1~2달 전. 아침·저녁 슬롯이 쌈", "alt": "카사 밀라(라 페드레라) 내부 €28로 대체 가능", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.casabatllo.es/en/tickets/"}, KLOOK("카사 바트요")]}
K_GUELL = {"what": "구엘 공원 (15:30 슬롯)", "where": "바르셀로나", "dates": "5/16 15:30", "price": "€18 (1인)", "when": "1달 전 공식. 30분 단위 슬롯", "alt": "", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://parkguell.barcelona/en/buy-tickets"}, KLOOK("구엘 공원")]}
K_SAILING = {"what": "포르트 벨 선셋 세일링 (18:30)", "where": "바르셀로나", "dates": "5/17 18:30", "price": "약 €45–60 (1인, 미확인)", "when": "1~2주 전. 날씨 보고 확정", "alt": "안 타면 바르셀로네타 해변 산책으로", "links": [KLOOK("바르셀로나 선셋 세일링"), {"name": "GetYourGuide", "tag": "비교", "url": "https://www.getyourguide.com/s/?q=barcelona%20sunset%20sailing"}]}
K_SEGOVIA = {"what": "세고비아 알카사르 (탑 포함)", "where": "세고비아", "dates": "5/17 13:30", "price": "€10 (1인)", "when": "현장 구매 가능. 온라인은 1~2주 전", "alt": "", "links": [{"name": "공식 예매", "tag": "공식", "url": "https://www.alcazardesegovia.com/en/"}]}
TICKETS = {
    "course1": [K_ALHAMBRA, K_SAGRADA, K_ALCAZAR, K_PALACIO, K_BATLLO, K_GUELL, K_HAMMAM, K_FLAMENCO_SEV, K_CATEDRAL_SEV, K_MEZQUITA, K_SAILING, K_SETAS, K_PRADO],
    "course2": [K_ALHAMBRA, K_SAGRADA, K_ALCAZAR, K_PALACIO, K_BATLLO, K_GUELL, K_FLAMENCO_SEV, K_CATEDRAL_SEV, K_MEZQUITA, K_SAILING, K_SETAS, K_PRADO],
    "course3": [K_ALHAMBRA, K_ALCAZAR, K_PALACIO, K_HAMMAM, K_SACROMONTE, K_FLAMENCO_SEV, K_CATEDRAL_SEV, K_MEZQUITA, K_SEGOVIA, K_SETAS, K_PRADO],
}

# ---------- 식당 (예약이 필요한 곳만) ----------
FORK = lambda kw: {"name": "TheFork", "tag": "비교", "url": "https://www.thefork.com/search/?q=" + q(kw)}
R_BOTIN = {"what": "Sobrino de Botín (세계 최고 오래된 식당, 새끼돼지 통구이)", "where": "마드리드", "dates": "5/10 21:15", "price": "1인 €50–65", "when": "1~2달 전 공식 사이트 예약. 신혼여행 메모 남기면 지하 와인셀러 자리", "alt": "Casa Lucio(계란 요리) 1인 €45–60", "links": [{"name": "공식 예약", "tag": "공식", "url": "https://botin.es/en/"}, FORK("Botin Madrid")]}
R_BOLA = {"what": "Taberna La Bola (코시도 마드릴레뇨)", "where": "마드리드", "dates": "5/10 12:35", "price": "1인 €31–45", "when": "1~2주 전 전화 또는 홈페이지 (+34 915 47 69 30)", "alt": "예약 안 되면 12:30 오픈런", "links": [{"name": "공식", "tag": "공식", "url": "https://labola.es/en/"}]}
R_BOTERO = {"what": "Taberna El Botero", "where": "톨레도", "dates": "5/11 11:24", "price": "1인 €30–40", "when": "1주 전 전화", "alt": "예약 없이 가도 11시 반엔 자리 있음", "links": [FORK("El Botero Toledo")]}
R_CAMPOS = {"what": "Bodegas Campos", "where": "코르도바", "dates": "5/12 12:17", "price": "1인 €40–50", "when": "1~2주 전 홈페이지", "alt": "", "links": [{"name": "공식 예약", "tag": "공식", "url": "https://www.bodegascampos.com/en/"}, FORK("Bodegas Campos")]}
R_RINCONCILLO = {"what": "El Rinconcillo (1670년 타파스 바)", "where": "세비야", "dates": "5/13 13:30", "price": "1인 €20–30", "when": "바 자리는 예약 없음. 테이블은 1주 전 전화", "alt": "", "links": [{"name": "공식", "tag": "공식", "url": "https://www.elrinconcillo.es/"}]}
R_ESLAVA = {"what": "Eslava", "where": "세비야", "dates": "5/13 20:40", "price": "1인 €30–40", "when": "1~2주 전 (식당 안 테이블만 예약)", "alt": "바 쪽은 줄", "links": [{"name": "공식", "tag": "공식", "url": "https://www.espacioeslava.com/"}, FORK("Eslava Sevilla")]}
R_MORAYMA = {"what": "Mirador de Morayma (알함브라 뷰 디너)", "where": "그라나다", "dates": "5/14 21:30", "price": "1인 €40–55", "when": "2~3주 전. 예약 때 '테라스, 알함브라 뷰' 요청", "alt": "Carmen Mirador de Aixa (같은 뷰, 더 고급 €60~)", "links": [{"name": "공식 예약", "tag": "공식", "url": "https://www.miradordemorayma.com/en/"}, FORK("Mirador de Morayma")]}
R_CALPEP = {"what": "Cal Pep (바 자리 해산물 타파스)", "where": "바르셀로나", "dates": "5/15 19:30", "price": "1인 €50–70", "when": "바는 예약 없음, 오픈(19:30) 전 줄. 테이블은 1달 전", "alt": "", "links": [{"name": "공식", "tag": "공식", "url": "https://www.calpep.com/"}]}
R_7PORTES = {"what": "7 Portes (1836년 파에야)", "where": "바르셀로나", "dates": "5/16 19:00", "price": "1인 €45–60", "when": "2~3주 전 홈페이지", "alt": "", "links": [{"name": "공식 예약", "tag": "공식", "url": "https://7portes.com/en/"}, FORK("7 Portes")]}
R_CANDIDO = {"what": "Mesón de Cándido (수도교 앞 새끼돼지)", "where": "세고비아", "dates": "5/17 11:45", "price": "1인 €45–60", "when": "2~3주 전 홈페이지. 수도교 보이는 창가 요청", "alt": "José María 1인 €40~", "links": [{"name": "공식 예약", "tag": "공식", "url": "https://www.mesondecandido.es/en/"}, FORK("Meson de Candido")]}
R_LUCIO = {"what": "Casa Lucio (계란 요리 우에보스 로토스)", "where": "마드리드", "dates": "5/16 20:30", "price": "1인 €45–60", "when": "2~3주 전 전화 (+34 913 65 32 52)", "alt": "", "links": [{"name": "공식", "tag": "공식", "url": "https://casalucio.es/"}]}
RESTAURANTS = {
    "course1": [R_BOTIN, R_MORAYMA, R_BOLA, R_CALPEP, R_7PORTES, R_CAMPOS, R_ESLAVA, R_RINCONCILLO, R_BOTERO],
    "course2": [R_BOTIN, R_MORAYMA, R_BOLA, R_CALPEP, R_7PORTES, R_CAMPOS, R_ESLAVA, R_RINCONCILLO, R_BOTERO],
    "course3": [R_BOTIN, R_MORAYMA, R_CANDIDO, R_LUCIO, R_BOLA, R_CAMPOS, R_ESLAVA, R_RINCONCILLO, R_BOTERO],
}

def due_of(when):
    """'언제' 설명문에서 짧은 꼬리표를 뽑는다 (지금 / 열리면 / 3개월 전 / … / 현장)."""
    w = when
    if "현장" in w or "당일" in w or "도착해서" in w:
        return "현장"
    if "판매 시작" in w or "12개월" in w or "열리는 대로" in w or "열리는 즉시" in w or "열리는지" in w:
        return "열리면"
    if "가장 먼저" in w or "바로" in w or "지금" in w or "다음으로" in w:
        return "지금"
    if "3~4개월" in w or "3개월" in w or "2~3달" in w or "3달" in w:
        return "3개월 전"
    if "2달" in w or "1~2달" in w:
        return "2개월 전"
    if "1달" in w or "한 달" in w:
        return "1개월 전"
    if "주 전" in w:
        return "2주 전"
    return "미리"


out = {"generated": "2026-11-04", "sites": SITES, "taxi": TAXI, "courses": {}}
for c in ("course1", "course2", "course3"):
    out["courses"][c] = {"groups": [
        {"cat": "국제선 항공", "hint": "가장 먼저. 코스가 정해지면 당일", "items": FLIGHTS[c]},
        {"cat": "숙소", "hint": "무료 취소 요금으로 먼저 잡고, 가격 떨어지면 갈아타기", "items": hotel_items(c)},
        {"cat": "열차·버스·국내선", "hint": "판매 시작 시점이 다 달라서 표마다 '언제'를 확인", "items": TRANSPORT[c]},
        {"cat": "입장권·공연·체험", "hint": "시간 지정 입장은 매진되면 끝. 알함브라·사그라다·알카사르 순", "items": TICKETS[c]},
        {"cat": "식당", "hint": "예약이 되는 집만. 바 자리 집은 오픈 시간 맞춰 가기", "items": RESTAURANTS[c]},
    ]}
    for g in out["courses"][c]["groups"]:
        g["items"] = [dict(it, due=due_of(it["when"])) for it in g["items"]]
json.dump(out, open(os.path.join(ROOT, "data", "booking.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("booking.json:", {c: sum(len(g["items"]) for g in v["groups"]) for c, v in out["courses"].items()}, "items")
