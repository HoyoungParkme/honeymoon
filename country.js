/* 나라별 코스 선택 페이지 공통 동작. <html data-k>로 나라를 고른다 */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var budget, courses, picked = null;
  // <html data-k="greece"> 이면 data/greece/ 를 읽는다. 스페인은 키 없이 data/
  var K = document.documentElement.getAttribute('data-k') || '';
  var DATA = 'data/' + (K ? K + '/' : '');
  var Q = K ? '?k=' + K : '';
  function get(name) { return fetch(DATA + name).then(function (r) { if (!r.ok) throw new Error(name); return r.json(); }); }

  function renderCards() {
    var keys = Object.keys(budget.courses);
    $('cards').innerHTML = keys.map(function (k) {
      var c = budget.courses[k];
      return '<button type="button" class="card" data-k="' + k + '" aria-pressed="' + (k === picked) + '">' +
        '<img src="' + esc(c.photo) + '" alt="' + esc(c.alt) + '"><span class="shade"></span>' +
        '<span class="no" style="color:' + c.accent + '">' + esc(c.no) + '</span>' +
        '<span class="body"><span class="ttl">' + esc(c.title) + '</span><span class="tag">' + esc(c.tag) + '</span>' +
        '<span class="tot"><b>약 ' + c.total + '만 원</b><small>2인</small></span>' +
        '<span class="meta">' + esc(c.flightShort) + ' · ' + esc(c.stayShort) + '<span class="go">자세히 보기 →</span></span></span></button>';
    }).join('');
    $('cards').classList.toggle('has-pick', !!picked);
  }

  function renderPanel() {
    if (!picked) { $('panel').hidden = true; $('empty').hidden = false; return; }
    var c = budget.courses[picked];
    var days = courses[picked].days;
    $('empty').hidden = true; $('panel').hidden = false;
    $('panel').style.setProperty('--acc', c.accent);
    $('pLbl').textContent = c.no + ' · 총비용 (2인)'; $('pLbl').style.color = c.accent;
    $('pTotal').textContent = '약 ' + c.total + '만 원';
    $('pPct').textContent = '예산 ' + budget.budgetTotal.toLocaleString('ko-KR') + '만 원 중 ' + Math.round(c.total / budget.budgetTotal * 100) + '%';
    $('pGo').href = 'web/' + Q + '#c' + picked.replace('course', '') + '-d1';
    $('pBook').href = 'booking.html' + Q + '#c' + picked.replace('course', '');
    $('pBar').innerHTML = c.parts.map(function (v, i) {
      return '<span style="width:' + (v / budget.budgetTotal * 100).toFixed(1) + '%;background:' + budget.categories[i].color + '"></span>';
    }).join('');
    $('pLegend').innerHTML = c.parts.map(function (v, i) {
      return '<div><span><i style="background:' + budget.categories[i].color + '"></i>' + esc(budget.categories[i].label) + '</span><b>' + Math.round(v) + '만</b></div>';
    }).join('');
    $('pFlight').textContent = c.flight; $('pStay').textContent = c.stay; $('pGood').textContent = c.good; $('pWatch').textContent = c.watch;
    $('pDays').innerHTML = days.map(function (d) {
      return '<li><span class="num" aria-hidden="true">' + d.n + '</span><span class="n">DAY ' + d.n + ' · ' + esc(d.date) + '</span><span class="c">' + esc(d.city) + '</span><span class="t">' + esc(d.title) + '</span></li>';
    }).join('');
    $('panel').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  $('cards').addEventListener('click', function (e) {
    var b = e.target.closest('.card'); if (!b) return;
    picked = b.dataset.k; renderCards(); renderPanel();
  });

  Promise.all([get('budget.json'), get('courses.json')]).then(function (res) {
    budget = res[0]; courses = res[1];
    var m = /^#c(\d)$/.exec(location.hash);
    if (m && budget.courses['course' + m[1]]) picked = 'course' + m[1];
    renderCards(); renderPanel();
  }).catch(function (e) { $('cards').innerHTML = '<p style="color:#9C3A22">데이터를 불러오지 못했어요: ' + esc(e.message) + '</p>'; });
})();
