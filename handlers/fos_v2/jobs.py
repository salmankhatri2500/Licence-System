"""
jobs.py  –  FOS v2
Scheduled background jobs:
  - Agent balance reminder (every 2.5 hours)
  - Client balance reminder (every 2.5 hours)
  - Daily summary to admin (9 AM IST)
"""
import logging
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)
IST = ZoneInfo("Asia/Kolkata")


async def agent_balance_reminder(bot):
    try:
        from db import all_agents, get_agent_balance, get_admin_rate, agent_active, reminders_enabled
        if not reminders_enabled(): return
        rate      = get_admin_rate()
        if rate <= 0: return
        threshold = rate * 5
        for ag in all_agents():
            if not agent_active(ag): continue
            bal  = get_agent_balance(ag["agent_id"])
            at   = int(ag.get("telegram_id",0))
            if not at: continue
            if bal < threshold:
                apps_left = int(bal // rate)
                try:
                    await bot.send_message(
                        at,
                        f"⚠️ *Balance Low Reminder!*\n\n"
                        f"💰 Balance: Rs{bal}\n"
                        f"📋 ~{apps_left} apps remaining\n\n"
                        f"💳 Pay Admin se recharge karo.",
                        parse_mode="Markdown")
                except: pass
    except Exception as e:
        logger.error(f"agent_balance_reminder: {e}")


async def client_balance_reminder(bot):
    try:
        from db import all_agents, all_clients, get_balance, agent_active, reminders_enabled
        from utils import safe_float
        if not reminders_enabled(): return
        for ag in all_agents():
            if not agent_active(ag): continue
            rate      = safe_float(ag.get("rate_per_app",0))
            if rate <= 0: continue
            threshold = rate * 5
            for c in all_clients(ag):
                if c.get("status") == "blocked": continue
                bal = get_balance(ag, c["client_code"])
                ct  = int(c.get("telegram_id",0))
                if not ct: continue
                if bal < threshold:
                    apps_left = int(bal // rate)
                    try:
                        await bot.send_message(
                            ct,
                            f"⚠️ *Balance Low!*\n\n"
                            f"💰 Balance: Rs{bal}\n"
                            f"📋 ~{apps_left} apps possible\n\n"
                            f"💳 Pay Agent se recharge karo.",
                            parse_mode="Markdown")
                    except: pass
    except Exception as e:
        logger.error(f"client_balance_reminder: {e}")


async def daily_admin_summary(bot):
    """Send daily summary to admin at 9 AM IST."""
    try:
        from config import SUPER_ADMIN_ID
        from db import queue_today_count, all_agents, agent_active, get_admin_rate
        from utils import today_ist, progress_bar
        q    = queue_today_count()
        ags  = all_agents()
        rate = get_admin_rate()
        bar  = progress_bar(q["done"], q["total"]) if q["total"] else "▱"*10
        earned = q["done"] * rate

        await bot.send_message(
            SUPER_ADMIN_ID,
            f"🌅 *Daily Summary – {today_ist()}*\n"
            f"━━━━━━━━━━━━━━\n"
            f"{bar}\n"
            f"📥 {q['total']}  ✅ {q['done']}  ⏳ {q['pending']}  🔒 {q['held']}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👔 Active Agents: {sum(1 for a in ags if agent_active(a))}\n"
            f"💰 Earned today: Rs{earned}",
            parse_mode="Markdown")
    except Exception as e:
        logger.error(f"daily_admin_summary: {e}")


def register_jobs(app):
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        s = AsyncIOScheduler(timezone=IST)
        s.add_job(agent_balance_reminder,  "interval", minutes=150,
                  args=[app.bot], id="agent_bal",   replace_existing=True)
        s.add_job(client_balance_reminder, "interval", minutes=150,
                  args=[app.bot], id="client_bal",  replace_existing=True)
        s.add_job(daily_admin_summary,     "cron",     hour=9, minute=0,
                  args=[app.bot], id="daily_summary", replace_existing=True)
        s.start()
        logger.info("✅ Jobs started: balance reminders + daily summary")
    except Exception as e:
        logger.warning(f"Jobs error (non-fatal): {e}")
