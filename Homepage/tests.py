# from views import two_list
from django.test import TestCase
import unittest


class Tests(unittest.TestCase):
    def test_two_list(self):
        result = two_list([2, 13, 5, 8], [6, 8, 2, 33])
        self.assertTrue(result == [2, 8])

    def test_two_list_del(self):
        result = two_list_del([2, 13, 1], [6, 2])
        self.assertTrue(result == [13, 1])


def two_list(ls1, ls2):
    ls3 = []
    for i in ls1:
        if i in ls2:
            ls3.append(i)
    return ls3


def two_list_del(ls1, ls2):
    ls3 = []
    for i in ls1:
        if i not in ls2:
            ls3.append(i)
    return ls3


if __name__ == '__main__':
    unittest.main()