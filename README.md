# Turkish Super Lig Football Ontology (TSL Ontology)

A formal OWL 2 ontology for modeling professional football data in the Turkish Super Lig, developed as a course project for **Knowledge Engineering and Ontologies** (2025-2026 Spring Semester) at Celal Bayar University.

## Overview

This ontology provides a structured knowledge model for querying and reasoning about teams, players, matches, goals, cards, transfers, stadiums, coaching staff, and league standings in the Turkish Super Lig.

## Repository Structure

```
├── README.md
├── docs/
│   ├── orsd-football-ontology.docx
│   ├── specification-document-v2.docx
│   ├── phase2-report.docx
│   └── index.html                    # Widoco-style ontology documentation
├── ontology/
│   ├── tsl_tbox.ttl                  # TBox — 20 classes, 24 obj props, 27 data props
│   ├── tsl_abox.ttl                  # ABox — 1314 triples
│   └── tsl_shacl.ttl                 # SHACL — 11 Node Shapes
├── queries/
│   └── sparql_queries.rq             # 8 SPARQL competency questions
└── presentation/
    └── tsl-presentation.pptx
```

## Ontology Statistics

| Component | Count |
|-----------|-------|
| TBox Triples | 403 |
| ABox Triples | 1314 |
| **Total Triples** | **1717** |
| OWL Classes | 20 |
| Object Properties | 24 |
| Data Properties | 27 |
| SHACL Node Shapes | 11 |

## ABox Coverage (2025-2026 Season)

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
| **Standings** | **18 (full league table)** |

## Competency Questions

| # | Question | Status |
|---|----------|--------|
| CQ1 | Which players currently play for a given team? | PASS |
| CQ2 | How many goals did a specific player score in a given season? | PASS |
| CQ3 | What is the capacity of a given stadium and which team plays there? | PASS |
| CQ4 | Which players were transferred from one specific club to another? | PASS |
| CQ5 | Which players received a red or yellow card in a specific match? | PASS |
| CQ6 | Who is the head coach of a given team? | PASS |
| CQ7 | What are all the matches played in a given season week (hafta)? | PASS |
| CQ8 | What is the final standing/ranking of teams in a season? | PASS |

## Key Design Features

- **Property Chain Axiom**: `goalForTeam` is inferred via `scoredBy → playsFor` chain
- **Ontology Reuse**: Schema.org (SportsTeam, SportsEvent), FOAF (Person), Dublin Core, VANN
- **SHACL Validation**: 11 Node Shapes with cardinality, value range, SPARQL, and qualified value shape constraints
- **Disjointness Axioms**: Player/Coach, YellowCard/RedCard, Position subclasses

## Tools & Technologies
- **Protégé** — Ontology editing
- **GraphDB** — Triple store and SPARQL endpoint
- **pyshacl** — SHACL validation in Python
- **rdflib** — RDF parsing and SPARQL querying

## Authors
- Cemil Koca
- Recep Göktuğ Avcı
- Murat Genç

## License
This project is developed for educational purposes.
