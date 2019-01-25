import pandas as pd
import numpy as np
import numpy.ma as ma
import time


class SuperSlicer:
    def __init__(self, low, high):
        self.current = low
        self.high = high

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

    def update(self, goto):
        self.current = goto


class Slice:

    def __init__(self, area, r1, r2, c1, c2):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
        self.slice = area[self.r1:self.r2,self.c1:self.c2]
 
    def __repr__(self):
        return "\nSlice : [{}:{},{}:{}]".format(self.r1, self.r2, self.c1, self.c2)


class Pizza(Slice):
    """
    Pizza
    """
    def __init__(self):
        """
        example.in
        small.in
        medium.in
        big.in
        """
        print('\n================== Initialise pizza ==================\n')
        self.filename = '../data/small.in'
        # self.ingredients_encode = {'T': '0', 'M': '1'}
        self.load_input()
        self.R, self.C, self.L, self.H = map(int, self.dataraw[0].split())
        self.pizza = np.array([list(map(int, list(e.replace('T', '0').replace('M', '1')))) for e in self.dataraw[1:]])
        # self.pizza = [list(map(int, list(e.replace(i, c) for i, c in self.ingredients.items()))) for e in self.dataraw[1:]]
        self.pizza_sliced = []
        self.mask_cuts = np.zeros(self.pizza.shape)
        self.sm_r1 = 0
        self.sm_c1 = 0

    def __repr__(self):
        return "\nPizza : ({},{})".format(self.pizza.shape[0], self.pizza.shape[1])

    def load_input(self):
        """
        R – number of rows of the pizza (1 ≤ R ≤ 1000)
        C – number of columns of the pizza (1 ≤ C ≤ 1000)
        L – number minimum of each ingredient cells in a slice (1 ≤ L ≤ 1000)
        H – number maximum of cells in a slice (1 ≤ H ≤ 1000)
        """
        f = open(self.filename,'r')
        self.dataraw = np.array([i.replace('\n', '') for i in f.readlines()])

    def display(self, area=None):
        if area is None:
            area = self.pizza
        s = [[str(e) for e in row] for row in area]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '  '.join('{{:{}}}'.format(x) for x in lens)
        matrix = [fmt.format(*row) for row in s]
        print('\n'.join(matrix))

    def display_param(self):
        print('\n------------------ Parameters ------------------')
        self.cells = self.R * self.C
        print(
            '\n R (rows) : {} \
            \n C (columns) : {} \
            \n L (number of each ingredient cells in a slice) : {} \
            \n H (Number maximum of cells in a slice) : {}' \
            .format(self.R, self.C, self.L, self.H))

    def display_constrains(self):
        print('\n------------------ Constrains ------------------')
        self.cells = self.R * self.C
        self.slice_avg_size = self.cells / self.H
        self.ingredients = self.count_ingredients(self.pizza)
        self.mix_ing_per_slice = (self.ingredients['1'] / self.ingredients['0']) / self.H
        print(
            '\n Cells in the pizza : {} \
            \n Average size of a slice : {} \
            \n Ingredients in the pizza : {} \
            \n Average mix of ingredients for a slice : {} \
            ' \
            .format(self.cells, self.slice_avg_size, self.ingredients, self.mix_ing_per_slice)
        )
        # print(np.count_nonzero(self.pizza, 1).T)

    def check(self, area=None):
        print('\t- Checking')
        if area is None:
            area = self.pizza
        cells = area.shape[0] * area.shape[1]
        ingredients = self.count_ingredients(area)
        if (ingredients['0'] <= 0) or (ingredients['1'] <= 0):
            print("\t> Wrong number of ingredients !")
            return None
        if cells >= self.H:
            print("\t> Slice too BIG ! limit cells: {}".format(self.H))
            return None
        print(
            '\t- Cells in the slice : {} \
            \n\t- Ingredients in the slice : {} \
            ' \
            .format(cells, ingredients)
        )
        return 1

    def count_ingredients(self, area):
        m = np.count_nonzero(area, 1)
        t = np.count_nonzero(area, 0)
        return {'1': sum(m), '0': sum(t)}

    def cut_a_slice(self, r1, r2, c1, c2):
        print('\t- Cut a Slice')
        pizza_slice = Slice(self.pizza, r1, r2, c1, c2)
        return pizza_slice

    def slicer(self):
        print('\n================== Slicer ==================')
        r1, c1 = 0, 0
        for i in range(1, self.cells + 1):
            r2 = r1 + 1
            c2 = c1 + 1
            pizza_slice = self.cut_a_slice(r1, r2, c1, c2)
            print('\n-------------- Slice : [{}:{},{}:{}] --------------'.format(r1,r2, c1, c2))
            pizza_slice = self.cut_a_slice(r1, r2, c1, c2)
            if self.check(area=pizza_slice.slice):
                self.display(area=pizza_slice.slice)
                r1 = r2
                c1 = c2
                self.pizza_sliced.append(pizza_slice)
                print("\t> Good slice !")


if __name__ == '__main__':
    start = time.time()

    # execute simulation
    pizza = Pizza()
    pizza.display()
    pizza.display_param()
    pizza.display_constrains()
    pizza.slicer()
 
    print('\nExecution finished in {:.2f}s'.format(time.time() - start))
