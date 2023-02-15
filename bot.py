from aiogram import Bot, Dispatcher, types, executor
import config as cfg

bot = Bot(cfg.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
admin_id = cfg.ADMIN_ID


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
