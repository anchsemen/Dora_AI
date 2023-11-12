from aiogram import F, Router, flags, Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aniemore.models import HuggingFaceModel
from aniemore.recognizers.text import TextRecognizer
from aniemore.recognizers.voice import VoiceRecognizer
from pathlib import Path
from langdetect import detect

import audio_transcribe
import config
import db
import kb
import text
import utils
from states import Avatar

dp = Dispatcher(storage=MemoryStorage())
router = Router()
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

model_text = HuggingFaceModel.Text.Bert_Tiny2
tr = TextRecognizer(model_text)
model_voice = HuggingFaceModel.Voice.WavLM
vr = VoiceRecognizer(model=model_voice)


@router.message(Command("start"))
async def start_handler(msg: Message):
    chat_id = msg.chat.id
    if db.check_user(chat_id):
        if db.check_avatar(chat_id):
            type_avatar = "characters/" + db.get_type_avatar(chat_id) + '.jpg'
            photo = FSInputFile(type_avatar)
            await msg.answer(text.repeat_greet, reply_markup=ReplyKeyboardRemove())
            await bot.send_photo(chat_id=chat_id, photo=photo)
        else:
            await msg.answer(text.first_create_avatar)
    else:
        db.create_user(chat_id)
        await msg.answer(text.greet, reply_markup=ReplyKeyboardRemove())
        await msg.answer(text.set_avatar_1, reply_markup=kb.menu_1)


@router.callback_query(F.data == "man")
@router.callback_query(F.data == "woman")
async def set_avatar_1(clbck: CallbackQuery, state: FSMContext):
    chat_id = clbck.message.chat.id
    if db.check_avatar(chat_id):
        type_avatar = "characters/" + db.get_type_avatar(chat_id) + '.jpg'
        photo = FSInputFile(type_avatar)
        await clbck.message.answer(text.repeat_greet, reply_markup=ReplyKeyboardRemove())
        await bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        await state.set_state(Avatar.gender.state)
        await state.update_data(gender=clbck.data)
        await clbck.message.answer(text.set_avatar_2, reply_markup=kb.menu_2)


@router.callback_query(F.data == "young")
@router.callback_query(F.data == "medium")
@router.callback_query(F.data == "adult")
async def set_avatar_2(clbck: CallbackQuery, state: FSMContext):
    chat_id = clbck.message.chat.id
    if db.check_avatar(chat_id):
        type_avatar = "characters/" + db.get_type_avatar(chat_id) + '.jpg'
        photo = FSInputFile(type_avatar)
        await clbck.message.answer(text.repeat_greet, reply_markup=ReplyKeyboardRemove())
        await bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        await state.set_state(Avatar.age.state)
        await state.update_data(age=clbck.data)
        await clbck.message.answer(text.set_avatar_3, reply_markup=kb.menu_3)


@router.callback_query(F.data == "blond")
@router.callback_query(F.data == "lightbrown")
@router.callback_query(F.data == "dark")
async def set_avatar_3(clbck: CallbackQuery, state: FSMContext):
    chat_id = clbck.message.chat.id
    if db.check_avatar(chat_id):
        type_avatar = "characters/" + db.get_type_avatar(chat_id) + '.jpg'
        photo = FSInputFile(type_avatar)
        await clbck.message.answer(text.repeat_greet, reply_markup=ReplyKeyboardRemove())
        await bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        await state.set_state(Avatar.hair.state)
        await state.update_data(hair=clbck.data)
        user_data = await state.get_data()
        characteristic = user_data['gender'] + '_' + user_data['hair'] + '_' + user_data['age']
        db.type_avatar(clbck.message.chat.id, characteristic)
        type_avatar = "characters/" + characteristic + '.jpg'
        photo = FSInputFile(type_avatar)
        await bot.send_photo(chat_id=clbck.message.chat.id, photo=photo)
        await clbck.message.answer(text.avatar, reply_markup=ReplyKeyboardRemove())


@router.message(Command("feedback"))
async def feedback_handler(msg: Message):
    await msg.answer(text.feedback, reply_markup=kb.feedback)


@router.message(Command("count_users"))
async def count_handler(msg: Message):
    if msg.chat.id in config.access_list:
        count_users, users = db.count_users()
        await msg.answer('Количество пользователей: ' + str(count_users + 70), reply_markup=ReplyKeyboardRemove())
    else:
        print(msg.chat.id)
        await msg.answer(text.error, reply_markup=ReplyKeyboardRemove())


@router.message(F.content_type == "voice")
async def voice_handler(msg: Message):
    chat_id = msg.chat.id
    if db.check_user(chat_id):
        file_id = msg.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_on_disk = Path("", f"1.wav")
        await bot.download_file(file_path, destination=file_on_disk)
        voice_color = vr.recognize('1.wav', return_single_label=True)
        text_speech = audio_transcribe.transcribe(file_on_disk)
        print(voice_color, text_speech)
        oldmes, character, count_mes = db.get_inf(msg.chat.id)
        answer = await utils.generate_text(text_speech, oldmes, voice_color, character)
        if detect(answer[0]) != 'ru':
            answer = await utils.translated_text(answer[0])
        db.add_text(chat_id, text_speech, answer[0])
        await msg.answer(answer[0], disable_web_page_preview=True)
    else:
        await msg.answer(text.first_create_avatar)


@router.message(F.content_type == "text")
@flags.chat_action("typing")
async def message_handler(msg: Message):
    chat_id = msg.chat.id
    if db.check_user(chat_id):
        oldmes, character, count_mes = db.get_inf(chat_id)
        text_color = tr.recognize(msg.text, return_single_label=True)
        answer = await utils.generate_text(msg.text, oldmes, text_color, character)
        if detect(answer[0]) != 'ru':
            answer = await utils.translated_text(answer[0])
        db.add_text(chat_id, msg.text, answer[0])
        await msg.answer(answer[0], disable_web_page_preview=True)

    else:
        await msg.answer(text.first_create_avatar)
