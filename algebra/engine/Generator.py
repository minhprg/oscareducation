
from fractions import Fraction
from random import choice

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.str import StrPrinter

from Expression import Expression

class GeneratorError(Exception):
    pass


class Generator(object):

    _operators = ['-', '+', '*', '/']

    @staticmethod
    def generate(degree=2, ranges=20, domain=S.Reals):
        number = choice(range(0, 10))

        if 0<=number<=5:
            return Generator.generateEquation(degree,ranges)
        elif number<=7:
            return Generator.remarkableProducts(ranges)
        elif number<=9:
            return Generator.remarkableProductsSum(ranges)
        else:
            return Generator.impossibleEquation(ranges)


    @staticmethod
    def solution(e_degree, e_range):
        solutions = []

        for i in range (0,e_degree):
            solutions.append(choice(range(-e_range, e_range)))

        return tuple(solutions)

    @staticmethod
    def generateEquation(e_degree, e_range):
        tabSolution = Generator.solution(e_degree, e_range)

        string = ""
        for i in range (0,e_degree):
            if i!=0 :
                string+="*"
            string += "(x-"+str(tabSolution[i])+")"

        return string

    @staticmethod
    def remarkableProducts(e_range):
        tabSolution = Generator.solution(2, e_range)
        string = "("+str(tabSolution[0])+"*x+"+str(tabSolution[1])+")^2"
        return string

    @staticmethod
    def remarkableProductsSum(e_range):
        tabSolution = Generator.solution(2, e_range)
        string = "("+str(tabSolution[0])+"*x)^2-("+str(tabSolution[1])+")^2"
        return string

    @staticmethod
    def impossibleEquation(e_range):
        delta=0
        while delta>=0:
            tabSolution = Generator.solution(3, e_range)
            delta = tabSolution[1]**2-4*tabSolution[0]*tabSolution[2]
        return str(tabSolution[0])+"*x^2+"+str(tabSolution[1])+"*x+"+str(tabSolution[2])

x, y, z = symbols("x y z")
maVariable = sympify(Expression._sanitize(Generator.generate()))
print simplify(maVariable)
print solveset(maVariable)
