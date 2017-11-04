from fraction import Fraction
from tester import tester


class RPN:
    def __init__(self, string):
        self.string = RPN.get_normal_string(string)
        self.string_elements = self.string.split()
        self.polish_notation_list = self.get_reversed_polish_notation()
        #try:
        #    self.result = self.old_calc()
        #except Exception:
        #    self.result = "ERROR. INCORRECT EXPRESSION"

    @staticmethod
    def get_normal_string(string):
        string = string.replace(' ', '')
        string_len = len(string)
        normal_string = ''
        i = 0
        while i < string_len:
            current_symbol = string[i]

            if i == string_len-1:
                next_symbol = ''
            else:
                next_symbol = string[i + 1]

            if current_symbol.isalpha() and (next_symbol.isalpha() or next_symbol == '(' or next_symbol.isdigit()):
                normal_string += current_symbol + ' *'

            elif current_symbol.isdigit():
                while current_symbol.isdigit() or current_symbol == '.':
                    normal_string += current_symbol
                    i += 1
                    if i < len(string):
                        current_symbol = string[i]
                    else:
                        break
                if i < len(string):
                    next_symbol = string[i]
                    if next_symbol.isalpha() or next_symbol == '(':
                        normal_string += ' *'
                i -= 1

            elif current_symbol == ')' and (next_symbol.isalpha() or next_symbol == '(' or next_symbol.isdigit()):
                normal_string += current_symbol + ' *'
            else:
                normal_string += current_symbol
            normal_string += ' '
            i += 1
        return normal_string

    @staticmethod
    def get_priority(operation):
        if operation in ('+', '-'):
            return 1
        if operation in ('*', '/'):
            return 2
        if operation in ('u+', 'u-'):
            return 3
        return -1

    @staticmethod
    def is_operation(symbol):
        return symbol in ('+', '-', '/', '*', 'u+', 'u-')

    @staticmethod
    def usual(symbol):
        return symbol.replace('.', '', 1).isdigit() or symbol.isalpha() or RPN.is_operation(symbol) or symbol in ('(', ')')

    def get_reversed_polish_notation(self):
        operations = list()
        notation = list()
        unary_operation = True
        for element in self.string_elements:

            if not RPN.usual(element):
                continue

            if element == '(':
                operations.append(element)
                unary_operation = True

            elif element == ')':
                while operations[-1] != '(':
                    notation.append(operations[-1])
                    operations.pop()
                operations.pop()
                unary_operation = False

            elif RPN.is_operation(element):
                if unary_operation and element in ('+', '-'):
                    element = 'u' + element
                while operations and \
                        (not unary_operation and RPN.get_priority(operations[-1]) >= RPN.get_priority(element) or
                         unary_operation and RPN.get_priority(operations[-1]) > RPN.get_priority(element)):
                    notation.append(operations[-1])
                    operations.pop()
                operations.append(element)
                unary_operation = True

            else:
                notation.append(element)
                unary_operation = False

        while operations:
            notation.append(operations[-1])
            operations.pop()

        return notation

    def calc_with_Fraction(self):

        def process_operation(operation):
            r_operand = operands[-1];
            operands.pop()
            if operation[0] == 'u':
                if operation == 'u-':
                    operands.append(-r_operand)
                if operation == 'u+':
                    operands.append(r_operand)
            else:
                l_operand = operands[-1];
                operands.pop()
                if operation == '+':
                    operands.append(l_operand + r_operand)
                if operation == '-':
                    operands.append(l_operand - r_operand)
                if operation == '*':
                    operands.append(l_operand * r_operand)
                if operation == '/':
                    operands.append(l_operand / r_operand)

        operands = list()
        for element in self.polish_notation_list:
            if RPN.is_operation(element):
               process_operation(element)
            else:
                if element.isalpha():
                    operands.append(Fraction({element: 1}))
                else:
                    operands.append(Fraction({'1': float(element)}))
        return operands[-1]

    def calc_with_tree(self):
        pass

    def __str__(self):
        return str(self.result)

    def old_calc(self):
        unary_operation = True
        i = 0
        while i < len(self.string):
            c = self.string[i]

            if not RPN.usual(c):
                i += 1
                continue

            if c == '(':
                self.operations.append(c)
                unary_operation = True

            elif c == ')':
                while self.operations[-1] != '(':
                    self.old_process_operation()
                    self.operations.pop()
                self.operations.pop()
                unary_operation = False

            elif RPN.is_operation(c):
                if unary_operation and c in ('+', '-'):
                    c = 'u' + c
                while self.operations and \
                        ( not unary_operation and RPN.get_priority(self.operations[-1]) >= RPN.get_priority(c) or
                        unary_operation and RPN.get_priority(self.operations[-1]) > RPN.get_priority(c)):
                    self.old_process_operation()
                    self.operations.pop()
                self.operations.append(c)
                unary_operation = True

            else:
                operand = ''
                while i < len(self.string):
                    c = self.string[i]
                    if (RPN.usual(c) or c == '.') and (c.isalpha() or c.isdigit() or c == '.' and '.' not in operand):
                        operand += c
                    else:
                        break
                    i += 1
                i -= 1
                nums, letters = '', ''
                for x in operand:
                    if x.isalpha():
                        letters += x
                    else:
                        nums += x
                if not letters:
                    letters = '1'
                if not nums:
                    nums = '1'
                self.operands.append(Fraction({letters: float(nums)}))
                unary_operation = False
            i += 1

        while self.operations:
            self.old_process_operation()
            self.operations.pop()

        return self.operands[-1]

    def old_process_operation(self):
        operation = self.operations[-1]
        r_operand = self.operands[-1]; self.operands.pop()
        if operation[0] == 'u':
            if operation == 'u-':
                self.operands.append(-r_operand)
            if operation == 'u+':
                self.operands.append(r_operand)
        else:
            l_operand = self.operands[-1]; self.operands.pop()
            if operation == '+':
                self.operands.append(l_operand + r_operand)
            if operation == '-':
                self.operands.append(l_operand - r_operand)
            if operation == '*':
                self.operands.append(l_operand * r_operand)
            if operation == '/':
                self.operands.append(l_operand / r_operand)

if __name__ == '__main__':
    tester("tests_for_RPN.txt", RPN)
    #while True:
    #    line = input("Введите выражение:\n")
    #    print(RPN(line).calc_with_Fraction())












"""
failed tests:
 [5, 6, 7, 8, 9, 11, 12, 14, 16, 22]
"""















"""
Введите выражение:
(y*(2x-2))/(6x-5+1) + 3y
(-1-+10*x*y-6*y)/(-2+3*x)
Введите выражение:
(y*(2x-2))/(6x-5+1) + 3y
(10*x*y-7*y)/(-2+3*x)
Введите выражение:
(y*(-2))/(6x-5-1) + 3y
(10*x*y-10*y)/(-3+3*x)
Введите выражение:
(x-1)/(x-1)
(-1-+x)/(-1-+x)
Введите выражение:
x/x
1
Введите выражение:
y*(x
ERROR. BAD EXPRESSION
Введите выражение:
y*(x-1)/y
-1-+x
Введите выражение:
y*(x-1)/(2y)
(-1-+x)/(2)
Введите выражение:

(2x-1)/(6x-6)
ERROR. BAD EXPRESSION
Введите выражение:
(-1-+2*x)/(-6+6*x)
Введите выражение:
(2x-2)/(6x-6)
(-1-+x)/(-3+3*x)
Введите выражение:
(x+1)/(x+1)
(1+x)/(1+x)
Введите выражение:

Process finished with exit code 1

"""
