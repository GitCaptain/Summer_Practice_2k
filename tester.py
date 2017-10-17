
def tester(file_name, funcs):
    print('testing', file_name)
    with open(file_name) as FILE:
        i = 0
        while True:
            line = FILE.readline().split('_')
            if not line or line[0] == '\n' or line[0][0] == '#':
                break
            line[0] = line[0].strip()
            line[1] = line[1].strip()
            if not isinstance(funcs, list):
                funcs = [funcs]
            res = line[0]
            for func in funcs:
                res = func(res)
            res = str(res)
            print('test:', i)
            print("result of functions for", line[0], 'is', res)
            print(line[1], '==', res, line[1] == res)
            print()
            i += 1
