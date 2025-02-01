from tkinter import Canvas


class Esine:
    """Luokka Esine kuvaa esinettä pelissä (pallo, maila, palikka)"""

    def __init__(self, x: float, y: float, xkoko: float, ykoko: float, c: Canvas, f: callable, taytto: str, aariviiva: str) -> None:
        self.x, self.y, self.xkoko, self.ykoko, self.canvas = x, y, xkoko, ykoko, c
        self.muoto = f(
            self.x, self.y, self.x + xkoko, self.y + ykoko, fill=taytto, outline=aariviiva)
        self.poistettu = False

    def paivita(self):
        """Päivittää esineen tilan näytölle"""

        if not self.poistettu:
            self.canvas.moveto(self.muoto, self.x, self.y)

    def poista(self):
        """
        Poistaa esineen näytöltä
        ```python
        if pallo_osui:
            palikka.poista()
        ```
        """

        self.canvas.delete(self.muoto)
        self.poistettu = True
