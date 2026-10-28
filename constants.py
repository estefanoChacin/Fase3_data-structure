"""Application-wide constants and business-rule tables."""

# ----------------------------------------------------------------------------
# Student / course information
# ----------------------------------------------------------------------------
APP_NAME = "Fase3EstefanoCHacin"
STUDENT_NAME = "Estefano Leomar Chacin Lazaro"
COURSE_NAME = "Data Structures"
COURSE_CODE = "301305A_2204"
COLLABORATIVE_GROUP = "301305A_2204"
PROGRAM_NAME = "UNAD · ECBTI · Systems Engineering"

# ----------------------------------------------------------------------------
# Authentication and window titles
# ----------------------------------------------------------------------------
LOGIN_PASSWORD = "Caja"
LOGIN_TITLE = "Login - Compensándote"
MAIN_TITLE = "Caja Compensándote – Control de Afiliados"

# ----------------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------------
STACK = "Stack"
QUEUE = "Queue"
LIST = "List"
STRUCTURE_NAMES = (STACK, QUEUE, LIST)

STRUCTURE_HINTS = {
    STACK: "LIFO · the first row is the TOP of the stack",
    QUEUE: "FIFO · the first row is the FRONT of the queue",
    LIST: "Insertion order · new records are added at the end",
}

# ----------------------------------------------------------------------------
# Form options
# ----------------------------------------------------------------------------
ID_TYPES = ("CC", "CE", "NUIP", "PAS")

EMPLOYEE = "Employee"
INDEPENDENT = "Independent"

# Service -> (flat surcharge, percentage of current income)
SERVICES = {
    "Unemployment Subsidy": (0, 0.0),
    "Park Entry": (2_500, 0.0),
    "Training Course": (7_500, 0.0),
    "Travel Package": (10_000, 0.0),
    "Preventive Medicine": (0, 0.10),
}

# (upper income limit, employee fee, independent fee)
# Each bracket includes its upper limit; incomes above $5.000.000 use the last row.
INCOME_BRACKETS = (
    (2_000_000, 45_000, 10_000),
    (3_000_000, 60_000, 20_000),
    (4_000_000, 75_000, 30_000),
    (5_000_000, 90_000, 40_000),
    (float("inf"), 150_000, 80_000),
)
