# Artifact Card

## Artifact type
Anonymous review artifact with reference implementation, result recreation scripts, and precomputed paper outputs.

## Claims supported

1. CFC is a protocol-relative audit object, not a formal worst-case robustness proof.
2. CFC-FDS identifies held-out brittle high-confidence cases better than confidence, energy, perturbation, and attribution-style baselines.
3. The result is not just a confidence relabeling effect, because brittle labels are assigned from disjoint held-out stressors.
4. The greedy path is an auditable deterministic trajectory; exact and beam-search diagnostics quantify its approximation gap.

## Not included

- author-identifying machine paths or logs;
- private orchestration code;
- complete production training grid;
- full unblinded manuscript metadata.

## Reproducibility level

- `quick_demo.py`: fully runnable reference certificate on a toy sample.
- `reproduce_tables.py`: regenerates markdown tables from bundled anonymous CSVs.
- `make_figures.py`: recreates compact figures from bundled CSVs.
- `src/cfc_ref`: inspectable reference implementation of CFC core equations.
