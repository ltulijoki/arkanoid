from time import time
from tkinter import Button, Frame, Label, Tk, Canvas, Toplevel, messagebox
from os.path import join

from Maila import Maila
from Palikka import Palikka
from Pallo import Pallo
from TasoLataaja import TasoLataaja
from apuf import hae_tasot
import valikko


class Arkanoid:
    """
    Peli käynnistetään tekemällä luokasta Arkanoid olio
    ```python
    if __name__ == "__main__":
        Arkanoid()
    ```
    """

    def __init__(self) -> None:
        self.ikkuna = Tk()
        self.ikkuna.title("Pelaa - Arkanoid")
        self.ikkuna.geometry("600x500")
        self.ikkuna["bg"] = "red"
        self.ikkuna.focus_force()

        self.canvas = Canvas(self.ikkuna, width=500,
                             height=500, bg="blue",
                             highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        frame = Frame(self.ikkuna, bg="red")
        frame.grid(row=0, column=1)
        self.tilalabel = Label(frame, text="", bg="red",
                               font=("Arial", 10, "bold"))
        self.tilalabel.pack()
        Button(frame, text="Valikko", command=lambda: [
               self.ikkuna.destroy(), valikko.valikko()], bg="blue", fg="white").pack()
        Button(frame, text="Uusi peli", command=self.uusi_peli,
               bg="blue", fg="white").pack()
        Button(frame, text="Vaihda tasoa", command=self.vaihda_tasoa,
               bg="blue", fg="white").pack()

        self.maila = Maila(self.canvas)
        self.pallo = Pallo(self.canvas)
        self.taso = -1
        self.palikat = []

        self.ikkuna.bind("<Left>", lambda event: self.maila.vasen())
        self.ikkuna.bind("<Right>", lambda event: self.maila.oikea())

        self.tila = ""
        self.tasot = TasoLataaja("tasot.json")

        aika = time()
        while True:
            self.ikkuna.update()
            self.tilalabel["text"] = self.tila

            if self.tila:
                continue

            if time() - aika >= 0.05:
                self.pallo.liiku()
                if self.pallo.gameover():
                    self.tila = "GAMEOVER"
                    messagebox.showinfo("GAMEOVER", "Hävisit pelin!")
                self.pallo.kimpoa(self.pallo.kimpoamissuunta(self.maila))
                for i in range(len(self.palikat) - 1, -1, -1):
                    suunta = self.pallo.kimpoamissuunta(self.palikat[i])
                    if suunta:
                        self.pallo.kimpoa(suunta)
                        self.palikat[i].osu()
                        if self.palikat[i].osumia_tarvitaan == 0:
                            del self.palikat[i]
                aika = time()
            if not self.palikat:
                self.taso += 1
                try:
                    self.palikat = Palikka.listasta(
                        self.tasot[self.taso], self.canvas)
                except IndexError:
                    self.tila = "Voitto!"
                self.pallo.alkuun()
                aika = time() + 3

    def uusi_peli(self):
        for palikka in self.palikat:
            palikka.poista()
        self.palikat.clear()
        self.tila = ""
        self.taso = -1
        self.pallo.alkuun()

    def vaihda_tasoa(self):
        def vaihda(taso: str):
            nonlocal ikkuna_auki
            self.tasot = TasoLataaja(taso)
            ikkuna.destroy()
            ikkuna_auki = False
            self.uusi_peli()

        ikkuna_auki = True
        ikkuna = Toplevel(self.ikkuna)
        ikkuna["bg"] = "blue"
        ikkuna.title("Vaihda tasoa")
        ikkuna.focus_force()

        vasen = Frame(ikkuna, bg="blue")
        vasen.pack(side="left")
        oikea = Frame(ikkuna, bg="blue")
        oikea.pack(side="right")
        Label(vasen, text="Valmiit tasot", bg="blue").pack()
        Label(oikea, text="Omat tasot", bg="blue").pack()

        for taso in hae_tasot(TasoLataaja.POLKU):
            Button(vasen, text=taso.split(".")[
                   0], command=lambda taso=taso: vaihda(taso), bg="red").pack()

        for taso in hae_tasot(join(TasoLataaja.POLKU, "omat")):
            Button(oikea, text=taso.split(".")[
                   0], command=lambda taso=taso: vaihda(join("omat", taso)), bg="red").pack()

        def sulje():
            nonlocal ikkuna_auki
            ikkuna_auki = False
            ikkuna.destroy()
        ikkuna.protocol("WM_DELETE_WINDOW", sulje)

        while ikkuna_auki:
            ikkuna.update()
