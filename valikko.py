from tkinter import Button, Label, Tk

import Arkanoid
import Muu
import TasonHallinta
import TasonTekija


def valikko():
    """
    Avaa valikon
    ```python
    if __name__ == "__main__":
        valikko()
    ```
    """

    def pelaa():
        ikkuna.destroy()
        Arkanoid.Arkanoid()

    def tee_taso():
        ikkuna.destroy()
        TasonTekija.TasonTekija()

    def tason_hallinta():
        ikkuna.destroy()
        TasonHallinta.TasonHallinta()

    def muu():
        ikkuna.destroy()
        Muu.Muu()

    ikkuna = Tk()
    ikkuna["bg"] = "blue"
    ikkuna.title("Valikko - Arkanoid")
    ikkuna.geometry("600x600")

    Label(ikkuna, text="Arkanoid", font=(
        "Arial", 50, "bold"), bg="blue").pack()
    Button(ikkuna, text="Pelaa", font=(
        "Arial", 50, "bold"), command=pelaa, bg="red").pack()
    Button(ikkuna, text="Tee taso", font=(
        "Arial", 50, "bold"), command=tee_taso, bg="red").pack()
    Button(ikkuna, text="Tasojen hallinta", font=(
        "Arial", 50, "bold"), command=tason_hallinta, bg="red").pack()
    Button(ikkuna, text="Muu", font=(
        "Arial", 50, "bold"), command=muu, bg="red").pack()

    ikkuna.mainloop()
