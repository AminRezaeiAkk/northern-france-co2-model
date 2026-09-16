# Dashboard user guide

## Open the model

Double-click `START_MODEL.bat`. The first launch prepares the private model environment, then the dashboard opens in the default browser.

Keep the small model window open during the presentation. Close it when finished.

## Run a scenario

1. Choose a scenario in the left panel.
2. Optionally open **Economic sensitivity** and change electricity price, steam price, discount rate or project life.
3. Click **Run selected scenario**.
4. Wait for the scenario title and values to update.

Changing a control does not silently change the displayed results. The dashboard shows a message until **Run selected scenario** is clicked.

## Explain the result

Start with the three cards:

- **Capture** shows how much CO₂ is separated and its capture CAPEX/cost.
- **Purification** shows specification-compliant pipeline product and recovery.
- **Transport to sink** shows how much reaches Dunkerque, the network length and minimum pressure.

Then open the four tabs in order.

### Capture tab

Use the emissions-versus-captured chart to explain that whole-site emissions are not the same as capturable emissions. The table identifies technology, capture rate, availability, CAPEX and maturity.

### Purification tab

Use the feed/product metrics to explain the 99.5% recovery. The quality table covers six modeled components. State clearly that a complete vendor assay is still required.

### Transport tab

Hover over a pipeline segment to see route length, flow, diameter, Peng–Robinson density, compressibility factor, velocity and pressure drop. The map is an optimized screening topology, not a surveyed right-of-way.

### Environmental study tab

Use the climate-burden breakdown to separate capture energy, purification energy, direct pipeline leakage, pipeline operation and construction screening burdens. The transport benchmark compares pipeline tonne-kilometre intensity with truck, barge and rail screening factors. Treat these as decision-screening indicators, not a project-specific ISO LCA.

## Interpret the uncertainty range

The base cost is the deterministic model result. The range reflects source maturity and ±35% transport uncertainty. It is not a probability interval.

For presentations:

- quote the base and range together;
- identify project-backed versus conceptual sources;
- do not call the route construction-ready;
- do not add shipping or storage conclusions, because they are outside the model.

## Download results

Each engineering tab provides a CSV download. The Environmental study tab provides its own CSV, and command-line scenario outputs include `environmental_summary.csv`, `environmental_transport_benchmarks.csv` and `environmental_report.md`. The Transport tab also provides the full source audit and JSON summary for the selected case.

## Recommended starting statement

> This is a screening/pre-FEED decision model. It keeps capture, purification and Peng–Robinson pipeline transport separate, reconciles their mass and cost accounts, and adds an environmental climate/energy screening layer. The physical chain ends when CO₂ reaches the supplied Port of Dunkerque site.
