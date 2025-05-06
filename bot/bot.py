import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db, get_user, update_balance, get_click_power
from mechanics import click_coin
from upgrades import try_upgrade_click

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(commands=['start'])
async def cmd_start(message: types.Message):
    await get_user(message.from_user.id)
    kb = InlineKeyboardBuilder()
    kb.button(text="💰 Клик!", callback_data="click")
    kb.button(text="📈 Прокачка (100 KICH)", callback_data="upgrade")
    await message.answer("Добро пожаловать в <b>KICH COIN</b>! Нажимай 💰, чтобы зарабатывать монеты.", reply_markup=kb.as_markup())

@dp.callback_query(lambda c: c.data == "click")
async def handle_click(callback_query: types.CallbackQuery):
    amount = await click_coin(callback_query.from_user.id)
    user = await get_user(callback_query.from_user.id)
    await callback_query.answer(f"+{amount} KICH", show_alert=False)
    await callback_query.message.edit_text(
        f"💰 Баланс: {user[1] + amount} KICH\n⚡ Сила клика: {user[2]}",
        reply_markup=callback_query.message.reply_markup
    )

@dp.callback_query(lambda c: c.data == "upgrade")
async def handle_upgrade(callback_query: types.CallbackQuery):
    success = await try_upgrade_click(callback_query.from_user.id)
    user = await get_user(callback_query.from_user.id)
    if success:
        await callback_query.answer("Прокачка успешна! 🔥")
    else:
        await callback_query.answer("Недостаточно монет.")
    await callback_query.message.edit_text(
        f"💰 Баланс: {user[1]} KICH\n⚡ Сила клика: {user[2]}",
        reply_markup=callback_query.message.reply_markup
    )

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
