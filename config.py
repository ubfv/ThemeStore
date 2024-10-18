import os
from dotenv import load_dotenv

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN","7295726109:AAGr0NCXFkeFiZZgObks41yLbf11elE81JY")
CHANNEL = "@" + os.environ.get("CHANNEL", "okokokkkkkkkd")
OWNER_ID = int(os.environ.get("OWNER_ID", "7204102690"))

ytm = YTMusic()
ytd = YoutubeDL(
    {
        "username": "oauth2",
        "password": "",
        "format": "bestaudio",
        "outtmpl": "%(id)s.mp3",
    }
)
temp = {}


print(CHANNEL)
