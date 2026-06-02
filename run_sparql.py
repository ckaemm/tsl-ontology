import os
from pathlib import Path
from rdflib import Graph

BASE = Path(__file__).parent

g = Graph()
with open(BASE / "ontology" / "tsl_tbox.ttl", "rb") as f:
    g.parse(f, format="turtle")
with open(BASE / "ontology" / "tsl_abox.ttl", "rb") as f:
    g.parse(f, format="turtle")

PREFIX = """
PREFIX : <http://example.org/tsl-ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

queries = {
    "CQ1 — Players of Galatasaray": """
        SELECT ?name ?num WHERE {
            ?p a :Player ; :playsFor :Galatasaray ; rdfs:label ?name .
            OPTIONAL { ?p :jerseyNumber ?num }
        } ORDER BY ?num""",

    "CQ2 — Osimhen goals (2025-2026)": """
        SELECT ?name (COUNT(?g) AS ?goals) WHERE {
            ?g a :Goal ; :scoredBy :VictorOsimhen ; :goalInMatch ?m .
            ?m :inSeason :Season_2025_2026 .
            :VictorOsimhen rdfs:label ?name .
        } GROUP BY ?name""",

    "CQ3 — Stadiums by capacity": """
        SELECT ?team ?stadium ?cap WHERE {
            ?t a :Team ; rdfs:label ?team ; :homeStadium ?s ; :belongsToLeague :TurkishSuperLig .
            ?s rdfs:label ?stadium ; :stadiumCapacity ?cap .
        } ORDER BY DESC(?cap)""",

    "CQ4 — Transfers to Galatasaray": """
        SELECT ?player ?from ?fee WHERE {
            ?tr a :Transfer ; :transferPlayer ?p ; :transferredFrom ?f ; :transferredTo :Galatasaray .
            ?p rdfs:label ?player . ?f rdfs:label ?from .
            OPTIONAL { ?tr :transferFee ?fee }
        }""",

    "CQ5 — Cards in GS vs FB (W12)": """
        SELECT ?player ?min ?type WHERE {
            ?c :cardInMatch :Match_GS_FB_W12 ; :cardShownTo ?p ; :cardMinute ?min .
            ?p rdfs:label ?player .
            BIND(IF(EXISTS{?c a :RedCard},"RED","YELLOW") AS ?type)
        }""",

    "CQ6 — Head coaches": """
        SELECT ?team ?coach WHERE {
            ?c a :Coach ; rdfs:label ?coach ; :manages ?t .
            ?t a :Team ; rdfs:label ?team ; :belongsToLeague :TurkishSuperLig .
        } ORDER BY ?team""",

    "CQ7 — Week 8 matches": """
        SELECT ?home ?hs ?as ?away WHERE {
            ?m a :Match ; :matchWeek 8 ; :inSeason :Season_2025_2026 ;
               :homeTeam ?h ; :awayTeam ?a ; :homeScore ?hs ; :awayScore ?as .
            ?h rdfs:label ?home . ?a rdfs:label ?away .
        }""",

    "CQ8 — League standings": """
        SELECT ?pos ?team ?pts ?w ?d ?l WHERE {
            ?s a :Standing ; :standingSeason :Season_2025_2026 ;
               :standingTeam ?t ; :position ?pos ; :points ?pts ;
               :wins ?w ; :draws ?d ; :losses ?l .
            ?t rdfs:label ?team .
        } ORDER BY ?pos""",
}

print("=" * 55)
print("  SPARQL Results — TSL Football Ontology")
print("=" * 55)

for title, query in queries.items():
    print(f"\n--- {title} ---")
    results = list(g.query(PREFIX + query))
    if not results:
        print("  (no results)")
    for row in results:
        vals = [str(v) for v in row]
        print("  " + "  |  ".join(vals))

print(f"\n{'=' * 55}")
print(f"  Total triples in graph: {len(g)}")
print(f"  All 8 CQs executed successfully")
print(f"{'=' * 55}")
