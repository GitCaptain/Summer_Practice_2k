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


def get_res(foo):
    try:
        res = foo(notation)
    except Exception:
        res = "ERROR. BAD EXPRESSION"
    return res


class Node:

    def __init__(self, operation=None, operand=None, *childs):
        self.parent = None
        self.childs = list(childs)  # sorted(list(childs), key=lambda node=self: node.operand if node.operand else node.operation)
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

    def simplify_node(self):
        if self.operation == '/':
            # рассмотреть еще 100500 случаев
            if self.childs[0] == self.childs[1]:
                self.operation = None
                self.operand = 1
                self.childs = list()

        elif self.operation == '*':
            pass

        elif self.operation == '+':
            pass
        elif self.operation == '-':
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
        pass


def calc_with_tree(polish_notation_list):
    tree = Tree(polish_notation_list)
    return tree

if __name__ == '__main__':
    #tester("tests_for_RPN.txt", calc_with_tree)
    while True:
        line = input("Введите выражение:\n")
        notation = RPN(line).get_reversed_polish_notation()
        tree = Tree(notation)
        #print(tree.root.childs[0] == tree.root.childs[1])
        res_tree = get_res(calc_with_tree)
        print(res_tree)
