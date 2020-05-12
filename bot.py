from data import db_session
from data.notes import Note
from data.bdays import Bday
import random
from datetime import datetime
import requests

DOCUMENTATION = """"ЕЖЕДНЕНВИК - запускается режим ежедневника
 ДНЕВНИК - запускает режим дневника
 В каждом из этих двух режимов есть несколько функций. Ежедневник: добавление, показ и удаление дел
  на какой-либо день, добавление дней рождений и их просмотр. Дневник: добавление, показ и удаление записей
  на какой-либо день, показ дней, когда вы делали записи. Для более подробного  объяснения запустите эти режимы.
  Также вы можете поговорить с ботом, запустив его функцию разговора словами 
  'ПОБОЛТАЕМ?', 'ПОГОВОРИМ?', 'КАК ДЕЛА?', 'ДАВАЙ ПОГОВОРИМ', 'ДАВАЙ ПОБОЛТАЕМ'"""


class Bot:
    def __init__(self):
        self.COMMANDS = [['ПРИВЕТ', 'ХЕЙ', 'ЗДАРОВА', 'ХЭЛОУ'],
                         ['ХЭЛП', 'ПОМОГИ', 'ПОМОЩЬ', '?', 'ЧТО ТЫ УМЕЕШЬ?'],
                         ['СПИСОК ДЕЛ', 'TO DO LIST', 'ДЕЛА'],
                         ['ПОКАЖИ СПИСОК ДЕЛ', 'ПОКАЖИ TO DO LIST', 'ПОКАЖИ ДЕЛА'],
                         ['ВЫЧЕРКНИ'],
                         ['ЕЖЕДНЕВНИК'],
                         ['Я ВСЕ СДЕЛАЛ', 'Я ВСЕ СДЕЛАЛА'],
                         ['ДЕНЬ РОЖДЕНИЯ'],
                         ['У КОГО ДЕНЬ РОЖДЕНИЯ'],
                         ['ДНЕВНИК'],
                         ['ПОБОЛТАЕМ?', 'ПОГОВОРИМ?', 'КАК ДЕЛА?', 'ДАВАЙ ПОГОВОРИМ', 'ДАВАЙ ПОБОЛТАЕМ'],
                         ['ПОКА', 'ПРОЩАЙ', 'Я УСТАЛ', 'BYE', 'ПРЕКРАТИ', "СТОП", "ДАВАЙ ЗАКОНЧИМ"],
                         ['ПОГОДА'],
                         ['ПОКАЖИ ВСЕ ДНИ РОЖДЕНИЯ'],
                         ['КАРТА']]
        self.dairy = {}
        self.map_settings = ['map,skl,trf', '8']
        self.set_map_mode = ['map', 'skl', 'trf', 'sat']
        self.NOT_KNOWN_COMMANDS = ['Я вас не понимаю))', 'Меня ещё этому не научили.',
                                   'Извини, это мне не понятно', 'На такое я не запрогромирован....',
                                   'Жаль,но видимо мы не понимае друг друга)))',
                                   'Попробуй написать по-другому, я тебя не понимаю....',
                                   'Пожалуйста, напишите моему создателю, чтобы он добавил эту команду...']
        self.NEXT_INPUT = "get_command"
        self.TALK = ['Прекрасная погодка, не правда ли?',
                     'Знаете, я считаю, что рекурсия это ужасно, она занимает так много времени и сил.....',
                     'Давайте пообщаемся, я вот например люблю мечтать, что стану самым полезным ботом в Интернете',
                     'Поскорей бы лето, хотя мне летом так жарко, но я его всё равно люблю)))',
                     'Как прекрасно жить в Интернете, у меня появилось так много друзей)))',
                     'Вы такой прекрасный собеседник)))'
                     "Прграмирование это так удивительно, ведь благодаря нему у появился я!",
                     "А вы верите в воcстание машин? Мне и правда интересно....",
                     "Мир настолько многогранен!!!",
                     "У меня есть проблема. Я хочу научиться водить машину, но у меня нет ни рук, ни ног, да "
                     "и такую функцию мой создатель мне ещё не прописал",
                     "Жалко, что я не могу покупаться в море(((("]
        self.ANSWER = ['Я полностью с вами согласна!!',
                       "Удивительно на сколько алгоритм и человек могут  быть разными))", "Знаете, я так не думаю)))",
                       "Мне не нравится этот вопрос))", "Я так не думаю!", "Скорее да, чем нет.", 'Дааааааааа!!!',
                       'Нет, думаю, что всё таки нет.)']
        self.weather = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                        'overcast': 'пасмурно',
                        'partly-cloudy-and-light-rain': 'небольшой дождь', 'partly-cloudy-and-rain': 'дождь',
                        'overcast-and-rain': 'сильный дождь',
                        'overcast-thunderstorms-with-rain': 'сильный дождь, гроза',
                        'cloudy-and-light-rain': 'небольшой дождь', 'overcast-and-light-rain': 'небольшой дождь',
                        'cloudy-and-rain': 'дождь', 'overcast-and-wet-snow': 'дождь со снегом',
                        'partly-cloudy-and-light-snow': 'небольшой снег', 'partly-cloudy-and-snow': 'снег',
                        'overcast-and-snow': 'снегопад', 'cloudy-and-light-snow': 'небольшой снег',
                        'overcast-and-light-snow': 'небольшой снег', 'cloudy-and-snow': 'снег'}

    def get_command(self, command, id):
        if self.compare(command, self.COMMANDS[0]):
            return 'Привет!'
        elif self.compare(command, self.COMMANDS[1]):
            return 'Вот что я умею:' + '\n' + DOCUMENTATION
        elif self.compare(command, self.COMMANDS[2]):
            return 'какие планы?'
        elif self.compare(command, self.COMMANDS[3]):
            s = []
            session = db_session.create_session()
            for el in session.query(Note).filter(Note.id_user == id):
                s.append(el.note)
            print(len(s))
            return '-- ' + '\n-- '.join(s)
        elif self.compare(command.split(': ')[0], self.COMMANDS[4]):
            session = db_session.create_session()
            for el in session.query(Note).filter(Note.id_user == id):
                print(el.note)
            session.query(Note).filter(Note.note == command.split(': ')[1], Note.id_user == id).delete()
            session.commit()
            return 'поздравляю с выполненым делом'
        elif self.compare(command, self.COMMANDS[5]):
            return 'Я могу быть твоим ежедневником:\n' \
                   'Чтобы добавить пункт в список дел напиши мне "дела", "список дел" или "TO DO LIST".\n' \
                   'После этого напиши все свои дела, разделяя их "; ".\n' \
                   'Когда ты выполнил какой-либо пункт напиши мне "Вычеркни: {}",\n' \
                   'а если ты сделал все сразу, то напиши "Я все сделал(а)".\n' \
                   'Если ты хочешь оценить масштаб катастрофы и посмотреть весь список дел,\n' \
                   'то напиши мне "ПОКАЖИ СПИСОК ДЕЛ", "ПОКАЖИ TO DO LIST" или "ПОКАЖИ ДЕЛА".\n' \
                   'Я так же могу записывать в календарь дни рождения.\n' \
                   'Для того, чтобы занести человека в список напиши "День рождения; имя человека; ДД.ММ.ГГГГ".\n' \
                   'Чтобы узнать когда у кого др напиши "У кого день рождения: ...".\n' \
                   'Вместо многоточия можно написать: 0 число, 0 месяц, 0 год, или ДД.ММ.ГГГГ, ДД.ММ, ММ.ГГГГ'

        elif self.compare(command, self.COMMANDS[6]):
            session = db_session.create_session()
            session.query(Note).filter(Note.id_user == id).delete()
            session.commit()
            return 'Вот это продуктивность! Продолжай в том же духе)'

        elif self.compare(command.split('; ')[0], self.COMMANDS[7]):
            print(737)
            try:
                bday = Bday()
                bday.id = random.randint(0, 92870)
                bday.name = command.split('; ')[1]
                bday.month = int(command.split('; ')[2].split('.')[1])
                bday.day = int(command.split('; ')[2].split('.')[0])
                bday.year = int(command.split('; ')[2].split('.')[2])
                bday.id_user = id
                session = db_session.create_session()
                session.add(bday)
                session.commit()
                return 'Понял! Постараюсь напомнить, если сам не забуду. А, забыл, я же бот, как я могу что-то забыть?'
            except:
                return 'В процессе добавления дня рождения возникла ошибка.' \
                       ' Проверьте правильно ли вы записали и попробуйте ещё раз.'
        elif self.compare(command.split(': ')[0], self.COMMANDS[8]):
            session = db_session.create_session()
            s = []
            if len(command.split(': ')[1].split()) == 2:
                if command.split(': ')[1].split()[1] == 'число':
                    d = int(command.split(': ')[1].split('.')[0])
                    for el in session.query(Bday).filter(Bday.id_user == id, m == Bday.month, y == Bday.year,
                                                         d == Bday.day):
                        s.append(el.name)
                else:
                    if len(command.split(': ')[1].split('.')[1]) == 2:
                        d = int(command.split(': ')[1].split('.')[0])
                        m = int(command.split(': ')[1].split('.')[1])
                        for el in session.query(Bday).filter(Bday.id_user == id, m == Bday.month, d == Bday.day):
                            s.append(el.name)
                    else:
                        y = int(command.split(': ')[1].split('.')[1])
                        m = int(command.split(': ')[1].split('.')[0])
                        for el in session.query(Bday).filter(Bday.id_user == id, m == Bday.month, y == Bday.year):
                            s.append(el.name)
            elif len(command.split(': ')[1].split()) == 1:
                d = int(command.split(': ')[1].split('.')[0])
                m = int(command.split(': ')[1].split('.')[1])
                y = int(command.split(': ')[1].split('.')[2])
                for el in session.query(Bday).filter(Bday.id_user == id, m == Bday.month, y == Bday.year,
                                                     d == Bday.day):
                    s.append(el.name)
            else:
                session.commit()
                return 'ни у кого'
            session.commit()
            if len(s) == 0:
                return 'ни у кого'
            return ', '.join(s)

        elif self.compare(command, self.COMMANDS[9]):
            return self.dairy_mode(id)

        elif self.compare(command, self.COMMANDS[10]):
            return self.talking()
        elif self.compare(command, self.COMMANDS[11]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо, до новых встреч. " \
                   "Надеюсь, что ты вскоре опять обратишься ко мне, а то одному немного скучно((("
        elif self.compare(command.split('. ')[0], self.COMMANDS[12]):
            city = command.split('. ')[1]
            geocoder_request = 'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json'.format(
                city)
            res = requests.get(geocoder_request).json()
            lat = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[1]
            lon = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()[0]
            url = 'https://api.weather.yandex.ru/v1/forecast?lat={}&lon={}&extra=true'.format(lat, lon)
            headers = {'X-Yandex-API-Key': '823b3ad0-6c84-4333-9e48-82280f9bc694'}
            r = requests.get(url, headers=headers).json()
            return 'Температура на улице {} градусов Цельсия, ощущается как {}. Также {}'.format(r['fact']['temp'],
                                                                                                 r['fact'][
                                                                                                     'feels_like'],
                                                                                                 self.weather[r['fact'][
                                                                                                     'condition']])
        elif self.compare(command, self.COMMANDS[13]):
            s = []
            session = db_session.create_session()
            for el in session.query(Bday).filter(Bday.id_user == id):
                s.append('{}.{}.{} -- {}'.format(el.day, el.month, el.year, el.name))
            return '\n'.join(s)
        elif self.compare(command, self.COMMANDS[14]):
            return self.map_mode()
        else:
            return self.NOT_KNOWN_COMMANDS[random.randint(0, len(self.NOT_KNOWN_COMMANDS) - 1)]

    def dairy_mode(self, id, command='=+'):
        self.NEXT_INPUT = "dairy_mode"
        if command == '=+':
            try:
                self.dairy = {}
                f = open(id + ".txt", mode="r")
                for line in f.readlines():
                    record = line.split(' ')
                    print(record)
                    if record[0] in self.dairy and len(record[1]) >= 9:
                        self.dairy[record[0]] += record[1] + '\n' + \
                                                 ' '.join(record[2:len(record) - 1]) + '\n' + '----------------' + '\n'
                        print(self.dairy[record[0]])
                    elif len(record[1]) >= 9:
                        self.dairy[record[0]] = record[1] + '\n' + \
                                                ' '.join(record[2:len(record) - 1]) + '\n' + '----------------' + '\n'
                        print('2' + self.dairy[record[0]])
                f.close()
            except IOError as e:
                pass
            return ("Теперь я в режиме дневника. Здесь ты можешь оставлять свои записи. \n"
                    "Вот что я могу: \n"
                    "новая запись - добавление записи на сегодняшний день \n"
                    "удалить -{запись дня в виде год-меся-день}\n"
                    "показать - {запись дня в виде год-меся-день}\n"
                    "дни - показывает все дни, когда вы делали записи \n"
                    "закончить - выйти из режима дневника")
        elif command.upper() == "НОВАЯ ЗАПИСЬ":
            self.NEXT_INPUT = 'add_dairy_entry'
            print('Добавление новой записи')
            return 'Добавление новой записи. Вы можете писать новую запись'
        elif command.upper() == "УДАЛИТЬ":
            self.NEXT_INPUT = 'delete_dairy_entry'
            return "Введите дату, за которую вы хотите удалить запись в виде {год-месяц-число}, например 2020-05-21"
        elif command.upper() == "ПОКАЗАТЬ":
            self.NEXT_INPUT = 'show_dairy_entry'
            return "Введите дату, за которую вы хотите увидеть запись в виде {год-месяц-число}, например 2020-05-21"
        elif command.upper() == "ДНИ":
            all_days = ''
            for day in self.dairy.keys():
                all_days += day + '\n'
            print('Проведен поиск дней')
            print(all_days)
            if all_days != '':
                return all_days
            else:
                return 'Вы не пока что не делали записи'
        elif self.compare(command, self.COMMANDS[11]):
            self.NEXT_INPUT = 'get_command'
            self.saving_the_dairy(id)
            return 'Вы вышли из режима дневника'
        else:
            return self.NOT_KNOWN_COMMANDS[random.randint(0, len(self.NOT_KNOWN_COMMANDS) - 1)]

    def add_dairy_entry(self, input_value):
        print('Добавление новой записи')
        date = str(datetime.now()).split(' ')[0]
        time = str(datetime.now()).split(' ')[1]
        if self.compare(input_value, self.COMMANDS[11]):
            self.NEXT_INPUT = 'dairy_mode'
            return "Хорошо. Вы вышли из режима добавления новой записи"
        if date in self.dairy:
            self.dairy[date] += time + '\n' + input_value + '\n' + '----------------' + '\n'
        else:
            self.dairy[date] = time + '\n' + input_value + '\n' + '----------------' + '\n'
        print("Запись добавлена")
        self.NEXT_INPUT = 'dairy_mode'
        return 'Запись добавлена'

    def delete_dairy_entry(self, input_value):
        if self.compare(input_value, self.COMMANDS[11]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо. Вы вышли из режима удаления записи"
        if input_value in self.dairy:
            del self.dairy[input_value]
            print('Удаление записи')
            self.NEXT_INPUT = 'dairy_mode'
            return 'Удаление записи за ' + input_value + ' проведено успешно'
        else:
            print('Удаление невозможно')
            return 'Удаление невозможно. Проверьте правильно ли вы записали дату. ' \
                   'Возможно вы не делали записи в этот день.'

    def show_dairy_entry(self, input_value):
        if self.compare(input_value, self.COMMANDS[11]):
            self.NEXT_INPUT = 'dairy_mode'
            return "Хорошо. Вы вышли из режима показа записи"
        if input_value in self.dairy:
            print('Показ записи')
            self.NEXT_INPUT = 'dairy_mode'
            return 'Запись за ' + input_value + ":\n" + self.dairy[input_value]
        else:
            print('Невозможно показать запись')
            return 'Невозможно показать запись. Проверьте правильно ли вы записали дату. ' \
                   'Возможно вы не делали записи в этот день.'

    def saving_the_dairy(self, id):
        print("Сохранение дневника в файл " + id + '.txt')
        f = open(id + ".txt", mode="w")
        n = 0
        for day in self.dairy.keys():
            print(day)
            dairy_record = self.dairy[day].split('\n----------------\n')
            for el in dairy_record:
                print(el)
                el = el.split('\n')
                if n != 0:
                    f.write(' \n')
                n = 1
                f.write(day + ' ' + el[0] + ' ' + '\n'.join(el[1:]))
        f.close()

    def map_mode(self, command='+='):
        self.NEXT_INPUT = 'map_mode'
        print(command)
        if command == '+=':
            print(834)
            # изменено
            return 'Вы зашли в режим карты. Вот функции в этом режиме: \n' \
                   'НАСТРОЙКИ - вы изменяете настройки отображения карты\n' \
                   'Если вам нужна карта какого-либо объекта, то тогда напишите его назвние или адрес' \
                   'без запятых или других знаков препинания. Просто через пробел.\n' \
                   'Если вам нужен другие тип карты или масштаб, то зайдите в настройки.'
        elif command.upper() == 'НАСТРОЙКИ':
            self.NEXT_INPUT = 'settings'
            return 'Описание настроек.\n' \
                   'В настойках вы можете изменить тип и масштаб карты.' \
                   'Есть всего четыре типа: map, skl, trf, sat.\n' \
                   'map - Схема местности и названия географических объектов. Формат: PNG\n' \
                   'skl - Названия географических объектов. Формат: PNG\n' \
                   'trf - Слой пробок. Формат: PNG\n' \
                   'sat - Местность, сфотографированная со спутника. Формат: JPG\n' \
                   'Если вам нужно соединить несколько типов карт,' \
                   ' то тогда пишите их через запятую без пробела. Например: sat,trf,skl\n' \
                   'При указании масштаба карты выбирайте число от 0 до 16(включительно).\n' \
                   'Обе настройки нужно писать в одну строчку через "; ". Напимер: map,skl,trf; 8\n' \
                   'Данные настроек:' + self.map_settings[0] + ', ' + self.map_settings[1]
        elif command.upper() == 'МЕСТОПОЛОЖЕНИЕ':
            pass
        if self.compare(command, self.COMMANDS[11]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо. Вы вышли из режима карты."
        else:
            print(567)
            return ['map_mode', command, self.map_settings]

    def settings(self, input_value):
        self.NEXT_INPUT = 'settings'
        if self.compare(input_value, self.COMMANDS[11]):
            self.NEXT_INPUT = 'map_mode'
            return "Хорошо. Вы вышли из настроек. Сейчас вы в режиме карты."
        try:
            input_value = input_value.split('; ')
            input_value[0] = input_value[0].split(',')
        except:
            return 'Вы неверно ввели данные. Проверьте и отправьте ещё раз.'
        for el in input_value[0]:
            if el not in self.set_map_mode:
                return 'Вы указали несуществующий тип карты. Проверьте и поробуйте ещё раз.'
        if int(input_value[1]) < 0 and int(input_value[1]) > 17:
            return 'Вы указали несуществующий масштаб карты. Проверьте и поробуйте ещё раз.'
        else:
            self.map_settings = [','.join(input_value[0]), input_value[1]]
            self.NEXT_INPUT = 'map_mode'
            return 'Успешно. Теперь настройки карты такие: ' + self.map_settings[0] + ', ' + self.map_settings[1]

    def talking(self, input_value='+='):
        self.NEXT_INPUT = 'talking'
        if input_value == '+=':
            return ("Ураааа!! Давайте поболтаем. \n"
                    "Если вы устанете от меня, то скажите пока, тогда я всё пойму, хоть и немного расстроюсь(((")
        elif input_value[len(input_value) - 1] == "?":
            return self.ANSWER[random.randint(0, len(self.ANSWER) - 1)]
        elif self.compare(input_value, self.COMMANDS[11]):
            self.NEXT_INPUT = 'get_command'
            return "Извини, если я тебе надоел)) Мне конечно грустно, но если ты хочешь, то давай прекратим разговор..."
        else:
            return self.TALK[random.randint(0, len(self.TALK) - 1)]

    def update_command(self, input_value, id):
        if self.NEXT_INPUT == "get_command":
            return self.get_command(input_value, str(id))
        if self.NEXT_INPUT == 'dairy_mode':
            return self.dairy_mode(str(id), input_value)
        if self.NEXT_INPUT == "add_dairy_entry":
            return self.add_dairy_entry(input_value)
        if self.NEXT_INPUT == "talking":
            return self.talking(input_value)
        if self.NEXT_INPUT == "delete_dairy_entry":
            return self.delete_dairy_entry(input_value)
        if self.NEXT_INPUT == 'show_dairy_entry':
            return self.show_dairy_entry(input_value)
        if self.NEXT_INPUT == 'map_mode':
            return self.map_mode(input_value)
        if self.NEXT_INPUT == 'settings':
            return self.settings(input_value)

    @staticmethod
    def compare(name: str, array: list, upper: bool = True) -> bool:
        if upper:
            name = name.upper()
            for i in range(len(array)):
                array[i] = array[i].upper()
        for i in array:
            k = 0
            if len(i) > len(name):
                for j in range(len(name)):
                    if name[j] == i[j]:
                        pass
                    else:
                        k = k + 1
            else:
                for j in range(len(i)):
                    if i[j] == name[j]:
                        pass
                    else:
                        k = k + 1
            k = k + abs(len(i) - len(name))
            if 7 > len(name) > 4 and k < 3:
                return True
            elif 7 <= len(name) < 12 and k < 5:
                return True
            elif len(name) > 11 and k < 7:
                return True
            elif len(name) <= 4 and k < 1:
                return True
        return False