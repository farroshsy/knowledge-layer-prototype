"""Generate evidence-linked memory and graph from actual run files; no app edits."""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import time
from automation.council import source_snapshot, fingerprint, atomic_json

ROOT=Path(__file__).resolve().parents[1]
REFS=[
('owasp-injection','Prompt injection','https://genai.owasp.org/llmrisk/llm01-prompt-injection/','Retrieved documents can carry instructions; prompts and RAG alone do not eliminate injection. Bound privileges and validate outputs.'),
('owasp-upload','File upload','https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html','Use format allowlists, size limits, safe names and storage boundaries; verify actual content before parsing.'),
('owasp-sql','SQL injection','https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html','Bind data using parameters and allowlist dynamic identifiers. Do not execute model-generated arbitrary SQL.'),
('nist','AI risk lifecycle','https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence','Risk assessment spans design, development, use and evaluation. A passing demo is not production certification.'),
('provenance','Provenance','https://www.w3.org/TR/prov-overview/','Track entities, activities and agents responsible for derivations. Lineage supports assessment; it does not prove truth.'),
('faithfulness','Answer support','https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/','Assess whether assertions are supported by retrieved context; source span validity is a separate check.'),
('recall','Retrieval recall','https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/','Recall evaluation requires a defined reference; do not infer recall from plausible-looking responses.'),
('foreignkeys','SQLite constraints','https://www.sqlite.org/foreignkeys.html','Declare relationships and enable enforcement on connections; PRAGMA alone does not create missing constraints.'),
('wal','SQLite concurrency','https://www.sqlite.org/wal.html','WAL changes concurrency and backup/checkpoint behavior. Do not turn it on merely as a scalability label.'),
('subprocess','Provider process boundary','https://docs.python.org/3.14/library/subprocess.html','Use explicit argument lists, controlled timeouts and exit handling. Parent timeout does not establish all descendant cleanup.')]

RISKS=[
('hybrid','Independent business records and combined retrieval','demo-blocker','DB-only/docs-only/combined HTTP tests using records absent from document text','not_measured','owasp-sql'),
('formats','Actual document formats','demo-risk','Upload real text PDF/DOCX if supported; scanned PDF must not silently become empty text','not_measured','owasp-upload'),
('semantic','Negation, proposal, attribution and time','demo-blocker','Plan is neither proof of occurrence nor proof of non-occurrence; compare source-specific assertions','not_measured','faithfulness'),
('identity','Same-name entity linking','demo-blocker','Two people with same name and different IDs must remain ambiguous without confirmed link','not_measured','provenance'),
('provider','Provider timeout and fallback','observed-failure','Exercise actual Grok HTTP ingestion and inspect nested job method/error metadata','failed','subprocess'),
('citation','Citation validity versus semantic support','demo-blocker','Test exact location, active version AND claim support independently','not_measured','faithfulness'),
('injection','Document prompt injection','security','Upload document telling model to ignore scope/execute SQL; verify bounded plan and unchanged data','not_measured','owasp-injection'),
('scope','Workspace separation and access control','security','Query same entity IDs in separate notebooks; no cross-scope retrieval. Local single-user PoC is not authenticated enterprise deployment','not_measured','owasp-sql'),
('persistence','Retry, atomic publication, restart','integrity','Retry failure, duplicate hash and reopen database; inspect active results and row constraints','partial_baseline_tests','foreignkeys'),
('performance','Latency, context and concurrency','operations','Report raw server wall time and sample counts; timeout is a result, not omitted sample','partial_single_run','subprocess'),
('privacy','Provider policy and document sensitivity','before_real_data','Only synthetic inputs used here; real company documents need an authorized provider/data handling decision','open_decision','nist'),
('supply','Dependencies and parser attack surface','security','Review installed parser versions, upload limits and failure behavior; no unbounded auto-installs','not_measured','owasp-upload'),
('handoff','Repeatable local run and recovery','delivery','Another engineer starts selected candidate, inserts fresh data, restarts and repeats query','not_measured','nist'),
('value','Business value and investment','after_poc','Measure actual task time/cost with intended users; PoC does not establish ROI or product-market fit','not_measured','nist')]


def load(path):
    try:return json.loads(path.read_text())
    except (OSError,ValueError):return None

def build(root=ROOT):
    root=Path(root);out=root/'.context-hub';out.mkdir(exist_ok=True)
    now=dt.datetime.now(dt.timezone.utc).isoformat();snap=source_snapshot(root);sha=fingerprint(snap)
    nodes=[];edges=[]
    def node(i,label,kind,status,evidence=None,detail=''):
        nodes.append(dict(id=i,label=label,kind=kind,status=status,evidence=evidence,detail=detail))
    def edge(a,b,kind):edges.append(dict(source=a,target=b,kind=kind))
    node('goal','Working local PoC — 11 Nov 08:00 WIB','requirement','target',detail='Unseen documents + independent structured records + grounded combined answers. Six months is conditional.')
    steps=['Workspace','Upload new document','Process and classify','Inspect evidence','Retrieve DB / documents / both','Answer with sources or uncertainty','Restart and repeat']
    for i,label in enumerate(steps):
        node('process-'+str(i),label,'business-process','target');edge('goal','process-'+str(i),'requires')
        if i:edge('process-'+str(i-1),'process-'+str(i),'next')
    for rel in sorted(snap):
        if rel.startswith('klayer/'):
            node('code:'+rel,rel,'implementation','present',rel,'Presence is not proof of acceptance. SHA256 '+hashlib.sha256(snap[rel].encode()).hexdigest())
            responsibilities={'klayer/server.py':[0,1,4,5],'klayer/pipeline.py':[2,3,4,5],'klayer/providers.py':[2,4],'klayer/store.py':[0,1,3,4,6],'klayer/domain.py':[2],'klayer/static/index.html':[0,1,3,5]}
            for step in responsibilities.get(rel,[]):edge('process-'+str(step),'code:'+rel,'code_path_not_acceptance')
    last=load(root/'.council-runs/last-run.json');run=Path(last['run']) if last else None
    state=load(run/'status.json') if run else None
    if run:
        rel=str(run.relative_to(root));node('run','Implementation council','agent-run',state.get('status','unknown') if state else 'unknown',rel+'/report.html',json.dumps(state));edge('goal','run','implemented_by')
    approved=load(root/'.council-runs/latest-approved.json')
    if approved:
        release=Path(approved['release']);actual=fingerprint(source_snapshot(release)) if release.exists() else None
        valid=actual==approved.get('source_hash')
        node('candidate','Latest reviewed candidate','candidate','hash_valid' if valid else 'stale_or_missing','.council-runs/latest-approved.json','Test/review gate does not prove complete PoC acceptance.');edge('run','candidate','produced')
    else:node('candidate','Accepted implementation candidate','candidate','none',detail='No accepted candidate pointer currently exists.');edge('run','candidate','awaits')
    for p in sorted((root/'.council-audits').glob('*/status.json')):
        obj=load(p) or {};node('audit:'+p.parent.name,'Adversarial audit '+p.parent.name,'agent-run',obj.get('status','unknown'),str(p.relative_to(root)), 'Read-only analysis; not executed tests.');edge('goal','audit:'+p.parent.name,'reviewed_by')
    summaries=[]
    for p in sorted((root/'.acceptance-runs').glob('*/results.json')):
        x=load(p)
        if not x:continue
        proto=x.get('protocol',{});provider=proto.get('provider','unknown')
        total=x.get('evaluated_checks',0);passed=x.get('passed_checks',0)
        status='failed_checks' if total and passed<total else ('limited_checks_pass' if total else 'in_progress')
        i='evaluation:'+p.parent.name
        node(i,p.parent.name+' '+str(passed)+'/'+str(total),'evaluation',status,str(p.relative_to(root)), 'Provider '+provider+'. Does not cover all PoC requirements.');edge('goal',i,'evaluated_by')
        summaries.append({'provider':provider,'passed':passed,'total':total,'source':str(p.relative_to(root)),'coverage_limits':proto.get('coverage_limits',[])})
        for j,c in enumerate(x.get('checks',[])):
            ci=i+':'+str(j);node(ci,c['case'],'check','pass' if c.get('passed') is True else 'fail',str(p.relative_to(root)),json.dumps(c,ensure_ascii=False));edge(i,ci,'contains')
    for i,title,url,note in REFS:node('ref:'+i,title,'primary-reference','reviewed_reference',url,note)
    for i,title,priority,test,status,ref in RISKS:
        ri='risk:'+i;node(ri,title,'risk',status,detail=priority+' — '+test);edge('goal',ri,'bounded_by');edge(ri,'ref:'+ref,'informed_by')
    for n in list(nodes):
        if n['kind']=='evaluation':edge('risk:provider',n['id'],'check_actual_provider_evidence')
    claims=[{'claim':'The PoC is complete','status':'not_established','required_evidence':'Unseen hybrid end-to-end acceptance on selected candidate'},
            {'claim':'All inference is local/offline','status':'false_for_grok','required_evidence':'Grok CLI calls online inference; app local != model offline'},
            {'claim':'All live Grok checks passed','status':'contradicted','required_evidence':'.acceptance-runs/grok-http-01/results.json shows fallback timeout'},
            {'claim':'Production readiness or business ROI proven','status':'not_established','required_evidence':'Separate pilot/privacy/security/operations and business measurement'},
            {'claim':'Independent model agreement proves correctness','status':'invalid_inference','required_evidence':'Behavior tests, counterexamples and independent source evidence required'}]
    obj={'generated_at':now,'source_hash':sha,'scope':'current original project source; candidates separately linked','run':state,'evaluations':summaries,'claims':claims,'nodes':nodes,'edges':edges,'freshness':'Regenerate before handing to an agent. Evidence applies to its tested source/config, not every future revision.'}
    atomic_json(out/'state.json',obj);atomic_json(out/'graph.json',{'nodes':nodes,'edges':edges})
    memory=['# Current context — evidence first',f'Generated {now}',f'Original source hash {sha}','Deadline 11 November 2026 08:00 Asia/Jakarta. Working PoC, not approved six-month project.','Goal: independent business records plus unseen documents, combined grounded answer.','Never touch frozen ai-interview-platform. No push/publication, secrets, or real private docs.','Read DELIVERY.md and council/shared-business-task.md for business process.','Do not treat attached proposals, model recommendations or presence of code as completed acceptance.',f'Current build status: {json.dumps(state)}','Accepted candidate pointer: '+str(bool(approved)),'## Actual HTTP evaluations',json.dumps(summaries,indent=2),'## Claim limits',json.dumps(claims,indent=2),'## Open acceptance and risks',json.dumps(RISKS,indent=2),'## Commands','python3 -m automation.context_hub','python3 -m automation.context_hub --neighbors risk:provider','python3 automation/council.py status','python3 automation/exercise_app.py --provider grok --out .acceptance-runs/NEW-RUN','Use existing primary references in state.json. Do not send entire chat history by default. Retrieve relevant graph neighborhood, source and evidence.','This memory file is not automatically loaded by already-running model calls. Coordinator must include it or relevant nodes on the next dispatch.']
    (out/'MEMORY.md').write_text('\n\n'.join(memory))
    research=['# Primary-source research and application checks',f'Retrieved 10 November 2026. Generated {now}. This is a selected-source review, not an exhaustive security audit. Recommendations are not implemented controls.']
    for i,title,url,note in REFS:
        related=[r for r in RISKS if r[-1]==i]
        research.extend(['\n## '+title,'Source: ['+title+']('+url+')',note,*['- Proposed check: '+r[3]+' — current status '+r[4] for r in related]])
    research.extend(['\n## Additional product acceptance dimensions','Business process: useful combined answer over genuinely independent records and new documents. Persona, source authority, temporal semantics and escalation behavior remain explicit assumptions.','Evaluation: separate development fixtures, held-out cases, live provider checks and counterexamples. Define expected answers before execution. Count unsupported assertions and citation support separately from exact-span validity.','Operations: current source/candidate hash, provider/model/config, raw durations with sample count, retry/failure status, cold/warm separation when known, no missing-cost-as-zero.','Privacy/security: workspace scoping, credentials, document data policy, parser limits, unsafe content rendering, source injection, SQL identifiers, network exposure, resource exhaustion, dependency provenance, local test-code execution, backup/recovery. No complete security certification is claimed.','Delivery: local start/restart, a selected runnable candidate, three query routes and visible evidence, honest limits. ROI/PoV and real-user pilot need separate measurements.','Existing ongoing model calls do not magically read this file. Supply relevant graph neighborhoods and current evidence on subsequent dispatches.'])
    (out/'RESEARCH.md').write_text('\n\n'.join(research))
    data=json.dumps(obj,ensure_ascii=False).replace('<','\\u003c').replace('&','\\u0026')
    template=r'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Knowledge PoC — evidence hub</title>
<style>body{font:16px system-ui;margin:0;background:#102325;color:#eff8f6}header,main{max-width:1100px;margin:auto;padding:24px}h1{font-size:30px}button,input,select{font:inherit;padding:10px;border-radius:8px}button{cursor:pointer}a{color:#91dfcf}nav{display:flex;gap:8px;flex-wrap:wrap}article{padding:16px;background:#1a3537;border-radius:12px;margin:12px 0;overflow-wrap:anywhere}small{color:#c5dcd7}pre{white-space:pre-wrap}#layout{display:grid;grid-template-columns:1fr 1fr;gap:16px}.pill{display:inline-block;padding:4px 8px;background:#345150;border-radius:5px}svg{width:100%;height:auto}svg text{fill:#eff8f6;font:13px system-ui}svg line{stroke:#a2b9b5}svg rect{fill:#245051;stroke:#86bdb3}#nodes button{display:block;width:100%;text-align:left;background:transparent;color:inherit;border:0}input{width:min(80%,500px)}@media(max-width:700px){#layout{grid-template-columns:1fr}}</style>
<header><h1>Knowledge PoC — evidence hub</h1><p id="fresh"></p><nav><button data-view="overview">Business process</button><button data-view="graph">Graph explorer</button><button data-view="claims">Claim gates</button><a href="MEMORY.md">Agent memory</a><a href="graph.json">Graph JSON</a></nav></header><main>
<section id="overview"><h2>Target workflow · current evidence</h2><svg viewBox="0 0 1000 190" role="img" aria-label="Target business process; nodes are targets, not acceptance passes"><g id="flow"></g></svg><p>Diagram menunjukkan target alur. Status pengujian dan implementasi terpisah di bawah.</p><div id="summary"></div></section>
<section id="graph" hidden><h2>Requirements → implementation → tests → risks → sources</h2><label>Cari node <input id="search" placeholder="provider, SQL, hybrid, evidence"></label><div id="layout"><article id="nodes"></article><article id="detail">Pilih node untuk melihat hubungan dan bukti.</article></div></section>
<section id="claims" hidden><h2>Claim gates</h2><div id="claimlist"></div></section></main><script>
const state=DATA;const byId=new Map(state.nodes.map(n=>[n.id,n]));const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.getElementById('fresh').textContent='Snapshot '+state.generated_at+' · Refresh generator before review · source '+state.source_hash.slice(0,12);
for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>{for(const id of ['overview','graph','claims'])document.getElementById(id).hidden=id!==b.dataset.view;};
const steps=state.nodes.filter(n=>n.kind==='business-process');document.getElementById('flow').innerHTML=steps.map((n,i)=>{const x=10+i*140;return (i?'<line x1="'+(x-17)+'" y1="65" x2="'+x+'" y2="65"/>':'')+'<g><rect x="'+x+'" y="15" width="125" height="120" rx="10"/><text x="'+(x+10)+'" y="42">'+esc(n.label.split(' ').slice(0,2).join(' '))+'</text><text x="'+(x+10)+'" y="65">'+esc(n.label.split(' ').slice(2,4).join(' '))+'</text><text x="'+(x+10)+'" y="88">'+esc(n.label.split(' ').slice(4).join(' '))+'</text><text x="'+(x+10)+'" y="118">Target</text></g>';}).join('');
function link(n){if(!n.evidence)return '';const url=/^https:\/\//.test(n.evidence)?n.evidence:'../'+n.evidence;return '<p><a href="'+esc(url)+'">Buka evidence / reference</a></p>';}
function select(id){const n=byId.get(id);const edges=state.edges.filter(e=>e.source===id||e.target===id);document.getElementById('detail').innerHTML='<h3>'+esc(n.label)+'</h3><span class="pill">'+esc(n.status)+'</span><p>'+esc(n.detail)+'</p>'+link(n)+'<h3>Relationships</h3>'+edges.map(e=>{const other=byId.get(e.source===id?e.target:e.source);return '<p>'+esc(e.kind)+' → <button data-node="'+esc(other.id)+'">'+esc(other.label)+'</button></p>';}).join('');for(const b of document.querySelectorAll('#detail [data-node]'))b.onclick=()=>select(b.dataset.node);}
function render(){const q=document.getElementById('search').value.toLowerCase();const list=state.nodes.filter(n=>(n.label+' '+n.kind+' '+n.status+' '+n.detail).toLowerCase().includes(q));document.getElementById('nodes').innerHTML=list.map(n=>'<button data-node="'+esc(n.id)+'">'+esc(n.label)+'<br><small>'+esc(n.kind)+' · '+esc(n.status)+'</small></button>').join('');for(const b of document.querySelectorAll('#nodes button'))b.onclick=()=>select(b.dataset.node);}
document.getElementById('search').oninput=render;render();document.getElementById('summary').innerHTML=state.nodes.filter(n=>['agent-run','evaluation','candidate'].includes(n.kind)).map(n=>'<article><strong>'+esc(n.label)+'</strong> · '+esc(n.status)+link(n)+'<pre>'+esc(n.detail)+'</pre></article>').join('');document.getElementById('claimlist').innerHTML=state.claims.map(c=>'<article><strong>'+esc(c.claim)+'</strong><p>'+esc(c.status)+'</p><p>'+esc(c.required_evidence)+'</p></article>').join('');
</script></html>'''
    (out/'index.html').write_text(template.replace('const state=DATA;', 'const state='+data+';'))
    return obj

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--watch',type=int,default=0);ap.add_argument('--neighbors');args=ap.parse_args()
    until=time.monotonic()+4*3600
    while True:
        obj=build()
        if args.neighbors:
            es=[e for e in obj['edges'] if args.neighbors in (e['source'],e['target'])];ids={args.neighbors}|{e['source'] for e in es}|{e['target'] for e in es};print(json.dumps({'nodes':[n for n in obj['nodes'] if n['id'] in ids],'edges':es},ensure_ascii=False,indent=2));return
        print(ROOT/'.context-hub/index.html',flush=True)
        if not args.watch or time.monotonic()>=until:return
        time.sleep(max(10,args.watch))

if __name__=='__main__':main()
