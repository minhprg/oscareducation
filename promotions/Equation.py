import sys
import sympy
from sympy.solvers import solve
from sympy import Symbol

class Equation: #(Exercice):
    def __init__(self, equation, error = None):
        self.equation = equation
        x = Symbol('x')
        self.solution = solve(self.equation,x)
        self.error = error

    def isEquivalant(self, other):
        x = Symbol('x')
        return solve(other.equation,x) == self.solution

    def isSolution(self, solution): #int solution
        return solution == self.solution[0]


#tests
#Equation1 = Equation('x+2-(1+2)')
#print Equation1.isSolution(1)
#Equation2 = Equation('x-(1)')
#print Equation1.isEquivalant(Equation2)