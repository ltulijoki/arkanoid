from json import dumps, loads
from tkinter import Button, Canvas, Entry, Frame, Label, Text, Tk, Toplevel, messagebox, ttk
from const import PALAUTTEET_TIEDOSTO

import valikko


class Muu:
    """Tekemällä luokasta olio, Muu-valikko avautuu
    ```python
    if __name__ == "__main__":
        Muu()
    ```
    """

    def __init__(self) -> None:
        self.ikkuna = Tk()
        self.ikkuna.title("Muu - Arkanoid")
        self.ikkuna.geometry("600x600")
        self.ikkuna["bg"] = "blue"
        self.ikkuna.focus_force()

        Label(self.ikkuna, text="Arkanoid", font=(
            "Arial", 50, "bold"), bg="blue").pack()
        Label(self.ikkuna, text="Muu", font=(
            "Arial", 40, "bold"), bg="blue").pack()
        Button(self.ikkuna, text="Takaisin valikkoon", command=lambda: [
               self.ikkuna.destroy(), valikko.valikko()], bg="red",
               font=("Arial", 50, "bold")).pack()
        Button(self.ikkuna, text="Palaute", command=self.palaute1, bg="red",
               font=("Arial", 50, "bold")).pack()

        self.ikkuna.mainloop()

    def alusta_palauteikkuna(self, vaihe: int, max: int) -> Tk:
        self.palauteikkuna = Toplevel(self.ikkuna)
        self.palauteikkuna.title("Palaute - Arkanoid")
        self.palauteikkuna.geometry("500x500")
        self.palauteikkuna["bg"] = "blue"
        self.palauteikkuna.focus_force()

        f = Frame(self.palauteikkuna)
        f.pack(fill="both", expand=1)
        canvas = Canvas(f, bg="blue", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=1)
        vieritys = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        vieritys.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vieritys.set)
        canvas.bind("<Configure>", lambda event: canvas.config(
            scrollregion=canvas.bbox("all")))
        self.palauteikkuna.bind(
            "<MouseWheel>", lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"))
        ikkuna = Frame(canvas, bg="blue")
        canvas.create_window((0, 0), window=ikkuna, anchor="nw")

        c = Canvas(ikkuna, width=500, height=50,
                   bg="blue", highlightthickness=0)
        c.pack()
        c.create_rectangle(0, 0, 500 / max * vaihe, 50,
                           fill="green", outline="green")

        Label(ikkuna, text="Anna palautetta",
              font=("Arial", 47, "bold"), bg="blue").pack()

        return ikkuna

    def palaute_seuraava(self, f: callable, tarkistus: callable = lambda: True) -> callable:
        def palautettava():
            if tarkistus():
                self.palauteikkuna.destroy()
                f()
        return palautettava

    def palaute1(self):
        ikkuna = self.alusta_palauteikkuna(1, 5)

        Button(ikkuna, text="Aloita",
               bg="green", font=("Arial", 30, "bold"),
               command=self.palaute_seuraava(self.palaute2)).pack()
        Button(ikkuna,
               text="Haluan antaa vain sanallista palautetta", bg="red",
               font=("Arial", 19, "bold"),
               command=self.palaute_seuraava(self.vain_sanallinen2)).pack()

        self.palauteikkuna.mainloop()

    def palaute2(self):
        ikkuna = self.alusta_palauteikkuna(2, 5)

        Button(ikkuna,
               text="Takaisin", bg="red",
               font=("Arial", 15, "bold"),
               command=self.palaute_seuraava(self.palaute1)).pack()

        self.kysymykset = list(map(lambda kysymys: {"kysymys": kysymys}, [
            "Kuinka selkeää pelaaminen oli?",
            "Kuinka selkeää tason tekeminen oli?",
            "Kuinka selkeää tasojen hallinta oli?",
            "Kuinka helposti löysit tämän palautelomakkeen?",
            "Kuinka helppoa palautelomakkeen täyttäminen oli?"
        ]))

        Label(ikkuna, text="Vastaa kysymyksiin asteikolla 1-5",
              font=("Arial", 15, "bold"), bg="blue").pack()
        for kysymys in self.kysymykset:
            Label(ikkuna,
                  text=kysymys["kysymys"], bg="blue",
                  font=("Arial", 15, "bold")).pack()
            kysymys["entry"] = Entry(ikkuna, width=1)
            kysymys["entry"].pack()

        Label(ikkuna, text="Anna halutessasi sanallista palautetta:",
              font=("Arial", 15, "bold"), bg="blue").pack()

        self.sanallinen_laatikko = Text(ikkuna, width=30, height=10)
        self.sanallinen_laatikko.pack()

        def tarkistus():
            for kysymys in self.kysymykset:
                try:
                    numero = int(Entry.get(kysymys["entry"]))
                except ValueError:
                    messagebox.showerror(
                        "Virhe", f"Anna numero kohtaan {kysymys['kysymys']}!",
                        parent=self.palauteikkuna)
                    return False
                if numero < 1 or numero > 5:
                    messagebox.showerror(
                        "Virhe", f"Kohdan {kysymys['kysymys']} vastaus ei ole välillä 1-5!",
                        parent=self.palauteikkuna)
                    return False
                kysymys["numero"] = numero

            self.sanallinen = self.sanallinen_laatikko.get(1.0, "end-1c")
            return True

        Button(ikkuna, text="Seuraava", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.palaute3, tarkistus)
        ).pack()

        self.palauteikkuna.mainloop()

    def palaute3(self):
        ikkuna = self.alusta_palauteikkuna(3, 5)

        Button(ikkuna,
               text="Takaisin", bg="red",
               font=("Arial", 15, "bold"),
               command=self.palaute_seuraava(self.palaute2)).pack()

        for kysymys in self.kysymykset:
            Label(ikkuna, text=f"{kysymys['kysymys']}",
                  bg="blue", font=("Arial", 15, "bold")).pack()
            Label(ikkuna, text=str(kysymys["numero"]), bg="blue").pack()
            if kysymys["numero"] < 5:
                Label(ikkuna, text="Miksi annoit tämän numeron?\nMitä voisi parantaa?",
                      bg="blue", font=("Arial", 15, "bold")).pack()
                kysymys["lisatietolaatikko"] = Text(
                    ikkuna, width=30, height=10)
                kysymys["lisatietolaatikko"].pack()

        Label(ikkuna, text=f"Anna halutessasi sanallista palautetta:",
              font=("Arial", 15, "bold"), bg="blue").pack()
        Label(ikkuna, text=self.sanallinen, bg="blue").pack()

        def tarkistus():
            for kysymys in self.kysymykset:
                if "lisatietolaatikko" in kysymys:
                    lisatiedot = kysymys["lisatietolaatikko"].get(
                        1.0, "end-1c")
                    if not lisatiedot:
                        messagebox.showerror(
                            "Virhe", f"Vastaa kysymykseen miksi annoit tämän \
numeron\nkohdassa {kysymys['kysymys']}!",
                            parent=self.palauteikkuna)
                        return False
                    kysymys["lisatiedot"] = lisatiedot
            return True

        Button(ikkuna, text="Seuraava", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.palaute4, tarkistus)
        ).pack()

        self.palauteikkuna.mainloop()

    def palaute4(self):
        ikkuna = self.alusta_palauteikkuna(4, 5)

        Button(ikkuna,
               text="Takaisin", bg="red",
               font=("Arial", 15, "bold"),
               command=self.palaute_seuraava(self.palaute3)).pack()

        for kysymys in self.kysymykset:
            Label(ikkuna, text=f"{kysymys['kysymys']}",
                  bg="blue", font=("Arial", 15, "bold")).pack()
            Label(ikkuna, text=str(kysymys["numero"]), bg="blue").pack()
            if kysymys["numero"] < 5:
                Label(ikkuna, text=f"Miksi annoit tämän numeron?\
\nMitä voisi parantaa?",
                      bg="blue", font=("Arial", 15, "bold")).pack()
                Label(ikkuna, text=kysymys["lisatiedot"], bg="blue").pack()

        Label(ikkuna, text=f"Anna halutessasi sanallista palautetta:",
              font=("Arial", 15, "bold"), bg="blue").pack()
        Label(ikkuna, text=self.sanallinen, bg="blue").pack()

        Button(ikkuna, text="Lähetä", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.laheta_palaute)
        ).pack()

        self.palauteikkuna.mainloop()

    def vain_sanallinen2(self):
        ikkuna = self.alusta_palauteikkuna(2, 4)

        Button(ikkuna,
               text="Takaisin", bg="red",
               font=("Arial", 15, "bold"),
               command=self.palaute_seuraava(self.palaute1)).pack()

        self.kysymykset = []

        Label(ikkuna, text="Kirjoita palautteesi tähän:",
              font=("Arial", 15, "bold"), bg="blue").pack()

        self.sanallinen_laatikko = Text(ikkuna, width=30, height=10)
        self.sanallinen_laatikko.pack()

        def tarkistus():
            self.sanallinen = self.sanallinen_laatikko.get(1.0, "end-1c")
            if not self.sanallinen:
                messagebox.showerror(
                    "Virhe", "Anna palautetta!", parent=self.palauteikkuna)
                return False
            return True

        Button(ikkuna, text="Seuraava", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.vain_sanallinen3, tarkistus)
        ).pack()

        self.palauteikkuna.mainloop()

    def vain_sanallinen3(self):
        ikkuna = self.alusta_palauteikkuna(3, 4)

        Button(ikkuna,
               text="Takaisin", bg="red",
               font=("Arial", 15, "bold"),
               command=self.palaute_seuraava(self.vain_sanallinen2)).pack()

        Label(ikkuna, text=f"Kirjoita palautteesi tähän:",
              font=("Arial", 15, "bold"), bg="blue").pack()
        Label(ikkuna, text=self.sanallinen, bg="blue").pack()

        Button(ikkuna, text="Lähetä", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.laheta_palaute)
        ).pack()

        self.palauteikkuna.mainloop()

    def laheta_palaute(self):
        with open(PALAUTTEET_TIEDOSTO) as tied:
            palautteet = loads(tied.read())
        uusi = {"Sanallinen palaute": self.sanallinen}
        for kysymys in self.kysymykset:
            uusi_kysymys = {"numero": kysymys["numero"]}
            if "lisatiedot" in kysymys:
                uusi_kysymys["Miksi annoit tämän numeron"] = kysymys["lisatiedot"]
            uusi[kysymys["kysymys"]] = uusi_kysymys
        palautteet.append(uusi)
        with open(PALAUTTEET_TIEDOSTO, "w") as tied:
            tied.write(dumps(palautteet))

        ikkuna = self.alusta_palauteikkuna(5, 5)

        Label(ikkuna, text="Valmis\nPalautteet tallennettu",
              bg="blue", font=("Arial", 25, "bold")).pack()

        for kysymys in self.kysymykset:
            Label(ikkuna, text=f"{kysymys['kysymys']}",
                  bg="blue", font=("Arial", 15, "bold")).pack()
            Label(ikkuna, text=str(kysymys["numero"]), bg="blue").pack()
            if kysymys["numero"] < 5:
                Label(ikkuna, text=f"Miksi annoit tämän numeron?\
\nMitä voisi parantaa?",
                      bg="blue", font=("Arial", 15, "bold")).pack()
                Label(ikkuna, text=kysymys["lisatiedot"], bg="blue").pack()

        Label(ikkuna, text=f"Sanallinen palaute:",
              font=("Arial", 15, "bold"), bg="blue").pack()
        Label(ikkuna, text=self.sanallinen, bg="blue").pack()

        Button(ikkuna, text="Valmis", bg="green", font=(
            "Arial", 30, "bold"), command=self.palaute_seuraava(self.ikkuna.focus_force)
        ).pack()

        self.palauteikkuna.mainloop()
