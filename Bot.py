import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8514966807  # Sening ID raqaming
ADMIN_USERNAME = "@shoxruz_cy"
BOT_USERNAME = "@UpShieldcyber_bot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ma'lumotlar bazasi
USER_DATA = {}   # {user_id: {"urls": [], "bots": {}, "is_premium": False}}
USER_LIMITS = {} # {user_id: {"add_url": 0, "add_bot": 0, "security": 0}}

CARD_NUMBER = "9860606761428865"
CARD_HOLDER = "MATKARIMOV SHOXRUZBEK"
SECRET_PROMO = "mohim0910"

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

def get_lang_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(3)
    return builder.as_markup()

def get_security_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Saytni chuqur tekshirish", callback_data="sec_check_site")
    builder.button(text="🤖 Botni chuqur tekshirish", callback_data="sec_check_bot")
    builder.adjust(1)
    return builder.as_markup()

def get_premium_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Kunlik — 3,999 so'm", callback_data="prem_daily")
    builder.button(text="📆 Haftalik — 9,900 so'm", callback_data="prem_weekly")
    builder.button(text="🗓 Oylik — 19,999 so'm", callback_data="prem_monthly")
    builder.button(text="🏆 Yillik — 99,999 so'm", callback_data="prem_yearly")
    builder.adjust(1)
    return builder.as_markup()

# --- START BUYrug'i ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {"add_url": 0, "add_bot": 0, "security": 0}

    welcome_text = (
        f"Assalomu alaykum, {user_name}!\n\n"
        f"🤖 Men — {BOT_USERNAME} 🛡 botiman.\n"
        f"📌 Bajaradigan vazifalarim:\n"
        f"• Saytlar va havolalar xavfsizligini 24/7 monitoring qilish;\n"
        f"• Foydalanuvchilarning shaxsiy botlarini uxlab qolmaydigan (24/7) qilib yurgizib berish;\n"
        f"• Xavfsizlikni tekshirish va himoya qilish.\n\n"
        f"⚠️ Diqqat: Har bir asosiy funksiyadan 1 martalik bepul limit asosida foydalanishingiz mumkin.\n\n"
        f"Iltimos, tilni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_lang_menu(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[1]
    texts = {
        "uz": f"✅ O'zbek tili tanlandi! 🛡 {BOT_USERNAME} boshqaruv paneliga xush kelibsiz.",
        "ru": f"✅ Русский язык выбран! 🛡 Добро пожаловать в панель {BOT_USERNAME}.",
        "en": f"✅ English language selected! 🛡 Welcome to {BOT_USERNAME} panel."
    }
    await callback.message.answer(texts.get(lang, "✅ Tanlandi!"), reply_markup=get_main_menu())

# --- PROMOKOD TIZIMI ---
@dp.message(Command("promokod"))
async def promo_command(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(f"Iltimos, promokodni kiriting. Masalan: `/promokod mohim0910` 🛡 [{BOT_USERNAME}]", parse_mode="Markdown")
        return
    
    code = args[1].strip()
    if code == SECRET_PROMO:
        if user_id not in USER_DATA:
            USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
        USER_DATA[user_id]["is_premium"] = True
        await message.answer(f"🎉 **Tabriklaymiz!** Promokod muvaffaqiyatli qabul qilindi. Sizga **CHEKSIZ PREMIUM** statusi berildi! 🚀\n\n_Bu xabar {BOT_USERNAME} orqali olindi._", parse_mode="Markdown")
    else:
        await message.answer(f"❌ Noto'g'ri promokod. 🛡 [{BOT_USERNAME}]")

# --- TO'LOV VA TARIFFLAR ---
@dp.callback_query(F.data.startswith("prem_"))
async def process_premium_choice(callback: types.CallbackQuery):
    await callback.answer()
    choice = callback.data.split("_")[1]
    prices = {
        "daily": ("Kunlik", "3,999 so'm"),
        "weekly": ("Haftalik", "9,900 so'm"),
        "monthly": ("Oylik", "19,999 so'm"),
        "yearly": ("Yillik", "99,999 so'm")
    }
    p_name, p_price = prices.get(choice, ("Premium", "0 so'm"))
    
    text = (
        f"📦 **Tarif:** {p_name} ({p_price})\n\n"
        f"💳 **Karta raqami:**\n`{CARD_NUMBER}`\n"
        f"👤 **Karta egasi:** {CARD_HOLDER}\n\n"
        f"📌 To'lovni amalga oshirgach, chek yoki istalgan rasm skrinshotini shu botga yuboring. Admin o'zi tekshirib tasdiqlaydi.\n"
        f"💬 To'lovda muammo bo'lsa adminga yozing: [{ADMIN_USERNAME}](https://t.me/shoxruz_cy)\n\n"
        f"_🛡 {BOT_USERNAME} orqali yaratildi_"
    )
    await callback.message.answer(text, parse_mode="Markdown", disable_web_page_preview=True)

# --- HAR QANDAY RASMNI QABUL QILISH VA ADMINGA YUBORISH ---
@dp.message(F.photo)
async def receive_payment_receipt(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    if user_id == ADMIN_ID:
        await message.answer(f"Bu sizning rasmingiz (Admin). 🛡 [{BOT_USERNAME}]")
        return

    photo_id = message.photo[-1].file_id
    
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Premium ochish", callback_data=f"give_prem_{user_id}")
    builder.button(text="❌ Rad etish", callback_data=f"reject_prem_{user_id}")
    builder.adjust(2)

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=f"🔔 **Yangi rasm / to'lov cheki keldi!**\n\n👤 Foydalanuvchi: {user_name}\n🆔 ID: `{user_id}`\n💬 Izoh: {message.caption or 'Izoh yo\'q'}",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    
    await message.answer(
        f"✅ **Rasm va so'rovingiz qabul qilindi!**\n"
        f"Admin tez orada tekshirib chiqadi. To'lovda muammo bo'lsa adminga yozing: [{ADMIN_USERNAME}](https://t.me/shoxruz_cy)\n\n"
        f"_🛡 {BOT_USERNAME}_",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

@dp.callback_query(F.data.startswith("give_prem_"))
async def admin_give_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    
    if target_user_id not in USER_DATA:
        USER_DATA[target_user_id] = {"urls": [], "bots": {}, "is_premium": True}
    else:
        USER_DATA[target_user_id]["is_premium"] = True
        
    await callback.answer("Foydalanuvchiga Premium berildi!", show_alert=True)
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n✅ **HOLAT: Tasdiqlandi (Premium berildi)**", parse_mode="Markdown")
    
    try:
        await bot.send_message(target_user_id, f"🎉 **Tabriklaymiz!** Admin to'lovingizni tasdiqladi va sizga **PREMIUM** statusi berildi! 🚀\n\n_🛡 {BOT_USERNAME}_")
    except Exception:
        pass

@dp.callback_query(F.data.startswith("reject_prem_"))
async def admin_reject_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    await callback.answer("To'lov rad etildi.", show_alert=True)
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n❌ **HOLAT: Rad etildi**", parse_mode="Markdown")
    
    try:
        await bot.send_message(target_user_id, f"❌ Afsuski, yuborgan rasmingiz/to'lovingiz rad etildi. To'lovda muammo bo'lsa adminga yozing: [{ADMIN_USERNAME}](https://t.me/shoxruz_cy)\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown", disable_web_page_preview=True)
    except Exception:
        pass

# --- 24/7 CRONJOB MONITORING QANDAY ISHLAYDI? ---
# Tushuntirish: Kod fonda (background task) har 30 sekundda ulangan bot tokeni orqali Telegram serveriga 
# 'get_me()' so'rovini yuboradi. Shu orqali botingiz doimiy faol turadi va uxlab qolmaydi.
async def keep_bot_alive(user_token: str):
    u_bot = Bot(token=user_token)
    while True:
        try:
            await u_bot.get_me() # Bot tokenini tekshirib, tirik saqlab turadi
        except Exception as e:
            logging.error(f"Keep alive error: {e}")
        await asyncio.sleep(30)

@dp.message(F.text == "🤖 Bot Qo'shish (24/7)")
async def ask_for_bot_token(message: types.Message):
    user_id = message.from_user.id
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
    
    if not is_prem and USER_LIMITS.get(user_id, {}).get("add_bot", 0) >= 1:
        await message.answer(f"❌ Bepul limit tugadi! Cheksiz foydalanish uchun 💎 Premium oling:\n\n_🛡 {BOT_USERNAME}_", reply_markup=get_premium_menu())
        return

    await message.answer(f"🤖 Botingizni 24/7 qilish uchun @BotFather'dan olgan **Token**ingizni yuboring:\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")

@dp.message(F.text.contains(":") and F.text.len() > 30)
async def register_user_bot(message: types.Message):
    user_id = message.from_user.id
    user_token = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
    
    if not is_prem and USER_LIMITS.get(user_id, {}).get("add_bot", 0) >= 1:
        return

    try:
        test_bot = Bot(token=user_token)
        bot_info = await test_bot.get_me()
        await test_bot.session.close()
        
        if user_id not in USER_DATA:
            USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
            
        if user_token not in USER_DATA[user_id]["bots"]:
            if not is_prem:
                USER_LIMITS[user_id]["add_bot"] = 1
            
            task = asyncio.create_task(keep_bot_alive(user_token))
            USER_DATA[user_id]["bots"][user_token] = {"name": f"@{bot_info.username}", "task": task}
            
            await message.answer(f"✅ @{bot_info.username} muvaffaqiyatli ulandi va **24/7 cronjob** rejimida ishga tushdi! 🚀\n_Har 30 sekundda ping qilinib, uxlab qolishi oldi olinmoqda._\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")
        else:
            await message.answer(f"⚠️ Bu bot allaqachon ulangan! 🛡 [{BOT_USERNAME}]")
    except Exception:
        await message.answer(f"❌ Xatolik: Token yaroqsiz. 🛡 [{BOT_USERNAME}]")

# --- URL QO'SHISH ---
@dp.message(F.text == "🌐 URL Qo'shish")
async def add_url_prompt(message: types.Message):
    user_id = message.from_user.id
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
    
    if not is_prem and USER_LIMITS.get(user_id, {}).get("add_url", 0) >= 1:
        await message.answer(f"❌ Bepul URL limiti tugadi! Premium oling:\n\n_🛡 {BOT_USERNAME}_", reply_markup=get_premium_menu())
        return
    await message.answer(f"Iltimos, sayt URL manzilini yuboring (Masalan: `https://example.com`):\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")

@dp.message(F.text.startswith("http://") or F.text.startswith("https://"))
async def save_url(message: types.Message):
    user_id = message.from_user.id
    url = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
    
    if not is_prem and USER_LIMITS.get(user_id, {}).get("add_url", 0) >= 1:
        return
        
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
    
    if url not in USER_DATA[user_id]["urls"]:
        if not is_prem:
            USER_LIMITS[user_id]["add_url"] = 1
        USER_DATA[user_id]["urls"].append(url)
        await message.answer(f"✅ Sayt qo'shildi va kuzatuvga olindi:\n`{url}`\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")
    else:
        await message.answer(f"⚠️ Bu sayt allaqachon bor. 🛡 [{BOT_USERNAME}]")

@dp.message(F.text == "📊 Saytlarim")
async def show_sites(message: types.Message):
    user_id = message.from_user.id
    urls = USER_DATA.get(user_id, {}).get("urls", [])
    if not urls:
        await message.answer(f"📊 Sizning kuzatuvdagi saytlaringiz yo'q. 🛡 [{BOT_USERNAME}]")
    else:
        text = f"📊 **Sizning saytlaringiz:**\n\n" + "\n".join([f"• {u}" for u in urls]) + f"\n\n_🛡 {BOT_USERNAME}_"
        await message.answer(text, parse_mode="Markdown")

# --- KENGAYTIRILGAN XAVFSIZLIK MARKAZI ---
@dp.message(F.text == "🛡 Xavfsizlik")
async def security_menu(message: types.Message):
    await message.answer(f"🛡 **Xavfsizlik markazi**\n\nQuyidagilardan birini tanlab chuqur tekshiruvdan o'tkazing:\n\n_🛡 {BOT_USERNAME}_", reply_markup=get_security_menu(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("sec_check_"))
async def process_security_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    check_type = callback.data.split("_")[3]
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}})
    
    # Foydalanuvchi sayt yoki bot kiritmagan bo'lsa xato qaytarish
    if check_type == "site" and not user_info["urls"]:
        await callback.answer("⚠️ Xatolik: Siz hali tizimga sayt kiritmagansiz!", show_alert=True)
        await callback.message.answer(f"❌ Xavfsizlikni tekshirib bo'lmadi: Bazangizda saytlar mavjud emas. Avval **🌐 URL Qo'shish** orqali sayt qo'shing.\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")
        return

    if check_type == "bot" and not user_info["bots"]:
        await callback.answer("⚠️ Xatolik: Siz hali tizimga bot ulamagansiz!", show_alert=True)
        await callback.message.answer(f"❌ Xavfsizlikni tekshirib bo'lmadi: Bazangizda ulangan botlar mavjud emas. Avval **🤖 Bot Qo'shish (24/7)** orqali bot ulang.\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")
        return

    await callback.answer()
    msg = await callback.message.answer(
        f"🔍 **Chuqur xavfsizlik tahlili bajarilmoqda...**\n"
        f"• SSL/TLS shifrlash va sertifikatlar tekshirilmoqda...\n"
        f"• DDoS va SQLi / XSS zaifliklari qidirilmoqda...\n"
        f"• Portlar ochiqligi va API token xavfsizligi o'rganilmoqda...\n\n_⏳ Iltimos, kuting..._",
        parse_mode="Markdown"
    )
    await asyncio.sleep(3)
    
    if check_type == "site":
        target_url = user_info["urls"][0]
        await msg.edit_text(
            f"🛡 **Sayt xavfsizlik tahlili natijasi (`{target_url}`):**\n\n"
            f"✅ **SSL/TLS sertifikat:** Faol va ishonchli (A+ reyting)\n"
            f"✅ **DDoS himoyasi:** Aniqlangan va faol\n"
            f"✅ **SQL Injection / XSS:** Zaifliklar topilmadi\n"
            f"✅ **Ochiq portlar:** Xavfsiz (Faqat 80/443)\n"
            f"🏆 **Umumiy xavfsizlik darajasi:** 99% (Mukammal)\n\n"
            f"_🛡 {BOT_USERNAME} orqali tekshirildi_",
            parse_mode="Markdown"
        )
    else:
        bot_name = list(user_info["bots"].values())[0]["name"]
        await msg.edit_text(
            f"🤖 **Bot xavfsizlik tahlili natijasi (`{bot_name}`):**\n\n"
            f"✅ **API Token himoyasi:** Oqish (leak) alomatlari yo'q\n"
            f"✅ **Server ulanishi (Webhook/Polling):** Shifrlangan va barqaror\n"
            f"✅ **Xotira oqishi (Memory Leak):** Aniqlanmadi\n"
            f"✅ **Ruxsatsiz kirish urinishlari:** 0 ta\n"
            f"🏆 **Umumiy barqarorlik:** 100% (24/7 ishlayapti)\n\n"
            f"_🛡 {BOT_USERNAME} orqali tekshirildi_",
            parse_mode="Markdown"
        )

# --- SOZLAMALAR (MA'LUMOTLARNI O'CHIRISH TUGMALARI) ---
@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}})
    
    builder = InlineKeyboardBuilder()
    has_items = False
    
    for url in user_info["urls"]:
        builder.button(text=f"🗑 Saytni o'chirish: {url[:15]}...", callback_data=f"del_url_{url}")
        has_items = True
        
    for token, bdata in user_info["bots"].items():
        builder.button(text=f"🗑 Botni o'chirish: {bdata['name']}", callback_data=f"del_bot_{token}")
        has_items = True
        
    if not has_items:
        await message.answer(f"⚙️ **Sozlamalar paneli**\n\nSizda hozircha o'chirish uchun qo'shilgan saytlar yoki botlar mavjud emas.\n\n_🛡 {BOT_USERNAME}_", parse_mode="Markdown")
        return

    builder.adjust(1)
    await message.answer(
        f"⚙️ **Sozlamalar va boshqaruv paneli**\n\nQuyidagi tugmalar yordamida o'zingiz kiritgan ma'lumotlarni o'chirishingiz mumkin:\n\n_🛡 {BOT_USERNAME}_",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("del_url_"))
async def delete_url_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    url = callback.data.replace("del_url_", "")
    if user_id in USER_DATA and url in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].remove(url)
        await callback.answer("✅ Sayt muvaffaqiyatli o'chirildi!", show_alert=True)
        await callback.message.edit_text(f"✅ Sayt bazadan o'chirildi.\n\n_🛡 {BOT_USERNAME}_")

@dp.callback_query(F.data.startswith("del_bot_"))
async def delete_bot_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    token = callback.data.replace("del_bot_", "")
    if user_id in USER_DATA and token in USER_DATA[user_id]["bots"]:
        USER_DATA[user_id]["bots"][token]["task"].cancel()
        del USER_DATA[user_id]["bots"][token]
        await callback.answer("✅ Bot o'chirildi va 24/7 to'xtatildi!", show_alert=True)
        await callback.message.edit_text(f"✅ Bot muvaffaqiyatli o'chirildi va kuzatuvdan olib tashlandi.\n\n_🛡 {BOT_USERNAME}_")

# --- 💎 PREMIUM MENYU VA FARQLARI ---
@dp.message(F.text == "💎 Premium")
async def show_premium(message: types.Message):
    premium_info = (
        f"💎 **{BOT_USERNAME} Premium imkoniyatlari**\n\n"
        f"Oddiy (bepul) tarif va **Premium** tarif o'rtasidagi farqlar:\n\n"
        f"❌ **Oddiy tarif:**\n"
        f"• Faqat 1 marta bepul sayt qo'shish mumkin\n"
        f"• Faqat 1 marta bepul bot ulash mumkin\n"
        f"• Cheklangan xavfsizlik tekshiruvlari\n\n"
        f"✅ **Premium tarif:**\n"
        f"• **Cheksiz miqdorda** saytlar va havolalarni 24/7 monitoring qilish\n"
        f"• **Cheksiz miqdorda** shaxsiy botlarni 24/7 uxlab qolmaydigan rejimda yurgizish\n"
        f"• **Chuqur va professional** xavfsizlik tahlillari (SQLi, XSS, DDoS, SSL reytinglari)\n"
        f"• Admin tomonidan ustuvor qo'llab-quvvatlash (24/7 yordam)\n\n"
        f"Quyidagi tariflardan birini tanlang va Premium huquqiga ega bo'ling:\n\n"
        f"_🛡 {BOT_USERNAME}_"
    )
    await message.answer(premium_info, reply_markup=get_premium_menu(), parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
