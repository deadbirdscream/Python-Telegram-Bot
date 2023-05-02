from random import choice

import telebot

token = '5544163375:AAG7uwjkKcque5J5zv4e7ekfaUIr3wdmZ5k'

bot = telebot.TeleBot(token)


RANDOM_TASKS = ["Записаться на массаж", "Посмотреть Рика и Морти", "Спеть любимую песню", "Сходить погулять", "Заняться спортом", "Поиграть в Resident Evil", "Покормить кота", "Приготовить ужин", "Навести порядок в доме"]

todos = dict()


HELP = '''
Привет!
Список доступных команд:
/help - вывести список доступных команд
/show  - напечать все задачи на заданную дату ("""/show дата""")
/add - добавить задачу ("""/add дата текст задачи""")
/random - добавить на сегодня случайную задачу
'''


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')


@bot.message_handler(commands=['show'])
def show(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'- {task}\n'
    else:
        tasks = 'Вы не планировали никаких дел на эту дату'
    bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)