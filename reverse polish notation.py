from fraction import Fraction
from tester import tester

class RPN:
    def __init__(self, string):
        self.string = string
        self.operations = []
        self.operands = []

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
        try:
            return str(self.calc())
        except Exception:
            return "ERROR. BAD EXPRESSION"

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
    # tester("tests_for_RPN.txt", RPN)
    print(RPN(input()))
