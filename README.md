# Turkish Super Lig Football Ontology (TSL Ontology)

A formal OWL 2 ontology for modeling professional football data in the Turkish Super Lig, developed as a course project for **Knowledge Engineering and Ontologies** (2025–2026 Spring Semester) at Celal Bayar University.

## Project Objective

The goal of this project is to build a machine-readable knowledge model for the Turkish Super Lig (Trendyol Süper Lig). Football data is scattered across many websites in unstructured formats, making it difficult to query, reason over, or integrate systematically. This ontology formalizes the football domain using OWL 2, constructs a knowledge graph populated with real-world data from the 2025–2026 season, and demonstrates querying (SPARQL), validation (SHACL), and LLM-based ontology population capabilities.

## Dataset Sources

| Source | Data Provided |
|--------|---------------|
| [Transfermarkt](https://www.transfermarkt.com/) | Player profiles, market values, transfer histories, squad rosters |
| [Wikipedia](https://en.wikipedia.org/) | Season overviews, match results, stadium capacities, coach histories |
| [Mackolik](https://www.mackolik.com/) | Match scores, fixtures, goal and card statistics |
| [TFF.org](https://www.tff.org/) | Official standings, fixture lists, regulations |
| [FlashScore](https://www.flashscore.com/) | Real-time scores, detailed match events |

All data was collected manually and preprocessed with ASCII transliteration, date normalization (xsd:date), and currency standardization (EUR).

## Installation / Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Install Dependencies

```bash
pip install rdflib pyshacl
```

For LLM-based ontology population (optional):

```bash
pip install google-genai
```

### Run SPARQL Queries

```bash
python run_sparql.py
```

This loads the TBox and ABox, merges them into a single graph, and executes all 8 competency questions defined in `queries/sparql_queries.rq`.

### Run SHACL Validation

```bash
python -c "
from rdflib import Graph
from pyshacl import validate

g = Graph()
g.parse('ontology/tsl_tbox.ttl', format='turtle')
g.parse('ontology/tsl_abox.ttl', format='turtle')

r = validate(g, shacl_graph='ontology/tsl_shacl.ttl', inference='rdfs')
print('Conforms:', r[0])
print(r[2])
"
```

### Run LLM Population (Demo Mode)

```bash
python llm_population.py
```

For live mode with Gemini API (requires API key):

```bash
python llm_population.py --live
```

## Repository Structure

```
tsl-ontology/
├── README.md                          # Project documentation (this file)
├── ontology/
│   ├── tsl_tbox.ttl                   # TBox — 20 classes, 24 object props, 27 data props (403 triples)
│   ├── tsl_abox.ttl                   # ABox — instance data for 2025-2026 season (1314 triples)
│   └── tsl_shacl.ttl                  # SHACL — 11 Node Shapes for data validation
├── queries/
│   └── sparql_queries.rq              # 8 SPARQL competency questions
├── docs/                              # WIDOCO-generated ontology documentation
│   ├── index.html                     # Main documentation page
│   ├── sections/                      # Cross-reference sections (classes, properties)
│   ├── webvowl/                       # Interactive WebVOWL ontology visualization
│   ├── resources/                     # CSS/JS resources
│   └── provenance/                    # Provenance information
├── presentation/
│   └── tsl-presentation.pptx         # Project presentation slides
├── llm_population.py                  # LLM-based ontology population script (Gemini API)
└── run_sparql.py                      # SPARQL query execution script
```

## Ontology Statistics

| Component | Count |
|-----------|-------|
| OWL Classes | 20 |
| Object Properties | 24 |
| Data Properties | 27 |
| TBox Triples | 403 |
| ABox Triples | 1,314 |
| **Total Triples** | **1,717** |
| SHACL Node Shapes | 11 |

## ABox Coverage (2025–2026 Season)

| Entity | Count |
|--------|-------|
| Teams | 18 (full Super Lig) + 4 external |
| Players | 55 |
| Coaches | 14 |
| Stadiums | 17 |
| Matches | 15 |
| Goals | 27 |
| Cards | 8 |
| Transfers | 4 |
| Standings | 18 (full league table) |

## Competency Questions

| # | Question | Status |
|---|----------|--------|
| CQ1 | Which players currently play for a given team? | PASS |
| CQ2 | How many goals did a specific player score in a given season? | PASS |
| CQ3 | What is the capacity of a given stadium and which team plays there? | PASS |
| CQ4 | Which players were transferred from one specific club to another? | PASS |
| CQ5 | Which players received a red or yellow card in a specific match? | PASS |
| CQ6 | Who is the head coach of a given team? | PASS |
| CQ7 | What are all the matches played in a given season week? | PASS |
| CQ8 | What is the final standing/ranking of teams in a season? | PASS |

## Key Design Features

- **Property Chain Axiom**: `goalForTeam` is automatically inferred via the `scoredBy → playsFor` chain
- **Ontology Reuse**: Schema.org (SportsTeam, SportsEvent), FOAF (Person), Dublin Core, VANN
- **SHACL Validation**: 11 Node Shapes with cardinality, value range, SPARQL, and qualified value shape constraints
- **Disjointness Axioms**: Player/Coach, YellowCard/RedCard, Position subclasses (GK, DEF, MID, FWD)
- **LLM Integration**: Gemini API-based ontology population from match reports following Norouzi et al. (2024)

## Tools & Technologies

- **Protégé** — Ontology design and editing
- **rdflib** — RDF parsing and SPARQL query execution
- **pyshacl** — SHACL constraint validation
- **Gemini API** — LLM-based triple extraction from match reports
- **WIDOCO** — Ontology documentation generation

## Documentation

- **WIDOCO Ontology Documentation**: [https://ckaemm.github.io/tsl-ontology/](https://ckaemm.github.io/tsl-ontology/)
- **GitHub Repository**: [https://github.com/ckaemm/tsl-ontology](https://github.com/ckaemm/tsl-ontology)

## Team Members

| Name | Email | University |
|------|-------|------------|
| Cemil Koca | 220316024@ogr.cbu.edu.tr | Celal Bayar University |
| Recep Göktüğ Avcı | 220316021@ogr.cbu.edu.tr | Celal Bayar University |
| Murat Genç | 220316046@ogr.cbu.edu.tr | Celal Bayar University |

## License

This project is developed for educational purposes as part of the Knowledge Engineering and Ontologies course at Celal Bayar University.
