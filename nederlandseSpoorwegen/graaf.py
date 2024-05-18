import networkx as nx
import polars as pl
import pandas as pd
import statistics


def maak_stationsgraaf(coordinaten_stations: dict[str, tuple[float, float]]) -> nx.DiGraph:
    """
    Ontvangt een dictionary stations met hun coördinaten, en maakt er een gerichte graaf van.
    """
    D: nx.DiGraph = nx.DiGraph()

    for station, coordinaten_station in coordinaten_stations.items():
        D.add_node(station, pos=(coordinaten_station[1], coordinaten_station[0]))

    return D


def voeg_verbindingen_toe(stationsgraaf: nx.DiGraph, stations: pl.DataFrame) -> nx.DiGraph:
    """
    Ontvangt een stationsgraaf en DataFrame verbindingen, en voegt de verbindingen toe aan de graaf.
    """
    AANTAL_STATIONS: int = stations.shape[0]

    for i in range(AANTAL_STATIONS):
        station1: str = stations["station"][i]
        directe_verbindingen: str = stations["directe verbindingen"][i]

        if not (pd.isna(directe_verbindingen)):
            for station2 in directe_verbindingen.split(','):
                if not (station2 == station1):
                    stationsgraaf.add_edge(station1, station2)

    return stationsgraaf


def aantal_verbindingen_nodig_voor_complete_graaf(graaf: nx.Graph) -> int:
    """
    Ontvangt een graaft, en geeft terug hoeveel lijnen er nodig zijn om de graaf volledig te maken.
    """
    aantal_lijnen_graaf: int = graaf.number_of_edges()
    aantal_lijnen_complete_graaf: int = nx.complete_graph(len(graaf)).number_of_edges()

    aantal_lijnen_voor_compleet: int = aantal_lijnen_complete_graaf - aantal_lijnen_graaf

    return aantal_lijnen_voor_compleet


def print_graafgegevens(stationsgraaf: nx.DiGraph, hoofdstations: set[str], buitenlandse_stations: set[str],
                        aantal_inwoners_en_stations_per_provincie: dict[str, list[int | set[str]]], provincie: str = '') -> None:
    """
    Print de gegevens van de stationsgraaf.
    """
    bereiken_stations: dict[str, int] = {station1: sum(1 for station2 in stationsgraaf if nx.has_path(stationsgraaf, station1, station2)) for
                                         station1 in stationsgraaf}

    minimumbereik: int = min(bereiken_stations.values())
    maximumbereik: int = max(bereiken_stations.values())
    gemiddelde_bereik_station: float = statistics.mean(list(bereiken_stations.values()))

    uitgraden_stations: list[int] = [uitgraad for station, uitgraad in stationsgraaf.out_degree()]
    ingraden_stations: list[int] = [ingraad for station, ingraad in stationsgraaf.in_degree()]
    gemiddelde_uitgraad_stations: float = statistics.mean(uitgraden_stations)
    gemiddelde_ingraad_stations: float = statistics.mean(ingraden_stations)

    TUSSENSTATIONS: set[str] = {station for station in stationsgraaf if not (station in hoofdstations)}
    NEDERLANDSE_STATIONS: set[str] = {station for station in stationsgraaf if not (station in buitenlandse_stations)}

    aantallen_stations_per_provincie: list = [len(stationsgegevens[1]) for stationsgegevens in
                                              aantal_inwoners_en_stations_per_provincie.values()]
    aantallen_hoofdstations_per_provincie: list = [
        len({station for station in stationsgegevens[1] if station in hoofdstations})
        for stationsgegevens in aantal_inwoners_en_stations_per_provincie.values()
    ]
    aantallen_tussenstations_per_provincie: list = [
        len({station for station in stationsgegevens[1] if station in TUSSENSTATIONS})
        for stationsgegevens in aantal_inwoners_en_stations_per_provincie.values()
    ]

    aantal_symmetrische_verbindingen: int = sum(1 for station1, station2 in stationsgraaf.edges() if stationsgraaf.has_edge(station2, station1))

    stations_met_buitenlandse_verbindingen: set[str] = set()

    for station in stationsgraaf:
        for buitenlands_station in buitenlandse_stations:
            if stationsgraaf.has_edge(station, buitenlands_station):
                stations_met_buitenlandse_verbindingen.add(station)

    print(f"GRAAFGEGEVENS {provincie.upper()}\n{'-' * 78}")

    print(f"- aantal stations: {len(stationsgraaf)};")
    print(f"- aantal Nederlandse stations: {len(NEDERLANDSE_STATIONS)};")
    print(f"- aantal buitenlandse (Duitse en Belgische) stations: {len({station for station in stationsgraaf if station in buitenlandse_stations})};")
    print(f"- aantal hoofdstations: {len({station for station in stationsgraaf if station in hoofdstations})};")
    print(f"- aantal tussenstations: {len(TUSSENSTATIONS)};")

    if provincie == '':
        print(f"- gemiddeld aantal stations per provincie: {statistics.mean(aantallen_stations_per_provincie)};")
        print(f"- gemiddeld aantal hoofdstations per provincie: {round(statistics.mean(aantallen_hoofdstations_per_provincie), 2)};")
        print(f"- gemiddeld aantal tussenstations per provincie: {round(statistics.mean(aantallen_tussenstations_per_provincie), 2)};\n")

    print(f"- aantal verbindingen tussen stations: {len(stationsgraaf.edges())};")
    print(f"- aantal symmetrische verbindingen tussen stations: {aantal_symmetrische_verbindingen};")
    print(f"- aantal stations met (directe) buitenlandse verbindingen: {len(stations_met_buitenlandse_verbindingen)};")
    print(
        f"- aantal verbindingen vereist om graaf compleet te maken: {aantal_verbindingen_nodig_voor_complete_graaf(stationsgraaf)};\n")

    print(f"- gemiddelde uitgraad stations: {round(gemiddelde_uitgraad_stations, 3)};")
    print(f"- gemiddelde ingraad stations: {round(gemiddelde_ingraad_stations, 3)};")
    print(f"- minimumgraad stations: {min(ingraden_stations)};")
    print(f"- maximumingraad stations: {max(ingraden_stations)};")
    print(f"- minimumuitgraad stations: {min(uitgraden_stations)};")
    print(f"- minimumuitgraad stations: {max(uitgraden_stations)};\n")

    print(f"- minimumbereik stations: {minimumbereik};")
    print(f"- maximumbereik stations: {maximumbereik};")
    print(f"- gemiddeld bereik stations: {round(gemiddelde_bereik_station, 3)};")
    print(
        f"- ieder Nederlands station kan ieder ander Nederlands station bereiken: {list(bereiken_stations.values()).count(len(NEDERLANDSE_STATIONS)) == len(stationsgraaf)};\n")

    print(f"- clustervormingscoëfficiënt: {round(nx.average_clustering(stationsgraaf), 3)};")
    print(f"- dichtheid: {round(nx.density(stationsgraaf), 3)};")
    print(f"- diameter: {nx.diameter(stationsgraaf) if nx.is_strongly_connected(stationsgraaf) else "niet sterk verbonden"};")
    print(f"- radius: {nx.radius(stationsgraaf) if nx.is_strongly_connected(stationsgraaf) else "niet sterk verbonden"}.\n")


def geef_frequentie_graden(graaf: nx.Graph) -> dict[str | int, int]:
    """
    Geeft voor iedere graad in een graaf terug hoe vaak deze voorkomt.
    """
    frequentie_per_graad: dict[str | int, int] = {graad[1]: sum(1 for knoop in graaf.nodes() if graaf.degree(knoop) == graad[1]) for graad in graaf.degree()}

    return frequentie_per_graad


def grootte_component_na_verwijderen_knoop(graaf: nx.Graph, knoop: str | int) -> int:
    """
    Geeft de grootte van het grootste component terug na de verwijdering van een knoop uit een netwerk.
    """
    graaf_zonder_knoop: nx.Graph = graaf.copy()
    graaf_zonder_knoop.remove_node(knoop)

    componenten: list[str | int] = list(nx.connected_components(graaf_zonder_knoop))
    grootste_component: [str | int] = max(componenten, key=len)

    grootte_grootste_component: str | int = len(grootste_component)

    return grootte_grootste_component
