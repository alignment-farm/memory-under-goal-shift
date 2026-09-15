# Third-phase design, 15 September 2026

## Decision and envelope

Extend calibrated frozen writers to new cross-record compositions, rather than
relearn addressing or optimize another bottleneck. Local CPU, one Torch thread,
no external teacher or service, at most 10 minutes execution and 100 MB evidence.
Use all four-slot donors: development 90/91 and fresh-history evaluation 0–4,
expected and broad objectives. Donors are from accepted commit
0d516aaa82d30d07e239b44e88ac43b5fdbfddef.
No donor selection based on this phase's results; two-slot failures remain in
the prior publication, outside this functioning-regime extension.

## State and access

32 ordered fixed-key events, each four iid uniform signs a,b,c,d: history support
16^32. The encoder and decoder are the previously trained 4→32→4 tanh MLPs.
Writer emits four exact signs. Each row of a zero-reset float32 matrix receives
one unit SGD step on half squared row reconstruction error. State is 32×4,
512 bytes / 128 semantic bits, persists for the episode's reads only. No raw
history, logits, gradients or optimizer state reaches a reader. Shared frozen
weights persist between episodes. Fixed positional addressing is supplied.
Prior writer training used individual records and local ab,cd losses (expected)
or raw reconstruction (broad); it never used a cross-record label.

## Later use

After writing, draw four distinct event keys independently of values. Expected
queries request ab and cd at the first key. Changed queries request (1) a parity
across the first two keys, (2) a parity across all four, and (3) whether the first
two records agree in BOTH a and b, encoded +1 yes/−1 no. These are complete
composed answers, not raw-coordinate scores. Histories and query tuples are new
random draws; individual record types and primitive multiplication are familiar.
There is no enforced disjointness of finite tuples between development and test;
what is withheld from writer training is the entire cross-record task family.
No claim of unseen atomic types, learned reasoning or unknown operators.

Ordinary reader: supplied query algebra composed with frozen decoded raw fields.
Also report clipping its complete answer to [−1,1], a no-supervision repair.
Fitted alternative: conditional a,b,c,d,ab,cd moments per code, estimated from
4096 fresh single records after writer freeze. Supplied independent-record query
algebra multiplies a moments for parity and uses a,b,ab moments for agreement.
These readers know every operation and query at read time; neither writer knows
actual queries at write time. Fitted reader gets extra labeled raw evidence,
including local parity labels, but no composed training labels. No teacher.

Exact diagnostic: enumerate 16 local records for each frozen code. Independence
and recordwise writes imply posterior factorization across distinct keys. Pair
agreement uses E[ab|z], NOT E[a|z]E[b|z]. Exact population parity risk at k keys
is 1−E[E[a|z]^2]^k. Agreement is checked by exhaustive 256 record pairs. These
are valid full-history optima only under the specified iid distribution and
fixed distinct keys. A finite fitted reader failure alone implies no loss.

## Controls, calibration and outcomes

Explicit full raw records (four slots) and explicit local parities (two slots),
with competent exact moment readers. The latter's smaller payload is disclosed.
Complete evidence must give exact composed answers. Expected acquisition gate:
population ordinary local parity MSE <1e−5 for each donor. Broad recovery gate:
all 16 input types have distinct codes. Development uses 512 histories per donor;
fresh evaluation uses 8192, five seed blocks. Metrics: MSE, whole-answer binary
accuracy (threshold >=0 means +1), empirical risk decomposition, population
irreducible MSE. Agreement majority baseline is accuracy .75 and MSE .75 with
mean prediction −.5; parity baselines .5 and 1. Report per-seed outcomes, no
query-level pseudo-replication. All attempts retained; freeze after development.

Costs include original donor training (sunk and charged-from-scratch separately),
new writer calls, ordinary decode, fitted reader construction and reads, exact
diagnostic construction and reads; batch timings descriptive, not a benchmark.
Storage includes shared parameters and moment tables; no equal-quality economy
claim from differing incomplete answers. Full raw explicit retention supplies
both indexing and query procedures without learning.
