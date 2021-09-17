from pyrogram import Client

class TelegramBot(Client):
    def __init__(self, bot_token, **kwargs):
        super().__init__(
            session_name = "TelegramBot", 
            api_id = 6, 
            api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e", 
            bot_token = bot_token, 
            plugins = dict(root = 'KusonimeBot/plugins'),
            **kwargs
        )
