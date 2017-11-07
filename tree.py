from reverse_polish_notation import RPN
from tester import tester


def make_tree(index):
    element = notation[index]

    if element in ('+', '-', '/', '*'):
        right_child = make_tree(index - 1)
        index = right_child[1]
        right_child = right_child[0]

        left_child = make_tree(index - 1)
        index = left_child[1]
        left_child = left_child[0]

        node = Node(element, None, left_child, right_child)
    elif element in ('u+', 'u-'):
        left_child = make_tree(index - 1)
        index = left_child[1]
        left_child = left_child[0]

        node = Node(element, None, left_child)
    else:
        node = Node(None, element)

    for child in node.childs:
        child.parent = node

    return node, index


class Node:

    def __init__(self, operation=None, operand=None, *childs):
        self.parent = None
        self.childs = list(childs)
        if not operand:
            operand = ''
        self.operand = operand
        self.operation = operation

    def __eq__(self, other):
        return self.operation == other.operation and \
               self.operand == other.operand and \
               self.childs == other.childs

    def __str__(self):
        if self.operand:
            return self.operand
        elif self.operation:
            return self.operation
        else:
            return ''

    @staticmethod
    def sorted_node_childs(*childs):
        return sorted(childs, key=lambda node: node.operand if node.operand else node.operation)

    def simplify_node(self):
        # Добавить везде обработку чисел!

        for child in self.childs:
            child.simplify_node()

        if self.operation == '/':
            if self.childs[0] == self.childs[1]:
                self.operation = None
                self.operand = 1
                self.childs = list()

            elif self.childs[0].operand.replace('.', '', 1).isdigit() and \
                    self.childs[1].operand.repace('.', '', 1).isdigit():
                self.operation = None
                self.operand = float(self.childs[0])/float(self.childs[1])
                try:
                    self.operand = int(self.operand)
                except ValueError:
                    pass
                self.operand = str(self.operand)

            elif self.childs[0].operation == self.childs[1].operation == '*':
                delete_childs = dict()
                for child_child in self.childs[0].childs:
                    if delete_childs.get(child_child):
                        continue
                    delete_childs[child_child] = min(self.childs[0].childs.count(child_child),
                                                     self.childs[1].childs.count(child_child))
                for delete_child in delete_childs.keys():
                    for i in range(delete_childs[delete_child]):
                        self.childs[0].childs.remove(delete_child)
                        self.childs[1].childs.remove(delete_child)

        elif self.operation == '*':
            new_childs = list()
            delete_childs = list()
            multiply_result = 1
            for child in self.childs:
                if child.operation == '*':
                    new_childs.extend(child.childs)
                    for new_child in child.childs:
                        new_child.parent = self
                elif child.operand.replace('.', '', 1).isdigit():
                    delete_childs.append(child)
                    multiply_result *= float(child.operand)
            multiply_result = str(multiply_result)
            try:
                multiply_result = str(int(multiply_result))
            except ValueError:
                pass

            for child in delete_childs:
                self.childs.remove(child)

            multiply_result_node = Node(None, multiply_result)
            multiply_result_node.parent = self
            self.childs.append(multiply_result_node)
            self.childs = Node.sorted_node_childs(new_childs)

        elif self.operation == '+':
            new_childs = list()
            for child in self.childs:
                if child.operation == '+' or child.operation == 'u+':
                    new_childs.extend(child.childs)
                    for new_child in child.childs:
                        new_child.parent = self
                else:
                    new_childs.append(child)
            operand_count = dict()
            delete_childs = list()
            for operand in self.childs:
                if operand.operation:
                    continue
                if operand_count.get(operand):
                    operand_count[operand] += 1
                    delete_childs.append(operand)
                else:
                    operand_count[operand_count] = 1

            for child in delete_childs:
                self.childs.remove(child)

            for operand in operand_count:
                if operand_count[operand] == 1:
                    self.childs.append(operand)
                else:
                    new_node_left_child = Node(None, str(operand_count[operand]))
                    new_node_right_child = Node(None, operand)

                    new_node = Node('*', None, new_node_left_child, new_node_right_child)
                    new_node_left_child.parent = new_node
                    new_node_right_child.parent = new_node
                    new_node.parent = self

                    self.childs.append(new_node)
            self.childs = Node.sorted_node_childs(new_childs)

        elif self.operation == '-':
            if self.childs[0] == self.childs[1]:
                self.operation = None
                self.operand = '0'
            elif self.childs[0].operand.replace('.', '', 1).isdigit() and self.childs[1].operand.repace('.', '', 1).isdigit():
                self.operation = None
                self.operand = str(float(self.childs[0]) - float(self.childs[1]))
                try:
                    self.operand = str(int(self.operand))
                except ValueError:
                    pass


class Tree:

    def __init__(self, reversed_polish_notation):
        self.root = make_tree(len(reversed_polish_notation) - 1)[0]

    def __str__(self):

        def make_string(current_node, deep=0):
            string = '|    ' * deep + '|' + current_node.__str__() + ':\n'
            for child in current_node.childs:
                string += make_string(child, deep + 1)
            return string

        return make_string(self.root)

    def simplify(self):
        self.root.simplify_node()

    def get_plain_tree(self):

        def make_string(current_node):
            string = ''
            if current_node.operand:
                return current_node.operand
            for child in current_node.childs:
                if child.operation:
                    string += '( ' + make_string(child) + ' )'
                else:
                    string += make_string(child)
                if current_node.operation == 'u+':
                    continue
                elif current_node.operation == 'u-':
                    string = '-' + string
                else:
                    string += current_node.operation
            return string[:-1]

        return make_string(self.root)


def get_res(foo):
    try:
        res = foo(notation)
    except Exception:
        res = "ERROR. BAD EXPRESSION"
    return res


def calc_with_tree(polish_notation_list):
    tree = Tree(polish_notation_list)
    tree.simplify()
    return tree.get_plain_tree()

if __name__ == '__main__':
    #tester("tests_for_RPN.txt", calc_with_tree)
    while True:
        line = input("Введите выражение:\n")
        notation = RPN(line).get_reversed_polish_notation()
        res_tree = get_res(calc_with_tree)
        print(res_tree)
