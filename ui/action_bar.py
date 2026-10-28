"""Row of action buttons of the main window."""

import tkinter as tk
from typing import Callable

from ui.pastel_button import PastelButton
from ui.theme import Theme


class ActionBar(tk.Frame):
    """Register / Delete / Report / Clear / Exit buttons."""

    def __init__(self, parent: tk.Misc, on_register: Callable, on_delete: Callable,
                 on_report: Callable, on_clear: Callable, on_exit: Callable) -> None:
        super().__init__(parent, bg=Theme.BG)
        self.columnconfigure(tuple(range(5)), weight=1, uniform="actions")

        buttons = (
            ("✚  Register", on_register, Theme.MINT),
            ("🗑  Delete", on_delete, Theme.PINK),
            ("📊  Report", on_report, Theme.SKY),
            ("🧹  Clear", on_clear, Theme.PEACH),
            ("🚪  Exit", on_exit, Theme.CLOUD),
        )
        for column, (text, command, palette) in enumerate(buttons):
            PastelButton(self, text, command, palette).grid(
                row=0, column=column, sticky="ew", padx=5, ipady=11)
