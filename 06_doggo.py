import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Funktionen
def show_dog():
    global current_image, current_photo

    # Auswahl aus Combobox holen
    rasse = auswahl.get().lower()

    # API-URL zusammenbauen
    if rasse == "zufällig":
        url = "https://dog.ceo/api/breeds/image/random"
    else:
        url = f"https://dog.ceo/api/breed/{rasse}/images/random"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        img_url = data["message"]

        # Bild laden
        img_data = requests.get(img_url).content
        current_image = Image.open(BytesIO(img_data))
        current_photo = ImageTk.PhotoImage(current_image)

        # Bild ins Label einsetzen
        Hund_label.config(image=current_photo)
        Hund_label.image = current_photo  # Referenz halten


def save_dog():
    if current_image:
        current_image.save("hund_api.jpg")
        print("Bild gespeichert als hund_api.jpg")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Süße Hunde!")

    auswahl = tk.StringVar()
    combobox = ttk.Combobox(root, textvariable=auswahl)
    combobox["values"] = ("  Zufällig", "beagle", "labrador", "shiba", "dachshund")
    combobox.current(0)
    combobox.pack(pady=10)

    tk.Label(root,
             text="Wähle eine Hunderasse oder 'zufällig' aus, "
                  "um ein Bild zu erhalten."
             ).pack(pady=10)

    Hund_label = tk.Label(root)  # Platzhalter für Bild
    Hund_label.pack(padx=10, pady=10)

    show_button = tk.Button(root, text="Hundebild anzeigen", command=show_dog)
    show_button.pack(padx=10, pady=5)

    save_button = tk.Button(root, text="Hundebild speichern", command=save_dog)
    save_button.pack(padx=10, pady=5)

    # Platzhalter-Variablen
    current_image = None
    current_photo = None

    root.mainloop()
