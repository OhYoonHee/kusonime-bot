from KusonimeBot.TelegramBot import TelegramBot
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
if BOT_TOKEN == None:
    raise "Where you bot token"
bot = TelegramBot(BOT_TOKEN)

bot.run()
