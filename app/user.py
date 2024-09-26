from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.database.requests import set_user
from app.generators import generate
from app.states import Work
from config import TOKEN

bot=Bot(token=TOKEN)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.full_name)
    await message.answer(f'Добро пожаловать {message.from_user.full_name}!\n\n'
                         f'Не знаешь с чего начать? Тогда просто спроси "Что ты умеешь?"')


@user.message(Work.process)
async def stop(message: Message):
    await message.answer('Подождите, ответ на ваше сообщение генерируется!')

@user.message()
async def ai(message: Message, state: FSMContext):
    await state.set_state(Work.process)
    await bot.send_chat_action(message.chat.id, action='typing')
    try:
        res = await generate(message.text)
        after_res = res.choices[0].message.content
        cleaned_res = after_res.replace("```", "$").replace("**", "").replace("###", "").replace("####", "")
        await message.answer(cleaned_res)
    except:
        await message.answer('Ошибка обработки запроса, введите что-то другое')
    await state.clear()