# Turkish Super Lig Football Ontology (TSL Ontology)

A formal OWL 2 ontology for modeling professional football data in the Turkish Super Lig, developed as a course project for **Knowledge Engineering and Ontologies** (2025-2026 Spring Semester) at Celal Bayar University.

## Overview

This ontology provides a structured knowledge model for querying and reasoning about teams, players, matches, goals, cards, transfers, stadiums, and coaching staff in the Turkish Super Lig.

## Repository Structure

```
├── README.md                  # This file
├── docs/
│   └── orsd-football-ontology.docx   # ORSD specification document
├── ontology/
│   ├── tsl_tbox.ttl           # TBox — classes, properties, axioms
│   ├── tsl_abox.ttl           # ABox — sample instance data
│   └── tsl_shacl.ttl          # SHACL validation shapes
├── queries/
│   └── sparql_queries.rq      # SPARQL competency question queries
└── LICENSE
```

## Competency Questions

| # | Question |
|---|----------|
| CQ1 | Which players currently play for a given team? |
| CQ2 | How many goals did a specific player score in a given season? |
| CQ3 | What is the capacity of a given stadium and which team plays there? |
| CQ4 | Which players were transferred from one specific club to another? |
| CQ5 | Which players received a red or yellow card in a specific match? |
| CQ6 | Who is the head coach of a given team in a specific season? |
| CQ7 | What are all the matches played in a given season week (hafta)? |

## Ontology Design

### Classes
- `League`, `Season`, `Team`, `Player`, `Coach`, `Match`, `Stadium`
- `Goal`, `Card` (subclasses: `YellowCard`, `RedCard`), `Transfer`
- `Position` (subclasses: `Goalkeeper`, `Defender`, `Midfielder`, `Forward`)

### Reused Vocabularies
- [Schema.org](https://schema.org/) — `SportsTeam`, `SportsEvent`, `StadiumOrArena`
- [FOAF](http://xmlns.com/foaf/0.1/) — `Person`
- [Dublin Core](http://purl.org/dc/elements/1.1/) — Metadata annotations

### Tools & Technologies
- **Protégé** — Ontology editing and visualization
- **GraphDB** — Triple store and SPARQL endpoint
- **pyshacl** — SHACL validation in Python
- **SHACL Play** — Browser-based SHACL validation
- **Widoco** — Ontology documentation generation

## Getting Started

> **Note:** The ABox contains sample data for demonstration purposes. Match scores and some details are representative examples to validate the ontology structure and SPARQL queries.

1. Clone the repository
2. Open `ontology/tsl_tbox.ttl` in Protégé
3. Import `ontology/tsl_abox.ttl` as instance data
4. Run SPARQL queries from `queries/sparql_queries.rq` in GraphDB

## Authors

- Cemil,Murat and Göktuğ

## License

This project is developed for educational purposes.
