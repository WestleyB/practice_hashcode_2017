import pandas as pd
import numpy as np
import time


class Pizza():
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
        print('\n------------------ Initialise pizza ------------------\n')
        self.filename = '../data/small.in'
        self.load_input()
        self.R, self.C, self.L, self.H = map(int, self.dataraw[0].split())
        self.pizza = [list(map(int, list(e.replace('T', '0').replace('M', '1')))) for e in self.dataraw[1:]]

    def load_input(self):
        """
        R – number of rows of the pizza (1 ≤ R ≤ 1000)
        C – number of columns of the pizza (1 ≤ C ≤ 1000)
        L – number minimum of each ingredient cells in a slice (1 ≤ L ≤ 1000)
        H – number maximum of cells in a slice (1 ≤ H ≤ 1000)
        """
        f = open(self.filename,'r')
        self.dataraw = [i.replace('\n', '') for i in f.readlines()]

    def display(self):
        s = [[str(e) for e in row] for row in self.pizza]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        matrix = [fmt.format(*row) for row in s]
        print('\n'.join(matrix))

    def display_param(self):
        print('\n------------------ Parameters ------------------\n')
        print('\n R (rows) : {}\n C (columns) : {}\n L (number of each ingredient cells in a slice) : {}\n H (Number maximum of cells in a slice) : {}' \
            .format(self.R, self.C, self.L, self.H))



if __name__ == '__main__':
    start = time.time()

    # execute simulation
    pizza = Pizza()
    pizza.display()
    pizza.display_param()
    
    print('\nExecution finished in {:.2f}s'.format(time.time() - start))
