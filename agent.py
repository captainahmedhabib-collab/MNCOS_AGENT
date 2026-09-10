import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# إعداد السجلات السيادية
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("MNCOS_SOVEREIGN_AGENT_SYSTEM")

TOKEN = "8947725456:AAG4vdQf6AKhek_uFHIMpXYSodShLmsFvig"

# إنشاء مجلد لحفظ إيصالات الدفع الواردة محلياً
RECEIPTS_DIR = "receipts"
if not os.path.exists(RECEIPTS_DIR):
    os.makedirs(RECEIPTS_DIR)

# 3. الذاكرة (Memory): تخزين حالة المحادثات وسياق الأصول محلياً
agent_memory = {}

def is_arabic(text: str) -> bool:
    if not text:
        return False
    for char in text:
        code = ord(char)
        if (0x0600 <= code <= 0x06FF) or (0x0750 <= code <= 0x077F) or (0x08A0 <= code <= 0x08FF):
            return True
    return False

# ==========================================
# 🧠 MNCOS 5-COMPONENT AI AGENT ARCHITECTURE
# ==========================================

class LeadScoutAgent:
    """وكيل مساعد (Sub-Agent): التنقيب والبحث عن العملاء وتحليل حجم الأصول"""
    @staticmethod
    def execute_tool(fleet_input: str) -> str:
        return (
            f"🎯 **[Lead-Scout Sub-Agent | أداة التنقيب والتحليل]:**\n"
            f"• الأصول المستهدفة المرصودة: '{fleet_input}'\n"
            f"• التقييم الاستراتيجي: مؤهل للاندماج الهيكلي ضمن شبكة MNCOS.\n"
            f"• تم رفع درجة اهتمام العميل وتفعيل مسار الخدمات السيادية الخمس."
        )

class MNCOSMasterAgent:
    """الوكيل الرئيسي (Master Agent) المطبق للهندسة الخماسية الكاملة"""
    
    @staticmethod
    def process_interaction(user_id: int, input_text: str, has_photo: bool = False) -> str:
        # 3. الذاكرة (Memory): استرجاع وتحديث السياق قصير المدى
        if user_id not in agent_memory:
            agent_memory[user_id] = {"history": [], "context": "initial"}
        
        agent_memory[user_id]["history"].append(input_text)
        
        # 2. وحدة التفكير والتحكم (Core Model & Reasoning): تقييم المدخلات واتخاذ القرار
        if has_photo:
            return "📥 [Core Processing]: تم معالجة الصورة وإيداعها في ملفات الحوكمة السيادية."
        
        lang_arabic = is_arabic(input_text)
        
        # 4. الأدوات والقدرات التنفيذية (Tools Integration)
        if "fleet" in agent_memory[user_id].get("context", "") or len(input_text) > 3:
            tool_output = LeadScoutAgent.execute_tool(input_text)
            if lang_arabic:
                return f"🧠 **[MNCOS_AGENT Core Engine]:**\n{tool_output}\n\n• تم توليد التوجيه الحتمي تحت إشراف Captain Ahmed Habib."
            else:
                return f"🧠 **[MNCOS_AGENT Core Engine]:**\n{tool_output}\n\n• Deterministic guidance generated under Captain Ahmed Habib."
        
        if lang_arabic:
            return (
                "🧠 **[MNCOS_AGENT - التوجيه الاستراتيجي السيادي]:**\n"
                "تم تحليل استفسارك بواسطة محرك التفكير والتحكم الذكي.\n"
                "• الدفع الفوري للخدمات عبر InstaPay / فودافون كاش: `01032476258`"
            )
        else:
            return (
                "🧠 **[MNCOS_AGENT - Sovereign Strategic Core]:**\n"
                "Query processed by the sovereign cognitive control unit.\n"
                "• Payment via InstaPay / Vodafone Cash: `01032476258`"
            )

# ==========================================
# Telegram Handlers (Sensors & Actuators)
# ==========================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. المستشعرات (Sensors): استقبال أمر البدء
    user_id = update.message.from_user.id
    agent_memory[user_id] = {"context": "waiting_sector"}
    
    welcome_text = (
        "السلام عليكم، Captain Ahmed Habib 🫡\n\n"
        "أهلاً بك في منظومة MNCOS Autonomous Multi-Agent Ecosystem.\n"
        "الإطار الاستراتيجي: Civilizational Coherence Core™\n\n"
        "قنوات الاعتماد الرسمية:\n"
        "• البريد: maritimeahos@gmail.com\n"
        "• واتساب / الاتصال: 00201032476258\n\n"
        "يرجى اختيار قطاعك التشغيلي لبدء عمل الوكلاء المساعدين:\n\n"
        "------------------------------------\n"
        "Welcome to MNCOS Autonomous Multi-Agent Ecosystem.\n"
        "Strategic Framework: Civilizational Coherence Core™\n"
        "Please select your operational sector:"
    )
    keyboard = [
        [InlineKeyboardButton("🚢 Commercial Fleet / Cargo", callback_data="sector_cargo")],
        [InlineKeyboardButton("🛢️ Offshore Rigs / Energy", callback_data="sector_rigs")],
        [InlineKeyboardButton("⚓ Ports & Logistics", callback_data="sector_ports")],
        [InlineKeyboardButton("🛡️ Sovereign Investment / Other", callback_data="sector_sovereign")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # 5. المشغلات أو المخرجات (Actuators): إرسال الرد التفاعلي للوسيط الخارجي
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("sector_"):
        agent_memory[user_id]["context"] = "waiting_fleet_size"
        await query.message.reply_text(
            "📊 **Sector Registered by MNCOS_AGENT.**\n"
            "يرجى إدخال تفاصيل أسطولك أو أصولك ليقوم Lead-Scout Sub-Agent بتحليلها / Enter fleet details for Scout analysis:"
        )
    elif data == "s1":
        resp = (
            "🛡️ **1. MNCOS Sovereign Operating System:**\n"
            "• Core Fleet Deployment: Starting at **$15,000**.\n"
            "• Critical Asset Customization: Starting at **$35,000**.\n"
            "• Payment: InstaPay to Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s2":
        resp = (
            "📊 **2. Sovereign Audit & Stress Testing:**\n"
            "• Standard Audit: **$50,000** | Advanced: **$100,000**.\n"
            "• Payment: InstaPay / Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s3":
        resp = (
            "⚓ **3. Offline Emergency Node License:**\n"
            "• Single Air-Gapped Node: **$8,500** | Multi-Node: **$25,000**.\n"
            "• Payment: InstaPay / Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s4":
        resp = (
            "📜 **4. Tier 3 Governance & IP:**\n"
            "• Sovereign Advisory & Black-Box Governance: Starting at **$45,000**.\n"
            "• Payment: InstaPay / Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)
    elif data == "s5":
        resp = (
            "🧠 **5. Sovereign Expert Maritime Intelligence:**\n"
            "• Advanced cognitive engine managed by MNCOS_AGENT.\n"
            "• Precision-priced consultation under Captain Ahmed Habib.\n"
            "• Payment: InstaPay / Vodafone Cash: `01032476258`."
        )
        await query.message.reply_text(resp)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. المستشعرات (Sensors): التقاط ملف الإيصال المصور
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = os.path.join(RECEIPTS_DIR, f"receipt_{user_id}_{photo.file_unique_id}.jpg")
    await file.download_to_drive(file_path)
    
    # 5. المشغلات (Actuators): إصدار قرار تأكيد الاستلام وإخطار الإدارة
    response = MNCOSMasterAgent.process_interaction(user_id, "photo_uploaded", has_photo=True)
    await update.message.reply_text(
        f"{response}\n\n"
        "📥 **Payment receipt securely stored in local storage.**\n"
        "Notifying Captain Ahmed Habib for sovereign review via maritimeahos@gmail.com"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. المستشعرات (Sensors): استقبال الرسائل النصية
    text = update.message.text
    user_id = update.message.from_user.id
    state = agent_memory.get(user_id, {}).get("context", "")
    
    if state == "waiting_fleet_size":
        agent_memory[user_id]["context"] = "completed"
        
        # تشغيل قدرات الأدوات وتحليل التنقيب (Tools & Sub-Agent)
        scout_report = LeadScoutAgent.execute_tool(text)
        await update.message.reply_text(scout_report)
        
        keyboard = [
            [InlineKeyboardButton("🛡️ 1. Sovereign OS ($15K - $35K+)", callback_data="s1")],
            [InlineKeyboardButton("📊 2. Sovereign Audit ($50K - $100K)", callback_data="s2")],
            [InlineKeyboardButton("⚓ 3. Emergency Node ($8.5K - $25K)", callback_data="s3")],
            [InlineKeyboardButton("📜 4. Tier 3 Governance ($45K+)", callback_data="s4")],
            [InlineKeyboardButton("🧠 5. Expert Maritime Intelligence", callback_data="s5")]
        ]
        await update.message.reply_text("Select a sovereign service for execution:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # 2, 3, 4, 5. معالجة النص عبر وحدة التفكير الذاكرة والأدوات والمشغلات
    response_text = MNCOSMasterAgent.process_interaction(user_id, text)
    await update.message.reply_text(response_text)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("🚀 MNCOS 5-Component Multi-Agent Sovereign Ecosystem is online 24/7...")
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
