"""
utils.py  –  FOS v2
All helper functions, ID generators, validators.
"""
import random, string
from datetime import datetime, date
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

# ── In-memory user session store ─────────────────────────────
_ud: dict = {}

def user_data(tid: int) -> dict:
    if tid not in _ud:
        _ud[tid] = {}
    return _ud[tid]

def clear_user_data(tid: int):
    _ud[tid] = {}

# ── Time helpers ─────────────────────────────────────────────
def now_ist() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

def today_ist() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d")

def month_ist() -> str:
    return datetime.now(IST).strftime("%Y-%m")

def ts_to_display(ts: str) -> str:
    """'2025-03-16 08:45:00' → '16 Mar 08:45'"""
    try:
        dt = datetime.strptime(ts[:16], "%Y-%m-%d %H:%M")
        return dt.strftime("%d %b %H:%M")
    except:
        return ts[:16] if ts else ""

# ── ID generators ─────────────────────────────────────────────
def gen_agent_id() -> str:
    return f"AGT-{random.randint(1000, 9999)}"

def gen_client_code(agent_id: str) -> str:
    tag  = agent_id.replace("AGT-", "").replace("-", "")
    rand = "".join(random.choices(string.digits, k=3))
    return f"FOS-{tag}-{rand}"

def gen_app_id() -> str:
    return "APP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def gen_pay_id() -> str:
    return "PAY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def gen_op_id() -> str:
    return "OP-" + "".join(random.choices(string.digits, k=4))

# ── Validators ────────────────────────────────────────────────
def valid_phone(p: str) -> bool:
    return p.isdigit() and len(p) >= 10

def valid_dob(d: str) -> bool:
    """Validate DOB and check 18+ age."""
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(d, fmt).date()
            # 18+ check
            today  = date.today()
            age    = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
            return age >= 18
        except:
            pass
    return False

def valid_dob_format(d: str) -> bool:
    """Only check format, not age."""
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            datetime.strptime(d, fmt)
            return True
        except:
            pass
    return False

def is_adult(d: str) -> bool:
    """Check if DOB is 18+."""
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            dt    = datetime.strptime(d, fmt).date()
            today = date.today()
            age   = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
            return age >= 18
        except:
            pass
    return False

# ── Math helpers ──────────────────────────────────────────────
def safe_float(v) -> float:
    try:
        return float(str(v).replace(",", "").strip())
    except:
        return 0.0

def safe_int(v) -> int:
    try:
        return int(float(str(v).strip()))
    except:
        return 0

# ── Display helpers ───────────────────────────────────────────
def div() -> str:
    return "━━━━━━━━━━━━━━"

def progress_bar(done: int, total: int, width: int = 10) -> str:
    if total == 0: return "▱" * width
    filled = int((done / total) * width)
    return "▰" * filled + "▱" * (width - filled)
