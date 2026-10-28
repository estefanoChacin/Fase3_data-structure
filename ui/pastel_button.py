"""Flat pastel button with hover effect."""

import tkinter as tk

from ui.helpers import shade_color
from ui.theme import Theme


class PastelButton(tk.Button):
    """A flat button painted with a pastel (background, text) color pair."""

    def __init__(self, parent: tk.Misc, text: str, command, palette: tuple, **kwargs) -> None:
        background, foreground = palette
        super().__init__(
            parent, text=text, command=command, bg=background, fg=foreground,
            activebackground=shade_color(background, 0.94), activeforeground=foreground,
            relief="flat", bd=0, cursor="hand2", font=Theme.FONT_BOLD,
            highlightthickness=0, **kwargs,
        )
        self._background = background
        self.bind("<Enter>", lambda _e: self.config(bg=shade_color(self._background, 0.94)))
        self.bind("<Leave>", lambda _e: self.config(bg=self._background))
