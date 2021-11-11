import re
import math
from collections import namedtuple


# Задача 1
def accum(text):
    up = 2
    res = text[0].upper()
    for i in text[1:]:
        res += '-' + i.upper() + i.lower() * (up - 1)
        up += 1
    print(res)


# accum('cwAt')

# Задача 2
def task2(ls1, ls2):
    n = 1
    for i in ls2:
        ls1.insert(n, i)
        n += 2
    print(ls1)


# task2(['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'])


# Задача 2 (а)
def task2_1(ls1, ls2):
    res = []
    for i, j in zip(ls1, ls2):
        res.append(i)
        res.append(j)
    print(res)


# task2_1(['a1', 'b1', 'c1'], ['a2', 'b2', 'c2'])


# Задача 3
def task3(ls):
    n = 0
    for i in ls[1:]:
        if i < ls[n]:
            res = 'Список НЕ монотонный'
            break
        n += 1
        res = 'Список монотонный'
    print(res)


# task3([1, 2, 3, 4, 5, 8, 13, 22])


# Задача 4
def task4(ls):
    s = list(set(ls))
    num = 0
    time = 0
    for i in s:
        if ls.count(i) > time:
            time = ls.count(i)
            num = i
    print(f'Число {num} повторяется {time} раз')


# task4([1, 3, 2, 3, 4, 5, 8, 13, 22, 3, 8, 25, 9, 13, 3])


# Задача 5
def task5(w, ls):
    res = []
    for i in ls:
        if sorted(w.lower()) == sorted(i.lower()):
            res.append(i)
        # print(i, sorted(i))
    print(f'для слова "{w}" анаграммами являются слова {res}')


# task5('Нос', ['рон', 'сон', 'онс', 'раву', 'сна'])

# Задача 7

def get_datetimes(text):
    res = re.findall(r'\d\d.\d\d.\d\d\d\d', text)
    if res:
        print(res)
    else:
        print('hz')


# get_datetimes('Lorem Ipsum is simply 12-01-2018 dummy text of the printing 10-13-2018 and typesetting industry.'
#               '10-02-2018 Lorem Ipsum has been the industry a s x')

# Задача 8
s = "64 bytes from 216.58.215.110: icmp_seq=0 ttl=54 time=30.391 ms" \
    "64 bytes from 216.58.215.110: icmp_seq=1 ttl=54 time=30.667 ms" \
    "64 bytes from 216.58.215.110: icmp_seq=2 ttl=54 time=33.201 ms" \
    "64 bytes from 216.58.215.110: icmp_seq=3 ttl=54 time=30.140 ms" \
    "64 bytes from 216.58.215.110: icmp_seq=4 ttl=54 time=31.822 ms"


def get_result(text):
    result = []
    pattern1 = re.findall(r'icmp_seq=\d', text)
    pattern2 = re.findall(r'time=\d*.\d*', text)
    for i, j in zip(pattern1, pattern2):
        res1 = re.findall(r'\d', i)
        res2 = re.findall(r'\d\d.\d\d\d', j)
        result_tuple = (int(res1[0]), float(res2[0]))
        result.append(result_tuple)
    print(tuple(result))


# get_result(s)

# Задача 9
class Figure:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        x = type(self.__class__.__name__)
        return f'{self.__class__.__name__}:"{self.name}"'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.square() == other.square()

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.square() < other.square()

    def __gt__(self, other):
        return isinstance(other, self.__class__) and self.square() > other.square()

    def __le__(self, other):
        return isinstance(other, self.__class__) and self.square() <= other.square()

    def __ge__(self, other):
        return isinstance(other, self.__class__) and self.square() >= other.square()


class Triangle(Figure):
    def __init__(self, name, a, b, c):
        super(Triangle, self).__init__(name)
        if a < 0 or b < 0 or c < 0:
            raise Exception('sides must be positive')
        elif (a + b < c) or (a + c < b) or (c + b < a):
            raise Exception('the sum of any two sides must be greater than the third ')
        else:
            self.side_a = a
            self.side_b = b
            self.side_c = c

    def square(self):
        p = (self.side_a + self.side_b + self.side_c) / 2  # Полупериметр
        return math.sqrt(p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c))

    def perimeter(self):
        return sum([self.side_a, self.side_b, self.side_c])


class Circle(Figure):
    def __init__(self, name, radius):
        super().__init__(name)
        if radius < 0:
            raise Exception('radius must be positive')
        else:
            self.radius = radius

    def square(self):
        return 3.14 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14 * self.radius

    def __eq__(self, other):
        return isinstance(other, Circle) and self.square() == other.square()


class Rectangle(Figure):
    def __init__(self, name, a, b):
        super(Rectangle, self).__init__(name)
        if a < 0 or b < 0:
            raise Exception('sides must be positive')
        else:
            self.side_a = a
            self.side_b = b

    def square(self):
        return self.side_a * self.side_b

    def perimeter(self):
        return 2 * (self.side_a * self.side_b)

    def __eq__(self, other):
        return isinstance(other, Rectangle) and self.square() == other.square()


# t1 = Triangle('Triangle1', 1, 2, 3)
# t2 = Triangle('Triangle2', 3, 4, 2)
# t3 = Triangle('Triangle3', 3, 2, 1)
# c1 = Circle('Circle1', 41)
# c2 = Circle('Circle2', 23)
# c3 = Circle('Circle3', 41)
# r1 = Rectangle('rec1', 2, 5)
# r2 = Rectangle('rec2', 5, 6)
# r3 = Rectangle('rec3', 5, 2)


