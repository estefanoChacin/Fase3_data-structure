"""Data-entry form (three pastel cards) of the main window."""

import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
from typing import Callable, Optional

from constants import (EMPLOYEE, ID_TYPES, INDEPENDENT, SERVICES, STACK,STRUCTURE_NAMES)
from models.affiliate_data_structure import AffiliateDataStructure
from services.fee_calculator import FeeCalculator
from ui.theme import Theme
from utils.formatters import format_currency


class AffiliateForm(tk.Frame):
    """Collects the affiliate data, validates it and computes the tariff."""

    def __init__(self, parent: tk.Misc, on_structure_change: Callable[[], None]) -> None:
        super().__init__(parent, bg=Theme.BG)
        self._on_structure_change = on_structure_change

        self._create_variables()
        self.columnconfigure((0, 1, 2), weight=1, uniform="cards")
        self._build_identification_card()
        self._build_economic_card()
        self._build_affiliation_card()
        self._register_traces()

    # -- state -----------------------------------------------------------------
    def _create_variables(self) -> None:
        today = date.today()
        self.id_type_var = tk.StringVar(value=ID_TYPES[0])
        self.id_number_var = tk.StringVar()
        self.full_name_var = tk.StringVar()
        self.income_var = tk.StringVar()
        self.employment_var = tk.StringVar(value=EMPLOYEE)
        self.service_var = tk.StringVar(value=next(iter(SERVICES)))
        self.fee_var = tk.StringVar()
        self.day_var = tk.StringVar(value=str(today.day))
        self.month_var = tk.StringVar(value=str(today.month))
        self.year_var = tk.StringVar(value=str(today.year))
        self.structure_var = tk.StringVar(value=STACK)
        self.report_var = tk.StringVar()

    def _register_traces(self) -> None:
        for variable in (self.income_var, self.employment_var, self.service_var):
            variable.trace_add("write", self._update_fee)

    # -- public API ---------------------------------------------------------------
    @property
    def structure(self) -> str:
        """Data structure currently selected (Stack, Queue or List)."""
        return self.structure_var.get()

    def set_report(self, text: str) -> None:
        self.report_var.set(text)

    def focus_first(self) -> None:
        self.id_number_entry.focus_set()

    def clear(self) -> None:
        """Reset every field. The stored records are never touched."""
        today = date.today()
        self.id_type_var.set(ID_TYPES[0])
        self.id_number_var.set("")
        self.full_name_var.set("")
        self.income_var.set("")
        self.employment_var.set(EMPLOYEE)
        self.service_var.set(next(iter(SERVICES)))
        self.fee_var.set("")
        self.day_var.set(str(today.day))
        self.month_var.set(str(today.month))
        self.year_var.set(str(today.year))
        self.report_var.set("")
        self.focus_first()

    def read_affiliate(self) -> Optional[AffiliateDataStructure]:
        """Validate the form and build an affiliate; None if something is wrong."""
        id_number = self.id_number_var.get().strip()
        full_name = " ".join(self.full_name_var.get().split())
        income_text = self.income_var.get().strip()

        missing = []
        if not self.id_type_var.get():
            missing.append("ID Type")
        if not id_number:
            missing.append("ID Number")
        if not full_name:
            missing.append("Full Name")
        if not income_text:
            missing.append("Current Income")
        if not self.service_var.get():
            missing.append("Desired Service")
        if not self.employment_var.get():
            missing.append("Employment Type")
        if missing:
            messagebox.showwarning(
                "Missing data",
                "Please complete the following required fields:\n\n• " + "\n• ".join(missing),
                parent=self)
            return None

        income = int(income_text)
        if income <= 0:
            messagebox.showwarning("Invalid income", "Income must be greater than zero.",
                                   parent=self)
            return None

        try:
            affiliation_date = date(int(self.year_var.get()), int(self.month_var.get()),
                                    int(self.day_var.get()))
        except ValueError:
            messagebox.showwarning("Invalid date",
                                   "Please enter a valid affiliation date.", parent=self)
            return None

        fee = FeeCalculator.calculate(income, self.employment_var.get(), self.service_var.get())
        return AffiliateDataStructure(
            id_type=self.id_type_var.get(),
            id_number=id_number,
            full_name=full_name,
            current_income=income,
            desired_service=self.service_var.get(),
            employment_type=self.employment_var.get(),
            affiliation_fee=fee,
            affiliation_date=affiliation_date,
        )

    # -- cards -----------------------------------------------------------------
    def _build_identification_card(self) -> None:
        card = self._create_card(0, "👤  Identification", Theme.LAVENDER)

        self._add_label(card, "ID Type", 1, 0)
        self._add_label(card, "ID Number (digits only)", 1, 1)
        self._place(ttk.Combobox(card, textvariable=self.id_type_var, values=ID_TYPES,
                                 state="readonly", style="App.TCombobox"), 2, 0)
        self.id_number_entry = ttk.Entry(
            card, textvariable=self.id_number_var, style="App.TEntry", validate="key",
            validatecommand=(self.register(self._digits_validator(15)), "%P"))
        self._place(self.id_number_entry, 2, 1)

        self._add_label(card, "Full Name (letters only)", 3, 0, columnspan=2)
        self._place(ttk.Entry(card, textvariable=self.full_name_var, style="App.TEntry",
                              validate="key",
                              validatecommand=(self.register(self._letters_validator), "%P")),
                    4, 0, columnspan=2)

    def _build_economic_card(self) -> None:
        card = self._create_card(1, "💰  Economic data", Theme.MINT)

        self._add_label(card, "Current Income ($)", 1, 0)
        self._add_label(card, "Affiliation Tariff ($)", 1, 1)
        self._place(ttk.Entry(card, textvariable=self.income_var, style="App.TEntry",
                              validate="key",
                              validatecommand=(self.register(self._digits_validator(12)), "%P")),
                    2, 0)
        self._place(ttk.Entry(card, textvariable=self.fee_var, style="Tariff.TEntry",
                              state="readonly"), 2, 1)

        self._add_label(card, "Employment Type", 3, 0, columnspan=2)
        radios = tk.Frame(card, bg=Theme.SURFACE)
        radios.grid(row=4, column=0, columnspan=2, sticky="w")
        for option in (EMPLOYEE, INDEPENDENT):
            ttk.Radiobutton(radios, text=option, value=option, variable=self.employment_var,
                            style="App.TRadiobutton").pack(side="left", padx=(0, 18))

        self._add_label(card, "Desired Service", 5, 0, columnspan=2)
        self._place(ttk.Combobox(card, textvariable=self.service_var,
                                 values=tuple(SERVICES), state="readonly",
                                 style="App.TCombobox"), 6, 0, columnspan=2)

    def _build_affiliation_card(self) -> None:
        card = self._create_card(2, "📅  Affiliation & structure", Theme.PEACH)

        self._add_label(card, "Affiliation Date (dd/mm/yyyy)", 1, 0, columnspan=2)
        date_frame = tk.Frame(card, bg=Theme.SURFACE)
        date_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        date_frame.columnconfigure((0, 1, 2), weight=1, uniform="date")
        spinners = (
            ("Day", self.day_var, 1, 31, 2),
            ("Month", self.month_var, 1, 12, 2),
            ("Year", self.year_var, 2000, 2100, 4),
        )
        for column, (label, variable, low, high, size) in enumerate(spinners):
            padx = (0, 4) if column == 0 else (4, 0) if column == 2 else 4
            tk.Label(date_frame, text=label, bg=Theme.SURFACE, fg=Theme.MUTED,
                     font=Theme.FONT_SMALL).grid(row=0, column=column, sticky="w", padx=padx)
            ttk.Spinbox(
                date_frame, from_=low, to=high, textvariable=variable, width=5, wrap=True,
                style="App.TSpinbox", validate="key",
                validatecommand=(self.register(self._digits_validator(size)), "%P"),
            ).grid(row=1, column=column, sticky="ew", padx=padx)

        self._add_label(card, "Data Structure", 3, 0)
        self._add_label(card, "Report", 3, 1)
        structure_box = ttk.Combobox(card, textvariable=self.structure_var,
                                     values=STRUCTURE_NAMES, state="readonly",
                                     style="App.TCombobox")
        self._place(structure_box, 4, 0)
        structure_box.bind("<<ComboboxSelected>>", self._structure_selected)
        self._place(ttk.Entry(card, textvariable=self.report_var, style="Report.TEntry",
                              state="readonly"), 4, 1)

    # -- layout helpers ------------------------------------------------------------
    def _create_card(self, column: int, title: str, palette: tuple) -> tk.Frame:
        card = tk.Frame(self, bg=Theme.SURFACE, highlightbackground=Theme.BORDER,
                        highlightthickness=1, padx=16, pady=12)
        card.grid(row=0, column=column, sticky="nsew",
                  padx=(0 if column == 0 else 7, 0 if column == 2 else 7))
        card.columnconfigure((0, 1), weight=1, uniform=f"card{column}")
        tk.Label(card, text=f"  {title}  ", bg=palette[0], fg=palette[1],
                 font=Theme.FONT_CHIP, pady=3).grid(row=0, column=0, columnspan=2,
                                                     sticky="w", pady=(0, 4))
        return card

    @staticmethod
    def _add_label(card: tk.Frame, text: str, row: int, column: int,
                   columnspan: int = 1) -> None:
        tk.Label(card, text=text, bg=Theme.SURFACE, fg=Theme.MUTED, font=Theme.FONT_SMALL,
                 anchor="w").grid(row=row, column=column, columnspan=columnspan,
                                  sticky="w", pady=(6, 2))

    @staticmethod
    def _place(widget: tk.Widget, row: int, column: int, columnspan: int = 1) -> None:
        padx = 0 if columnspan == 2 else (0, 5) if column == 0 else (5, 0)
        widget.grid(row=row, column=column, columnspan=columnspan, sticky="ew", padx=padx)

    # -- validation and events -----------------------------------------------------------
    @staticmethod
    def _digits_validator(max_length: int):
        """Validation callback that only accepts digits (up to max_length)."""
        def validator(proposed: str) -> bool:
            return proposed == "" or (proposed.isascii() and proposed.isdigit()
                                      and len(proposed) <= max_length)
        return validator

    @staticmethod
    def _letters_validator(proposed: str) -> bool:
        return len(proposed) <= 60 and all(c.isalpha() or c == " " for c in proposed)

    def _update_fee(self, *_args) -> None:
        """Recalculate the read-only tariff whenever one of its inputs changes."""
        income_text = self.income_var.get()
        service = self.service_var.get()
        if not income_text or service not in SERVICES:
            self.fee_var.set("")
            return
        fee = FeeCalculator.calculate(int(income_text), self.employment_var.get(), service)
        self.fee_var.set(format_currency(fee))

    def _structure_selected(self, _event=None) -> None:
        self.report_var.set("")
        self._on_structure_change()
