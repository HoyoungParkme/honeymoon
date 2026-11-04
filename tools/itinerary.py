"""세 코스의 일자별 문앞-문앞 이동 데이터. 시간은 build_days()가 순서대로 계산한다."""


def mv(frm, to, mode, mins, line="", stops="", fare="", note=""):
    return {"kind": "move", "frm": frm, "to": to, "mode": mode, "mins": mins, "line": line, "stops": stops, "fare": fare, "note": note}


def st(place, do, dur, fare="", note="", at=None, link=""):
    return {"kind": "stop", "place": place, "do": do, "dur": dur, "fare": fare, "note": note, "at": at, "link": link}


# 자주 쓰는 요금 문구
M10 = "10회권 1회 차감 (€0.73)"
T_CASUAL = "T-casual 1회 차감 (€1.30)"
GRA_BUS = "€1.60 기사에게 현금·카드 (60분 내 환승 무료)"

CAFES = {
    "hotelA_mad": "La Mallorquina (솔 광장 8번지, 1894년 제과점) 추로스·토스타다 약 €5–8",
    "hotelB_mad": "La Mallorquina (솔 광장 8번지, 호텔에서 6분) 추로스·토스타다 약 €5–8",
    "hotelA_sev": "Bar El Comercio (Calle Lineros 9, 1904년 추로스 바) 약 €4–6",
    "hotelB_sev": "Bar El Comercio (Calle Lineros 9, 1904년 추로스 바) 약 €4–6",
    "hotelA_gra": "호텔 조식 권장 (언덕 위라 주변 카페가 멀어)",
    "hotelB_gra": "Café Fútbol (Plaza Mariana Pineda 6, 추로스 명가) 약 €4–6",
    "parador": "파라도르 조식 (성벽 안이라 대안이 없어)",
    "hotelA_bcn": "Granja Viader (Carrer d'en Xuclà 4, 1870년 우유가게) 핫초코·추로스 약 €5–8",
    "hotelB_bcn": "Granja Viader (Carrer d'en Xuclà 4, 호텔에서 4분) 핫초코·추로스 약 €5–8",
}

# 호텔 조식 (2026-11-03 각 호텔 공식 사이트 확인). 금액이 없는 곳은 예약 화면 옵션으로만 나온다
BREAKFAST = {
    "hotelA_mad": "호텔 조식 — 유료 옵션, 금액은 예약 화면에서 확인 (보통 €12–20)",
    "hotelB_mad": "호텔 조식 — €11.95 (예약 시 옵션 추가)",
    "hotelA_sev": "호텔 조식 — 유료 옵션, 금액은 예약 화면에서 확인 (보통 €12–20)",
    "hotelB_sev": "호텔 조식 — 유료 옵션, 금액은 예약 화면에서 확인 (보통 €12–20)",
    "hotelA_gra": "호텔 조식 — 약 €16 (예약 시 옵션 추가)",
    "hotelB_gra": "호텔 조식 — 공식 사이트로 예약하면 포함",
    "parador": "파라도르 조식 — 유료 옵션, 금액은 예약 화면에서 확인",
    "hotelA_bcn": "호텔 조식 — 유료 옵션, 금액은 예약 화면에서 확인 (보통 €12–20)",
    "hotelB_bcn": "호텔 조식 — 유료 옵션, 금액은 예약 화면에서 확인 (보통 €12–20)",
}


# ───────────────────────── 마드리드 공통 ─────────────────────────
def madrid_day2(hotel):
    first = (mv(hotel, "palacio_real", "walk", 21, note="솔 광장 → 마요르 거리 → 바일렌 거리. 메트로 환승이 더 오래 걸려")
             if hotel == "hotelA_mad" else
             mv(hotel, "palacio_real", "metro", 10, "5호선 Casa de Campo 방면", "Callao → Ópera (1정거장) + 도보 5분", M10, "걸어도 14분"))
    return {
        "date": "5/10", "dow": "월", "city": "마드리드", "title": "왕궁에서 프라도까지", "photo": "palacio_real", "sleep": hotel, "start": "08:45",
        "items": [
            first,
            st("palacio_real", "마드리드 왕궁 관람 (09:30 입장 슬롯)", 120, "€18.77", "15분 단위 시간 지정, 큰 가방 자제", at="09:30",
               link="https://tickets.patrimonionacional.es/en/tickets/palacio-real-de-madrid"),
            mv("palacio_real", "almudena", "walk", 2, note="아르메리아 광장 건너편"),
            st("almudena", "알무데나 대성당 외관·내부", 30, "무료"),
            mv("almudena", "sabatini", "walk", 8, note="바일렌 거리 따라 북쪽"),
            st("sabatini", "사바티니 정원에서 왕궁 북쪽 면 보기", 20, "무료"),
            mv("sabatini", "la_bola", "walk", 5),
            st("la_bola", "점심: Taberna La Bola — 항아리 코시도 (예약 권장)", 75, "€31–45", link="https://www.esmadrid.com/en/restaurants/bola"),
            mv("la_bola", "plaza_villa", "walk", 6, note="오페라 광장 → 마요르 거리 → 비야 광장"),
            st("plaza_villa", "비야 광장 — 15세기 옛 시청사·루하네스 탑 (여행사 시내투어 코스)", 15, "무료"),
            mv("plaza_villa", "mercado_san_miguel", "walk", 3),
            st("mercado_san_miguel", "산 미겔 시장 — 1916년 철골 시장, 타파스 한두 접시 맛보기", 35, "€5–10", link="https://mercadodesanmiguel.es/en/"),
            mv("mercado_san_miguel", "plaza_mayor", "walk", 2, note="쿠치예로스 아치로 올라가기"),
            st("plaza_mayor", "마요르 광장 한 바퀴", 25, "무료"),
            mv("plaza_mayor", "sol", "walk", 5),
            mv("sol", "retiro_metro", "metro", 8, "2호선 Las Rosas 방면", "Sol → Retiro (3정거장)", M10, "걸으면 23분"),
            mv("retiro_metro", "puerta_alcala", "walk", 2),
            st("puerta_alcala", "레티로 공원 산책 (알칼라 문 → 호수)", 60, "무료"),
            mv("puerta_alcala", "prado", "walk", 13, note="알폰소 12세 거리 따라 남쪽, 고야 문으로"),
            st("prado", "프라도 미술관 (18–20시 무료 입장 시간)", 110, "무료", "월~토 18:00–20:00 무료. 줄이 길면 17:30부터 서기", at="18:00",
               link="https://www.museodelprado.es/en/visit/opening-times-and-prices"),
            mv("prado", "cba", "walk", 10, note="프라도 대로 → 알칼라 거리"),
            st("cba", "시르쿨로 데 베야스 아르테스 옥상 (5월 일몰 약 21:20)", 60, "€5.50", link="https://circulobellasartes.com/?p=118688"),
            mv("cba", "botin", "walk", 15, note="알칼라 → 솔 → 마요르 광장 → 쿠치예로스 아치"),
            st("botin", "저녁: Sobrino de Botín — 새끼돼지 통구이 (예약 필수)", 90, "€50–65", link="https://www.timeout.com/madrid/restaurants-and-cafes/el-sobrino-de-botin"),
            mv("botin", hotel, "walk", 12 if hotel == "hotelA_mad" else 11),
        ],
    }


CERC_AVANT = "€1.70 (Avant 표는 Combinado Cercanías 대상이 아니라 유료)"
CERC_AVE = "€0 (AVE 표의 Combinado Cercanías — 출발 4시간 전부터 무료, 표의 코드로 발매기에서 뽑기)"


def madrid_to_atocha(hotel, cercanias_fare=CERC_AVANT):
    if hotel == "hotelA_mad":
        return [mv(hotel, "atocha_station", "walk", 14, note="우에르타스 거리 → 아토차 거리 남쪽. 메트로(안톤 마르틴 1호선 → Atocha 2정거장)도 12분")]
    return [mv(hotel, "sol", "walk", 7),
            mv("sol", "atocha_station", "train", 8, "세르카니아스 C-3/C-4 Atocha 방면", "Sol → Atocha (1정거장, 4분)", cercanias_fare, "메트로로 가면 Callao 3호선 → Sol → 1호선 → Atocha, 20~25분")]


def madrid_day3(hotel):
    return {
        "date": "5/11", "dow": "화", "city": "톨레도", "title": "중세 도시 톨레도 당일치기", "photo": "toledo", "sleep": hotel, "start": "08:10",
        "items": madrid_to_atocha(hotel) + [
            st("atocha_station", "Avant 열차 탑승 (08:50 출발 기준, 예매 시 시간 확정)", 5, note="첫차 06:45. 60일 전 renfe.com 오픈", at="08:40",
               link="https://everyrail.com/trains/madrid-to-toledo/"),
            mv("atocha_station", "toledo_station", "train", 33, "Renfe Avant", "Madrid-Puerta de Atocha → Toledo", "편도 €11–13 (왕복 약 €22)"),
            mv("toledo_station", "zocodover", "bus", 12, "Unauto 61·62번 (또는 5번) 센트로 방면", "역 앞 정류장 (출구에서 오른쪽) → Plaza de Zocodover", "€1.40 기사에게 현금 (unauto.es 1회권)", "걸으면 오르막 20~25분, 택시 €5–7"),
            st("zocodover", "소코도베르 광장", 15, "무료"),
            mv("zocodover", "toledo_cathedral", "walk", 6, note="코메르시오 거리 → 옴브레 데 팔로 거리"),
            st("toledo_cathedral", "톨레도 대성당", 90, "€12 (블로그 기준, 공식 미게시)", link="https://lamaletainquieta.com/catedral-de-toledo/"),
            mv("toledo_cathedral", "el_botero", "walk", 3),
            st("el_botero", "점심: Taberna El Botero — 크로케타 테이스팅", 75, "€30–40", link="https://miraespanha.com/en/where-to-eat-in-toledo/"),
            mv("el_botero", "mirador_valle", "taxi", 10, "", "소코도베르 택시 승강장 → Mirador del Valle", "€8–10 (차량당, 미확인)", "기사에게 20분 기다려 달라고 하거나 Radio Taxi +34 925 255 050"),
            st("mirador_valle", "타호강 건너편 전망대에서 톨레도 전경", 30, "무료"),
            mv("mirador_valle", "toledo_station", "taxi", 12, "", "", "€8–10 (차량당, 미확인)"),
            st("toledo_station", "열차 대기 (17:30경 Avant, 예매 시 확정)", 10, at="17:15"),
            mv("toledo_station", "atocha_station", "train", 33, "Renfe Avant", "Toledo → Madrid-Puerta de Atocha", "편도 €11–13"),
            mv("atocha_station", "sol", "metro", 10, "1호선 Pinar de Chamartín 방면", "Atocha → Sol (4정거장)", M10, "세르카니아스로 가면 4분, €1.70"),
            mv("sol", "casa_labra", "walk", 3),
            st("casa_labra", "저녁: Casa Labra — 대구 튀김·크로케타 (서서 먹는 바)", 50, "€15–25", link="https://www.timeout.es/madrid/es/bares-y-pubs/casa-labra"),
            mv("casa_labra", hotel, "walk", 8 if hotel == "hotelA_mad" else 5),
        ],
    }


def day4_cordoba_sevilla(hotel_mad, hotel_sev):
    return {
        "date": "5/12", "dow": "수", "city": "코르도바 → 세비야", "title": "메스키타 찍고 세비야로", "photo": "mezquita", "sleep": hotel_sev, "start": "06:40",
        "note": "10/28 사고로 마드리드–안달루시아 고속선이 멈춰 있어. 5월에도 안 다니면 마드리드→세비야 국내선으로 바꾸고 코르도바는 빼야 해.",
        "items": madrid_to_atocha(hotel_mad, CERC_AVE) + [
            st("atocha_station", "AVE 07:30 탑승 (보안검색 있어서 15분 전 도착)", 10, at="07:10", link="https://everyrail.com/trains/madrid-to-cordoba/"),
            mv("atocha_station", "cordoba_station", "train", 105, "Renfe AVE / Iryo / OUIGO", "Madrid-Puerta de Atocha → Córdoba", "€9–45 (조기 예매)", "OUIGO는 큰 캐리어 +€5"),
            mv("cordoba_station", "cordoba_lockers", "walk", 3, note="트레스 쿨투라스 광장 건너편 버스터미널"),
            st("cordoba_lockers", "짐 보관소(consigna)에 캐리어 맡기기 (05:00–01:00)", 10, "약 €4–5/개 (미확인)", "동전·카드 준비",
               link="https://www.trvlogue.com/en/cordoba-luggage-storage-lockers"),
            mv("cordoba_lockers", "mezquita", "walk", 25, note="아메리카 대로 → 빅토리아 산책로 → 유대인 지구. 평지 1.8km. 버스 3번은 San Fernando 하차 후 8분이라 이득이 없어"),
            st("mezquita", "메스키타 관람", 90, "€15", "이슬람 사원 안에 성당. 월~토 08:30–09:30은 무료지만 시간상 유료 입장", link="https://www.mezquita-catedraldecordoba.es/en/organiza-la-visita/entradas-y-horarios/"),
            mv("mezquita", "flores", "walk", 2),
            st("flores", "꽃의 골목 · 유대인 지구 골목", 25, "무료"),
            mv("flores", "puente_romano", "walk", 7),
            st("puente_romano", "로마 다리 건너서 메스키타 전경", 20, "무료"),
            mv("puente_romano", "bodegas_campos", "walk", 10, note="론다 데 이사사 → 루카노 거리 → 리네로스 거리"),
            st("bodegas_campos", "점심: Bodegas Campos — 소꼬리 스튜, 살모레호 (전화 예약 +34 957 497 500)", 80, "€40–50", link="https://tablejourney.com/spain/cordoba/restaurants/bodegas-campos/"),
            mv("bodegas_campos", "stop_potro", "walk", 4),
            mv("stop_potro", "cordoba_station", "bus", 14, "Aucorsa 3번 Albaida 방면", "El Potro (La Ribera) → RENFE–Est. Buses", "€1.30 차내 현금·컨택리스", "걸으면 28~30분"),
            st("cordoba_lockers", "짐 찾기 → 역으로", 15),
            st("cordoba_station", "열차 대기 (16:00경 출발, 예매 시 확정)", 5, at="15:45", link="https://www.trenes.com/ave/cordoba-sevilla/"),
            mv("cordoba_station", "santa_justa", "train", 50, "Renfe AVE/Avlo", "Córdoba → Sevilla-Santa Justa", "€7–37"),
            mv("santa_justa", "stop_prado", "bus", 12, "Tussam C1번 Prado de San Sebastián 방면", "역 앞 정류장 → Prado de San Sebastián (종점)", "€1.40 기사에게 현금 또는 차내 카드", "C2는 반대 방향으로 돌아가니 타지 마. 짐 많으면 택시 €10–12"),
            mv("stop_prado", hotel_sev, "walk", 8 if hotel_sev == "hotelA_sev" else 11, note="푸에르타 데 라 카르네 → 산타 마리아 라 블랑카 거리"),
            st(hotel_sev, "체크인 · 휴식", 60),
            mv(hotel_sev, "eme", "walk", 10 if hotel_sev == "hotelA_sev" else 6, note="마테오스 가고 거리"),
            st("eme", "EME 루프탑에서 히랄다 탑 보며 일몰 한 잔 (5월 일몰 약 21:15)", 60, "입장 무료, 음료값", link="https://www.therooftopguide.com/rooftop-bars-in-seville/la-terazza-de-eme-at-eme-catedral-hotel-sevilla.html"),
            mv("eme", "las_teresas", "walk", 7),
            st("las_teresas", "저녁: Las Teresas — 하몬 이베리코 (바 자리)", 60, "약 €25", link="https://www.lonelyplanet.com/articles/best-tapas-restaurants-seville"),
            mv("las_teresas", hotel_sev, "walk", 4 if hotel_sev == "hotelA_sev" else 3),
        ],
    }


def day5_sevilla(hotel_sev):
    a = hotel_sev == "hotelA_sev"
    return {
        "date": "5/13", "dow": "목", "city": "세비야", "title": "알카사르와 플라멩코", "photo": "giralda", "sleep": hotel_sev, "start": "08:45",
        "items": [
            mv(hotel_sev, "alcazar_sev", "walk", 9 if a else 6, note="입장은 트리운포 광장 쪽 '사자의 문'. 반데라스 광장 쪽은 출구"),
            st("alcazar_sev", "세비야 알카사르 (09:30 슬롯)", 120, "€15.50", "30분 단위 시간 지정, 여권 지참. 약 2달 전 오픈", at="09:30",
               link="https://alcazarsevilla.org/wp-content/uploads/2025/02/BOP-ORDENANZA-PATRONATO-2025.pdf"),
            mv("alcazar_sev", "cathedral_sev", "walk", 3, note="출구(반데라스 광장) → 트리운포 광장 남쪽 산 크리스토발 문"),
            st("cathedral_sev", "세비야 대성당 + 히랄다 탑 오르기", 100, "€13 (온라인)", link="https://www.catedraldesevilla.es/en/cultural-visit/schedules-and-rates/"),
            mv("cathedral_sev", "rinconcillo", "walk", 17, note="콘스티투시온 대로 → 시에르페스 거리 → 엔카르나시온 광장 → 헤로나 거리. 버스 이득 없음"),
            st("rinconcillo", "점심: El Rinconcillo (1670년) — 시금치 병아리콩 스튜, 대구 튀김", 70, "€20–30", link="https://www.elrinconcillo.es/history"),
            mv("rinconcillo", hotel_sev, "walk", 17 if a else 16),
            st(hotel_sev, "시에스타 (호텔 루프탑 수영장)", 75),
            mv(hotel_sev, "universidad_sev", "walk", 9 if a else 8, note="무리요 정원 → 산 페르난도 거리"),
            st("universidad_sev", "세비야 대학교 — 옛 왕립 담배공장 (오페라 '카르멘' 배경), 안뜰만 둘러보기", 10, "무료"),
            mv("universidad_sev", "plaza_espana", "walk", 8, note="산 페르난도 거리 → 포르투갈 대로. 트램은 이득 없음"),
            st("plaza_espana", "스페인 광장 (타일 벤치, 운하)", 60, "무료"),
            mv("plaza_espana", "maria_luisa", "walk", 3),
            st("maria_luisa", "마리아 루이사 공원 산책", 25, "무료"),
            mv("maria_luisa", "torre_oro", "walk", 15, note="공원 서쪽 출구 → 과달키비르 강변 산책로(Paseo de las Delicias) 따라 북쪽"),
            st("torre_oro", "황금의 탑 — 13세기 강변 망루, 과달키비르 강 (여행사 코스)", 15, "무료 (해군박물관 €3, 패스)"),
            mv("torre_oro", "plaza_toros", "walk", 8, note="강변 Paseo de Colón 따라"),
            st("plaza_toros", "마에스트란사 투우장 외관 (내부 투어 €10, 시간상 패스)", 10, "무료"),
            mv("plaza_toros", "casa_memoria", "walk", 15, note="아레날 거리 → 시에르페스 거리 → 쿠나 거리"),
            st("casa_memoria", "플라멩코: Casa de la Memoria 19:30 공연 (60분)", 70, "€24", "온라인 예매", at="19:15", link="https://www.ticketlens.com/en/p370860326/seville/casa-de-la-memoria"),
            mv("casa_memoria", "eslava", "walk", 12, note="쿠나 → 알폰소 12세 거리 → 무세오 광장"),
            st("eslava", "저녁: Eslava — 창작 타파스 (예약 없음, 줄 서기)", 80, "€30–40", link="https://www.timeout.com/es/sevilla/bares-y-pubs/eslava"),
            mv("eslava", "setas", "walk", 10, note="알폰소 12세 거리 → 엔카르나시온 광장"),
            st("setas", "세타스 데 세비야(메트로폴 파라솔) 옥상 산책로 야경 — 세계 최대 목조 구조물", 40, "약 €15 (미확인)", "23:00 이후 입장 마감 시간 확인", link="https://setasdesevilla.com/en/"),
            mv("setas", hotel_sev, "walk", 16 if a else 15, note="쿠나 → 시에르페스 → 대성당 옆 → 산타크루스. 밤이면 택시 €7–9"),
        ],
    }


# ───────────────────────── 그라나다 ─────────────────────────
def day6_granada(course, hotel_sev, hotel_gra):
    by_train = course == 1
    if by_train:
        head = [
            mv(hotel_sev, "santa_justa", "taxi", 10, "", "", "€7–8 (차량당)", "이른 아침 짐 들고 버스 환승은 비추"),
            st("santa_justa", "Renfe 07:40 직통 열차 탑승 (2026.11 시간표 기준, 5월 시간표는 60일 전 확인)", 10, at="07:20", link="https://www.omio.es/trenes/sevilla/granada"),
            mv("santa_justa", "granada_station", "train", 165, "Renfe Avant 직통", "Sevilla-Santa Justa → Granada", "€30–48"),
        ]
        start = "06:40"
        arrive = [mv("granada_station", hotel_gra, "taxi", 15, "", "역 앞 택시 승강장", "€7–9 (차량당)", "버스는 4번(Catedral 하차)+C30 환승 35분")] if hotel_gra == "hotelA_gra" else [
            mv("granada_station", "stop_catedral_gra", "bus", 10, "4번 Zaidín(센트로) 방면", "Avda Constitución–Estación Ferrocarril → Catedral", "€1.60, 정류장 기계에서 먼저 구매(4번은 차내 구매 불가)", "택시 €6–8"),
            mv("stop_catedral_gra", hotel_gra, "walk", 7, note="그란 비아 → 누에바 광장 → 아세이투네로스 언덕길")]
    else:
        head = [
            mv(hotel_sev, "plaza_armas", "taxi", 10, "", "", "€7–8 (차량당)", "걸으면 28~30분, 짐 있으면 택시"),
            st("plaza_armas", "ALSA 08:00 버스 탑승 (alsa.com 예매)", 15, at="07:40", link="https://www.omio.es/autobuses/sevilla/granada"),
            mv("plaza_armas", "granada_bus", "bus", 180, "ALSA 고속버스", "Plaza de Armas → Granada 버스터미널", "€21–29"),
        ]
        start = "07:10"
        arrive = [mv("granada_bus", hotel_gra, "taxi", 15, "", "", "€8–11 (차량당)", "버스 33번 → Catedral 25분 + 도보 7분도 가능")]
    a = hotel_gra == "hotelA_gra"
    to_centre = ([mv("hotelA_gra", "generalife_stop", "walk", 4), mv("generalife_stop", "plaza_isabel", "bus", 12, "C30번 센트로 방면", "Alhambra–Generalife 2 → Plaza Isabel la Católica", GRA_BUS, "12분 간격"), mv("plaza_isabel", "plaza_nueva_gra", "walk", 2)]
                 if a else [mv("hotelB_gra", "plaza_nueva_gra", "walk", 3)])
    back = ([mv("morayma", "hotelA_gra", "taxi", 12, "", "", "€7–8 (차량당)", "'Hotel Alixares, Paseo de la Sabica'라고 말하기")]
            if a else [mv("morayma", "hotelB_gra", "walk", 14, note="차피스 언덕 → 트리스테스 산책로 → 다로 강변 → 누에바 광장 (미확인)")])
    hammam = [mv("plaza_nueva_gra", "hammam", "walk", 2),
              st("hammam", "아랍식 목욕탕 Hammam Al Ándalus (90분 + 마사지 15분)", 110, "€65", "시간대별 가격 변동, 예약 필수", link="https://www.granadadirect.com/ocio/banos-arabes/")] if course != 2 else [
              mv("plaza_nueva_gra", "hammam", "walk", 2),
              st("hammam", "(코스 2는 하맘 생략) 누에바 광장 주변 카페에서 휴식", 60, "약 €5")]
    return {
        "date": "5/14", "dow": "금", "city": "그라나다", "title": "하맘에서 쉬고 알바이신 일몰" if course != 2 else "알바이신 일몰", "photo": "alhambra_view", "sleep": hotel_gra, "start": start,
        "items": head + arrive + [st(hotel_gra, "체크인 · 짐 풀기 · 가벼운 점심", 60)] + to_centre + hammam + [
            mv("plaza_nueva_gra", "plaza_larga", "bus", 12, "C31번 알바이신 방면", "Plaza Nueva → Plaza Larga (기사에게 'San Nicolás' 말하기)", GRA_BUS, "걸으면 칼데레리아 누에바 거리로 오르막 20~30분"),
            mv("plaza_larga", "san_nicolas", "walk", 6, note="아르코 데 라스 페사스 통과"),
            st("san_nicolas", "산 니콜라스 전망대 — 알함브라 일몰 (5월 일몰 약 21:10)", 70, "무료", at="20:15"),
            mv("san_nicolas", "morayma", "walk", 9, note="산 아구스틴 길 → 차피스 언덕 내리막 (미확인)"),
            st("morayma", "저녁: Mirador de Morayma — 알함브라 뷰 테라스 (전화 예약 +34 958 22 82 90)", 90, "€40–55", link="https://en.andalucia.org/listing/mirador-de-morayma/5461101/"),
        ] + back,
    }


def alhambra_morning(hotel_gra):
    if hotel_gra == "hotelA_gra":
        return [mv("hotelA_gra", "generalife_stop", "walk", 5, note="파세오 데 라 사비카 따라 매표소(Access Pavilion)까지")]
    return [mv("hotelB_gra", "plaza_isabel", "walk", 3),
            mv("plaza_isabel", "generalife_stop", "bus", 12, "C30번 알함브라 방면", "Plaza Isabel la Católica → Alhambra–Generalife 2 (종점)", GRA_BUS, "8~12분 간격, 첫차 약 07:00. 걸으면 고메레스 언덕길 20~30분")]


def alhambra_block():
    return [
        st("generalife_stop", "알함브라 입장 (08:30 개장과 동시에). 티켓 바코드 + 여권 원본", 10, "€22.27 (온라인) + 수수료", "환불·변경 불가, 여권 이름과 동일하게. 여행사들은 3개월 전 구매 안내, 온라인은 전날 23:59까지", at="08:25", link="https://tickets.alhambra-patronato.es/en/?p=3090"),
        st("generalife_stop", "헤네랄리페 정원", 45, note="입구 바로 옆"),
        mv("generalife_stop", "alcazaba", "walk", 18, note="파세오 데 라스 토레스 따라 서쪽"),
        st("alcazaba", "알카사바 요새 · 벨라 탑 전망", 35),
        mv("alcazaba", "nasrid", "walk", 4),
        st("nasrid", "나스르 궁전 (티켓에 찍힌 시간 정각 입장, 10:30 슬롯 기준)", 75, note="10분 전에 궁전 입구 줄에 서기. 늦으면 입장 거부", at="10:20"),
        mv("nasrid", "carlos_v", "walk", 2),
        st("carlos_v", "카를로스 5세 궁전 — 르네상스 원형 안뜰 (알함브라 박물관 무료, 여행사 투어 코스)", 15, "무료"),
        mv("carlos_v", "stop_carlos_v", "walk", 2),
        mv("stop_carlos_v", "plaza_isabel", "bus", 11, "C30번 센트로 방면", "Palacio de Carlos V → Plaza Isabel la Católica", GRA_BUS, "걸으면 고메레스 언덕 내리막 15분"),
        mv("plaza_isabel", "diamantes", "walk", 6, note="레예스 카톨리코스 거리 → 나바스 거리"),
        st("diamantes", "점심: Los Diamantes — 음료마다 타파스 무료, 튀긴 생선·새우", 50, "€15–25", link="https://andalucia.com/cities/granada/tapas.htm"),
    ]


def day7_to_barcelona(hotel_gra, hotel_bcn):
    a = hotel_gra == "hotelA_gra"
    bags = ([mv("diamantes", "hotelA_gra", "taxi", 8, "", "", "€7 (차량당, 토요일 할증 요금)", "C30으로 가도 됨"),
             st("hotelA_gra", "짐 찾기 (아침에 로비에 맡겨 두기)", 10),
             mv("hotelA_gra", "generalife_stop", "walk", 4),
             mv("generalife_stop", "plaza_isabel", "bus", 12, "C30번 센트로 방면", "Alhambra–Generalife 2 → Plaza Isabel la Católica", GRA_BUS),
             mv("plaza_isabel", "stop_catedral_gra", "walk", 4)]
            if a else
            [mv("diamantes", "hotelB_gra", "walk", 8),
             st("hotelB_gra", "짐 찾기", 15),
             mv("hotelB_gra", "stop_catedral_gra", "walk", 6, note="그란 비아 대성당 앞 정류장")])
    bcn_hotel_walk = 9 if hotel_bcn == "hotelA_bcn" else 4
    return {
        "date": "5/15", "dow": "토", "city": "그라나다 → 바르셀로나", "title": "알함브라, 그리고 지중해로", "photo": "leones", "sleep": hotel_bcn, "start": "07:40" if a else "07:45",
        "items": alhambra_morning(hotel_gra) + alhambra_block() + bags + [
            st("stop_catedral_gra", "Alsa 245번 공항버스 탑승 (13:30–14:00 통과편, 시간표 alsa.es '0245' 확인)", 10, "€3.10 차내 결제", "주말엔 Av. Constitución 쪽에 설 때가 있으니 정류장에서 확인. 택시는 €30–35", at="13:40",
               link="https://lovegranada.com/buses/airport-bus"),
            mv("stop_catedral_gra", "grx", "bus", 50, "Alsa 0245 Aeropuerto 방면", "Catedral → Aeropuerto", "€3.10"),
            st("grx", "부엘링 체크인·보안검색 (16:30경 출발 기준, 하루 4편 09:05~22:55 중 예매 시 확정)", 90, "항공권 €41부터 (5월 초 편도) + 위탁수하물 25kg 웹 €18–99", "수하물은 예매 때 같이 사기 (공항에서 사면 €50–160). 1인 1캐리어", link="https://www.vueling.com/en/vueling-services/prepare-your-trip/luggage"),
            mv("grx", "bcn_t1", "plane", 86, "Vueling", "GRX → BCN T1"),
            st("bcn_t1", "수하물 찾기 → T1 도착층 'Aerobús' 표지 따라 이동", 25),
            mv("bcn_t1", "aerobus_catalunya", "bus", 35, "Aerobús A1 (T1 전용, A2 타지 말 것)", "T1 → Plaça de Catalunya", "편도 €7.45 · 왕복 €12.85 (90일 유효, 왕복권 사기)", "정류장 발매기·차내·앱 카드 결제. 5~10분 간격"),
            mv("aerobus_catalunya", hotel_bcn, "walk", bcn_hotel_walk, note="포르탈 데 랑헬 거리 → 아르크스 거리" if hotel_bcn == "hotelA_bcn" else "광장 건너 펠라이 거리"),
            st(hotel_bcn, "체크인", 30),
            mv(hotel_bcn, "cal_pep", "walk", 11 if hotel_bcn == "hotelA_bcn" else 21, note="라이에타나 대로 → 아르헨테리아 거리"),
            st("cal_pep", "저녁: Cal Pep — 대구 오믈렛, 바지락 (카운터 예약 불가, 줄 서기)", 80, "€50–70", link="https://guia.barcelona.cat/en/detall/bar-restaurant-cal-pep_75990095014.html"),
            mv("cal_pep", hotel_bcn, "walk", 11 if hotel_bcn == "hotelA_bcn" else 21),
        ],
    }


def day7_parador():
    return {
        "date": "5/15", "dow": "토", "city": "그라나다", "title": "알함브라 데이, 성벽 안에서 하룻밤", "photo": "leones", "sleep": "parador", "start": "07:45",
        "items": alhambra_morning("hotelB_gra") + alhambra_block() + [
            mv("diamantes", "hotelB_gra", "walk", 8),
            st("hotelB_gra", "짐 찾기", 15),
            mv("hotelB_gra", "plaza_nueva_gra", "walk", 3),
            mv("plaza_nueva_gra", "parador", "taxi", 10, "", "누에바 광장 택시 승강장 → Parador", "€7 (차량당, 토요일 요금)", "알함브라 차단기에서 예약 확인증 보여주면 통과"),
            st("parador", "파라도르 체크인 · 관람객 빠진 성벽 안 산책 · 정원", 300, note="15세기 수도원 개조, 객실 40개"),
            mv("parador", "stop_carlos_v", "walk", 3),
            mv("stop_carlos_v", "plaza_isabel", "bus", 11, "C30번 센트로 방면", "Palacio de Carlos V → Plaza Isabel la Católica", GRA_BUS),
            mv("plaza_isabel", "plaza_nueva_gra", "walk", 2),
            st("plaza_nueva_gra", "저녁: 누에바 광장 주변 타파스 바 (음료 시키면 타파스 무료)", 80, "€15–25"),
            mv("plaza_nueva_gra", "venta_gallo", "bus", 15, "C34번 사크로몬테 방면", "Plaza Nueva → Camino del Sacromonte (Barranco de los Negros 근처, 정류장명 미확인) + 오르막 5분", GRA_BUS, "15~20분 간격. 택시 €10"),
            st("venta_gallo", "사크로몬테 동굴 플라멩코 Venta El Gallo 21:15 공연", 75, "€25 (공연만)", at="21:00", link="https://www.granadadirect.com/ocio/flamenco-granada/"),
            mv("venta_gallo", "parador", "taxi", 12, "", "식당에서 택시 불러 줌", "€10 (차량당, 야간 요금)", "C34 심야 운행 미확인이라 택시. 파라도르 투숙객 차량 통과"),
        ],
    }


# ───────────────────────── 바르셀로나 ─────────────────────────
def day8_gaudi(hotel_bcn):
    a = hotel_bcn == "hotelA_bcn"
    first = ([mv("hotelA_bcn", "jaume_i", "walk", 4),
              mv("jaume_i", "verdaguer", "metro", 8, "L4 Trinitat Nova 방면", "Jaume I → Verdaguer (3정거장)", T_CASUAL, "Verdaguer에서 L5로 짧은 환승. Passeig de Gràcia 환승은 통로가 길어 피하기"),
              mv("verdaguer", "sagrada_metro", "metro", 4, "L5 Vall d'Hebron 방면", "Verdaguer → Sagrada Família (1정거장)", "환승 무료 (75분 내)")]
             if a else
             [mv("hotelB_bcn", "pg_gracia_metro", "walk", 8, note="그란 비아 쪽 입구"),
              mv("pg_gracia_metro", "sagrada_metro", "metro", 6, "L2 Badalona Pompeu Fabra 방면", "Passeig de Gràcia → Sagrada Família (2정거장)", T_CASUAL, "Catalunya L1은 사그라다에 안 가")])
    return {
        "date": "5/16", "dow": "일", "city": "바르셀로나", "title": "하루 종일 가우디", "photo": "park_guell", "sleep": hotel_bcn, "start": "08:30",
        "items": first + [
            mv("sagrada_metro", "sagrada", "walk", 3, note="마리나 거리 쪽 출구. 개인 티켓 입장은 탄생의 파사드(마리나 거리) 쪽"),
            st("sagrada", "사그라다 파밀리아 09:00 슬롯 (탑 포함)", 120, "€36 (서드파티 가이드 기준)", "일요일 운영시간 예매 때 확인", at="09:00", link="https://www.artvisitguide.com/sagrada-familia-2026-tower-jesus-tickets/"),
            mv("sagrada", "sagrada_metro", "walk", 3),
            mv("sagrada_metro", "pg_gracia_metro", "metro", 6, "L2 Paral·lel 방면", "Sagrada Família → Passeig de Gràcia (2정거장)", T_CASUAL, "걸으면 마요르카 거리로 25분"),
            mv("pg_gracia_metro", "casa_batllo", "walk", 2),
            st("casa_batllo", "카사 바트요 12:00 슬롯", 80, "€35~ (다이내믹 가격)", "늦게 살수록 비쌈", at="12:00", link="https://barcelonahacks.com/is-casa-batllo-worth-it/"),
            mv("casa_batllo", "casa_mila", "walk", 7, note="그라시아 거리 따라 북쪽 (92번지)"),
            st("casa_mila", "카사 밀라(라 페드레라) 외관 — 물결치는 석조 파사드 (내부 €28·시간상 외관만, 여행사 투어도 외부 관람)", 12, "무료"),
            mv("casa_mila", "cerveceria", "walk", 4, note="프로벤사 거리 → 마요르카 거리"),
            st("cerveceria", "점심: Cervecería Catalana — 타파스·몬타디토 (줄 서는 곳)", 65, "€25–35", link="https://barcelonanavigator.com/cerveceria-catalana/"),
            mv("cerveceria", "bus24_stop", "walk", 3),
            mv("bus24_stop", "park_guell", "bus", 30, "24번 El Carmel 방면", "Pg. de Gràcia–Rosselló → Ctra. del Carmel–Albert Llanas (바로 앞 정류장은 C N Catalunya–Park Güell)", T_CASUAL, "카르멜 도로 23번 입구 150m 앞에 내려줘서 오르막이 없어. 메트로 L3 Vallcarca는 오르막 15~20분"),
            st("park_guell", "구엘 공원 15:30 슬롯", 100, "€18", "30분 넘게 늦으면 입장 불가", at="15:30", link="https://parkguell.barcelona/en/planning-your-visit/prices-and-times"),
            mv("park_guell", "bunkers", "walk", 23, note="카르멜 도로 → 마리아 라베르니아 거리, 오르막. 24번 버스 2~3정거장 'Doctor Bové–Gran Vista' 하차 후 5~8분도 가능"),
            st("bunkers", "벙커 델 카르멜 360° 전망 (19:30 폐쇄, 일몰은 못 봄)", 40, "무료", link="https://www.trvlogue.com/en/bunkers-del-carmel-barcelona"),
            mv("bunkers", "alfons_x", "walk", 23, note="가파른 내리막. 해질녘이면 택시 €12–15가 편해"),
            mv("alfons_x", "barceloneta_metro", "metro", 12, "L4 La Pau 방면", "Alfons X → Barceloneta (6정거장)", T_CASUAL),
            mv("barceloneta_metro", "set_portes", "walk", 3),
            st("set_portes", "저녁: 7 Portes (1836년) — 해산물 빠에야 Arròs Parellada (이메일 예약 reserves@7portes.com)", 90, "€45–60", link="https://barcelonanavigator.com/restaurant-7-portes/"),
            mv("set_portes", hotel_bcn, "walk", 13 if a else 25, note="라이에타나 대로" if a else "L4 Barceloneta → Urquinaona 2정거장 + 도보 6분도 가능"),
        ],
    }


def day9_montserrat(hotel_bcn):
    a = hotel_bcn == "hotelA_bcn"
    first = ([mv("hotelA_bcn", "liceu", "walk", 8, note="페란 거리 → 람블라"),
              mv("liceu", "espanya_fgc", "metro", 9, "L3 Zona Universitària 방면", "Liceu → Espanya (4정거장)", "Trans Montserrat 통합권에 포함")]
             if a else
             [mv("hotelB_bcn", "catalunya_metro", "walk", 2),
              mv("catalunya_metro", "espanya_fgc", "metro", 8, "L1 Hospital de Bellvitge 방면", "Catalunya → Espanya (3정거장)", "Trans Montserrat 통합권에 포함")])
    return {
        "date": "5/17", "dow": "월", "city": "몬세라트 → 바르셀로나", "title": "바위산 수도원, 작별의 밤", "photo": "montserrat", "sleep": hotel_bcn, "start": "07:30",
        "items": first + [
            st("espanya_fgc", "FGC 안내소(Punt d'Acollida)에서 Trans Montserrat 통합권 구매 → R5 플랫폼 ('FGC' 표지 따라)", 20, "€50 (메트로 왕복 + R5 왕복 + 산악열차 + 푸니쿨라)", "온라인으로 미리 사도 됨. T-casual로는 못 가", at="08:05",
               link="https://www.fgc.cat/en/fgc-faq/what-are-the-conditions-prices-and-discounts-children-students-for-the-transmontserrat-combined-ticket-and-how-can-date-changes-be-managed/"),
            mv("espanya_fgc", "monistrol", "train", 65, "FGC R5 Manresa 방면 08:36 출발 (매시 :36, 가이드 기준·fgc.cat 확인)", "Plaça d'Espanya → Monistrol de Montserrat", "통합권 포함"),
            mv("monistrol", "montserrat", "rack", 20, "Cremallera 산악열차", "Monistrol de Montserrat → Montserrat", "통합권 포함", "케이블카(Aeri)를 타려면 한 정거장 전 Montserrat-Aeri 하차, 요금 별도"),
            st("montserrat", "수도원 · 바실리카 · 검은 성모상 (줄 30분 예상)", 90, "무료"),
            mv("montserrat", "sant_joan", "funicular", 6, "Sant Joan 푸니쿨라", "하부역 → 상부역", "통합권 포함"),
            st("sant_joan", "산 조안 상부 능선 산책 · 전망", 60, note="Santa Cova 푸니쿨라는 2026.11 현재 운행 중단(turistren.cat), 출발 전 확인"),
            mv("sant_joan", "montserrat", "funicular", 6, "Sant Joan 푸니쿨라", "상부역 → 하부역", "통합권 포함"),
            st("montserrat", "점심: 수도원 옆 카페테리아 (간단히)", 45, "€15–20 (추정)"),
            mv("montserrat", "monistrol", "rack", 20, "Cremallera 산악열차", "", "통합권 포함"),
            mv("monistrol", "espanya_fgc", "train", 65, "FGC R5 Barcelona 방면 (오후 매시)", "Monistrol → Plaça d'Espanya", "통합권 포함"),
            mv("espanya_fgc", "liceu" if a else "catalunya_metro", "metro", 9 if a else 8, "L3 Trinitat Nova 방면" if a else "L1 Fondo 방면", "Espanya → Liceu" if a else "Espanya → Catalunya", "통합권 포함"),
            mv("liceu" if a else "catalunya_metro", hotel_bcn, "walk", 8 if a else 2),
            st(hotel_bcn, "휴식 · 루프탑 수영장" if a else "휴식", 150),
            mv(hotel_bcn, "port_vell", "walk", 16 if a else 24, note="라이에타나 대로 → 콜럼버스 기념탑 → 모이 데 라 푸스타 (선착장은 예약 바우처 확인)"),
            st("port_vell", "선셋 세일링 — 범선 타고 지중해에서 보는 바르셀로나 (여행사 허니문 특전 코스, 1.5~2시간)", 120, "약 €45–60 (미확인)", "GetYourGuide·Civitatis '바르셀로나 선셋 세일링'으로 예약. 5월 일몰 약 21:05", at="18:30"),
            mv("port_vell", "xampanyet", "walk", 9, note="팔라우 광장 → 몬카다 거리"),
            st("xampanyet", "작별 디너: 보른 지구 타파스 바 호핑 (El Xampanyet은 월요일 휴무라 주변 바)", 120, "€40–60"),
            mv("xampanyet", hotel_bcn, "walk", 10 if a else 20),
        ],
    }


def day10_bcn(hotel_bcn):
    a = hotel_bcn == "hotelA_bcn"
    return {
        "date": "5/18", "dow": "화", "city": "바르셀로나 → 인천", "title": "보른 산책하고 귀국", "photo": "gothic", "sleep": None, "start": "09:30",
        "items": [
            st(hotel_bcn, "체크아웃, 짐은 호텔에 맡기기", 20),
            mv(hotel_bcn, "boqueria", "walk", 7 if a else 5, note="포르타페리사 거리 → 람블라" if a else "람블라 따라 남쪽"),
            st("boqueria", "보케리아 시장 — 생과일 주스·하몬 한 컵 (여행사 자유일정 추천 1순위)", 35, "€5–10", link="https://www.boqueria.barcelona/"),
            mv("boqueria", "bcn_cathedral", "walk", 7, note="포르타페리사 거리 → 비스베 거리 (비스베 다리)"),
            st("bcn_cathedral", "바르셀로나 대성당 · 고딕 지구 골목", 30, "무료 (평일 12:30 전 예배 시간. 관광 입장 €11, 미확인)"),
            mv("bcn_cathedral", "xampanyet", "walk", 8, note="자우메 1세 광장 → 아르헨테리아 거리 → 몬카다 거리"),
            st("xampanyet", "보른 지구·피카소 미술관 골목 산책 후 점심: El Xampanyet — 멸치·카바 (12:00 오픈)", 110, "€20–30", at="11:00", link="https://barcelonanavigator.com/el-xampanyet/"),
            mv("xampanyet", "barceloneta_beach", "walk", 20, note="보른 산책로 → 팔라우 광장 → 조안 데 보르보 산책로"),
            st("barceloneta_beach", "바르셀로네타 해변에서 마지막 지중해", 60, "무료"),
            mv("barceloneta_beach", hotel_bcn, "walk", 25 if a else 35, note="L4 Barceloneta → Jaume I/Urquinaona도 가능"),
            st(hotel_bcn, "짐 찾기", 15),
            mv(hotel_bcn, "aerobus_catalunya", "walk", 8 if a else 3, note="엘 코르테 잉글레스 앞, 그라시아 거리 건너편 정류장. 'A1 / T1' 표시 확인"),
            st("aerobus_catalunya", "Aerobús A1 탑승 (17:45까지)", 5, "5/15에 산 왕복권 사용", at="17:40"),
            mv("aerobus_catalunya", "bcn_t1", "bus", 40, "Aerobús A1", "Plaça de Catalunya → T1", "왕복권"),
            st("bcn_t1", "체크인·출국 (20:50 출발, 코스 1은 카타르 16:35 출발이라 전체를 3시간 앞당기고 대성당·해변은 생략)", 150, note="다구간 귀국편은 예매 시 시간 확정"),
        ],
    }


# ───────────────────────── 코스 3 마드리드 후반 ─────────────────────────
def day8_back_to_madrid():
    return {
        "date": "5/16", "dow": "일", "city": "그라나다 → 마드리드", "title": "다시 마드리드로, 그란 비아의 저녁", "photo": "cibeles", "sleep": "hotelB_mad", "start": "08:30",
        "note": "고속선이 5월에도 멈춰 있으면 Iberia 직항(약 1시간 10분, $30–85)으로 바꿔.",
        "items": [
            st("parador", "파라도르 정원 아침 산책 · 체크아웃", 60),
            mv("parador", "granada_station", "taxi", 15, "", "리셉션에서 택시 호출", "€9–10 (차량당, 일요일 요금)", "버스는 C30 → Catedral 도보 → 4번, 약 40분"),
            st("granada_station", "AVE 11:04 탑승 (2026.11 시간표 기준, renfe.com 확인)", 20, at="10:30", link="https://everyrail.com/trains/madrid-to-granada/"),
            mv("granada_station", "atocha_station", "train", 214, "Renfe AVE 직통", "Granada → Madrid-Puerta de Atocha (14:38 도착)", "€23–30 (조기 예매)"),
            mv("atocha_station", "sol", "train", 6, "세르카니아스 C-3/C-4 Chamartín 방면", "Atocha → Sol (1정거장, 4분)", "€0 (AVE 표의 Combinado Cercanías — 도착 후 4시간 안에 무료)", "택시는 역 승차 최소 €8"),
            mv("sol", "hotelB_mad", "walk", 7),
            st("hotelB_mad", "체크인 · 휴식", 60),
            mv("hotelB_mad", "cibeles", "walk", 18, note="카야오 → 그란 비아 동쪽 끝 → 알칼라 거리"),
            st("cibeles", "시벨레스 광장 · 우체국 궁전 전망대(선택)", 40, "무료 (전망대 €3, 미확인)"),
            mv("cibeles", "la_latina", "metro", 20, "2호선 Cuatro Caminos 방면 → Ópera에서 5호선 Casa de Campo 방면", "Banco de España → Ópera (3정거장) → La Latina (1정거장)", M10, "걸으면 솔·마요르 광장 거쳐 25분"),
            mv("la_latina", "casa_lucio", "walk", 3),
            st("casa_lucio", "저녁: Casa Lucio — 우에보스 에스트레야도스 (20:30 오픈)", 90, "€45–60", at="20:30", link="https://www.timeout.es/madrid/es/restaurantes-y-cafes/casa-lucio"),
            mv("casa_lucio", "la_latina", "walk", 3),
            mv("la_latina", "callao", "metro", 5, "5호선 Alameda de Osuna 방면", "La Latina → Callao (2정거장)", M10, "걸으면 16분"),
            mv("callao", "hotelB_mad", "walk", 2),
        ],
    }


def day9_segovia():
    return {
        "date": "5/17", "dow": "월", "city": "세고비아", "title": "로마 수도교와 알카사르, 세고비아 당일치기", "photo": "segovia_aq", "sleep": "hotelB_mad", "start": "08:00",
        "items": [
            mv("hotelB_mad", "sol", "walk", 7),
            mv("sol", "chamartin", "train", 14, "세르카니아스 C-4 (또는 C-3) Chamartín 방면", "Sol → Chamartín-Clara Campoamor (2정거장)", CERC_AVANT, "메트로로는 Callao 5호선 → Alonso Martínez → 10호선, 30분"),
            st("chamartin", "Avant 09:00대 열차 탑승 (예매 시 확정)", 15, at="08:40", link="https://www.omio.com.ar/trenes/madrid-chamartin/segovia-guiomar-ashif"),
            mv("chamartin", "guiomar", "train", 27, "Renfe Avant/Alvia", "Madrid-Chamartín → Segovia-Guiomar", "편도 €19.70부터"),
            mv("guiomar", "acueducto", "bus", 15, "Urbanos de Segovia 11번 Acueducto 방면", "역 앞 정류장 → Acueducto", "€2.25 기사에게 (AVE역 연결 11·12번 전용 요금)", "12번은 버스터미널로 가니 타지 마"),
            st("acueducto", "로마 수도교 (아소게호 광장)", 40, "무료"),
            mv("acueducto", "segovia_cathedral", "walk", 12, note="레알 거리 오르막"),
            st("segovia_cathedral", "세고비아 대성당", 60, "€4 (탑 포함 패키지 €10)", link="https://lamaletainquieta.com/?p=9365"),
            mv("segovia_cathedral", "candido", "walk", 12, note="레알 거리 내리막"),
            st("candido", "점심: Mesón de Cándido — 코치니요(새끼돼지 통구이), 수도교 바로 앞 (예약 권장)", 90, "€45–60", link="https://gastroranking.es/r/meson-de-candido_186/"),
            mv("candido", "alcazar_segovia", "walk", 22, note="레알 거리 → 마요르 광장 → 마르케스 델 아르코 거리"),
            st("alcazar_segovia", "알카사르 + 후안 2세 탑 (4~10월 10:00–19:30)", 90, "€10 (탑 포함)", "탑은 표 살 때 같이 선택", link="https://lamaletainquieta.com/alcazar-segovia/"),
            mv("alcazar_segovia", "guiomar", "taxi", 14, "", "마요르 광장 또는 수도교 앞 승강장", "€10–12 (차량당, 미확인)", "걸어서 수도교(20분) → 11번 버스(15분)도 가능"),
            st("guiomar", "열차 대기 (18:30경 Avant, 예매 시 확정)", 15, at="18:10"),
            mv("guiomar", "chamartin", "train", 27, "Renfe Avant", "Segovia-Guiomar → Madrid-Chamartín", "편도 €19.70부터"),
            mv("chamartin", "sol", "train", 14, "세르카니아스 C-4 Sol 방면", "Chamartín → Sol", "€1.70"),
            st("sol", "마지막 밤: 솔·라스 레트라스 지구 바 호핑 (Casa Labra 재방문도 좋아)", 90, "€20–30"),
            mv("sol", "hotelB_mad", "walk", 7),
        ],
    }


def day10_madrid():
    return {
        "date": "5/18", "dow": "화", "city": "마드리드 → 인천", "title": "레티로 산책하고 저녁 귀국", "photo": "retiro", "sleep": None, "start": "09:30",
        "items": [
            st("hotelB_mad", "체크아웃, 짐은 호텔에 맡기기", 20),
            mv("hotelB_mad", "sol", "walk", 7),
            mv("sol", "retiro_metro", "metro", 8, "2호선 Las Rosas 방면", "Sol → Retiro (3정거장)", M10, "그란 비아·알칼라 거리로 걸으면 23분"),
            mv("retiro_metro", "palacio_cristal", "walk", 15, note="알칼라 문 → 아르헨티나 산책로"),
            st("palacio_cristal", "레티로 공원 · 크리스탈 궁전 · 호수", 90, "무료"),
            mv("palacio_cristal", "retiro_metro", "walk", 15),
            mv("retiro_metro", "sol", "metro", 8, "2호선 Cuatro Caminos 방면", "Retiro → Sol", M10),
            st("sol", "점심: 솔 광장 근처 타파스 · 기념품 (산 미겔 시장도 7분)", 120, "€15–25"),
            mv("sol", "hotelB_mad", "walk", 7),
            st("hotelB_mad", "짐 찾기, 호텔에서 택시 호출", 15),
            mv("hotelB_mad", "mad_t1", "taxi", 35, "", "", "€33 (차량당 정액, M-30 안쪽 ↔ 공항)", "메트로는 Callao 5호선 → Alonso Martínez 10호선 → Nuevos Ministerios 8호선 → Aeropuerto T1-T2-T3, 50분 + €0.73 + 공항 할증 €3. 대한항공은 T1 (Aena 기준)"),
            st("mad_t1", "체크인·출국 (20:00 출발, 대한항공 T1)", 150),
        ],
    }


# ───────────────────────── 코스별 1일차 ─────────────────────────
def day1(course, hotel):
    if course == 1:
        return {
            "date": "5/9", "dow": "일", "city": "마드리드", "title": "경유 끝, 마드리드 첫 저녁", "photo": "plaza_mayor", "sleep": hotel, "start": "14:15",
            "items": [
                st("mad_t4", "카타르항공 도착 (14:15). 입국심사 EES 얼굴·지문 등록 → 수하물", 60),
                st("mad_t4", "메트로 8호선 매표기: Multi 카드 €2.50 + 1회권 + '공항 할증' 구매 (1인 1장)", 10, "Multi 카드 €2.50 + 1회권 €1.50~2 + 공항 할증 €3",
                   link="https://crtm.es/billetes-transporte-publico-aeropuerto-madrid"),
                mv("mad_t4", "nuevos_ministerios", "metro", 20, "8호선 Nuevos Ministerios 방면", "Aeropuerto T4 → Nuevos Ministerios (종점)", "위 1회권"),
                mv("nuevos_ministerios", "tribunal", "metro", 8, "10호선 Puerta del Sur 방면", "Nuevos Ministerios → Tribunal (3정거장)", "환승 무료"),
                mv("tribunal", "anton_martin", "metro", 9, "1호선 Valdecarros 방면", "Tribunal → Antón Martín (4정거장)", "환승 무료", "짐이 무거우면 택시 €33 정액(25~40분)"),
                mv("anton_martin", "hotelA_mad", "walk", 4, note="아토차 거리 → 우에르타스 거리"),
                st("hotelA_mad", "체크인 · 샤워 · 휴식", 150),
                mv("hotelA_mad", "sol", "walk", 6),
                st("sol", "솔 광장 (0km 표지, 곰 동상)", 20, "무료"),
                mv("sol", "plaza_mayor", "walk", 5, note="마요르 거리"),
                st("plaza_mayor", "마요르 광장 저녁 산책", 30, "무료"),
                mv("plaza_mayor", "casa_labra", "walk", 5, note="포스타스 거리 → 솔 북쪽 테투안 거리"),
                st("casa_labra", "첫 저녁: Casa Labra (1860년) — 대구 튀김, 크로케타. 22:30까지", 50, "€15–25", link="https://www.timeout.es/madrid/es/bares-y-pubs/casa-labra"),
                mv("casa_labra", "hotelA_mad", "walk", 8),
            ],
        }
    return {
        "date": "5/9", "dow": "일", "city": "마드리드", "title": "직항으로 도착, 가볍게 첫 저녁", "photo": "plaza_mayor", "sleep": hotel, "start": "18:00",
        "items": [
            st("mad_t1", "대한항공 도착 (18:00, T1 — Aena 항공사 목록 기준. 아시아나는 마드리드 취항 없음, 바르셀로나행이라 항공권 확인). 입국심사 EES 등록 → 수하물", 60),
            mv("mad_t1", "hotelB_mad", "taxi", 35, "", "도착층 공식 택시 승강장, '타리파 피하 아에로푸에르토'", "€33 (차량당 정액, 카드 가능)", "메트로는 8호선 → 10호선 Alonso Martínez → 5호선 Callao, 45~50분 + €1.50~2 + 할증 €3"),
            st("hotelB_mad", "체크인 · 짐 풀기", 40),
            mv("hotelB_mad", "sol", "walk", 7, note="카야오 → 프레시아도스 거리"),
            st("sol", "솔 광장 (0km 표지, 곰 동상)", 15, "무료"),
            mv("sol", "plaza_mayor", "walk", 5, note="마요르 거리"),
            st("plaza_mayor", "마요르 광장 저녁 산책", 25, "무료"),
            mv("plaza_mayor", "casa_labra", "walk", 5),
            st("casa_labra", "첫 저녁: Casa Labra (1860년) — 대구 튀김, 크로케타. 22:30 마감이라 서둘러", 45, "€15–25", link="https://www.timeout.es/madrid/es/bares-y-pubs/casa-labra"),
            mv("casa_labra", "hotelB_mad", "walk", 5),
            st("hotelB_mad", "메트로 Callao역 매표기에서 내일 쓸 Multi 카드 €2.50 + 10회권 €7.30 구매 (1인 1장)", 10, "€9.80", link="https://crtm.es/media/s1qi0nmo/bocm-20251231-precios_transporte.pdf"),
        ],
    }


def build_course(course):
    hm = "hotelA_mad" if course == 1 else "hotelB_mad"
    hs = "hotelB_sev" if course == 2 else "hotelA_sev"
    hg = "hotelA_gra" if course == 1 else "hotelB_gra"
    hb = "hotelA_bcn" if course == 1 else "hotelB_bcn"
    days = [day1(course, hm), madrid_day2(hm), madrid_day3(hm), day4_cordoba_sevilla(hm, hs), day5_sevilla(hs), day6_granada(course, hs, hg)]
    if course in (1, 2):
        days += [day7_to_barcelona(hg, hb), day8_gaudi(hb), day9_montserrat(hb), day10_bcn(hb)]
    else:
        days += [day7_parador(), day8_back_to_madrid(), day9_segovia(), day10_madrid()]
    return days


def add_times(day):
    """start 시각부터 순서대로 시각을 계산한다. at이 있으면 그 시각으로 건너뛴다."""
    h, m = map(int, day["start"].split(":"))
    cursor = h * 60 + m
    out = []
    for it in day["items"]:
        if it["kind"] == "stop" and it.get("at"):
            ah, am = map(int, it["at"].split(":"))
            fixed = ah * 60 + am
            if fixed > cursor:
                it = dict(it, wait=fixed - cursor)
                cursor = fixed
        it = dict(it, time="%02d:%02d" % (cursor // 60 % 24, cursor % 60))
        cursor += it["mins"] if it["kind"] == "move" else it["dur"]
        out.append(it)
    day = dict(day, items=out, end="%02d:%02d" % (cursor // 60 % 24, cursor % 60))
    return day


COURSES = {c: [add_times(d) for d in build_course(c)] for c in (1, 2, 3)}
