from tkinter import Canvas
from Esine import Esine


class Pallo(Esine):
    """Luokka Pallo (perii luokan Esine) kuvaa palloa, jolla rikotaan palikoita"""

    def __init__(self, c: Canvas) -> None:
        self.xsuunta = 5
        self.ysuunta = 5
        super().__init__(245, 370, 10, 10, c, c.create_oval, "white", "white")

    def liiku(self):
        """Liikuttaa palloa eteenpäin ja kimpoaa reunoista"""

        self.x += self.xsuunta
        self.y += self.ysuunta

        self.kimpoa(("x" if self.x <= 0 or self.x >= 495 else "") +
                    ("y" if self.y <= 0 else ""))

        self.paivita()

    def gameover(self) -> bool:
        """
        Palauttaa tiedon pelin päättymisetä

        ## Palautus: bool
        - True, jos peli on päättynyt
        - False, jos peli on käynnissä
        """

        return self.y >= 495

    def kimpoa(self, suunta: str):
        """
        Kimpoaa parametrin mukaan
        ```python
        pallo.kimpoa(pallo.kimpoamissuunta(maila))
        ```
        ## Parametrit
        ### suunta: str
            - ""   = ei tee mitään
            - "x"  = kimpoaa sivusuunnassa
            - "y"  = kimpoaa pystysuunnassa
            - "xy" = kimpoaa molemmissa suunnissa
        """

        if "x" in suunta:
            self.xsuunta *= -1
        if "y" in suunta:
            self.ysuunta *= -1

    def kimpoamissuunta(self, toinen: Esine) -> str:
        """
        Palauttaa suunnan, johon kimmota
        ```python
        pallo.kimpoa(pallo.kimpoamissuunta(maila))
        ```
        ## Parametrit
        ### toinen: Esine
        Esine, josta kimpoamista katsotaan
        ## Palautus: str
            - ""   = ei kosketa toista esinettä
            - "x"  = koskettaa sivusuunnassa
            - "y"  = koskettaa pystysuunnassa
            - "xy" = koskettaa molemmissa suunnissa
        ## HUOM
        Pallo ei kimpoa tästä metodista!
        """

        palautettava = ""
        if (self.x - (toinen.x + toinen.xkoko) == 0 or toinen.x -
                (self.x + self.xkoko) == 0) and toinen.y <= self.y <= toinen.y + toinen.ykoko:
            palautettava += "x"
        if (self.y - (toinen.y + toinen.ykoko) == 0 or toinen.y -
                (self.y + self.ykoko) == 0) and toinen.x <= self.x <= toinen.x + toinen.xkoko:
            palautettava += "y"
        return palautettava

    def alkuun(self):
        """
        Palauttaa sijainnin ja suunnan samoiksi, kuin alussa
        ```python
        def uusi_taso():
            pallo.alkuun()
        ```
        """

        self.x, self.y, self.xsuunta, self.ysuunta = 245, 370, 5, 5
        self.paivita()
