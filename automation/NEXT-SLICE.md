# Working PoC delivery — small executable slices

Deadline 11 November 08:00 WIB. Build the application, not additional frameworks or research documentation. Six months is conditional, not an approved roadmap.

The previous builder timed out on a broad independent-records + planner + fusion + metrics request. Each next decision MUST fit at most THREE changed files and one concrete behavior. First add independent notebook-scoped business records with stable ids through the existing Store and a small behavior test, preserving current app behavior. Do NOT attempt to add the planner, UI, metrics and business schema together. Once independent records exist, choose the next smallest API/query integration slice. Completion of this first slice does not satisfy the entire PoC.

Keep database status, document claim, proposal, and event occurrence distinct. A plan is not evidence of occurrence AND not proof of non-occurrence. Never make database content universally authoritative over document content. Preserve attribution, temporal context and ambiguity.

Final product must exercise unseen uploads, independent records, safe typed query routing and evidence from both sources. Prioritize TXT/MD and assess text PDF only when an installed parser is available. No new dependency installation from model manifests. No hardcoded fixture answers. Ordinary question paraphrases should map to bounded operations, not fixed demo sentences.

Live HTTP evaluator exists at automation/exercise_app.py and stores separate rules and Grok results under .acceptance-runs; those are external coordinator evidence, not a claim that hybrid acceptance passed. Do not mark PoV, production readiness or business ROI as proven by the PoC.
