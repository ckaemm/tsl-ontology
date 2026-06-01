"""
LLM-Based Ontology Population Demo
Turkish Super Lig Football Ontology
---
Bu script, bir mac haberi metnini alip Gemini API kullanarak
otomatik olarak RDF triple'lari cikarir ve SHACL ile dogrular.

Kullanim:
    pip install google-genai rdflib pyshacl
    python llm_population.py          (demo mode - API gerektirmez)
    python llm_population.py --live   (canli mod - Gemini API gerektirir)
"""

import os
import sys
from rdflib import Graph, Namespace, RDF
from pyshacl import validate

# =============================================================================
# YAPILANDIRMA
# =============================================================================

# Demo mode: True = onceden hazirlanmis ciktiyla calisir (API gerektirmez)
#             False = Gemini API'yi kullanir (--live parametresiyle)
DEMO_MODE = "--live" not in sys.argv

GEMINI_API_KEY = "BURAYA_API_KEYINI_YAPISTIR"

# =============================================================================
# ORNEK MAC HABERI
# =============================================================================

SAMPLE_NEWS = """
Galatasaray, Rams Park'ta oynanan Super Lig 28. hafta macinda Konyaspor'u 
3-1 maglup etti. Macin 15. dakikasinda Victor Osimhen'in golüyle one gecen 
Galatasaray, 38. dakikada Baris Alper Yilmaz'in attigi golle farki 2'ye 
cikardi. Ikinci yarinin basinda 52. dakikada Abdulkerim Bardakci Konyaspor 
adina farki azaltti. 78. dakikada Leroy Sane'nin müthis sutu ile skor 
3-1'e yukseldi. Macta Bardakci 65. dakikada sari kart gordu.
Mac tarihi: 15 Mart 2026.
"""

# =============================================================================
# TBOX SEMASI (LLM'e context olarak gonderilir)
# =============================================================================

TBOX_SCHEMA = """
# Ontology Schema - Turkish Super Lig Football Ontology
# Namespace: http://example.org/tsl-ontology# (prefix: :)

## Classes: Team, Player, Coach, Match, Goal, YellowCard, RedCard, Transfer, Stadium, Season
## Object Properties: playsFor, homeTeam, awayTeam, scoredBy, assistedBy, goalInMatch, goalForTeam, cardShownTo, cardInMatch, playedAtStadium, inSeason
## Data Properties: matchDate(xsd:date), matchWeek(xsd:integer), homeScore, awayScore, goalMinute, isPenalty, isOwnGoal, cardMinute, cardReason
## Existing Teams: :Galatasaray, :Fenerbahce, :Besiktas, :Trabzonspor, :Konyaspor, etc.
## Existing Stadiums: :RamsPark, :SukruSaracoglu, :VodafonePark, etc.
## Season: :Season_2025_2026
"""

# =============================================================================
# DEMO CIKTISI (API gerektirmez)
# Gercek Gemini API ciktisiyla ayni formatta onceden hazirlanmis triple'lar
# =============================================================================

DEMO_OUTPUT = """@prefix : <http://example.org/tsl-ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# --- Match ---
:Match_GS_KON_W28
    a :Match ;
    rdfs:label "Galatasaray vs Konyaspor - Week 28"@en ;
    :homeTeam :Galatasaray ;
    :awayTeam :Konyaspor ;
    :playedAtStadium :RamsPark ;
    :matchDate "2026-03-15"^^xsd:date ;
    :matchWeek 28 ;
    :inSeason :Season_2025_2026 ;
    :homeScore 3 ;
    :awayScore 1 .

# --- Players ---
:VictorOsimhen
    a :Player ;
    rdfs:label "Victor Osimhen"@en ;
    :playsFor :Galatasaray ;
    :hasPosition :forward_position .

:BarisAlperYilmaz
    a :Player ;
    rdfs:label "Baris Alper Yilmaz"@en ;
    :playsFor :Galatasaray ;
    :hasPosition :midfielder_position .

:AbdulkerimBardakci
    a :Player ;
    rdfs:label "Abdulkerim Bardakci"@en ;
    :playsFor :Konyaspor ;
    :hasPosition :defender_position .

:LeroySane
    a :Player ;
    rdfs:label "Leroy Sane"@en ;
    :playsFor :Galatasaray ;
    :hasPosition :forward_position .

# --- Goals ---
:Goal_1_GS_KON_W28
    a :Goal ;
    rdfs:label "Osimhen goal vs Konyaspor (15')"@en ;
    :scoredBy :VictorOsimhen ;
    :goalInMatch :Match_GS_KON_W28 ;
    :goalForTeam :Galatasaray ;
    :goalMinute 15 ;
    :isOwnGoal false ;
    :isPenalty false .

:Goal_2_GS_KON_W28
    a :Goal ;
    rdfs:label "Baris Alper goal vs Konyaspor (38')"@en ;
    :scoredBy :BarisAlperYilmaz ;
    :goalInMatch :Match_GS_KON_W28 ;
    :goalForTeam :Galatasaray ;
    :goalMinute 38 ;
    :isOwnGoal false ;
    :isPenalty false .

:Goal_3_GS_KON_W28
    a :Goal ;
    rdfs:label "Bardakci goal vs Galatasaray (52')"@en ;
    :scoredBy :AbdulkerimBardakci ;
    :goalInMatch :Match_GS_KON_W28 ;
    :goalForTeam :Konyaspor ;
    :goalMinute 52 ;
    :isOwnGoal false ;
    :isPenalty false .

:Goal_4_GS_KON_W28
    a :Goal ;
    rdfs:label "Sane goal vs Konyaspor (78')"@en ;
    :scoredBy :LeroySane ;
    :goalInMatch :Match_GS_KON_W28 ;
    :goalForTeam :Galatasaray ;
    :goalMinute 78 ;
    :isOwnGoal false ;
    :isPenalty false .

# --- Cards ---
:Card_1_GS_KON_W28
    a :YellowCard ;
    rdfs:label "Bardakci yellow card (65')"@en ;
    :cardShownTo :AbdulkerimBardakci ;
    :cardInMatch :Match_GS_KON_W28 ;
    :cardMinute 65 ;
    :cardReason "Foul" .
"""

# =============================================================================
# LLM PROMPT
# =============================================================================

def create_prompt(news_text):
    return f"""
Sen bir ontoloji muhendisisin. Asagidaki mac haberinden RDF triple'lari cikar.

KURALLAR:
1. SADECE Turtle formati kullan
2. Asagidaki ontoloji semasina KESINLIKLE uy
3. Mevcut takimlarin URI'lerini kullan
4. Oyuncu URI'leri icin CamelCase kullan
5. Metinde olmayan bilgiyi UYDURMA
6. Prefix tanimlarini DAHIL ET

ONTOLOJI SEMASI:
{TBOX_SCHEMA}

MAC HABERI:
{news_text}

CIKTI (sadece Turtle kodu, baska bir sey yazma):
"""

# =============================================================================
# TRIPLE CIKARMA
# =============================================================================

def extract_triples(news_text):
    """Haber metninden triple cikar (demo veya canli mod)"""
    print("\n" + "=" * 60)
    print("ADIM 1: Haber Metni")
    print("=" * 60)
    print(news_text.strip())

    if DEMO_MODE:
        print("\n[DEMO MODE] Onceden hazirlanmis LLM ciktisi kullaniliyor...")
        turtle_text = DEMO_OUTPUT
    else:
        print("\n[LIVE MODE] Gemini API'ye gonderiliyor...")
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = create_prompt(news_text)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        turtle_text = response.text
        if "```turtle" in turtle_text:
            turtle_text = turtle_text.split("```turtle")[1].split("```")[0]
        elif "```" in turtle_text:
            turtle_text = turtle_text.split("```")[1].split("```")[0]

    print("\n" + "=" * 60)
    print("ADIM 2: LLM Ciktisi (Turtle Triple'lar)")
    print("=" * 60)
    print(turtle_text.strip())

    return turtle_text.strip()


def validate_triples(turtle_text):
    """Cikarilan triple'lari SHACL ile dogrula"""
    print("\n" + "=" * 60)
    print("ADIM 3: SHACL Dogrulama")
    print("=" * 60)

    try:
        extracted = Graph()
        extracted.parse(data=turtle_text, format="turtle")
        triple_count = len(extracted)
        print(f"Parse edilen triple sayisi: {triple_count}")

        tbox_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ontology", "tsl_tbox.ttl")
        shacl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ontology", "tsl_shacl.ttl")

        if os.path.exists(tbox_path) and os.path.exists(shacl_path):
            tbox = Graph()
            tbox.parse(tbox_path, format="turtle")
            shacl = Graph()
            shacl.parse(shacl_path, format="turtle")

            conforms, _, results_text = validate(
                extracted, shacl_graph=shacl, ont_graph=tbox,
                inference='both', allow_warnings=True
            )

            if conforms:
                print("SONUC: CONFORMS = True (Tum constraint'ler gecti!)")
            else:
                print("SONUC: CONFORMS = False")
                print(results_text[:500])
        else:
            print(f"UYARI: TBox/SHACL bulunamadi, sadece syntax kontrolu yapildi.")
            print(f"SONUC: Turtle syntax GECERLI — {triple_count} triple")

        return extracted, triple_count
    except Exception as e:
        print(f"HATA: {e}")
        return None, 0


def show_extracted_data(graph):
    """Cikarilan verileri ozetler"""
    if graph is None:
        return

    print("\n" + "=" * 60)
    print("ADIM 4: Cikarilan Veriler Ozeti")
    print("=" * 60)

    TSL = Namespace("http://example.org/tsl-ontology#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

    matches = list(graph.subjects(RDF.type, TSL.Match))
    goals = list(graph.subjects(RDF.type, TSL.Goal))
    yellows = list(graph.subjects(RDF.type, TSL.YellowCard))
    reds = list(graph.subjects(RDF.type, TSL.RedCard))

    print(f"\nMaclar: {len(matches)}")
    for m in matches:
        label = list(graph.objects(m, RDFS.label))
        hs = list(graph.objects(m, TSL.homeScore))
        aws = list(graph.objects(m, TSL.awayScore))
        if label:
            score = f" → {hs[0]}-{aws[0]}" if hs and aws else ""
            print(f"  {label[0]}{score}")

    print(f"\nGoller: {len(goals)}")
    for g_node in goals:
        scorer = list(graph.objects(g_node, TSL.scoredBy))
        minute = list(graph.objects(g_node, TSL.goalMinute))
        team = list(graph.objects(g_node, TSL.goalForTeam))
        if scorer:
            s_label = list(graph.objects(scorer[0], RDFS.label))
            name = s_label[0] if s_label else str(scorer[0]).split("#")[-1]
            t_name = str(team[0]).split("#")[-1] if team else "?"
            min_str = f" {minute[0]}'" if minute else ""
            print(f"  {name} ({min_str}) — {t_name}")

    print(f"\nKartlar: {len(yellows)} sari, {len(reds)} kirmizi")
    for c in yellows + reds:
        player = list(graph.objects(c, TSL.cardShownTo))
        minute = list(graph.objects(c, TSL.cardMinute))
        if player:
            p_label = list(graph.objects(player[0], RDFS.label))
            name = p_label[0] if p_label else str(player[0]).split("#")[-1]
            min_str = f" {minute[0]}'" if minute else ""
            ctype = "SARI" if (c, RDF.type, TSL.YellowCard) in graph else "KIRMIZI"
            print(f"  {name} ({min_str}) [{ctype}]")


# =============================================================================
# ANA PROGRAM
# =============================================================================

if __name__ == "__main__":
    mode_str = "DEMO MODE (onceden hazirlanmis cikti)" if DEMO_MODE else "LIVE MODE (Gemini API)"

    print("=" * 60)
    print("  LLM-Based Ontology Population Demo")
    print("  Turkish Super Lig Football Ontology")
    print(f"  Mod: {mode_str}")
    print("  Paper: 'Ontology Population using LLMs' (Week 11)")
    print("=" * 60)

    if not DEMO_MODE and "BURAYA" in GEMINI_API_KEY:
        print("\nHATA: API key ayarlanmamis!")
        sys.exit(1)

    # Adim 1-2: Triple cikar
    turtle_output = extract_triples(SAMPLE_NEWS)

    # Adim 3: SHACL dogrula
    graph, count = validate_triples(turtle_output)

    # Adim 4: Ozet goster
    show_extracted_data(graph)

    print(f"\n{'=' * 60}")
    print(f"  TAMAMLANDI — {count} triple cikarildi")
    print(f"  Pipeline: Preprocessing -> Retrieval -> Population -> Validation")
    print(f"{'=' * 60}")
    print("\nBu script, 'Ontology Population using LLMs' makalesindeki")
    print("3-asamali pipeline'i demonstre eder.")
    if DEMO_MODE:
        print("\nCanli mod icin: python llm_population.py --live")
