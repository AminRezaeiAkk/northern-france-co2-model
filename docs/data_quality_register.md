# Data quality register

| Item | Legacy value/behavior | Active treatment | Consequence |
|---|---|---|---|
| Coordinate labels | `X (Longitude)`, `Y (Latitude)` | Declared as Lambert-93 easting/northing, EPSG:2154 | Prevents degree/metre confusion. |
| Dunkirk endpoint | `650?510.80;7?104?922.04`; question marks stripped in code | User-specified `(636000, 7105000)` | Removes the artificial 13 m Arcelor-to-port segment. |
| Endpoint meaning | “Fixed storage sink” | Port receiving site and model boundary | Avoids claiming geological storage or adding terminal activities outside the requested scope. |
| Facility coordinates | Mixed rounded commune points and plant points | Official IREP WGS84 installation points converted to Lambert-93 | Better source-to-corridor distances; still not stack/tie-in coordinates. |
| Réty emissions | 642,894 t/y user case | User value retained; IREP 2024 total 603,000 t/y added | Scenario-selectable; CalCC design flow handled separately. |
| Auneuil identity | “Lafarge Plâtres”, sector `lime` | ETEX gypsum/plaster facility | Removes the Réty lime composition/capture preset. |
| Auneuil emissions | 270,899 t/y user case | IREP 2024 total 44,800 t/y added | Large discrepancy remains explicit. |
| Lumbres emissions | 483,691 t/y user case | IREP 2024 total 405,000 t/y; K6 design flow 800,000 t/y | Separates present declaration from the future reconfigured project. |
| Aluminium emissions | 616,381 t/y user case | IREP 2024 total 492,000 t/y | Avoids treating the input number as verified without lineage. |
| Steel emissions | 8,901,636 t/y user case | IREP 2024 total 5,995,000 t/y | Removes an unsupported 2.9 Mt/y excess in the reported-emissions scenario. |
| Capture coverage | 85–90% of every whole site | Separate capturable fraction, absorber capture rate, availability and purification recovery | Avoids equating unit capture performance with whole-site abatement. |
| Impurities | Raw-stack screening values compared to arbitrary mg/Nm³ thresholds | Final product checked against an export-quality ppm-mol specification | Makes the pipeline interface physically meaningful. |
| Cost | One-time CAPEX plus one year of variable cost | Capture, purification and transport CAPEX/OPEX separated; CAPEX annualized | Produces interpretable stage and chain €/t values. |
| Pipeline topology | Minimum spanning tree weighted only by length | Exact source/sink tree enumeration with flow, diameter, pressure and annualized cost | Adds capacity/economy-of-scale effects. |
| Route geometry | Straight lines | Straight lines × documented route factors | Still screening; a routed GIS model remains required. |

## IREP 2024 cross-check

The active data register uses the official installation IDs and current 2024 archive values:

| Source | IREP ID | Total CO₂ (t/y) | Non-biogenic CO₂ (t/y) |
|---|---|---:|---:|
| Chaux et Dolomies du Boulonnais, Réty | 0007000874 | 603,000 | 545,000 |
| ETEX, Auneuil | 0005100850 | 44,800 | 44,800 |
| S3 · EQIOM, Lumbres | 0007000785 | 405,000 | 367,000 |
| S4 · Aluminium Dunkerque | 0007000683 | 492,000 | 491,000 |
| S5 · ArcelorMittal France, Dunkerque | 0007000956 | 5,995,000 | 5,995,000 |
| **Total** |  | **7,539,800** | **7,442,800** |

Registry landing page: https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants

Direct annual archive pattern used for verification: `https://files.georisques.fr/irep/2024.zip`
