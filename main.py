"""
Fase3EstefanoChacin
===================
Compensándote - Family Compensation Fund: Affiliation Control.

Course  : Data Structures (301305A_2204) - UNAD / ECBTI / Systems Engineering
Student : Estefano Leomar Chacin Lazaro

Run with:  python main.py   (Python 3.8+, standard library only)
"""

from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main() -> None:
    login = LoginWindow()
    login.mainloop()
    if login.authenticated:
        MainWindow().mainloop()


if __name__ == "__main__":
    main()
