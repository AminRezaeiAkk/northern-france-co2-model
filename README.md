# Northern France CO₂ decision model

A point-and-click model for presenting the northern industrial CO₂ chain to technical and non-technical audiences.

The model has three physical engineering sections plus an environmental-study layer:

1. **Capture** at the industrial sources;
2. **Purification** and compression to pipeline specification;
3. **Transport** by dense-phase pipeline to the supplied Port of Dunkerque receiving point, with Peng–Robinson density/compressibility;
4. **Environmental study** for climate burden, energy demand, leakage and transport lifecycle screening.

Liquefaction, shipping, injection and geological storage are outside the calculation.

## Start the model

Double-click:

`START_MODEL.bat`

The first launch prepares an isolated model environment. Later launches open the dashboard directly. When the presentation is finished, close the model window.

No command-line knowledge is required.

## Recommended presentation workflow

1. Start with **Announced projects · 2030**. This is the most defensible base case because it uses the named CalCC and K6 project flows.
2. Use the three engineering cards to explain the flow from captured CO₂ to purified product to Dunkerque receipt, then open the environmental study.
3. Open the **Capture**, **Purification**, **Transport to sink** and **Environmental study** tabs in order.
4. Switch to **Verified 2024 cluster potential** to discuss the wider regional opportunity and its larger uncertainty.
5. Use **Build a custom case** only when the group wants to include/exclude sources or test economic assumptions.

See `docs/USER_GUIDE.md` for a short facilitator guide.

## Scenarios

| Interface choice | Calculation basis | Main use |
|---|---|---|
| Announced projects · 2030 | CalCC Réty 610 kt/y plus K6 Lumbres 800 kt/y; 1.5 Mt/y receiver limit | Recommended base case |
| Verified 2024 cluster potential | All five sources using official IREP 2024 total CO₂ | Regional screening |
| Original inventory · 4 Mt/y limit | Original user table constrained to 4 Mt/y | Reconcile the original study |
| Original inventory · unconstrained | Original user table without a binding limit | Diagnostic upper bound |
| Build a custom case | User-selected sources, basis, capacity and economics | Live sensitivity discussion |

## Recommended-case result

The current `announced_2030` base case estimates:

- 1.417 MtCO₂/y captured;
- 1.410 MtCO₂/y purified for transport;
- 1.410 MtCO₂/y received at Dunkerque after modeled leakage;
- 1.383 MtCO₂/y net avoided within the three-stage boundary;
- 93.8 km indicative collection routing;
- DN 200 screening pipe sizes;
- 90.2 bar minimum arrival pressure;
- €618.0 million three-stage CAPEX;
- €82.2/t received base annualized cost;
- €59.8–104.5/t received maturity-weighted screening range;
- 1.382 MtCO₂/y lifecycle net avoided in the environmental screening;
- 19.6 kg CO₂-eq/t received modeled climate-burden intensity.

These are screening/pre-FEED estimates, not vendor quotations or a routed construction design.

## What the calculations include

### Capture

- source-specific capturable fraction, unit capture rate and availability;
- Cryocap, oxyfuel/Cryocap, amine and DMX technology mappings;
- scaled CAPEX, annualized capital, fixed O&M, consumables, electricity and steam;
- capture-energy emissions.

### Purification

- independent recovery and mass loss;
- dehydration, polishing and compression to 110 bar;
- independent CAPEX, OPEX and electricity;
- screening against six published product-quality limits.

### Transport

- every feasible source/sink network tree without free junction nodes, up to 1,296 topologies;
- flow aggregation, standard diameter selection and route uplifts;
- Peng–Robinson EOS density/compressibility at 35 °C with a CO₂-rich multicomponent design composition;
- Darcy–Weisbach pressure loss and Swamee–Jain friction;
- velocity and minimum-arrival-pressure constraints;
- installed pipeline CAPEX, O&M and estimated leakage.

### Environmental study

- capture and purification energy-related greenhouse-gas emissions;
- direct modeled pipeline leakage;
- annual tonne-kilometres and pipeline operation/construction climate screening;
- transport-mode climate benchmarks;
- lifecycle net avoided CO₂ and burden intensity;
- explicit exclusions for route-specific biodiversity, land, water, noise and local air impacts until GIS/FEED data exist.

Equations, stage assumptions, uncertainty ranges and limitations are documented in `docs/assumptions.md`. Source corrections and IREP reconciliation are in `docs/data_quality_register.md`.

## Data quality

The five active verified IREP 2024 declarations total 7.540 MtCO₂/y, versus 10.916 MtCO₂/y in the original supplied table. Both bases remain available because hiding that difference would create false precision.

The model also corrects the legacy endpoint coordinate and uses Lambert-93 consistently. The active inventory is the sole source list used by the scenarios, interface and reports.

## Project structure

| Location | Purpose |
|---|---|
| `START_MODEL.bat` | One-click Windows launcher |
| `ui/` | Dashboard and presentation theme |
| `src/north_co2_model/` | Engineering model and reports |
| `config/model.toml` | Finance, pipeline, sink and scenario settings |
| `data/` | Active source inventory and quality limits |
| `docs/` | Assumptions, data quality and user guide |
| `tests/` | Regression checks |
| `outputs/` | Reproducible scenario reports and maps |

Superseded legacy prototypes, duplicate workbooks and stale output folders have been removed from the active project.

## Command-line use for model developers

Python 3.11 or newer is required.

```powershell
python -m pip install -r requirements.txt
python run_model.py --all-scenarios
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Primary public references

- French IREP/GEREP registry: https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants
- D’Artagnan capacity and investment: https://www.airliquide.com/group/press-releases-news/2024-06-18/decarbonization-dunkirk-basin-air-liquide-and-dunkerque-lng-co2-infrastructure-project-takes-major
- D’Artagnan pipeline and site scope: https://cinea.ec.europa.eu/news-events/news/cef-energy-supported-projects-core-pci-energy-days-2024-11-04_en
- CalCC factsheet: https://climate.ec.europa.eu/system/files/2022-12/if_pf_2022_calcc_en.pdf
- K6 factsheet: https://climate.ec.europa.eu/document/download/ab1d0b6c-6dbd-4786-b05b-fe6faf35b45e_en?filename=if_pf_2022_k6_en.pdf
- 3D/DMX Dunkerque pilot: https://innovation-centre-for-industrial-transformation.ec.europa.eu/innovative-techniques/carbon-capture-blast-furnace-flue-gas-emissions-absorption-using-amine
- Northern Lights product specification: https://norlights.com/wp-content/uploads/2025/06/Liquid-specification-2306251.pdf
- NETL pipeline method and cost guidance: https://www.netl.doe.gov/projects/files/QualityGuidelinesforEnergySystemStudiesCarbonDioxideTransportandStorageCostsinNETLStudies_073124.pdf
- JRC industrial capture assessment: https://publications.jrc.ec.europa.eu/repository/handle/JRC146193
