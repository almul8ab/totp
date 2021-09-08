from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import SUDO_USERS


@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>اعطني صلاحيات الادمن أولاً !</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "🤖: انضممت هنا لكي اساعدكم بتشغيل الموسيقى في المحادثات الصوتية")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>الحساب المساعد موجود مسبقاُ</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 خطأ 🛑 \n المستخدم {user.first_name} لم يستطع الدخول الى الكروب تأكد بانك لم تقم بحظره ."
            "\n\nاو قم باضافته الى الكروب بشكل يدوي .</b>",
        )
        return
    await message.reply_text(
        "<b>الحساب المساعد انضم للكروب .</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>حصل خطأ بخروج الحساب المساعد من الكروب ."
            "\n\nاذا تكرر الخطأ قم بازالته يدوياً</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("الحساب المساعد خرج من جميع الكروبات")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"الحساب المساعد غادر: {left} كروب . ولم يغادر من : {failed} كروب .")
            except:
                failed=failed+1
                await lol.edit(f"الحساب المساعد غادر: {left} كروب . ولم يغادر من : {failed} كروب .")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"غادر: {left} كروب . ولم يغادر من : {failed} كروب .")
