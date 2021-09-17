from KusonimeBot.TelegramBot import TelegramBot
from pyrogram.types import InlineQueryResultArticle as atr, InputTextMessageContent as append_text, InlineQuery
from KusonimeBot.util import Kusonime

@TelegramBot.on_inline_query()
async def InlineQueryHandler(_, iq : InlineQuery):
    q = iq.query
    if len(q) < 2:
        return
    querys = await Kusonime.search(q)
    if not querys['error']:
        results = []
        for x in querys['results']:
            results.append(
                atr(title = x['title'], 
                input_message_content = append_text(
                    message_text = x['url']
                ), 
                thumb_url = x['thumb'])
            )
        return await iq.answer(results)
