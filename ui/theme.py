"""Pastel light theme shared by every window."""

import tkinter as tk
from tkinter import ttk


class Theme:
    """Colors, fonts and ttk styles of the application."""

    # -- surfaces ---------------------------------------------------------------
    BG = "#FAF7FF"
    SURFACE = "#FFFFFF"
    HEADER = "#E9E1F7"
    BRAND = "#E4D9F7"
    BRAND_CARD = "#F4EEFD"
    FIELD = "#F4F0FB"
    BORDER = "#DCD2EE"
    FOCUS = "#9E88DB"

    # -- text -------------------------------------------------------------------
    TEXT = "#3F3557"
    MUTED = "#8C84A6"
    PURPLE = "#5B4A99"

    # -- pastel palette (background, text) ------------------------------------------
    LAVENDER = ("#DCCFF5", "#5B4A99")
    MINT = ("#BDEBD7", "#256650")
    PINK = ("#F9C6D5", "#9B2F55")
    SKY = ("#C4E2F7", "#245E8A")
    PEACH = ("#FFD9BF", "#8F4E1F")
    CLOUD = ("#E6E1F0", "#4B4466")
    BUTTER = ("#FFF3C9", "#7A5C00")

    # -- table ------------------------------------------------------------------
    ROW_ODD = "#FFFFFF"
    ROW_EVEN = "#F8F4FE"
    SELECTED = "#D9CCF4"

    # -- fonts ------------------------------------------------------------------
    FAMILY = "Segoe UI"
    FONT = (FAMILY, 10)
    FONT_SMALL = (FAMILY, 9)
    FONT_BOLD = (FAMILY, 10, "bold")
    FONT_CHIP = (FAMILY, 9, "bold")
    FONT_HEADER = (FAMILY, 15, "bold")
    FONT_TITLE = (FAMILY, 24, "bold")
    FONT_MONO = ("Consolas", 9)

    @classmethod
    def apply(cls, root: tk.Tk) -> None:
        """Configure the ttk widgets with the pastel look."""
        style = ttk.Style(root)
        style.theme_use("clam")

        root.option_add("*TCombobox*Listbox.background", cls.SURFACE)
        root.option_add("*TCombobox*Listbox.foreground", cls.TEXT)
        root.option_add("*TCombobox*Listbox.selectBackground", cls.SELECTED)
        root.option_add("*TCombobox*Listbox.selectForeground", cls.TEXT)
        root.option_add("*TCombobox*Listbox.font", f"{{{cls.FAMILY}}} 10")

        border = dict(bordercolor=cls.BORDER, lightcolor=cls.BORDER, darkcolor=cls.BORDER)
        focus = dict(
            bordercolor=[("focus", cls.FOCUS)],
            lightcolor=[("focus", cls.FOCUS)],
            darkcolor=[("focus", cls.FOCUS)],
        )

        style.configure("App.TEntry", fieldbackground=cls.FIELD, foreground=cls.TEXT,
                        insertcolor=cls.TEXT, padding=7, **border)
        style.map("App.TEntry", **focus)

        for name, (bg, fg) in (("Tariff.TEntry", cls.MINT), ("Report.TEntry", cls.BUTTER)):
            style.configure(name, fieldbackground=bg, foreground=fg, padding=7,
                            font=cls.FONT_BOLD, **border)
            style.map(name, fieldbackground=[("readonly", bg)],
                      foreground=[("readonly", fg)])

        style.configure("App.TCombobox", fieldbackground=cls.FIELD, background=cls.HEADER,
                        foreground=cls.TEXT, arrowcolor=cls.PURPLE, padding=6, **border)
        style.map("App.TCombobox",
                  fieldbackground=[("readonly", cls.FIELD)],
                  foreground=[("readonly", cls.TEXT)],
                  selectbackground=[("readonly", cls.FIELD)],
                  selectforeground=[("readonly", cls.TEXT)],
                  **focus)

        style.configure("App.TSpinbox", fieldbackground=cls.FIELD, background=cls.HEADER,
                        foreground=cls.TEXT, arrowcolor=cls.PURPLE, insertcolor=cls.TEXT,
                        padding=6, **border)
        style.map("App.TSpinbox", **focus)

        style.configure("App.TRadiobutton", background=cls.SURFACE, foreground=cls.TEXT,
                        focuscolor=cls.SURFACE, font=cls.FONT)
        style.map("App.TRadiobutton",
                  background=[("active", cls.SURFACE)],
                  indicatorcolor=[("selected", cls.PURPLE), ("!selected", cls.FIELD)])

        style.configure("App.Treeview", background=cls.SURFACE, fieldbackground=cls.SURFACE,
                        foreground=cls.TEXT, rowheight=30, borderwidth=0, font=cls.FONT)
        style.map("App.Treeview", background=[("selected", cls.SELECTED)],
                  foreground=[("selected", cls.TEXT)])
        style.configure("App.Treeview.Heading", background=cls.HEADER, foreground=cls.PURPLE,
                        relief="flat", font=cls.FONT_BOLD, padding=7)
        style.map("App.Treeview.Heading", background=[("active", cls.LAVENDER[0])])

        for orientation in ("Vertical", "Horizontal"):
            style.configure(f"App.{orientation}.TScrollbar", background=cls.HEADER,
                            troughcolor=cls.BG, bordercolor=cls.BG, arrowcolor=cls.PURPLE,
                            lightcolor=cls.HEADER, darkcolor=cls.HEADER)
