# Nonlinear value selection — development plan

14 September 2026. Preserve the accepted linear study. Local CPU, one Torch
thread, no endpoint or shared training machine. Envelope: two hours, 16
development fits and 20 evaluation fits, <=3,000 Adam updates each, <2 GB RAM.
No teacher, paid model calls or external training service.

Relax the linear value map and linear task: a record has four independent
uniform signs (a,b,c,d). Expected queries ask ab or cd; changed queries ask an
individual sign. Eight independent keyed records form a history. Fixed one-hot
addressing remains. The investigator knows both families. Expected training
knows only parity targets; broad training reconstructs the four raw inputs.
Actual query key, family and coordinate are absent from the write interface.

The slow encoder is an MLP 4→32→r with tanh hidden activations; its outputs are
thresholded to r signs, r in {2,4}. A straight-through tanh surrogate supplies
outer gradients. The ordinary decoder is an MLP r→32→4 (tanh hidden, linear
output). It predicts raw signs; expected answers are products of its first
two or last two predictions. Thus expected training updates the entire reader
through nonlinear products; there is no deliberately untrained output head.
Adam lr=.01, batch 128 records, 2,000 updates initially, seeds 90,91.

The mutable episodic state W has eight rows of r exact float32 signs. Starting
from zero, a unit SGD update on half squared error for each orthogonal key
writes its encoded sign vector. Read-only state persists for all questions;
reset at the next history. Slow networks persist; history, logits, activations
and optimizer are unavailable at reading. Training uses the equivalent direct
encoded rows. Exact +/-1 storage avoids hidden information in tiny real-valued
components. Report implemented bytes (32r per history) and semantic capacity
(8r bits); the implementation does not bit-pack either learned or explicit
states. This changes precision as well as nonlinearity and must be disclosed.

Development must establish expected parity MSE <.05 in at least one bounded
regime and broad raw MSE <.05 at r=4. Retain failures; diagnose capacity,
optimization and reader separately. Freeze a recipe before fresh evaluation
seeds/histories. Finite support has only 16 record types; fresh histories and
seeds are independent draws, not unseen record types or goal structures.

Diagnostics on the same frozen states: (1) empirical lookup reader trained on
512 separate histories with all six target labels; (2) privileged exhaustive
lookup using uniform probability over all 16 inputs. Conditional target means
minimize squared error among every state-only reader, including nonlinear
readers. Enumerated exact collisions establish residual uncertainty for this
finite noiseless distribution; a failed learned probe alone would not.
Both readers know the changed family, incur extra storage/fit computation,
and never alter the encoder or episodic state.

Competent explicit controls: two parities, two raw signs (a,c), and hybrid
(ab,c) at two slots; all raw signs at four; invertible nonlinear (ab,a,cd,c)
at four. Give explicit parity code a canonical ordinary raw decoder (1,ab,1,cd),
so it acquires expected questions. Give the invertible code a canonical
reader that ignores the orientation signs, plus its exact inverse alternative.
Disclose those supplied structures. This last reader contrast is an engineered
positive audit, not evidence for learned-reader failure. Apply identical
empirical/exhaustive diagnostics to all controls. Match episodic payload only,
not total system compute or parameter bytes. No storage-medium advantage claim.
