import functools
import os

import pytest
import numpy as np

from lammps.potential import (
    write_table_pair_potential,
    write_tersoff_potential,
    write_stillinger_weber_potential,
    write_gao_weber_potential
)


def test_custom_table_potential():
    parameters = {
        ('Mg', 'O'): [1309362.2766468062, 0.104, 0.0],
        ('Mg', 'O'): [9892.357, 0.20199, 0.0],
        ('O', 'O'): [2145.7345, 0.3, 30.2222]
    }

    def buckingham_potential(r, A, p, C):
        return A * np.exp(-r/p) - C / (r**6)

    samples = 1000
    keyword = 'PAIR'
    for (e1, e2), params in parameters.items():
        f = functools.partial(buckingham_potential, A=params[0], p=params[1], C=params[2])
        e1_e2_potential = write_table_pair_potential(f, keyword=keyword, samples=samples)


def test_tersoff_potential():
    parameters = {
        ('C', 'C', 'C'):    [3.0, 1.0, 0.0, 3.8049e4, 4.3484, -0.57058, 0.72751, 1.5724e-7, 2.2119, 346.74, 1.95, 0.15, 3.4879, 1393.6],
        ('Si', 'Si', 'Si'): [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 1.1000e-6, 1.7322, 471.18, 2.85, 0.15, 2.4799, 1830.8],
        ('Ge', 'Ge', 'Ge'): [3.0, 1.0, 0.0, 1.0643e5, 15.652, -0.43884, 0.75627, 9.0166e-7, 1.7047, 419.23, 2.95, 0.15, 2.4451, 1769.0],
        ('C', 'Si', 'Si'):  [3.0, 1.0, 0.0, 3.8049e4, 4.3484, -0.57058, 0.72751, 1.5724e-7, 1.97205, 395.1451, 2.3573, 0.1527, 2.9839, 1597.3111],
        ('C', 'Si', 'C'):   [3.0, 1.0, 0.0, 3.8049e4, 4.3484, -0.57058, 0.72751, 0.0, 0.0, 0.0, 1.95, 0.15, 0.0, 0.0],
        ('C', 'C', 'Si'):   [3.0, 1.0, 0.0, 3.8049e4, 4.3484, -0.57058, 0.72751, 0.0, 0.0, 0.0, 2.3573, 0.1527, 0.0, 0.0],
        ('Si', 'C', 'C'):   [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 1.1000e-6, 1.97205, 395.1451, 2.3573, 0.1527, 2.9839, 1597.3111],
        ('Si', 'Si', 'C'):  [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 0.0, 0.0, 0.0, 2.3573, 0.1527, 0.0, 0.0],
        ('Si', 'C', 'Si'):  [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 0.0, 0.0, 0.0, 2.85, 0.15, 0.0, 0.0],
        ('Si', 'Ge', 'Ge'): [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 1.1000e-6, 1.71845, 444.7177, 2.8996, 0.1500, 2.4625, 1799.6347],
        ('Si', 'Si', 'Ge'): [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 0.0, 0.0, 0.0, 2.8996, 0.1500, 0.0, 0.0],
        ('Si', 'Ge', 'Si'): [3.0, 1.0, 0.0, 1.0039e5, 16.217, -0.59825, 0.78734, 0.0, 0.0, 0.0, 2.85, 0.15, 0.0, 0.0],
        ('Ge', 'Si', 'Si'): [3.0, 1.0, 0.0, 1.0643e5, 15.652, -0.43884, 0.75627, 9.0166e-7, 1.71845, 444.7177, 2.8996, 0.1500, 2.4625, 1799.6347],
        ('Ge', 'Si', 'Ge'): [3.0, 1.0, 0.0, 1.0643e5, 15.652, -0.43884, 0.75627, 0.0, 0.0, 0.0, 2.95, 0.15, 0.0, 0.0],
        ('Ge', 'Ge', 'Si'): [3.0, 1.0, 0.0, 1.0643e5, 15.652, -0.43884, 0.75627, 0.0, 0.0, 0.0, 2.8996, 0.1500, 0.0, 0.0],
    }
    tersoff_potential_file = write_tersoff_potential(parameters)


def test_stillinger_weber_potential():
    parameters = {
        ('Cd', 'Cd', 'Cd'): [1.03, 2.51, 1.80, 25.0, 1.20, -0.333333333333, 5.1726, 0.8807, 4.0, 0.0, 0.0],
        ('Te', 'Te', 'Te'): [1.03, 2.51, 1.80, 25.0, 1.20, -0.333333333333, 8.1415, 0.6671, 4.0, 0.0, 0.0],
        ('Cd', 'Cd', 'Te'): [1.03, 0.0 , 0.0, 25.0, 0.0, -0.333333333333, 0.0, 0.0, 0.0, 0.0, 0.0],
        ('Cd', 'Te', 'Te'): [1.03, 2.51, 1.80, 25.0, 1.20, -0.333333333333, 7.0496, 0.6022, 4.0, 0.0, 0.0],
        ('Te', 'Cd', 'Cd'): [1.03, 2.51, 1.80, 25.0, 1.20, -0.333333333333, 7.0496, 0.6022, 4.0, 0.0, 0.0],
        ('Te', 'Cd', 'Te'): [1.03, 0.0, 0.0, 25.0, 0.0, -0.333333333333, 0.0, 0.0, 0.0, 0.0, 0.0],
        ('Te', 'Te', 'Cd'): [1.03, 0.0, 0.0, 25.0, 0.0, -0.333333333333, 0.0, 0.0, 0.0, 0.0, 0.0],
        ('Cd', 'Te', 'Cd'): [1.03, 0.0, 0.0, 25.0, 0.0, -0.333333333333, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    write_stillinger_weber_potential(parameters)


def test_gao_weber_potential():
    parameters = {
        ('Si', 'Si', 'Si'): [1, 0.013318, 0, 14, 2.1, -1, 0.78000, 1, 1.80821400248640, 632.658058300867, 2.35, 0.15, 2.38684248328205, 1708.79738703139],
        ('Si', 'Si', 'C'): [1, 0.013318, 0, 14, 2.1, -1, 0.78000, 1, 1.80821400248640, 632.658058300867, 2.35, 0.15, 2.38684248328205, 1708.79738703139],
        ('Si', 'C', 'Si'): [1, 0.013318, 0, 14, 2.1, -1, 0.78000, 1, 1.96859970919818, 428.946015420752, 2.35, 0.15, 3.03361215187440, 1820.05673775234],
        ('C', 'Si', 'Si'): [1, 0.011304, 0, 19, 2.5, -1, 0.80468, 1, 1.96859970919818, 428.946015420752, 2.35, 0.15, 3.03361215187440, 1820.05673775234],
        ('C', 'C', 'Si'): [1, 0.011304, 0, 19, 2.5, -1, 0.80469, 1, 1.76776695296637, 203.208547714849, 2.35, 0.15, 2.54558441227157, 458.510465798439],
        ('C', 'Si', 'C'): [1, 0.011304, 0, 19, 2.5, -1, 0.80469, 1, 1.96859970919818, 428.946015420752, 2.35, 0.15, 3.03361215187440, 1820.05673775234],
        ('Si', 'C', 'C'): [1, 0.013318, 0, 14, 2.1, -1, 0.78000, 1, 1.96859970919818, 428.946015420752, 2.35, 0.15, 3.03361215187440, 1820.05673775234],
        ('C', 'C', 'C'): [1, 0.011304, 0, 19, 2.5, -1, 0.80469, 1, 1.76776695296637, 203.208547714849, 2.35, 0.15, 2.54558441227157, 458.510465798439]
    }
    write_gao_weber_potential(parameters)
