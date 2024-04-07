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

objects = '''
⏺ small vehicle - маленький автомобиль
⏺ large vehicle - большой автомобиль
⏺ tennis court - теннисный корт
⏺ ground track field - стадион
⏺ ship - корабль
⏺ harbor - гавань (порт)
⏺ storage tank - большой резервуар
⏺ swimming pool - бассейн
⏺ plane - самолет
⏺ bridge - мост
⏺ roundabout - круговой перекрёсток
⏺ baseball diamond - бейсбольное поле
⏺ soccer ball field - футбольное поле
⏺ basketball court - баскетбольная площадка
⏺ helicopter - вертолёт
'''

class Form(StatesGroup):
    usless_state = State()  # на будущее


model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt', force_reload=True)


@dp.message_handler(commands=["start"])  # command /start handler
async def cmd_start(message: types.Message):
    await message.answer('Приветствую. Наш бот детектит объекты, относящиеся к 15 различным классам, среди которых '
                         'малый и крупный автотранспорт, самолеты, вертолеты, корабли и прочее. '
                         'Отправь мне изображение (к примеру, это может быть снимок со спутника), и я верну тебе '
                         'изображение с обозначенными объектами, если таковые найдутся')


@dp.message_handler(commands=["help"])  # command /help handler
async def cmd_help(message: types.Message):
    await message.answer(f"Наш бот классифицирует следующие объекты:\n{objects}\n"
                         "Чтобы получить изображение с классифицируемыми объектами, просто отправь боту изображение. "
                         "Это может быть как сжатое изображение, так и исходный файл, главное чтобы расширение файла "
                         "было либо .png, либо .jpg")


@dp.message_handler(content_types=['photo', 'document'])  # от юзера принимает только сжатые фотки / исходники изображений
async def processing_image(message):
    if message.content_type == 'photo':  # сохраняем сжатое изображение
        await bot.send_message(chat_id=message.chat.id, text='Начинаю обработку изображения...')
        await message.photo[-1].download('satellite_photo.jpg')
        im = 'satellite_photo.jpg'
        results = model(im)
        results.save()

        photo = InputFile("runs\detect\exp\satellite_photo.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        shutil.rmtree("runs\detect\exp")  # после отправки удаляю фолдер, чтобы не засорять папку

    elif message.content_type == 'document':  # сохраняем исходное изображение
        try:  # проверяем, является ли отправленный исходник изображением
            await bot.send_message(chat_id=message.chat.id, text='Начинаю обработку изображения...')
            await message.document.download('satellite_photo.jpg')
            im = 'satellite_photo.jpg'
            results = model(im)
            results.save()
            photo = InputFile("runs\detect\exp\satellite_photo.jpg")
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            shutil.rmtree("runs\detect\exp")
        except:
            await bot.send_message(chat_id=message.chat.id, text='Отправленный файл не является изображением')
            return


if __name__ == "__main__":
    # dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
