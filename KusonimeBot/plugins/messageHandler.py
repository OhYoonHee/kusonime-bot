from KusonimeBot.TelegramBot import TelegramBot
from pyrogram.types import Message
from pyrogram import filters
import re
from KusonimeBot.util import Kusonime, Storage

@TelegramBot.on_message(filters.text)
async def messageHandler(_, msg : Message):
    text = msg.text
    test = re.match(r"((https|http)://kusonime\.com/[\w\d\-]+/?)", text, (re.I))
    if test:
        url = test.group(1)
        init_url = Storage.get(url.lower(), None)
        if init_url == None:
            ph = init_url.get('ph_url')
            await msg.reply(ph, quote = True)
            return
        tgraph = await Kusonime.telegraph(url, msg.message_id)
        if not tgraph['error']:
            await msg.reply(tgraph['url'], quote = True)
            Storage[url.lower()] = dict(ph_url = tgraph['url'])
        return
