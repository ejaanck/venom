import asyncio

from VenomX import Ayush
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageDeleteForbidden, UserNotParticipant

from config import *
from VenomX.core.tools import *
from VenomX.utils.decorators.admins import *
from VenomX.core.message import *
from VenomX.utils.database import *


@app.on_message(filters.command("bl",["","/"]) & ~filters.private & Admin)
async def addblmessag(app : Ayush, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menambahakan` {trigger} `ke dalam blacklist..`")
    try:
        await add_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di tambahkan ke dalam blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()

@app.on_message(filters.command("delbl") & ~filters.private & Admin)
async def deldblmessag(app : Ayush, message : Message):
    trigger = get_arg(message)
    if message.reply_to_message:
        trigger = message.reply_to_message.text or message.reply_to_message.caption

    xxnx = await message.reply(f"`Menghapus` {trigger} `ke dalam blacklist..`")
    try:
        await remove_bl_word(trigger.lower())
    except BaseException as e:
        return await xxnx.edit(f"Error : `{e}`")

    try:
        await xxnx.edit(f"{trigger} `berhasil di hapus dari blacklist..`")
    except:
        await app.send_message(message.chat.id, f"{trigger} `berhasil di hapus dari blacklist..`")

    await asyncio.sleep(5)
    await xxnx.delete()
    await message.delete()


@app.on_message(filters.text & ~filters.private & Member & Gcast)
async def deletermessag(app : Ayush, message : Message):
    text = f"Maaf, Grup ini tidak terdaftar di dalam list. Silahkan hubungi @jaahilang Untuk mendaftarkan Group Anda.\n\n**Bot akan meninggalkan group!**"
    chat = message.chat.id
    chats = await get_actived_chats()
    if chat not in chats:
        await message.reply(text=text)
        await asyncio.sleep(60)
        try:
            await app.leave_chat(chat)
        except UserNotParticipant as e:
            print(e)
        return
    
    # Delete
    try:
        await message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.delete()
    except MessageDeleteForbidden:
        pass
