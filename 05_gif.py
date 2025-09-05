import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO

current_frames = []
frame_index = 0
current_gif = None
animation_running = False

# 👉 Deinen eigenen API-Key hier einsetzen
API_KEY = ""


def neues_gif():
    global current_frames, frame_index, current_gif, animation_running

    # Giphy Random Endpoint
    url = f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag=funny"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        img_url = data["data"]["images"]["original"]["url"]

        # GIF laden
        img_data = requests.get(img_url).content
        pil_img = Image.open(BytesIO(img_data))

        # Für später speichern
        current_gif = pil_img

        # Frames vorbereiten
        current_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                          for frame in ImageSequence.Iterator(pil_img)]

        frame_index = 0
        animation_running = True
        animate()
    else:
        print("Fehler beim Laden des GIF:", response.status_code)


def animate():
    global frame_index
    if animation_running and current_frames:
        meme_label.config(image=current_frames[frame_index])
        frame_index = (frame_index + 1) % len(current_frames)
        root.after(100, animate)  # Geschwindigkeit (ms) → kannst du anpassen


def speichern_gif():
    if current_gif:
        # Komplettes GIF mit allen Frames speichern
        frames = [frame.copy() for frame in ImageSequence.Iterator(current_gif)]
        frames[0].save(
            "meme.gif",
            save_all=True,
            append_images=frames[1:],
            loop=0
        )
        print("GIF gespeichert als meme.gif")
    else:
        print("Kein GIF zum Speichern vorhanden")


def destroy():
    global animation_running
    animation_running = False
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Giphy Finder")

    meme_label = tk.Label(root)
    meme_label.pack(padx=10, pady=10)

    new_button = tk.Button(root, text="Neues GIF suchen", command=neues_gif)
    new_button.pack(padx=10, pady=5)

    save_button = tk.Button(root, text="Speichern", command=speichern_gif)
    save_button.pack(padx=10, pady=5)

    close_button = tk.Button(root, text="Schließen", command=destroy)
    close_button.pack(padx=10, pady=5)

    root.mainloop()
