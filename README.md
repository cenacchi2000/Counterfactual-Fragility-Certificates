# Counterfactual Fragility Certificates
### For Tabular Classifications: Guarantees and Limits

**Which missing or degraded inputs can overturn a model decision?**

CFC audits a fixed model under a declared feature-failure protocol. The current manuscript combines a removal path that recomputes group effects after every step, separate graded tests of every group, and an exact minimum-removal result for affine class scores.

[Recomputed search and affine solver](explorer/reference.py) · [Runnable example](explorer/demo.py) · [Earlier artifact](LEGACY_README.md) · [Version map](explorer/PROVENANCE.md)

```mermaid
flowchart LR
  A[Fixed prediction and feature groups] --> B[Recompute next removal]
  B --> C[Record original-class margin]
  C --> B
  A --> D[Test every group at graded severity]
  A --> E[Affine model: exact subset envelope]
```

## Algorithmic contributions

**Recompute after each removal.** Redundant fields can mask one-step effects. At each step, evaluate all remaining groups against the current altered input and remove the group that most reduces the original-class margin. Keep the original class anchored even after a flip.

**Test partial degradation separately.** Removing a field entirely can behave differently from degrading it. The new example independently attenuates each group toward a fixed baseline at five severities. This demonstrates one operator; it does not implement the manuscript's entire failure family or FDS.

**Solve affine removal depth.** For known affine class scores and a fixed baseline, a rival's margin reduction is additive across disjoint groups. Sort its positive contributions and find the first prefix that defeats the original class; minimize over rivals. The mathematical result covers all subsets in this declared removal family, in `O(Cd + CG log G)` time.

## Run the paper-aligned reference examples

```bash
git clone https://github.com/cenacchi2000/Counterfactual-Fragility-Certificates.git
cd Counterfactual-Fragility-Certificates
python -m venv .venv
source .venv/bin/activate
pip install numpy
python explorer/demo.py
python -m unittest discover -s explorer/tests -v
```

The demo prints the recomputed removal trajectory, independent attenuation tests, and the affine minimum-removal witness. The tests compare the affine solver with exhaustive subset enumeration on small random models.

| Code | Purpose |
|---|---|
| [`removal_path`](explorer/reference.py) | Recompute every remaining group's effect at every step |
| [`graded_tests`](explorer/reference.py) | Independently test each group at each declared attenuation severity |
| [`affine_minimum_removals`](explorer/reference.py) | Minimum grouped baseline-removal depth, with smallest-index class tie rule |
| [`src/cfc_ref/`](src/cfc_ref) | Earlier compact implementation, preserved for version transparency |

## Possible use in surveillance research

A future forecasting audit could remove a wastewater stream, delay selected observations, or degrade input quality and measure changes in a surge flag. The grouping, replacement mechanism, and operational threshold would have to be declared for that pipeline. These examples operate on tabular class scores and contain no influenza data or forecasting evaluation.

## Version and interpretation boundaries

The earlier compact artifact in `src/cfc_ref/` uses a **fixed one-step ranking** and a narrower degradation check. It does not implement all algorithms described in the supplied current manuscript. Its figures and precomputed tables remain available through the [legacy overview](LEGACY_README.md).

The new `explorer/` code is an explicitly labelled **reference reimplementation**, not recovered original experiment code. It adds the three inspectable algorithms above without presenting legacy result tables as validation of this new code.

A removal witness describes dependence under the declared protocol. It is not causal recourse, a correctness certificate, or a general nonlinear robustness guarantee. The affine implementation uses floating point and requires disjoint groups covering all columns; near ties need careful numerical treatment.

Related work: [Conditional score training](https://github.com/cenacchi2000/Training-Scores-for-Conditional-Audits) · [Predictive-gain audits](https://github.com/cenacchi2000/Predictive-Gain-Audits)
