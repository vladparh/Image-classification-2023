import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import torch
import shutil
from config import TOKEN
from aiogram.types import FSInputFile


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

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


model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt')


@dp.message(Command("start"))  # command /start handler
async def cmd_start(message: types.Message):
    await message.answer('Приветствую. Наш бот детектит объекты, относящиеся к 15 различным классам, среди которых '
                         'малый и крупный автотранспорт, самолеты, вертолеты, корабли и прочее. '
                         'Отправь мне изображение (к примеру, это может быть снимок со спутника), и я верну тебе '
                         'изображение с обозначенными объектами, если таковые найдутся')


@dp.message(Command("help"))  # command /help handler
async def cmd_help(message: types.Message):
    await message.answer(f"Наш бот классифицирует следующие объекты:\n{objects}\n"
                         "Чтобы получить изображение с классифицируемыми объектами, просто отправь боту изображение. "
                         "Это может быть как сжатое изображение, так и исходный файл, главное чтобы расширение файла "
                         "было либо .png, либо .jpg")


@dp.message(F.photo)  # от юзера принимает только сжатые фотки / исходники изображений
async def processing_image(message: types.Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text='Начинаю обработку изображения...')
    await bot.download(message.photo[-1], destination='satellite_photo.jpg')
    im = 'satellite_photo.jpg'
    results = model(im)
    results.save()
    photo = FSInputFile("runs\detect\exp\satellite_photo.jpg")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    shutil.rmtree("runs\detect\exp")  # после отправки удаляю фолдер, чтобы не засорять папку


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
