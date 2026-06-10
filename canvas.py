
import tkinter as tk
from shapes import draw_shape_preview, finalize_shape
from utils import flood_fill


class DrawingCanvas:
    def __init__(self, parent, state):
        self.state = state
        self.last_x = None
        self.last_y = None
        self.preview_item = None   # väliaikainen muoto hiirtä liikuttaessa
        self.start_x = None
        self.start_y = None

        # Kehys
        self.frame = tk.Frame(parent, bg="#1e1e2e")

        # Canvas-widget
        self.canvas = tk.Canvas(
            self.frame,
            bg="#ffffff",
            cursor="crosshair",
            highlightthickness=2,
            highlightbackground="#6c6c8a",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Hiiren tapahtumat
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    #Hiiren tapahtumat

    def _on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.last_x = event.x
        self.last_y = event.y

        tool = self.state["tool"]

        if tool == "fill":
            flood_fill(self.canvas, event.x, event.y, self.state["color"])

    def _on_drag(self, event):
        tool = self.state["tool"]
        color = self.state["color"]
        size = self.state["brush_size"]

        if tool == "pen":
            if self.last_x is not None:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    fill=color, width=size, capstyle=tk.ROUND, smooth=True
                )
            self.last_x = event.x
            self.last_y = event.y

        elif tool == "eraser":
            if self.last_x is not None:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    fill="white", width=size * 3, capstyle=tk.ROUND
                )
            self.last_x = event.x
            self.last_y = event.y

        elif tool in ("line", "rect", "oval"):
            # Poista edellinen esikatselu
            if self.preview_item:
                self.canvas.delete(self.preview_item)
            self.preview_item = draw_shape_preview(
                self.canvas, tool, self.start_x, self.start_y,
                event.x, event.y, color, size, self.state["fill_shape"]
            )

    def _on_release(self, event):
        tool = self.state["tool"]
        color = self.state["color"]
        size = self.state["brush_size"]

        if tool in ("line", "rect", "oval"):
            if self.preview_item:
                self.canvas.delete(self.preview_item)
                self.preview_item = None
            finalize_shape(
                self.canvas, tool, self.start_x, self.start_y,
                event.x, event.y, color, size, self.state["fill_shape"]
            )

        self.last_x = None
        self.last_y = None

    #Julkiset metodit

    def clear(self):
        """Tyhjennä koko alusta."""
        self.canvas.delete("all")

    def get_canvas(self):
        return self.canvas