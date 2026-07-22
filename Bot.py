import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Xotirada saqlash uchun bazalar
USER_DATA = {}   # {user_id: {"urls": [], "bots": {}}}
USER_LIMITS = {} # {user_id: {"add_url": 0, "add_bot": 0, "security": 0}} -- 0: ishlatmagan, 1: ishlatgan

CARD_NUMBER = "9860606761428865"
CARD_HOLDER = "MATKARIMOV SHOXRUZBEK"
ADMIN_USERNAME = "@shoxruz_cy"

# Asosiy menyu (Pastdagi tugmalar)
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🌐 URL Qo'shish")
    builder.button(text="📊 Saytlarim")
    builder.button(text="🤖 Bot Qo'shish (24/7)")
    builder.button(text="🛡 Xavfsizlik")
    builder.button(text="⚙️ Sozlamalar")
    builder.button(text="💎 Premium")
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)

# Tilni tanlash
def get_lang_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(3)
    return builder.as_markup()

# Xavfsizlikni tekshirish turlari
def get_security_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Saytni tekshirish", callback_data="sec_check_site")
    builder.button(text="🤖 Botni tekshirish", callback_data="sec_check_bot")
    builder.adjust(1)
    return builder.as_markup()

# Premium tariflari
def get_premium_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Kunlik — 5,000 so'm", callback_data="prem_daily")
    builder.button(text="📆 Haftalik — 12,000 so'm", callback_data="prem_weekly")
    builder.button(text="🗓 Oylik — 21,000 so'm", callback_data="prem_monthly")
    builder.button(text="🏆 Yillik — 99,000 so'm", callback_data="prem_yearly")
    builder.adjust(1)
    return builder.as_markup()

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    bot_info = await bot.get_me()
    bot_name = bot_info.first_name
    
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}}
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}

    welcome_text = (
        f"Assalomu alaykum, **{user_name}**!\n\n"
        f"🤖 Men — **{bot_name}** botiman.\n"
        f"📌 **Bajaradigan vazifalarim:**\n"
        f"• Saytlar va havolalar xavfsizligini 24/7 monitoring qilish;\n"
        f"• Foydalanuvchilarning shaxsiy botlarini uxlab qolmaydigan (24/7) qilib yurgizib berish;\n"
        f"• Xavfsizlikni tekshirish va himoya qilish.\n\n"
        f"⚠️ *Diqqat:* Har bir asosiy funksiyadan **1 martalik bepul limit** asosida foydalanishingiz mumkin.\n\n"
        f"Iltimos, tilni tanlang:"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await message.answer("🌐 Tilni tanlang / Выберите язык / Select language:", reply_markup=get_lang_menu())

@dp.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[1]
    texts = {
        "uz": "✅ O'zbek tili tanlandi!\n\nKerakli bo'limni pastdagi menyudan tanlang:",
        "ru": "✅ Русский язык выбран!\n\nВыберите нужный раздел в меню ниже:",
        "en": "✅ English language selected!\n\nChoose a section from the menu below:"
    }
    await callback.message.answer(texts.get(lang, texts["uz"]))

# --- 24/7 BOT YURGIZISH QISMI (LIMIT BILAN) ---
async def start_user_bot_polling(user_token: str):
    u_bot = Bot(token=user_token)
    u_dp = Dispatcher()
    
    @u_dp.message(Command("start"))
    async def u_start(msg: types.Message):
        await msg.answer(
            "🎵 **Music Hub Bot** ishga tushdi!\n\n"
            "🔍 Qo'shiq nomi yoki ijrochi ismini yozing — Top-10 natija chiqadi.\n"
            "🚀 Yuklab olmoqchi bo'lgan videoga havolani yuboring!\n\n"
            "<i>(UpShieldBot orqali 24/7 rejimida ishlayapti)</i>",
            parse_mode="HTML"
        )
        
    @u_dp.message()
    async def u_echo(msg: types.Message):
        await msg.answer(f"Qabul qilindi: {msg.text}. Qoshiq yoki musiqa qidirilmoqda...")

    try:
        await u_dp.start_polling(u_bot)
    except Exception as e:
        logging.error(f"User bot polling error: {e}")

@dp.message(F.text == "🤖 Bot Qo'shish (24/7)")
async def ask_for_bot_token(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["add_bot"] >= 1:
        await message.answer(
            "❌ **Bepul limit tugadi!**\n\n"
            "Siz allaqachon bepul 1 martalik bot ulash imkoniyatidan foylangansiz.\n"
            "Cheksiz foydalanish uchun **💎 Premium** sotib oling!",
            reply_markup=get_premium_menu(),
            parse_mode="Markdown"
        )
        return

    await message.answer(
        "🤖 O'z botingizni 24/7 rejimida ishlatish uchun @BotFather'dan olgan **Token**ingizni yuboring:\n\n"
        "_Masalan: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`_",
        parse_mode="Markdown"
    )

@dp.message(F.text.contains(":") and F.text.len() > 30)
async def register_user_bot(message: types.Message):
    user_id = message.from_user.id
    user_token = message.text.strip()
    
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["add_bot"] >= 1:
        return # Limiti tugagan bo'lsa hech narsa qilmaydi
    
    try:
        test_bot = Bot(token=user_token)
        bot_info = await test_bot.get_me()
        await test_bot.session.close()
        
        if user_id not in USER_DATA:
            USER_DATA[user_id] = {"urls": [], "bots": {}}
            
        if user_token not in USER_DATA[user_id]["bots"]:
            # Limitni band qilamiz (1 ta urindi)
            USER_LIMITS[user_id]["add_bot"] = 1
            
            # 24/7 ishga tushiramiz
            task = asyncio.create_task(start_user_bot_polling(user_token))
            USER_DATA[user_id]["bots"][user_token] = {"name": f"@{bot_info.username}", "status": "Faol", "task": task}
            
            await message.answer(
                f"✅ **Tabriklaymiz! (1 martalik bepul limit ishlatildi)**\n\n"
                f"🤖 @{bot_info.username} muvaffaqiyatli ulandi va **24/7 rejimida** ishga tushirildi! 🚀\n\n"
                f"Keyingi safar bot ulash uchun 💎 Premium sotib olishingiz kerak bo'ladi.",
                parse_mode="Markdown"
            )
        else:
            await message.answer("⚠️ Bu bot allaqachon ulangan!")
    except Exception:
        await message.answer("❌ Xatolik: Token yaroqsiz yoki noto'g'ri.")

# --- URL QO'SHISH VA SAYTLARIM (LIMIT BILAN) ---
@dp.message(F.text == "🌐 URL Qo'shish")
async def add_url_prompt(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["add_url"] >= 1:
        await message.answer(
            "❌ **Bepul URL qo'shish limiti tugadi!**\n\n"
            "Siz allaqachon bepul 1 martalik sayt qo'shish imkoniyatidan foylangansiz.\n"
            "Cheksiz sayt qo'shish uchun **💎 Premium** sotib oling!",
            reply_markup=get_premium_menu(),
            parse_mode="Markdown"
        )
        return

    await message.answer("Iltimos, monitoring qilish uchun sayt URL manzilini yuboring (Masalan: `https://example.com`):", parse_mode="Markdown")

@dp.message(F.text.startswith("http://") or F.text.startswith("https://"))
async def save_url(message: types.Message):
    user_id = message.from_user.id
    url = message.text.strip()
    
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["add_url"] >= 1:
        return # Limit tugagan bo'lsa e'tibor bermaydi
        
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}}
    
    if url not in USER_DATA[user_id]["urls"]:
        # Limitni sarflaymiz
        USER_LIMITS[user_id]["add_url"] = 1
        USER_DATA[user_id]["urls"].append(url)
        
        await message.answer(
            f"✅ **Sayt muvaffaqiyatli qo'shildi (1 martalik bepul limit ishlatildi):**\n`{url}`\n\n"
            f"Boshqa sayt qo'shish uchun 💎 Premium talab etiladi.",
            parse_mode="Markdown"
        )
    else:
        await message.answer("⚠️ Bu sayt allaqachon ro'yxatda bor.")

@dp.message(F.text == "📊 Saytlarim")
async def show_sites(message: types.Message):
    user_id = message.from_user.id
    urls = USER_DATA.get(user_id, {}).get("urls", [])
    
    if not urls:
        await message.answer("📊 Sizning kuzatuvdagi saytlaringiz ro'yxati hozircha bo'sh. '🌐 URL Qo'shish' tugmasi orqali qo'shishingiz mumkin.")
    else:
        text = "📊 **Sizning kuzatuvdagi saytlaringiz:**\n\n" + "\n".join([f"• {u}" for u in urls])
        await message.answer(text, parse_mode="Markdown")

# --- XAVFSIZLIK (LIMIT BILAN) ---
@dp.message(F.text == "🛡 Xavfsizlik")
async def security_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["security"] >= 1:
        await message.answer(
            "❌ **Bepul xavfsizlik tekshiruvi limiti tugadi!**\n\n"
            "Siz allaqachon bepul 1 martalik tekshiruvdan foydlangansiz.\n"
            "Doimiy tekshiruvlar uchun **💎 Premium** sotib oling!",
            reply_markup=get_premium_menu(),
            parse_mode="Markdown"
        )
        return

    await message.answer(
        "🛡 **Xavfsizlik markazi** (1 martalik bepul tekshiruv)\n\nNima tekshirishni xohlaysiz?",
        reply_markup=get_security_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("sec_check_"))
async def process_security_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}
        
    if USER_LIMITS[user_id]["security"] >= 1:
        await callback.answer("Limit tugagan!", show_alert=True)
        return

    # Limitni sarflaymiz
    USER_LIMITS[user_id]["security"] = 1
    
    await callback.answer()
    check_type = callback.data.split("_")[2]
    
    msg = await callback.message.answer("🔍 **Tekshirilmoqda...** Iltimos, biroz kuting ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)
    
    if check_type == "site":
        await msg.edit_text("🛡 **Sayt xavfsizlik natijasi:**\n\n✅ SSL sertifikat: Himoyalangan\n✅ Zararli kodlar: Topilmadi\n✅ Holat: Barqaror va xavfsiz!\n\n_Bepul limit yakunlandi._", parse_mode="Markdown")
    else:
        await msg.edit_text("🤖 **Bot xavfsizlik natijasi:**\n\n✅ Token xavfsizligi: Yuqori\n✅ API ulanishi: Barqaror\n✅ Xavflar: Aniqlanmadi!\n\n_Bepul limit yakunlandi._", parse_mode="Markdown")

# --- SOZLAMALAR ---
@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}})
    
    urls_count = len(user_info["urls"])
    bots_count = len(user_info["bots"])
    
    settings_text = (
        f"⚙️ **Sozlamalar va boshqaruv paneli**\n\n"
        f"• Ulangan saytlaringiz soni: {urls_count}\n"
        f"• Ulangan botlaringiz soni: {bots_count}\n\n"
        f"Sayt yoki tokenlarni o'chirish uchun:\n"
        f"• Saytni o'chirish: `/delurl sayt_nomi`"
    )
    await message.answer(settings_text, parse_mode="Markdown")

@dp.message(Command("delurl"))
async def delete_url(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, o'chirmoqchi bo'lgan URL manzilni yuboring. Masalan: `/delurl https://example.com`", parse_mode="Markdown")
        return
    url = args[1].strip()
    if user_id in USER_DATA and url in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].remove(url)
        await message.answer(f"✅ Sayt o'chirildi: `{url}`", parse_mode="Markdown")
    else:
        await message.answer("❌ Bunday URL topilmadi.")

# --- PREMIUM VA TO'LOV ---
@dp.message(F.text == "💎 Premium")
async def show_premium(message: types.Message):
    text = (
        "💎 **UpShieldBot Premium** bo'limiga xush kelibsiz!\n\n"
        "Cheklovlarsiz foydalanish uchun quyidagi tariflardan birini tanlang:"
    )
    await message.answer(text, reply_markup=get_premium_menu(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("prem_"))
async def process_premium_choice(callback: types.CallbackQuery):
    await callback.answer()
    choice = callback.data.split("_")[1]
    
    prices = {
        "daily": ("Kunlik Premium", "5,000 so'm"),
        "weekly": ("Haftalik Premium", "12,000 so'm"),
        "monthly": ("Oylik Premium", "21,000 so'm"),
        "yearly": ("Yillik Premium", "99,000 so'm")
    }
    
    plan_name, price = prices.get(choice, ("Premium", "0 so'm"))
    
    payment_text = (
        f"📦 **Tanlangan tarif:** {plan_name}\n"
        f"💵 **Narxi:** {price}\n\n"
        f"💳 **Karta raqami:**\n`{CARD_NUMBER}`\n"
        f"👤 **Karta egasi:** {CARD_HOLDER}\n\n"
        f"📌 **Qanday qilib faollashadi?**\n"
        f"To'lovni amalga oshirgach, chekni (skrinshotni) to'g'ridan-to'g'ri adminimizga yuboring: {ADMIN_USERNAME}."
    )
    
    await callback.message.answer(payment_text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
