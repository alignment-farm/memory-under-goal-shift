# Nonlinear follow-up

Completed 14 September 2026. Read [FINDINGS.md](FINDINGS.md) for the result,
[design](notes/DESIGN.md), [diagnosis](notes/DIAGNOSIS.md), and
[frozen protocol](notes/PROTOCOL.md) for methods. Freeze commit: `c273ec9`.
The original study and accepted evidence remain unchanged.

From the study root, with the original pinned `uv.lock`:

```sh
uv sync --locked
uv run --locked python followup/scripts/verify.py
uv run --locked python followup/scripts/summarize.py
uv run --locked python followup/scripts/moments.py
```

Verification reloads all stored networks and independently checks finite-state
conditional risks without retraining. Summarization regenerates tables, costs,
PNG and PDF. The final command regenerates the post-evaluation algebraic
explanation of the nonlinear reader constraint. Timings and figure metadata
can vary. No excluded checkpoint is required.

For an optional full replay, choose a destination that does not exist:

```sh
uv run --locked python followup/scripts/experiment.py evaluation --destination /tmp/nonlinear-memory-replay
```

Use `development` instead for calibration. The runner refuses existing evidence
directories. The privileged acquisition diagnosis is preserved in
`analysis/diagnosis.json`; rerun `scripts/diagnose.py` in a fresh copy with that
output absent. This program also refuses to overwrite its evidence.

No experiment uses an external model or shared training machine. Metadata
access failures and exact source provenance are in [sources](sources/README.md).
