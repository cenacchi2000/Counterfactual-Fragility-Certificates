# Verification

Executed locally on 3 November 2026 using Python 3.13, NumPy 2.2.6 and SciPy 1.16.2.

- Four test methods passed. The affine solver matched exhaustive minimum depth and returned valid witnesses on 150 small random multiclass models.
- A nonlinear redundancy example confirmed that recomputation changes the second removal.
- Tests checked all group/severity pairs and a class-priority tie.
- `python explorer/demo.py` completed. These checks do not validate the full paper benchmark.
