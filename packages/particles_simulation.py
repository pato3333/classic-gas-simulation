from packages.store_tools import Array,SyMatrix
from math import sqrt
from matplotlib import pyplot as plt


def in_conditions(n, l, T):
    """
    :param n: number of particles (has to be the square of a number)
    :param l: size of the box
    :param T: temperature * k_b
    :return: initial condition arrays
    """
    in_x = Array(n)
    in_y = Array(n)
    in_vx = Array(n)
    in_vy = Array(n)

    vel0 = sqrt(T)
    part_line = int(sqrt(n))
    step = (l-1)/part_line
    j = 0
    i = 0
    for n_part in range(n):
        in_x[n_part] = (1 + j)*step
        in_vx[n_part] = vel0
        in_vy[n_part] = 0
        in_y[n_part] = (1 + i)*step
        if j < part_line - 1:
            j += 1
        else:
            j = 0
            i += 1

    return in_x, in_y, in_vx, in_vy


class Specks(object):
    def __init__(self, n, l, T, k1, k2, g):  # in_tuple are the initial condition matrices
        in_t = in_conditions(n, l, T)
        self._x = in_t[0]
        self._y = in_t[1]
        self._vx = in_t[2]
        self._vy = in_t[3]
        self._time = 0
        self.num = n
        self.k1 = k1
        self.k2 = k2
        self.g = g
        self.long_box = l
        self.height_box = l
        self._dis = None  # distance between particles
        self._force_f = None  # force field
        self._net_force = None
        self._velocity_f = None  # velocity field
        self._field_calculator()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_vx(self):
        return self._vx

    def get_vy(self):
        return self._vy

    def set_vx(self, value):
        self._vx = value

    def set_vy(self, value):
        self._vy = value

    def set_x(self, value):
        self._x = value

    def set_y(self, value):
        self._y = value

    def _field_calculator(self):
        n = self.num
        self._dist = SyMatrix(n)
        self._force = SyMatrix(n)
        self._net_force = Array(n)
        zero_a = Array(2)
        zero_a[0] = 0
        zero_a[1] = 0
        self._net_force.clear(zero_a)
        cont = 0

        for i in range(n):
            for j in range(n-i-1):
                dx = self._x[i+j+1]-self._x[i]
                dy = self._y[i+j+1]-self._y[i]
                r = sqrt(dx*dx)+sqrt(dy*dy)
                temp = Array(2)
                temp[0] = dx/r
                temp[1] = dy/r
                self._dist[i, j + i + 1] = temp  # each element of the matrix is an array
                f_l_j = 4*(12/r**13-6/r**7)
                if cont != 2 and j == 0:
                    if cont == 0:
                        f_e = self.k1*dx
                    elif cont == 1:
                        f_e = self.k2*dx
                    else:
                        raise RuntimeError("ERROR!")
                else:
                    f_e = 0
                    cont = 0
                temp2 = Array(2)
                temp2[0] = (f_l_j - f_e) * self._dist[i, j + i + 1][0]
                temp2[1] = (f_l_j - f_e) * self._dist[i, j + i + 1][1]
                self._force[i, j + i + 1] = temp2
                cont += 1
                self._net_force[i] += temp2
                self._net_force[j + 1 + i] += temp2
            temp = Array(2)
            temp[0] = 0
            temp[1] = - self.g*self._y[i]
            self._net_force[i] += temp


if __name__ == "__main__":
    plt.title("Gas simulation")
    part = Specks(144, 20, 200, 1, 2, 10)
    plt.axis([0, 20, 0, 20])
    pos_x = part.get_x()
    pos_y = part.get_y()
    plt.plot([x for x in pos_x], [y for y in pos_y], 'mo', ms=1)
    plt.show()
