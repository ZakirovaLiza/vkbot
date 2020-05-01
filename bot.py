class Bot:
    def __init__(self):
        self.COMMANDS = [['ПРИВЕТ', 'ХЕЙ', 'ЗДАРОВА', 'ХЭЛОУ'],
                         ['ХЭЛП', 'ПОМОГИ', 'ПОМОЩЬ', '?', 'ЧТО ТЫ УМЕЕШЬ?']]

    def get_command(self, command):
        if self.compare(command, self.COMMANDS[0]):
            return 'Привет!'

        elif self.compare(command, self.COMMANDS[1]):
            return 'Вот что я умею'

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
