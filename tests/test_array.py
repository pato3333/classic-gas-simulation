from unittest import TestCase
from packages import Array


class TestArray(TestCase):
    def test_clearing(self):
        ar_int = Array(10)
        ar_int.clearing(10)
        for i in ar_int:
            self.assertEqual(i, ar_int[i])
