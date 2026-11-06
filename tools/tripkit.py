"""나라와 상관없이 쓰는 일정 부품: 행 만들기(mv/st), 시각 계산, 요금 합산, 예약 시점 꼬리표.
itinerary.py(스페인)·build_boards.py·build_booking.py·build_country.py 가 가져다 쓴다."""
import re

MODE_KO = {"walk": "도보", "metro": "메트로", "train": "열차", "rack": "산악열차", "funicular": "푸니쿨라",
           "bus": "버스", "tram": "트램", "taxi": "택시", "plane": "비행기", "ferry": "페리", "boat": "보트", "car": "렌터카"}


def mv(frm, to, mode, mins, line="", stops="", fare="", note=""):
    return {"kind": "move", "frm": frm, "to": to, "mode": mode, "mins": mins, "line": line, "stops": stops, "fare": fare, "note": note}


def st(place, do, dur, fare="", note="", at=None, link=""):
    return {"kind": "stop", "place": place, "do": do, "dur": dur, "fare": fare, "note": note, "at": at, "link": link}


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
    return dict(day, items=out, end="%02d:%02d" % (cursor // 60 % 24, cursor % 60))


def eur_of(fare):
    """요금 문구에서 유로 합계(하한)를 뽑는다. 하루 비용 합산용."""
    if not fare:
        return 0.0
    text = re.sub(r"€\s?(\d+(?:\.\d+)?)\s?[–~-]\s?€?\d+(?:\.\d+)?", r"€\1", fare)
    return sum(float(v) for v in re.findall(r"€\s?(\d+(?:\.\d+)?)", text))


def shift(hhmm, minutes):
    h, m = map(int, hhmm.split(":"))
    t = max(h * 60 + m - minutes, 5 * 60 + 30)
    return "%02d:%02d" % (t // 60, t % 60)


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
