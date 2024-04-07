import pytest
from aiogram.filters import Command
from aiogram.methods import SendMessage
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from hse_bot import cmd_start
from hse_bot import cmd_help
from hse_bot import processing_image


@pytest.mark.asyncio
async def test_cmd_start():
    requester = MockedBot(request_handler=MessageHandler(cmd_start, Command(commands=['start'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/start'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ('Приветствую. Наш бот детектит объекты, относящиеся к 15 различным классам, '
                              'среди которых малый и крупный автотранспорт, самолеты, вертолеты, корабли и '
                              'прочее. Отправь мне изображение (к примеру, это может быть снимок со '
                              'спутника), и я верну тебе изображение с обозначенными объектами, если '
                              'таковые найдутся')


@pytest.mark.asyncio
async def test_cmd_help():
    requester = MockedBot(request_handler=MessageHandler(cmd_help, Command(commands=['help'])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='/help'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == ('Наш бот классифицирует следующие объекты:\n'
                              '\n'
                              '⏺ small vehicle - маленький автомобиль\n'
                              '⏺ large vehicle - большой автомобиль\n'
                              '⏺ tennis court - теннисный корт\n'
                              '⏺ ground track field - стадион\n'
                              '⏺ ship - корабль\n'
                              '⏺ harbor - гавань (порт)\n'
                              '⏺ storage tank - большой резервуар\n'
                              '⏺ swimming pool - бассейн\n'
                              '⏺ plane - самолет\n'
                              '⏺ bridge - мост\n'
                              '⏺ roundabout - круговой перекрёсток\n'
                              '⏺ baseball diamond - бейсбольное поле\n'
                              '⏺ soccer ball field - футбольное поле\n'
                              '⏺ basketball court - баскетбольная площадка\n'
                              '⏺ helicopter - вертолёт\n'
                              '\n'
                              'Чтобы получить изображение с классифицируемыми объектами, просто отправь '
                              'боту изображение. Это может быть как сжатое изображение, так и исходный '
                              'файл, главное чтобы расширение файла было либо .png, либо .jpg')
