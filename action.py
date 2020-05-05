from bot import Bot
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from data import db_session
from data.notes import Note
from data.bdays import Bday
import schedule
import datetime

TOKEN = '006f989c1dd87a457b8ba00b6533668a97d9a3b6b51ba8c5087883149a4a9f319d7586bc88763f0359903'
bot = Bot()
to_write_note = False


def main():
    db_session.global_init("db/notes.sqlite")
    db_session.global_init("db/bdays.sqlite")
    global to_write_note
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 194882917)

    for event in longpoll.listen():
        vk = vk_session.get_api()
        if event.type == VkBotEventType.MESSAGE_NEW and to_write_note:
            to_write_note = True
            for el in event.obj.message['text'].split(';'):
                user = Note()
                user.id_user = event.obj.message['from_id']
                user.note = el
                user.id = random.randint(0, 932)
                session = db_session.create_session()
                session.add(user)
                session.commit()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message='Добавил в список дел!',
                             random_id=random.randint(0, 2 ** 64))
            to_write_note = False
        elif event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            if event.obj.message['text'].upper() == 'список' or event.obj.message['text'].upper() == 'TO DO LIST' or \
                    event.obj.message['text'].upper() == 'ДЕЛА':
                to_write_note = True
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=bot.get_command(event.obj.message['text'], event.obj.message['from_id']),
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
