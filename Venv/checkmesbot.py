import telebot
from telebot import types
import pygsheets
import pandas as pd
import openpyxl

token = "5802628594:AAEqIAgZ2960dOSK-hEJyc5_kyU5FbacXxg"
checkmesbot = telebot.TeleBot(token)
gc = pygsheets.authorize(
            service_file=r'C:\Users\yaski\PycharmProjects\TeleBotcheckmes\Venv\checkmesbot-3efa4551c701.json') # authorization

@checkmesbot.message_handler(func=lambda message: True)
@checkmesbot.message_handler(regexp="@")
def handle_message(message):
    pec = message.text
    sh = gc.open(r'checkmesbot')

    def calc(pec):
        list = []

        for poc in pec.split():
            if (poc.startswith("@")):
                list.append(poc)
                print(poc)

        wks = sh[0]
        header = wks.cell('A1')
        header.value = 'mes'
        wks.append_table(list, start='A2')

    loc = calc(pec)
    loc

    return print('ok')

checkmesbot.infinity_polling()
checkmesbot.polling(none_stop=True, interval=0)