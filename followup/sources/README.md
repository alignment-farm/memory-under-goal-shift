# Focused methods reading

14 September 2026. No novelty or full-method reproduction claim.

- **TTT layers, 2407.04620v4**, reread §§2.1–2.3 and 2.7 in the accepted
  study's cached HTML/section text. Inspected the author tutorial `TTTMLP`
  implementation, `sources/official-ttt.py` lines 1073–1210, at upstream
  `cd831db10c8c9a0f6340f02da5613316a8a92b67`. It has two mutable weight
  matrices, GELU, residual/normalized reconstruction, and per-token update
  rates. Our extension instead makes the slow write map and read map nonlinear,
  retaining the simple orthogonal-key gradient write. It is **not TTT-MLP**.
  No implementation is imported; the accepted source files remain unchanged.
- **Bengio, Léonard and Courville, 1308.3432v1**, abstract and §4, with §5
  inspected for scope. [Versioned full text](https://arxiv.org/html/1308.3432v1)
  cached here. Straight-through gradients are biased surrogates for hard
  decisions. Our deterministic sign forward pass with tanh derivative backward
  is a local variant, not a reproduction of stochastic gating experiments.
  No author benchmark number is used as local evidence.

The initial API request to `https://export.arxiv.org/api/query?id_list=1308.3432`
received HTTP 429; its body/headers were not preserved (a logging failure).
One retry, over three seconds later, timed out after 30 seconds; no response
was available to cache. No further metadata requests were made. Both used one
connection and a descriptive `MemoryUnderGoalShiftResearch/1.0` User-Agent.
The exact v1 content was then read directly; no latest-version claim or search
engine metadata discovery is made. Its HTML download returned HTTP 200.
`provenance.json` records hashes for the reading artifacts and these limitations.

The consequential choices are local: finite signs permit exhaustive collision
analysis; parity prevents a purely linear task solution; quantization makes
exact equality meaningful. This simultaneously changes distribution, task,
precision and nonlinear architecture, so it cannot isolate an effect of
nonlinearity alone.
