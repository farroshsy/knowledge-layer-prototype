"""Read-only loopback monitor for recorded Grok activity; never sends agent input."""
from __future__ import annotations
import argparse
import datetime as dt
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
from urllib.parse import urlparse,parse_qs

ROOT=Path(__file__).resolve().parents[1]
FOLDERS=['.council-runs','.council-audits','.research-review','.parallel-builds']
PIDS={'20261110-212748-e5a9aa':73314,'20261110-211254-a352d8':53773}

def read_json(path):
    try:return json.loads(path.read_text())
    except (OSError,ValueError):return None

def events(path):
    rows=[]
    try:
        for line in path.read_text().splitlines():
            try:rows.append(json.loads(line))
            except ValueError:pass # reader can observe a partially appended final record
    except OSError:pass
    return rows

def collect(root=ROOT, process_ids=None, now=None):
    root=Path(root);now=now or dt.datetime.now(dt.timezone.utc)
    if process_ids is None:
        try:
            raw=subprocess.run(['ps','-axo','pid='],capture_output=True,text=True,timeout=2,check=True).stdout
            process_ids={int(x) for x in raw.split()}
        except (OSError,ValueError,subprocess.SubprocessError):process_ids=None
    runs=[];all_intervals=[]
    last=read_json(root/'.council-runs/last-run.json') or {}
    for parent in FOLDERS:
        for folder in sorted((root/parent).glob('*')):
            if not folder.is_dir():continue
            rows=events(folder/'events.jsonl')
            if not rows:continue
            state=read_json(folder/'status.json') or {};stopped=any(r['node'] in {'run-stop','audit-failed','audit-finished'} for r in rows)
            latest={};intervals=[]
            for index,row in enumerate(rows):
                role=row.get('node','');status=row.get('status')
                if status=='running':latest[role]={'role':role,'status':'running','start':row['time'],'model':row.get('model'),'index':index}
                elif status in {'finished','failed'}:
                    old=latest.get(role,{'role':role,'start':row['time'],'model':row.get('model')})
                    old.update(status=status,end=row['time'],duration_s=row.get('duration_s'),error=row.get('error'));latest[role]=old
                    intervals.append(dict(old))
            pid=PIDS.get(folder.name);alive=None if process_ids is None or pid is None else pid in process_ids
            writer='automation.repair_candidate' if folder.name.startswith('repair-') else {
                '.council-runs':'automation.council',
                '.parallel-builds':'automation.parallel_build',
                '.research-review':'automation.research_review',
                '.council-audits':'automation.council',
            }.get(parent)
            if process_ids is not None and writer:
                try:
                    commands=subprocess.run(['ps','-axo','command='],capture_output=True,text=True,timeout=2).stdout
                except (OSError,subprocess.SubprocessError):
                    commands=''
                writer_alive=writer in commands
                if pid is None:
                    alive=writer_alive
                elif alive:
                    try:
                        command=subprocess.run(['ps','-p',str(pid),'-o','command='],capture_output=True,text=True,timeout=2).stdout
                    except (OSError,subprocess.SubprocessError):
                        command=''
                    if writer not in command:
                        alive=False
            active=[]
            for role,row in latest.items():
                if row['status']=='running':
                    age=(now-dt.datetime.fromisoformat(row['start'])).total_seconds()
                    row['elapsed_s']=round(max(age,0),1)
                    if stopped:row['status']='interrupted_or_run_ended'
                    elif alive is False:row['status']='process_not_observed'
                    else:active.append(row)
                    intervals.append({**row,'end':now.isoformat()})
            if parent=='.council-runs' and not stopped:
                for role in ['proposal-a','proposal-b','adjudicator','builder','integrity-review','contract-review']:
                    if role not in latest:latest[role]={'role':role,'status':'waiting_for_dependency','model':None}
            lasttime=dt.datetime.fromisoformat(rows[-1]['time']);age=round(max((now-lasttime).total_seconds(),0),1)
            reviewpaths=[]
            for p in folder.glob('round-*/*.json'):
                if p.name.endswith('-usage.json'):continue
                reviewpaths.append(str(p.relative_to(root)))
            for p in folder.glob('*.json'):
                if p.name not in {'status.json'} and not p.name.endswith('-usage.json'):reviewpaths.append(str(p.relative_to(root)))
            runs.append({'id':folder.name,'kind':parent,'state':state,'current':str(folder)==last.get('run'),'controller_pid':pid,'controller_observed':alive,'stopped':stopped,'last_event_age_s':age,'roles':list(latest.values()),'active_count':len(active),'events':rows[-100:],'artifacts':reviewpaths,'event_log':str((folder/'events.jsonl').relative_to(root))})
            all_intervals.extend([{**x,'run':folder.name} for x in intervals])
    points=[]
    for row in all_intervals:
        if row.get('status')=='process_not_observed':continue
        points.extend([(dt.datetime.fromisoformat(row['start']),1),(dt.datetime.fromisoformat(row['end']),-1)])
    count=peak=0
    for _,change in sorted(points,key=lambda x:(x[0],x[1])):count+=change;peak=max(peak,count)
    return {'collected_at':now.isoformat(),'runs':sorted(runs,key=lambda r:(not r['current'],r['id'])),'active_recorded_calls':sum(r['active_count'] for r in runs),'peak_recorded_overlap':peak,'limits':['A running event means the CLI call started, not proof tokens are advancing.','Controller PID presence is only liveness evidence, not proof of useful progress. Unknown means not observed, not stopped.','Elapsed time advances in the UI; provider progress inside a call is unavailable.','Separate calls may overlap. Build and its dependent reviews deliberately run in order.'],'graph':['Independent A + B (parallel)','Adjudicator (waits for both)','Builder','Integrity + contract review (parallel)','Fixed tests','Accepted candidate or recorded rejection']}

PAGE=r'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Agent Activity</title><style>
body{font:16px system-ui;background:#10272a;color:#eef8f4;margin:0}header,main{max-width:1200px;margin:auto;padding:20px}h1{font-size:30px;margin:10px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.card,details{background:#1c3c3f;padding:16px;border-radius:12px;margin:12px 0;overflow-wrap:anywhere}.live{border-left:5px solid #6ce0b4}.fail{border-left:5px solid #ffb090}.muted{color:#c5d9d5}button,a{font:inherit;color:#a6f1df}button{background:#294f52;border:0;border-radius:6px;padding:8px;cursor:pointer}.pill{display:inline-block;background:#33575a;padding:4px 8px;border-radius:6px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}nav{display:flex;gap:10px;flex-wrap:wrap}#artifact{max-height:70vh;overflow:auto}svg{width:100%;height:auto}svg text{fill:#eef8f4;font:13px system-ui}svg line{stroke:#9ec8bf}svg rect{fill:#254e51;stroke:#97c8be}</style>
<header><h1>Aktivitas AI agent</h1><p id="connection">Connecting…</p><nav><button id="refresh">Refresh sekarang</button><label><input type="checkbox" id="history"> Tampilkan run lama</label></nav><p class="muted">Polling setiap 3 detik. Tidak ada tombol yang memberi instruksi atau mengubah kode.</p></header>
<main><div id="stats" class="grid"></div><details open><summary>Kenapa ada yang paralel dan ada yang menunggu?</summary><p>A dan B menganalisis secara paralel. Adjudicator menunggu keduanya. Builder menunggu keputusan. Dua reviewer berjalan bersamaan setelah ada diff. Jadi agent tidak selalu aktif semuanya pada saat yang sama.</p><div id="dag"></div></details><div id="runs"></div><details><summary>Batas observasi</summary><div id="limits"></div></details><article class="card"><h2>Hasil agent / evidence</h2><pre id="artifact">Pilih hasil agent untuk membacanya.</pre></article></main>
<script>
const $=id=>document.getElementById(id);const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let data;
function render(){if(!data)return;const rs=data.runs.filter(r=>$('history').checked||r.current||(!r.stopped&&r.kind!=='.council-runs'));$('stats').innerHTML=[['Panggilan tercatat aktif',data.active_recorded_calls],['Overlap maksimum tercatat',data.peak_recorded_overlap],['Kandidat diterima (run kini)',data.runs.find(r=>r.current)?.state.accepted??0]].map(([k,v])=>'<article class="card"><div class="muted">'+esc(k)+'</div><h2>'+esc(v)+'</h2></article>').join('');
$('dag').innerHTML='<p>'+data.graph.map(esc).join(' → ')+'</p>';
$('limits').innerHTML=data.limits.map(x=>'<p>'+esc(x)+'</p>').join('');
$('runs').innerHTML=rs.map(r=>'<section class="card"><h2>'+esc(r.current?'Implementasi saat ini':r.kind)+' · '+esc(r.id)+'</h2><p>Status tercatat '+esc(r.state.status)+' · event terakhir '+esc(r.last_event_age_s)+' detik lalu · controller '+esc(r.controller_observed===true?'PID terlihat':r.controller_observed===false?'PID tidak terlihat':'belum diverifikasi')+'</p><div class="grid">'+r.roles.map(a=>'<article class="card '+(a.status==='running'?'live':a.status==='failed'?'fail':'')+'"><strong>'+esc(a.role)+'</strong><p class="pill">'+esc(a.status)+'</p><p>'+esc(a.model??'model tidak tercatat')+'</p><p>'+esc(a.elapsed_s??a.duration_s??'?')+' detik</p>'+(a.error?'<p>'+esc(a.error)+'</p>':'')+'</article>').join('')+'</div><details><summary>Hasil tersimpan ('+r.artifacts.length+')</summary>'+r.artifacts.map(p=>'<p><button data-artifact="'+esc(p)+'">'+esc(p.split('/').slice(-2).join('/'))+'</button></p>').join('')+'</details><details><summary>Timeline event aktual</summary><pre>'+esc(r.events.map(e=>e.time+' '+e.node+' '+(e.status??'')+' '+(e.error??'')).join('\n'))+'</pre></details></section>').join('');
for(const b of document.querySelectorAll('[data-artifact]'))b.onclick=async()=>{try{const r=await fetch('/api/evidence?path='+encodeURIComponent(b.dataset.artifact));if(!r.ok)throw Error('HTTP '+r.status);$('artifact').textContent=await r.text();$('artifact').scrollIntoView({behavior:'smooth'});}catch(e){$('artifact').textContent=String(e);}};}
async function refresh(){try{const r=await fetch('/api/status',{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);data=await r.json();$('connection').textContent='Terhubung · snapshot '+new Date(data.collected_at).toLocaleTimeString('id-ID');render();}catch(e){$('connection').textContent='Koneksi terputus; tampilan terakhir bukan status live. '+e;}}
$('refresh').onclick=refresh;$('history').onchange=render;refresh();setInterval(refresh,3000);
</script></html>'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8766);args=ap.parse_args()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*_):pass
        def do_GET(self):
            parsed=urlparse(self.path)
            try:
                if parsed.path=='/':body=PAGE.encode();mime='text/html; charset=utf-8'
                elif parsed.path=='/api/status':body=json.dumps(collect()).encode();mime='application/json'
                elif parsed.path=='/api/evidence':
                    raw=parse_qs(parsed.query).get('path',[''])[0];p=(ROOT/raw).resolve()
                    allowed=any(p.is_relative_to((ROOT/f).resolve()) for f in FOLDERS)
                    if not allowed or p.suffix not in {'.json','.jsonl','.diff'} or not p.is_file() or p.stat().st_size>1_000_000:
                        self.send_error(404);return
                    body=p.read_bytes();mime='text/plain; charset=utf-8'
                else:self.send_error(404);return
                self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            except (OSError,ValueError):self.send_error(500)
    print(f'http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()

if __name__=='__main__':main()
