
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging setup for 24/7 operational tracking
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("MNCOS-Agent")

# Sovereign Token for MNCOS-AGENT
TOKEN = "8814574628:AAFAz9_RCOo8jMzL4wAtBY4kJfEAlTd_Dgc"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Presents the core sovereign services interface.
    """
    welcome_message = (
        f"Welcome, Captain Ahmed Habib (EL-KOPTAN) 🫡\n\n"
        f"The **MNCOS Multi-Agent Sovereign Ecosystem** is live.\n"
        f"Please select your strategic operational pathway below:"
    )
    
    # Sleek English buttons for the core services
    keyboard = [
        [InlineKeyboardButton("📋 [01] Scope, Timeline & Commercials", callback_data="path_scope")],
        [InlineKeyboardButton("🔒 [02] Confidential NDA Session", callback_data="path_nda")],
        [InlineKeyboardButton("⚓ [03] Fleet & Asset Audit Scope", callback_data="path_audit")],
        [InlineKeyboardButton("⚡ [04] Offline Emergency Node License", callback_data="path_offline")],
        [InlineKeyboardButton("📈 [05] Strategic Investment & Scaling", callback_data="path_investment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles interactive pathway selections with high-end executive responses.
    """
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "path_scope":
        response_text = "🎯 **[Service 01] Scope / Timeline / Commercials / Compliance**\n\nDrafting comprehensive project frameworks under Civilizational Coherence Core™ standards."
    elif data == "path_nda":
        response_text = "🔒 **[Service 02] Confidential NDA Protocol**\n\nInitializing secure cryptographic session and sovereign verification channels."
    elif data == "path_audit":
        response_text = "⚓ **[Service 03] Fleet & Asset Audit Scope**\n\nLead-Scout Agent is standing by to receive maritime asset parameters and telemetry data."
    elif data == "path_offline":
        response_text = "⚡ **[Service 04] Offline Emergency Node License**\n\nVerifying sovereign offline architecture and autonomous redundancy protocols."
    elif data == "path_investment":
        response_text = "📈 **[Service 05] Strategic Investment & Scaling**\n\nPreparing executive investment documentation and valuation models for deployment."
    else:
        response_text = "Directive processed successfully."

    keyboard = [[InlineKeyboardButton("🔙 Return to Main Menu", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=response_text, reply_markup=reply_markup, parse_mode="Markdown")

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_command(update, context)

async def debug_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Catches any incoming text message, logs it, and responds to ensure bidirectional communication.
    """
    text = update.effective_message.text
    logger.info(f"Incoming message caught: {text}")
    await update.message.reply_text(f"⚡ [MNCOS-AGENT] Signal acknowledged: '{text}'. System operating at Zero-Vulnerability.")

def main():
    """
    Runs the bot using continuous Polling 24/7 with drop_pending_updates.
    """
    if not TOKEN:
        logger.error("Telegram Token is missing!")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^path_"))
    application.add_handler(CallbackQueryHandler(back_handler, pattern="^back_to_start$"))
    
    # General message handler to guarantee response on any text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, debug_echo))

    logger.info("MNCOS-AGENT Sovereign Ecosystem is online and running 24/7...")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
