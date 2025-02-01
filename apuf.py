from os import listdir
from os.path import exists, isfile, join


def hae_tasot(kansio: str) -> list["str"]:
    """
    Hakee tasot annetusta kansiosta
    ```python
    tasot = hae_tasot(TasoLataaja.POLKU)
    ```
    """

    tasot = []
    tiedostot = list(filter(lambda tied: isfile(
        join(kansio, tied)), listdir(kansio)))
    for tied in tiedostot:
        if not (tied.endswith(".txt") and exists(join(kansio, tied.replace(".txt", ".json")))):
            tasot.append(tied)
    return tasot
