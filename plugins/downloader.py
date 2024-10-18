import requests
import os
import asyncio
import json
import glob
import random

from config import temp, ytm, ytd, CHANNEL
from database import get_audio, add_audio

from tgram import TgBot
from tgram.types import CallbackQuery, Message

from typing import Union


def cookie_txt_file():
    folder_path = f"{os.getcwd()}/cookies"
    filename = f"{os.getcwd()}/cookies/logs.csv"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Chosen File : {cookie_txt_file}\n')
    return cookie_txt_file


async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookie_txt_file(),  
            "-J",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return None
        return json.loads(stdout.decode())

@TgBot.on_callback_query()
async def on_callback_query(b: TgBot, c: CallbackQuery) -> Union[bool, Message]:
    video_id, album_id = c.data.split(":")

    album_info = ytm.get_album(album_id)
    song_info = temp.get(video_id)

    thumb = album_info["thumbnails"][-1]["url"]

    if aud := await get_audio(song_info["videoId"]):
        return await c.message.reply_audio(aud)

    msg = await c.message.reply_photo(
        thumb,
        caption=(
            "Title: {}\n"
            "Author: **{}**\n"
            "Year: **{}**\n"
            "Is Explict: **{}**\n\n"
            "**Downloading..**"
        ).format(
            song_info["title"],
            " ,".join(i["name"] for i in song_info["artists"]),
            album_info["year"],
            song_info["isExplicit"],
        ),
    )

    vid_info = ytd.extract_info(
        "https://youtube.com/watch?v=" + song_info["videoId"],
        download=True,
        extra_info={'cookiefile': cookie_txt_file()}  
    )
    path = ytd.prepare_filename(vid_info)

    audio = await b.send_audio(
        CHANNEL,
        path,
        performer=" ,".join(i["name"] for i in song_info["artists"]),
        caption="```" + song_info["videoId"] + "```",
        title=song_info["title"],
        thumbnail=requests.get(thumb).content,
        duration=song_info["duration_seconds"],
    )

    os.remove(path)

    await add_audio(song_info["videoId"], audio.link)

    return await msg.reply_audio(audio.link)