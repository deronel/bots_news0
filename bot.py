from aiogram import Bot, Dispatcher, executor,types
from config import token, user_id
import json
import datetime
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from main import check_news_update
from aiogram.dispatcher.filters import Text
import asyncio



bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message:types.message):
    start_buttons = ["Все новости", "Последнии 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Лента новостей", reply_markup=keyboard)




@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message:types.message):
    with open("news_dict.json")as file:
        news_dict = json.load(file)
    
    for k, v in news_dict.items():
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n"\
        #        f"<u>{v['article_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}"
        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"\
        #        f"{hunderline(v['article_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}"
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"\
               f"{hlink(v['article_title'], v['article_url'])}"
                
        await message.answer(news)


@dp.message_handler(Text(equals='Последнии 5 новостей'))
async def get_last_five_news(message:types.message):
    with open("news_dict.json")as file:
        news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"\
               f"{hlink(v['article_title'], v['article_url'])}"
        

        await message.answer(news)


@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news(message:types.message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"\
                   f"{hlink(v['article_title'], v['article_url'])}"
        await message.answer(news)

    else:
        await message.answer("Нового нечего нет")


async def news_every_menute():
    while True:
        fresh_news = check_news_update()
        
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-5:]:
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n"\
                       f"{hlink(v['article_title'], v['article_url'])}"
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, "Нет нечего нового")
        
        await asyncio.sleep(30)       







if __name__ == '__main__':
    executor.start_polling(dp)