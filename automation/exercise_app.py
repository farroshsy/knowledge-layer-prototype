"""Exercise actual local HTTP app with fresh synthetic inputs; preserve raw evidence.
Not a browser usability review or a broad semantic benchmark.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import urllib.request
import uuid

def provider_failures(value, expect_grok=False):
    found=[]
    if isinstance(value,dict):
        if value.get('provider_error'):found.append(str(value['provider_error']))
        if expect_grok and value.get('provider_label')=='local-rules':found.append('local-rules fallback')
        for child in value.values():found.extend(provider_failures(child,expect_grok))
    elif isinstance(value,list):
        for child in value:found.extend(provider_failures(child,expect_grok))
    return found

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default=str(Path(__file__).resolve().parents[1]));ap.add_argument('--provider',choices=['rules','grok'],default='rules');ap.add_argument('--out',required=True);args=ap.parse_args()
    source=Path(args.source).resolve();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(source))
    from klayer.store import Store
    from klayer.providers import build_provider
    from klayer.server import serve
    nonce='UNSEEN-'+uuid.uuid4().hex[:10]
    # Expectations are frozen before app requests, not inferred from its answers.
    from automation.council import source_snapshot, fingerprint
    protocol={'nonce':nonce,'provider':args.provider,'source':str(source),'source_hash':fingerprint(source_snapshot(source)),'expectations':{'new_upload':'completed and preserves original nonce','repeat_upload':'created false','affirmed_lookup':'must contain Sari attendance and exclude Budi negated attendance','unsupported':'abstain with no claims'},'coverage_limits':['independent business records and hybrid route not exercised by this baseline-compatible protocol','native PDF/DOCX not exercised','not a browser interaction or full semantic support evaluation']}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2))
    rows=[];checks=[]
    def save():
        report={'time':dt.datetime.now(dt.timezone.utc).isoformat(),'protocol':protocol,'requests':rows,'checks':checks,'passed_checks':sum(x['passed'] is True for x in checks),'evaluated_checks':len(checks),'quality_f1':None,'production_ready':False}
        (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    with tempfile.TemporaryDirectory(prefix='knowledge-http-eval-') as tmp:
        store=Store(Path(tmp)/'test.sqlite');server=serve(store,build_provider(args.provider),'127.0.0.1',0)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_address[1]}'
        def request(path,payload=None):
            t=time.monotonic();row={'path':path,'input':payload}
            try:
                req=urllib.request.Request(base+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=240) as response:
                    raw=response.read().decode();row.update(status=response.status,body=json.loads(raw) if 'json' in response.headers.get('Content-Type','') else raw)
                return row['body']
            except Exception as exc:row['error']=str(exc);raise
            finally:row['duration_s']=round(time.monotonic()-t,4);rows.append(row);save()
        try:
            page=request('/');checks.append({'case':'ui_available','passed':isinstance(page,str) and '<html' in page.lower()})
            nb=request('/api/notebooks',{'name':'fresh acceptance '+nonce})['notebook']['id']
            body='Notulen rapat operasional\n\nPeserta: Sari\nKeputusan: pilot direncanakan mulai 23 November. Kode '+nonce+'.\nMenurut catatan rapat, Sari hadir di rapat 14 Maret.\nBudi tidak hadir di rapat 14 Maret.\n'
            payload={'filename':'sop-'+nonce+'.txt','text':body}
            created=request(f'/api/notebooks/{nb}/documents',payload)
            checks.append({'case':'new_upload','passed':created.get('job',{}).get('status')=='completed' and nonce in created.get('document',{}).get('body','')})
            duplicate=request(f'/api/notebooks/{nb}/documents',payload);checks.append({'case':'repeat_upload','passed':duplicate.get('created') is False})
            answer=request(f'/api/notebooks/{nb}/query',{'question':'Siapa yang hadir di rapat?'})
            claims=answer.get('claims',[])
            checks.append({'case':'affirmed_lookup','passed':any('Sari' in c.get('quote','') and c.get('polarity')=='affirmed' for c in claims) and not any('Budi' in c.get('quote','') for c in claims)})
            answer=request(f'/api/notebooks/{nb}/query',{'question':'Berapa harga saham perusahaan kemarin?'})
            checks.append({'case':'unsupported','passed':answer.get('answer')=='abstain' and not answer.get('claims')})
            failures=provider_failures([r.get('body') for r in rows],args.provider=='grok')
            checks.append({'case':'no_provider_fallback','passed':not failures,'findings':failures,'note':'Nested job metadata is checked too; passing this does not establish semantic correctness.'})
        except Exception as exc:checks.append({'case':'exercise_error','passed':False,'error':str(exc)})
        finally:server.shutdown();server.server_close();thread.join(timeout=3);store.close();save()
    print(out/'results.json',flush=True)

if __name__=='__main__':main()
