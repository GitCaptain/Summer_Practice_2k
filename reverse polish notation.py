from fraction import Fraction
from tester import tester

class RPN:
    def __init__(self, string):
        self.string = string
        self.operations = []
        self.operands = []
        try:
            self.result = self.calc()
        except Exception:
            self.result = "ERROR. BAD EXPRESSION"


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
        return symbol.isdigit() or symbol.isalpha() or RPN.is_operation(symbol) or symbol in ('(', ')')

    def calc(self):
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
                    self.process_operation()
                    self.operations.pop()
                self.operations.pop()
                unary_operation = False

            elif RPN.is_operation(c):
                if unary_operation and c in ('+', '-'):
                    c = 'u' + c
                while self.operations and \
                        ( not unary_operation and RPN.get_priority(self.operations[-1]) >= RPN.get_priority(c) or
                        unary_operation and RPN.get_priority(self.operations[-1]) > RPN.get_priority(c)):
                    self.process_operation()
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
            self.process_operation()
            self.operations.pop()

        return self.operands[-1]

    def __str__(self):
        return str(self.result)


    def process_operation(self):
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
    while True:
         print(RPN(input("Введите выражение:\n")))

"""
5+3 _ 8
xy+zy+5-7x+39xy-2 _ 3-7*x+40*x*y+y*z
40x+7y-2x+5y-6x-20y _ 32*x-8*y
kek/k _ e*k
3x/5y _ (3*x)/(5*y)
7*x(5y-47-z)-7x*z _ -47*x+5*x*y-8*x*z
(kek + pek + ekk)/k/e _ 2*k+p
1.5d + 5.d + 5d _ 11.5*d
a/b+b/a+5 _ (a*a+5*a*b+b*b)/(a*b)
2/0 _ ERROR. BAD EXPRESSION
(x+1)/(x+1) _ 1
y*(x-1)/(2y) _ (-1+x)/(2)
(x-1)/(x-1) _ 1
y*(x-1)/y _ -1+x
x/x _ 1
x/-x _ -1
x-x _ 0
-x/-x _ 1
-x/x _ -1




Введите выражение:
x+x
2*x
Введите выражение:
2*(x-3)+3x-4
-10+5*x
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