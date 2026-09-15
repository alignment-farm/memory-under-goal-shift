# Development observations

15 September 2026, two frozen donor seed blocks 90/91, 512 histories each.
All four donors pass expected acquisition (<1e−5 MSE); broad codes are injective.
Full-evidence query algebra passed independently specified truth checks for all
65,536 possible four-record query tuples. Unit writes passed an autograd check.

Expected writers have exact population parity2 risks .437500 and .305556;
parity4 .683594 and .517747; two-field agreement .187500 and .138889.
Broad and explicit full raw memory have zero optimal error on every task.
Fitted conditional moments approach the exact reader. Ordinary raw estimates
can be poorly oriented/scaled for cross-record uses despite perfect local
parities. Clipping answers helps scale errors but does not remove uncertainty.
No acquisition failure, tuning, exclusion or donor retraining was needed.

Development also motivates a diagnostic ablation: agreement composed from exact
single-field means alone ignores the stored within-record ab moment. Freeze a
population comparison of that reader against the joint-moment reader before
fresh evaluation. This is extra supplied read computation, not extra writing.

Acquisition provenance script initially assumed this was part of the parent Git
repository and failed before copying anything. Corrected to this study's own
repository paths; every source now matches the accepted revision byte for byte.
This was an artifact-path repair, not an experimental failure.
