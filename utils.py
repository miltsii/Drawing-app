

import tkinter as tk
from tkinter import filedialog, messagebox
import os

try:
    from PIL import ImageGrab, Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def save_image(canvas: tk.Canvas):
    
    if not PIL_AVAILABLE:
        messagebox.showerror(
            "Puuttuva kirjasto",
            "Asenna Pillow tallennusta varten:\n\npip install Pillow"
        )
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG-kuva", "*.png"), ("JPEG-kuva", "*.jpg"), ("Kaikki", "*.*")],
        title="Tallenna piirustus"
    )
    if not filepath:
        return  # Käyttäjä peruutti

    try:
        # Ota kuvakaappaus canvasin alueelta
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        w = x + canvas.winfo_width()
        h = y + canvas.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))
        img.save(filepath)

        messagebox.showinfo("Tallennettu", f"Piirustus tallennettu:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Virhe tallennuksessa", str(e))


#Jakaminen

def share_image(canvas: tk.Canvas):
    
    if not PIL_AVAILABLE:
        messagebox.showerror(
            
        )
        return

    try:
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        w = x + canvas.winfo_width()
        h = y + canvas.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, w, h))

        
        temp_path = os.path.join(os.path.expanduser("~"), "piirustus_jaa.png")
        img.save(temp_path)

        # Näytä polku ikkunassa
        share_window = tk.Toplevel()
        share_window.title("Jaa piirustus")
        share_window.geometry("400x150")
        share_window.configure(bg="#2a2a3e")

        tk.Label(
            share_window,
            text="Kuva tallennettu jakamista varten:",
            bg="#2a2a3e", fg="white", font=("Helvetica", 10)
        ).pack(pady=(20, 5))

        path_var = tk.StringVar(value=temp_path)
        entry = tk.Entry(
            share_window, textvariable=path_var,
            width=50, state="readonly"
        )
        entry.pack(padx=20)

        def copy_path():
            share_window.clipboard_clear()
            share_window.clipboard_append(temp_path)
            messagebox.showinfo("Kopioitu", "Polku kopioitu leikepöydälle!")

        tk.Button(
            share_window, text="📋 Kopioi polku",
            bg="#5a5a8e", fg="white", relief=tk.FLAT,
            command=copy_path
        ).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Virhe", str(e))


#Täyttötyökalu

def flood_fill(canvas: tk.Canvas, x: int, y: int, fill_color: str):
    
    # Etsi päällimmäinen elementti klikkauskohdasta
    item = canvas.find_closest(x, y)
    if not item:
        # Tyhjä canvas — vaihda taustaväri
        canvas.configure(bg=fill_color)
        return

    item_id = item[0]
    item_type = canvas.type(item_id)

    try:
        if item_type in ("rectangle", "oval", "polygon"):
            canvas.itemconfig(item_id, fill=fill_color)
        elif item_type == "line":
            canvas.itemconfig(item_id, fill=fill_color)
        else:
            # Muille tyypeille: vaihda canvasin tausta
            canvas.configure(bg=fill_color)
    except tk.TclError:
        canvas.configure(bg=fill_color)