#  Fase3_data-structure

Desktop application written in **Python** that manages the affiliates of a family compensation fund (*Compensándote*) using **linear data structures**: **stack**, **queue** and **list**.

> Homework 3 (Phase 3 – Practical Component: Simulated Practices) of the **Data Structures** course (301305A_2204), Systems Engineering – **UNAD**.

---

##  Table of contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Project structure](#-project-structure)
- [Data structures used](#-data-structures-used)
- [Business rules](#-business-rules)
- [Requirements](#-requirements)
- [How to run](#-how-to-run)
- [How to use](#-how-to-use)
- [Author](#-author)

---

##  Features

- **Login screen** with a masked password field (`*`), an *About* dialog and an *Exit* button.
- **Affiliate registration form** with:
  - ID type (`CC`, `CE`, `NUIP`, `PAS`), ID number (digits only) and full name (letters only).
  - Current income (digits only), employment type (*Employee* / *Independent*) and desired service.
  - Affiliation date (`dd/mm/yyyy`) selected with spin boxes.
  - **Read-only affiliation tariff**, calculated automatically.
- **Single table (Treeview)** that shows the records of the selected structure.
- **Register**, **Delete** (with confirmation), **Report**, **Clear** and **Exit** actions.
- Modern, light **pastel** interface.
- Data is stored **only in main memory** (no databases, no files).

## Technologies

| Technology | Use |
|---|---|
| Python 3.8+ | Main language |
| `tkinter` / `ttk` | Graphical user interface (GUI) |
| `collections.deque` | Queue implementation |
| `dataclasses` | Affiliate model |

No external packages are required.

##  Project structure

```
Fase3HernandoRobles/
├── main.py                          # Entry point
├── constants.py                     # Constants and fee tables
├── models/
│   └── affiliate_data_structure.py  # AffiliateDataStructure (model)
├── services/
│   ├── fee_calculator.py            # FeeCalculator (business rules)
│   └── affiliate_repository.py      # AffiliateRepository (stack, queue, list)
├── utils/
│   └── formatters.py                # Currency and date formatting
└── ui/
    ├── theme.py                     # Theme (colors, fonts, styles)
    ├── helpers.py                   # Window helpers and About dialog
    ├── pastel_button.py             # PastelButton
    ├── action_bar.py                # ActionBar
    ├── affiliate_form.py            # AffiliateForm
    ├── affiliate_table.py           # AffiliateTable
    ├── login_window.py              # LoginWindow
    └── main_window.py               # MainWindow
```

The business logic (`models` and `services`) is independent from the GUI (`ui`), and every class lives in its own file.

##  Data structures used

| Structure | Python implementation | Register | Delete | Report |
|---|---|---|---|---|
| **Stack** | `list` | Push (add on top) | Pop (remove the top) | Sum of the affiliation tariffs |
| **Queue** | `collections.deque` | Enqueue (add at the end) | Dequeue (remove the front) | Number of records |
| **List** | `list` | Append at the end | Remove by ID number | Average of the current income |

In the table, the **stack** shows its top first, while the **queue** and the **list** show their records in insertion order.

##  Business rules

### Base affiliation tariff

| Income | Employee | Independent |
|---|---|---|
| Up to $2.000.000 | $45.000 | $10.000 |
| $2.000.001 – $3.000.000 | $60.000 | $20.000 |
| $3.000.001 – $4.000.000 | $75.000 | $30.000 |
| $4.000.001 – $5.000.000 | $90.000 | $40.000 |
| More than $5.000.000 | $150.000 | $80.000 |

### Service surcharge

| Service | Effect on the tariff |
|---|---|
| Unemployment Subsidy | No change |
| Park Entry | + $2.500 |
| Training Course | + $7.500 |
| Travel Package | + $10.000 |
| Preventive Medicine | + 10% of the current income |

## Requirements

- **Python 3.8 or higher**
- **tkinter** (included in the official Python installer for Windows and macOS)

On Debian/Ubuntu, install it with:

```bash
sudo apt install python3-tk
```

##  How to run

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-user>/Fase3_data-structure.git
   cd Fase3_data-structure
   ```

2. Run the application:

   ```bash
   python main.py
   ```

3. Log in with the password: **`Caja`**

> The project can also be opened and run from **Visual Studio Code**.

## 🕹How to use

1. **Log in** with the password `Caja`.
2. Choose the **data structure** (Stack, Queue or List) in the *Affiliation & structure* card.
3. Fill in the affiliate data. The **tariff** is calculated automatically.
4. Press **Register** to add the affiliate to the selected structure.
5. Press **Report** to see the report of the selected structure.
6. Press **Delete** to remove a record:
   - *Stack*: removes the top record.
   - *Queue*: removes the front record.
   - *List*: asks for the ID number of the affiliate to remove.
7. Press **Clear** to empty the form (the stored records are not affected) or **Exit** to close the application.

##  Author

**Estefano Leomar Chacin Lazaro**
Systems Engineering – Universidad Nacional Abierta y a Distancia (UNAD)
Course: Data Structures – 301305A_2204
