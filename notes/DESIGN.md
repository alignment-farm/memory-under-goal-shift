# Initial design and resource envelope — 14 September 2026

Question: when a learned write projection is optimized for one set of record
fields, which other fields remain recoverable after an episode is written?
This is a deliberately linear, synthetic mechanism study, not a reproduction
of PERK, TTCD, or the complete published TTT-Linear language model. It removes
key interference so acquisition, value selection, and reader failure can be
separated. No novelty claim is planned.

Local CPU only, one torch thread, at most 60 outer fits in the initial final
comparison plus 12 development fits, at most 2,000 updates per fit, under 2 GB
resident experiment data, and a two-hour wall-clock envelope. No shared Mac
Studio, endpoint, teacher, API model tokens, or paid training. Additional work
must be recorded as a bounded amendment.

History: eight records, each containing eight real scalar fields. Records use
fixed public one-hot keys. Four independent standard-normal fields a and four
fields b = rho*a + sqrt(1-rho^2)*noise, rho in {0, .8}. Expected goals ask for
fields 0–3; changed goals ask for fields 4–7. Both are evaluated on the same
frozen state. Entire histories contain all eight fields, but neither the query
key nor query field is supplied to the write function. The investigator knows
both distributions; expected training uses only expected query losses. A broad
reconstruction control uses all input fields as self-supervised targets, with
no actual future query. Correlation is present in the training histories too.

Slow learned state E is 8 by r, r in {2,4,8}; it also supplies the tied reader
E^T. Episodic mutable state W is 8 by r and resets to zero between histories.
For key k and record x, one SGD step at rate 1 on half squared error
||k^T W - xE||^2 writes W <- W - k(k^T W-xE).
With orthogonal keys used once, W=X E. The reader gets W, E, query key/field,
and no history, optimizer state, or write activations. Ordinary answer is
(k^T W E^T)[field]. W is fixed across all subsequent reads. This is compression
at the write interface, not evidence of forgetting previously stored episodes.

Outer training minimizes expected-field MSE or all-field reconstruction MSE.
No teacher, labels other than input record values, pretrained parameters, or
additional context. Tied projection/reader is a local simplification; fixed
keys, no normalization/gating/residual, zero fast initialization, and online
unit-rate SGD differ from published TTT-Linear. Orthogonal keys let training
use the algebraically identical X E E^T shortcut; a gradient audit will check
this against sequential differentiable SGD, including repeated-key overwrite.

Controls at the same r float32 slots per record: explicit expected-first fields
(order 0,1,2,3,4,5,6,7); explicit balanced fields (0,4,1,5,2,6,3,7); fixed random
orthogonal projection with tied reader; full eight-field records. Unstored
explicit fields ordinarily predict zero. A query-known family control stores
changed-first fields (4,5,6,7,0,1,2,3), supplied the family before writing; this
is hindsight, not goal-blind performance or exact-query optimal storage.

Diagnostic reader: fit unregularized linear least squares on separately
sampled histories with all field labels after freezing E. This privileged
reader has a new distribution/data/compute budget and never updates E or W.
Also compute the ideal Gaussian conditional covariance given the linear
projection. This is a mathematical diagnostic under the known distribution,
not deployed performance. For full-rank float32 states, actual recoverability
must be tested rather than inferred from ideal arithmetic. Preserve singular
values, fitted readouts, per-seed metrics, and initial/final projection probes.

Development first: seeds 90,91; ranks 2,4,8; rho=0; both objectives. Retain
learning curves and acquisition outcomes. Freeze final protocol and hashes
before generating fresh final histories. Development success criterion for
r>=4 expected objective: expected MSE <.01 vs zero-prediction MSE near 1.
Rank 2 cannot preserve four independent expected coordinates exactly and is
a capacity diagnostic. No success requirement is imposed on changed goals.
