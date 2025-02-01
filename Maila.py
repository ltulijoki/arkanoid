from tkinter import Canvas
from Esine import Esine


class Maila(Esine):
    """Luokka maila (perii luokan Esine) kuvaa mailaa, jolla lyödään palloa"""

    def __init__(self, c: Canvas) -> None:
        super().__init__(200, 440, 100, 20, c, c.create_rectangle, "white", "white")

    def vasen(self):
        """Siirtää mailaa vasemmalle"""

        self.x = max(self.x - 10, 0)
        self.paivita()

    def oikea(self):
        """Siirtää mailaa oikealle"""

        self.x = min(self.x + 10, 400)
        self.paivita()
