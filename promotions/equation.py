from sympy.solvers import solve
from sympy import Symbol

class equation: #(Exercice):
    def __init__(self, equa, lettre):
        self.equa = equa
        self.lettre = lettre
        self.x = Symbol(lettre)
        self.solution = solve(self.equa,self.x)

    def isEquivalant(self, other):
        return solve(other.equa,self.x) == self.solution

    def isSolution(self, solution): #int solution
        return solution == self.solution[0]


#tests
#Equation1 = equation('a+2-(1+2)','a')
#print Equation1.isSolution(1)
#Equation2 = equation('a-(1)','a')
#print Equation1.isEquivalant(Equation2)