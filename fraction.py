
class Fraction:

    def __init__(self, num={'1': 0}, denom={'1': 1}):
        self.numerator = {}
        self.denominator = {}
        for key in num:
            self.numerator[''.join(sorted(key))] = num[key]
        for key in denom:
            self.denominator[''.join(sorted(key))] = denom[key]

    def __add__(self, other):
        res_num = dict(self.numerator)
        res_denom = dict(self.denominator)
        other_num = dict(other.numerator)

        if self.denominator != other.denominator:
            res_denom = Fraction.dict_mul(self.denominator, other.denominator)
            res_num = Fraction.dict_mul(self.numerator, other.denominator)
            other_num = Fraction.dict_mul(other.numerator, self.denominator)

        for key in other_num:
            if key in res_num:
                res_num[key] += other_num[key]
            else:
                res_num[key] = other_num[key]

        return Fraction(res_num, res_denom)


    def __mul__(self, other):
        res_num = Fraction.dict_mul(self.numerator, other.numerator)
        res_denom = Fraction.dict_mul(self.denominator, other.denominator)
        return Fraction(res_num, res_denom)

    def __neg__(self):  # каждое слагаемое числителя домножаем на -1
        res_num = {}
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
            return '(' + Fraction.dict_to_string(self.numerator) + ') / ' +\
                   '(' + Fraction.dict_to_string(self.denominator) + ')'

    @staticmethod
    def dict_mul(a, b): # a, b - dicts, return a*b
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
    # a = Fraction({'xy': 3})
    # b = Fraction({'xy': 4})
    c = Fraction({'huesos': 1})
    d = Fraction({'1': 0.5})
    # print(Fraction() + Fraction()* Fraction({'1': 1}))
    # res1 = a + a - (b * c) + (a * b * c * d) - c - d - a # работает?
    # res2 = a + a - b * c + a * b * c * d - c - d - a
    # print(res1, res2, str(res1) == str(res2), sep = '\n')
    res3 = c + d * c
    print(res3)
