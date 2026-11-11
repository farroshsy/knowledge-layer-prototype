"""One bounded Grok research synthesis from coordinator-verified primary sources."""
import datetime as dt
from pathlib import Path
import json
from automation.context_hub import REFS,RISKS,ROOT
from automation.council import Supervisor
from automation.challenge_council import SCHEMA

def main():
    run=ROOT/'.research-review'/dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    s=Supervisor(ROOT,run,max_calls=1,max_hours=.2,provider_timeout=480)
    prompt='Read-only research synthesis. The coordinator opened these primary sources; you have no browser/tools. Do not claim you read additional pages. Cite only supplied URLs; distinguish source-backed general guidance from proposed project-specific controls. No code edits or new architecture frameworks. Deadline tomorrow 08:00 WIB: app delivery stays primary. Produce a concise risk-to-acceptance matrix in findings, experiments with exact expected behavior and evidence requirements, and unresolved human decisions. Cover business workflow, data quality, identity, temporal claims, provenance, retrieval, supported assertions, parser/file security, prompt injection, SQL/scope, subprocess, timeouts/fallback, persistence, privacy, operational metrics, reproducibility, accessibility and ROI. Do not claim exhaustive audit or compliance. Prioritize demo blockers, then before real-data pilot, then conditional productization.\nPRIMARY SOURCE NOTES\n'+json.dumps(REFS)+'\nCURRENT RISK REGISTER\n'+json.dumps(RISKS)+'\nACTUAL CURRENT EVIDENCE\n'+(ROOT/'.context-hub/MEMORY.md').read_text()
    obj=s.call('primary-research-review',prompt,SCHEMA,run)
    out=ROOT/'research/reliability-research-review.md'
    text=['# Reliability research review — Grok synthesis','Source notes were fetched by coordinator; this worker had no independent browser. Recommendations are not implemented controls or executed tests.',obj['summary']]
    for title,key in [('Findings','findings'),('Proposed falsification checks','experiments'),('Open decisions','open_decisions')]:
        text.extend(['\n## '+title,*['- '+x for x in obj[key]]])
    text.extend(['\n## Primary references',*['- ['+title+']('+url+') — '+note for _,title,url,note in REFS]])
    out.write_text('\n\n'.join(text));print(out,flush=True)

if __name__=='__main__':main()
