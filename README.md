# Memory under goal shift

**Status: first publication accepted; empirical follow-up commissioned, 14 September 2026.**
Read [FINDINGS.md](FINDINGS.md) for the completed linear study and
[FOLLOWUP.md](FOLLOWUP.md) for the current investigation: test whether its
selection-versus-reader distinction survives relaxing one consequential
simplification. Follow-up preparation has not run experiments.

This independent ancillary study asks **what learned memory retains for later
uses that differ from the goals anticipated during memory formation**. It
contributes to Construct-2's [S4 question](../../construct-2/studies/README.md#s4-what-does-learned-memory-lose-when-the-future-goal-changes).
Preparation ran no experiments; the subsequent investigator session performed
methods reading, acquisition calibration, a fresh bounded comparison, and an
explanatory explicit-compression control. Source studies and root documents
were left unchanged.

The experiment separates three cases: expected-goal acquisition, information
unavailable through a capacity-limited write projection, and a reader unable
to recover retained information. A simple linear test-time memory permits
both actual gradient writes and an analytic Gaussian diagnostic. It is a local
mechanism study, not a reproduction of a complete language-model method.

## Evidence

| Stage | Protocol / methods | Evidence |
| --- | --- | --- |
| Focused reading | [Versioned sources and author-code inspection](sources/README.md) | [Provenance](sources/provenance.json), [metadata cache](sources/metadata.xml) |
| Acquisition | [Design and resource envelope](notes/DESIGN.md), [development observations](notes/DEVELOPMENT.md) | [12 fits](analysis/development/), [gradient/write checks](analysis/preflight.json) |
| Fresh comparison | [Frozen protocol](notes/PROTOCOL.md) | [60 fits](analysis/evaluation/), [all-condition tables](analysis/TABLES.md), [summary](analysis/summary.json) |
| Explicit derived records | [Supplement protocol](notes/SUPPLEMENT_PROTOCOL.md) | [30 fresh-history evaluations, no new training](analysis/supplement/results.json) |
| Publication | [Findings](FINDINGS.md), [exportable figure](analysis/comparison.pdf) | [Verification](analysis/verification.json), [costs](analysis/costs.json) |

The first evaluation was frozen in Git commit `1081c78` after development;
the supplement in `39d6095` after the first evaluation. Failed-capacity cases
remain included. All learned matrices, diagnostic readers, curves, hashes,
seeds and configuration are retained locally in versioned JSON. No excluded
checkpoint, source checkout or remote service is required to inspect evidence.

## Reproduce

Use `uv` with the committed lockfile. Runtime: Python 3.14.7, PyTorch 2.14.0,
NumPy 2.4.6; local CPU, float32 writes, float64 diagnostic readers, one thread.

```sh
uv sync --locked
uv run --locked scripts/verify.py
uv run --locked scripts/summarize.py
```

Verification regenerates data and recomputes stored-state hashes and metrics,
including the supplement, without retraining. Summarization regenerates the
complete tables and PNG/PDF comparison. Timing fields and PDF metadata can
vary on rerun. The original data-generation/learning runner and protocols are
hash-checked; small numerical differences across libraries/hardware may require
inspection rather than silently relaxing the checks.

For an optional full training replay, supply a new destination that does not
already exist:

```sh
uv run --locked scripts/replay.py --stage evaluation --destination /tmp/memory-goal-shift-replay
```

This copies the frozen recipe to that directory, generates the 60 fits there,
and leaves original evidence intact. Change `--stage` to `development` and use
a different new destination to replay calibration. Original runners refuse to
overwrite existing manifests. The supplement is executable with
`scripts/supplement.py` in a fresh study copy containing the evaluation donors.

## Starting methods and remaining scope

The [source ledger](sources/README.md) records exact versions, reading scope,
retrieval details, and the distinction between published methods and our local
simplification:

- [PERK, 2507.06415v3](https://arxiv.org/html/2507.06415v3): context adaptation
  trained for a distribution of later reasoning questions.
- [TTCD, 2608.01672v1](https://arxiv.org/html/2608.01672v1): longer-window teacher
  supervision of a shorter-window student's fast weights.
- [Self-Guided TTT, 2607.09415v1](https://arxiv.org/html/2607.09415v1): question-known
  span selection, full-context answering, per-instance reset.
- [TTT layers, 2407.04620v4](https://arxiv.org/html/2407.04620v4): learned label
  views and gradient-updated recurrent state; the elementary implementation lead.

The sibling [neural-memory-depth](../neural-memory-depth/README.md) supplied
pinned reading artifacts, but no executable dependency. The first study reached
explanatory closure within its linear setting. The commissioned
[follow-up](FOLLOWUP.md) extends that setting while preserving the accepted
publication and evidence. [AGENTS.md](AGENTS.md) retains the operating
instructions and available resources. Root synthesis remains separate under
the [ancillary-study approach](../../construct-2/notes/ANCILLARY_STUDY.md).
