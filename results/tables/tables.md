# Reproduced Result Tables

Generated from bundled anonymous review CSV files.

## Brittle-case identification

| score       |   adult |   bank |   credit_g |   default |   electricity |   heloc |   covertype |   aggregate_auroc |   ci_low |   ci_high | delta_vs_neg_energy   |   unit_frac_delta_le_0 |
|:------------|--------:|-------:|-----------:|----------:|--------------:|--------:|------------:|------------------:|---------:|----------:|:----------------------|-----------------------:|
| Max-softmax |   0.361 |  0.421 |      0.369 |     0.321 |         0.669 |   0.391 |       0.503 |             0.434 |    0.413 |     0.454 | nan                   |               nan      |
| Neg-entropy |   0.361 |  0.421 |      0.369 |     0.321 |         0.669 |   0.391 |       0.505 |             0.434 |    0.414 |     0.454 | nan                   |               nan      |
| Margin      |   0.361 |  0.421 |      0.369 |     0.321 |         0.669 |   0.391 |       0.502 |             0.434 |    0.414 |     0.454 | nan                   |               nan      |
| Neg-energy  |   0.523 |  0.52  |      0.5   |     0.504 |         0.507 |   0.505 |       0.51  |             0.51  |    0.504 |     0.516 | best                  |               nan      |
| CFC-RCMA    |   0.558 |  0.661 |      0.479 |     0.762 |         0.684 |   0.441 |       0.546 |             0.59  |    0.57  |     0.61  | 0.08                  |                 0.3122 |
| CFC-FDS     |   0.929 |  0.935 |      0.868 |     0.962 |         0.952 |   0.831 |       0.928 |             0.915 |    0.905 |     0.925 | 0.405                 |                 0      |

## Perturbation and attribution-style baselines

| ranking_score                | uses_trajectory   | uses_heldout_label_channel_for_scoring   |   heldout_brittle_auroc |
|:-----------------------------|:------------------|:-----------------------------------------|------------------------:|
| Max-softmax                  | No                | No                                       |                   0.448 |
| Neg-entropy                  | No                | No                                       |                   0.449 |
| Margin                       | No                | No                                       |                   0.451 |
| Neg-energy                   | No                | No                                       |                   0.511 |
| Random group order           | No                | No                                       |                   0.504 |
| One-step margin drop only    | No                | No                                       |                   0.662 |
| Permutation importance order | No                | No                                       |                   0.691 |
| Group-SHAP aggregate         | No                | No                                       |                   0.718 |
| CFC-RCMA                     | Yes               | No                                       |                   0.756 |
| CFC-FDS                      | Yes               | No                                       |                   0.914 |

## Curated component ablation

| ranking_signal                  |   mean_auroc |   min_auroc | interpretation                  |
|:--------------------------------|-------------:|------------:|:--------------------------------|
| Best generic score (Neg-energy) |        0.499 |       0.49  | confidence/energy surrogate     |
| RCMA only                       |        0.64  |       0.549 | gradual support collapse alone  |
| Degradation threshold only      |        0.72  |       0.62  | partial evidence failure alone  |
| Flip budget only                |        0.812 |       0.714 | abrupt decision-flip risk alone |
| CFC-FDS full certificate        |        0.976 |       0.942 | combined trajectory certificate |

## Design stability checks

| check       | setting             |   mean_auroc_or_corr | interpretation                      |
|:------------|:--------------------|---------------------:|:------------------------------------|
| Audit depth | K=3                 |                0.991 | strong under shallow audit          |
| Audit depth | K=10 default        |                0.976 | strong at default depth             |
| Audit depth | K=15                |                0.975 | stable under deeper audit           |
| FDS weights | Equal default       |                0.976 | strong without tuning               |
| FDS weights | Flip-heavy          |                0.967 | stable when emphasizing flips       |
| FDS weights | Degradation-heavy   |                0.973 | stable when emphasizing degradation |
| Calibration | Raw FDS             |                0.976 | before temperature scaling          |
| Calibration | Temp-scaled FDS     |                0.976 | after probability rescaling         |
| Calibration | Raw-temp rank corr. |                1     | ranking preserved by calibration    |

## Greedy exact/beam diagnostics

| dataset     |   exact_feasible_cases |   exact_match |   greedy_over |   mean_gap |   pair_miss |   beam_improve |
|:------------|-----------------------:|--------------:|--------------:|-----------:|------------:|---------------:|
| Adult       |                    384 |         0.891 |         0.073 |       0.09 |       0.018 |          0.044 |
| Bank        |                    384 |         0.879 |         0.084 |       0.11 |       0.024 |          0.052 |
| Credit-G    |                    256 |         0.846 |         0.109 |       0.16 |       0.038 |          0.069 |
| Default     |                    256 |         0.862 |         0.098 |       0.14 |       0.032 |          0.063 |
| Electricity |                    384 |         0.913 |         0.057 |       0.07 |       0.014 |          0.039 |
| HELOC       |                    256 |         0.834 |         0.123 |       0.18 |       0.041 |          0.077 |
| Covertype   |                    128 |         0.857 |         0.102 |       0.15 |       0.036 |          0.081 |
| Mean        |                   2048 |         0.869 |         0.092 |       0.13 |       0.029 |          0.061 |

## Naturalistic field-unavailability proxy

| score         |   adult_bank_heloc |   eligible_subset | gap      |
|:--------------|-------------------:|------------------:|:---------|
| Max-softmax   |              0.472 |             0.481 | nan      |
| Neg-energy    |              0.541 |             0.552 | nan      |
| One-step drop |              0.644 |             0.661 | nan      |
| Group-SHAP    |              0.682 |             0.696 | best_alt |
| CFC-RCMA      |              0.735 |             0.748 | 0.052    |
| CFC-FDS       |              0.812 |             0.827 | 0.131    |

