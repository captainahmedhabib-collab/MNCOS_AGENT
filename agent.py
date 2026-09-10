import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("MNCOS-Agent-Webhook")

# Sovereign Token for MNCOS-AGENT
TOKEN = "8814574628:AAFAz9_RCOo8jMzL4wAtBY4kJfEAlTd_Dgc"

# Official Digital Signature & Watermark
SIGNATURE = "Verified by Captain Ahmed Habib | MNCOS Sovereign Infrastructure"

# Initialize Flask app for Webhook handling
app = Flask(__name__)

# Initialize Telegram Application globally
telegram_app = None

async def setup_telegram_bot():
    """
    Initializes the telegram application and registers handlers.
    """
    global telegram_app
    if telegram_app is None:
        telegram_app = Application.builder().token(TOKEN).build()
        
        # Register handlers
        telegram_app.add_handler(CommandHandler("start", start_command))
        telegram_app.add_handler(CallbackQueryHandler(button_handler, pattern="^path_"))
        telegram_app.add_handler(CallbackQueryHandler(back_handler, pattern="^back_to_start$"))
        
        await telegram_app.initialize()
    return telegram_app

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Presents the core sovereign high-ticket executive interface.
    """
    welcome_message = (
        f"Welcome, Executive Partner 🫡\n\n"
        f"You have accessed the **MNCOS Multi-Agent Sovereign Ecosystem**.\n"
        f"Operating under Civilizational Coherence Core™ standards.\n\n"
        f"Select a strategic institutional pathway below to initiate deployment:"
    )
    
    # High-Ticket B2B Service Pathways
    keyboard = [
        [InlineKeyboardButton("📋 [01] Scope, Timeline & Commercials ($25k+)", callback_data="path_scope")],
        [InlineKeyboardButton("🔒 [02] Confidential NDA & Sovereign Protocol", callback_data="path_nda")],
        [InlineKeyboardButton("⚓ [03] Fleet & Asset Audit Scope ($50k)", callback_data="path_audit")],
        [InlineKeyboardButton("⚡ [04] Offline Emergency Node License ($100k)", callback_data="path_offline")],
        [InlineKeyboardButton("📈 [05] Strategic Investment & Scaling ($1M+)", callback_data="path_investment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles high-ticket executive conversions and strategic pitch responses.
    """
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "path_scope":
        response_text = (
            "🎯 **[Service 01] Commercial Scope & Compliance Framework**\n\n"
            "• **Target:** Enterprise Maritime Operators & Port Authorities.\n"
            "• **Deliverable:** Comprehensive project blueprints, deterministic execution timelines, and regulatory compliance frameworks.\n"
            "• **Value Tier:** Starting at $25,000 per institutional deployment.\n\n"
            f"*{SIGNATURE}*"
        )
    elif data == "path_nda":
        response_text = (
            "🔒 **[Service 02] Confidential NDA & Sovereign Protocol**\n\n"
            "• **Target:** Strategic Partners & Institutional Investors.\n"
            "• **Deliverable:** Cryptographic secure session initialization and binding non-disclosure frameworks for proprietary Black-Box architecture.\n"
            "• **Status:** Ready for immediate digital execution.\n\n"
            f"*{SIGNATURE}*"
        )
    elif data == "path_audit":
        response_text = (
            "⚓ **[Service 03] Fleet & Asset Audit Scope**\n\n"
            "• **Target:** Global Fleet Managers & Shipping Lines.\n"
            "• **Deliverable:** Full telemetry analysis, structural efficiency audit, and Zero-Vulnerability infrastructure hardening.\n"
            "• **Value Tier:** $50,000 per fleet audit package.\n\n"
            f"*{SIGNATURE}*"
        )
    elif data == "path_offline":
        response_text = (
            "⚡ **[Service 04] Offline Emergency Node License**\n\n"
            "• **Target:** Critical Marine Infrastructures Requiring Total Isolation.\n"
            "• **Deliverable:** Sovereign autonomous offline node license, eliminating cyber-vulnerabilities and ensuring 24/7 mission-critical redundancy.\n"
            "• **Value Tier:** $100,000 B2B Enterprise License.\n\n"
            f"*{SIGNATURE}*"
        )
    elif data == "path_investment":
        response_text = (
            "📈 **[Service 05] Strategic Investment & Scaling**\n\n"
            "• **Target:** High-Net-Worth Investors & Blue Economy Venture Funds.\n"
            "• **Deliverable:** Executive equity placement documentation, financial valuation models, and direct participation in the $1M+ scaling roadmap.\n"
            "• **Status:** Limited institutional slots available.\n\n"
            f"*{SIGNATURE}*"
        )
    else:
        response_text = f"Directive processed successfully.\n\n*{SIGNATURE}*"

    keyboard = [[InlineKeyboardButton("🔙 Return to Main Menu", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=response_text, reply_markup=reply_markup, parse_mode="Markdown")

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_command(update, context)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """
    Endpoint that receives incoming updates from Telegram via Webhook.
    """
    import asyncio
    json_data = request.get_json(force=True)
    
    async def process():
        bot_app = await setup_telegram_bot()
        update = Update.de_json(json_data, bot_app.bot)
        await bot_app.process_update(update)
        
    asyncio.run(process())
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "MNCOS-AGENT Sovereign Webhook Server is Online.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

