from tester import tester

def gcd(a, b):
    if a != int(a) or b != int(b):
        return -1

    a, b = abs(a), abs(b)
    while a and b:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


class Fraction:

    def __init__(self, num={'1': 0}, denom={'1': 1}):
        self.numerator = dict()
        self.denominator = dict()
        for key in num:
            self.numerator[''.join(sorted(key))] = num[key]
        for key in denom:
            self.denominator[''.join(sorted(key))] = denom[key]

    def __add__(self, other):
        result_num = dict(self.numerator)
        result_denom = dict(self.denominator)
        other_num = dict(other.numerator)


        if self.denominator != other.denominator:
            result_denom = Fraction.dictionary_multiplier(self.denominator, other.denominator)
            result_num = Fraction.dictionary_multiplier(self.numerator, other.denominator)
            other_num = Fraction.dictionary_multiplier(other.numerator, self.denominator)

        for key in other_num:
            if key in result_num:
                result_num[key] += other_num[key]
            else:
                result_num[key] = other_num[key]

        return Fraction(result_num, result_denom)

    def __mul__(self, other):
        result_num = Fraction.dictionary_multiplier(self.numerator, other.numerator)
        result_denom = Fraction.dictionary_multiplier(self.denominator, other.denominator)
        return Fraction(result_num, result_denom)

    def __neg__(self):  # каждое слагаемое числителя домножаем на -1
        result_num = {}
        result_denom = dict(self.denominator)
        for key in self.numerator:
            result_num[key] = -self.numerator[key]
        return Fraction(result_num, result_denom)

    def __sub__(self, other):  # вычитание = сложение с отрицательным
        return self.__add__(other.__neg__())

    def __truediv__(self, other):  # деление = умножение на обратную дробь
        return self.__mul__(Fraction(other.denominator, other.numerator))

    def __floordiv__(self, other):  # // делает тоже самое, что и /
        return self.__truediv__(other)

    def __str__(self):

        zero = True
        only_num = True
        for val in self.numerator.values():
            if val:
                zero = False

        for key in self.denominator:
            if key != '1' and self.denominator[key] or\
               key == '1' and self.denominator[key] > 1:
                only_num = False

        if zero:
            return '0'
        elif only_num:
            return Fraction.dict_to_string(self.numerator)
        else:
            return '(' + Fraction.dict_to_string(self.numerator) + ')/' +\
                   '(' + Fraction.dict_to_string(self.denominator) + ')'

    @staticmethod
    def dictionary_multiplier(a, b): # a, b - dicts, return a*b
        res = dict()
        for Bitem in b.items():
            for Aitem in a.items():

                if Aitem[0] == '1' and Bitem[0] == '1':
                    key = '1'
                elif Aitem[0] == '1':
                    key = Bitem[0]
                elif Bitem[0] == '1':
                    key = Aitem[0]
                else:
                    key = Aitem[0] + Bitem[0]

                res[''.join(sorted(key))] = Aitem[1] * Bitem[1]

        return res

    @staticmethod
    def dict_to_string(dictionary):
        res = ''
        first = True
        for key in sorted(dictionary.keys()):
            num = dictionary[key]
            if not num:
                continue
            if int(num) == num:
                num = int(num)
            if num > 0 and not first:
                res += '+'
            if abs(num) != 1 or key == '1':
                res += str(num)
            if num == -1:
                res += '-'
            first = False
            if key == '1':
                continue
            if abs(num) != 1:
                res += '*'
            res += '*'.join(key)
        return res


    @staticmethod
    def find_common_multiplier_in_dict(dictionary):
        res_key = ""
        res_num = -1
        first_iteration = True
        for key in dictionary.keys():
            if first_iteration:
                res_key = key
                res_num = abs(dictionary[key])
                first_iteration = False
                continue
            if res_num > 0:
                res_num = gcd(res_num, dictionary[key])
            cur_common_str = ""
            used_letters = set()
            for letter in key:
                if letter in res_key and letter not in used_letters:
                    cur_common_str += letter * min(key.count(letter), res_key.count(letter))
                    used_letters.add(letter)
            res_key = cur_common_str
        if res_num < 0:
            res_num = 1
        return {res_key: res_num}

    @staticmethod
    def reduce_dictionary(dictionary, divisor):  # тестить
        result = dict()
        for key in dictionary:
            new_key = ""
            for letter in key:
                new_key += letter * (key.count(letter) - divisor[0].count(letter))
            result[''.join(sorted(new_key))] = dictionary[key]/divisor[1]
        return result

    def reduce_fraction(self): # Изменяет саму дробь! тестить
        common_in_numerator = Fraction.find_common_multiplier_in_dict(self.numerator)
        common_in_denominator = Fraction.find_common_multiplier_in_dict(self.denominator)
        if common_in_denominator.keys() == common_in_numerator.keys():
            a = common_in_numerator.popitem()
            common_in_numerator_and_denominator = {a[0], gcd(a[0], common_in_denominator(a[0]))}
        else:
            common_in_numerator.update(common_in_denominator)
            common_in_numerator_and_denominator = Fraction.find_common_multiplier_in_dict(common_in_numerator)
        common_in_numerator_and_denominator = common_in_numerator_and_denominator.popitem()
        self.numerator = Fraction.reduce_dictionary(self.numerator, common_in_numerator_and_denominator)
        self.denominator = Fraction.reduce_dictionary(self.denominator, common_in_numerator_and_denominator)
        

if __name__ == '__main__':
    tester("tests_for_find_common_multiplier_in_dict.txt", [eval, Fraction.find_common_multiplier_in_dict])
    tester("tests_for_reduce_dictionary.txt", [])
    tester("tests_for_reduce_fraction.txt", [])





"""
class Fraction:

    def __init__(self, num={'1': 0}, denom={'1': 1}):
        self.numerator = dict()
        self.denominator = dict()
        for key in denom:
            self.denominator[''.join(sorted(key))] = denom[key]
        for key in num:
            self.numerator[''.join(sorted(key))] = num[key]


    def __add__(self, other):
        res_num = dict(self.numerator)
        res_denom = dict(self.denominator)
        other_num = dict(other.numerator)

        if self.denominator != other.denominator:
            res_denom = Fraction.dictionary_multiplier(self.denominator, other.denominator)
            res_num = Fraction.dictionary_multiplier(self.numerator, other.denominator)
            other_num = Fraction.dictionary_multiplier(other.numerator, self.denominator)

        for key in other_num:
            if key in res_num:
                res_num[key] += other_num[key]
            else:
                res_num[key] = other_num[key]

        return Fraction(res_num, res_denom)


    def __mul__(self, other):
        res_num = Fraction.dictionary_multiplier(self.numerator, other.numerator)
        res_denom = Fraction.dictionary_multiplier(self.denominator, other.denominator)
        return Fraction(res_num, res_denom)

    def __neg__(self):  # каждое слагаемое числителя домножаем на -1
        res_num = dict()
        res_denom = dict(self.denominator)
        for key in self.numerator:
            res_num[key] = -self.numerator[key]
        return Fraction(res_num, res_denom)

    def __sub__(self, other):  # вычитание = сложение с отрицательным
        return self.__add__(other.__neg__())

    def __truediv__(self, other):  # деление = умножение на обратную дробь
        return self.__mul__(Fraction(other.denominator, other.numerator))

    def __floordiv__(self, other):  # // делает тоже самое, что и /
        return self.__truediv__(other)

    def __str__(self):
        numerator_common_multiplier = Fraction.find_common_multiplier(self.numerator)  # Общий множитель числителя
        denominator_common_multiplier = Fraction.find_common_multiplier(self.denominator)  # Общий множитель знаменателя
        numerator_common_multiplier.update(denominator_common_multiplier) # Объединения первого и второго в один словарь
        common = Fraction.find_common_multiplier(numerator_common_multiplier)  # Общий множитель числителя и знаменателя

        self.numerator = Fraction.reduce_dict(self.numerator, common)
        self.denominator = Fraction.reduce_dict(self.denominator, common)

        zero = True  # self == 0
        only_num = True  # self.denominator == 1
        for val in self.numerator.values():
            if val:
                zero = False

        for key in self.denominator:
            if key != '1' and self.denominator[key] or\
               key == '1' and self.denominator[key] > 1:
                only_num = False

        if zero:
            return '0'
        elif only_num:
            return Fraction.dict_to_string(self.numerator)
        elif self.numerator == self.denominator:
            return '1'
        else:
            if len(self.numerator.items()) == 1:
                res = Fraction.dict_to_string(self.numerator)
            else:
                res = '(' + Fraction.dict_to_string(self.numerator) + ')'
            res += ' / '
            if len(self.denominator.items()) == 1:
                res += Fraction.dict_to_string(self.denominator)
            else:
                res += '(' + Fraction.dict_to_string(self.denominator) + ')'
            return res


    @staticmethod
    def dictionary_multiplier(a, b):  # a, b - словари, результат = a*b
        res = {}
        for Bitem in b.items():
            for Aitem in a.items():

                if Aitem[0] == '1' and Bitem[0] == '1': key = '1'
                elif Aitem[0] == '1': key = Bitem[0]
                elif Bitem[0] == '1': key = Aitem[0]
                else: key = Aitem[0] + Bitem[0]

                res[''.join(sorted(key))] = Aitem[1] * Bitem[1]

        return res

    @staticmethod
    def gcd(a, b):  # НОД 2х чисел
        a, b = map(int, map(abs, (a, b)))
        while a and b:
            if a > b:
                a %= b
            else:
                b %= a
        return a + b

    @staticmethod
    def find_common_multiplier(dct):  # НОД словаря, скорее всего не работает с одинаковыми буквами
        commonstr, commonval = '', 1
        firstiter = True
        for key, val in dct.items():
            if firstiter:
                commonstr = key
                commonval = dct[key]
                firstiter = False
                continue
            commonval = Fraction.gcd(commonval, dct[key])
            curcomstr = ''
            usd = set()
            for c in key:
                if c in usd:
                    continue
                if c in commonstr:
                    curcomstr += c * min(key.count(c), commonstr.count(c))
                    usd.add(c)
            commonstr = curcomstr
        return {commonstr: commonval}

    @staticmethod
    def reduce_dict(dct, common): #

        res = {}

        GCDstr, GCDnum = list(common.items())[0]

        for key, value in dct.items():
            curstr, curval = '', dct[key] // GCDnum
            usd = set()
            for c in key:
                if c in usd:
                    continue
                cnt = key.count(c) - GCDstr.count(c)
                curstr += c * cnt
                usd.add(c)
            res[curstr] = curval
        return res

    @staticmethod
    def dict_to_string(dct):
        res = ''
        first = True
        for key in sorted(dct.keys()):
            num = dct[key]
            if not num:
                continue
            if int(num) == num:
                num = int(num)
            if num > 0 and not first:
                res += '+'
            if abs(num) != 1 or key == '1':
                res += str(num)
            if num == -1:
                res += '-'
            first = False
            if key == '1':
                continue
            if abs(num) != 1:
                res += '*'
            res += '*'.join(key)
        return res


if __name__ == '__main__':
    a = b = c = Fraction({'hui': 1})  #  , Fraction({'huesos':1}), Fraction({'huesos':1})
    a = Fraction({'dick': 1})
    b = Fraction({'kid': 1})
    c = Fraction({'kid': 2})
    # a = Fraction({'a': 2})
    # b = Fraction({'a': 1})
    # c = Fraction({'c': 3})
    a += b
    a /= c
    print(a)
"""
