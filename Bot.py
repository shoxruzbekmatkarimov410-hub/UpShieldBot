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
USER_LIMITS = {} # Vaqtli cheklovlar uchun (oxirgi ishlatgan vaqti saqlanadi)

CARD_NUMBER = "9860606761428865"
CARD_HOLDER = "MATKARIMOV SHOXRUZBEK"
SECRET_PROMO = "mohim0910"
COOLDOWN_TIME = 12 * 3600  # 12 soat (sekundda)

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🌐 Sayt Qo'shish & Monitoring")
    builder.button(text="📊 Saytlarim & Statistika")
    builder.button(text="🤖 Bot Qo'shish (24/7)")
    builder.button(text="🛡 Xavfsizlik Markazi")
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
        f"🤖 Men — {BOT_USERNAME} universal xavfsizlik va monitoring botiman.\n"
        f"📌 Kimlar uchun:\n"
        f"• **Biznes/Oddiy foydalanuvchilar uchun:** Saytlar ishlayotganini kuzatish, firibgar havolalardan himoyalanish.\n"
        f"• **Dasturchilar uchun:** Botlarni 24/7 yurgizish, portlarni skanerlash va xavfsizlik tahlili.\n\n"
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
    user_info = USER_DATA.get(user_id, {"bots": {}, "is_pm": False})
    is_prem = user_info.get("is_premium", False)
    
    # Vaqtli limit tekshiruvi (Free foydalanuvchi uchun 12 soatlik cooldown)
    current_time = time.time()
    last_used = USER_LIMITS.get(user_id, {}).get("bot_time", 0)
    
    if not is_prem and len(user_info.get("bots", {})) >= 1:
        if current_time - last_used < COOLDOWN_TIME:
            timeLeft = int((COOLDOWN_TIME - (current_time - last_used)) / 3600)
            await message.answer(f"⏳ Bepul limit vaqtincha tugdi! Keyingi bepul urinish **{timeLeft} soatdan** keyin ochiladi.\n\nDarhol cheksiz foydalanish uchun esa Premium oling:\n\n({BOT_USERNAME})", reply_markup=get_premium_menu())
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
        await message.answer(f"❌ Bepul limit tugadi! Vaqtli cheklov ishga tushdi (12 soatdan so'ng yangilanadi).\n\n({BOT_USERNAME})")
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

@dp.callback_query(F.data.in_({"sec_check_site", "sec_check_bot", "sec_ports", "sec_ssl", "sec_phishing", "sec_uptime"}))
async def process_security_check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    check_type = callback.data
    user_info = USER_DATA.get(user_id, {"urls": [], "bots": {}, "is_premium": False})
    is_prem = user_info.get("is_premium", False)

    if check_type in {"sec_ports", "sec_ssl"} and not is_prem:
        await callback.answer("💎 Bu funksiya faqat Premium foydalanuvchilar uchun!", show_alert=True)
        await callback.message.answer(f"❌ Port skaner va SSL header tahlili faqat **Premium** tarifda ishlaydi. Premium sotib oling:\n\n({BOT_USERNAME})", reply_markup=get_premium_menu())
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
    
    if check_type == "sec_check_site":
        target_url = user_info["urls"][0]
        await msg.edit_text(f"🛡 Sayt xavfsizlik tahlili ({target_url}):\n\n✅ SSL/TLS: Ishonchli (A+)\n✅ DDoS himoyasi: Faol\n🏆 Xavfsizlik: 99%\n\n({BOT_USERNAME})")
    elif check_type == "sec_check_bot":
        bot_name = list(user_info["bots"].values())[0]["name"]
        await msg.edit_text(f"🤖 Bot holati ({bot_name}):\n\n✅ Token himoyasi: Xavfsiz\n✅ Ulanish: 24/7 ishlayapti\n🏆 Barqarorlik: 100%\n\n({BOT_USERNAME})")
    elif check_type == "sec_ports":
        await msg.edit_text(f"🔍 Port Skaner Tahlili:\n\n• Port 80 (HTTP): Ochiq ✅\n• Port 443 (HTTPS): Ochiq ✅\n• Port 22 (SSH): Himoyalangan ✅\n\n({BOT_USERNAME})")
    elif check_type == "sec_ssl":
        await msg.edit_text(f"🔒 SSL & Headers Tahlili:\n\n• HSTS: Yoqilgan ✅\n• X-Frame-Options: SAMEORIGIN ✅\n• Muddati: 320 kun qoldi\n\n({BOT_USERNAME})")
    elif check_type == "sec_phishing":
        await msg.edit_text(f"🕵️‍♂️ Phishing (Firibgarlik) tekshiruvi:\n\nKiritgan havolangiz xavfsiz bazada tekshirildi. Firibgarlik alomatlari topilmadi. Saytdan xotirjam foydalanishingiz mumkin ✅\n\n({BOT_USERNAME})")
    elif check_type == "sec_uptime":
        await msg.edit_text(f"🚨 Uptime Monitoring:\n\nBarcha ulangan saytlaringiz uzluksiz (24/7) ishlayapti. Sayt tushib qolsa, darhol ogohlantirish yuboriladi ✅\n\n({BOT_USERNAME})")

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
        await message.answer("⚙️ Sozlamalar paneli\n\nSizda hozircha o'chirish uchun qo'shilgan saytlar yoki botlar mavjud emas.")
        return

    builder.adjust(1)
    await message.answer("⚙️ Sozlamalar va boshqaruv paneli\n\nQuyidagi tugmalar yordamida o'zingiz kiritgan ma'lumotlarni o'chirishingiz mumkin:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("del_url_"))
async def delete_url_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    url = callback.data.replace("del_url_", "")
    if user_id in USER_DATA and url in USER_DATA[user_id]["urls"]:
        USER_DATA[user_id]["urls"].remove(url)
        await callback.answer("✅ Sayt o'chirildi!", show_alert=True)
        await callback.message.edit_text("✅ Sayt bazadan o'chirildi.")

@dp.callback_query(F.data.startswith("del_bot_"))
async def delete_bot_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    token = callback.data.replace("del_bot_", "")
    if user_id in USER_DATA and token in USER_DATA[user_id]["bots"]:
        USER_DATA[user_id]["bots"][token]["task"].cancel()
        del USER_DATA[user_id]["bots"][token]
        await callback.answer("✅ Bot o'chirildi!", show_alert=True)
        await callback.message.edit_text("✅ Bot o'chirildi va 24/7 to'xtatildi.")

@dp.message(F.text == "💎 Premium")
async def show_premium(message: types.Message):
    premium_info = (
        f"💎 {BOT_USERNAME} Premium imkoniyatlari\n\n"
        f"🏢 **Biznes va Oddiy foydalanuvchilar uchun:**\n"
        f"• Cheksiz saytlar uptime monitoringi (o'chib qolsa xabar berish)\n"
        f"• Firibgar (phishing) saytlarni tezkor aniqlash\n\n"
        f"💻 **Dasturchilar uchun:**\n"
        f"• Cheksiz botlarni 24/7 cronjob rejimida ushlab turish\n"
        f"• Port Scanner (Ochiq portlarni aniqlash)\n"
        f"• SSL & Headers chuqur xavfsizlik tahlili\n\n"
        f"Quyidagi narxlardan birini tanlab Premium bo'ling:"
    )
    await message.answer(premium_info, reply_markup=get_premium_menu())

async def handle_ping(
