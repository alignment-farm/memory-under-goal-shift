# Memory for later combinations and relations

**Third phase completed, 15 September 2026.** See [findings](future-use/FINDINGS.md)
and [reproduction](future-use/README.md). The original commission follows;
preparation itself ran no experiments.

**When does learned memory support later uses whose relevant combinations or
relations are not directly covered by writer training, and how do we distinguish
unavailable information from insufficient read computation?**

The [nonlinear publication](followup/FINDINGS.md), commit
`0d516aaa82d30d07e239b44e88ac43b5fdbfddef`, establishes that exact collision
uncertainty and reader error can coexist despite sufficient nominal capacity.
It also shows why the quantity estimated by a reader matters: products of
conditional means need not answer questions about conditional products. But
all 16 record types were repeatedly trained, and broad reconstruction directly
covered the changed raw-field targets. This phase investigates future use
beyond that coverage. The root's [learning and maintenance note](../../construct-2/notes/LEARNING_MAINTENANCE.md)
provides context; this commission is sufficient to begin if that note is not
available in the local checkout.

## One substantive extension

Develop one tractable setting with a larger input support or structured
histories, where later questions require new combinations or relations.
One optional lead is a history of events associated with entities, followed
by aggregate, order-sensitive or relational questions whose compositions differ
from anticipated use. Choose the setting and mechanism locally; a small CPU
experiment is suitable. Learning new addressing, handling noisy writes and
introducing several new goal families at once are unnecessary. Existing
competent components may be reused rather than relearned.

Changed queries should require more than requesting raw coordinates already
used as reconstruction targets. Make the generalization contrast explicit:
which histories, combinations or structures are fresh, which operations were
already available, and what the investigator, writer training and reader
training each know. Hold the actual query back during writing. A reader may
have learned an operation elsewhere while the writer lacked its eventual
use; disclose that boundary rather than calling both components uninformed.

Choose state constraints and questions that can distinguish anticipated-use
optimization from broader retention. Preserve evaluation of expected-use
behavior alongside changed use. The root expects broader retention to help
when later combinations need evidence omitted by a narrower writer. Recovery
with an alternative reader narrows the information-loss claim and identifies
a limitation in read computation. Equality with competent explicit retention
limits a storage-medium advantage; it does not by itself refute selection
driven by the learned memory's objective. A neural advantage is not a required
outcome.

## Distinguishing the explanations

Establish reader competence with access to the complete evidence. Failure to
execute an unfamiliar operation, even with its inputs available, must not be
counted as memory loss. Calibrate useful acquisition on development material;
use purposeful diagnostic comparisons when it fails. Preserve those attempts
and test the developed explanation on fresh histories and combinations.

Compare ordinary and alternative readers of the same frozen memory state.
Disclose any extra supervision, goal knowledge, lookup coverage, parameters
or computation supplied to the alternative. Successful recovery establishes
availability for that use; failed finite probes alone cannot establish absence.
Apply an analytic or exhaustive bound only when its assumptions and coverage
remain valid in the new setting.

Use competent explicit retention and disclose any structures supplied by hand,
including indices, summaries or query procedures. Identify what each learned
component actually acquires. Report complete-query utility as well as useful
component diagnostics: preserving a relation is insufficient if the system
cannot answer the resulting question reliably.

## Execution and contribution

Measure writing, reading, recovery and evidence-access costs, including training
and additional readers. These measurements connect to S5's question of when
learning repays its cost. Match useful quality before making an economy claim;
fewer bytes or faster incomplete answers alone do not establish a benefit.

The ancillary investigator owns methods, resource sizing and the numerical
budget, and may execute independently without further routine root permission.
Coordinate heavyweight shared-machine work when needed. Preserve both accepted
publications, their protocols and evidence. Record this phase separately and
publish its findings with reproducible supporting artifacts, explaining how
they change our account of retaining experience for later use.
