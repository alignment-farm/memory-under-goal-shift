# Methods reading and provenance

14 September 2026. This investigation is a new synthetic experiment, not a
reproduction of any paper's language-model results. It makes no novelty claim.

| Source | Exact version and reading scope | Consequence for this design |
| --- | --- | --- |
| [TTT layers](https://arxiv.org/html/2407.04620v4) | 2407.04620v4, §§2.1–2.3, 2.6; equations 1–5 and Figure 5 | Learned label view determines what a fast weight update receives; separate slow projection from episodic fast state. Linear SGD admits an inspectable minimal case. |
| [PERK](https://arxiv.org/html/2507.06415v3) | 2507.06415v3, §3 and Appendix B adaptation/data collation paragraphs | Context-only LoRA adaptation followed by context-free question answering; outer objective learns a reasoning distribution. Our question overlaps this motivation, but tests changed field use in a much smaller mechanism. |
| [TTCD](https://arxiv.org/html/2608.01672v1) | 2608.01672v1, abstract and §3 context-distillation equations and in-place fast weights | Long-window causal teacher supplies hidden-state targets to short-window student. Teacher sees more history, not noncausal future tokens. Our experiment has no teacher and does not test TTCD. |
| [Self-Guided TTT](https://arxiv.org/html/2607.09415v1) | 2607.09415v1, §2.1–2.2 and Algorithm 1 | Span selection receives current question; answering still conditions on full context; weights reset each instance. It motivates disclosing hindsight in the query-known control, not a claim of goal-blind compression. |

TTT HTML and section extraction were copied unchanged from the sibling
neural-memory-depth study. Their exact file hashes and sibling Git revision
are in `provenance.json`. The sibling's source-loaded implementation checkout
was not present at the documented path during this session. No sibling code
or experiment output is used by our executable experiment.

Other HTML was fetched from exact versioned URLs. `retrieval.json` retains
URLs, response headers/status, timestamps and hashes. One batch metadata GET
to `https://export.arxiv.org/api/query` returned HTTP 200. It used a descriptive
User-Agent, one connection, and no retries or other API/OAI requests. No
requests within three seconds of another API/OAI request were made by this
investigator. `metadata.xml` is the complete cached response. No search engine
was used for arXiv discovery/metadata. The metadata versions resolve to:

- TTT v4 updated 2025-08-31T18:32:59Z.
- PERK v3 updated 2026-08-31T15:26:53Z.
- TTCD v1 submitted/updated 2026-08-03T04:06:06Z.
- Self-Guided TTT v1 submitted/updated 2026-07-10T13:45:56Z.

## Closest implementation inspection

Author tutorial implementation:
[test-time-training/ttt-lm-pytorch](https://github.com/test-time-training/ttt-lm-pytorch/tree/cd831db10c8c9a0f6340f02da5613316a8a92b67),
revision `cd831db10c8c9a0f6340f02da5613316a8a92b67` (2024-07-14).
The GitHub commit API response is cached as `official-repo.json`; the pinned
`ttt.py`, README and MIT license are retained with `official-` prefixes.
Inspected `TTTLinear` lines 918–1058: learned initial W1/b1, reconstruction
target XV-XK, normalized squared-loss derivative, dual/primal updates, cached
state and outputs; also located projections and per-token learning-rate gates.
The README explicitly identifies this as a tutorial implementation. It is
older than paper v4; we do not infer exact v4 configuration parity.

Our `scripts/experiment.py` implements the paper's elementary linear SGD
formulation independently. It does **not** load the official module or claim
numerical equivalence to its normalized, residual, gated language-model layer.
It uses fixed orthogonal keys, rectangular zero-initialized fast weights,
a tied learned label projection/readout, no normalization, no bias, and a
fixed rate of one on half squared error. This choice isolates value selection
and supplies an analytic recoverability diagnostic; it cannot assess long
sequence key interference or natural-language reasoning.

The initially attempted web open at `test-time-training/ttt-lm` returned 404;
the actual author PyTorch repository above was acquired directly. This access
failure did not influence the experiment. Author-reported benchmark numbers
are not used as local evidence.
