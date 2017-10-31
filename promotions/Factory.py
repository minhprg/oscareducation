from __future__ import division
from sympy.solvers import solve
from sympy.solvers.inequalities import reduce_rational_inequalities as solveIn
from sympy import Symbol
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr as eval
from sympy.parsing.sympy_parser import standard_transformations as st
from sympy.parsing.sympy_parser import implicit_multiplication_application as imp
from sympy import Poly
import InputHandler
from sympy import linsolve
import sys
import traceback
# Based on http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html

def factory(type,question,letter):
    #return eval(type + "()")
    if type == "algebraicEquation": return Equation(question,letter)
    if type == "algebraicInequation": return Inequation(question,letter)
    if type == "algebraicSystem": return System(question,letter)


class Equation: #(Exercice):
    def __init__(self, equa, lettre):
        self.equa = equa
        self.lettre = lettre
        self.x = Symbol(lettre)
        self.solution = solve(self.equa,self.x)

    def isEquivalant(self, other): # self est l'equation precedente

        leftOther, rightOther, coeffLeftOther, coeffRightOther = other.analyse()
        leftPrevious, rightPrevious, coeffLeftPrevious, coeffRightPrevious = self.analyse()
        hint = None
        if(other.solution == self.solution):
            if(not(str(leftOther).lstrip("-").replace("/","").isdigit()) and coeffLeftOther[0] == 0):
                hint = 'Aide : simplifie a gauche'
            elif(not(str(rightOther).lstrip("-").replace("/","").isdigit()) and coeffRightOther[0] == 0):
                hint = 'Aide : simplifie a droite'
            elif(coeffLeftOther[0]!=0 and coeffRightOther[0]!=0):
                hint = 'Aide : isole la variable a gauche en applicant une operation de chaque cote'
            elif(coeffLeftOther[1] != 0 and coeffRightOther[0] == 0):
                hint = 'Aide : isole la variable de gauche en applicant une operation de chaque cote'
            elif(coeffRightOther[1] != 0 and coeffLeftOther[0] == 0):
                hint = 'Aide : isole la variable de droite en applicant une operation de chaque cote'
            elif(coeffLeftOther[0] != 1 and coeffRightOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation'
            elif (coeffRightOther[0] != 1 and coeffLeftOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation'
            return (True,hint)
        else:
            if(coeffLeftPrevious[0] == coeffLeftOther[0] and coeffLeftOther[1]-coeffLeftPrevious[1] != coeffRightOther[1]-coeffRightPrevious[1]):
                hint = 'Aide : tu as fait +('+str(coeffLeftOther[1]-coeffLeftPrevious[1])+') a gauche et +('\
                       +str(coeffRightOther[1]-coeffRightPrevious[1])+') a droite'
                return (False,hint)
            ratio = None
            if coeffLeftPrevious[0] !=0 and coeffLeftOther[0] != 0 :
                ratio = coeffLeftPrevious[0]/coeffLeftOther[0]
            if coeffLeftPrevious[1] !=0 and coeffLeftOther[1] != 0:
                if ratio is not None and coeffLeftPrevious[1]/coeffLeftOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False,hint)
                if ratio is None:
                    ratio = coeffLeftPrevious[1]/coeffLeftOther[1]

            if coeffRightPrevious[0] !=0 and coeffRightOther[0] != 0:
                if ratio is not None and coeffRightPrevious[0]/coeffRightOther[0] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False,hint)
                if ratio is None:
                    ratio = coeffRightPrevious[0]/coeffRightOther[0]

            if coeffRightPrevious[1] !=0 and coeffRightOther[1] != 0:
                if ratio is not None and coeffRightPrevious[1]/coeffRightOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False,hint)

            return (False,hint)


    def isSolution(self, solution): # self: equation de base, solution: derniere equation
        if (self.isEquivalant(solution)[1] is None):
            return True
        else:
            return False

    def analyse(self):
        left = ''
        right = ''

        i = len(self.equa)-1
        parenthese = 0
        mid = 0
        while(i>0):
            if(self.equa[i] == ')'):
                parenthese = parenthese + 1
            elif(self.equa[i] == '('):
                parenthese = parenthese - 1
            elif(parenthese == 0):
                mid = i
                i = -1
            i = i-1

        i = 0
        while(i<mid):
            left = left+self.equa[i]
            i = i+1
        i = mid+2
        while(i<len(self.equa)-1):
            right = right+self.equa[i]
            i = i+1

        coeffLeft = eval(left,transformations=(st+(imp,)))
        coeffRight = eval(right,transformations=(st+(imp,)))

        if(not(str(coeffLeft).lstrip("-").replace("/","").isdigit())):
            coeffLeft = Poly(coeffLeft).all_coeffs()
        else:
            coeffLeft = [0, coeffLeft]
        if(not(str(coeffRight).lstrip("-").replace("/","").isdigit())):
            coeffRight = Poly(coeffRight).all_coeffs()
        else:
            coeffRight = [0, coeffRight]
        return left, right, coeffLeft, coeffRight


class Inequation: #(Exercice):
    def __init__(self, equation, lettre):
        self.x = Symbol(lettre)
        self.lettre = lettre
        self.equa = equation # top kek
        self.equation = eval(equation,transformations=(st+(imp,)))
        self.solution = solveIn([[self.equation]], self.x)

    def isEquivalant(self, other):

        leftOther, rightOther, coeffLeftOther, coeffRightOther, conditionOther = other.analyse()
        leftPrevious, rightPrevious, coeffLeftPrevious, coeffRightPrevious, conditionPrevious = self.analyse()
        hint = None

        if (other.solution == self.solution):
            if (not (str(leftOther).lstrip("-").replace("/", "").isdigit()) and coeffLeftOther[0] == 0):
                hint = 'Aide : simplifie a gauche'
            elif (not (str(rightOther).lstrip("-").replace("/", "").isdigit()) and coeffRightOther[0] == 0):
                hint = 'Aide : simplifie a droite'
            elif (coeffLeftOther[0] != 0 and coeffRightOther[0] != 0):
                hint = 'Aide : isole la variable a gauche en applicant une operation de chaque cote'
            elif (coeffLeftOther[1] != 0 and coeffRightOther[0] == 0):
                hint = 'Aide : isole la variable de gauche en applicant une operation de chaque cote'
            elif (coeffRightOther[1] != 0 and coeffLeftOther[0] == 0):
                hint = 'Aide : isole la variable de droite en applicant une operation de chaque cote'
            elif (coeffLeftOther[0] != 1 and coeffRightOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation'
            elif (coeffRightOther[0] != 1 and coeffLeftOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation'
            return (True, hint)
        else:
            if (coeffLeftPrevious[0] == coeffLeftOther[0] and coeffLeftOther[1] - coeffLeftPrevious[1] !=
                    coeffRightOther[1] - coeffRightPrevious[1]):
                hint = 'Aide : tu as fait +(' + str(coeffLeftOther[1] - coeffLeftPrevious[1]) + ') a gauche et +(' \
                       + str(coeffRightOther[1] - coeffRightPrevious[1]) + ') a droite'
                return (False,hint)
            ratio = None
            if coeffLeftPrevious[0] != 0 and coeffLeftOther[0] != 0:
                ratio = coeffLeftPrevious[0] / coeffLeftOther[0]
            if coeffLeftPrevious[1] != 0 and coeffLeftOther[1] != 0:
                if ratio is not None and coeffLeftPrevious[1] / coeffLeftOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
                if ratio is None:
                    ratio = coeffLeftPrevious[1] / coeffLeftOther[1]
            if coeffRightPrevious[0] != 0 and coeffRightOther[0] != 0:
                if ratio is not None and coeffRightPrevious[0] / coeffRightOther[0] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
                if ratio is None:
                    ratio = coeffRightPrevious[0] / coeffRightOther[0]
            if coeffRightPrevious[1] != 0 and coeffRightOther[1] != 0:
                if ratio is not None and coeffRightPrevious[1] / coeffRightOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
            if conditionOther != conditionPrevious:
                hint = "Aide : le signe d'equivalence n'est pas dans la bon sens"
            return (False, hint)


    def isSolution(self, solution): #string solution
        nbr = ''
        boolNbr = 0
        lettre = ''
        boolLettre = 0
        boolCondition = 0
        i = 0
        while(i<len(solution)): # ca marche tg
            if((solution[i].isdigit() or solution[i]=="/" or solution[i]=="-") and boolNbr==0):
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
        return solveIn([[eval(solution,transformations=(st+(imp,)))]],self.x) == self.solution

    def analyse(self):
        left = ''
        right = ''
        condition = ''

        i = 0
        while(not(self.equa[i] == "<" or self.equa[i] == ">")):
            left = left+self.equa[i]
            i = i+1
        condition = condition+self.equa[i]
        i = i+1
        if(self.equa[i] == "="):
            condition = condition + self.equa[i]
            i = i+1
        while(i<len(self.equa)):
            right = right+self.equa[i]
            i = i+1

        coeffLeft = eval(left,transformations=(st+(imp,)))
        coeffRight = eval(right,transformations=(st+(imp,)))

        if(not(str(coeffLeft).lstrip("-").replace("/","").isdigit())):
            coeffLeft = Poly(coeffLeft).all_coeffs()
        else:
            coeffLeft = [0, coeffLeft]
        if(not(str(coeffRight).lstrip("-").replace("/","").isdigit())):
            coeffRight = Poly(coeffRight).all_coeffs()
        else:
            coeffRight = [0, coeffRight]

        return left, right, coeffLeft, coeffRight, condition



class System: #(Exercice):
    def __init__(self, sys, var):
        self.sys = [eval(x,transformations=(st+(imp,))) for x in sys]
        self.var = symbols(var)
        self.solution = linsolve(self.sys, self.var)

    def isEquivalant(self, other):
        return other.solution == self.solution

    def isSolution(self, solution): #int solution
        for s in solution:
            if(not(s in list(self.solution)[0])):
                return False
        return True



# tests Equation
#handler = InputHandler.InputHandler()
#eq1 = u'4*a-8 = 2*a +16'
#Equation1.analyse()
#Equation1 = Equation(handler.parse(eq1),'a')

#Equation1 = None
#print "Rentrez l'equation a resoudre"
#print Equation1.isSolution(-1)
"""for line in iter(sys.stdin.readline,''):
    try:
        if Equation1 == None:
            string = handler.parse(unicode(line.strip(),"utf-8"))
            print string
            Equation1 = Equation(string,"a")
            Equation1.analyse()
            print "Vous pouvez maintenant entrer les etapes de resolution"
       #print line
        else:
            string = handler.parse(unicode(line.strip(),"utf-8"))
            Equation2 = Equation(string,'a')
            temp = Equation1.isEquivalant(Equation2)
            print temp
            if temp[0] and temp[1] is None:
                break
    except Exception as e:
        traceback.print_exc()
        print "L'expression de l'equation n'est pas bonne (parse error)"""


# tests Inequation
#Inequation1 = Inequation('4*a-1/4>0', 'a')
#Inequation2 = Inequation('a>1/16','a')
#print Inequation1.isSolution('a>1/16')
#print Inequation1.isEquivalant(Inequation2)


#tests System
System1 = System(['2x-2', 'y+x'], "x, y") # 2x=2 y+x=0
print System1.isSolution([-1, 1]) # x=-1 y=1 ou l'inverse
System2 = System(['x-1', 'y+x'], "x, y") # x=1 x=-y
print System1.isEquivalant(System2)
