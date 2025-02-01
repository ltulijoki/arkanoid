from tkinter import Canvas
from Esine import Esine
from const import PALIKAN_VARIT


class Palikka(Esine):
    """Luokka Palikka (perii luokan Esine) kuvaa palikkaa, joka rikotaan pallolla"""

    def __init__(self, c: Canvas, x: float, y: float, taso: int, koko: int = 50) -> None:
        vari = PALIKAN_VARIT[taso]
        super().__init__(x, y, koko, koko, c, c.create_rectangle,
                         vari, "white" if vari == "black" else "black")
        self.osumia_tarvitaan = taso

    def osu(self):
        """Vähentää palikan rikkomiseen tarvittavien osumien määrää.
        Jos osumien määrä on 0, palikka poistetaan
        ```python
        if pallo.kimpoamissuunta(palikka): # kaikista paitsi "" (ei osu) tulee True
            palikka.osu()
        ```
        """

        self.osumia_tarvitaan -= 1
        if self.osumia_tarvitaan == 0:
            self.poista()
        else:
            vari = PALIKAN_VARIT[self.osumia_tarvitaan]
            self.canvas.itemconfig(
                self.muoto, fill=vari, outline="white" if vari == "black" else "black")

    @classmethod
    def listasta(cls, lista: list[str], c: Canvas, koko: int = 50) -> list["Palikka"]:
        """
        Muodostaa palikat listasta
        ```python
        Palikka.listasta([
            "    11    ",
            "  111111  ",
            "1111111111",
            "  111111  ",
            "    11    "
        ], canvas)
        ```
        ## Parametrit
        ### lista: list[str]
        Esim.
        ```python
        [
            "    11    ",
            "  111111  ",
            "1111111111",
            "  111111  ",
            "    11    "
        ]
        ```
        - Numero = palikan rikkomiseen tarvittavien osumien määrä
        - Väli = ei palikkaa
        ### c: Canvas
        Canvas, johon palikat lisätään
        ## Palautus: list[Palikka]
        Lista palikoista
        """

        palautettava = []
        y = 0
        for rivi in lista:
            x = 0
            for palikka in rivi:
                if palikka != " ":
                    palautettava.append(Palikka(c, x, y, int(palikka), koko))
                x += koko
            y += koko
        return palautettava

    @classmethod
    def listaksi(cls, lista: list["Palikka"]) -> list[str]:
        """
        Muuttaa palikat listaksi
        ```python
        tasot = Palikka.listasta([ # haetaan list[Palikka]
            "    11    ",
            "  111111  ",
            "1111111111",
            "  111111  ",
            "    11    "
        ], canvas)
        Palikka.listaksi(tasot)
        ```
        ## Parametrit
        ### lista: list[Palikka]
        lista palikoista
        ## Palautus: list[str]
        esim.
        ```python
        [
            "    11    ",
            "  111111  ",
            "1111111111",
            "  111111  ",
            "    11    "
        ]
        ```
        """

        palikat = {(palikka.x // 50, palikka.y // 50)                   : palikka.osumia_tarvitaan for palikka in lista}
        suurin_y = int(max(map(lambda p: p[1], palikat.keys()), default=-1))
        palautettava = []
        for y in range(suurin_y + 1):
            palautettava.append("")
            for x in range(10):
                if (x, y) in palikat:
                    palautettava[-1] += str(palikat[(x, y)])
                else:
                    palautettava[-1] += " "
            palautettava[-1] = palautettava[-1].rstrip(" ")
        return palautettava
