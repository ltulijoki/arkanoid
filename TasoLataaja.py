from json import loads
from os.path import join


class TasoLataaja:
    """
    Lataa tasot tiedostosta (json tai txt)
    ```python
    tasot = TasoLataaja("tasot.txt")
    ```
    ## JSON
    ```json
    [
        [
            "  111111",
            "",
            "  111111",
            "  111111",
            "1111111111"
        ],
        [
            "",
            "   3333",
            " 33233233",
            " 33333333",
            " 32222223",
            "   3333"
        ]
    ]
    ```
    ## TXT
    ```
      111111

      111111
      111111
    1111111111
    ,
       3333
     33233233
     33333333
     32222223
       3333

    ```
    """

    POLKU = join("tiedostot", "tasot")

    def __init__(self, tiedosto: str) -> None:
        tiedosto = join(self.POLKU, tiedosto)
        tyyppi = tiedosto.split(".")[-1]

        with open(tiedosto) as tied:
            sis = tied.read()

        if tyyppi == "json":
            self.tasot = loads(sis)

        if tyyppi == "txt":
            self.tasot = list(map(lambda t: t.split(
                "\n"), sis.rstrip("\n").split("\n,\n")))

    def __getitem__(self, i: int) -> list[str]:
        return self.tasot[i]

    def __len__(self) -> int:
        return len(self.tasot)

    def __bool__(self) -> bool:
        return bool(self.tasot)
