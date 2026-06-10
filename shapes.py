


def _outline_and_fill(fill_shape, color):
    outline = color
    fill = color if fill_shape else ""
    return outline, fill


def draw_shape_preview(canvas, tool, x1, y1, x2, y2, color, size, fill_shape):

    outline, fill = _outline_and_fill(fill_shape, color)

    if tool == "line":
        return canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=size, dash=(4, 4)
        )

    elif tool == "rect":
        return canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=outline, fill=fill,
            width=size, dash=(4, 4)
        )

    elif tool == "oval":
        return canvas.create_oval(
            x1, y1, x2, y2,
            outline=outline, fill=fill,
            width=size, dash=(4, 4)
        )

    return None


def finalize_shape(canvas, tool, x1, y1, x2, y2, color, size, fill_shape):
    
    outline, fill = _outline_and_fill(fill_shape, color)

    if tool == "line":
        canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=size, capstyle="round"
        )

    elif tool == "rect":
        canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=outline, fill=fill, width=size
        )

    elif tool == "oval":
        canvas.create_oval(
            x1, y1, x2, y2,
            outline=outline, fill=fill, width=size
        )