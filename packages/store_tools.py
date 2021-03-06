# Array ADT

from ctypes import py_object


class Array(object):
    def __init__(self, size):
        assert size > 0  # size must be positive
        self._size = size
        p_array = py_object*size
        self._elements = p_array()
        self.clear(None)

    def __setitem__(self, idx, value):
        assert idx in range(self._size)  # verify that idx is valid
        self._elements[idx] = value

    def __getitem__(self, idx):
        return self._elements[idx]

    def __len__(self):
        return self._size

    def clear(self, value):
        for i in range(self._size):
            self._elements[i] = value

    def __iter__(self):
        return _ArrayIterator(self._elements)

    def __add__(self, other):
        assert self._size == len(other),\
            "arrays can't be add"
        add_a = Array(self._size)
        for x in range(self._size):
            add_a[x] = self[x]+other[x]
        return add_a

    def scale_by(self, value):
        for x in range(self._size):
            self[x] *= value


class _ArrayIterator(object):
    def __init__(self, elements):
        assert elements is not None
        self._elements = elements
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


# Array ADT one-dimension
class Array2D(object):
    def __init__(self, rows, columns):
        assert rows > 0
        self._theRows = Array(rows)
        assert columns > 0
        for i in range(rows):
            self._theRows[i] = Array(columns)

    def num_rows(self):
        return len(self._theRows)

    def num_columns(self):
        return len(self._theRows[0])

    def clear(self, value):
        for i in self._theRows:
            i.clear(value)

    def __getitem__(self, idx_tuple):
        assert len(idx_tuple) == 2
        row = idx_tuple[0]
        column = idx_tuple[1]
        assert 0 <= row < self.num_rows() and\
            0 <= column < self.num_columns(),\
            "Array subscript out of range."
        column_array = self._theRows[row]
        return column_array[column]

    def __setitem__(self, idx_tuple, value):
        assert len(idx_tuple) == 2
        row = idx_tuple[0]
        column = idx_tuple[1]
        assert 0 <= row < self.num_rows() and\
            0 <= column < self.num_columns(),\
            "Array subscript out of range."
        column_array = self._theRows[row]
        column_array[column] = value


class Matrix(object):
    def __init__(self, n, m):
        self._theGrid = Array2D(n, m)
        self._theGrid.clear(0)

    def num_rows(self):
        return self._theGrid.num_rows()

    def num_columns(self):
        return self._theGrid.num_columns()

    def __getitem__(self, idx_tuple):
        return self._theGrid[idx_tuple[0], idx_tuple[1]]

    def __setitem__(self, idx_tuple, value):
        self._theGrid[idx_tuple[0], idx_tuple[1]] = value

    def scale_by(self, scale):
        for i in range(self.num_rows()):
            for j in range(self.num_columns()):
                self[i, j] *= scale

    def __add__(self, other):
        assert other.num_rows() == self.num_rows() and\
            other.num_columns() == self.num_columns(),\
            "The matrices are not compatible"
        sum_matrix = Matrix(self.num_rows(), self.num_columns())
        for i in range(self.num_rows()):
            for j in range(self.num_columns()):
                sum_matrix[i, j] = self[i, j] + other[i, j]
        return sum_matrix

    def __sub__(self, other):
        aux_matrix = other
        aux_matrix.scale_by(-1)
        return self + aux_matrix

    def print_matrix(self):
        for row in range(self.num_rows()):
            for column in range(self.num_columns()):
                print(self[row, column], end = "")
            print("")


class SyMatrix(object):
    def __init__(self, n):
        self._array = Array(n*(n+1))
        self._array.clear(None)
        self._size = n

    def get_size(self):
        return self._size

    def _transform(self, i, j):
        return j + i*(self._size - 2) + 1

    def __getitem__(self, idx_tuple):
        i = idx_tuple[0]
        j = idx_tuple[1]
        if j < i:
            temp = i
            i = j
            j = temp
        return self._array[self._transform(i, j)]

    def __setitem__(self, idx_tuple, value):
        i = idx_tuple[0]
        j = idx_tuple[1]
        if j < i:
            temp = i
            i = j
            j = temp
        self._array[self._transform(i, j)] = value

