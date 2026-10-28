"""Text formatting helpers."""

from datetime import date


def format_currency(value: float) -> str:
    """Format a number using Colombian separators: 1.234.567,50"""
    text = f"{value:,.2f}"
    text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    if text.endswith(",00"):
        text = text[:-3]
    return text


def today_text() -> str:
    """Today's date as 'June 05, 2026'."""
    return date.today().strftime("%B %d, %Y")
