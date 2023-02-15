from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import state as st
import config as cfg
import keyboard as kb

bot = Bot(cfg.bot_token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
admin_id = cfg.admin_id
group_ids = cfg.group_ids


@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    user_name = m.from_user.first_name
    if m.chat.type == 'private':
        if m.from_user.id == admin_id:
            await m.answer(f"Hello, admin {user_name}!")
            await m.delete()
        else:
            await m.answer(f"{user_name}, you have no access to use this bot")
            await m.delete()
    else:
        await m.answer(f"{user_name}, this bot for private use only")
        await m.delete()


@dp.message_handler(commands=['new_ad'])
async def new_ad(m: types.Message):
    user_name = m.from_user.first_name
    if m.chat.type == 'private':
        if m.from_user.id == admin_id:
            await m.answer("Add some text:")
            await m.delete()
            await st.CreateAd.text.set()
        else:
            await m.answer(f"{user_name}, you have no access to use this bot")
            await m.delete()
    else:
        await m.answer(f"{user_name}, this bot for private use only")
        await m.delete()


@dp.message_handler(content_types='text', state=st.CreateAd.text)
async def adv_text(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = m.text
        print(data['text'])
    await m.answer("Would you like to add image?", reply_markup=kb.text())
    await st.CreateAd.next()


@dp.callback_query_handler(text='new_text', state=st.CreateAd)
async def new_text(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Add new text:")
    await st.CreateAd.text.set()


@dp.callback_query_handler(text="image", state=st.CreateAd)
async def adv_image_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Send me image:")


@dp.message_handler(content_types=['photo'], state=st.CreateAd.image)
async def adv_image(m: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["image"] = m.photo[0].file_id
        print(data['image'])
        await m.answer("You ad is ready", reply_markup=kb.image())
        await st.CreateAd.next()


@dp.callback_query_handler(text='new_image', state=st.CreateAd)
async def new_text(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Add new image:")
    await st.CreateAd.image.set()


@dp.callback_query_handler(text="finish", state=st.CreateAd)
async def adv_image_call(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.delete()
        await call.message.answer("Here it is:")
        await call.message.answer(data['text'], reply_markup=kb.finish())


@dp.callback_query_handler(text="finish_", state=st.CreateAd)
async def adv_image_call(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.delete()
        await call.message.answer("Here it is:")
        await call.bot.send_photo(admin_id, photo=data['image'], caption=data['text'], reply_markup=kb.finish_())


@dp.callback_query_handler(text="send", state=st.CreateAd.send)
async def adv_image_call(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        for group_id in group_ids:
            await call.bot.send_message(chat_id=group_id, text=data['text'])
            await call.message.answer(f"Message has been send to group id: {group_id}")
            await state.finish()


@dp.callback_query_handler(text="send_", state=st.CreateAd.send)
async def adv_image_call(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        for group_id in group_ids:
            await call.bot.send_photo(chat_id=group_id, photo=data['image'], caption=data['text'])
            await call.message.answer(f"Message has been send to group id: {group_id}")
            await state.finish()


@dp.callback_query_handler(text="cancel")
async def adv_image_call(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Operation is canceled. If you want to try again, press /new_ad")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
