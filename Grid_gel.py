__author__ = 'Cyprien de Salve Villedieu'
__Filename__ = 'Application_gel_final.py'
__Creationdate__ = '27/05/2020'


import numpy as np
import random as rd
import matplotlib.pyplot as plt

class Grid_gel(object) :

    def __init__(self, height: int, ratio: int, A2_liaisons: int, p_A1: float, p_A2: float, p_B: float, seed: int):
        """
        Initialize an empty grid
        :param height: The height of the grid
        :param ratio: The ratio length / height
        :param A2_liaisons: The number of liaison a A2 molecule can form ( between 2 and 6 )
        :param p_A1: Probability to be A1
        :param p_A2: Probability to be A2
        :param p_B : Probability to be B
        :param seed: The seed for random generation
        """
        length = int(height * ratio) * 2
        grid = np.empty((height, length), tuple)
        self.A2_liaisons = A2_liaisons
        self.p_A1 = p_A1
        self.p_A2 = p_A2
        self.p_B = p_B
        self.seed = seed
        for i in range(height):
            for j in range(length):
                if i % 2 != j % 2:
                    grid[i, j] = (0, 0)
        self.grid = grid

    @property
    def seed(self):
        return self.__seed

    @seed.setter
    def seed(self, x):
        if isinstance(x, int):
            self.__seed = x

    @property
    def A2_liaisons(self):
        return self.__A2_liaisons

    @A2_liaisons.setter
    def A2_liaisons(self, x):
        if isinstance(x, int) :
            self.__A2_liaisons = x

    @property
    def p_A1(self):
        return self.__p_A1

    @p_A1.setter
    def p_A1(self, x):
        if isinstance(x, float):
            self.__p_A1 = x

    @property
    def p_A2(self):
        return self.__p_A2

    @p_A2.setter
    def p_A2(self, x):
        if isinstance(x, float):
            self.__p_A2 = x

    @property
    def p_B(self):
        return self.__p_A1

    @p_B.setter
    def p_B(self, x):
        if isinstance(x, float) and  np.isclose(1,self.p_A1 + self.p_A2 + x):
            self.__p_B = x

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
    def constant_generation(cls, height: int, ratio: int, A2_liaisons ,p_A1: float, p_A2: float, p_B: float, seed=None):
        '''
        :param height: The height of the grid
        :param ratio: The ratio length / height
        :param p_A1: Probability to be A1
        :param p_A2: Probability to be A2
        :param p_B: Probability to be B
        :param seed: The seed for random generation
        :return: An instance of the grid
        '''
        if seed is None:
            seed = rd.randint(1, 10 ** 15)
        Network = cls(height, ratio, A2_liaisons, p_A1, p_A2, p_B, seed)
        size = np.shape(Network.grid)
        rd.seed(seed)
        draw = np.random.choice(['A1', 'A2', 'B'], size[0] * size[1], p=[p_A1, p_A2, p_B])
        k = 0
        for i in range(size[0]):
            for j in range(size[1]):
                if i % 2 == j % 2:
                    Network.grid[i, j] = draw[k]
                    k += 1
        return Network

    def neighborhood(self, h: int, l: int) -> list:
        '''
        find all the neighbors of the cell
        :param h: the height coordinate of cell
        :param l: the length coordinate of cell
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

    @staticmethod
    def randome_position_list(matrice):

        '''
        A map of the link between the cells
        '''

        position_list = []

        for i in range(np.shape(matrice)[0]):
            for j in range(np.shape(matrice)[1]):
                position_list += [(i, j)]
        rd.shuffle(position_list)
        return position_list

    def A1_link(self, position, link):
        """
        creat links betweenn A1 cells and his neighbors
        :param position: cells coordinates
        :param link: The output of the 'link' function
        :return:
        """
        if link[position[0], position[1]] == 0:
            rest = 2
        else:
            rest = 2 - len(link[position[0], position[1]])
        potential = []
        for k in self.neighborhood(position[0], position[1]):
            if self.grid[k[0], k[1]] == 'B' and (link[k[0], k[1]] == 0 or len(link[k[0], k[1]]) < 2):
                if link[k[0], k[1]] == 0:
                    potential += [k]

                elif (position[0], position[1]) not in link[k[0], k[1]]:
                    potential += [k]

        rd.shuffle(potential)
        for w in range(min(rest, len(potential))):
            if link[position[0], position[1]] == 0:
                link[position[0], position[1]] = [potential[w]]
            else:
                link[position[0], position[1]] += [potential[w]]

            if link[potential[w][0], potential[w][1]] == 0:
                link[potential[w][0], potential[w][1]] = [(position[0], position[1])]
            else:
                link[potential[w][0], potential[w][1]] += [(position[0], position[1])]

    def A2_link(self, position, link):
        """
        creat links betweenn A2 cells and his neighbors
        :param position: cells coordinates
        :param link: The output of the 'link' function
        :return:
        """

        if link[position[0], position[1]] == 0:
            rest = self.A2_liaisons
        else:
            rest = self.A2_liaisons - len(link[position[0], position[1]])
        potential = []
        for k in self.neighborhood(position[0], position[1]):
            if self.grid[k[0], k[1]] == 'B' and (link[k[0], k[1]] == 0 or len(link[k[0], k[1]]) < 2):
                if link[k[0], k[1]] == 0:
                    potential += [k]

                elif (position[0], position[1]) not in link[k[0], k[1]]:
                    potential += [k]

        rd.shuffle(potential)
        for w in range(min(rest, len(potential))):
            if link[position[0], position[1]] == 0:
                link[position[0], position[1]] = [potential[w]]
            else:
                link[position[0], position[1]] += [potential[w]]

            if link[potential[w][0], potential[w][1]] == 0:
                link[potential[w][0], potential[w][1]] = [(position[0], position[1])]
            else:
                link[potential[w][0], potential[w][1]] += [(position[0], position[1])]

    def B_link(self, position, link):
        """
        creat links betweenn A2 cells and his neighbors
        :param position: cells coordinates
        :param link: The output of the 'link' function
        :return:
        """


        if link[position[0], position[1]] == 0:
            rest = 2
        else:
            rest = 2 - len(link[position[0], position[1]])
        potential = []
        for k in self.neighborhood(position[0], position[1]):
            if self.grid[k[0], k[1]] == 'A1' and (link[k[0], k[1]] == 0 or len(link[k[0], k[1]]) < 2):
                if link[k[0], k[1]] == 0:
                    potential += [k]

                elif (position[0], position[1]) not in link[k[0], k[1]]:
                    potential += [k]

            if self.grid[k[0], k[1]] == 'A2' and (link[k[0], k[1]] == 0 or len(link[k[0], k[1]]) < self.A2_liaisons):
                if link[k[0], k[1]] == 0:
                    potential += [k]

                elif (position[0], position[1]) not in link[k[0], k[1]]:
                    potential += [k]

        rd.shuffle(potential)
        #            print(potential)
        for w in range(min(rest, len(potential))):
            if link[position[0], position[1]] == 0:
                link[position[0], position[1]] = [potential[w]]
            else:
                link[position[0], position[1]] += [potential[w]]

            if link[potential[w][0], potential[w][1]] == 0:  # Je pense qu'il faut aussi ajouter
                link[potential[w][0], potential[w][1]] = [(position[0], position[1])]  # le sommet étudier aux sommets du sommet relié
            else:
                link[potential[w][0], potential[w][1]] += [(position[0], position[1])]

    def link(self):
        '''
        A map of the link between the cells
        '''
        link = np.zeros(self.grid.shape, dtype=object)

        positions = self.randome_position_list(link)

        for p in positions:
            if p[0] % 2 == p[1] % 2:

                if self.grid[p[0], p[1]] == 'A1':

                    self.A1_link(p, link)

                elif self.grid[p[0], p[1]] == 'A2':

                    self.A2_link(p, link)

                elif self.grid[p[0], p[1]] == 'B':

                    self.B_link(p, link)

        return link

    @staticmethod
    def neighborhood_link(link, h: int, l: int):
        """
        :param link: The output of the fonction link applied to our grid
        :param h: The height coordinate of cell
        :param l: the length coordinate of cell
        :return: a list of tuple with the coordinates of all neighbors
        """
        if link[h, l] == 0:
            return ()
        else:
            return link[h, l]

    def high_burning_summit(self: 'Grid_gel', link, position):
        """
        burn a ama from a summit, modify the instance
        :param link : The output of the 'link' function
        :return:
        """
        burn = [position]
        while burn:
            studied = burn[0]
            val_studied = self.grid[studied[0], studied[1]]
            if val_studied == "A1" or val_studied == "A2" or val_studied == "B":
                neighborhood = self.neighborhood_link(link, studied[0], studied[1])
                burn += neighborhood
                if val_studied == 'A1':
                    self.grid[studied[0]][studied[1]] = 'A1_HB'

                if val_studied == 'A2':
                    self.grid[studied[0]][studied[1]] = 'A2_HB'

                if val_studied == 'B':
                    self.grid[studied[0]][studied[1]] = 'B_HB'

            del burn[0]

    def percol_or_not(self: 'Grid_gel'):
        """
        Us to know if a latice percol or not
        :return: True or False
        """

        for i in range(self.grid_shape[0]):
            burn = 0
            for j in range(self.grid_shape[1]):
                if i % 2 == j % 2:
                    if self.grid[i, j] == 'A1_HB' or self.grid[i, j] == 'A2_HB' or self.grid[i, j] == 'B_HB':

                        burn = 1

            if burn == 0:

                return False

        return  True

    def high_burning(self: 'Grid_gel', link):

        """
        burn amas, modify the instance
        :param link : The output of the 'link' function
        :return:
        """

        liste_j = []

        for j in range(int(self.grid_shape[1])):
            if self.grid[int(self.grid_shape[0] / 2), j][0] != "N":
                self.high_burning_summit(link, (int(self.grid_shape[0] / 2), j))
                if self.percol_or_not() == True:
                    break

                else:
                    liste_j += [str(j)]
                    for h in range(self.grid_shape[0]):
                        for k in range(self.grid_shape[1]):
                            if self.grid[h, k] == "A1_HB":
                                self.grid[h, k] = "N_A1" + str(j)

                            elif self.grid[h, k] == "A2_HB":
                                self.grid[h, k] = "N_A2" + str(j)

                            elif self.grid[h, k] == "B_HB":
                                self.grid[h, k] = "N_B" + str(j)

        if self.percol_or_not() == False:
            max = 0
            j_max = '0'

            for j in liste_j:
                n_j = 0

                for h in range(self.grid_shape[0]):
                    for k in range(self.grid_shape[1]):
                        if self.grid[h, k][:4] == 'N_A1' or self.grid[h, k][:4] == 'N_A2':
                            if self.grid[h, k][4:] == j:
                                n_j += 1

                        elif self.grid[h, k][:3] == 'N_B':
                            if self.grid[h, k][3:] == j:
                                n_j += 1


                if n_j > max:
                    max = n_j
                    j_max = j

            for h in range(self.grid_shape[0]):
                for k in range(self.grid_shape[1]):
                    if self.grid[h, k] == 'N_B' + j_max:
                            self.grid[h, k] = 'B_HB'

                    elif self.grid[h, k] == 'N_A1' + j_max:
                            self.grid[h, k] = 'A1_HB'

                    elif self.grid[h, k] == 'N_A2' + j_max:
                            self.grid[h, k] = 'A2_HB'

    def count_BA_and_A(self, link):

        """
        :param link: The output of the 'link' cells
        :return: numbre of links between A fonctions and B fonctions, number of A fonctions,
        number of links between A fonctions and B fonctions divaid by number of A fonctions
        """

        nAB = 0

        nA = 0

        for i in range (self.grid_shape[0]):
            for j in range (self.grid_shape[1]):
                if i % 2 == j % 2:
                    val_studied = self.grid[i, j]

                    if val_studied == 'B_HB' or val_studied == 'B' or val_studied == 'N_B':
                        if link[i, j] != 0:
                            nAB += len(link[i, j])

                    elif val_studied == 'A1_HB' or val_studied == 'A1' or val_studied == 'N_A1':
                        nA += 2

                    elif val_studied == 'A2_HB' or val_studied == 'A2' or val_studied == 'N_A2':
                        nA += self.A2_liaisons

        if nA == 0:
            return 'Pas de A'
        return nAB, nA, nAB/nA

    def displayGrid(self: 'Grid_gel', hull=None) -> None:
        """
        :return: the gird display
        """
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                if i % 2 == j % 2:


                    if self.grid[i, j] == 'A1':
                        plt.plot(j, i, 'wh')
                    elif self.grid[i, j] == 'A2':
                        plt.plot(j, i, 'wh')
                    elif self.grid[i, j] == 'B':
                        plt.plot(j, i, 'wh')

                    if self.grid[i, j] == 'A1_HB':
                        plt.plot(j, i, 'yh')
                    elif self.grid[i, j] == 'A2_HB':
                        plt.plot(j, i, 'ch')
                    elif self.grid[i, j] == 'B_HB':
                        plt.plot(j, i, 'kh')

        if hull:
            x = []
            y = []
            for elt in hull:
                x += [elt[1]]
                y += [elt[0] + 0.4 - (0.4 * elt[2])]
            plt.plot(x, y)
        plt.show()






