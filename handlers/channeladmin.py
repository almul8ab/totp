from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from cache.admins import set
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from callsmusic import callsmusic



@Client.on_message(filters.command(["channelpause","cpause"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def pause(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل يوجد قناة متصلة بالكروب ؟")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ لا يوجد شيء لايقافه مؤقتاً")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ تم ايقاف الاغنية مؤقتاً")


@Client.on_message(filters.command(["channelresume","cresume"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def resume(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل يوجد قناة متصلة بالكروب ؟")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ لا يوجد شيء لتشغيله")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ تم تشغيل الاغنية")


@Client.on_message(filters.command(["channelend","cend"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل يوجد قناة متصلة بالكروب ؟")
      return    
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ لا يوجد شيء لايقافه")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ تم ايقاف البث")


@Client.on_message(filters.command(["channelskip","cskip"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل يوجد قناة متصلة بالكروب ؟")
      return    
    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ لا يوجد شيء لكي اتخطاه")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- تم تخطي **{skip[0]}**\n- الان جاري تشغيل **{qeue[0][0]}**")


@Client.on_message(filters.command("admincache"))
@errors
async def admincache(client, message: Message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل يوجد قناة متصلة بالكروب ؟")
      return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✅ تم تحديث الملف المؤقت للادمن")
