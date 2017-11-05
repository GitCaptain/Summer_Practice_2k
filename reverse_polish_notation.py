
def get_normal_string(string):
    string = string.replace(' ', '')
    string_len = len(string)
    normal_string = ''
    i = 0
    while i < string_len:
        current_symbol = string[i]

        if i == string_len - 1:
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


class RPN:
    def __init__(self, string):
        self.string = get_normal_string(string)
        self.string_elements = self.string.split()
        self.polish_notation_list = self.get_reversed_polish_notation()

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

    def __str__(self):
        return ''.join(self.polish_notation_list)

if __name__ == '__main__':
    pass

