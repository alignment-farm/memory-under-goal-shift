# Third phase: memory for later combinations

Completed 15 September 2026. Read [FINDINGS.md](FINDINGS.md).
Protocol freeze: `06570bd`; accepted donor revision:
`0d516aaa82d30d07e239b44e88ac43b5fdbfddef`.

- [Design and resource envelope](notes/DESIGN.md)
- [Development and artifact-path repair](notes/DEVELOPMENT.md)
- [Frozen protocol](notes/PROTOCOL.md)
- [Methods and provenance](sources/README.md)
- [All fresh-history results](analysis/TABLES.md)
- [Exact population and ablation results](analysis/population.json)
- [Costs](analysis/costs.json), [verification](analysis/verification.json)
- [Standalone PDF figure](analysis/comparison.pdf)

From the study root, using the original committed lockfile:

```sh
uv sync --locked
uv run --locked python future-use/scripts/verify.py
uv run --locked python future-use/scripts/summarize.py
```

Verification regenerates histories, calibration records, queries and states;
checks pinned sources, script and protocol hashes; independently recomputes
metrics and exact conditional grouping over 16^4 query inputs for each state.
It regenerates population.json and verification.json. Summarization regenerates
tables, costs and PNG/PDF. Timing fields and PDF metadata may vary. No retraining
or remote service is needed. Python 3.14.7, Torch 2.14.0, NumPy 2.4.6, one CPU
thread; float32 state and networks, float64 moment arithmetic.

For full experiment replay into a destination that does not exist:

```sh
uv run --locked python future-use/scripts/experiment.py evaluation --destination /tmp/memory-future-use-replay
```

Use `development` and a different new directory for acquisition replay. The
runner refuses existing destinations. Seeds, hashes, tables and metrics should
match; timings may vary. Copies of every donor are retained under donors/;
the optional acquire.py verifies the exact accepted Git revision before copying
original local artifacts. It is unnecessary for normal reproduction. No source
study, accepted publication or root synthesis was modified by this phase.
