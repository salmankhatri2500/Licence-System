"""
config.py  –  FOS v2  (Faiz Online Service)
All conversation states, constants, env-loading.
"""
import os, json

# ── Env ───────────────────────────────────────────────────────
BOT_TOKEN      = os.environ.get("BOT_TOKEN", "")
SUPER_ADMIN_ID = int(os.environ.get("SUPER_ADMIN_ID", "0"))
MASTER_SHEET   = "FOS_Master"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_raw = os.environ.get("GOOGLE_CREDS_JSON", "")
try:
    GOOGLE_CREDS = json.loads(_raw) if _raw else {}
except Exception as e:
    print(f"GOOGLE_CREDS_JSON error: {e}")
    GOOGLE_CREDS = {}

# ── Conversation states ───────────────────────────────────────
# Registration
(REG_NAME, REG_PHONE) = (1, 2)

# Add Agent
(AA_NAME, AA_PHONE, AA_TID, AA_RATE, AA_SHEET) = range(10, 15)

# New Application
(APP_NO, APP_DOB, APP_PASS) = range(20, 23)

# Client Pay Agent
PAY_AMOUNT = 30

# Agent Pay Admin
AGENT_PAY_AMOUNT = 35

# Agent Broadcast
(BC_TYPE, BC_MSG) = range(40, 42)

# Admin Broadcast
(ABC_TYPE, ABC_MSG) = range(50, 52)

# Update Rate
UR_RATE = 60

# Add Operator
ADD_OP_PHONE = 70

# Operator confirm queue done
OP_DONE = 80

# ── Limits & thresholds ───────────────────────────────────────
LOW_BAL_APPS_THRESHOLD = 5   # warn when < 5 apps worth of balance
MAX_QUEUE_SHOW         = 30  # max queue items shown at once
DAILY_HIGH_VOLUME      = 1000  # expected daily volume
