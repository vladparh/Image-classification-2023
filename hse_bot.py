import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


token = '6912058799:AAHfM3T6RTDDqHHAFD-u3YY9GA61wFRgj04'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):  # машина состояний на будущее
    usless_state = State()


@dp.message_handler(commands=["start"])  # Хэндлер на команду /start
async def cmd_start(message: types.Message):
    await message.answer('Отправь мне изображение и я верну тебе изображение с обозначенными объектами')


@dp.message_handler(is_media_group=False, content_types=['photo', 'document'])
async def picture_with_bbox(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        # здесь вместо зеркальной отправки фото будет фотка с bbox объектов, возвращаемая нейронной сетью
        await bot.send_photo(chat_id=message.from_user.id, photo=message.photo[-1].file_id)
    elif message.content_type == 'document':
        await bot.send_document(chat_id=message.from_user.id, document=message.document.file_id)


if __name__ == "__main__":
    # dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
