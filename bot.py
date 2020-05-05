from data import db_session
from data.notes import Note
from data.bdays import Bday
import random


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
                         ['У КОГО ДЕНЬ РОЖДЕНИЯ']]

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
