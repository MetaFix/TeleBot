import telebot
from telebot import types
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import pandas as pd
import psycopg2

bot_token = '6206750369:AAGI3k5aYwUJpMNVw4T2leth1DVOji3TlUA'
Your_diary_bot = telebot.TeleBot(bot_token)

class DatabaseManager :
    def __init__(self, database, user, password, host, port):
        self.database = "DBchat"
        self.user = "postgres"
        self.password = "3005"
        self.host = "localhost"
        self.port = "5432"

    def connect(self):
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                           host=self.host, port=self.port)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()

class User :

    @Your_diary_bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Створити запис")
        btn2 = types.KeyboardButton("Створити групу")
        btn3 = types.KeyboardButton("Закрити запис")
        btn4 = types.KeyboardButton("Перегляд")
        markup.add(btn1, btn2, btn3, btn4)
        Your_diary_bot.send_message(message.chat.id,
                         text="Вітаю, {0.first_name}! Чим можу допомогти ?".format(message.from_user), reply_markup=markup)

        username = message.from_user.username
        db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password", host="your_host", port="your_port")
        db_manager.connect()
        query_select = "SELECT Login FROM ffggffgg WHERE Login = %s"
        values_select = (username,)
        db_manager.execute_query(query_select, values_select)
        existing_record = db_manager.cursor.fetchone()

        if existing_record:
            print("Запис з таким значенням вже існує.")
        else:
            query_insert = 'INSERT INTO ffggffgg (Login) VALUES (%s)'
            values_insert = (username,)
            db_manager.execute_query(query_insert, values_insert)
            db_manager.commit()
            print("Запис був успішно вставлений.")
        db_manager.disconnect()

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Створити запис")
    def creTaskB(message):
        if (message.text == "Створити запис"):
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назва та опис")
            btn2 = types.KeyboardButton("Додати в групу")
            btn3 = types.KeyboardButton("Оцінити пріоритетність")
            back = types.KeyboardButton("Головне меню")
            markup1.add(btn1, btn2, btn3, back)
            Your_diary_bot.send_message(message.chat.id, text="Можемо починати", reply_markup=markup1)
            #CreateTask

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Створити групу")
    def creGroupB(message):
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Додати назву")
            btn3 = types.KeyboardButton("Оцінити пріоритетність групи")
            back = types.KeyboardButton("Головне меню")
            markup1.add(btn1, btn3, back)
            Your_diary_bot.send_message(message.chat.id, text="Можемо починати", reply_markup=markup1)

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Перегляд")
    def reviewB(message):
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Перегляд груп")
            btn2 = types.KeyboardButton("Перегляд завдань з групи")
            btn4 = types.KeyboardButton("Завдання за пріоритетністю")
            back = types.KeyboardButton("Головне меню")
            markup1.add(btn1, btn2, btn4, back)
            Your_diary_bot.send_message(message.chat.id, text="Можемо починати", reply_markup=markup1)

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Закрити запис")
    def closeTaskB(message):
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Обрати запис")
            btn2 = types.KeyboardButton("Коментар до виконання")
            btn3 = types.KeyboardButton("Оцінити виконання")
            back = types.KeyboardButton("Головне меню")
            finish = types.KeyboardButton("Завершити")
            markup1.add(btn1, btn2, btn3, finish, back)
            Your_diary_bot.send_message(message.chat.id, text="Можемо починати", reply_markup=markup1)

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Головне меню")
    def menu(message):
            Your_diary_bot.send_message(message.chat.id, text="Повертаємось")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Створити запис")
            btn2 = types.KeyboardButton("Створити групу")
            btn3 = types.KeyboardButton("Закрити запис")
            btn4 = types.KeyboardButton("Перегляд")
            markup.add(btn1, btn2, btn3, btn4)
            Your_diary_bot.send_message(message.chat.id,
                                        text="Вітаю, {0.first_name}! Чим можу допомогти ?".format(message.from_user),
                                        reply_markup=markup)

class CreateTask :

    user_id = None
    group_list = ""
    global task
    global mark
    global task_description
    global group_id
    global waiting_for_task
    global waiting_for_mark
    global waiting_for_description
    global waiting_for_group

    try :
        @Your_diary_bot.message_handler(func=lambda message: message.text == "Назва та опис")
        def enterTask(message):
            global waiting_for_task

            Your_diary_bot.send_message(message.chat.id, text="Напиши назву в лапках")
            waiting_for_task = True
        @Your_diary_bot.message_handler(func=lambda message: waiting_for_task)
        def processTask(message):

            global task
            global waiting_for_task
            global waiting_for_description
            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            username = message.from_user.username
            query_select = "SELECT ffggffgg.id_user FROM ffggffgg WHERE login = %s"
            values_select = (username,)
            db_manager.execute_query(query_select, values_select)
            existing_record = db_manager.cursor.fetchone()
            CreateTask.user_id = existing_record[0]
            task = message.text
            waiting_for_task = False
            query_insert = 'INSERT INTO tasks (id_user, name) VALUES (%s, %s)'
            values_insert = (CreateTask.user_id, task)
            db_manager.execute_query(query_insert, values_insert)
            db_manager.connection.commit()
            Your_diary_bot.send_message(message.chat.id, text="Чудово, опиши своє завдання без лапок.")
            waiting_for_description = True
            db_manager.disconnect()

        @Your_diary_bot.message_handler(func=lambda message: waiting_for_description)
        def processDescription(message):
            global task_description
            global waiting_for_description
            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            task_description = message.text
            waiting_for_description = False
            query_update = "UPDATE tasks SET description = %s WHERE name = %s"
            values_insert = (task_description, task)
            db_manager.execute_query(query_update, values_insert)
            db_manager.connection.commit()
            db_manager.disconnect()
            Your_diary_bot.send_message(message.chat.id, text="Завдання успішно названо та описано. Тепер можна додати його в групу або оцінити його пріоритетність.")
    except :
        def err1(message):
            Your_diary_bot.send_message(message.chat.id, text="Упс, щось пішло не так. Спробуйте ще раз з початку створити назву та опис запису.")
    try :
        @Your_diary_bot.message_handler(func=lambda message: message.text == "Додати в групу")
        def groupTask(message):
            global waiting_for_group

            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            query_select = "SELECT groups.id_group, groups.name_group FROM groups WHERE id_user = %s"
            values_select = (CreateTask.user_id,)
            db_manager.execute_query(query_select, values_select)
            existing_record = db_manager.cursor.fetchone()
            group_list = existing_record[0]
            group_list = str(group_list) + "Обери номер групи з наведених вище"
            Your_diary_bot.send_message(message.chat.id, text=group_list)
            waiting_for_group = True

        @Your_diary_bot.message_handler(func=lambda message: waiting_for_group)
        def processGroup(message):
            global group_id
            global waiting_for_group
            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            group_id = message.text
            waiting_for_group = False
            query_update = "UPDATE tasks SET id_group = %s WHERE name = %s"
            values_insert = (group_id, task)
            db_manager.execute_query(query_update, values_insert)
            db_manager.connection.commit()
            db_manager.disconnect()

    except :
        def err2(message):
            Your_diary_bot.send_message(message.chat.id,
                                        text="Упс, щось пішло не так. Такої групи ще немає.")

    try:
        @Your_diary_bot.message_handler(func=lambda message: message.text == "Оцінити пріоритетність")
        def enterMark(message):
            global waiting_for_mark

            Your_diary_bot.send_message(message.chat.id, text="Оцініть важливість від 1 до 5")
            waiting_for_mark = True

        @Your_diary_bot.message_handler(func=lambda message: waiting_for_mark)
        def markTask(message):

            global mark
            global waiting_for_mark

            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            query_select = "SELECT tasks.id_task FROM tasks WHERE name = %s"
            values_select = (task,)
            db_manager.execute_query(query_select, values_select)
            existing_record = db_manager.cursor.fetchone()
            task_id = existing_record[0]
            mark = message.text
            waiting_for_mark = False
            query_insert = 'INSERT INTO marks (id_task, mark_priority) VALUES (%s, %s)'
            values_insert = (task_id, mark)
            db_manager.execute_query(query_insert, values_insert)
            db_manager.connection.commit()
            db_manager.disconnect()
    except :
        def err3(message):
            Your_diary_bot.send_message(message.chat.id,
                                        text="Упс, щось пішло не так. Перед тим як оцінити запис створіть його назву та опис. ( не забудьте видалити неповноцінний запис якщо такий випадково було створено)")

class Review(User):
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Перегляд груп")
    def viewGroup(message):
        Your_diary_bot.send_message(message.chat.id, text="")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Перегляд завдань з групи")
    def tasksFromGroup(message):
        Your_diary_bot.send_message(message.chat.id, text="")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Завдання за пріоритетністю")
    def viewMarkTasks(message):
        Your_diary_bot.send_message(message.chat.id, text="")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Групи за пріоритетністю")
    def viewMarkGroup(message):
        Your_diary_bot.send_message(message.chat.id, text="")

class CreateGroup :

    user_id = None
    global group
    global mark_group
    global group_id
    global waiting_for_group
    global waiting_for_mark_g


    try:
        @Your_diary_bot.message_handler(func=lambda message: message.text == "Додати назву")
        def enterGroup(message):
            global waiting_for_group

            Your_diary_bot.send_message(message.chat.id, text="Напиши назву групи в лапках")
            waiting_for_group = True

        @Your_diary_bot.message_handler(func=lambda message: waiting_for_group)
        def processTask(message):

            global group
            global waiting_for_group
            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            username = message.from_user.username
            query_select = "SELECT ffggffgg.id_user FROM ffggffgg WHERE login = %s"
            values_select = (username,)
            db_manager.execute_query(query_select, values_select)
            existing_record = db_manager.cursor.fetchone()
            CreateTask.user_id = existing_record[0]
            group = message.text
            waiting_for_group = False
            query_insert = 'INSERT INTO tasks (id_user, name) VALUES (%s, %s)'
            values_insert = (CreateTask.user_id, group)
            db_manager.execute_query(query_insert, values_insert)
            db_manager.connection.commit()
            db_manager.disconnect()
    except:
        def err4(message):
            Your_diary_bot.send_message(message.chat.id,
                                        text="Упс, щось пішло не так. Спробуйте ще раз з початку створити назву групи.")


    try:
        @Your_diary_bot.message_handler(func=lambda message: message.text == "Оцінити пріоритетність")
        def enterMark(message):
            global waiting_for_mark_g

            Your_diary_bot.send_message(message.chat.id, text="Оцініть важливість від 1 до 5")
            waiting_for_mark_g = True

        @Your_diary_bot.message_handler(func=lambda message: waiting_for_mark_g)
        def markTask(message):

            global mark_group
            global waiting_for_mark_g

            db_manager = DatabaseManager(database="your_database", user="your_user", password="your_password",
                                         host="your_host", port="your_port")
            db_manager.connect()
            query_select = "SELECT groups.id_group FROM groups WHERE name_ = %s"
            values_select = (task,)
            db_manager.execute_query(query_select, values_select)
            existing_record = db_manager.cursor.fetchone()
            task_id = existing_record[0]
            mark_group = message.text
            waiting_for_mark_g = False
            query_insert = 'INSERT INTO marks (id_task, mark_priority) VALUES (%s, %s)'
            values_insert = (task_id, mark)
            db_manager.execute_query(query_insert, values_insert)
            db_manager.connection.commit()
            db_manager.disconnect()
    except :
        def err3(message):
            Your_diary_bot.send_message(message.chat.id,
                                        text="Упс, щось пішло не так. Перед тим як оцінити запис створіть його назву та опис. ( не забудьте видалити неповноцінний запис якщо такий випадково було створено)")

    @Your_diary_bot.message_handler(func=lambda message: message.text == "Оцінити пріоритетність групи")
    def markGroup(message):
        Your_diary_bot.send_message(message.chat.id, text="Оцініть важливість від 1 до 5")

class CloseTask(User) :
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Обрати запис")
    def choiseTask(message):
        Your_diary_bot.send_message(message.chat.id, text="Виберіть номер групи зі списку")
        Your_diary_bot.send_message(message.chat.id, text="Виберіть номер запису зі списку")
        Your_diary_bot.send_message(message.chat.id, text="Видалити разом із групою ?")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Коментар до виконання")
    def comentEnd(message):
        Your_diary_bot.send_message(message.chat.id, text="Опишіть процес та результат")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Оцінити виконання")
    def markEnd(message):
        Your_diary_bot.send_message(message.chat.id, text="Як ви впорались із цим завданням від 1 до 10?")
    @Your_diary_bot.message_handler(func=lambda message: message.text == "Завершити")
    def end(message):
        Your_diary_bot.send_message(message.chat.id, text="Дякую за відгук, завдання завершено, можемо повертатись до головного меню")


Your_diary_bot.polling(none_stop=True)
