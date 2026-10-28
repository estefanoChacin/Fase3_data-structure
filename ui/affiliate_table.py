"""Treeview card that shows the records of the selected data structure."""

import tkinter as tk
from tkinter import ttk
from typing import List

from constants import STACK, STRUCTURE_HINTS
from models.affiliate_data_structure import AffiliateDataStructure
from ui.theme import Theme


class AffiliateTable(tk.Frame):
    """Displays the affiliates stored in a stack, a queue or a list."""

    COLUMNS = (
        ("id_type", "ID Type", 75, "center"),
        ("id_number", "ID Number", 120, "center"),
        ("full_name", "Full Name", 240, "w"),
        ("income", "Income ($)", 120, "e"),
        ("service", "Service", 170, "w"),
        ("employment", "Employment", 110, "center"),
        ("fee", "Tariff ($)", 105, "e"),
        ("date", "Date", 100, "center"),
    )

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, bg=Theme.SURFACE, highlightbackground=Theme.BORDER,
                         highlightthickness=1, padx=14, pady=12)
        self.title_var = tk.StringVar()
        self.hint_var = tk.StringVar()
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = tk.Frame(self, bg=Theme.SURFACE)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        tk.Label(toolbar, textvariable=self.title_var, bg=Theme.SURFACE, fg=Theme.PURPLE,
                 font=(Theme.FAMILY, 12, "bold")).pack(side="left")
        tk.Label(toolbar, textvariable=self.hint_var, bg=Theme.LAVENDER[0],
                 fg=Theme.LAVENDER[1], font=Theme.FONT_CHIP, padx=10, pady=3
                 ).pack(side="right")

        self.tree = ttk.Treeview(self, columns=[c[0] for c in self.COLUMNS],
                                 show="headings", style="App.Treeview",
                                 selectmode="browse")
        for key, heading, width, anchor in self.COLUMNS:
            self.tree.heading(key, text=heading)
            self.tree.column(key, width=width, anchor=anchor, minwidth=60)
        self.tree.tag_configure("odd", background=Theme.ROW_ODD)
        self.tree.tag_configure("even", background=Theme.ROW_EVEN)
        self.tree.grid(row=1, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview,
                                 style="App.Vertical.TScrollbar")
        x_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview,
                                 style="App.Horizontal.TScrollbar")
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        y_scroll.grid(row=1, column=1, sticky="ns")
        x_scroll.grid(row=2, column=0, sticky="ew")

    def refresh(self, structure: str, records: List[AffiliateDataStructure]) -> None:
        """Redraw the table with the records of the given structure."""
        self.tree.delete(*self.tree.get_children())
        for index, affiliate in enumerate(records):
            self.tree.insert("", "end", values=affiliate.to_row(),
                             tags=("even" if index % 2 == 0 else "odd",))
        self.title_var.set(f"📋  {structure} · Registered Affiliates ({len(records)})")
        self.hint_var.set(STRUCTURE_HINTS[structure])

    def highlight_last_added(self, structure: str) -> None:
        """Select the record that was just added (top of the stack, end otherwise)."""
        children = self.tree.get_children()
        if not children:
            return
        target = children[0] if structure == STACK else children[-1]
        self.tree.selection_set(target)
        self.tree.see(target)
