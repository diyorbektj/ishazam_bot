import os
from aiogram import types
from misc import *
from exceptions import NotFoundTrack
from serializer import Track
from pytube import Search, YouTube
from pydub import AudioSegment
import random


def mp3_download(title, subtitle):
    s = Search(f"{title} - {subtitle}")

    keys = s.results[0].__dict__

    yt = YouTube(keys['watch_url'])

    stream = yt.streams.get_by_itag(18)
    rand = random.randint(10, 50)
    print(rand)
    stream.download(filename=f"{rand}.mp4")
    song = AudioSegment.from_file(str(rand) + ".mp4", "mp4")
    song.export(str(rand) + ".mp3", format="mp3")
    return str(rand) + ".mp3"


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=333458329, text=f'Bot yangi azosi {message.from_user.first_name}')
    await message.reply(f"Assalomu alaykum {message.from_user.first_name}\n\n"
                        "Men siz istagan barcha musiqangizni topishga yordam beraman 🎵\n\n"
                        "Dasturchi @Diyorbek_Tj")


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def recognize_song(message: types.Message):
    voice = await message.voice.download()
    info = await shazam.recognize_song(voice.name)
    await message.reply("🔎")
    try:
        serialized_track = Track(info)
        print(serialized_track)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        if serialized_track.text != "test":
            await message.reply(serialized_track.text)
        if serialized_track.image == "image":
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"{serialized_track.subtitle} - {serialized_track.title}\n\n"
                                        "@ishazam_bot orqali topildi!\n\n"
                                        f"Powered By @Diyorbek_Tj \n")
            path = mp3_download(serialized_track.title, serialized_track.subtitle)
            with open(path, "") as music:
                await message.reply_audio(music, performer=serialized_track.title, title=serialized_track.subtitle)
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=serialized_track.image,
                                 caption=f"{serialized_track.subtitle} - {serialized_track.title}\n\n"
                                         "@ishazam_bot orqali topildi!\n\n"
                                         "Powered By @Diyorbek_Tj \n")
            path = mp3_download(serialized_track.title, serialized_track.subtitle)
            with open(path, "rb") as music:
                await message.reply_audio(music, performer=serialized_track.title, title=serialized_track.subtitle)

    except NotFoundTrack:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        await bot.send_message(chat_id=message.from_user.id, text='Afsuski topilmadi 😔')
