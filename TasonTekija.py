from os.path import exists, join, split
from tkinter import Button, Canvas, Event, Frame, Label, PhotoImage, Tk, Toplevel, messagebox, simpledialog, ttk

from Palikka import Palikka
from TasoLataaja import TasoLataaja
from TasonHallinta import TasonHallinta
from apuf import hae_tasot
from const import PALIKAN_VARIT
import valikko


class TasonTekija:
    """
    Tee taso käynnistetään tekemälä luokasta olio
    ```python
    if __name__ == "__main__":
        TasonTekija()
    ```
    """

    def __init__(self) -> None:
        self.ikkuna = Tk()
        self.ikkuna.title("Tee taso - Arkanoid")
        self.ikkuna.geometry("600x500")
        self.ikkuna["bg"] = "red"
        self.ikkuna.focus_force()

        self.canvas = Canvas(self.ikkuna, width=500,
                             height=500, bg="blue", highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        for x in range(10):
            for y in range(6):
                self.canvas.create_rectangle(
                    x * 50, y * 50, x * 50 + 50, y * 50 + 50, outline="gray")
        self.canvas.bind("<Button-1>", self.klikkaus)

        frame = Frame(self.ikkuna, bg="red")
        frame.grid(row=0, column=1)

        Button(frame, text="Valikko", command=lambda: [
               self.ikkuna.destroy(), valikko.valikko()], bg="blue", fg="white").pack()
        Button(frame, text="Aloita alusta", command=self.aloita_alusta,
               bg="blue", fg="white").pack()

        px = PhotoImage(width=1, height=1)
        for vahvuus, vari in list(enumerate(PALIKAN_VARIT))[1:]:
            Button(frame, text=str(vahvuus),
                   command=lambda vahvuus=vahvuus: self.aseta_vahvuus(vahvuus),
                   bg=vari,
                   fg="white" if vari == "black" else "black",
                   width=50, height=50, image=px, compound="c").pack()

        Button(frame, text="Tallenna", command=self.tallenna,
               bg="blue", fg="white").pack()
        Button(frame, text="Avaa", command=self.avaa1,
               bg="blue", fg="white").pack()

        self.vahvuus = 1
        self.palikat = []
        self.ikkuna.mainloop()

    def klikkaus(self, klikkaus: Event):
        x = (klikkaus.x // 50) * 50
        y = (klikkaus.y // 50) * 50

        sijainnit = list(map(lambda palikka: (
            palikka.x, palikka.y), self.palikat))
        if (x, y) in sijainnit:
            i = sijainnit.index((x, y))
            self.palikat[i].poista()
            del self.palikat[i]
        else:
            self.palikat.append(Palikka(self.canvas, x, y, self.vahvuus))

    def aloita_alusta(self):
        for palikka in self.palikat:
            palikka.poista()
        self.palikat.clear()
        self.vahvuus = 1

    def aseta_vahvuus(self, vahvuus: int):
        self.vahvuus = vahvuus

    def tallenna(self):
        if max(map(lambda p: p.y, self.palikat)) >= 300:
            messagebox.showwarning("Varoitus", "Taso menee tosi alas")
        nimi = simpledialog.askstring(
            "Tallenna", "Anna tasosarjan nimi\nAntamalla aiemmin annetun, lisäät nykyisen tason sen loppuun.")
        if not nimi:
            return
        tasot = []
        if exists(join(TasoLataaja.POLKU, "omat", nimi + ".json")):
            lataaja = TasoLataaja(join("omat", nimi + ".json"))
            tasot = list(lataaja)
        elif exists(join(TasoLataaja.POLKU, "omat", nimi + ".txt")):
            lataaja = TasoLataaja(join("omat", nimi + ".txt"))
            tasot = list(lataaja)
        tasot.append(Palikka.listaksi(self.palikat))
        TasonHallinta.tallenna_tasot(join("omat", nimi), tasot)

    def avaa1(self):
        ikkuna = Toplevel(self.ikkuna)
        ikkuna["bg"] = "blue"
        ikkuna.title("Avaa")
        ikkuna.focus_force()

        vasen = Frame(ikkuna, bg="blue")
        vasen.pack(side="left")
        oikea = Frame(ikkuna, bg="blue")
        oikea.pack(side="right")
        Label(vasen, text="Valmiit tasot", bg="blue").pack()
        Label(oikea, text="Omat tasot", bg="blue").pack()

        for taso in hae_tasot(TasoLataaja.POLKU):
            Button(vasen, text=taso.split(".")[
                   0], command=lambda taso=taso: [ikkuna.destroy(), self.avaa2(taso)], bg="red").pack()

        for taso in hae_tasot(join(TasoLataaja.POLKU, "omat")):
            Button(oikea, text=taso.split(".")[
                   0], command=lambda taso=taso: [ikkuna.destroy(), self.avaa2(join("omat", taso))], bg="red").pack()

        ikkuna.mainloop()

    def avaa2(self, sarja: str):
        oikea_ikkuna = Toplevel(self.ikkuna)
        oikea_ikkuna.title("Avaa")
        oikea_ikkuna.geometry("500x500")
        oikea_ikkuna.focus_force()

        f = Frame(oikea_ikkuna)
        f.pack(fill="both", expand=1)
        canvas = Canvas(f, bg="red", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=1)
        vieritys = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        vieritys.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vieritys.set)
        canvas.bind("<Configure>", lambda event: canvas.config(
            scrollregion=canvas.bbox("all")))
        oikea_ikkuna.bind(
            "<MouseWheel>", lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"))
        ikkuna = Frame(canvas, bg="red")
        canvas.create_window((0, 0), window=ikkuna, anchor="nw")

        Button(ikkuna, text="Takaisin", command=lambda: [oikea_ikkuna.destroy(
        ), self.avaa1()], font=("Arial", 20, "bold"), bg="blue", fg="white").pack()
        Label(ikkuna, text=split(sarja)
              [1].split(".")[0], font=("Arial", 20, "bold"), bg="red").pack()

        lataaja = TasoLataaja(sarja)
        def valitse(taso: list[str]):
            self.aloita_alusta()
            self.palikat = Palikka.listasta(taso, self.canvas)
            oikea_ikkuna.destroy()
        for taso in lataaja:
            c = Canvas(ikkuna, width=100, height=100,
                       bg="blue", highlightbackground="red")
            c.pack()
            c.bind("<Button-1>", lambda event, taso=taso: valitse(taso))
            Palikka.listasta(taso, c, 10)

        ikkuna.mainloop()
