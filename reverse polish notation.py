from fraction import Fraction


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
        return symbol in ('+', '-', '/', '*')

    @staticmethod
    def usual(symbol):
        return symbol.isdigit() or symbol.isalpha() or RPN.is_operation(symbol) or symbol in ('(', ')')

    def calc(self):

        i = 0
        while i < len(self.string):
            c = self.string[i]

            if not RPN.usual(c):
                i += 1
                continue

            if c == '(':
                self.operations.append(c)

            elif c == ')':
                while self.operations[-1] != '(':
                    self.process_operation()
                    self.operations.pop()
                self.operations.pop()

            elif RPN.is_operation(c):
                while self.operations and RPN.get_priority(self.operations[-1]) >= RPN.get_priority(c):
                    self.process_operation()
                    self.operations.pop()
                self.operations.append(c)

            else:
                operand = ''
                while i < len(self.string):
                    c = self.string[i]
                    if (RPN.usual(c) or c == '.') and (c.isalpha() or c.isdigit() or \
                       c == '.' and '.' not in operand):
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

            i += 1

        while self.operations:
            self.process_operation()
            self.operations.pop()

        return self.operands[-1]

    def __str__(self):
        return str(self.calc())

    def process_operation(self):
        operation = self.operations[-1]
        r_operand = self.operands[-1]; self.operands.pop()
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
    # R = RPN('.5huesos + 2.5huesos')
    # print(R)
    print(RPN(input()))