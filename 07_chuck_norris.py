import tkinter as tk
from tkinter import ttk
import requests
from deep_translator import GoogleTranslator
import threading

api_url = "https://api.chucknorris.io/jokes/random"

def safe_hello():
    def task():
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                witz_text = data['value']

                if auswahl.get() == "de":
                    witz_text = GoogleTranslator(source="en", target="de").translate(witz_text)

                label_witz.config(text=witz_text)
            else:
                label_witz.config(text="Fehler beim Abrufen des Witzes")
        except Exception as e:
            label_witz.config(text=f"Fehler: {e}")

    threading.Thread(target=task).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chuck Norris Witze")

    tk.Label(root, text="Witz-Sprache wählen:").pack()

    auswahl = tk.StringVar(value="en")
    combo = ttk.Combobox(
        root,
        textvariable=auswahl,
        values=["en", "de"],
        width=15,
        state="readonly"
    )
    combo.pack()

    tk.Button(root, text="Neuer Witz!", command=safe_hello).pack()

    label_witz = tk.Label(root, text="", wraplength=300, justify="left")
    label_witz.pack()

    root.mainloop()
