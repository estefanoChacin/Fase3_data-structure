"""Main window: affiliate registration with Stack / Queue / List."""

import tkinter as tk
from tkinter import messagebox, simpledialog

from constants import (COURSE_CODE, COURSE_NAME, LIST, MAIN_TITLE, QUEUE, STACK,
                       STUDENT_NAME)
from services.affiliate_repository import AffiliateRepository
from ui.action_bar import ActionBar
from ui.affiliate_form import AffiliateForm
from ui.affiliate_table import AffiliateTable
from ui.helpers import center_window
from ui.theme import Theme


class MainWindow(tk.Tk):
    """Coordinates the form, the table and the repository."""

    def __init__(self) -> None:
        super().__init__()
        self.repository = AffiliateRepository()
        self.status_var = tk.StringVar()

        self.title(MAIN_TITLE)
        self.configure(bg=Theme.BG)
        Theme.apply(self)
        center_window(self, 1280, 760)
        self.minsize(1150, 700)

        self._build_ui()
        self._refresh_table()
        self._set_status("Ready — fill in the form and click Register.")
        self.form.focus_first()

    # -- layout ----------------------------------------------------------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self._build_header()

        self.form = AffiliateForm(self, on_structure_change=self._on_structure_change)
        self.form.grid(row=1, column=0, sticky="ew", padx=16, pady=(14, 10))

        self.table = AffiliateTable(self)
        self.table.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 10))

        ActionBar(
            self,
            on_register=self._register_affiliate,
            on_delete=self._delete_affiliate,
            on_report=self._show_report,
            on_clear=self._clear_form,
            on_exit=self.destroy,
        ).grid(row=3, column=0, sticky="ew", padx=11, pady=(0, 10))

        tk.Label(self, textvariable=self.status_var, bg=Theme.HEADER, fg=Theme.PURPLE,
                 font=Theme.FONT_MONO, anchor="w", padx=14, pady=5
                 ).grid(row=4, column=0, sticky="ew")

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=Theme.HEADER)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="🌼  Compensándote · Affiliation Control", bg=Theme.HEADER,
                 fg=Theme.PURPLE, font=Theme.FONT_HEADER).pack(side="left", padx=18, pady=12)
        tk.Label(header, text=f"🎓 {STUDENT_NAME}  ·  {COURSE_NAME} {COURSE_CODE}",
                 bg=Theme.SURFACE, fg=Theme.PURPLE, font=Theme.FONT_CHIP,
                 padx=12, pady=5).pack(side="right", padx=18)

    # -- helpers ---------------------------------------------------------------
    def _set_status(self, message: str) -> None:
        self.status_var.set(f"›  {message}")

    def _refresh_table(self) -> None:
        structure = self.form.structure
        self.table.refresh(structure, self.repository.records(structure))

    def _on_structure_change(self) -> None:
        self._refresh_table()
        self._set_status(f"Working with the {self.form.structure}.")

    # -- button actions ----------------------------------------------------------
    def _register_affiliate(self) -> None:
        affiliate = self.form.read_affiliate()
        if affiliate is None:
            return

        structure = self.form.structure
        if self.repository.find_by_id(structure, affiliate.id_number) is not None:
            messagebox.showwarning(
                "Duplicate affiliate",
                f"The ID number {affiliate.id_number} is already registered in the "
                f"{structure}.", parent=self)
            return

        self.repository.add(structure, affiliate)  # push / enqueue / append
        self._refresh_table()
        self.table.highlight_last_added(structure)
        self.form.clear()
        verb = {STACK: "pushed onto the stack", QUEUE: "enqueued",
                LIST: "added at the end of the list"}[structure]
        self._set_status(f"{affiliate.full_name} {verb}.")

    def _delete_affiliate(self) -> None:
        structure = self.form.structure
        if self.repository.count(structure) == 0:
            messagebox.showinfo("Nothing to delete", f"The {structure.lower()} is empty.",
                                parent=self)
            return

        if structure == LIST:
            self._delete_from_list()
            return

        candidate = self.repository.peek_next(structure)
        position = "top of the stack" if structure == STACK else "front of the queue"
        action = "pop" if structure == STACK else "dequeue"
        if not messagebox.askyesno(
                "Confirm deletion",
                f"The record at the {position} will be removed ({action}):\n\n"
                f"ID: {candidate.id_number}\nName: {candidate.full_name}\n\n"
                "Do you want to continue?", parent=self):
            return

        removed = self.repository.remove_next(structure)
        self._refresh_table()
        self.form.set_report("")
        self._set_status(f"{removed.full_name} removed from the {structure.lower()}.")

    def _delete_from_list(self) -> None:
        id_number = simpledialog.askstring(
            "Delete from List", "Enter the affiliate's ID number:", parent=self)
        if id_number is None:  # dialog cancelled
            return
        id_number = id_number.strip()
        if not id_number.isascii() or not id_number.isdigit():
            messagebox.showwarning("Invalid ID", "The ID number must contain digits only.",
                                   parent=self)
            return

        affiliate = self.repository.find_by_id(LIST, id_number)
        if affiliate is None:
            messagebox.showwarning(
                "Not found", f"No affiliate with ID number {id_number} exists in the list.",
                parent=self)
            return

        if not messagebox.askyesno(
                "Confirm deletion",
                f"Delete this affiliate from the list?\n\n"
                f"ID: {affiliate.id_number}\nName: {affiliate.full_name}", parent=self):
            return

        self.repository.remove_by_id(id_number)
        self._refresh_table()
        self.form.set_report("")
        self._set_status(f"{affiliate.full_name} removed from the list.")

    def _show_report(self) -> None:
        structure = self.form.structure
        self.form.set_report(self.repository.build_report(structure))
        self._set_status(f"Report generated for the {structure.lower()}.")

    def _clear_form(self) -> None:
        self.form.clear()
        self._set_status("Form cleared. Stored records were not modified.")
