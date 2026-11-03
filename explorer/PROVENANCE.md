# Version map

Current source manuscript: **Counterfactual Fragility Certificates for Tabular Classifications: Guarantees and Limits**, supplied as `27578_Counterfactual_Fragility (2).pdf`.

The existing public `src/cfc_ref/` artifact predates the current algorithm description. Its fixed removal order is preserved; `LEGACY_README.md` contains its previous overview.

`explorer/reference.py` and `explorer/demo.py` were newly written on 3 November 2026 from the supplied manuscript's recomputed search description and Proposition 1 / Equation 8. They are not recovered benchmark scripts. The attenuation example covers one declared operator and does not compute the full paper certificate or FDS.

No new benchmark accuracy or brittleness-detection result is claimed for these additions. Affine exactness is a real-arithmetic mathematical property; the reference solver is floating point. Exhaustive small-case checks validate implementation behavior away from numerical ties.
