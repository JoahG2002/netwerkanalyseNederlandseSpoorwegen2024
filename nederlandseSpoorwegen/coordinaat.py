

def dms_naar_decimaalgraden(dms_coordinaat: str) -> tuple[float, float]:
    """
    Ontvangt een coördinaat in de vorm '50°56'09"N 5°50'19"E' (degrees-minutes-secondsnotatie; dms), en zet dit om naar decimalen.
    """
    graden_breedtegraad: int = int(dms_coordinaat[:2])
    minuten_breedtegraad: int = int(dms_coordinaat[3:5])
    seconden_breedtegraad: int = int(dms_coordinaat[6:8])

    # Ddecimaal = D + (M / 60) + (S / 3600)
    decimaalgraden_breedtegraad: float = graden_breedtegraad + (minuten_breedtegraad / 60) + (seconden_breedtegraad / 3600)

    elementen_lengtegraad: str = dms_coordinaat.split(' ')[1]
    graden_lengtegraad: int = int(elementen_lengtegraad[0])
    minuten_lentegraad: int = int(elementen_lengtegraad[2:4])
    seconden_lentegraad: int = int(elementen_lengtegraad[5:7])

    decimaalgraden_lengtegraad: float = graden_lengtegraad + (minuten_lentegraad / 60) + (seconden_lentegraad / 3600)

    coordinaat_exact: tuple[float, float] = (decimaalgraden_breedtegraad, decimaalgraden_lengtegraad)

    return coordinaat_exact


def string_dd_naar_decimaalgraden(dd_coordinaat: str) -> tuple[float, float]:
    """
    Ontvangt een coördinaat in de vorm '50.9671° N, 5.8432° E' (decimal degrees; dd), en zet dit om naar decimalen.
    """
    elementen_breedtegraad, elementen_lengtegraad = dd_coordinaat.split(", ")

    decimaalgraden_breedtegraad: float = float(elementen_breedtegraad.split('°')[0])
    decimaalgraden_lengtegraad: float = float(elementen_lengtegraad.split('°')[0])

    coordinaat_exact: tuple[float, float] = (decimaalgraden_breedtegraad, decimaalgraden_lengtegraad)

    return coordinaat_exact


def coordinaatstring_naar_exact(coordinaat: str) -> tuple[float, float]:
    """
    Ontvangt een coördinaat in dms- of dd-notatie (50°56'09"N 5°50'19"E of 24.9671° N, 3.8432° E), en geeft dit exact terug.
    """
    if "\"E" in coordinaat:
        coordinaat_exact: tuple[float, float] = dms_naar_decimaalgraden(coordinaat)
    else:
        coordinaat_exact: tuple[float, float] = string_dd_naar_decimaalgraden(coordinaat)

    return coordinaat_exact
