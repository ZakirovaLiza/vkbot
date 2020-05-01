from bot import Bot
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

TOKEN = '006f989c1dd87a457b8ba00b6533668a97d9a3b6b51ba8c5087883149a4a9f319d7586bc88763f0359903'
bot = Bot()


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 194882917)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            vk.messages.send(peer_id=event.object.peer_id,
                             message=bot.get_command(event.obj.message['text']),
                             random_id=random.randint(0, 2 ** 64),
                             user_id=event.obj.message['from_id'])


if __name__ == '__main__':
    main()
