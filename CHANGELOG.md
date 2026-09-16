# Changelog

## 0.4.0

- Removed the requested legacy source from the active inventory, configuration, interface, documentation and generated outputs; remaining sources are compactly renumbered S1–S5.
- Replaced fixed transport density with a Peng–Robinson EOS calculation of mixture density and compressibility at the configured pressure, temperature and composition.
- Added an Environmental study to every scenario, command-line output and the dashboard launched by `START_MODEL.bat`.


## 0.3.0 — 2026-08-21

- Added a complete 27-item receiving-quality reference register for the June 2025 Northern Lights liquid-CO₂ cargo benchmark.
- Added explicit six-of-27 screening coverage, a machine-readable unscreened-component list and a warning that the benchmark is not a Dunkerque acceptance contract.
- Added a structured model assumption register with evidence class, uncertainty and FEED replacement actions.
- Updated the dashboard purification section to expose the full specification coverage and assay requirements.
- Extended regression coverage for reference-specification consistency.

## 0.2.0 — 2026-08-19

- Added a local point-and-click Streamlit dashboard and one-click Windows launcher.
- Limited the visible and calculated boundary to Capture, Purification and Transport to Dunkerque.
- Removed terminal liquefaction, shipping and storage costs/energy from the model.
- Split integrated source economics into separately reconciled capture and purification accounts while preserving combined reference values.
- Added stage mass balances, energy emissions, CAPEX, annual cost and levelized cost.
- Added maturity-weighted cost ranges and explicit interpretation warnings.
- Added custom source, inventory, receiving-capacity and finance controls.
- Added interactive pipeline mapping, quality-screen tables and downloadable audit results.
- Expanded regression coverage to ten mass, cost, quality, capacity and hydraulic checks.

## 0.1.0 — 2026-08-19

- Consolidated root/June/July prototypes into one installable Python package.
- Archived all legacy assets with a SHA-256 manifest.
- Corrected the Dunkirk hub coordinate and reclassified the port as an export terminal.
- Reconciled the active industrial sources to official IREP installation identities, coordinates and 2024 reported CO₂ while retaining the original user inventory as a scenario.
- Added announced CalCC/K6, reported-emissions, user-potential and unconstrained diagnostic scenarios.
- Added source-specific capture coverage, capture rate, availability, purification recovery, energy, CAPEX and OPEX.
- Added final product-quality screening against Northern Lights liquid-CO₂ limits.
- Replaced length-only MST routing with exact flow-aware tree enumeration, standard-diameter selection and Darcy-Weisbach pressure screening.
- Added receiving-capacity dispatch, net-avoided emissions, reproducible reports/maps and regression tests.
