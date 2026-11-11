"""Bounded repair of source-verified review blockers, with micro and macro gates."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from automation.council import Supervisor,MANIFEST,REVIEW,validate_manifest,write_snapshot,source_snapshot,fingerprint,make_diff,atomic_json,evaluate_staging,GateError
ROOT=Path(__file__).resolve().parents[1]

def main():
    seed=ROOT/'.parallel-builds/20261110-214747-9bf46f/candidate-1';base=source_snapshot(seed)
    run=ROOT/'.parallel-builds'/('repair-'+dt.datetime.now().strftime('%Y%m%d-%H%M%S'));s=Supervisor(ROOT,run,max_calls=6,max_hours=1,provider_timeout=480);s.model_overrides={'targeted-query-repair':'grok-4.7-build-fast','repair-contract-review':'grok-4.7-build-fast'}
    pinned=run/'pinned-tests';write_snapshot(pinned,{k[6:]:v for k,v in s.origin.items() if k.startswith('tests/')})
    reviews=[json.loads((seed.parent/(k+'.json')).read_text()) for k in ['integration-integrity-review','integration-contract-review']]
    macro=json.loads((ROOT/'.acceptance-runs/macro-business-v1/results.json').read_text())
    evidence={'review_findings':reviews,'macro_expectations':macro['protocol'],'macro_checks':macro['checks'],'actual_combined_responses':[q['response'] for r in macro['scenarios'] for q in r['requests'] if q['action']=='combined']}
    summary='''Repair only proven integration blockers. Preserve all existing tests; do not game the macro questions or expand unrelated claims to satisfy a nonce. Exact/whole-token names: Budi must not match Budiono; overlapping full names should not spuriously merge. Docs-only must have route document_only and its original selected claims, not every sibling claim in a source. Combined route requires exact stable record-id evidence; support ordinary Indonesian suffix/paraphrase such as dokumennya. Do not confuse plan with occurrence/nonoccurrence. No arbitrary SQL or extra dependencies. Keep explicit method/fallback. Add meaningful focused regressions; do not weaken assertions. You may output at most THREE files, only klayer/business_query.py, klayer/static/index.html (only route label changes if needed), tests/test_query_regressions.py. Domain extraction already emits source sentences; diagnose rather than assume missing claims. User-supplied X interpretation advocates domain contracts and stage-specific evidence metrics, not a graph-engine rewrite. Deliver code JSON manifest only.'''
    s.state['status']='repairing';s.event('targeted-repair-start',seed=str(seed),reason='independent review and macro failures')
    previous={}
    try:
        for attempt in range(2):
            selected={k:base[k] for k in ['klayer/business_query.py','klayer/domain.py']}
            ui=base.get('klayer/static/index.html','');selected['UI_ROUTE_RELEVANT_EXCERPTS']='\n'.join(line for line in ui.splitlines() if any(w in line for w in ['db_only','combined','unsupported','route']))
            prompt=summary+'\nEVIDENCE\n'+json.dumps(evidence)+'\nPREVIOUS TEST FAILURE\n'+json.dumps(previous)+'\nRELEVANT SOURCE\n'+s.context(selected)
            result=s.call('targeted-query-repair',prompt,MANIFEST,run/f'attempt-{attempt}');validate_manifest(ROOT,result['files'])
            owned={'klayer/business_query.py','klayer/static/index.html','tests/test_query_regressions.py'}
            if len(result['files'])>3 or any(f['path'] not in owned for f in result['files']):raise GateError('repair ownership violation')
            proposed=dict(base)
            for f in result['files']:proposed[f['path']]=f['content']
            stage=run/f'candidate-{attempt}';write_snapshot(stage,proposed);sha=fingerprint(source_snapshot(stage));s.state['status']='testing';s.event('repair-tests-start',attempt=attempt)
            checks=evaluate_staging(stage,legacy_tests=pinned,check=s.check);atomic_json(run/f'tests-{attempt}.json',checks)
            out=run/f'macro-{attempt}'
            cmd=[sys.executable,'-m','automation.macro_business_eval','--source',str(stage),'--out',str(out)]
            executed=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=120)
            m=json.loads((out/'results.json').read_text()) if (out/'results.json').exists() else {'error':executed.stderr[-2000:]}
            good=bool(m.get('scenarios')) and len(m['scenarios'])==3 and all(len(r['checks'])==3 and all(c['pass'] for c in r['checks']) for r in m['scenarios'])
            atomic_json(run/f'macro-summary-{attempt}.json',{'passed':good,'report':str(out/'results.json'),'stdout':executed.stdout,'exit_code':executed.returncode})
            if fingerprint(source_snapshot(stage))!=sha:raise GateError('tests changed candidate source')
            if not checks['passed'] or not good:
                previous={'unit':checks,'macro':m};base=proposed;s.event('repair-checks-failed',attempt=attempt);continue
            diff=make_diff(source_snapshot(seed),proposed);h=hashlib.sha256(diff.encode()).hexdigest();(run/'candidate.diff').write_text(diff)
            prompt='Independently review this exact repair diff against existing blockers. Return exact diff_hash '+h+'. Reject correctness/security/scope gaps and test weakening; no new future features. Passing rules checks is not real-model or broad product validation.\nORIGINAL FINDINGS\n'+json.dumps(evidence)+'\nTEST RESULTS\n'+json.dumps(checks)+'\nDIFF\n'+diff+'\nCURRENT BUSINESS QUERY MODULE\n'+proposed['klayer/business_query.py']
            s.state['status']='reviewing'
            with cf.ThreadPoolExecutor(max_workers=2) as pool:rs=[f.result() for f in [pool.submit(s.call,r,prompt,REVIEW,run) for r in ['repair-integrity-review','repair-contract-review']]]
            if any(r.get('diff_hash')!=h or r.get('verdict')!='approve' for r in rs):raise GateError('repair review rejected')
            s.check();pointer={'release':str(stage),'source_hash':sha,'tests':'pass','synthetic_macro':'9/9','reviews':'two approve','remaining':'real-model macro, browser usability, formats, production controls not certified'}
            atomic_json(ROOT/'.parallel-builds/latest-reviewed.json',pointer);s.state.update(status='candidate_ready',accepted=1,latest_release=str(stage));s.event('repair-candidate-ready',**pointer);return
        raise GateError('repair acceptance not met')
    except Exception as exc:s.state['status']='blocked';s.event('repair-failed',error=str(exc)[:500]);raise

if __name__=='__main__':main()
