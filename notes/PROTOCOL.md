# Frozen first evaluation protocol

Freeze this file and the runner in Git before running `evaluation`.
The mechanism, timing, comparators and costs are as specified in DESIGN.md.
The unchanged development recipe passed acquisition (DEVELOPMENT.md).

## Material and conditions

- Five new initialization/stream seeds 0–4, disjoint from development 90–91.
- Ranks 2,4,8 × expected or broad objective × rho=0 or .8: 60 learned fits.
- 1,200 Adam updates, lr=.02, no weight decay, batches of 32 eight-record
  histories generated afresh each step. Initialization E ~ Normal(0,.1).
  Data stream seed=10000+model seed, paired across ranks/objectives and rho.
- For each seed and rho, 2,048 test histories (16,384 records), generated with
  seed 700000+seed. All branches and ranks share these histories. Probe fits
  use 1,024 separate histories (8,192 records), seed 700100+seed. Gaussian
  draws are shared across rho before applying the correlation transform.
- Test histories are first generated only after protocol freeze. Development
  used seeds 900090–900091 and 900190–900191 for test/probe material.
- Rho=.8 is an explicitly uncalibrated extension testing whether changed-field
  prediction can arise from retained correlated expected fields. The .8
  correlation is known to the generator/investigator and visible in histories,
  but no changed-field query loss is supplied to expected-objective training.

Queries conceptually arrive after all writes. Evaluation enumerates every
key/field rather than sampling queries; querying either family cannot change
state. This is an expected distribution vs disjoint field-family shift, not a
claim that all aspects of the new goal were unknown to the experiment designer.
Broad self-supervision sees all input field values; explicit balanced storage
knows the field schema. Changed-first control receives family identity before
writing. No reference history is accessible through ordinary read functions.

## Measures and claims to test

MSE averaged over four fields and eight records per episode; expected and
changed measured separately. Each field has population variance one, so a
zero prediction has population MSE one. No classification accuracy proxy.

Primary, rho=0:
1. Expected-only rank 4 acquires expected questions (<.01 MSE), while changed
   questions have materially larger error under both ordinary and probe reads.
2. At rank 8, expected-only ordinary changed error is higher than probe error;
   positive recovery from an unchanged state establishes a reader limitation.
3. At matched rank 4, broad learning and balanced explicit storage trade some
   expected performance for changed performance. Expected-first explicit
   storage fails changed use too, constraining storage-medium explanations.

Secondary: correlated rho=.8, rank 2 capacity floor, random orthogonal storage,
full records, query-known changed-first control, and initial vs final probes.
No significance-based stopping or selection. Report all seeds and conditions.
Means and seed ranges are descriptive; paired differences use all five seeds.
A seed bootstrap (10,000 resamples, seed 20260914) provides descriptive 95%
intervals, not a strong small-sample population inference or 81,920 independent
training replications. Unit is a trained-seed/data block.

The privileged decoder uses CPU float64 least squares (gelsd, rcond=1e-12), no
intercept (known zero population mean), all eight target fields, and a new
8,192-record supervision budget per representation. Preserve readout weights.
Ideal Gaussian residual covariance uses SVD of L^T E, Sigma=L L^T, retaining
singular values above relative 1e-12. This bounds ideal real-valued linear
observations under this Gaussian generator, including nonlinear readers;
float32 rounding is not covered by an exact continuous-information theorem.
Actual probe results on float32 stored states supply the empirical check.
Do not equate failed probes alone with absence of information.

## Resource accounting and verification

E has 8r float32 scalars (32r bytes), shared across episodes and used as the
reader transpose. Fast state W has 8r float32 scalars (32r bytes) per episode.
Explicit compressed records have the same 32r payload bytes; full records use
256. Public key schema is fixed, so no per-record key payload. Explicit field
indices are shared configuration, not zero-cost arbitrary discovered metadata.
Dense explicit projections in the harness are a common evaluation interface;
actual explicit storage needs only field copies and field-index lookups.
Training Adam moments require 2×E bytes plus E gradients, discarded before
writes. No hidden history or optimizer state persists between episodes.

Generic dense projection costs 8r multiply-accumulates per record, with an
8-by-r state SGD update; one-hot keys admit an r-scalar row replacement.
Ordinary learned single-field read costs r multiply-accumulates. Explicit
storage writes r scalars per record and reads one selected scalar (or zero).
There are 307,200 training records and 1,200 optimizer steps per learned fit;
outer forward uses 16r multiply-accumulates per record plus backward and Adam.
No computation matching is claimed. Report loop time and write/read timing
separately, treating microsecond-scale CPU timings as descriptive only. Probe
solve excludes feature extraction; extra writing and readout storage are
charged separately. Labels are copied from history, with zero teacher calls.

Verification reloads saved E/readouts, regenerates data and state hashes,
recomputes metrics, checks expected acquisition and full-record control,
checks source/protocol/lock hashes, and supplies an independent linear algebra
check of projection/covariance. All matrices are small enough to retain in JSON;
no excluded model file is necessary to reproduce results. Freeze a manifest
before the loop, preserve curves and output for every fit, and retain any
failed attempts. A new claim developed from this evaluation requires fresh
material for its test.
