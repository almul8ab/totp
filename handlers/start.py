from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **مرحبا {message.from_user.first_name}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) يسمح لك بتشغيل الموسيقى بالكروبات عبر ميزة المحادثة الصوتية او التحميل من اليوتيوب .

❓ ** للمزيد من المعلومات عن البوت وطريقة عمله ارسل /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ اضفني لكروبك ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                         "📚 الاوامر", url="https://telegra.ph/VEEZ-MUSIC-GUIDE-07-27"
                    ),
                    InlineKeyboardButton(
                        "💝 التواصل معنا", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "👥 الكروب الاساسي", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 القناة", url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **البوت مفعل**\n<b>💠 **وقت بدء التشغيل:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ الكروب", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 القناة", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 مرحبا {message.from_user.mention()}, الرجاء الضغط على الزر في الاسفل لمعرفة طريقة استخدام البوت</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❔ تعليمات الاستخدام", url=f"https://t.me/{BOT_USERNAME}?start=help"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>مرحبا {message.from_user.mention()}, هذه قائمة الاوامر الخاصة بالبوت ✨
\n📙 طريقة الاستخدام ?
\n1. اضف البوت الى الكروب الخاص بك .
2. اعطي البوت صلاحيات الادمن .
3. ثم اضف الحساب المساعد @{ASSISTANT_NAME} الى الكروب او قم بكتابة /userbotjoin.
4. تأكد بتشغيل المحادثة الصوتية قبل تشغيل الاغاني .
\n💁🏻‍♀️ ** الاوامر الخاصة بالاعضاء : **
\n/play ( اسم الاغنية ) - تشغيل الاغاني من اليوتيوب .
/stream ( الرد على رسالة ) - تشغيل اغنية باستخدام ملف الصوت .
/playlist - عرض قائمة الأغاني في قائمة الانتظار .
/current - إظهار الأغنية في البث .
/song ( اسم الاغنية ) - تحميل اغنية من اليوتيوب .
/search ( اسم الفيديو ) - جلب تفاصيل الفيديو من اليوتيوب .
/vsong ( اسم الفيديو ) - تحميل فيديو من اليوتيوب مع التفاصيل .
\n👷🏻‍♂️ ** الاوامر الخاصة بالادمن : **
\n/player - فتح لوحة إعدادات مشغل الموسيقى .
/pause - ايقاف مؤقت للموسيقى .
/resume - استئناف الموسيقى التي تم ايقافها .
/skip - تخطي إلى الأغنية التالية .
/end - ايقاف الموسيقى .
/userbotjoin - دعوة الحساب المساعد للانضمام الى الكروب .
/reload - تحديث قائمة الادمن .
/cache - تنظيف الملف المؤقت لقائمة الادمن .
/musicplayer (on / off) - تعطيل / تمكين مشغل الموسيقى في مجموعتك .
\n🧙‍♂️ الاوامر الخاصة بالمطور الاساسي :
\n/userbotleaveall - الطلب من الحساب المساعد مغادرة كافة الكروبات .
/gcast - ارسال رسالة بث عبر الحساب المساعد .
\n🎊 ** اوامر للتسلية : **
\n/lyric - ( اسم الاغنية ) لعرض كلمات الاغنية .
\n/ping - لقياس سرعة استجابة البوت .
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ الكروب ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 القناة ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👩🏻‍💻 المطور ", url=f"https://t.me/{OWNER_NAME}"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("جاري قياس السرعة .....")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `السرعة : `\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 حالة البوت :\n"
        f"• **مدة التشغيل :** `{uptime}`\n"
        f"• **تاريخ بدأ التشغيل :** `{START_TIME_ISO}`"
    )
