/* 스페인 신혼여행 웹앱
 * data/courses.json  : 코스 × 날짜 × 행 (화면 내용 전부)
 * data/index.json    : 지도 구간 ↔ 행 번호 · 마커 번호(장소 키) 대응표
 * data/coords.json   : 장소 키 → 위경도
 * data/routes.json   : "출발|도착" 장소 키 → 도보 실제 경로
 * 마커 번호는 구간마다 1부터 다시 매기며, 행 제목("3 트리부날역 → 4 안톤 마르틴역")의 번호와 같다. */
(function () {
  'use strict';

  // 로컬(web/ 아래)에서는 한 단계 위, 아티팩트로 발행하면 같은 폴더에서 읽는다
  var LOCAL = /\/web\/?$/.test(location.pathname);
  var DATA = LOCAL ? '../data/' : 'data/';
  var ASSET = LOCAL ? '../' : '';
  // 로컬은 OSM 타일 서버를 직접 쓴다. ?atlas 를 붙이면 로컬에서도 내장 타일로 확인할 수 있다
  var ONLINE_TILES = LOCAL && !/[?&]atlas/.test(location.search);

  var BADGE = {
    walk: ['도보', '#1E56A0'], metro: ['메트로', '#B8432A'], train: ['열차', '#B8432A'],
    rack: ['산악열차', '#B8432A'], funicular: ['푸니쿨라', '#B8432A'], bus: ['버스', '#2F7A57'],
    tram: ['트램', '#2F7A57'], taxi: ['택시', '#7A5C99'], plane: ['비행기', '#7A5C99'], stop: ['장소', '#1C2230']
  };

  var trip = null;          // { courses, coords, routes }
  var state = { course: 'course1', day: 0, seg: 0, sel: -1 };
  var map, layer, pins = {};

  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ── 금액 표기 (board_template.dc.html 의 won / splitFare 와 같은 규칙) ──

  // 유로·달러 금액을 원화로 바꿔 쓴다 (1유로 = 1,500원, 1달러 = 1,330원)
  function won(text) {
    if (!text) return text || '';
    var fmt = function (v) {
      var step = v >= 100000 ? 1000 : (v >= 10000 ? 100 : 10);
      return (Math.round(v / step) * step).toLocaleString('ko-KR');
    };
    var range = function (rate) {
      return function (m, a, b) {
        var low = parseFloat(a) * rate;
        return b ? fmt(low) + '–' + fmt(parseFloat(b) * rate) + '원' : fmt(low) + '원';
      };
    };
    return text
      .replace(/€\s?(\d+(?:\.\d+)?)(?:\s?[–~-]\s?€?(\d+(?:\.\d+)?))?/g, range(1500))
      .replace(/\$(\d+(?:\.\d+)?)(?:\s?[–~-]\s?\$?(\d+(?:\.\d+)?))?/g, range(1330));
  }

  // 요금 문구를 '굵은 합계 한 줄 + 항목별 한 줄씩 + 회색 설명'으로 나눈다
  function splitFare(text) {
    var money = /(€|\$)\s?(\d+(?:\.\d+)?)(?:\s?[–~-]\s?(?:€|\$)?(\d+(?:\.\d+)?))?/;
    if (!text) return { main: '', lines: [], note: '' };
    if (text.indexOf(' + ') > 0) {
      var parts = text.split(' + ');
      var low = 0, high = 0, unknown = false;
      parts.forEach(function (p) {
        var m = money.exec(p);
        if (!m) { unknown = true; return; }
        var rate = m[1] === '€' ? 1500 : 1330;
        low += parseFloat(m[2]) * rate;
        high += (m[3] ? parseFloat(m[3]) : parseFloat(m[2])) * rate;
      });
      var total = won('€' + (low / 1500) + (high > low ? '–' + (high / 1500) : ''));
      return { main: '합계 약 ' + total + (unknown ? ' +α' : ''), lines: parts.map(won), note: '' };
    }
    var note = '';
    var paren = /\s*\(([^)]*)\)\s*$/.exec(text);
    if (paren && !money.test(paren[1])) { note = paren[1]; text = text.slice(0, paren.index); }
    if (text.indexOf(' · ') > 0) return { main: '', lines: text.split(' · ').map(won), note: note };
    var m = money.exec(text);
    if (!m) return text.length <= 8 ? { main: text, lines: [], note: note } : { main: '', lines: [text], note: note };
    var rest = (text.slice(0, m.index) + text.slice(m.index + m[0].length)).replace(/\(\s*\)/g, '').trim();
    return { main: won(m[0]), lines: [], note: [rest, note].filter(Boolean).join(' · ') };
  }

  // ── 데이터 준비 ──

  // 행 제목에서 마커 번호와 장소 이름을 뽑는다: "3 트리부날역 → 4 안톤 마르틴역"
  function parseHead(head) {
    return head.split(' → ').map(function (part) {
      var m = /^(\d+) (.*)$/.exec(part);
      return m ? { n: +m[1], name: m[2] } : null;
    }).filter(Boolean);
  }

  // index.json 을 날짜별 구간(segs)으로 붙이고, 행마다 구간 번호·장소 키를 단다
  function attachSegments(courses, index, coords, routes) {
    Object.keys(index).forEach(function (file) {
      var e = index[file];
      var day = courses['course' + e.course].days[e.day - 1];
      var inv = {};
      Object.keys(e.order).forEach(function (key) { inv[e.order[key]] = key; });
      var seg = { no: e.seg, city: e.city, markers: [], lines: [], caption: '' };
      var names = {};
      e.items.forEach(function (i) {
        var it = day.items[i];
        var spots = parseHead(it.head);
        it.seg = e.seg - 1;
        it.keys = spots.map(function (s) { names[s.n] = names[s.n] || s.name; return inv[s.n]; });
        it.nums = spots.map(function (s) { return s.n; });
        if (it.kind === 'move' && it.keys.length === 2) {
          var a = it.keys[0], b = it.keys[1];
          var pts = it.mode === 'walk' && (routes[a + '|' + b] || (routes[b + '|' + a] || []).slice().reverse());
          if (!pts || !pts.length) pts = [ll(coords, a), ll(coords, b)];
          seg.lines.push({ mode: it.mode, pts: pts, item: i });
        }
      });
      Object.keys(inv).sort(function (x, y) { return x - y; }).forEach(function (n) {
        var c = coords[inv[n]];
        if (c) seg.markers.push({ n: +n, key: inv[n], lat: c.lat, lon: c.lon, name: names[n] || inv[n] });
      });
      seg.caption = seg.markers.map(function (mk) { return mk.n + ' ' + mk.name; }).join(' → ');
      (day.segs = day.segs || [])[e.seg - 1] = seg;
    });
    Object.keys(courses).forEach(function (k) {
      courses[k].days.forEach(function (d) {
        d.segs = (d.segs || []).filter(Boolean);
        d.cost = d.items.reduce(function (s, it) { return s + (it.eur || 0); }, 0);
      });
    });
  }

  function ll(coords, key) { var c = coords[key]; return c ? [c.lat, c.lon] : null; }

  function load() {
    var get = function (name) {
      return fetch(DATA + name).then(function (r) {
        if (!r.ok) throw new Error(name + ' ' + r.status);
        return r.json();
      });
    };
    var previews = get('previews.json').catch(function () { return {}; });  // 없어도 앱은 돈다
    return Promise.all(['courses.json', 'index.json', 'coords.json', 'routes.json'].map(get).concat([previews])).then(function (res) {
      attachSegments(res[0], res[1], res[2], res[3]);
      trip = { courses: res[0], coords: res[2], routes: res[3], previews: res[4] || {} };
    });
  }

  // ── 주소(#c1-d3)와 상태 ──

  function readHash() {
    var m = /^#c(\d)-d(\d+)$/.exec(location.hash);
    if (m && trip.courses['course' + m[1]]) {
      state.course = 'course' + m[1];
      state.day = Math.min(Math.max(+m[2] - 1, 0), trip.courses[state.course].days.length - 1);
    }
    state.seg = 0; state.sel = -1;
  }

  function go(courseKey, day) {
    location.hash = '#c' + courseKey.replace('course', '') + '-d' + (day + 1);
  }

  // ── 그리기 ──

  function renderHeader() {
    var course = trip.courses[state.course];
    document.documentElement.style.setProperty('--accent', course.accent);

    $('courseTabs').innerHTML = Object.keys(trip.courses).map(function (k) {
      var c = trip.courses[k];
      var label = c.name.replace(/^코스 \d · /, '');
      return '<button class="course-tab" role="tab" data-c="' + k + '" style="--tab-c:' + c.accent + '" aria-selected="' + (k === state.course) + '">' +
        esc(k.replace('course', '') + ' · ' + label) + '</button>';
    }).join('');

    var total = course.days.reduce(function (s, d) { return s + d.cost; }, 0);
    $('courseBar').innerHTML = '<b>' + esc(course.name) + '</b> · ' + course.days.length + '일 · 이동·입장 합계 1인 약 <b>' +
      esc(won('€' + Math.round(total))) + '</b> (숙박·식비·항공 별도)';

    $('dayTabs').innerHTML = course.days.map(function (d, i) {
      return '<button class="day-tab" role="tab" data-d="' + i + '" aria-selected="' + (i === state.day) + '">' +
        '<span class="d">DAY ' + d.n + '</span><span class="t">' + esc(d.date) + ' (' + esc(d.dow) + ')</span>' +
        '<span class="c">' + esc(d.city) + '</span></button>';
    }).join('');
    var on = $('dayTabs').querySelector('[aria-selected="true"]');
    if (on) on.scrollIntoView({ block: 'nearest', inline: 'center' });
  }

  function renderPlan() {
    var d = trip.courses[state.course].days[state.day];
    var h = '';
    h += '<article class="day">';
    h += '<div class="card hero"><div>';
    h += '<div class="hero-meta"><span class="n">DAY ' + d.n + '</span><span class="date">' + esc(d.date) + ' (' + esc(d.dow) + ')</span><span class="pill">' + esc(d.city) + '</span></div>';
    h += '<h2>' + esc(d.title) + '</h2>';
    if (d.note) h += '<div class="day-note">' + esc(won(d.note)) + '</div>';
    h += '<dl class="morning">' +
      '<dt>' + esc(d.wake) + ' 기상</dt><dd>' + esc(d.sleepAt) + '</dd>' +
      '<dt>아침 A</dt><dd>' + esc(won(d.bfA)) + '</dd>' +
      '<dt>아침 B</dt><dd>' + esc(won(d.bfB)) + '</dd>' +
      '<dt>' + esc(d.start) + ' 출발</dt><dd>' + esc(d.startNote || '') + '</dd></dl>';
    if (d.sleepName) {
      h += '<div class="stay"><b>오늘 숙소</b> ' + esc(d.sleepName) + ' · 1박 ' + esc(won(d.sleepPrice || '')) +
        (d.sleepUrl ? ' <a href="' + esc(d.sleepUrl) + '" target="_blank" rel="noopener">요금 보기 ↗</a>' : '') + '</div>';
    }
    h += '</div>';
    if (d.photo && d.photo.file) {
      h += '<figure class="photo"><img src="' + esc(ASSET + d.photo.file) + '" alt="' + esc(d.photo.alt) + '" loading="lazy" onerror="this.parentNode.remove()">' +
        '<a href="' + esc(d.photo.page) + '" target="_blank" rel="noopener">' + esc(d.photo.credit) + '</a></figure>';
    }
    h += '</div>';

    h += '<div class="card"><ol class="timeline">';
    var lastSeg = null;
    d.items.forEach(function (it, i) {
      var seg = it.seg == null ? null : it.seg;
      if (d.segs.length > 1 && seg !== null && seg !== lastSeg) {
        h += '<li class="leg-break">지도 ' + (seg + 1) + ' · ' + esc(d.segs[seg].city) + '</li>';
      }
      if (seg !== null) lastSeg = seg;
      h += rowHtml(it, i);
    });
    h += '</ol><div class="day-total">일정 끝 ' + esc(d.end) + ' · 오늘 이동·입장 비용 1인 약 <b>' + esc(won('€' + Math.round(d.cost))) + '</b> (식비 별도)</div></div>';
    h += '</article>';
    $('plan').innerHTML = h;
  }

  function rowHtml(it, i) {
    var b = BADGE[it.kind === 'stop' ? 'stop' : it.mode] || ['이동', '#555'];
    var fare = splitFare(it.fare || '');
    var f = '';
    if (fare.main) f += '<span class="fm">' + esc(fare.main) + '</span>';
    fare.lines.forEach(function (t) { f += '<span class="fl">' + esc(t) + '</span>'; });
    if (fare.note) f += '<span class="fn">' + esc(fare.note) + '</span>';
    return '<li class="row" data-i="' + i + '" id="row-' + i + '">' +
      '<time>' + esc(it.time) + '</time>' +
      '<span class="badge" style="--c:' + b[1] + '">' + b[0] + '</span>' +
      '<div class="main"><span class="head">' + esc(it.head) + '</span>' +
      (it.line ? '<span>' + esc(won(it.line)) + '</span>' : '') +
      (it.note ? '<span class="note">' + esc(won(it.note)) + '</span>' : '') + '</div>' +
      '<div class="side"><span class="dur">' + esc(it.dur) + '</span>' + (f ? '<span class="fare">' + f + '</span>' : '') + '</div>' +
      '<div class="links">' +
      (it.mapUrl ? '<a href="' + esc(it.mapUrl) + '" target="_blank" rel="noopener">' + esc(it.mapLabel || '지도 ↗') + '</a>' : '') +
      (it.link ? '<a class="src" href="' + esc(it.link) + '" target="_blank" rel="noopener">출처·예매 ↗</a>' : '') +
      '</div></li>';
  }

  // ── 지도 ──

  var LINE_COLOR = { walk: '#1E56A0', metro: '#B8432A', train: '#B8432A', rack: '#B8432A', funicular: '#B8432A', bus: '#2F7A57', tram: '#2F7A57', taxi: '#7A5C99', plane: '#7A5C99' };

  // 아티팩트로 발행된 페이지는 외부 타일 서버를 못 쓴다. 미리 받아 둔 타일을
  // 아틀라스(JPEG 16×16장)에서 잘라 그리는 타일 레이어로 대신한다.
  var AtlasLayer = L.GridLayer.extend({
    initialize: function (index, opts) { this._index = index; this._sheets = {}; L.GridLayer.prototype.initialize.call(this, opts); },
    _sheet: function (no) {
      if (!this._sheets[no]) {
        var img = new Image();
        img.src = 'tiles/atlas_' + no + '.jpg';
        this._sheets[no] = img;
      }
      return this._sheets[no];
    },
    createTile: function (c, done) {
      var tile = document.createElement('canvas');
      tile.width = tile.height = 256;
      var hit = this._index[c.z + '/' + c.x + '/' + c.y];
      if (!hit) { setTimeout(function () { done(null, tile); }, 0); return tile; }
      var img = this._sheet(hit[0]);
      var draw = function () {
        tile.getContext('2d').drawImage(img, hit[1] * 256, hit[2] * 256, 256, 256, 0, 0, 256, 256);
        done(null, tile);
      };
      if (img.complete && img.naturalWidth) draw();
      else { img.addEventListener('load', draw); img.addEventListener('error', function () { done(null, tile); }); }
      return tile;
    }
  });

  function initMap() {
    var attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> 기여자';
    map = L.map('map', { zoomControl: true, scrollWheelZoom: true });
    layer = L.featureGroup().addTo(map);
    if (ONLINE_TILES) {
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: attribution }).addTo(map);
      return Promise.resolve();
    }
    return fetch('tiles/atlas.json').then(function (r) { return r.json(); }).then(function (index) {
      map.setMinZoom(12); map.setMaxZoom(16);
      new AtlasLayer(index, { minZoom: 12, maxZoom: 16, attribution: attribution }).addTo(map);
    }).catch(function () {});
  }

  function renderMap() {
    var d = trip.courses[state.course].days[state.day];
    $('segTabs').innerHTML = d.segs.length > 1 ? d.segs.map(function (s, i) {
      return '<button class="seg-tab" data-s="' + i + '" aria-selected="' + (i === state.seg) + '">지도 ' + (i + 1) + ' · ' + esc(s.city) + '</button>';
    }).join('') : '';

    layer.clearLayers(); pins = {};
    var seg = d.segs[state.seg];
    if (!seg) { $('mapCaption').textContent = '이날은 지도 구간이 없어요.'; return; }
    seg.lines.forEach(function (l) {
      var walk = l.mode === 'walk';
      L.polyline(l.pts, { color: LINE_COLOR[l.mode] || '#555', weight: walk ? 4 : 3, dashArray: walk ? null : '8 6', opacity: 0.9 })
        .on('click', function () { select(l.item, true); })
        .addTo(layer);
    });
    seg.markers.forEach(function (mk) {
      var m = L.marker([mk.lat, mk.lon], {
        icon: L.divIcon({ className: '', html: '<div class="pin">' + mk.n + '</div>', iconSize: [28, 28], iconAnchor: [14, 14] }),
        title: mk.n + ' ' + mk.name, riseOnHover: true
      }).bindTooltip(mk.n + ' ' + esc(mk.name), { direction: 'top', offset: [0, -14] })
        .on('click', function () { selectMarker(mk.n); })
        .addTo(layer);
      pins[mk.n] = m;
    });
    $('mapCaption').textContent = '지도 ' + (state.seg + 1) + ' · ' + seg.caption;
    map.invalidateSize();
    map.fitBounds(layer.getBounds(), { padding: [36, 36], maxZoom: 16 });
  }

  // 행의 링크(예매·식당·출처) 미리보기 카드. tools/fetch_previews.py 가 만든 스크린샷·제목을 쓴다
  function previewHtml(it) {
    if (!it.link) return '<p class="preview-empty">이 행은 예매·식당 링크가 없어요. 지도 링크는 행 안의 "' + esc(it.mapLabel || '지도 ↗') + '"를 눌러요.</p>';
    var p = trip.previews[it.link] || {};
    var host = p.host || it.link.replace(/^https?:\/\/(www\.)?/, '').split('/')[0];
    var kind = /ticket|entrada|renfe|omio|trenes|vueling|alsa|everyrail|patrimonio|alhambra|alcazar|parkguell|sagrada|fgc|crtm/i.test(it.link) ? '예매·요금' :
               /restaurant|tapas|bar|eat|food|gastro|table|rinconcillo|botin|menu|mercado|boqueria/i.test(it.link + ' ' + (it.line || '')) ? '식당' : '출처';
    return '<a class="pv" href="' + esc(it.link) + '" target="_blank" rel="noopener">' +
      '<span class="shot">' + (p.file ? '<img src="' + esc(ASSET + p.file) + '" alt="' + esc(p.title || host) + ' 페이지 화면" loading="lazy">' : '<span class="noimg">미리보기 없음 · 눌러서 열기</span>') + '</span>' +
      '<span class="meta"><span class="kind">' + kind + '</span>' +
      '<span class="title">' + esc(p.title || it.line || it.head) + '</span>' +
      (p.desc ? '<span class="desc">' + esc(p.desc) + '</span>' : '') +
      '<span class="host">' + esc(host) + '<b>열기 ↗</b></span></span></a>';
  }

  function renderPreview(it, row) {
    var html = previewHtml(it);
    $('preview').innerHTML = html;                                   // 데스크톱: 지도 아래
    document.querySelectorAll('.row-preview').forEach(function (e) { e.remove(); });
    if (row && it.link) {                                            // 폰: 그 행 아래
      var li = document.createElement('li');
      li.className = 'row-preview'; li.innerHTML = html;
      row.insertAdjacentElement('afterend', li);
    }
  }

  // 행을 고르면 그 행의 장소(또는 출발·도착)를 지도에서 강조하고 맞춰 보여 준다
  function select(i, scroll) {
    var d = trip.courses[state.course].days[state.day];
    var it = d.items[i];
    state.sel = i;
    document.querySelectorAll('.row.on').forEach(function (r) { r.classList.remove('on'); });
    var row = $('row-' + i);
    if (row) {
      row.classList.add('on');
      if (scroll) row.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    renderPreview(it, row);
    if (it.seg == null) return;              // 기차·비행기 장거리 구간은 지도 밖
    if (it.seg !== state.seg) { state.seg = it.seg; renderMap(); }
    Object.keys(pins).forEach(function (n) { pins[n].getElement() && pins[n].getElement().firstChild.classList.remove('on'); });
    var pts = [];
    it.nums.forEach(function (n) {
      var p = pins[n];
      if (!p) return;
      if (p.getElement()) p.getElement().firstChild.classList.add('on');
      p.setZIndexOffset(1000);
      pts.push(p.getLatLng());
    });
    if (pts.length === 1) map.flyTo(pts[0], Math.max(map.getZoom(), 16), { duration: 0.5 });
    else if (pts.length > 1) map.flyToBounds(L.latLngBounds(pts), { padding: [60, 60], maxZoom: 17, duration: 0.5 });
  }

  // 마커를 누르면 그 장소에 머무는 첫 행(없으면 그 장소가 나오는 첫 행)으로 간다
  function selectMarker(n) {
    var d = trip.courses[state.course].days[state.day];
    var hit = -1, any = -1;
    d.items.forEach(function (it, i) {
      if (it.seg !== state.seg || it.nums.indexOf(n) < 0) return;
      if (any < 0) any = i;
      if (hit < 0 && it.kind === 'stop') hit = i;
    });
    if (hit < 0) hit = any;
    if (hit >= 0) select(hit, true);
  }

  function render() {
    readHash();
    renderHeader();
    var bl = $('bookLink'); if (bl) bl.href = '../booking.html#c' + (location.hash.match(/^#c(\d)/) || [0, 1])[1];
    renderPlan();
    renderMap();
    $('preview').innerHTML = '<p class="preview-empty">일정 행을 누르면 그 행의 예매·식당 페이지 미리보기가 여기에 떠요.</p>';
    window.scrollTo({ top: 0 });
  }

  // ── 이벤트 ──

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.closest('a')) return;
    var c = t.closest('.course-tab');
    if (c) return go(c.dataset.c, 0);
    var d = t.closest('.day-tab');
    if (d) return go(state.course, +d.dataset.d);
    var s = t.closest('.seg-tab');
    if (s) { state.seg = +s.dataset.s; return renderMap(); }
    var r = t.closest('.row');
    if (r) return select(+r.dataset.i, false);
  });

  document.addEventListener('keydown', function (e) {
    if (e.target.closest('input, textarea')) return;
    var days = trip && trip.courses[state.course].days;
    if (!days) return;
    if (e.key === 'ArrowRight' && state.day < days.length - 1) go(state.course, state.day + 1);
    if (e.key === 'ArrowLeft' && state.day > 0) go(state.course, state.day - 1);
  });

  window.addEventListener('hashchange', render);

  Promise.all([initMap(), load()]).then(render).catch(function (err) {
    $('plan').innerHTML = '<p class="error">일정 데이터를 불러오지 못했어요 (' + esc(err.message) + ').<br>' +
      '프로젝트 폴더에서 <code>python -m http.server 8000</code> 실행 후 http://localhost:8000/web/ 으로 열어 주세요.</p>';
  });
})();
