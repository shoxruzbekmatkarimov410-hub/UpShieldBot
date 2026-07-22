import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

# 🔑 Bot Token
BOT_TOKEN = "8537284527:AAFh84M21G83czRRKSG2IcuwnWgQYt8p69Q"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

def language_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "uz":
        kb = [
            [InlineKeyboardButton(text="🌐 URL Qo'shish", callback_data="add_url"), InlineKeyboardButton(text="📊 Saytlarim", callback_data="my_sites")],
            [InlineKeyboardButton(text="🛡 Xavfsizlik", callback_data="security"), InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")]
        ]
    elif lang == "ru":
        kb = [
            [InlineKeyboardButton(text="🌐 Добавить URL", callback_data="add_url"), InlineKeyboardButton(text="📊 Мои сайты", callback_data="my_sites")],
            [InlineKeyboardButton(text="🛡 Безопасность", callback_data="security"), InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
        ]
    else:
        kb = [
            [InlineKeyboardButton(text="🌐 Add URL", callback_data="add_url"), InlineKeyboardButton(text="📊 My Sites", callback_data="my_sites")],
            [InlineKeyboardButton(text="🛡 Security", callback_data="security"), InlineKeyboardButton(text="⚙️ Settings", callback_data="settings")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "/start")
async def start_handler(message: Message):
    text = (
        "👋 Assalomu alaykum! Tilni tanlang:\n"
        "👋 Здравствуйте! Выберите язык:\n"
        "👋 Hello! Select your language:"
    )
    await message.answer(text, reply_markup=language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def set_language(call: CallbackQuery):
    lang = call.data.split("_")[1]
    
    if lang == "uz":
        text = "✅ **O'zbek tili tanlandi!**\n\n🛡 **UpShieldBot** ga xush kelibsiz. Kerakli bo'limni tanlang:"
    elif lang == "ru":
        text = "✅ **Выбран русский язык!**\n\n🛡 Добро пожаловать в **UpShieldBot**. Выберите нужный раздел:"
    else:
        text = "✅ **English language selected!**\n\n🛡 Welcome to **UpShieldBot**. Choose a section:"

    await call.message.edit_text(text, reply_markup=main_menu_keyboard(lang), parse_mode=ParseMode.MARKDOWN)
    await call.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
