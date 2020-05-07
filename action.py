from bot import Bot
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from data import db_session
from data.notes import Note
from data.bdays import Bday
import schedule
import datetime
import requests

TOKEN = '006f989c1dd87a457b8ba00b6533668a97d9a3b6b51ba8c5087883149a4a9f319d7586bc88763f0359903'
bot = Bot()
to_write_note = False
today = datetime.date(month=2, day=29, year=4)


def main():
    db_session.global_init("db/notes.sqlite")
    db_session.global_init("db/bdays.sqlite")
    global to_write_note
    global today
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
            elif bot.update_command(event.obj.message['text'], event.obj.message['from_id'])[0] != 'map_mode':
                print(666)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=bot.update_command(event.obj.message['text'], event.obj.message['from_id']),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                answer = bot.update_command(event.obj.message['text'], event.obj.message['from_id'])
                answer[1] = '+'.join(answer[1].split(' '))
                print(666)
                geocoder_request = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json'.format(
                    answer[1])
                response = requests.get(geocoder_request)
                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_coodrinates = toponym["Point"]["pos"]
                    map_request = f"http://static-maps.yandex.ru/1.x/?" \
                        f"ll={','.join(toponym_coodrinates.split(' '))}&" \
                        f"spn=0.002,0.002&l={answer[2][0]}&z={answer[2][1]}"
                    response = requests.get(map_request)
                    if response:
                        map_file = "map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('map.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         random_id=random.randint(0, 2 ** 64), attachment=attachment)
                    else:
                        print("Ошибка выполнения запроса:")
                        print(map_request)
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Ошибка выполнения запроса. Попробуйте ещё раз. 2',
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    print("Ошибка выполнения запроса:")
                    print(geocoder_request)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Ошибка выполнения запроса. Попробуйте ещё раз. 1',
                                     random_id=random.randint(0, 2 ** 64))
            session = db_session.create_session()
            s = []
            for el in session.query(Bday).filter(Bday.id_user == event.obj.message['from_id']):
                s.append(el)
            for el in s:
                if datetime.date.today().month == int(el.month) and datetime.date.today().day == int(
                        el.day) and today.day != int(el.day) and today.month != int(el.month):
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='{} сегодня празднует свой день рождения. Не забудь поздравить!'.format(
                                         el.name),
                                     random_id=random.randint(0, 2 ** 64))
            today = datetime.date.today()
            session.commit()

if __name__ == '__main__':
    main()