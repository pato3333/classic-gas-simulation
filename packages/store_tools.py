# Array ADT

from ctypes import py_object


class Array(object):
    def __init__(self, size):
        assert size > 0  # size must be positive
        self._size = size
        p_array = py_object*self._size
        self._elements = p_array()

    def __setitem__(self, idx, value):
        assert idx in range(self._size)  # verify that idx is valid
        self._elements[idx] = value

    def __getitem__(self, idx):
        return self._elements[idx]

    def __len__(self):
        return self._size

    def clearing(self, value):
        for i in range(self._size):
            self._elements = value

    def __iter__(self):
        return ArrayIterator(self._elements)


class ArrayIterator(object):
    def __init__(self, elements):
        assert elements is not None
        self. _elements = elements
        self._idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < len(self._elements):
            value = self._elements[self._idx]
            self._idx += 1
            return value
        else:
            raise StopIteration











