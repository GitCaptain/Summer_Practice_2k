from reverse_polish_notation import RPN


def tester(file_name, *funcs):
    print('testing', file_name)
    with open(file_name) as FILE:
        test = 0
        failed_tests = []
        while True:
            line = FILE.readline().split('_')
            if not line or line[0] == '\n' or line[0][0] == '#':
                break
            line[0] = line[0].strip()
            line[1] = line[1].strip()
            res = line[0]
            notation = RPN(res).get_reversed_polish_notation()
            try:
                res = str(funcs[0](notation))
            except Exception:
                res = "ERROR. BAD EXPRESSION"
            print('test:', test)
            print('result of functions for', line[0], 'is', res)
            print(line[1], '==', res, line[1] == res)
            print()
            if line[1] != res:
                failed_tests.append(test)
            test += 1
        print('failed tests:\n', failed_tests)