from aiogram import types
from misc import *
from exceptions import NotFoundTrack
from serializer import Track

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
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        if serialized_track.text != "test":
            await message.reply(serialized_track.text)
        if serialized_track.image == "image":
            await bot.send_message(chat_id=message.from_user.id, text=f"{serialized_track.subtitle} - {serialized_track.title}\n\n"
                        "@ishazam_bot orqali topildi!\n\n"
                        f"Powered By @Diyorbek_Tj \n")
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=serialized_track.image, caption=f"{serialized_track.subtitle} - {serialized_track.title}\n\n"
                        "@ishazam_bot orqali topildi!\n\n"
                        f"Powered By @Diyorbek_Tj \n")

    except NotFoundTrack:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
        await bot.send_message(chat_id=message.from_user.id, text='Afsuski topilmadi 😔')

