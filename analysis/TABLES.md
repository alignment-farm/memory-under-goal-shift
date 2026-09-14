# Evaluation tables

Mean MSE over five seed/data blocks; all conditions shown. Lower is better.

## Correlation 0.0

| Slots | Condition | Expected ordinary | Changed ordinary | Changed probe | Changed ideal |
| --- | --- | ---: | ---: | ---: | ---: |
| 2 | expected | 0.499775 | 1.00107 | 1.00128 | 0.999999 |
| 2 | broad | 0.750395 | 0.753007 | 0.753162 | 0.751656 |
| 2 | expected_first | 0.503179 | 1.00108 | 1.00142 | 1 |
| 2 | balanced | 0.754034 | 0.751677 | 0.751957 | 0.75 |
| 2 | random_orthogonal | 0.722783 | 0.779711 | 0.779968 | 0.77882 |
| 2 | changed_known | 1.00335 | 0.500571 | 0.500716 | 0.5 |
| 2 | full_records | 0 | 0 | 1.86599e-30 | 0 |
| 4 | expected | 4.22273e-15 | 1.00108 | 1.00164 | 1 |
| 4 | broad | 0.581265 | 0.422469 | 0.422648 | 0.421091 |
| 4 | expected_first | 0 | 1.00108 | 1.00164 | 1 |
| 4 | balanced | 0.503179 | 0.500571 | 0.500802 | 0.5 |
| 4 | random_orthogonal | 0.444405 | 0.558557 | 0.55897 | 0.555377 |
| 4 | changed_known | 1.00335 | 0 | 1.03148e-30 | 0 |
| 4 | full_records | 0 | 0 | 1.86599e-30 | 0 |
| 8 | expected | 5.62249e-15 | 0.909038 | 4.651e-12 | 2.55351e-16 |
| 8 | broad | 6.48797e-15 | 6.14328e-15 | 2.74415e-15 | 1.27676e-16 |
| 8 | expected_first | 0 | 0 | 1.86599e-30 | 0 |
| 8 | balanced | 0 | 0 | 1.78348e-30 | 0 |
| 8 | random_orthogonal | 6.02478e-14 | 4.40043e-14 | 2.6698e-15 | 1.44329e-16 |
| 8 | changed_known | 0 | 0 | 3.12418e-30 | 0 |
| 8 | full_records | 0 | 0 | 1.86599e-30 | 0 |

## Correlation 0.8

| Slots | Condition | Expected ordinary | Changed ordinary | Changed probe | Changed ideal |
| --- | --- | ---: | ---: | ---: | ---: |
| 2 | expected | 0.500011 | 1.00562 | 0.682099 | 0.680808 |
| 2 | broad | 0.551007 | 0.55154 | 0.55154 | 0.550371 |
| 2 | expected_first | 0.503179 | 1.00336 | 0.682174 | 0.68 |
| 2 | balanced | 0.754034 | 0.753265 | 0.753502 | 0.75 |
| 2 | random_orthogonal | 0.730632 | 0.770428 | 0.622793 | 0.621241 |
| 2 | changed_known | 1.00335 | 0.501783 | 0.501894 | 0.5 |
| 2 | full_records | 0 | 0 | 3.55045e-30 | 0 |
| 4 | expected | 4.65645e-15 | 1.00336 | 0.360589 | 0.36 |
| 4 | broad | 0.100301 | 0.101486 | 0.100802 | 0.100654 |
| 4 | expected_first | 0 | 1.00336 | 0.360589 | 0.36 |
| 4 | balanced | 0.503179 | 0.501783 | 0.501989 | 0.5 |
| 4 | random_orthogonal | 0.402911 | 0.525534 | 0.299654 | 0.298219 |
| 4 | changed_known | 1.00335 | 0 | 7.58688e-31 | 0 |
| 4 | full_records | 0 | 0 | 3.55045e-30 | 0 |
| 8 | expected | 4.92478e-15 | 0.93655 | 6.90392e-12 | 1.06915e-16 |
| 8 | broad | 6.09964e-15 | 6.0208e-15 | 2.75142e-15 | 9.181e-17 |
| 8 | expected_first | 0 | 0 | 3.55045e-30 | 0 |
| 8 | balanced | 0 | 0 | 3.23932e-30 | 0 |
| 8 | random_orthogonal | 6.19208e-14 | 4.31725e-14 | 2.68307e-15 | 7.62141e-17 |
| 8 | changed_known | 0 | 0 | 3.75971e-30 | 1.09972e-16 |
| 8 | full_records | 0 | 0 | 3.55045e-30 | 0 |

## Paired differences

| Contrast | Mean | Seed bootstrap 95% |
| --- | ---: | --- |
| rank4 expected objective: changed minus expected | 1.00108 | 0.9983, 1.00428 |
| rank8 expected objective: changed ordinary minus probe | 0.909038 | 0.889456, 0.929494 |
| rank4 changed: narrow minus broad objective | 0.578609 | 0.531597, 0.616301 |
| rank4 expected: broad minus narrow objective | 0.581265 | 0.537266, 0.620619 |
| correlated rank4 changed: ordinary minus probe | 0.642771 | 0.640707, 0.644644 |
