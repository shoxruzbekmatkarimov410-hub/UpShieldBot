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

# To'lov uchun karta ma'lumotlari
CARD_NUMBER = "9860606761428865"
CARD_HOLDER = "MATKARIMOV SHOXRUZBEK"

# Fa ishlab turgan foydalanuvchi botlarini saqlash uchun lug'at (Task'lar)
running_user_bots = {}

# 1. Asosiy menyu tugmalari
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

# 2. Tilni tanlash inline tugmalari
def get_lang_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(3)
    return builder.as_markup()

# 3. Premium tariflari inline tugmalari
def get_premium_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Kunlik — 5,000 so'm", callback_data="prem_daily")
    builder.button(text="📆 Haftalik — 12,000 so'm", callback_data="prem_weekly")
    builder.button(text="🗓 Oylik — 21,000 so'm", callback_data="prem_monthly")
    builder.button(text="🏆 Yillik — 99,000 so'm", callback_data="prem_yearly")
    builder.adjust(1)
    return builder.as_markup()

# /start komissiyasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.full_name
    bot_info = await bot.get_me()
    bot_name = bot_info.first_name
    
    welcome_text = (
        f"Assalomu alaykum, **{user_name}**!\n\n"
        f"🤖 Men — **{bot_name}** botiman.\n"
        f"📌 **Bajaradigan vazifam:** Saytlar xavfsizligini monitoring qilish va o'z botlaringizni 24/7 rejimida bepul yurgizib berish.\n\n"
        f"Iltimos, tilni tanlang:"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    await message.answer("🌐 Tilni tanlang / Выберите язык / Select language:", reply_markup=get_lang_menu())

# Tilni tanlash
@dp.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[1]
    
    if lang == "uz":
        text = "✅ O'zbek tili tanlandi!\n\nKerakli bo'limni pastdagi menyudan tanlang:"
    elif lang == "ru":
        text = "✅ Русский язык выбран!\n\nВыберите нужный раздел в меню ниже:"
    else:
        text = "✅ English language selected!\n\nChoose a section from the menu below:"
        
    await callback.message.answer(text)

# --- FOYDALANUVCHI BOTINI 24/7 ISHLatuvchi FUNKSIYA ---
async def start_user_bot_polling(user_token: str):
    """Foydalanuvchi tokeni orqali uning botini fonda 24/7 ishga tushiradi"""
    u_bot = Bot(token=user_token)
    u_dp = Dispatcher()
    
    @u_dp.message(Command("start"))
    async def u_start(message: types.Message):
        await message.answer("Salom! Bu bot UpShieldBot orqali 24/7 rejimida ishga tushirildi! 🚀")
        
    try:
        await u_dp.start_polling(u_bot)
    except Exception as e:
        logging.error(f"User bot error: {e}")

@dp.message(F.text == "🤖 Bot Qo'shish (24/7)")
async def ask_for_bot_token(message: types.Message):
    await message.answer(
        "🤖 O'z botingizni 24/7 ishga tushirish uchun @BotFather'dan olgan **Token**ingizni yuboring:\n\n"
        "_Masalan: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`_",
        parse_mode="Markdown"
    )

# Token kelganda uni tekshirib 24/7 ishga tushirish
@dp.message(F.text.contains(":") and F.text.len() > 30)
async def register_user_bot(message: types.Message):
    user_token = message.text.strip()
    
    try:
        test_bot = Bot(token=user_token)
        bot_info = await test_bot.get_me()
        await test_bot.session.close()
        
        if user_token not in running_user_bots:
            # Fondagi vazifaga qo'shamiz (24/7 ishlashi uchun)
            task = asyncio.create_task(start_user_bot_polling(user_token))
            running_user_bots[user_token] = task
            
            await message.answer(
                f"✅ **Tabriklaymiz!**\n\n"
                f"🤖 @{bot_info.username} muvaffaqiyatli ulandi va hozirda **24/7 rejimida** ishga tushirildi! 🚀",
                parse_mode="Markdown"
            )
        else:
            await message.answer("⚠️ Bu bot allaqachon ulangan va ishlamoqda!")
            
    except Exception:
        await message.answer("❌ Xatolik: Token noto'g'ri yoki yaroqsiz. Iltimos, @BotFather'dan to'g'ri tokenni yuboring.")

# --- PREMIUM VA BOSHQA BO'LIMLAR ---
@dp.message(F.text == "💎 Premium")
async def show_premium(message: types.Message):
    text = (
        "💎 **UpShieldBot Premium** bo'limiga xush kelibsiz!\n\n"
        "Quyidagi tariflardan o'zingizga mos keladiganini tanlang:"
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
        f"_To'lovni amalga oshirgach, chekni adminga yuboring._"
    )
    
    await callback.message.answer(payment_text, parse_mode="Markdown")

@dp.message(F.text == "🌐 URL Qo'shish")
async def add_url(message: types.Message):
    await message.answer("Iltimos, monitoring qilish uchun URL manzilni yuboring:")

@dp.message(F.text == "📊 Saytlarim")
async def my_sites(message: types.Message):
    await message.answer("Sizning kuzatuvdagi saytlaringiz ro'yxati hozircha bo'sh.")

@dp.message(F.text == "🛡 Xavfsizlik")
async def security_info(message: types.Message):
    await message.answer("🛡 Xavfsizlik holati: Tizim barqaror va himoyalangan.")

@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: types.Message):
    await message.answer("⚙️ Sozlamalar menyusi. Tilni o'zgartirish uchun /start buyrug'ini yuboring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
