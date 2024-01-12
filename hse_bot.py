import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import torch
import shutil

from aiogram.types import InputFile

token = ''  # здесь мой локальный токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    usless_state = State()  # на будущее


model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt', force_reload=True)


@dp.message_handler(commands=["start"])  # command /start handler
async def cmd_start(message: types.Message):
    await message.answer('Отправь мне изображение и я верну тебе изображение с обозначенными объектами')


@dp.message_handler(content_types=['photo', 'document'])  # от юзера принимает только сжатые фотки / исходники изображений
async def processing_image(message):
    if message.content_type == 'photo':  # сохраняем сжатое изображение
        await bot.send_message(chat_id=message.chat.id, text='Начинаю обработку изображения...')
        await message.photo[-1].download('satellite_photo.jpg')
        im = 'C:\Python\\telegramBot\satellite_photo.jpg'
        results = model(im)
        results.save()

        photo = InputFile("C:\Python\\telegramBot\\runs\detect\exp\satellite_photo.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        shutil.rmtree("C:\Python\\telegramBot\\runs\detect\exp")  # после отправки удаляю фолдер, чтобы не засорять папку

    elif message.content_type == 'document':  # сохраняем исходное изображение
        try:  # проверяем, является ли отправленный исходник изображением
            await bot.send_message(chat_id=message.chat.id, text='Начинаю обработку изображения...')
            await message.document.download('satellite_photo.jpg')
            im = 'C:\Python\\telegramBot\satellite_photo.jpg'
            results = model(im)
            results.save()
            photo = InputFile("C:\Python\\telegramBot\\runs\detect\exp\satellite_photo.jpg")
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            shutil.rmtree("C:\Python\\telegramBot\\runs\detect\exp")
        except:
            await bot.send_message(chat_id=message.chat.id, text='Отправленный файл не является изображением')
            return


if __name__ == "__main__":
    # dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
