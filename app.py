# app.py — Pääikkuna, kokoaa kaikki osat yhteen

import tkinter as tk
from canvas import DrawingCanvas
from toolbar import Toolbar


class DrawingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎨 Piirustussovellus")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)

        # Jaettu tila — kaikki osat lukevat tästä
        self.state = {
            "tool": "pen",           # pen | eraser | line | rect | oval | fill
            "color": "#ffffff",
            "bg_color": "#1e1e2e",
            "brush_size": 4,
            "fill_shape": False,
        }

        self._build_ui()

    def _build_ui(self):
        # Vasemmalle: työkalupalkki
        self.toolbar = Toolbar(self.root, self.state)
        self.toolbar.frame.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0), pady=8)

        # Oikealle: piirtoalusta
        self.canvas = DrawingCanvas(self.root, self.state)
        self.canvas.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Anna toolbarille viittaus canvasiin (tallennusta varten)
        self.toolbar.set_canvas(self.canvas)

    def run(self):
        self.root.mainloop()