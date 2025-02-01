from json import dumps
from os import remove
from os.path import exists, join, split
from tkinter import Button, Canvas, Entry, Frame, Label, Tk, Toplevel, messagebox, simpledialog, ttk
from Palikka import Palikka
from TasoLataaja import TasoLataaja

from apuf import hae_tasot
import valikko


class TasonHallinta:
    """
    Tasojen hallinta käynnistetään tekemällä luokasta olio
    ```python
    if __name__ == "__main__":
        TasonHallinta()
    ```
    """

    def __init__(self) -> None:
        self.ikkuna = Tk()
        self.ikkuna.title("Tasojen hallinta - Arkanoid")
        self.ikkuna.geometry("500x500")
        self.ikkuna["bg"] = "blue"
        self.ikkuna.focus_force()

        Button(self.ikkuna, text="Valikko", command=lambda: [
               self.ikkuna.destroy(), valikko.valikko()], bg="red").pack()
        Button(self.ikkuna, text="Uusi tyhjä tasosarja",
               command=self.uusi_tasosarja, bg="red").pack()
        Label(self.ikkuna, text="Arkanoid", font=(
            "Arial", 50, "bold"), bg="blue").pack()
        Label(self.ikkuna, text="Valitse tasosarja",
              font=("Arial", 25, "bold"), bg="blue").pack()

        Label(self.ikkuna, text="Valmiit", font=(
            "Arial", 15, "bold"), bg="blue").pack()
        for taso in hae_tasot(TasoLataaja.POLKU):
            Button(self.ikkuna, text=taso.split(".")[
                0], command=lambda taso=taso:
                self.valitse_tasosarja(taso), bg="red").pack()

        Label(self.ikkuna, text="Omat", font=(
            "Arial", 15, "bold"), bg="blue").pack()
        self.tasosarjanapit = []
        for taso in hae_tasot(join(TasoLataaja.POLKU, "omat")):
            b = Button(self.ikkuna, text=taso.split(".")[
                0], command=lambda taso=taso:
                self.valitse_tasosarja(join("omat", taso)), bg="red")
            b.pack()
            self.tasosarjanapit.append(b)

        self.ikkuna.mainloop()

    def paivita_ikkuna(self):
        for nappi in self.tasosarjanapit:
            nappi.pack_forget()
        self.tasosarjanapit.clear()

        for taso in hae_tasot(join(TasoLataaja.POLKU, "omat")):
            b = Button(self.ikkuna, text=taso.split(".")[
                0], command=lambda taso=taso:
                self.valitse_tasosarja(join("omat", taso)), bg="red")
            b.pack()
            self.tasosarjanapit.append(b)
        self.ikkuna.focus_force()

    def uusi_tasosarja(self):
        nimi = simpledialog.askstring("Uusi tasosarja", "Tasosarjan nimi")
        if not nimi:
            return
        polulla = join(TasoLataaja.POLKU, "omat", nimi)
        if exists(polulla + ".json") or exists(polulla + ".txt"):
            messagebox.showerror("Virhe", f"Tasosarja {nimi} on olemassa!")
            return
        with open(polulla + ".json", "w") as json, open(polulla + ".txt", "w") as txt:
            json.write("[]")
            txt.write("")
        self.paivita_ikkuna()

    def valitse_tasosarja(self, tasosarja: str):
        try:
            self.tasosarjaikkuna.winfo_width()
            self.tasosarjaikkuna.destroy()
        except:
            pass
        tasosarjan_nimi = split(tasosarja)[1].split('.')[0]
        on_oma = split(split(tasosarja)[0])[1] == "omat"
        self.tasosarjaikkuna = Toplevel(self.ikkuna)
        self.tasosarjaikkuna.title(
            f"Hallitse tasosarjaa {tasosarjan_nimi} - Tasojen hallinta - Arkanoid")
        self.tasosarjaikkuna.geometry("500x500")
        self.tasosarjaikkuna.focus_force()

        f = Frame(self.tasosarjaikkuna)
        f.pack(fill="both", expand=1)
        canvas = Canvas(f, bg="red", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=1)
        vieritys = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        vieritys.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vieritys.set)
        canvas.bind("<Configure>", lambda event: canvas.config(
            scrollregion=canvas.bbox("all")))
        self.tasosarjaikkuna.bind(
            "<MouseWheel>", lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"))
        ikkuna = Frame(canvas, bg="red")
        canvas.create_window((0, 0), window=ikkuna, anchor="nw")

        Label(ikkuna, text=f"Hallitse tasosarjaa {tasosarjan_nimi}", font=(
            "Arial", 25, "bold"), bg="red").pack()
        if on_oma:
            Button(ikkuna, text="Poista tasosarja",
                   command=lambda sarja=tasosarja:
                   self.poista_tasosarja(sarja), bg="blue", fg="white").pack()
        Label(ikkuna, text="Tasot",
              font=("Arial", 25, "bold"), bg="red").pack()

        frame = Frame(ikkuna, bg="red")
        frame.pack()

        lataaja = TasoLataaja(tasosarja)
        i = 0
        entryt = []

        if lataaja:
            Label(frame, text="Numero", bg="red").grid(row=0, column=0)
            Label(frame, text="Taso", bg="red").grid(row=0, column=1)
            Label(frame, text="Vaikeus", bg="red").grid(row=0, column=2)

            for taso in lataaja:
                if on_oma:
                    e = Entry(frame, width=2)
                    e.insert(0, str(i + 1))
                    entryt.append(e)
                else:
                    e = Label(frame, text=str(i + 1), bg="red")
                e.grid(row=i + 1, column=0)
                c = Canvas(frame, width=100, height=100,
                           bg="blue", highlightbackground="red")
                c.grid(row=i + 1, column=1)
                lista = Palikka.listasta(taso, c, 10)
                vaikeus = sum(map(lambda p: p.osumia_tarvitaan, lista))
                Label(frame, text=str(vaikeus), bg="red").grid(
                    row=i + 1, column=2)
                if on_oma:
                    Button(frame, text="Poista taso", command=lambda sarja=tasosarja,
                           i=i: self.poista_taso(sarja, i), bg="blue",
                           fg="white").grid(row=i + 1, column=3)
                    Button(frame, text="Vaihda tasosarjaa", command=lambda sarja=tasosarja,
                           i=i: self.vaihda_sarjaa1(sarja, i), bg="blue",
                           fg="white").grid(row=i + 1, column=4)
                i += 1

            if on_oma:
                Label(ikkuna, text="""Tasojen järjestyksen vaihtaminen:
1. Kirjoita oikeat numerot tason kohdalle
2. Paina alla olevaa nappia""", bg="red").pack()
                Button(ikkuna, text="Vaihda järjestystä",
                       command=lambda: self.vaihda_jarjestysta(
                           tasosarja, entryt),
                       bg="blue", fg="white").pack()
        else:
            Label(ikkuna, text="Ei tasoja", bg="red").pack()

        self.tasosarjaikkuna.mainloop()

    def poista_tasosarja(self, sarja: str):
        nimi = sarja.split(".")[0]
        if messagebox.askokcancel("Poista tasosarja",
                                  "Haluatko varmasti poistaa tasosarjan {0}?"
                                  .format(split(nimi)[1]),
                                  parent=self.tasosarjaikkuna):
            if exists(join(TasoLataaja.POLKU, nimi + ".json")):
                remove(join(TasoLataaja.POLKU, nimi + ".json"))
            if exists(join(TasoLataaja.POLKU, nimi + ".txt")):
                remove(join(TasoLataaja.POLKU, nimi + ".txt"))
            self.tasosarjaikkuna.destroy()
            self.paivita_ikkuna()

    def poista_taso(self, sarja: str, i: int):
        tasot = list(TasoLataaja(sarja))
        del tasot[i]

        self.tallenna_tasot(sarja, tasot)
        self.valitse_tasosarja(sarja.split(".")[0] + ".json")

    def vaihda_sarjaa1(self, vanha: str, i: int):
        ikkuna = Toplevel(self.tasosarjaikkuna)
        ikkuna.title("Siirrä taso")
        ikkuna.geometry("500x500")
        ikkuna["bg"] = "blue"
        ikkuna.focus_force()

        Label(ikkuna, text="Valitse tasosarja",
              font=("Arial", 25, "bold"), bg="blue").pack()

        for taso in filter(lambda sarja: sarja != split(vanha)[1],
                           hae_tasot(join(TasoLataaja.POLKU, "omat"))):
            Button(ikkuna, text=taso.split(".")[
                   0], command=lambda uusi=taso, vanha=vanha, i=i:
                   [ikkuna.destroy(), self.vaihda_sarjaa2(vanha, i, uusi)],
                   bg="red").pack()

    def vaihda_sarjaa2(self, vanha: str, i: int, uusi: str):
        vanhan_tasot = list(TasoLataaja(vanha))
        uuden_tasot = list(TasoLataaja(join("omat", uusi)))
        uuden_tasot.append(vanhan_tasot.pop(i))

        self.tallenna_tasot(vanha, vanhan_tasot)
        self.tallenna_tasot(join("omat", uusi), uuden_tasot)
        self.valitse_tasosarja(join("omat", uusi.split(".")[0] + ".json"))

    def vaihda_jarjestysta(self, sarja: str, entryt: list[Entry]):
        try:
            uudet_numerot = list(map(int, map(Entry.get, entryt)))
        except ValueError:
            messagebox.showerror("Virhe", "Anna numerot!",
                                 parent=self.tasosarjaikkuna)
            return
        if len(set(uudet_numerot)) != len(uudet_numerot):
            messagebox.showerror(
                "Virhe", "Jokaisen numeron täytyy olla eri!", parent=self.tasosarjaikkuna)
            return

        tasot = list(TasoLataaja(sarja))
        kopio = tasot.copy()
        tasot.sort(key=lambda taso: uudet_numerot[kopio.index(taso)])

        self.tallenna_tasot(sarja, tasot)
        self.valitse_tasosarja(sarja.split(".")[0] + ".json")

    @classmethod
    def tallenna_tasot(cls, sarja: str, tasot: list[list[str]]):
        """
        Tallentaa parametrinään saadut tasot tiedostoon
        ## Parametrit
        ### sarja: str
        tasosarjan nimi esim.
        ```python
        "omat\\\\omat tasot"
        ```
        ### tasot: list[list[str]]
        tasot esim.
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

        nimi = join(TasoLataaja.POLKU, sarja.split(".")[0])
        with open(nimi + ".json", "w") as json, open(nimi + ".txt", "w") as txt:
            json.write(dumps(tasot))
            txt.write("\n,\n".join(map(lambda t: "\n".join(t), tasot)))
            txt.write("\n")
