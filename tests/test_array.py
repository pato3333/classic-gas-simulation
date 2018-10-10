from unittest import TestCase
from packages.store_tools import Array


class TestArray(TestCase):
    def test_clear(self):
        ar_int = Array(10)
        ar_int.clear(3)
        for i in ar_int:
            self.assertEqual(i, ar_int[i])
