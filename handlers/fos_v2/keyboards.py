"""
keyboards.py  –  FOS v2
All reply keyboards and inline keyboard helpers.
"""
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

REMOVE = ReplyKeyboardRemove()

# ── Reply Keyboards ───────────────────────────────────────────

def kb_admin():
    return ReplyKeyboardMarkup([
        ["📊 Dashboard",    "👔 All Agents"],
        ["➕ Add Agent",     "🔍 Find Agent"],
        ["📋 Queue",         "✅ Done Apps"],
        ["💳 Agent Payments","⚙️ Settings"],
        ["📢 Broadcast All", "📊 Monthly Report"],
        ["👥 Operators",     "🔧 Debug"],
    ], resize_keyboard=True)

def kb_agent():
    return ReplyKeyboardMarkup([
        ["📋 My Queue",      "📅 Today Summary"],
        ["👥 My Clients",    "📊 My Stats"],
        ["💰 My Balance",    "💳 Pay Admin"],
        ["🔗 Referral Link", "⚙️ Settings"],
        ["📢 Broadcast",     "📋 Work History"],
        ["🔄 Refresh"],
    ], resize_keyboard=True)

def kb_client():
    return ReplyKeyboardMarkup([
        ["📱 New Application"],
        ["📋 My Apps",        "💰 My Balance"],
        ["💳 Pay Agent",      "📞 Contact Agent"],
        ["👤 My Profile"],
    ], resize_keyboard=True)

def kb_operator():
    """Operator sees a limited queue-processing panel."""
    return ReplyKeyboardMarkup([
        ["📋 My Queue",     "✅ Done Apps"],
        ["📊 Today Stats"],
    ], resize_keyboard=True)

# ── Inline Keyboards ──────────────────────────────────────────

def ik_queue_item(queue_id, client_code, agent_id, agent_tid, client_tid):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "✅ MARK DONE",
            callback_data=f"QDONE|{queue_id}|{client_code}|{agent_id}|{agent_tid}|{client_tid}")
    ]])

def ik_agent_actions(agent_id: str, is_active: bool):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗑 Remove",      callback_data=f"REMOVE_AGENT|{agent_id}"),
            InlineKeyboardButton("💰 Add Balance", callback_data=f"AGENT_BAL|{agent_id}"),
        ],
        [
            InlineKeyboardButton(
                "🚫 Block" if is_active else "✅ Unblock",
                callback_data=f"AGENT_BLOCK|{agent_id}"),
        ]
    ])

def ik_client_actions(client_code: str, agent_id: str):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🚫 Block",   callback_data=f"C_BLOCK|{client_code}|{agent_id}"),
        InlineKeyboardButton("✅ Unblock", callback_data=f"C_UNBLK|{client_code}|{agent_id}"),
    ]])

def ik_payment_review(pay_id: str, client_code: str, agent_id: str, client_tid: int):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Approve",
            callback_data=f"PAY_APP|{pay_id}|{client_code}|{agent_id}|{client_tid}"),
        InlineKeyboardButton("❌ Reject",
            callback_data=f"PAY_REJ|{pay_id}|{client_code}|{agent_id}|{client_tid}"),
    ]])

def ik_agent_payment_review(pay_id: str, agent_id: str):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Approve", callback_data=f"AGPAY_APP|{pay_id}|{agent_id}"),
        InlineKeyboardButton("❌ Reject",  callback_data=f"AGPAY_REJ|{pay_id}|{agent_id}"),
    ]])

def ik_admin_settings():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Upload/Update QR",   callback_data="ADMIN_SET_QR")],
        [InlineKeyboardButton("💰 Update App Rate",    callback_data="ADMIN_SET_RATE")],
        [InlineKeyboardButton("👥 Manage Operators",   callback_data="MANAGE_OPS")],
        [InlineKeyboardButton("🔔 Toggle Reminders",   callback_data="TOGGLE_REMINDERS")],
    ])

def ik_agent_settings(agent_id: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Update Rate", callback_data=f"SET_RATE|{agent_id}")],
        [InlineKeyboardButton("🖼 Upload QR",   callback_data=f"SET_QR|{agent_id}")],
    ])

def ik_broadcast_type(prefix: str = "BC"):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📝 Text",  callback_data=f"{prefix}_TEXT"),
        InlineKeyboardButton("🖼 Image", callback_data=f"{prefix}_IMAGE"),
        InlineKeyboardButton("🔊 Voice", callback_data=f"{prefix}_VOICE"),
    ]])

def ik_operator_remove(op_id: str):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🗑 Remove Operator", callback_data=f"REMOVE_OP|{op_id}")
    ]])
