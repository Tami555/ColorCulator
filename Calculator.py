import math
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from string import digits
import sys


class Colorculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('color_culator.ui', self)
        self.setFixedSize(418, 640)
        self.second_input.setText('0')
        self.count_mains = ['0']
        self.use_sign = False
        self.main_symbols = ('-', '+', '/', '*', '%', '**')

        self.buttons_num()
        self.buttons_symbols()
        self.count_brackets = 0

    def buttons_num(self):
        """Добавляет функцию numbers ко всем числам"""
        buttons = [self.num_0, self.num_1, self.num_2, self.num_3, self.num_4, self.num_5,
                   self.num_6, self.num_7, self.num_8,self.num_9]
        for b in buttons:
            b.clicked.connect(self.numbers)

    def buttons_symbols(self):
        """Все функции и их кнопки"""
        buttons = [self.btn_divide, self.btn_multipy, self.btn_minus, self.btn_plus, self.btn_point,
                   self.btn_procent, self.btn_stepen,]
        for b in buttons:
            b.clicked.connect(self.symbols)

        self.btn_equally.clicked.connect(self.equally)
        self.btn_c.clicked.connect(self.clear_C)
        self.btn_ce.clicked.connect(self.clear_CE)
        self.btn_plus_minus.clicked.connect(self.minus_plus)
        self.btn_factorial.clicked.connect(self.factorial)
        self.btn_coren.clicked.connect(self.mat_sqrt)
        self.btn_sin.clicked.connect(self.trigonometric_functions)
        self.btn_cos.clicked.connect(self.trigonometric_functions)
        self.btn_open.clicked.connect(self.main_brakets)
        self.btn_close.clicked.connect(self.main_brakets)

    def get_text_main_to_second(self):
        """Из главного массива отображает в верхней строке все выражение"""
        text_s = ''.join([x if x not in self.main_symbols else ' ' + x + ' ' for x in self.count_mains])
        self.second_input.setText(text_s)

    def numbers(self):
        """Функция для чисел"""
        num = self.sender().text()
        if self.count_mains[-1] not in (')', '!', ']'):
            if self.count_mains[0] == '0' and len(self.count_mains) == 1 or \
                    (len(self.count_mains) > 1 and self.count_mains[-1] == '0' and self.count_mains[-2] == '('):
                self.main_input.setText('')
                self.count_mains.pop()

            elif self.count_mains[-1] == '0' and self.count_mains[-2] in (*self.main_symbols, 'K'):
                if self.count_mains[-2] == 'K':
                    self.main_input.setText(self.main_input.text()[:-1])
                else:
                    self.main_input.setText('')
                self.count_mains.pop()

            elif self.use_sign or (self.count_mains[-1] == '(' and self.main_input.text() == '0'):
                self.main_input.setText('')
                self.use_sign = False

            text_m = self.main_input.text()
            self.main_input.setText(text_m + num)
            self.count_mains.append(num)
            self.get_text_main_to_second()

    def symbols(self):
        """Функция для арифметических знаков и точки"""
        if self.main_input.text() == 'Error':
            self.main_input.setText('0')

        last = self.count_mains[-1]
        if (last in digits) or last in ('', ')', '!', ']') and last != '.':
            self.use_sign = True

            symbol = self.sender().text()
            if symbol == '.':
                text_s = self.second_input.text()  # чтобы было в моменте
                text_m = self.main_input.text()

                if '.' not in text_m and self.count_mains[-1] not in (')', '!', ']'):
                    self.main_input.setText(text_m + symbol)
                    self.second_input.setText(text_s + symbol)
                    self.count_mains.append(symbol)
                self.use_sign = False

            else:
                if symbol == '÷':
                    symbol = '/'
                elif symbol == 'x':
                    symbol = '*'
                elif symbol == '^^':
                    symbol = '**'
                self.count_mains.append(symbol)
                self.get_text_main_to_second()

    def find_index_fisrt_bracets(self, start=-1, br='('):
        """" для поиска первой с конца '(' или '[' скобок"""
        index_1 = 0
        for x in range(start, -len(self.count_mains) - 1, -1):
            if self.count_mains[x] == br:
                index_1 = x
                break
        return index_1

    def find_index_last_bracets(self, start=0):
        """" для поиска первой с начала ')' """
        index_1 = 0
        for x in range(start, len(self.count_mains)):
            if self.count_mains[x] == ')':
                index_1 = x
                break
        return index_1

    def find_last_number(self, start=-1):
        """" для нахождения последнего числа от определ момента (с конца в начало <<-) """
        index_1 = -1
        for x in range(start, -len(self.count_mains) - 1, -1):
            if self.count_mains[x] in (*self.main_symbols, '(') and x != -len(self.count_mains):
                index_1 = x
                break
        return index_1 + 1

    def main_brakets(self):
        """ для поставления собственных скобок ()"""
        bracket = self.sender().text()
        try:
            if bracket == '(' and (self.count_mains[0] == '0' or self.count_mains[-1] in (*self.main_symbols, '(')):
                if self.count_mains[0] == '0':
                    self.main_input.setText('0')
                    self.count_mains.pop()
                else:
                    self.main_input.setText('0')

                self.count_brackets += 1
                self.count_mains.append(bracket)

            else:
                if bracket == ')' and self.count_brackets > 0:
                    if self.count_mains[-1] not in (*self.main_symbols, '.'):
                        self.count_mains.append(bracket)
                        self.count_brackets -= 1

            self.get_text_main_to_second()
        except Exception as e:
            print(e)

    def more_firs_bracket(self, first=-1, br='(', br2=')'):
        """ для нахождение последней открытой cкобки смотря на количество закрытых )) """
        index_bracket = self.find_index_fisrt_bracets(first, br)
        close_br = self.count_mains[index_bracket: first] if first != -1 else self.count_mains[index_bracket:]
        close_br = close_br.count(br2)
        open_br = 1

        while open_br != close_br:
            first = index_bracket - 1
            index_bracket = self.find_index_fisrt_bracets(first, br)
            open_br += 1
            close_br += self.count_mains[index_bracket:first].count(br2)
        return index_bracket

    def more_last_bracket(self, first=0):
        """ для нахождение последней открытой скобки смотря на количество закрытых )) """
        index_bracket = self.find_index_last_bracets(first)
        open_br = self.count_mains[first: index_bracket].count('(')
        close_br = 1

        while close_br != open_br:
            first = index_bracket + 1
            index_bracket = self.find_index_last_bracets(first)
            close_br += 1
            open_br += self.count_mains[first: index_bracket].count('(')
        return index_bracket

    def get_last_full_number(self):
        """ возвращает последнее число со всеми скобками и т.д и т.п"""
        start = 0
        # 1) для факториала положительного
        if self.count_mains[-1] == '!':
            if self.count_mains[-2] == ')':
                start = self.more_firs_bracket()

        # 2) для положительного числа
        elif self.count_mains[-1] in digits:
            start = self.find_last_number()

        # 3) для sin/cos
        elif self.count_mains[-1] == ']':
            start = self.more_firs_bracket(br='[', br2=']') - 1

        # 4) для отрицательных. корня. main скобок
        elif self.count_mains[-1] == ')':
            start = self.more_firs_bracket()
            if start != -(len(self.count_mains)) and self.count_mains[start - 1] == 'K':
                start -= 1
        # 5) для знака
        elif self.count_mains[-1] in self.main_symbols:
            start = -1

        element = self.count_mains[start:]
        return start, element

    def minus_plus(self):
        """Функция +- для смены знака числа"""
        if self.count_mains[-1] != '.':
            start, element = self.get_last_full_number()

            may = True
            if ((len(element) == 1 and element[0] == '0') or
                    (element[0] == '0' and len(element) > 1 and not any([x in '123456789' for x in element[1:]])) or
                    (len(element) > 1 and element[0] == '(' and element[1] == '0' and not
                        any([x in '123456789' for x in element[2:]])) or
                    (element[-1] == '(')):
                may = False

            # Начинаем преобразование
            if may:
                if element[0] in self.main_symbols:
                    element = element[0]
                    match element:
                        case '-':
                            element = '+'
                        case '+':
                            element = '-'
                        case '*':
                            element = '/'
                        case '/':
                            element = '*'
                    self.count_mains[-1] = element

                # либо отрицалка, main скобка, большой факториал
                elif element[0] == '(':

                    if element[1] == '-':
                        self.count_mains[start:] = element[2:-1]
                        self.main_input.setText(''.join(element[2:-1]))

                    elif element[-1] in (')', '!'):
                        self.count_mains[start:] = ['(', '-', *element, ')']
                        self.main_input.setText('(-' + ''.join(element) + ')')

                    elif element[-1] != ')':
                        self.count_mains[start:] = [element[0], '(', '-', *element[1:], ')']
                        self.main_input.setText(''.join(self.count_mains[start:]))

                else:
                    self.count_mains[start:] = ['(', '-', *element, ')']
                    self.main_input.setText('(-' + ''.join(element) + ')')

        self.get_text_main_to_second()

    def factorial(self):
        """Функция для поставки факториала 1.1"""
        if self.count_mains[-1] not in ('.', *self.main_symbols, '('):
            start, element = self.get_last_full_number()
            self.count_mains[start:] = ['(', *element, ')', '!']
            self.main_input.setText('(' + ''.join(element) + ')!')
            self.get_text_main_to_second()

    def for_factorial(self, index):
        """Функция для вычисления факториала 1.2"""
        negative_start = -(len(self.count_mains) - index)
        start = self.more_firs_bracket(negative_start)
        self.count_mains[start: index + 1] = ['math.factorial', *self.count_mains[start:index]]

    @staticmethod
    def integer(num: str):
        """Метод для корня; помогает сделать целым числом, дробные типа => 3.0 (для факториала)"""
        num = float(num)
        return str(int(num)) if num % 1 == 0 else str(num)

    def mat_sqrt(self):
        """Функция для поставки корня 2.1"""
        if self.count_mains[-1] not in ('.', *self.main_symbols, '('):
            start, element = self.get_last_full_number()

            if element[0] == '(' and element[-1] in digits:
                self.count_mains[start:] = [element[0], 'K', '(', *element[1:], ')']
                self.main_input.setText(''.join(self.count_mains[start:]))
            else:
                self.count_mains[start:] = ['K', '(', *element, ')']
                self.main_input.setText('K' + '(' + ''.join(element) + ')')
            self.get_text_main_to_second()

    def for_sqrt(self, coren_in):
        """Функция для вычисления корня 2.2"""
        try:
            index = self.more_last_bracket(coren_in)

            if 'K' in self.count_mains[coren_in + 1: index]:
                self.for_sqrt(self.count_mains.index('K', coren_in + 1))
            elif any([x in self.count_mains[coren_in + 1: index] for x in ('sin', 'cos')]):
                self.for_trigonometric_functions(self.count_mains.index('[', coren_in + 1))

            number = self.integer(eval(''.join(['math.sqrt', '(', *self.count_mains[coren_in + 2: index], ')'])))
            self.count_mains[coren_in: index + 1] = [number]
        except SyntaxError:
            pass

    def trigonometric_functions(self):
        """ Для синусов и косинусов 3.1"""
        if self.count_mains[-1] not in ('.', *self.main_symbols, '('):
            start, element = self.get_last_full_number()
            angle = self.sender().text()

            if element[0] == '(' and element[-1] in digits:
                self.count_mains[start:] = [element[0], angle, '[', *element[1:], ']']
                self.main_input.setText(''.join(self.count_mains[start:]))
            else:
                self.count_mains[start:] = [angle, '[', *element, ']']
                self.main_input.setText(''.join([angle, '[', *element, ']']))
            self.get_text_main_to_second()

    def for_trigonometric_functions(self, coren_in):
        """Функция для вычисления синусов и косинусов 3.2"""
        index_1 = 0
        for x in range(coren_in + 1, len(self.count_mains)):
            if self.count_mains[x] == ']':
                if x == len(self.count_mains) - 1 or self.count_mains[x + 1] in (*self.main_symbols, '))', ')'):
                    index_1 = x
                    break
        func = [f"math.{self.count_mains[coren_in - 1]}(math.radians(", *self.count_mains[coren_in + 1: index_1], "))"]
        self.count_mains[coren_in - 1: index_1 + 1] = func

    def clear_C(self):
        """Функция для отчистки всего поля"""
        self.main_input.setText('0')
        self.count_mains = ['0']
        self.second_input.setText('0')
        self.count_brackets = 0

    def clear_CE(self):
        """Функция для стирания только одного символа или операции"""
        start, last = self.get_last_full_number()
        print('CE', start, last)
        if last[-1] in (*digits, '.', *self.main_symbols, '('):
            self.count_mains.pop()
            if last[-1] not in self.main_symbols:
                self.main_input.setText(self.main_input.text()[:-1])

            if last[-1] == '(':
                self.count_brackets -= 1

        elif last[-1] == ']':
            self.count_mains[start:] = last[2:-1]
            self.main_input.setText(''.join(last[2:-1]))

        elif last[-1] == ')':

            if last[0] == '(':
                if last[1] != '-':
                    self.count_mains.pop()
                    self.count_brackets += 1
                else:
                    self.count_mains[start:] = last[2:-1]
                    self.main_input.setText(''.join(last[2:-1]))

            elif last[0] == 'K':
                self.count_mains[start:] = last[2:-1]
                self.main_input.setText(''.join(last[2:-1]))

        elif last[-1] == '!':
            self.count_mains[start:] = last[1:-2]
            self.main_input.setText(''.join(last[1:-2]))

        self.get_text_main_to_second()
        if len(self.count_mains) == 0:
            self.count_mains.append('0')
            self.main_input.setText('0')

        elif self.main_input.text() == '':
            start, last = self.get_last_full_number()
            if last[0] not in self.main_symbols and last[-1] != '(' and\
                    not (last[0] == '(' and last[1] != '-' and last[-1] == ')'):
                self.main_input.setText(''.join(last))

    def equally(self):
        """Функция для вычисления результата"""
        try:
            if len(self.count_mains) > 1:

                while '!' in self.count_mains:
                    fac_in = self.count_mains.index('!')
                    self.for_factorial(fac_in)

                while 'K' in self.count_mains:
                    coren_in = self.count_mains.index('K')
                    self.for_sqrt(coren_in)

                while '[' in self.count_mains:
                    coren_in = self.count_mains.index('[')
                    self.for_trigonometric_functions(coren_in)

                res = str(eval(''.join(self.count_mains)))
                if len(res) > 10:
                    res = res[:8]
                if len(res) > 1 and res[-2:] == '.0':
                    res = res[:-2]

                self.second_input.setText(res)
                self.main_input.setText(res)

                self.count_mains = []
                self.count_mains.extend(list(res))

                if self.count_mains[0] == '-':
                    self.count_mains.insert(0, '(')
                    self.count_mains.append(')')
                    self.get_text_main_to_second()

        except Exception as e:
            print(e)
            self.clear_C()
            self.main_input.setText('Error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Colorculator()
    window.show()
    sys.exit(app.exec())