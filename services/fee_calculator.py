"""Business rules used to compute the affiliation fee (Tables 2 and 3)."""

from constants import EMPLOYEE, INCOME_BRACKETS, SERVICES


class FeeCalculator:
    """Computes the affiliation fee from income, employment type and service."""

    @staticmethod
    def calculate(income: int, employment_type: str, service: str) -> float:
        base_fee = 0.0
        for upper_limit, employee_fee, independent_fee in INCOME_BRACKETS:
            if income <= upper_limit:
                base_fee = employee_fee if employment_type == EMPLOYEE else independent_fee
                break

        flat_surcharge, income_rate = SERVICES[service]
        return base_fee + flat_surcharge + income * income_rate
