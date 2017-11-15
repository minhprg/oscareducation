
from fractions import Fraction
from random import choice

from sympy import S

class GeneratorError(Exception):
    pass


class Generator(object):

    _operators = ['-', '+', '*', '/']

    @staticmethod
    def generate(degree=2, range=20, domain=S.Reals):
        pass

    @staticmethod
    def solution(e_degree, e_range):
        solutions = []

        solutions.append(choice(range(-e_range, e_range)))
        if e_degree is 2:
            solutions.append(choice(range(-e_range, e_range)))

        return tuple(solutions)
