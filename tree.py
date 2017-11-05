from reverse_polish_notation import RPN
from tester import tester


def make_tree(index):
    element = notation[index]
    if element in ('+', '-', '/', '*'):
        node = Node(element, None,
                    make_tree(index - 2),
                    make_tree(index - 1))
    elif element in ('u+', 'u-'):
        node = Node(element, None,
                    make_tree(index - 1))
    else:
        node = Node(None, element)

    for child in node.childs:
        child.parent = node
    return node


def get_res(foo):
    try:
        res = foo(notation)
    except Exception:
        res = "ERROR. BAD EXPRESSION"
    return res


class Node:

    def __init__(self, operation=None, operand=None, *childs):
        self.parent = None
        self.childs = sorted(list(childs), key=lambda node=self: node.operand if node.operand else node.operation)
        self.operand = operand
        self.operation = operation

    def __eq__(self, other):
        return self.childs == other.childs and self.operation == other.operation and self.operand == other.operand

    def __str__(self):
        if self.operand:
            return self.operand
        elif self.operation:
            return self.operation
        else:
            return ''


class Tree:

    def __init__(self, reversed_polish_notation):
        self.root = make_tree(len(reversed_polish_notation) - 1)

    def __str__(self):
        # сделать позднее
        return "Tree doesn't work yet"

    def simplify(self):
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
        print(tree.root.childs[0] == tree.root.childs[1])
        res_tree = get_res(calc_with_tree)
        print(res_tree)
