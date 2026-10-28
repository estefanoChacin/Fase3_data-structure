"""Model that stores the data of one affiliate."""

from dataclasses import dataclass
from datetime import date
from utils.formatters import format_currency


@dataclass
class AffiliateDataStructure:
    """Data collected from a user when affiliating to the service center."""

    id_type: str
    id_number: str
    full_name: str
    current_income: int
    desired_service: str
    employment_type: str
    affiliation_fee: float
    affiliation_date: date

    @property
    def formatted_date(self) -> str:
        return self.affiliation_date.strftime("%d/%m/%Y")

    def to_row(self) -> tuple:
        """Values in the same order as the table columns."""
        return (
            self.id_type,
            self.id_number,
            self.full_name,
            format_currency(self.current_income),
            self.desired_service,
            self.employment_type,
            format_currency(self.affiliation_fee),
            self.formatted_date,
        )
