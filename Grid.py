__author__ = 'Gastaldi'
__Filename__ = 'Grid'
__Creationdate__ = '29/02/2020'

import numpy as np
import random as rd
import matplotlib.pyplot as plt


class Grid(object):

    def __init__(self, height: int, ratio: int, p_max: float, p_min: float, seed: int):
        '''
        Initialize an empty grid
        :param height: the height of the grid
        :param ratio: the ratio length / height
        :param p_max: maximal probability
        :param p_min: minimal probability
        :param seed:
        '''
        length = int(height * ratio) * 2
        grid = np.empty((height, length), tuple)
        self.p_max = p_max
        self.p_min = p_min
        self.seed = seed
        for i in range(height):
            for j in range(length):
                if i % 2 != j % 2:
                    grid[i, j] = (0, 0)
        self.grid = grid

    @property
    def p_max(self):
        return self.__p_max

    @p_max.setter
    def p_max(self, x):
        if 0 <= x <= 1.:
            self.__p_max = x

    @property
    def p_min(self):
        return self.__p_min

    @p_min.setter
    def p_min(self, x):
        if 0 <= x <= self.p_max:
            self.__p_min = x

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, x):
        if isinstance(x, int):
            self.__seed = x

    @property
    def grid(self):
        return self.__grid

    @grid.setter
    def grid(self, x):
        self.__grid = x

    @property
    def grid_shape(self):
        size = np.shape(self.grid)
        return size

    @classmethod
    def linear_generation(cls, height: int, ratio: int, p_max: float = 0.5, p_min: float = 0., seed=None) -> 'Grid':
        '''
        Generate a Grid with a gradient of probability
        :param height: the height of the grid
        :param ratio: the ratio length / height
        :param p_max: maximal probability
        :param p_min: minimal probability
        :param seed:
        :return: an instance of the Grid
        '''
        if seed is None:
            seed = rd.randint(1, 10 ** 15)
        Network = cls(height, ratio, p_max, p_min, seed)
        size = np.shape(Network.grid)
        rd.seed(seed)
        for i in range(size[0]):
            prob = p_max - (i * ((p_max - p_min) / size[0]))
            for j in range(size[1]):
                if i % 2 == j % 2:
                    value = rd.random()
                    if value <= prob:
                        Network.grid[i, j] = 1
                    else:
                        Network.grid[i, j] = 0
        return Network

    @classmethod
    def constant_generation(cls, height: int, ratio: int, probability: float, seed=None) -> 'Grid':
        '''
        Generate a Grid with same of probability on all line
        :param height: the height of the grid
        :param ratio: the ratio length / height
        :param probability: probability to be blue
        :param seed:
        :return: an instance of grid class
        '''
        if seed is None:
            seed = rd.randint(1, 10 ** 15)
        Network = cls(height, ratio, probability, probability, seed)
        size = np.shape(Network.grid)
        rd.seed(seed)
        for i in range(size[0]):
            for j in range(size[1]):
                if i % 2 == j % 2:
                    value = rd.random()
                    if value <= probability:
                        Network.grid[i, j] = 1
                    else:
                        Network.grid[i, j] = 0
        return Network

    def neighborhood(self, h: int, l: int) -> list:
        '''
        find all the neighbors of the cell
        :param h: the height coordinate of cell
        :param l: the height coordinate of cell
        :return: a list of tuple with the coordinates of all neighbors
        '''
        height, length = self.grid.shape

        if h == 0:
            return [(h + 1, (l - 1) % length), (h + 1, (l + 1) % length),
                    (h, (l - 2) % length), (h, (l + 2) % length)]
        if h == height - 1:
            return [(h - 1, (l - 1) % length), (h - 1, (l + 1) % length),
                    (h, (l - 2) % length), (h, (l + 2) % length)]
        else:
            return [(h - 1, (l - 1) % length), (h - 1, (l + 1) % length),
                    (h + 1, (l - 1) % length), (h + 1, (l + 1) % length),
                    (h, (l - 2) % length), (h, (l + 2) % length)]

    def high_burning(self):
        """
        burn the main ama, modify the instance
        :return:
        """
        height, length = self.grid.shape
        percolation = False
        burn = [(0, i) for i in range(0, length - 1, 2)]
        while burn:
            studied = burn[0]
            val_studied = self.grid[studied[0], studied[1]]
            if val_studied == 0 or val_studied == 1:
                neighborhood = self.neighborhood(studied[0], studied[1])
                for neighbor in neighborhood:
                    if (val_studied == 0 and self.grid[neighbor[0]][neighbor[1]] == 1) or (val_studied == 1 and self.grid[neighbor[0]][neighbor[1]] == 0):
                        burn += [neighbor]
                self.grid[studied[0]][studied[1]] += 10
            del burn[0]
        return percolation

    def low_burning(self):
        """
        burn the secondary ama, modify the instance
        :return:
        """
        burn = []
        for i in range(self.grid_shape[1]):
            if isinstance(self.grid[-1, i], int) and self.grid[-1, i] == 0:
                burn += [(self.grid_shape[0] - 1, i)]
        while burn:
            studied = burn[0]
            val_studied = self.grid[studied[0], studied[1]]
            if val_studied == 0:
                neighborhood = self.neighborhood(studied[0], studied[1])
                for neighbor in neighborhood:
                    if self.grid[neighbor[0]][neighbor[1]] == 0:
                        burn += [neighbor]
                self.grid[studied[0]][studied[1]] += 20
            del burn[0]

    def demarcation_line(self) -> list:
        """
        find the demarcation line, modify the instance
        :return: the list of tuple, contain the coordinate of demarcation's point
        """
        burn = []
        demarcation_line = []
        i = 0
        while not burn:
            if self.grid[(i + 1), (i + 1) % 2] == 20:
                burn = [(i, i % 2)]
            i += 1
        while burn:
            studied = burn[0]
            neighborhood = self.neighborhood(studied[0], studied[1])
            if self.grid[studied[0], studied[1]] == 10:
                for neighbor in neighborhood:
                    if self.grid[neighbor[0], neighbor[1]] == 10:
                        for neighbor2 in self.neighborhood(neighbor[0], neighbor[1]):
                            if self.grid[neighbor2[0], neighbor2[1]] == 20:
                                burn += [neighbor]
                demarcation_line += [studied]
                self.grid[studied[0], studied[1]] += 100
            del burn[0]
        return demarcation_line

    def demarcation_line_probability(self, demarcation_line: list) -> float:
        """
        calcul the critical probability
        :param demarcation_line: the output of demarcation_line
        :return: return the critical probability
        """
        prob_t = 0
        for cell in demarcation_line:
            prob_t += self.p_max - (cell[0] * ((self.p_max - self.p_min) / self.grid_shape[0]))
        prob = prob_t / len(demarcation_line)
        return prob

    def triangulation(self, h, l, d):
        """

        :param h:
        :param l:
        :param d:
        :return:
        """
        height, length = self.grid.shape
        if d % 3 == 0:
            return [(h, (l - 1) % length), (h, (l + 1) % length)]
        if d == 1:
            return [(h, (l + 1) % length), (h + 1, l)]
        if d == 2:
            return [(h, (l + 1) % length), (h - 1, l)]
        if d == 4:
            return [(h, (l - 1) % length), (h - 1, l)]
        if d == 5:
            return [(h, (l - 1) % length), (h + 1, l)]

    def go_forward(self, h, l, d):
        next = self.triangulation(h, l, d)
        next1 = next[0]
        next2 = next[1]
        if self.grid[next1[0], next1[1]] % 10 == 0 and self.grid[next2[0], next2[1]] % 10 == 0:
            return True
        else:
            return False

    def hull_begin(self, demarcation):
        height, length = self.grid.shape
        for point in demarcation:
            if self.grid[point[0], (point[1] + 2) % length] == 110:
                start = (point[0], (point[1] + 1) % length)
                return start
            elif self.grid[point[0], (point[1] - 2) % length] == 110:
                start = (point[0], (point[1] - 1) % length)
                return start

    def hull(self, demarcation):
        """
        find the hull
        :param demarcation: the output of demarcation_line
        :return: the list of coordinate of the hull
        """
        height, length = self.grid.shape
        start_point = self.hull_begin(demarcation)
        p = 0
        d = 1
        point = list(start_point)
        hull = []
        if self.go_forward(point[0], point[1], d):
            hull += [[point[0], point[1], p]]
            point[0] += 1
            point[1] = (point[1] + 1) % length
            d = d + 1 % 6
            p = 1
        else:
            d = d + 2 % 6
        while list(start_point) != point or d != 1:
            if self.go_forward(point[0], point[1], d):
                hull += [[point[0], point[1], p]]
                if d == 1:
                    point[0] += 1
                    point[1] = (point[1] + 1) % length
                if d == 2:
                    point[0] -= 1
                    point[1] = (point[1] + 1) % length
                if d == 4:
                    point[0] -= 1
                    point[1] = (point[1] - 1) % length
                if d == 5:
                    point[0] += 1
                    point[1] = (point[1] - 1) % length
                p = (p + 1) % 2
                d = (d + 1) % 6
            else:
                d = (d + 2) % 6
        return hull

    def hull_probability(self, hull):
        """

        :param hull: the output of hull
        :return: the critical probability
        """
        prob_t = 0
        delta_p = (self.p_max - self.p_min) / self.grid_shape[0]
        for cell in hull:
            prob_t += self.p_max - ((cell[0] * delta_p) + (delta_p / 3) - ((2 * delta_p)/3 * cell[2]))
        prob = prob_t / len(hull)
        return prob

    def displayGrid(self: 'Grid', hull=None) -> None:
        """
        :return: the gird display
        """
        delta_p = self.p_max - self.p_min
        p = self.p_min
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                if i % 2 == j % 2:
                    if self.grid[i, j] == 0:
                        plt.plot(j, i, 'rh')
                    elif self.grid[i, j] == 1:
                        plt.plot(j, i, 'bh')
                    elif self.grid[i, j] == 10:
                        plt.plot(j, i, 'yh')
                    elif self.grid[i, j] == 11:
                        plt.plot(j, i, 'mh')
                    elif self.grid[i, j] == 20:
                        plt.plot(j, i, 'ch')
                    elif self.grid[i, j] == 110:
                        plt.plot(j, i, 'gh')
        if hull:
            x = []
            y = []
            for elt in hull:
                x += [elt[1]]
                y += [elt[0] + 0.4 - (0.4 * elt[2])]
            plt.plot(x, y,)
        plt.show()
