import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

current_img = None

def neues_gif():
    global current_img
    response = requests.get("https://meme-api.com/gimme")
    if response.status_code == 200:
        data = response.json()
        img_url = data["url"]

        # Bild laden
        img_data = requests.get(img_url).content
        pil_img = Image.open(BytesIO(img_data))

        # Im Tkinter-Format speichern
        current_img = pil_img
        tk_img = ImageTk.PhotoImage(pil_img)

        meme_label.config(image=tk_img)
        meme_label.image = tk_img  


def speichern_gif():
    if current_img is not None:
        current_img.save("meme.png")
        print("Meme gespeichert als meme.png")
    else:
        print("Kein Bild zum Speichern vorhanden")


def destroy():
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("GIF Finder")

    # Label für das Meme
    meme_label = tk.Label(root)
    meme_label.pack(padx=10, pady=10)

    # Button für suchen
    new_button = tk.Button(root, text="Suchen", command=neues_gif)
    new_button.pack(padx=10, pady=5)

    # Button für speichern
    save_button = tk.Button(root, text="Speichern", command=speichern_gif)
    save_button.pack(padx=10, pady=5)

    # Button für Schließen Meme
    close_button = tk.Button(root, text="Schließen", command=destroy)
    close_button.pack(padx=10, pady=5)

    root.mainloop()
