from sympy.solvers import solve
from sympy import Symbol
from sympy import linsolve, symbols
from sympy.parsing.sympy_parser import parse_expr as eval
from sympy.parsing.sympy_parser import standard_transformations as st
from sympy.parsing.sympy_parser import implicit_multiplication_application as imp
# Based on http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html

class Exercice(object):
    # Create based on class name:
    def factory(type):
        #return eval(type + "()")
        if type == "Equation": return Equation()
        if type == "Inequation": return Inequation()
        if type == "System": return System()
    factory = staticmethod(factory)


class Equation: #(Exercice):
    def __init__(self, equa, lettre):
        self.equa = equa
        self.lettre = lettre
        self.x = Symbol(lettre)
        self.solution = solve(self.equa,self.x)

    def isEquivalant(self, other):
        return solve(other.equa,self.x) == self.solution

    def isSolution(self, solution): #int solution
        if (type(solution) == int):
            return solution == self.solution[0]
        else:
            return False



class Inequation: #(Exercice):
    def __init__(self, equation, lettre):
        self.x = Symbol(lettre)
        self.lettre = lettre
        self.equation = eval(equation,transformations=(st+(imp,)))
        self.solution = solve([[self.equation]], self.x)
        print self.solution

    def isEquivalant(self, other):
        return solve([[eval(other,transformations=(st+(imp,)))]],self.x) == self.solution

    def isSolution(self, solution): #string solution
        nbr = ''
        boolNbr = 0
        lettre = ''
        boolLettre = 0
        boolCondition = 0
        i = 0
        while(i<len(solution)): # ca marche tg
            if(solution[i].isdigit() and boolNbr==0):
                nbr = nbr+solution[i]
            elif(solution[i].islower() and boolLettre==0):
                boolLettre = 1
                lettre = lettre+solution[i]
            elif(((solution[i] == "<" and solution[i+1] == "=") or (solution[i] == ">" and solution[i+1] == "=")) and boolCondition == 0):
                i = i+1
                boolCondition = 1
                if(nbr != ''): boolNbr = 1
            elif ((solution[i] == "<" or solution[i] == ">") and boolCondition == 0):
                boolCondition = 1
                if (nbr != ''): boolNbr = 1
            else:
                return False
            i = i+1
        return solve([[eval(solution,transformations=(st+(imp,)))]],self.x) == self.solution


class System: #(Exercice):
    def __init__(self, sys, var):
        self.sys = [eval(x,transformations=(st+(imp,))) for x in sys]
        self.var = symbols(var)
        self.solution = linsolve(self.sys, self.var)

    def isEquivalant(self, other):
        return other.solution == self.solution

    def isSolution(self, solution, var): #int solution

        return linsolve([eval(x,transformations=(st+(imp,))) for x in solution], symbols(var)) == self.solution



# tests Equation
# Equation1 = Equation('a+2-(1+2)','a')
# print Equation1.isSolution(1)
# Equation2 = Equation('a-(1)','a')
# print Equation1.isEquivalant(Equation2)

# tests Inequation
# Inequation1 = Inequation('a+3>5', 'a')
# print Inequation1.isSolution('3<a+1')
# print Inequation1.isEquivalant('3<a+1')

#tests System
#System1 = System(['2x-2', 'y+x'], "x, y") # 2x=2 y+x=0
#print System1.isSolution(['x-3/2','y+3/2'],"x, y") # x=3/2 y=-3/2
#System2 = System(['x-3/2', 'y+x'], "x, y") # x=5 x=-y
#print System1.isEquivalant(System2)