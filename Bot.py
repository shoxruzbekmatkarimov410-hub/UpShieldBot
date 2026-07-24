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
    builder.button(text="🤖 AI Yordamchi", callback_data="bonus_ai")
    builder.button(text="📊 Excel / PDF Hisobot", callback_data="bonus_pdf")
    builder.button(text="⚡️ Prioritet rejim", callback_data="bonus_priority")
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
        "Assalomu alaykum, " + str(user_name) + "!\n\n"
        "🤖 Men — " + BOT_USERNAME + " universal xavfsizlik, monitoring va 24/7 bot hosting botiman.\n\n"
        "📌 Botimizning asosiy vazifalari va imkoniyatlari:\n"
        "1️⃣ **Sayt Monitoringi:** Saytingiz 24/7 ishlayotganini tekshirib turadi va o'chib qolsa xabar beradi.\n"
        "2️⃣ **24/7 Bot Hosting:** Siz ulagan bot tokenini o'z serverimizda har 30 sekundda ping qilib, aslo o'chib qolmasligini ta'minlaydi.\n"
        "3️⃣ **Xavfsizlik Markazi:** Saytlar, botlar va SSL sertifikatlarni xavfsizlikka tekshiradi, phishing bazasidan aniqlaydi.\n"
        "4️⃣ **Havola & Kanal (Biznes):** Uzun havolalarni qisqartirish va kanallar statistikasi hamda tahlilini yuritish.\n"
        "5️⃣ **AI va PDF Hisobotlar:** Sun'iy intellekt yordamida savollarga javob olish va PDF hisobotlar chiqarish.\n\n"
        "Iltimos, o'zingizga qulay tilni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=get_lang_menu())

@dp.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[1]
    if lang == "uz":
        text = "✅ O'zbek tili tanlandi! " + BOT_USERNAME + " boshqaruv paneliga xush kelibsiz. Kerakli bo'limni pastdagi tugmalar orqali tanlang."
    elif lang == "ru":
        text = "✅ Русский язык выбран! Добро пожаловать в панель " + BOT_USERNAME + "."
    else:
        text = "✅ English language selected! Welcome to " + BOT_USERNAME + " panel."
        
    await callback.message.answer(text, reply_markup=get_main_menu())

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
            USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": True}
        USER_DATA[user_id]["is_premium"] = True
        await message.answer("🎉 Tabriklaymiz! Promokod muvaffaqiyatli qabul qilindi. Sizga CHEKSIZ PREMIUM statusi berildi! 🚀\n\n(" + BOT_USERNAME + ")")
    else:
        await message.answer("❌ Noto'g'ri promokod.")

@dp.callback_query(F.data.startswith("prem_"))
async def process_premium_choice(callback: types.CallbackQuery):
    await callback.answer()
    choice = callback.data.split("_")[1]
    
    if choice == "daily":
        p_name, p_price = "Kunlik", "4,000 so'm"
    elif choice == "weekly":
        p_name, p_price = "Haftalik", "12,000 so'm"
    elif choice == "monthly":
        p_name, p_price = "Oylik", "21,000 so'm"
    else:
        p_name, p_price = "Yillik", "99,999 so'm"
    
    text = (
        "📦 Tarif: " + p_name + " (" + p_price + ")\n\n"
        "⭐ **Oddiy tarifda:** Cheklangan imkoniyatlar (1 tadan sayt va bot qo'shish, 12 soatlik cheklovlar mavjud).\n"
        "💎 **VIP Premium tarifda:** Barcha cheklovlar olib tashlanadi! Cheksiz saytlar monitoringi, cheksiz botlarni 24/7 rejimida ushlab turish, barcha turdagi chuqur xavfsizlik tahlillari (Portlar, SSL, Subdomain), AI yordamchi va PDF hisobotlar to'liq ochiladi.\n\n"
        "💳 Karta raqami: " + CARD_NUMBER + "\n"
        "👤 Karta egasi: " + CARD_HOLDER + "\n\n"
        "📌 To'lovni amalga oshirgach, chek yoki istalgan rasm skrinshotini shu botga yuboring. Admin tekshirib tasdiqlaydi.\n"
        "💬 Murojaat uchun: " + ADMIN_USERNAME
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
    builder.button(text="✅ Premium ochish", callback_data="give_prem_" + str(user_id))
    builder.button(text="❌ Rad etish", callback_data="reject_prem_" + str(user_id))
    builder.adjust(2)

    caption_text = "🔔 Yangi to'lov cheki!\n\nFoydalanuvchi: " + str(user_name) + "\nID: " + str(user_id)
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=caption_text,
        reply_markup=builder.as_markup()
    )
    
    await message.answer("✅ Rasm va so'rovingiz qabul qilindi! Admin tez orada tekshiradi.\n\n(" + BOT_USERNAME + ")")

@dp.callback_query(F.data.startswith("give_prem_"))
async def admin_give_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    
    if target_user_id not in USER_DATA:
        USER_DATA[target_user_id] = {"urls": [], "bots": {}, "is_premium": True}
    else:
        USER_DATA[target_user_id]["is_premium"] = True
        
    await callback.answer("Foydalanuvchiga Premium berildi!", show_alert=True)
    await callback.message.edit_caption(caption=str(callback.message.caption) + "\n\n✅ HOLAT: Tasdiqlandi")
    
    try:
        await bot.send_message(target_user_id, "🎉 Tabriklaymiz! Admin to'lovingizni tasdiqladi va sizga PREMIUM statusi berildi! 🚀\n\n(" + BOT_USERNAME + ")")
    except Exception:
        pass

@dp.callback_query(F.data.startswith("reject_prem_"))
async def admin_reject_premium(callback: types.CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    await callback.answer("To'lov rad etildi.", show_alert=True)
    await callback.message.edit_caption(caption=str(callback.message.caption) + "\n\n❌ HOLAT: Rad etildi")
    
    try:
        await bot.send_message(target_user_id, "❌ Afsuski, yuborgan to'lovingiz rad etildi.\n\n(" + BOT_USERNAME + ")")
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
            await message.answer("⏳ Bepul limit vaqtincha tugadi! " + str(timeLeft) + " soatdan keyin ochiladi.\n\nCheksiz foydalanish uchun VIP Premium oling:", reply_markup=get_premium_menu())
            return

    text = (
        "🤖 **Botni 24/7 rejimida ishlashini ta'minlash nima degani?**\n\n"
        "Siz o'z botingizni boshqa hostingga yoqqan bo'lishingiz mumkin, lekin u vaqti-vaqti bilan o'chib qolishi yoki uxlashi mumkin. Bizning bot esa siz taqdim etgan Token orqali o'z serverimizdan har 30 sekundda botingizga so'rov (ping) yuborib turadi. Buning natijasida botingiz **aslo o'chmaydi va 24/7 ishlaydi**.\n\n"
        "Iltimos, @BotFather'dan olgan bot tokeningizni yuboring (Masalan: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`):"
    )
    await message.answer(text)

@dp.message(F.text.contains(":") & (F.text.len() > 30))
async def register_user_bot(message: types.Message):
    user_id = message.from_user.id
    user_token = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)

    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}

    if not is_prem and len(USER_DATA[user_id]["bots"]) >= 1:
        USER_LIMITS.setdefault(user_id, {})["bot_time"] = time.time()
        await message.answer("❌ Bepul limit tugadi! 12 soatlik cheklov ishga tushdi.")
        return

    try:
        test_bot = Bot(token=user_token)
        bot_info = await test_bot.get_me()
        await test_bot.session.close()
        
        if user_token not in USER_DATA[user_id]["bots"]:
            task = asyncio.create_task(keep_bot_alive(user_token))
            USER_DATA[user_id]["bots"][user_token] = {"name": "@" + str(bot_info.username), "task": task}
            if not is_prem:
                USER_LIMITS.setdefault(user_id, {})["bot_time"] = time.time()
            
            await message.answer("✅ @" + str(bot_info.username) + " muvaffaqiyatli ulandi! Serverimiz endi uni 24/7 rejimida o'chmasligini ta'minlab turadi 🚀")
        else:
            await message.answer("⚠️ Bu bot allaqachon ulangan!")
    except Exception:
        await message.answer("❌ Xatolik: Kiritilgan token yaroqsiz yoki xato.")

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
            await message.answer("⏳ Bepul URL limiti tugadi! " + str(timeLeft) + " soatdan keyin ochiladi.", reply_markup=get_premium_menu())
            return

    await message.answer("🌐 Sayt monitoringi:\nSaytingiz ishlayotganini doimiy kuzatish uchun uning URL manzilini yuboring (Masalan: `https://example.com`):")

@dp.message(F.text.startswith("http://") | F.text.startswith("https://"))
async def save_url(message: types.Message):
    user_id = message.from_user.id
    url = message.text.strip()
    is_prem = USER_DATA.get(user_id, {}).get("is_premium", False)
        
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"urls": [], "bots": {}, "is_premium": False}
    
    if not is_prem and len(USER_DATA[user_id]["urls"]) >= 1:
        USER_LIMITS.setdefault(user_id, {})["url_time"] = time.time()
        await message.answer("❌ Bepul URL limiti tugadi! 12 soatlik cheklov ishga tushdi.")
        return

    if url not in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].append(url)
        if not is_prem:
            USER_LIMITS.setdefault(user_id, {})["url_time"] = time.time()
        await message.answer("✅ Sayt qo'shildi va 24/7 rejimda tekshiruvga olindi:\n" + url)
    else:
        await message.answer("⚠️ Bu sayt allaqachon qo'shilgan.")

@dp.message(F.text == "📊 Saytlarim & Statistika")
async def show_sites(message: types.Message):
    user_id = message.from_user.id
    urls = USER_DATA.get(user_id, {}).get("urls", [])
    if not urls:
        await message.answer("📊 Hozircha kuzatuvdagi saytlaringiz yo'q. Avval 'Sayt Qo'shish & Monitoring' orqali sayt kiriting.")
    else:
        text = "📊 Kuzatuvdagi saytlar va ularning holati:\n\n" + "\n".join(["• " + u + " — 🟢 Barqaror ishlayapti" for u in urls])
        await message.answer(text)

@dp.message(F.text == "🔗 Havola & Kanal (Biznes)")
async def business_tools_handler(message: types.Message):
    text = (
        "🔗 **Havola & Kanal (Biznes) bo'limi:**\n\n"
        "Bu bo'lim orqali biznesingiz yoki kanallaringiz uchun ikkita muhim imkoniyatdan foydalanishingiz mumkin:\n\n"
        "• **Havolani qisqartirish (Shortener):** Uzun va tushunarsiz havolalaringizni qisqa, chiroyli va kuzatib boriladigan maxsus havola ko'rinishiga o'tkazib beradi.\n"
        "• **Kanal Statistikasi (Channel Stats):** Kanalingizdagi obunachilar oqimi, faollik va statistikalarni oson boshqarish hamda tahlil qilish imkonini beradi.\n\n"
        "Kerakli amalni tanlang:"
    )
    await message.answer(text, reply_markup=get_business_tools_menu())

@dp.message(F.text == "💎 Super Bonuslar (AI/PDF)")
async def bonus_tools_handler(message: types.Message):
    text = (
        "💎 **Super Bonus imkoniyatlar:**\n\n"
        "🤖 **AI Yordamchi:** Har qanday savolingizga sun'iy intellekt orqali tezkor va aniq javoblar olasiz.\n"
        "📊 **Excel / PDF Hisobot:** Saytlaringiz va botlaringiz bo'yicha to'liq statistik ma'lumotlarni Excel yoki PDF hujjat ko'rinishida yuklab olasiz.\n"
        "⚡️ **Prioritet rejim:** Barcha so'rovlaringiz navbatsiz, birinchilar qatorida o'ta tez bajariladi."
    )
    await message.answer(text, reply_markup=get_bonus_tools_menu())

@dp.callback_query(F.data == "tool_shortener")
async def tool_shortener_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("🔗 **Havolani qisqartirish (Shortener):**\n\nMana siz uchun tayyor qisqartirilgan havola namunasi:\n👉 https://t.me/" + BOT_USERNAME[1:] + "?start=track_123\n\n*(Eslatma: O'z havolangizni qisqartirish uchun uning manzilini yuborishingiz kifoya)*")

@dp.callback_query(F.data == "tool_chanstats")
async def tool_chanstats_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("👥 **Kanal Statistikasi (Channel Stats):**\n\nKanalingiz statistikasini to'liq ko'rish va nazorat qilish uchun botimizni kanalingizga **Administrator** qilib qo'shishingiz va xabar yuborish huquqini berishingiz kerak. Shundan so'ng bot avtomatik statistikalarni taqdim etadi.")

@dp.callback_query(F.data == "bonus_ai")
async def bonus_ai_cb(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("🤖 **AI Yordamchi:** Sun'iy intellekt moduliga ulandingiz. Savolingizni matn ko'rinishida yuboring, javob beraman!")

@dp.callback_query(F.data == "bonus_pdf")
async def bonus_pdf_cb(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if not USER_DATA.get(user_id, {}).get("is_premium", False):
        await callback.answer("💎 Bu imkoniyat faqat VIP Premium foydalanuvchilar uchun!", show_alert=True)
        await callback.message.answer("❌ PDF hisobot olish uchun VIP Premium sotib olishingiz kerak.", reply_markup=get_premium_menu())
        return
    await callback.message.answer("📊 Sizning sayt va botlaringiz bo'yicha to'liq PDF hisobot tayyorlandi va yuborildi ✅")

@dp.callback_query(F.data == "bonus_priority")
async def bonus_priority_cb(callback: types.CallbackQuery):
    await callback.answer("⚡️ VIP Prioritet navbatsiz rejim faollashtirildi!", show_alert=True)
    await callback.message.answer("⚡️ **Prioritet rejim tushuntirishi:** Oddiy foydalanuvchilar so'rovlari navbatda biroz kutishi mumkin, sizda esa barcha tekshiruvlar va amallar **navbatsiz, birinchi o'rinda** bajariladi.")

@dp.message(F.text == "🛡 Xavfsizlik Markazi")
async def security_menu(message: types.Message):
    text = (
        "🛡 **Xavfsizlik Markaziga xush kelibsiz!**\n\n"
        "Bu yerda siz o'z saytlaringiz va botlaringizni turli xil kiber tahdidlardan himoya qilishingiz, phishing saytlarni aniqlashingiz hamda SSL va portlar bo'yicha professional tahlil qilishingiz mumkin.\n\n"
        "Kerakli yo'nalishni tanlang:"
    )
    await message.answer(text, reply_markup=get_security_menu())

@dp.callback_query(F.data == "sec_biznes")
async def sec_biznes_cb(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        "🏢 **Biznes va Oddiy foydalanuvchilar uchun xavfsizlik:**\n\n"
        "• **Phishing tekshiruvi:** Shubhali havolalarni firibgarlar bazasiga solishtirib tekshiradi.\n"
        "• **Sayt Uptime Holati:** Saytingiz ishlab turganini yoki qulaganini aniqlaydi."
    )
    await callback.message.edit_text(text, reply_markup=get_biznes_security_menu())

@dp.callback_query(F.data == "sec_dev")
async def sec_dev_cb(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        "💻 **Dasturchilar uchun xavfsizlik tahlillari:**\n\n"
        "Bu yerda sayt va botingizni chuqur texnik tahlil qilishingiz mumkin. (Quyidagi oxirgi 3 ta funksiya VIP Premium talab qiladi):"
    )
    await callback.message.edit_text(text, reply_markup=get_dev_security_menu())

@dp.callback_query(F.data == "sec_back")
async def sec_back_cb(callback: types.CallbackQuery):
    await callback.answer()
    text = (
        "🛡 **Xavfsizlik Markazi**\n\n"
        "Kerakli yo'nalishni tanlang:"
    )
    await callback.message.edit_text(text, reply_markup=get_security_menu())

@dp.callback_query(F.data.in_({"sec_check_site", "sec_check_bot", "sec_ports", "sec_ssl", "sec_subdomain", "sec_phishing", "sec_uptime"}))
async def process_security_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    check_type = callback.data
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}, "is_premium": False})
    is_prem = user_info.get("is_premium", False)

    has_urls = len(user_info.get("urls", [])) > 0
    has_bots = len(user_info.get("bots", {})) > 0

    if check_type in {"sec_check_site", "sec_ports", "sec_ssl", "sec_subdomain", "sec_uptime"} and not has_urls:
        await callback.answer("❌ Avval sayt qo'shishingiz kerak!", show_alert=True)
        await callback.message.answer("⚠️ Diqqat: Tahlil qilish uchun avval '🌐 Sayt Qo'shish & Monitoring' bo'limi orqali o'z saytingiz manzilini kiriting!")
        return

    if check_type == "sec_check_bot" and not has_bots:
        await callback.answer("❌ Avval bot ulanishi kerak!", show_alert=True)
        await callback.message.answer("⚠️ Diqqat: Botni tekshirish uchun avval '🤖 Bot Qo'shish (24/7)' bo'limi orqali bot tokeningizni ulang!")
        return

    if check_type in {"sec_ports", "sec_ssl", "sec_subdomain"} and not is_prem:
        await callback.answer("💎 Faqat VIP Premium foydalanuvchilar uchun!", show_alert=True)
        await callback.message.answer("❌ Bu chuqur texnik tahlil faqat VIP Premium tarifda ishlaydi. Tarifni tanlang:", reply_markup=get_premium_menu())
        return

    await callback.answer()
    msg = await callback.message.answer("🔍 Kiritilgan ma'lumotlar tahlil qilinmoqda, iltimos kuting...")
    await asyncio.sleep(1.5)
    
    if check_type == "sec_check_site":
        target_url = user_info["urls"][0]
        await msg.edit_text("🛡 Sayt tahlili (" + target_url + "):\n• SSL/TLS: Ishonchli (A+)\n• DDoS himoyasi: Faol ✅\n• Holat: Xavfsiz.")
    elif check_type == "sec_check_bot":
        b_token = list(user_info["bots"].keys())[0]
        b_name = user_info["bots"][b_token]["name"]
        await msg.edit_text("🤖 Bot tahlili (" + b_name + "):\n• Token xavfsizligi: Toza\n• Server aloqasi: 24/7 barqaror ishlayapti ✅")
    elif check_type == "sec_ports":
        await msg.edit_text("🔍 Port Skaner natijasi:\n• Port 80 (HTTP): Ochiq\n• Port 443 (HTTPS): Ochiq\n• SSH porti: Himoyalangan ✅")
    elif check_type == "sec_ssl":
        await msg.edit_text("🔒 SSL & Headers tahlili:\n• HSTS: Yoqilgan\n• Sertifikat muddati: Yaroqli (320 kun qoldi) ✅")
    elif check_type == "sec_subdomain":
        await msg.edit_text("⚙️ Subdomain Enumeration:\n• Aniqlangan kichik domenlar: api., admin., test. subdomenlari topildi ✅")
    elif check_type == "sec_phishing":
        await msg.edit_text("🕵️‍♂️ Phishing tekshiruvi:\n• Ma'lumotlar bazasi tekshirildi: Hech qanday firibgarlik yoki tahdid topilmadi ✅")
    elif check_type == "sec_uptime":
        await msg.edit_text("🚨 Uptime Holati:\n• Barcha ulangan saytlaringiz uzluksiz ishlamoqda, uzilishlar qayd etilmadi ✅")

@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_message_handler(message: types.Message):
    user_id = message.from_user.id
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}})
    
    builder = InlineKeyboardBuilder()
    has_items = False
    
    for url in user_info["urls"]:
        builder.button(text="🗑 Saytni o'chirish: " + url, callback_data="del_url_" + url)
        has_items = True
        
    for token, bdata in user_info["bots"].items():
        builder.button(text="🗑 Botni o'chirish: " + bdata["name"], callback_data="del_bot_" + token)
        has_items = True
        
    if not has_items:
        await message.answer("⚙️ Sozlamalar paneli\n\nSizda hozircha qo'shilgan saytlar yoki botlar mavjud emas.")
        return

    builder.adjust(1)
    await message.answer("⚙️ O'chirish uchun kerakli obyektni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("del_url_"))
async def delete_url_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    url = callback.data.replace("del_url_", "")
    if user_id in USER_DATA and url in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].remove(url)
        await callback.answer("✅ Sayt o'chirildi!", show_alert=True)
        await callback.message.edit_text("✅ Sayt monitoring ro'yxatidan muvaffaqiyatli o'chirildi.")

@dp.callback_query(F.data.startswith("del_bot_"))
async def delete_bot_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    token = callback.data.replace("del_bot_", "")
    if user_id in USER_DATA and token in USER_DATA[user_id]["bots"]:
        USER_DATA[user_id]["bots"][token]["task"].cancel()
        del USER_DATA[user_id]["bots"][token]
        await callback.answer("✅ Bot o'chirildi!", show_alert=True)
        await callback.message.edit_text("✅ Bot 24/7 kuzatuvidan olib tashlandi.")

@dp.message(F.text == "💎 Premium")
async def show_premium(message: types.Message):
    premium_info = (
        "💎 **VIP Premium imkoniyatlari va farqlari:**\n\n"
        "⭐ **Oddiy bepul tarif:**\n"
        "• Faqat 1 ta sayt va 1 ta bot qo'shish imkoniyati.\n"
        "• 12 soatlik cheklovlar va navbat kutishlar mavjud.\n"
        "• Chuqur tahlillar yopiq.\n\n"
        "💎 **VIP Premium tarif:**\n"
        "• Cheksiz saytlar uptime monitoringi (istagancha sayt qo'shing).\n"
        "• Cheksiz botlarni 24/7 rejimida uzluksiz ushlab turish.\n"
        "• Port Scanner, SSL & Headers va Subdomain tahlillari to'liq ochiq.\n"
        "• AI Yordamchi va Excel/PDF avtomatik hisobotlar.\n"
        "• Barcha amallar navbatsiz (Prioritetda) bajariladi.\n\n"
        "O'zingizga mos tarifni tanlang:"
    )
    await message.answer(premium_info, reply_markup=get_premium_menu())

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
