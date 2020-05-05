from data import db_session
from data.notes import Note
from data.bdays import Bday
import random
from datetime import datetime


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
                         ['ПИСЬМО В БУДУЩЕЕ', "ХОЧУ НАПИСАТЬ ПИСЬМО В БУДУЩЕЕ", "ПИСЬМО", "НАПИСАТЬ ПИСЬМО"],
                         ['ПОБОЛТАЕМ?', 'ПОГОВОРИМ?', 'КАК ДЕЛА?', 'ДАВАЙ ПОГОВОРИМ', 'ДАВАЙ ПОБОЛТАЕМ'],
                         ['ПОКА', 'ПРОЩАЙ', 'Я УСТАЛ', 'BYE', 'ПРЕКРАТИ', "СТОП", "ДАВАЙ ЗАКОНЧИМ"]]
        self.dairy = {}
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
                     "А вы верите в воcстаниие машин? Мне и правда интересно....",
                     "Мир настолько многогранен!!!",
                     "У меня есть проблема. Я хочу научиться водить машину, но у меня нет ни рук, ни ног, да "
                     "и такую функцию мой создатель мне ещё не прописал",
                     "Жалко, что я не могу покупаться в море(((("]
        self.ANSWER = ['Я полностью с вами согласна!!',
                       "Удивительно на сколько алгоритм и человек могут  быть разными))", "Знаете, я так не думаю)))",
                       "Мне не нравится этот вопрос))", "Я так не думаю!", "Скорее да, чем нет."]

    def get_command(self, command, id):
        if self.compare(command, self.COMMANDS[0]):
            return 'Привет!'

        elif self.compare(command, self.COMMANDS[1]):
            return 'Вот что я умею'

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

        elif self.compare(command.split(': ')[0], self.COMMANDS[8]):
            session = db_session.create_session()
            s = []
            if len(command.split(': ')[1].split()) == 2:
                if command.split(': ')[1].split()[1] == 'число':
                    for el in session.query(Bday).filter(Bday.id_user == id,
                                                         int(command.split(': ')[1].split()[0]) == Bday.day):
                        s.append(el.name)
                elif command.split(': ')[1].split()[1] == 'месяц':
                    for el in session.query(Bday).filter(Bday.id_user == id,
                                                         int(command.split(': ')[1].split()[0]) == Bday.month):
                        s.append(el.name)
                elif command.split(': ')[1].split()[1] == 'год':
                    for el in session.query(Bday).filter(Bday.id_user == id,
                                                         int(command.split(': ')[1].split()[0]) == Bday.year):
                        s.append(el.name)
            elif len(command.split(': ')[1].split()) == 1:
                if len(command.split(': ')[1].split('.')) == 3:
                    y = int(command.split(': ')[1].split('.')[2])
                    m = int(command.split(': ')[1].split('.')[1])
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
            else:
                session.commit()
                return 'ни у кого'
            session.commit()
            if len(s) == 0:
                return 'ни у кого'
            return ', '.join(s)

        elif self.compare(command, self.COMMANDS[9]):
            return self.dairy_mode()

        elif self.compare(command, self.COMMANDS[10]):
            return "Письмо в будущее отправлено!"

        elif self.compare(command, self.COMMANDS[11]):
            return self.talking()

        elif self.compare(command, self.COMMANDS[12]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо, до новых встреч. " \
                   "Надеюсь, что ты вскоре опять обратишься ко мне, а то одному немного скучно((("
        else:
            return self.NOT_KNOWN_COMMANDS[random.randint(0, len(self.NOT_KNOWN_COMMANDS) - 1)]

    def add_dairy_entry(self, input_value):
        print('Добавление новой записи')
        date = str(datetime.now()).split(' ')[0]
        time = str(datetime.now()).split(' ')[1]
        if self.compare(input_value, self.COMMANDS[5]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо. Вы вышли из режима добавления новой записи"
        if date in self.dairy:
            self.dairy[date] += time + '\n' + input_value + '\n' + '----------------' + '\n'
        else:
            self.dairy[date] = time + '\n' + input_value + '\n' + '----------------' + '\n'
        print("Запись добавлена")
        self.NEXT_INPUT = 'dairy_mode'
        return 'Запись добавлена'

    def delete_dairy_entry(self, input_value):
        if self.compare(input_value, self.COMMANDS[5]):
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
        if self.compare(input_value, self.COMMANDS[5]):
            self.NEXT_INPUT = 'get_command'
            return "Хорошо. Вы вышли из режима показа записи"
        if input_value in self.dairy:
            print('Показ записи')
            self.NEXT_INPUT = 'dairy_mode'
            return 'Запись за ' + input_value + ":\n" + self.dairy[input_value]
        else:
            print('Невозможно показать запись')
            return 'Невозможно показать запись. Проверьте правильно ли вы записали дату. ' \
                   'Возможно вы не делали записи в этот день.'

    def talking(self, input_value='+='):
        self.NEXT_INPUT = 'talking'
        if input_value == '+=':
            return ("Ураааа!! Давайте поболтаем. \n"
                    "Если вы устанете от меня, то скажите пока, тогда я всё пойму, хоть и немного расстроюсь(((")
        elif input_value[len(input_value) - 1] == "?":
            return self.ANSWER[randdom.randint(0, len(self.ANSWER) - 1)]
        elif self.compare(input_value, self.COMMANDS[5]):
            self.NEXT_INPUT = 'get_command'
            return "Извини, если я тебе надоел)) Мне конечно грустно, но если ты хочешь, то давай прекратим разговор..."
        else:
            return self.TALK[random.randint(0, len(self.TALK) - 1)]

    def update_command(self, input_value):
        if self.NEXT_INPUT == "get_command":
            return self.get_command(input_value)
        if self.NEXT_INPUT == 'dairy_mode':
            return self.dairy_mode(input_value)
        if self.NEXT_INPUT == "add_dairy_entry":
            return self.add_dairy_entry(input_value)
        if self.NEXT_INPUT == "talking":
            return self.talking(input_value)
        if self.NEXT_INPUT == "delete_dairy_entry":
            return self.delete_dairy_entry(input_value)
        if self.NEXT_INPUT == 'show_dairy_entry':
            return self.show_dairy_entry(input_value)



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
