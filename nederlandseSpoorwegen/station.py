import networkx as nx
import polars as pl
from collections import Counter


def geef_hoofdstations(stationsgraaf: nx.DiGraph) -> set[str]:
    """
    Ontvangt een graaf stations, en geeft alle hoofdstations terug — stations met meer dan vier uitrichtingen.

    Officiëel:
    "Je krijgt de naam Centraal als een station aan de volgende eisen voldoet:
    - de stad waar het station zich bevindt moet minimaal drie treinstations hebben;
    - in de stad moeten minimaal 100.000 mensen wonen;
    - dagelijks moeten minimaal 40.000 mensen via het station reizen."

    Bron: https://www.maxvakantieman.nl/artikelen/eropuit-in-nederland/wanneer-mag-een-treinstation-de-naam-centraal-station-dragen/
    """
    hoofdstations: set[str] = {
        station for station in stationsgraaf.nodes()
        if (stationsgraaf.out_degree(station) >= 4) or (station == "Antwerpen-Centraal") or (station == "Mönchengladbach Hbf")
    }

    return hoofdstations


def geef_inwoners_en_stations_provincies(stations: pl.DataFrame, aantal_inwoners_per_provincies: dict[str, int]) -> dict[str, list[int | set[str]]]:
    """
    Ontvangt een dataframe stationsdata en een dictionary dat het aantal inwoners per provincie bevat, en geeft het aantal inwoners en de stations van iedere provincie terug.
    """
    aantal_inwoners_en_stations_per_provincie: dict[str, list[int | set[str]]] = {
        provincie: [aantal_inwoners, set()] for provincie, aantal_inwoners in aantal_inwoners_per_provincies.items()
    }

    AANTAL_STATIONS: int = stations.shape[0]

    for i in range(AANTAL_STATIONS):
        station: str = stations["station"][i]
        provincie_van_station: str = stations["provincie"][i]

        if not (provincie_van_station is None):
            aantal_inwoners_en_stations_per_provincie[provincie_van_station][1].add(station)

    return aantal_inwoners_en_stations_per_provincie


def geef_top_n_stations(waarden_per_eenheid: dict[str, int | float], n: int = 10) -> dict[str, int | float]:
    """
    Ontvangt een dictionary stations met hun waarden, en geeft de top n stations terug — van groot naar klein.
    """
    counter: Counter = Counter(waarden_per_eenheid)

    top_n_stations: dict[str, int | float] = {}

    for station, waarde in counter.most_common():
        if len(top_n_stations) < n:
            top_n_stations[station] = waarde
        elif waarde == list(top_n_stations.values())[-1]:
            top_n_stations[station] = waarde
        else:
            break

    return top_n_stations
