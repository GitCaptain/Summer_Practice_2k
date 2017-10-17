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
        if not other:
            raise ArithmeticError
        return self.__mul__(Fraction(other.denominator, other.numerator))

    def __floordiv__(self, other):  # // делает тоже самое, что и /
        return self.__truediv__(other)

    def __bool__(self):
        for val in self.numerator.values():
            if val:
                return True
        return False

    def __str__(self):
        self = self.reduce_fraction()
        zero = not self.__bool__()
        only_num = True

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
            used_letters = set()
            for letter in key:
                if not letter in used_letters:
                    new_key += letter * (key.count(letter) - divisor[0].count(letter))
                    used_letters.add(letter)
            if not new_key:
                new_key = '1'
            result[''.join(sorted(new_key))] = dictionary[key]/divisor[1]
        return result

    def reduce_fraction(self):  # тестить
        common_in_numerator = Fraction.find_common_multiplier_in_dict(self.numerator)
        common_in_denominator = Fraction.find_common_multiplier_in_dict(self.denominator)
        if common_in_denominator.keys() == common_in_numerator.keys():
            common_item = common_in_numerator.popitem()
            common_in_numerator_and_denominator = {common_item[0]: gcd(common_item[1], common_in_denominator[common_item[0]])}
        else:
            common_in_numerator.update(common_in_denominator)
            common_in_numerator_and_denominator = Fraction.find_common_multiplier_in_dict(common_in_numerator)
        common_in_numerator_and_denominator = common_in_numerator_and_denominator.popitem()
        new_numerator = Fraction.reduce_dictionary(self.numerator, common_in_numerator_and_denominator)
        new_denominator = Fraction.reduce_dictionary(self.denominator, common_in_numerator_and_denominator)
        return Fraction(new_numerator, new_denominator)
        

if __name__ == '__main__':
    # tester("tests_for_find_common_multiplier_in_dict.txt", [eval, Fraction.find_common_multiplier_in_dict])
    """
    a = {'xy':5, 'y':5}
    print(Fraction.reduce_dictionary(a, ('y', 5)))
    a = {'xyp': 15, 'zyx': 25}
    print(Fraction.reduce_dictionary(a, ('xy', 5)))
    a = {'kk': 15, 'spec': 70}
    print(Fraction.reduce_dictionary(a, ('', 5)))
    """
    """
    a = Fraction({'xy':5, 'y':5}, {'zyx':12, 'y':1})
    print(a.reduce_fraction(), a, sep = '\n')
    a = Fraction({'xy':5, 'pyx':5}, {'zyx':25, 'cyx':15})
    print(a.reduce_fraction(), a, sep='\n')
    """
    #tester("tests_for_reduce_dictionary.txt", [])
    #a = Fraction({'xy': 5, 'y': 5}, {'zyx': 12, 'y': 1})
    #print(a.reduce_fraction())
    # tester("tests_for_reduce_fraction.txt", [])
