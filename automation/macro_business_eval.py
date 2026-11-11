"""Synthetic cross-domain HTTP journeys; not proof of real-user value or universal support."""
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
from automation.council import source_snapshot,fingerprint

SCENARIOS=[('people-operations','Onboarding karyawan','HR memeriksa status onboarding dan memo terbaru'),('project-operations','Peluncuran kelas','PIC memeriksa status peluncuran dan notulen persiapan'),('procurement','Pengadaan laptop','Operasional memeriksa status pembelian dan catatan rapat')]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--provider',default='rules',choices=['rules','grok']);a=ap.parse_args()
    source=Path(a.source).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(source))
    from klayer.store import Store
    from klayer.providers import build_provider
    from klayer.server import serve
    protocol={'dataset':'synthetic-macro-v1','scenarios':SCENARIOS,'source_hash':fingerprint(source_snapshot(source)),'provider':a.provider,'expected_before_execution':{'db_only':'retrieves independent matching stable record id without document evidence','combined':'returns route combined with matching record id plus fresh document claim containing exact record id','isolation':'another empty notebook must not return the original record'},'limits':['Synthetic representative workflows, not real users or all domains.','HTTP journey, not browser usability test.','Rules execution does not establish real-model extraction quality.','Manual semantic support and business task-time comparison still required.']}
    (out/'protocol.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2))
    results=[]
    with tempfile.TemporaryDirectory(prefix='macro-business-') as tmp:
        st=Store(Path(tmp)/'eval.sqlite');server=serve(st,build_provider(a.provider),'127.0.0.1',0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_address[1]}'
        def call(path,payload):
            t=time.monotonic();req=urllib.request.Request(base+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=240) as r:return json.load(r),round(time.monotonic()-t,4)
        try:
            for domain,title,job in SCENARIOS:
                nonce=uuid.uuid4().hex[:10];row={'domain':domain,'user_job':job,'nonce':nonce,'requests':[],'checks':[]};results.append(row)
                try:
                    nb,_=call('/api/notebooks',{'name':domain+' '+nonce});nid=nb['notebook']['id'];p=f'/api/notebooks/{nid}'
                    created,seconds=call(p+'/records',{'kind':'work_item','display_name':title+' '+nonce,'status':'planned'});rid=created['record']['id'];row['requests'].append({'action':'independent_record','seconds':seconds,'response':created})
                    ans,seconds=call(p+'/query',{'question':f'Apa status item dengan ID {rid}?'});row['requests'].append({'action':'db_only','seconds':seconds,'response':ans});row['checks'].append({'case':'db_only','pass':ans.get('route')=='db_only' and any(r.get('id')==rid for r in ans.get('records',[]))})
                    body=f'Notulen rapat operasional\n\nPeserta: Sari.\nKeputusan: {title} dengan ID {rid} direncanakan mulai 23 November. Kode {nonce}.\n'
                    doc,seconds=call(p+'/documents',{'filename':'baru-'+nonce+'.txt','text':body});row['requests'].append({'action':'unseen_document','seconds':seconds,'response':doc})
                    ans,seconds=call(p+'/query',{'question':f'Apa status item dengan ID {rid} dan bukti dari dokumennya?'});row['requests'].append({'action':'combined','seconds':seconds,'response':ans});row['checks'].append({'case':'combined','pass':ans.get('route')=='combined' and any(r.get('id')==rid for r in ans.get('records',[])) and any(rid in c.get('quote','') for c in ans.get('claims',[]))})
                    other,_=call('/api/notebooks',{'name':'isolated '+nonce});ans,seconds=call(f'/api/notebooks/{other["notebook"]["id"]}/query',{'question':f'Apa status item dengan ID {rid}?'});row['requests'].append({'action':'isolation','seconds':seconds,'response':ans});row['checks'].append({'case':'isolation','pass':not any(r.get('id')==rid for r in ans.get('records',[]))})
                except Exception as exc:row['error']=str(exc);row['checks'].append({'case':'journey_completed','pass':False})
                finally:(out/'results.json').write_text(json.dumps({'protocol':protocol,'time':dt.datetime.now(dt.timezone.utc).isoformat(),'scenarios':results,'business_value':'not_measured','real_user_validation':False},ensure_ascii=False,indent=2))
        finally:server.shutdown();server.server_close();thread.join(timeout=3);st.close()
    print(json.dumps({'scenarios':len(results),'checks_passed':sum(c['pass'] for r in results for c in r['checks']),'checks_total':sum(len(r['checks']) for r in results),'report':str(out/'results.json')}))

if __name__=='__main__':main()
