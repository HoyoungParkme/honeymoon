// 아트보드의 renderVals()를 실제로 실행해서 원화 변환·링크·사진 연결이 맞는지 확인한다
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const script = html.split('data-dc-script')[1].split('>').slice(1).join('>').split('</script>')[0];
class DCLogic { constructor() { this.props = {}; this.state = {}; } }
const Component = new Function('DCLogic', script + '\nreturn Component;')(DCLogic);
const vals = new Component().renderVals();
if (vals.days) {
  let noLink = 0;
  vals.days.forEach((d) => {
    console.log(`DAY ${d.n} photo=${d.photo ? 'Y' : '-'} stay=${d.stayUrl ? 'L' : '-'} | ${d.stay}`);
    d.stops.forEach((s) => console.log(`   ${s.t} ${s.what} | ${s.price} ${s.url ? '[L]' : ''}`));
    d.eat.forEach((e) => { console.log(`   먹: ${e.name} ${e.price} ${e.url ? '[L]' : '[NO LINK]'}`); if (!e.url) noLink++; });
    d.move.forEach((m) => console.log(`   교: ${m.how} ${m.price} ${m.url ? '[L]' : '[NO LINK]'} | ${m.pay.slice(0, 50)}`));
  });
  vals.budget.forEach((b) => console.log(`예산 ${b.k} ${b.v} ${b.url ? '[L]' : ''} | ${b.note}`));
  console.log('식당 링크 없음:', noLink);
}
if (vals.cities) vals.cities.forEach((c) => c.rows.forEach((r) => console.log(`${c.name} | ${r.what} | ${r.price} ${r.url ? '[L]' : '[NO LINK]'}`)));
if (vals.todo) vals.todo.forEach((t) => console.log(`할일 ${t.n} ${t.price} ${t.url ? '[L]' : ''}`));
if (vals.courses) vals.courses.forEach((c) => console.log(`코스 ${c.no} photo=${c.photo ? 'Y' : '-'}`));
