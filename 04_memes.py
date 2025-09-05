import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

current_img = None  # globale Variable für das aktuelle Bild

def neues_meme():
    global current_img
    try:
        # API aufrufen
        response = requests.get("https://meme-api.com/gimme")
        if response.status_code == 200:
            data = response.json()
            img_url = data["url"]

            # Bild herunterladen
            img_data = requests.get(img_url).content
            img = Image.open(BytesIO(img_data))
            img = img.resize((400, 400))  # optional skalieren
            current_img = img

            # In Tkinter anzeigen
            tk_img = ImageTk.PhotoImage(img)
            meme_label.config(image=tk_img)
            meme_label.image = tk_img
        else:
            print("Fehler beim Laden des Memes:", response.status_code)
    except Exception as e:
        print("Fehler:", e)

def meme_speichern():
    if current_img is not None:
        current_img.save("meme.png")
        print("Meme gespeichert als meme.png")
    else:
        print("Kein Bild zum Speichern vorhanden")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Meme anzeigen")

    # Label für das Meme
    meme_label = tk.Label(root)
    meme_label.pack(padx=10, pady=10)

    # Button für neues Meme
    new_button = tk.Button(root, text="Neues Meme", command=neues_meme)
    new_button.pack(padx=10, pady=5)

    # Button für Meme speichern
    save_button = tk.Button(root, text="Meme speichern", command=meme_speichern)
    save_button.pack(padx=10, pady=5)

    root.mainloop()
