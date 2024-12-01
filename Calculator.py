import math
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
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
        self.btn_equally.clicked.connect(self.equally)

    def buttons_num(self):
        buttons = [self.num_0, self.num_1, self.num_2, self.num_3, self.num_4, self.num_5,
                   self.num_6, self.num_7, self.num_8,self.num_9]
        for b in buttons:
            b.clicked.connect(self.numbers)

    def buttons_symbols(self):
        buttons = [self.btn_divide, self.btn_multipy, self.btn_minus, self.btn_plus, self.btn_point,
                   self.btn_procent, self.btn_stepen,]
        for b in buttons:
            b.clicked.connect(self.symbols)

        self.btn_c.clicked.connect(self.clear_C)
        self.btn_ce.clicked.connect(self.clear_CE)
        self.btn_plus_minus.clicked.connect(self.minus_plus)
        self.btn_factorial.clicked.connect(self.factorial)
        self.btn_coren.clicked.connect(self.mat_root)

    def numbers(self):
        num = self.sender().text()
        if self.count_mains[-1] not in (')', '!'):
            if self.count_mains[0] == '0' and len(self.count_mains) == 1:
                self.main_input.setText('')
                self.second_input.setText('')
                self.count_mains.pop()

            elif self.count_mains[-1] == '0' and self.count_mains[-2] in self.main_symbols:
                self.main_input.setText('')
                self.second_input.setText(self.second_input.text()[:-1])
                self.count_mains.pop()

            elif self.use_sign:
                self.main_input.setText('')
                self.use_sign = False

            text = self.main_input.text()
            s_text = self.second_input.text()

            self.main_input.setText(text + num)
            self.second_input.setText(s_text + num)
            self.count_mains.append(num)

    def symbols(self):
        if self.main_input.text() == 'ERROR':
            self.main_input.setText('0')

        last = self.count_mains[-1]
        if (last in digits) or last in ('', ')', '!') and last != '.':
            self.use_sign = True

            symbol = self.sender().text()
            text = self.second_input.text()

            if symbol == '.':
                text_m = self.main_input.text()
                if '.' not in text_m and self.count_mains[-1] not in (')', '!'):
                    self.main_input.setText(text_m + symbol)
                    self.second_input.setText(text + symbol)
                    self.count_mains.append(symbol)
                self.use_sign = False

            else:
                self.second_input.setText(text + ' ' + symbol + ' ')
                if symbol == '÷':
                    symbol = '/'
                elif symbol == 'x':
                    symbol = '*'
                elif symbol == '^^':
                    symbol = '**'
                self.count_mains.append(symbol)
            print(self.count_mains)

    def find_index_fisrt_bracets(self):
        """" для поиска последнего отрицательного числа, первой с конца ( """
        index_1 = 0
        for x in range(-1, -len(self.count_mains) - 1, -1):
            if self.count_mains[x] == '(':
                index_1 = x
                break
        return index_1

    def find_last_number(self, start):
        """" для нахождения последнего числа от определ момента (с конца в начало <<-) """
        index_1 = -1
        for x in range(start, -len(self.count_mains) - 1, -1):
            if self.count_mains[x] in self.main_symbols and x != -len(self.count_mains):
                index_1 = x
                break
        return index_1 + 1

    def find_first_number(self, start):
        """" для  нахождения первого числа от определ момента (из начала в конец ->> ) """
        index = len(self.count_mains)
        for x in range(start + 1, len(self.count_mains)):
            if self.count_mains[x] in (*self.main_symbols, ')'):
                index = x
                break
        return index

    def minus_plus(self):
        fact = False
        if self.count_mains[-1] != '.':
            print('+-', self.count_mains)

            if self.count_mains[-1] == '!' and self.count_mains[-2] == ')':
                i = self.find_index_fisrt_bracets()
                element = self.count_mains[i + 1:-2]
                fact = True

            elif self.count_mains[-1] == ')' or (self.count_mains[-1] == '!' and self.count_mains[-2] == ')'):
                i = self.find_index_fisrt_bracets()
                element = self.count_mains[i + 1:-1]

            else:
                i = self.find_last_number(-1)
                element = self.count_mains[i:]

            text_m = self.main_input.text()

            if element[-1] == '!':
                element = element[:-1]
                text_m = text_m[:-1]
                fact = True
            print('Element_start ', element)

            if self.count_mains[-1] in self.main_symbols:
                print('yes1')
                sign = element[-1]
                if sign in ('-', '+'):
                    element[-1] = '+' if element[-1] == '-' else '-'
                elif sign in ('*', '/'):
                    element[-1] = '*' if element[-1] == '/' else '/'

            elif (element[0] in tuple('123456789')) or (element[0] == '0' and '.' in element[1:]) or element[0] == 'K':
                print('yes2')
                element = '(-' + ''.join(element) + ')'
                text_m = '-' + text_m
                if fact:
                    element += '!'
                    text_m += '!'
                print('scobcii', element)

            elif element[0] == '-':
                try:
                    print('yes3')
                    element = element[1:]
                    text_m = text_m[1:]
                    if fact:
                        element.append('!')
                        text_m.append('!')
                except Exception as e:
                    print(e)

            self.count_mains[i:] = element
            text_s = ''.join([x if x not in self.main_symbols else ' ' + x + ' ' for x in self.count_mains])

            print('Element', element)
            print('Text', text_m, ';', text_s)
            print('COUNT', self.count_mains)

            self.main_input.setText(text_m)
            self.second_input.setText(text_s)

    def factorial(self):
        f = '!'
        text_m = self.main_input.text()
        text_s = self.second_input.text()
        if text_m[0] != '0' and text_m[-1] != '.' and text_s[-1] not in self.main_symbols and text_s[-1] in digits:
            self.main_input.setText(text_m + f)
            self.second_input.setText(text_s + f)
            self.count_mains.append(f)
            print('Factorial', self.count_mains)

    def for_factorial(self, index):
        index_1 = self.find_last_number(-(len(self.count_mains) - index))
        number = self.count_mains[index_1: index]
        self.count_mains[index_1: index + 1] = f'math.factorial({''.join(number)})' if number[-1] != ')' else None
        print('FACTORIAL WORK', self.count_mains)

    def mat_root(self):
        try:
            if self.count_mains[-1] == ')' or (self.count_mains[-1] == '!' and self.count_mains[-2] == ')'):
                i = self.find_index_fisrt_bracets()
            else:
                i = self.find_last_number(-1)
            element = list(map(str, self.count_mains[i:]))
            element.insert(0, 'K')
            # sqrt \u221a "√"
            text_m = self.main_input.text()
            text_s = self.second_input.text()
            if text_m[-1] != '.' and text_s[-1] not in self.main_symbols and text_s[-1] in digits and text_m[0] != "K":
                self.main_input.setText('K' + text_m)
                self.second_input.setText(text_s[:i] + 'K' + text_s[i:])
                self.count_mains[i:] = element
            print('SQRT', element)
        except Exception as e:
            print(e)

    def for_root(self, coren_in):
        index = self.find_first_number(coren_in)
        number = self.count_mains[coren_in + 1: index]
        self.count_mains[coren_in: index] = f'math.sqrt({''.join(number)})'
        print('coreeen ', self.count_mains)

    def clear_C(self):
        self.main_input.setText('0')
        self.count_mains = ['0']
        self.second_input.setText('0')

    def clear_CE(self):
        try:
            last = self.count_mains[-1]
            print('Last : ' + last)

            if (len(self.count_mains) <= 1 or
                    (self.count_mains[0] == '(' and self.count_mains.count('(') == 1 and self.count_mains[-1] == ')') or
                    self.count_mains[0] == 'K' and all([x not in self.count_mains for x in self.main_symbols]) and
                    self.count_mains[-1] != ')'):
                self.clear_C()
                return

            text2 = self.second_input.text()[:-1]

            if last in ('.', *digits, '!', 'K'):
                text = self.main_input.text()[:-1]
                self.main_input.setText(text)
                self.count_mains = self.count_mains[:-1]
                print(self.main_input.text())

            elif last == ')':
                self.main_input.setText('')
                index_bracket = self.find_index_fisrt_bracets()
                text2 = text2[:index_bracket - 1]
                self.count_mains = self.count_mains[:index_bracket]

            else:
                text2 = self.second_input.text()[:-3]
                self.count_mains = self.count_mains[:-1]
                self.use_sign = False

            self.second_input.setText(text2)
            print('Finish2:', self.count_mains)

            if (self.count_mains[-1] in digits or
                    (self.count_mains[-1] == '!' and self.count_mains[-2] != ')')
                    and self.main_input.text() == ''):

                index_1 = self.find_last_number(-1)
                print(index_1, self.count_mains[index_1:])
                self.main_input.setText(''.join(self.count_mains[index_1:]))

            elif self.count_mains[-1] == ')' and self.main_input.text() == '':
                index_bracket = self.find_index_fisrt_bracets()
                self.main_input.setText(''.join(self.count_mains[index_bracket + 1:-1]))

        except Exception as e:
            print(e)

    def equally(self):
        try:
            if len(self.count_mains) > 1:
                print(''.join(self.count_mains))
                while '!' in self.count_mains:
                    fac_in = self.count_mains.index('!')
                    self.for_factorial(fac_in)

                while 'K' in self.count_mains:
                    print('передаем игдекс ', self.count_mains.index('K'))
                    coren_in = self.count_mains.index('K')
                    self.for_root(coren_in)

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
                    text_s = ''.join(
                        [x if x not in self.main_symbols else ' ' + x + ' ' for x in self.count_mains])
                    self.second_input.setText(text_s)
                print(res)
                print(self.count_mains)

        except Exception as e:
            print(e)
            self.clear_C()
            self.main_input.setText('Error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Colorculator()
    window.show()
    sys.exit(app.exec())