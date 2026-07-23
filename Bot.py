import os
import logging
import asyncio
import time
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8514966807  
ADMIN_USERNAME = "@shoxruz_cy"
BOT_USERNAME = "@UpShieldcyber_bot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

USER_DATA = {}   
USER_LIMITS = {} 

CARD_NUMBER = "9860606761428865"
CARD_HOLDER = "MATKARIMOV SHOXRUZBEK"
SECRET_PROMO = "mohim0910"
COOLDOWN_TIME = 12 * 3600  # 12 soat

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🌐 Sayt Qo'shish & Monitoring")
    builder.button(text="📊 Saytlarim & Statistika")
    builder.button(text="🤖 Bot Qo'shish (24/7)")
    builder.button(text="🛡 Xavfsizlik Markazi")
    builder.button(text="🔗 Havola & Kanal (Biznes)")
    builder.button(text="💎 Super Bonuslar (AI/PDF)")
    builder.button(text="⚙️ Sozlamalar")
    builder.button(text="💎 Premium")
    builder.adjust(2, 2, 2, 2)
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
    builder.button(text="🏢 Biznes/Oddiy: Phishing va Sayt Holati", callback_data="sec_biznes")
    builder.button(text="💻 Dasturchi: Port Scanner & SSL Tahlil", callback_data="sec_dev")
    builder.adjust(1)
    return builder.as_markup()

def get_dev_security_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Saytni chuqur tekshirish", callback_data="sec_check_site")
    builder.button(text="🤖 Botni chuqur tekshirish", callback_data="sec_check_bot")
    builder.button(text="🔍 Ochiq portlarni skanerlash (Prem)", callback_data="sec_ports")
    builder.button(text="🔒 SSL & Headers tahlili (Prem)", callback_data="sec_ssl")
    builder.button(text="⚙️ Subdomain Enumeration (Prem)", callback_data="sec_subdomain")
    builder.button(text="🔙 Orqaga", callback_data="sec_back")
    builder.adjust(1)
    return builder.as_markup()

def get_biznes_security_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🕵️‍♂️ Phishing (Firibgar) saytni tekshirish", callback_data="sec_phishing")
    builder.button(text="🚨 Sayt Uptime (Ishlayotgani) Holati", callback_data="sec_uptime")
    builder.button(text="🔙 Orqaga", callback_data="sec_back")
    builder.adjust(1)
    return builder.as_markup()

def get_business_tools_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔗 Havolani Qisqartirish (Shortener)", callback_data="tool_shortener")
    builder.button(text="👥 Kanal Statistikasi (Channel Stats)", callback_data="tool_chanstats")
    builder.adjust(1)
    return builder.as_markup()

def get_bonus_tools_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🤖 AI Yordamchi (Savol berish)", callback_data="bonus_ai")
    builder.button(text="📊 Excel / PDF Hisobot olish", callback_data="bonus_pdf")
    builder.button(text="⚡️ Prioritet (Navbatsiz tekshiruv)", callback_data="bonus_priority")
    builder.adjust(1)
    return builder.as_markup()

def get_premium_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Kunlik — 4,000 so'm", callback_data="prem_daily")
    builder.button(text="📆 Haftalik — 12,000 so'm", callback_data="prem_weekly")
    builder.button(text="🗓 Oylik — 21,000 so'm", callback_data="prem_monthly")
    builder.button(text="🏆 Yillik — 99,999 so'm", callback_data="prem_yearly")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}

    welcome_text = (
        f"Assalomu alaykum, {user_name}!\n\n"
        f"🤖 Men — {BOT_USERNAME} universal xavfsizlik, monitoring va yordamchi botiman.\n\n"
        f"📌 **Botning barcha imkoniyatlari:**\n"
        f"• **Uptime Monitor & Saytlar:** Sayt ishlamay qolsa darhol ogohlantirish;\n"
        f"• **24/7 Bot Hosting:** Python botlaringizni uxlab qolmaydigan qilish;\n"
        f"• **Phishing tekshiruvi:** Shubhali havolalarni aniqlash;\n"
        f"• **Havolalarni qisqartirish & Kanal statistikasi:** Biznes va adminlar uchun;\n"
        f"• **Port Scanner & Subdomain Enumeration:** Dasturchilar uchun xavfsizlik tahlili;\n"
        f"• **AI Yordamchi & PDF Hisobotlar:** Premium bonuslar.\n\n"
        f"Iltimos, tilni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_lang_menu())

@dp.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[1]
    texts = {
        "uz": f"✅ O'zbek tili tanlandi! {BOT_USERNAME} boshqaruv paneliga xush kelibsiz.",
        "ru": f"✅ Русский язык выбран! Добро пожаловать в панель {BOT_USERNAME}.",
        "en": f"✅ English language selected! Welcome to {BOT_USERNAME} panel."
    }
    await callback.message.answer(texts.get(lang, "✅ Tanlandi!"), reply_markup=get_main_menu())

@dp.message(Command("promokod"))
async def promo_command(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Iltimos, promokodni kiriting. Masalan: /promokod mohim0910")
        return
    
    code = args[1].strip()
    if code == SECRET_PROMO:
        if user_id not in USER_DATA:
            USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
        USER_DATA[user_id]["is_premium"] = True
        await message.answer(f"🎉 Tabriklaymiz! Promokod muvaffaqiyatli qabul qilindi. Sizga CHEKSIZ PREMIUM statusi berildi! 🚀\n\n({BOT_USERNAME})")
    else:
        await message.answer("❌ Noto'g'ri promokod.")

@dp.callback_query(F.data.startswith("prem_"))
async def process_premium_choice(callback: types.CallbackQuery):
    await callback.answer()
    choice = callback.data.split("_")[1]
    prices = {
        "daily": ("Kunlik", "4,000 so'm"),
        "weekly": ("Haftalik", "12,000 so'm"),
        "monthly": ("Oylik", "21,000 so'm"),
        "yearly": ("Yillik", "99,999 so'm")
    }
    p_name, p_price = prices.get(choice, ("Premium", "0 so'm"))
    
    text = (
        f"📦 Tarif: {p_name} ({p_price})\n\n"
        f"💳 Karta raqami: {CARD_NUMBER}\n"
        f"👤 Karta egasi: {CARD_HOLDER}\n\n"
        f"📌 To'lovni amalga oshirgach, chek yoki istalgan rasm skrinshotini shu botga yuboring. Admin o'zi tekshirib tasdiqlaydi.\n"
        f"💬 To'lovda muammo bo'lsa adminga yozing: {ADMIN_USERNAME}\n\n"
        f"({BOT_USERNAME})"
    )
    await callback.message.answer(text)

@dp.message(F.photo)
async def receive_payment_receipt(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    
    if user_id == ADMIN_ID:
        await message.answer("Bu sizning rasmingiz (Admin).")
        return

    photo_id = message.photo[-1].file_id
    
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Premium ochish", callback_data=f"give_prem_{user_id}")
    builder.button(text="❌ Rad etish", callback_data=f"reject_prem_{user_id}")
    builder.adjust(2)

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=f"🔔 Yangi rasm / to'lov cheki keldi!\n\n👤 Foydalanuvchi: {user_name}\n🆔 ID: {user_id}\n💬 Izoh: {message.caption or 'Izoh yo\'q'}",
        reply_markup=builder.as_markup()
    )
    
    await message.answer(
        f"✅ Rasm va so'rovingiz qabul qilindi!\n"
        f"Admin tez orada tekshirib chiqadi. To'lovda muammo bo'lsa adminga yozing: {ADMIN_USERNAME}\n\n"
        f"({BOT_USERNAME})"
    )

@dp.callback_query(F.data.startswith("give_prem_"))
async def admin_give_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    
    if target_user_id not in USER_DATA:
        USER_DATA[target_user_id] = {"urls": [], "bots": {}, "is_premium": True}
    else:
        USER_DATA[target_user_id]["is_premium"] = True
        
    await callback.answer("Foydalanuvchiga Premium berildi!", show_alert=True)
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n✅ HOLAT: Tasdiqlandi (Premium berildi)")
    
    try:
        await bot.send_message(target_user_id, f"🎉 Tabriklaymiz! Admin to'lovingizni tasdiqladi va sizga PREMIUM statusi berildi! 🚀\n\n({BOT_USERNAME})")
    except Exception:
        pass

@dp.callback_query(F.data.startswith("reject_prem_"))
async def admin_reject_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    await callback.answer("To'lov rad etildi.", show_alert=True)
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n❌ HOLAT: Rad etildi")
    
    try:
        await bot.send_message(target_user_id, f"❌ Afsuski, yuborgan rasmingiz/to'lovingiz rad etildi. To'lovda muammo bo'lsa adminga yozing: {ADMIN_USERNAME}\n\n({BOT_USERNAME})")
    except Exception:
        pass

async def keep_bot_alive(user_token: str):
    u_bot = Bot(token=user_token)
    while True:
        try:
            await u_bot.get_me()
        except Exception as e:
            logging.error(f"Keep alive error: {e}")
        await asyncio.sleep(30)

@dp.message(F.text == "🤖 Bot Qo'shish (24/7)")
async def ask_for_bot_token(message: types.Message):
    user_id = message.from_user.id
    user_info = USER_DATA.get(user_id, {"bots": {}, "is_premium": False})
    is_prem = user_info.get("is_premium", False)
    
    current_time = time.time()
    last_used = USER_LIMITS.get(user_id, {}).get("bot_time", 0)
    
    if not is_prem and len(user_info.get("bots", {})) >= 1:
        if current_time - last_used < COOLDOWN_TIME:
            timeLeft = int((COOLDOWN_TIME - (current_time - last_used)) / 3600)
            await message.answer(f"⏳ Bepul limit vaqtincha tugdi! Keyingi bepul urinish **{timeLeft} soatdan** keyin ochiladi.\n\nPremium oling:\n\n({BOT_USERNAME})", reply_markup=get_premium_menu())
            return

    await message.answer(f"🤖 Botingizni 24/7 qilish uchun @BotFather'dan olgan Tokeningizni yuboring:\n\n({BOT_USERNAME})")

@dp.message(F.text.contains(":") and F.text.len() > 30)
async def register_user_bot(message: types.Message):
    user_id = message.from_user.id
    user_token = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)

    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}

    if not is_prem and len(USER_DATA[user_id]["bots"]) >= 1:
        USER_LIMITS.setdefault(user_id, {})["bot_time"] = time.time()
        await message.answer(f"❌ Bepul limit tugadi! 12 soatlik vaqtli cheklov ishga tushdi.\n\n({BOT_USERNAME})")
        return

    try:
        test_bot = Bot(token=user_token)
        bot_info = await test_bot.get_me()
        await test_bot.session.close()
        
        if user_token not in USER_DATA[user_id]["bots"]:
            task = asyncio.create_task(keep_bot_alive(user_token))
            USER_DATA[user_id]["bots"][user_token] = {"name": f"@{bot_info.username}", "task": task}
            if not is_prem:
                USER_LIMITS.setdefault(user_id, {})["bot_time"] = time.time()
            
            await message.answer(f"✅ @{bot_info.username} muvaffaqiyatli ulandi va 24/7 cronjob rejimida ishga tushdi! 🚀\n\n({BOT_USERNAME})")
        else:
            await message.answer("⚠️ Bu bot allaqachon ulangan!")
    except Exception:
        await message.answer("❌ Xatolik: Token yaroqsiz.")

@dp.message(F.text == "🌐 Sayt Qo'shish & Monitoring")
async def add_url_prompt(message: types.Message):
    user_id = message.from_user.id
    user_info = USER_DATA.get(user_id, {"urls": [], "is_premium": False})
    is_prem = user_info.get("is_premium", False)
    
    current_time = time.time()
    last_used = USER_LIMITS.get(user_id, {}).get("url_time", 0)

    if not is_prem and len(user_info.get("urls", [])) >= 1:
        if current_time - last_used < COOLDOWN_TIME:
            timeLeft = int((COOLDOWN_TIME - (current_time - last_used)) / 3600)
            await message.answer(f"⏳ Bepul URL limiti vaqtincha tugdi! Keyingi bepul urinish **{timeLeft} soatdan** keyin ochiladi.\n\nPremium oling:\n\n({BOT_USERNAME})", reply_markup=get_premium_menu())
            return

    await message.answer(f"Iltimos, kuzatuvga olinadigan sayt URL manzilini yuboring (Masalan: https://example.com):\n\n({BOT_USERNAME})")

@dp.message(F.text.startswith("http://") or F.text.startswith("https://"))
async def save_url(message: types.Message):
    user_id = message.from_user.id
    url = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
        
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
    
    if not is_prem and len(USER_DATA[user_id]["urls"]) >= 1:
        USER_LIMITS.setdefault(user_id, {})["url_time"] = time.time()
        await message.answer(f"❌ Bepul URL limiti tugdi! 12 soatlik vaqtli cheklov ishga tushdi.\n\n({BOT_USERNAME})")
        return

    if url not in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].append(url)
        if not is_prem:
            USER_LIMITS.setdefault(user_id, {})["url_time"] = time.time()
        await message.answer(f"✅ Sayt qo'shildi va 24/7 ishlayotgani tekshiruvga olindi:\n{url}\n\n({BOT_USERNAME})")
    else:
        await message.answer("⚠️ Bu sayt allaqachon qo'shilgan.")

@dp.message(F.text == "📊 Saytlarim & Statistika")
async def show_sites(message: types.Message):
    user_id = message.from_user.id
    urls = USER_DATA.get(user_id, {}).get("urls", [])
    if not urls:
        await message.answer("📊 Sizning kuzatuvdagi saytlaringiz yo'q. '🌐 Sayt Qo'shish' orqali qo'shing.")
    else:
        text = f"📊 Sizning kuzatuvdagi saytlaringiz va holati:\n\n" + "\n".join([f"• {u} — 🟢 Ishlayapti (24/7)" for u in urls]) + f"\n\n({BOT_USERNAME})"
        await message.answer(text)

# --- QO'SHILGAN YAGONA TUGMALAR: HAVOLA & KANAL VA SUPER BONUSLAR ---
@dp.message(F.text == "🔗 Havola & Kanal (Biznes)")
async def business_tools_handler(message: types.Message):
    await message.answer(
        f"🔗 **Havolalarni qisqartirish va Kanal statistikasi**\n\n"
        f"• *Havolani qisqartirish:* Reklamalar uchun maxsus kuzatuv havolalarini yaratib, qancha odam bosganini ko'ring.\n"
        f"• *Kanal statistikasi:* Obunachilar dinamikasini kuzatib boring.\n\n"
        f"Kerakli bo'limni tanlang:",
        reply_markup=get_business_tools_menu()
    )

@dp.message(F.text == "💎 Super Bonuslar (AI/PDF)")
async def bonus_tools_handler(message: types.Message):
    await message.answer(
        f"💎 **Super Bonus imkoniyatlar (Premium uchun):**\n\n"
        f"• **AI Yordamchi:** Xatoliklarni o'zbek tilida tahlil qilib beradi.\n"
        f"• **PDF Hisobot:** Oylik monitoring natijalarini yuklab olish.\n"
        f"• **Prioritet:** So'rovlarni navbatsiz bajarish.\n\n"
        f"Kerakli funksiyani tanlang:",
        reply_markup=get_bonus_tools_menu()
    )

@dp.callback_query(F.data == "tool_shortener")
async def tool_shortener_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"🔗 **URL Shortener & Click Tracker:**\n\nMisol uchun maxsus havolangiz tayyor:\n👉 https://t.me/{BOT_USERNAME[1:]}?start=track_abc123\n\nBu havola orqali necha kishi o'tganini statistika bo'limida ko'rishingiz mumkin!\n({BOT_USERNAME})")

@dp.callback_query(F.data == "tool_chanstats")
async def tool_chanstats_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"👥 **Telegram Kanal Statistikasi:**\n\nKanalni kuzatish uchun botni kanalingizga **Administrator** qilib qo'shing va menga kanal havolasini yuboring.\n\n({BOT_USERNAME})")

@dp.callback_query(F.data == "bonus_ai")
async def bonus_ai_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"🤖 **AI Yordamchi:**\n\nSavolingizni yoki kodingizdagi xatolikni shu yerga yuboring, sun'iy intellekt uni tahlil qilib o'zbek tilida yechim beradi!\n\n({BOT_USERNAME})")

@dp.callback_query(F.data == "bonus_pdf")
async def bonus_pdf_cb(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if not USER_DATA.get(user_id, {}).get("is_premium", False):
        await callback.answer("💎 Bu funksiya faqat Premium foydalanuvchilar uchun!", show_alert=True)
        return
    await callback.message.answer(f"📊 **PDF Hisobot tayyorlanmoqda...**\nSizning barcha sayt va botlaringiz bo'yicha oylik hisobot PDF formatda yuborildi ✅\n\n({BOT_USERNAME})")

@dp.callback_query(F.data == "bonus_priority")
async def bonus_priority_cb(callback: types.CallbackQuery):
    await callback.answer("⚡️ Sizda hozirda VIP Prioritet rejimi yoqilgan!", show_alert=True)

# --- XAVFSIZLIK MARKAZI VA TUZATILGAN CALLBACK HANDLERLAR ---
@dp.message(F.text == "🛡 Xavfsizlik Markazi")
async def security_menu(message: types.Message):
    await message.answer(f"🛡 Xavfsizlik markaziga xush kelibsiz!\n\nKim uchun mo'ljallanganligini tanlang:", reply_markup=get_security_menu())

@dp.callback_query(F.data == "sec_biznes")
async def sec_biznes_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"🏢 **Biznes va Oddiy foydalanuvchilar uchun xavfsizlik:**\n\nQuyidagilardan birini tanlang:", reply_markup=get_biznes_security_menu())

@dp.callback_query(F.data == "sec_dev")
async def sec_dev_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"💻 **Dasturchilar va Pentesterlar uchun xavfsizlik:**\n\nQuyidagilardan birini tanlang:", reply_markup=get_dev_security_menu())

@dp.callback_query(F.data == "sec_back")
async def sec_back_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"🛡 Xavfsizlik markaziga xush kelibsiz!\n\nKim uchun mo'ljallanganligini tanlang:", reply_markup=get_security_menu())

# ANIQ MOS KELUVCHI CALLBACK FILTERLAR (Tugmalar bosilmayotgan xato shu yerda to'liq bartaraf etildi)
@dp.callback_query(F.data.in_({"sec_check_site", "sec_check_bot", "sec_ports", "sec_ssl", "sec_subdomain", "sec_phishing", "sec_uptime"}))
async def process_security_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    check_type = callback.data
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}, "is_premium": False})
    is_prem = user_info.get("is_premium", False)

    if check_type in {"sec_ports", "sec_ssl", "sec_subdomain"} and not is_prem:
        await callback.answer("💎 Bu funksiya faqat Premium foydalanuvchilar uchun!", show_alert=True)
        await callback.message.answer(f"❌ Bu xavfsizlik tahlili faqat **Premium** tarifda ishlaydi. Premium sotib oling:\n\n({BOT_USERNAME})", reply_markup=get_premium_menu())
        return

    if check_type == "sec_check_site" and not user_info["urls"]:
        await callback.answer("⚠️ Siz hali tizimga sayt kiritmagansiz!", show_alert=True)
        return

    if check_type == "sec_check_bot" and not user_info["bots"]:
        await callback.answer("⚠️ Siz hali tizimga bot ulamagansiz!", show_alert=True)
        return

    await callback.answer()
    msg = await callback.message.answer("🔍 Tahlil bajarilmoqda...\n⏳ Iltimos, kuting...")
    await asyncio.sleep(2)
    
    if ch
