# Model modifications — version 0.4

## Source inventory

- The requested legacy source has been deleted from the active source inventory and all dependent configuration, interface, documentation, assumptions, figures and regenerated outputs.
- The remaining source identifiers are compactly renumbered S1–S5.
- All built-in scenarios now use the five-source inventory.

## Peng–Robinson transport EOS

- The transport hydraulics no longer use a fixed CO₂ density.
- Mixture density and compressibility factor `Z` are calculated from the Peng–Robinson EOS at the configured pressure, temperature and composition.
- The EOS uses classical quadratic mixing with `kij = 0` as the screening assumption.
- Density and `Z` are iterated at an estimated segment-mean pressure and written to every `pipeline_segments.csv`.
- The dashboard exposes PR density, `Z` and EOS reference pressure for each segment.

## Environmental study

- Every scenario now includes a climate/energy environmental screening layer.
- The study reports capture and purification electricity, capture steam, direct pipeline leakage, transport tonne-kilometres, pipeline operation/construction climate burden, lifecycle net avoided CO₂, burden intensity and alternative transport-mode benchmarks.
- Separate files are generated for each scenario: `environmental_summary.csv`, `environmental_transport_benchmarks.csv` and `environmental_report.md`.
- A fourth **Environmental study** tab is included in the dashboard opened by `START_MODEL.bat`.

## Validation

- Core model regression suite: 13 tests pass.
- Python source, dashboard and report scripts pass syntax compilation.
- All four built-in scenarios were executed and their outputs regenerated.
- Text-level validation confirms the deleted source and its former sector labels are absent from the package.
