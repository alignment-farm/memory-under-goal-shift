# Frozen evaluation protocol

15 September 2026. DESIGN.md defines state, workload, access and costs.
Development completed with all four acquisition gates passed. Freeze runner,
donors, source hashes, design and this protocol in Git before evaluation.

Evaluate all accepted four-slot donor seeds 0–4, expected and broad, with 8192
new iid histories each. The same histories and queries pair representations
within each seed. 128 distinct calibration histories (4096 records) per seed
fit each alternative table. Seeds/base and exact generator operations are in
the runner; no development RNG streams reused. No gradient training this phase.
Prior atomic evaluation results are known, so this is fresh-history and
fresh-composition evaluation of existing writers, not independent new fits.

Use ordinary, clipped ordinary, fitted moment and exact moment readers.
Explicit full raw and two-parity states use their exact moment readers for
primary comparisons; canonical explicit decodes are recorded only as diagnostics.
Report all five tasks and all seeds, means and seed ranges, complete binary
answer accuracy and MSE; no winner selection or accuracy-based tuning.
Expected-use acquisition remains mandatory for every donor. If it fails, stop
this evaluation as a protocol failure and preserve the evidence before repair.

Analytic population risks exploit conditional independence at distinct keys.
Independently verify parity4 by all 16^4 queried record tuples and agreement by
all 16^2 pairs. Also compute exact population reader excess for agreement when
E[ab|z] is replaced by E[a|z]E[b|z], to test the development explanation.
Verify data/query/state hashes, fitted tables, metrics and sample decomposition
by a separate NumPy reader and separately specified truth operations.

Timings include encoding/write, state gather, ordinary decode/composition,
4096-record fitting with write, support-table construction and fitted/exact read.
Report these as single batch measurements with no speed or economy claim.
Original donor training is a sunk reuse cost and separately charged if rebuilt.
No teacher, remote model, shared machine or additional neural reader training.
