import random
import time
import func

from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, URL_PROBLEMSET, MSG_ERROR
from db import BotDB

BotDB = BotDB('ICPCFUdb.db')

bot = Bot(TOKEN)
dp = Dispatcher(bot)

TASK_LINKS = []
TYPE_BONUSES = {'BeginnerBonus': 0, 'StandardBonus': 1, 'ExpertBonus': 2, 'LegendaryBonus': 3}
BONUSES_X = []
BONUSES_T = []
BONUSES_C = []

def check_id(id) :
    if not BotDB.user_exists(id):
        return False
    return True

def update_bonus(id):
    bon = BotDB.get_cur_bonus(id)
    t = BONUSES_T[bon]
    last_time = t - (round(time.time()) - BotDB.get_time_bonus(id))
    if last_time <= 0:
        BotDB.add_cur_bonus(id, -1)

def get_x(id):
    bon = BotDB.get_cur_bonus(id)
    if bon == -1:
        return 1
    x = BONUSES_X[bon]
    return x

@dp.message_handler(commands= "check")
async def checker(message: types.Message):
    id = message.from_user.id
    if check_id(id) is False:
        await message.reply(MSG_ERROR)
        return 0
    update_bonus(id)
    url = message.text.replace("/check ", "")
    name = BotDB.get_name(id)
    task_id = BotDB.get_task(id)
    if ("/check " in message.text) is False or ("https://codeforces.com/" in url) is False:
        await message.reply(MSG_ERROR)
        return 0
    result = func.parser_solves(url, name, task_id)
    if result and func.IsSolvedProblem(BotDB.get_problemset(id), task_id) is False:
        BotDB.add_task(id, "none")
        BotDB.add_problemset(id, BotDB.get_problemset(id) + task_id)
        total_coins = func.update_coins(BotDB.get_diff(id))
        total_exp, exp, level = func.update_level(BotDB.get_diff(id), BotDB.get_exp(id),
                                                  BotDB.get_level(id), get_x(id))
        BotDB.add_exp(id, exp)
        BotDB.add_level(id, level)
        BotDB.add_money(id, BotDB.get_money(id) + total_coins)
        await message.reply(f"Well done, you got {total_coins} coins and {round(total_exp)} exp")
    else:
        await message.reply(MSG_ERROR)

############shop#######

@dp.message_handler(commands="shop")
async def shop(message: types.Message):
    await message.reply(f"Here you could buy bonus for exp!\n\n"
                        f"BeginnerBonus - multiply by 1.4 earned exp within 15 minutes (price: 4 coins)\n\n"
                        f"StandardBonus - multiply by 2 earned exp within 1 hour (price: 50 coins)\n\n"
                        f"ExpertBonus - multiply by 3 earned exp within 4 hours (price: 210 coins)\n\n"
                        f"LegendaryBonus - multiply by 4.2 earned exp within 12 hours (price: 520 coins)\n\n"
                        f"In order to buy bonus, you have to enter /buy <bonus name>")

def create_bonus(x, c, t):
    BONUSES_T.append(t)
    BONUSES_X.append(x)
    BONUSES_C.append(c)

def create_bonuses():
    create_bonus(1.4, 4, 900)
    create_bonus(2, 50, 3600)
    create_bonus(3, 210, 14400)
    create_bonus(4.2, 520, 43200)

@dp.message_handler(commands="buy")
async def pay(message: types.Message):
    id = message.from_user.id
    bon = message.text.replace("/buy ", "")
    money = BotDB.get_money(id)
    if TYPE_BONUSES.get(bon) == None:
        await message.reply(MSG_ERROR)
        return 0
    bon = TYPE_BONUSES.get(bon)
    c = BONUSES_C[bon]
    if money < c:
        await message.reply("Not enough coins!")
        return 0
    BotDB.add_cur_bonus(id, bon)
    BotDB.add_time_bonus(id, round(time.time()))
    BotDB.add_money(id, money - c)
    await message.reply("Successful purchase!")

@dp.message_handler(commands="profile")
async def profile(message: types.Message):
    id = message.from_user.id
    if check_id(id) is False:
        await message.reply(MSG_ERROR)
        return 0
    update_bonus(id)
    bon = BotDB.get_cur_bonus(id)
    text = ''
    if bon == -1:
        text = "You have no bonus exp!"
    else:
        t = BONUSES_T[bon]
        last_time = t - (round(time.time()) - BotDB.get_time_bonus(id))
        h, m, s = func.get_time(last_time)
        text = f"Bonus exp will be active for {h // 10}{h % 10}:{m // 10}{m % 10}:{s // 10}{s % 10} hours"
    await message.reply(f"Your money {BotDB.get_money(id)}\n"
                        f"Your level {BotDB.get_level(id)} "
                        f"({round(BotDB.get_exp(id))}/"
                        f"{func.new_level(BotDB.get_level(id))})\n"
                        f"{text}")

@dp.message_handler(commands = "help")
async def help(message: types.Message):
    await message.reply(f"/manual - about this bot.\n"
                        f"/manual_errors - how to fix some errors.\n"
                        f"/reg <nickname> - register your nick on codeforces.com for bot.\n"
                        f"/get <difficulty> - bot will send you task's link.\n"
                        f"/profile - check information about you.\n"
                        f"/check <your link to solution> - bot will check your submission.\n"
                        f"/shop - that's a shop.\n"
                        f"/buy <name bonus> - buy a new super bonus!\n"
                        f"/leaders - look at the leaders of solving problems.")

@dp.message_handler(commands= "manual")
async def help(message: types.Message):
    await message.reply("The bot was created for people who likes to solve programming problems on codeforces "
                        "and compete with other participants. It looks like the game to make it more fun. "
                        "if you get issue with some commands you can ride the /manual_errors or write "
                        "to our administration @yar_kk. Good luck!")

@dp.message_handler(commands= "manual_errors")
async def help(message: types.Message):
    await message.reply("If you get SOMETHING WENT WRONG, TRY AGAIN, then:\n\n"
                        "1.Probably you are not registered (/reg).\n"
                        "2.Not correct link to solution, must be (for example): "
                        "https://codeforces.com/contest/1845/submission/211709448\n"
                        "3.Not found bonus with that name (/shop).\n"
                        "4.Not correct command or if you use /check, then in case of such error, "
                        "the solution is wrong.\n"
                        "5.Probably bot has some bags, so you should to write @yar_kk.")

@dp.message_handler(commands= "illia")
async def help(message: types.Message):
    await message.reply("@hepocinkup4ik призыв Ильи!!!")

@dp.message_handler(commands="chmax")
async def help(message: types.Message):
    await message.reply("small to Chmyaaaaaaaaaaaaaaks, Feb 2!!!")

@dp.message_handler(commands="Ignut")
async def help(message: types.Message):
    await message.reply("/Ignut")

@dp.message_handler(commands="tell_me_about")
async def help(message: types.Message):
    await message.reply("он харош")

@dp.message_handler(commands="rainboy")
async def help(message: types.Message):
    await message.reply("до до свидания.")

################################################################################

def create_problems():
    for i in range(28):
        rank = str((i + 8) * 100)
        url = URL_PROBLEMSET + rank + "-" + rank
        new_task_links = func.parser_problems(url)
        TASK_LINKS.append(new_task_links)
        random.shuffle(TASK_LINKS[i])

create_problems()
create_bonuses()

@dp.message_handler(commands= "leaders")
async def get_leaders(message: types.Message):
    LEADERS = BotDB.get_leaders()
    text = "Leaders by level:\n\n"
    for i in range(min(len(LEADERS), 10)):
        text += LEADERS[i][0] + " - " + str(LEADERS[i][1]) + " level\n"
    await message.answer(text)

@dp.message_handler(commands= "get")
async def get_problem(message: types.Message):
    if check_id(message.from_user.id) is False or ("/get " in message.text) is False:
        await message.reply(MSG_ERROR)
        return 0
    val = message.text.replace("/get ", "")
    rank = int(val) // 100 - 8
    if (rank < 0 or rank > 27):
        await message.reply("Not correct rank (800-3500).")
        return 0
    index = random.randint(0, 99)
    task_link = "https://codeforces.com" + TASK_LINKS[rank][index]
    new_task_link = task_link.replace("https://codeforces.com/problemset/problem/", "")
    new_task_link = new_task_link.replace("/", "")
    BotDB.add_task(message.from_user.id, new_task_link)
    BotDB.add_diff(message.from_user.id, rank)
    await message.reply(f"{task_link}\n you will get {func.new_coins(rank)} "
                        f"coins and {func.new_exp(rank)} exp (without bonuses)")

@dp.message_handler(commands = "reg")
async def reg(message: types.Message):
    if check_id(message.from_user.id) or ("/reg " in message.text) is False:
        await message.reply(MSG_ERROR)
        return 0
    name = message.text.replace("/reg ", "")
    if func.check_name(name) is False:
        await message.reply("NickName not found!")
        return 0
    BotDB.add_user(message.from_user.id)
    BotDB.add_name(message.from_user.id, name)
    await message.reply(f"Hello, {name}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)