"""Advisory decision review with role-scoped evidence packets, not an autonomous board."""
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
from pathlib import Path
from automation.council import Supervisor,atomic_json
from automation.challenge_council import SCHEMA

ROOT=Path(__file__).resolve().parents[1]
ROLES={
'cto-investment-review':('Identify business/process and investment decisions: user job, build/buy, opportunity cost, conditional productization, ownership and return INCLUDING human verification time. Give decision options/unknowns/measurement gates, no fictitious ROI or x-times gain.',[(1,100),(831,965),(967,1036)]),
'staff-stack-review':('Compare current Python/SQLite, Python/Postgres, Rails/Postgres/React alignment, TypeScript backend and Rust for a measured hotspot. Evaluate boundaries, migration/handoff/security/ops and plugin provenance. Recommend what stays tonight and what evidence triggers revisiting. Do not assume company-wide stack from one repo.',[(29,166),(504,687)]),
'retrieval-evidence-review':('Critically evaluate retrieval, source/statement/proposition/finding, partial completeness, contradiction versus different event/time, deterministic versus semantic verification. Compare algorithm source notes and say which bounded benchmark could justify each. Translate legal examples into generic business docs without inventing Rakamin workflows.',[(282,556),(689,829)]),
'delivery-acceptance-review':('Convert useful ideas into at most five implementable acceptance tickets with scope, expected behavior, evidence, dependencies, and remaining limitations. Distinguish tomorrow blockers from after-demo pilot. No new enterprise scope merely because attached report suggests it. Use current artifacts as evidence, not imagined features.',[(101,232),(689,929)])}

def packet(lines,ranges):
    return '\n'.join(l for l in lines if any(a<=int(l.split(':')[0][1:])<=b for a,b in ranges))

def main():
    run=ROOT/'.research-review'/('strategy-'+dt.datetime.now().strftime('%Y%m%d-%H%M%S'))
    s=Supervisor(ROOT,run,max_calls=5,max_hours=1,provider_timeout=480)
    s.model_overrides={'delivery-acceptance-review':'grok-4.7-build-fast'}
    lines=(ROOT/'.context-hub/input-packets/perkara-architecture-review.txt').read_text().splitlines()
    notes=(ROOT/'research/stack-and-retrieval-source-notes.md').read_text()
    status=(ROOT/'.context-hub/MEMORY.md').read_text()[:12000]
    common='You are an advisory reviewer, not the real CTO or decision authority. User-supplied GPT text is conceptual secondary material, not verified Perkara implementation and not binding requirements. No tools or edits. Read your relevant source packet carefully, then check assumptions/counterexamples, then reconcile with actual project status. Output concise source-linked findings and decisions, not private deliberation. Each recommendation needs applicability, tradeoff and falsifiable next check. Existing app builders continue; do not demand broad rewrite tonight. Do not invent measured results, dates, citations or company requirements. Explicitly label source statement, inference, proposed experiment and unknown.\nVERIFIED PRIMARY NOTES\n'+notes+'\nACTUAL CONTEXT SNAPSHOT\n'+status
    atomic_json(run/'source-manifest.json',{'attachment':json.loads((ROOT/'.context-hub/input-packets/manifest.json').read_text()),'packets':{r:{'line_ranges':rs,'characters':len(packet(lines,rs))} for r,(_,rs) in ROLES.items()},'policy':'read-only advisory; no actual company authority'})
    s.state['status']='independent_role_reviews';s.event('strategy-start',reviewers=4)
    try:
        def work(role):
            task,ranges=ROLES[role];return role,s.call(role,common+'\nTASK\n'+task+'\nSECONDARY ATTACHMENT EXCERPTS WITH ORIGINAL LINE NUMBERS\n'+packet(lines,ranges),SCHEMA,run)
        with cf.ThreadPoolExecutor(max_workers=4) as pool:results=dict(pool.map(work,ROLES))
        s.state['status']='cross_review_synthesis'
        final=s.call('strategy-adjudicator',common+'\nFour independent perspectives now exist. Cross-check their disagreements rather than vote. Reject ungrounded recommendations. Produce a bounded decision map: now / next experiment / after CTO clarification, specifying ownership and evidence required. Do not change source. Include why Rust/team-aligned stack/new retrieval algorithm might or might not be selected and what invalidates recommendation.\nREVIEWS\n'+json.dumps(results),SCHEMA,run)
        atomic_json(run/'decision-map.json',final)
        out=ROOT/'research/strategy-review-latest.md';text=['# Strategy review — advisory, not implemented decisions',final['summary']]
        for title,key in [('Evidence and tradeoffs','findings'),('Experiments / acceptance tickets','experiments'),('Human decisions and unknowns','open_decisions')]:text.extend(['\n## '+title,*['- '+v for v in final[key]]])
        out.write_text('\n\n'.join(text));s.state['status']='advisory_completed';s.event('strategy-finished',recommendation_file=str(out.relative_to(ROOT)),implementation_approved=False)
    except Exception as exc:s.state['status']='failed';s.event('strategy-failed',error=str(exc)[:500]);raise

if __name__=='__main__':main()
