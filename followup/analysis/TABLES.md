# Fresh nonlinear comparison

MSE; five seed blocks. Lower is better. Population values enumerate all 16 record types.

| Representation | Expected ordinary | Changed ordinary | Changed fitted reader | Changed optimal (population) | Occupied codes |
| --- | ---: | ---: | ---: | ---: | ---: |
| learned_broad_r2 | 0.600983 | 0.500939 | 0.500443 | 0.5 | [4, 4, 4, 4, 4] |
| learned_expected_r2 | 0.496173 | 1.15811 | 0.587937 | 0.5875 | [4, 4, 4, 3, 4] |
| learned_broad_r4 | 1.11736e-07 | 5.14937e-08 | 0 | 0 | [16, 16, 16, 16, 16] |
| learned_expected_r4 | 3.7445e-14 | 2.38433 | 0.350615 | 0.35 | [10, 9, 12, 12, 10] |
| parities | 0 | 1.99583 | 1.00076 | 1 | [4, 4, 4, 4, 4] |
| balanced_raw | 1 | 0.5 | 0.500327 | 0.5 | [4, 4, 4, 4, 4] |
| hybrid | 0.5 | 1.24523 | 0.750652 | 0.75 | [4, 4, 4, 4, 4] |
| full_raw | 0 | 0 | 0 | 0 | [16, 16, 16, 16, 16] |
| invertible_nonlinear_canonical | 0 | 1.99583 | 0 | 0 | [16, 16, 16, 16, 16] |

## Per-seed population risks

| Representation | Seed index | Expected ordinary | Changed ordinary | Changed optimal | Reader excess |
| --- | ---: | ---: | ---: | ---: | ---: |
| learned_broad_r2 | 0 | 0.500049 | 0.500726 | 0.5 | 0.000725639 |
| learned_broad_r2 | 1 | 1.00283 | 0.501426 | 0.5 | 0.00142606 |
| learned_broad_r2 | 2 | 0.500233 | 0.500923 | 0.5 | 0.000922503 |
| learned_broad_r2 | 3 | 0.500862 | 0.500823 | 0.5 | 0.000823484 |
| learned_broad_r2 | 4 | 0.501384 | 0.501077 | 0.5 | 0.00107686 |
| learned_expected_r2 | 0 | 0.5 | 0.502174 | 0.5 | 0.0021736 |
| learned_expected_r2 | 1 | 0.500003 | 1.50161 | 0.5 | 1.00161 |
| learned_expected_r2 | 2 | 0.500431 | 0.513725 | 0.5 | 0.013725 |
| learned_expected_r2 | 3 | 0.50002 | 1.00536 | 0.75 | 0.255363 |
| learned_expected_r2 | 4 | 0.478521 | 2.26182 | 0.6875 | 1.57432 |
| learned_broad_r4 | 0 | 4.2416e-08 | 2.3278e-08 | 0 | 2.3278e-08 |
| learned_broad_r4 | 1 | 2.09005e-07 | 9.78811e-08 | 0 | 9.78811e-08 |
| learned_broad_r4 | 2 | 1.255e-07 | 5.94477e-08 | 0 | 5.94477e-08 |
| learned_broad_r4 | 3 | 8.53192e-08 | 3.49943e-08 | 0 | 3.49943e-08 |
| learned_broad_r4 | 4 | 9.61062e-08 | 4.18678e-08 | 0 | 4.18678e-08 |
| learned_expected_r4 | 0 | 8.39329e-14 | 2.38994 | 0.375 | 2.01494 |
| learned_expected_r4 | 1 | 6.66134e-15 | 3.08204 | 0.5 | 2.58204 |
| learned_expected_r4 | 2 | 1.14353e-14 | 2.02141 | 0.25 | 1.77141 |
| learned_expected_r4 | 3 | 2.13163e-14 | 1.54787 | 0.25 | 1.29787 |
| learned_expected_r4 | 4 | 2.94209e-14 | 2.88287 | 0.375 | 2.50787 |
| parities | 0 | 0 | 2 | 1 | 1 |
| parities | 1 | 0 | 2 | 1 | 1 |
| parities | 2 | 0 | 2 | 1 | 1 |
| parities | 3 | 0 | 2 | 1 | 1 |
| parities | 4 | 0 | 2 | 1 | 1 |
| balanced_raw | 0 | 1 | 0.5 | 0.5 | 0 |
| balanced_raw | 1 | 1 | 0.5 | 0.5 | 0 |
| balanced_raw | 2 | 1 | 0.5 | 0.5 | 0 |
| balanced_raw | 3 | 1 | 0.5 | 0.5 | 0 |
| balanced_raw | 4 | 1 | 0.5 | 0.5 | 0 |
| hybrid | 0 | 0.5 | 1.25 | 0.75 | 0.5 |
| hybrid | 1 | 0.5 | 1.25 | 0.75 | 0.5 |
| hybrid | 2 | 0.5 | 1.25 | 0.75 | 0.5 |
| hybrid | 3 | 0.5 | 1.25 | 0.75 | 0.5 |
| hybrid | 4 | 0.5 | 1.25 | 0.75 | 0.5 |
| full_raw | 0 | 0 | 0 | 0 | 0 |
| full_raw | 1 | 0 | 0 | 0 | 0 |
| full_raw | 2 | 0 | 0 | 0 | 0 |
| full_raw | 3 | 0 | 0 | 0 | 0 |
| full_raw | 4 | 0 | 0 | 0 | 0 |
| invertible_nonlinear_canonical | 0 | 0 | 2 | 0 | 2 |
| invertible_nonlinear_canonical | 1 | 0 | 2 | 0 | 2 |
| invertible_nonlinear_canonical | 2 | 0 | 2 | 0 | 2 |
| invertible_nonlinear_canonical | 3 | 0 | 2 | 0 | 2 |
| invertible_nonlinear_canonical | 4 | 0 | 2 | 0 | 2 |
