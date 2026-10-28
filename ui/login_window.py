"""Login window: password validation."""

import tkinter as tk
from tkinter import messagebox

from constants import (APP_NAME, COURSE_CODE, COURSE_NAME, LOGIN_PASSWORD,
                       LOGIN_TITLE, PROGRAM_NAME, STUDENT_NAME)
from ui.helpers import center_window, show_about
from ui.pastel_button import PastelButton
from ui.theme import Theme
from utils.formatters import today_text


class LoginWindow(tk.Tk):
    """Split-layout login: brand panel on the left, password card on the right."""

    WIDTH = 820
    HEIGHT = 500

    def __init__(self) -> None:
        super().__init__()
        self.authenticated = False
        self.password_var = tk.StringVar()

        self.title(LOGIN_TITLE)
        self.configure(bg=Theme.SURFACE)
        self.resizable(False, False)
        Theme.apply(self)

        self._build_menu()
        self._build_brand_panel()
        self._build_login_panel()
        center_window(self, self.WIDTH, self.HEIGHT)

        self.bind("<Return>", lambda _event: self._login())
        self.password_entry.focus_set()

    # -- layout ----------------------------------------------------------------
    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self)
        menu_bar.add_command(label="About", command=lambda: show_about(self))
        self.config(menu=menu_bar)

    def _build_brand_panel(self) -> None:
        panel = tk.Frame(self, bg=Theme.BRAND, width=340)
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)

        tk.Label(panel, text="🌼", bg=Theme.BRAND, font=(Theme.FAMILY, 54)).pack(pady=(42, 0))
        tk.Label(panel, text="Compensándote", bg=Theme.BRAND, fg=Theme.PURPLE,
                 font=Theme.FONT_TITLE).pack()
        tk.Label(panel, text="Family Compensation Fund\nAffiliation Control", bg=Theme.BRAND,
                 fg=Theme.MUTED, font=Theme.FONT).pack(pady=(4, 22))

        card = tk.Frame(panel, bg=Theme.BRAND_CARD, padx=16, pady=12)
        card.pack(fill="x", padx=28)
        info = (
            ("Application", APP_NAME),
            ("Student", STUDENT_NAME),
            ("Course", f"{COURSE_NAME} · {COURSE_CODE}"),
            ("Date", today_text()),
        )
        for label, value in info:
            tk.Label(card, text=label, bg=Theme.BRAND_CARD, fg=Theme.MUTED,
                     font=Theme.FONT_SMALL, anchor="w").pack(fill="x")
            tk.Label(card, text=value, bg=Theme.BRAND_CARD, fg=Theme.TEXT,
                     font=Theme.FONT_BOLD, anchor="w").pack(fill="x", pady=(0, 6))

    def _build_login_panel(self) -> None:
        panel = tk.Frame(self, bg=Theme.SURFACE)
        panel.pack(side="left", fill="both", expand=True, padx=52)

        tk.Label(panel, text="Welcome 👋", bg=Theme.SURFACE, fg=Theme.TEXT,
                 font=(Theme.FAMILY, 24, "bold"), anchor="w").pack(fill="x", pady=(70, 0))
        tk.Label(panel, text="Enter your password to open the affiliate control.",
                 bg=Theme.SURFACE, fg=Theme.MUTED, font=Theme.FONT, anchor="w"
                 ).pack(fill="x", pady=(2, 28))

        tk.Label(panel, text="Password", bg=Theme.SURFACE, fg=Theme.PURPLE,
                 font=Theme.FONT_BOLD, anchor="w").pack(fill="x")

        self.field = tk.Frame(panel, bg=Theme.FIELD, highlightbackground=Theme.BORDER,
                              highlightthickness=2)
        self.field.pack(fill="x", pady=(6, 2), ipady=6)
        tk.Label(self.field, text="🔒", bg=Theme.FIELD, font=Theme.FONT).pack(
            side="left", padx=(10, 4))
        self.password_entry = tk.Entry(
            self.field, textvariable=self.password_var, show="*", bd=0, bg=Theme.FIELD,
            fg=Theme.TEXT, insertbackground=Theme.TEXT, font=(Theme.FAMILY, 12),
            relief="flat")
        self.password_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.password_entry.bind(
            "<FocusIn>", lambda _e: self.field.config(highlightbackground=Theme.FOCUS))
        self.password_entry.bind(
            "<FocusOut>", lambda _e: self.field.config(highlightbackground=Theme.BORDER))
        tk.Button(self.field, text="👁", bg=Theme.FIELD, activebackground=Theme.FIELD,
                  fg=Theme.MUTED, bd=0, relief="flat", cursor="hand2",
                  command=self._toggle_password).pack(side="right", padx=10)

        tk.Label(panel, text="Password masked (* * *)", bg=Theme.SURFACE, fg=Theme.MUTED,
                 font=Theme.FONT_SMALL, anchor="w").pack(fill="x", pady=(2, 22))

        buttons = tk.Frame(panel, bg=Theme.SURFACE)
        buttons.pack(fill="x")
        buttons.columnconfigure((0, 1), weight=1, uniform="login")
        PastelButton(buttons, "Login  →", self._login, Theme.MINT).grid(
            row=0, column=0, sticky="ew", padx=(0, 6), ipady=11)
        PastelButton(buttons, "🚪  Exit", self.destroy, Theme.PINK).grid(
            row=0, column=1, sticky="ew", padx=(6, 0), ipady=11)

        PastelButton(panel, "ℹ  About", lambda: show_about(self), Theme.LAVENDER).pack(
            fill="x", pady=(14, 0), ipady=7)

        tk.Label(panel, text=PROGRAM_NAME, bg=Theme.SURFACE, fg=Theme.MUTED,
                 font=Theme.FONT_SMALL).pack(side="bottom", pady=14)

    # -- actions ---------------------------------------------------------------
    def _toggle_password(self) -> None:
        masked = self.password_entry.cget("show") == "*"
        self.password_entry.config(show="" if masked else "*")

    def _login(self) -> None:
        if self.password_var.get() == LOGIN_PASSWORD:
            self.authenticated = True
            self.destroy()  # close the login; main.py then opens the data form
            return
        messagebox.showerror("Access denied", "Incorrect password. Please try again.",
                             parent=self)
        self.password_var.set("")
        self.password_entry.focus_set()
