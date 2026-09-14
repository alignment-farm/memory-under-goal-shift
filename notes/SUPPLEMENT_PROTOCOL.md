# Bounded explanatory supplement — after first evaluation

The completed first evaluation gives correlated broad rank-4 MSE near .1,
versus .5 for balanced explicit field subsets. This does not isolate storage
medium: the subset stores both members of some correlated pairs and neither
member of others. Add an explicit derived-record control before publication.
This amendment is developed from the first evaluation; its empirical test
uses fresh histories. No new outer fitting, tuning, or shared-machine work.

For each existing seed 0–4 and rho in {0,.8}, load frozen rank-4 expected and
broad E from the first evaluation. Generate 2,048 new eight-record histories
with seed 810000+seed, never used for training, development, test, or probing.
Write each representation before reading both field families. Add an explicit
record containing four normalized sums (a_i+b_i)/sqrt(2), and decode both fields
as (a_i+b_i)/2. It knows the pairing/schema but no actual future question;
all source values are available at write time. Storage is four float32 scalars
per record, equal to learned rank-4 episodic state. The fixed transform is
shared configuration, needs no training or teacher, and can be implemented
with four additions and four scalings per record.

In the ideal Gaussian model this control's expected and changed MSE are both
(1-rho)/2, so .5 at rho=0 and .1 at rho=.8. These are analytic predictions,
not empirical results. Compare all five seed blocks; retain states' hashes,
source checkpoint JSON hashes and ordinary MSE for every condition. No new
probe is needed. This supplement tests an explanatory equivalence, not an
additional neural win, and does not modify the frozen first evaluation.
