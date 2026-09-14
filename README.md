# Memory under goal shift

**Status: Prepared for an independent ancillary session; experiments not started during preparation.**

This study asks **what information learned memory makes available when its
later use differs from the goals anticipated when that memory was formed**.
It develops Construct-2's [S4 question](../../construct-2/studies/README.md#s4-what-does-learned-memory-lose-when-the-future-goal-changes),
contributing evidence about when accumulated experience should remain in
accessible records and when a learned representation is sufficient.

The study can begin independently of procedural retention and experience
selection. It owns its workload, mechanism choice, methods, calibration,
experiments and publication. Prefer a setting beyond the current Qwen routing
tasks when feasible; a small learned-memory task is useful if its outcomes
distinguish explanations.

## Question and first empirical direction

A memory trained for expected questions might preserve broadly reusable
evidence, or favor expected uses while making other details inaccessible.
Failure on a changed goal could also arise because learning never acquired
the relevant information, or because the reader cannot use information still
present. These explanations require different evidence.

A starting comparison gives branches the same history, forms memory, then
reveals either an expected use or a changed goal that requires evidence in that
history. Compare a usable learned memory with a compact explicit representation
and an evidence-access reference such as full context or retrieval. A
query-known-before-writing condition can measure the advantage of advance
knowledge. The investigator chooses a tractable implementation and the
smallest comparison that makes scientific contact; this sketch is not a fixed
protocol or a requirement to implement every branch at once.

Make the timing meaningful: disclose which goal distribution informed training,
which goals were known during each history write, and what remains accessible
to the reader. Changed goals must be withheld at the write stage whose
uncertainty is being tested. A finite memory cannot preserve every possible
future detail; specify the range of future uses under investigation.

Expected-goal acquisition and an evidence-access reference help interpret a
changed-goal deficit. Reader interventions can test whether a failure is
recoverable, but a privileged diagnostic reader is not deployed performance,
and an unsuccessful probe does not prove that information is absent. If
compressed branches fail similarly, investigate capacity, task uncertainty or
reader limitations rather than attributing the result to neural storage alone.

Record useful behavior alongside retained state, information access, writing
and reading costs, and any training or teacher cost. Equal bytes, parameters
and compute are different constraints; disclose what is matched. Across
differently pretrained architectures, report a system comparison rather than
an isolated effect of storage medium.

## Starting sources and implementation leads

These are leads from the root's [paper map](../../construct-2/studies/README.md#3-paper-map-what-we-can-build-on),
not interchangeable mechanisms or locally reproduced systems. Inspect the
closest method and its goal timing before making a novelty claim.

- **PERK — P8:** [2507.06415v3](https://arxiv.org/html/2507.06415v3), §§2–4.
  Meta-learns an adapter initialization for encoding context that supports
  later queries. Inspect the query distribution and adaptation boundary.
- **TTCD — P11:** [2608.01672v1](https://arxiv.org/html/2608.01672v1), §§2–4.
  A longer-context teacher trains a shorter-context student's fast weights.
  Inspect teacher access, causal write timing and resets; include teacher cost.
- **Self-Guided TTT — P13:** [2607.09415v1](https://arxiv.org/html/2607.09415v1),
  method and Algorithm 1. Selection uses the current question, full context
  remains available for answering, and updates reset per instance. This is a
  lead for a query-known comparison, not evidence of goal-blind compression.
- **Local S3 implementation:** [neural-memory-depth](../neural-memory-depth/README.md)
  contains a source-loaded CPU route and small learned associative-memory
  experiments. It offers an inspectable implementation lead; its tested recall
  and derivative findings do not establish performance under changed goals or
  equivalence to the language-model methods above.

The [source guide](../../construct-2/sources/README.md) records the root's
reading scope. Verify the exact paper versions, implementation revisions and
memory boundaries used here. Focus reading on selecting a usable existing
mechanism and distinguishing the proposed comparison from its closest overlap.

## Begin the investigation

Select and reproduce a suitable trainable memory mechanism, calibrate useful
acquisition on development material, and execute a first bounded comparison
between expected and changed uses of the same history. Size the workload and
compute budget locally from the available resources. Diagnose an acquisition
failure through comparisons that separate plausible causes; successful updates
alone are not a functioning learning regime. Preserve development attempts and
use fresh material for claims developed from them.

No further routine root permission is needed to begin this bounded empirical
work. Coordinate heavyweight use of the shared Mac Studio with the other active
investigators; reading, local tests and analysis can proceed independently.
[AGENTS.md](AGENTS.md) records the available resources and working practices.

Publish the question, methods, results, explanatory conclusion and limitations
in `FINDINGS.md`, linking local evidence and reproduction instructions from
this README. No findings exist at preparation. Follow the
[ancillary-study approach](../../construct-2/notes/ANCILLARY_STUDY.md): the root
synthesizes the publication; operational work remains here.
