import sys
import sympy
from sympy.solvers import solve
from sympy import Symbol

class Equation: #(Exercice):
    def __init__(self, equation, error = None):
        self.equation = equation
        self.error = error

    def isEquivalant(self, other):
        pass

    def isSolution(self, solution):
        x = Symbol('x')
        return solution == solve(self.equation,x)[0]


#tests
Equation = Equation('x+2-(1+2)')
print Equation.isSolution(1)