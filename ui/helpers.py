"""Small window helpers shared by the UI classes."""

import tkinter as tk
from tkinter import messagebox

from constants import (COLLABORATIVE_GROUP, COURSE_CODE, COURSE_NAME,
                       PROGRAM_NAME, STUDENT_NAME)
from utils.formatters import today_text


def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Place the window in the middle of the screen."""
    x = max(0, (window.winfo_screenwidth() - width) // 2)
    y = max(0, (window.winfo_screenheight() - height) // 2 - 20)
    window.geometry(f"{width}x{height}+{x}+{y}")


def shade_color(hex_color: str, factor: float) -> str:
    """Lighten (>1) or darken (<1) a #rrggbb color."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    r, g, b = (max(0, min(255, int(c * factor))) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def show_about(parent: tk.Misc) -> None:
    """Dialog with the course, student and collaborative group information."""
    messagebox.showinfo(
        "About",
        f"Course: {COURSE_NAME} — {COURSE_CODE}\n"
        f"Student: {STUDENT_NAME}\n"
        f"Collaborative Group: {COLLABORATIVE_GROUP}\n"
        f"{PROGRAM_NAME}\n"
        f"{today_text()}",
        parent=parent,
    )
