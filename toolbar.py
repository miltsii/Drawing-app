
import tkinter as tk
from tkinter import colorchooser
from utils import save_image, share_image


TOOLS = [
    ("✏️", "pen",    "Kynä"),
    ("⬜", "rect",   "Suorakaide"),
    ("⭕", "oval",   "Ellipsi"),
    ("╱",  "line",   "Viiva"),
    ("🪣", "fill",   "Täyttö"),
    ("🧹", "eraser", "Pyyhekumi"),
]

PALETTE = [
    "#ffffff", "#000000", "#e63946", "#f4a261",
    "#2a9d8f", "#457b9d", "#a8dadc", "#e9c46a",
    "#8338ec", "#ff006e", "#fb5607", "#3a86ff",
]


class Toolbar:
    def __init__(self, parent, state):
        self.state = state
        self.canvas_ref = None   # asetetaan myöhemmin set_canvas():lla
        self._tool_buttons = {}

        self.frame = tk.Frame(parent, bg="#2a2a3e", width=130)
        self.frame.pack_propagate(False)

        self._build(self.frame)

    def set_canvas(self, drawing_canvas):
        self.canvas_ref = drawing_canvas

    #Rakentaminen
    def _build(self, parent):
        self._section_label(parent, "TYÖKALUT")
        self._build_tools(parent)

        self._section_label(parent, "VÄRI")
        self._build_color_picker(parent)
        self._build_palette(parent)

        self._section_label(parent, "KOKO")
        self._build_brush_slider(parent)

        self._section_label(parent, "MUODOT")
        self._build_fill_toggle(parent)

        self._section_label(parent, "TIEDOSTO")
        self._build_file_buttons(parent)

    def _section_label(self, parent, text):
        tk.Label(
            parent, text=text, bg="#2a2a3e", fg="#6c6c8a",
            font=("Helvetica", 8, "bold")
        ).pack(pady=(12, 2))

    #Työkalut

    def _build_tools(self, parent):
        grid = tk.Frame(parent, bg="#2a2a3e")
        grid.pack()

        for i, (icon, tool_id, tooltip) in enumerate(TOOLS):
            btn = tk.Button(
                grid, text=icon, width=4, font=("Helvetica", 14),
                bg="#3a3a5e", fg="white", relief=tk.FLAT,
                activebackground="#5a5a8e",
                command=lambda t=tool_id: self._select_tool(t)
            )
            btn.grid(row=i // 2, column=i % 2, padx=2, pady=2)
            self._tool_buttons[tool_id] = btn
            self._add_tooltip(btn, tooltip)

        self._select_tool("pen")

    def _select_tool(self, tool_id):
        self.state["tool"] = tool_id
        for tid, btn in self._tool_buttons.items():
            btn.configure(bg="#5a5a9e" if tid == tool_id else "#3a3a5e")

    #Väri
    def _build_color_picker(self, parent):
        self.color_preview = tk.Label(
            parent, bg=self.state["color"],
            width=8, height=2, relief=tk.FLAT,
            cursor="hand2"
        )
        self.color_preview.pack(pady=4)
        self.color_preview.bind("<Button-1>", self._pick_color)

    def _pick_color(self, _event=None):
        color = colorchooser.askcolor(
            color=self.state["color"], title="Valitse väri"
        )[1]
        if color:
            self.state["color"] = color
            self.color_preview.configure(bg=color)

    def _build_palette(self, parent):
        grid = tk.Frame(parent, bg="#2a2a3e")
        grid.pack()
        for i, hex_color in enumerate(PALETTE):
            swatch = tk.Label(
                grid, bg=hex_color, width=2, height=1,
                cursor="hand2", relief=tk.RAISED
            )
            swatch.grid(row=i // 4, column=i % 4, padx=1, pady=1)
            swatch.bind("<Button-1>", lambda e, c=hex_color: self._set_color(c))

    def _set_color(self, color):
        self.state["color"] = color
        self.color_preview.configure(bg=color)

    #Sivellin
    def _build_brush_slider(self, parent):
        self.size_label = tk.Label(
            parent, text=f"Koko: {self.state['brush_size']}",
            bg="#2a2a3e", fg="#ccccdd", font=("Helvetica", 9)
        )
        self.size_label.pack()

        slider = tk.Scale(
            parent, from_=1, to=40, orient=tk.HORIZONTAL,
            bg="#2a2a3e", fg="#ccccdd", troughcolor="#3a3a5e",
            highlightthickness=0, length=110,
            command=self._set_brush_size
        )
        slider.set(self.state["brush_size"])
        slider.pack()

    def _set_brush_size(self, val):
        self.state["brush_size"] = int(val)
        self.size_label.configure(text=f"Koko: {val}")

    #Täyttö-asetus

    def _build_fill_toggle(self, parent):
        self.fill_var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(
            parent, text="Täytä muoto", variable=self.fill_var,
            bg="#2a2a3e", fg="#ccccdd", selectcolor="#3a3a5e",
            activebackground="#2a2a3e", activeforeground="white",
            font=("Helvetica", 9),
            command=lambda: self.state.update(fill_shape=self.fill_var.get())
        )
        cb.pack(pady=2)

    #Tiedosto-painikkeet

    def _build_file_buttons(self, parent):
        for text, cmd in [
            ("💾 Tallenna", self._save),
            ("🔗 Jaa",      self._share),
            ("🗑️ Tyhjennä", self._clear),
        ]:
            tk.Button(
                parent, text=text, bg="#3a3a5e", fg="white",
                font=("Helvetica", 9), relief=tk.FLAT,
                activebackground="#5a5a8e", width=13,
                command=cmd
            ).pack(pady=2)

    def _save(self):
        if self.canvas_ref:
            save_image(self.canvas_ref.get_canvas())

    def _share(self):
        if self.canvas_ref:
            share_image(self.canvas_ref.get_canvas())

    def _clear(self):
        if self.canvas_ref:
            self.canvas_ref.clear()

    #Tooltip

    def _add_tooltip(self, widget, text):
        tip = None

        def show(e):
            nonlocal tip
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.geometry(f"+{e.x_root+12}+{e.y_root+6}")
            tk.Label(
                tip, text=text, bg="#ffffe0", relief=tk.SOLID,
                borderwidth=1, font=("Helvetica", 9)
            ).pack()

        def hide(_e):
            nonlocal tip
            if tip:
                tip.destroy()
                tip = None

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)