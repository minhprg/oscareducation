from sympy.solvers.inequalities import reduce_rational_inequalities as solve
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr as eval
import sympy

class inequation: #(Exercice):
    def __init__(self, equation, lettre):
        self.x = Symbol(lettre)
        self.lettre = lettre
        self.equation = eval(equation)
        self.solution = solve([[self.equation]], self.x)

    def isEquivalant(self, other):
        return solve([[other.equation]],self.x) == self.solution

    def isSolution(self, solution): #string solution
        return solve([[eval(solution)]],self.x) == self.solution


#tests
#Inequation1 = inequation('a+3>5', 'a')
#print Inequation1.isSolution('a>2')
#Inequation2 = inequation('a+2>4','a')
#print Inequation1.isEquivalant(Inequation2)