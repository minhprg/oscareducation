from __future__ import division
from sympy.solvers import solve
from sympy.solvers.inequalities import reduce_rational_inequalities as solveIn
from sympy import Symbol
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr as eval
from sympy.parsing.sympy_parser import standard_transformations as st
from sympy.parsing.sympy_parser import implicit_multiplication_application as imp
from sympy import Poly
import copy
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
    if type == "algebraicExpression":return Expression(question)


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
                hint = 'Aide : isole la variable en applicant une operation de chaque cote'
            elif(coeffLeftOther[1] != 0 and coeffRightOther[0] == 0):
                hint = 'Aide : isole la variable de gauche en applicant une operation de chaque cote'
            elif(coeffRightOther[1] != 0 and coeffLeftOther[0] == 0):
                hint = 'Aide : isole la variable de droite en applicant une operation de chaque cote'
            elif(coeffLeftOther[0] != 1 and coeffRightOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote'
            elif (coeffRightOther[0] != 1 and coeffLeftOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote'
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
                hint = 'Aide : isole la variable en applicant une operation de chaque cote'
            elif (coeffLeftOther[1] != 0 and coeffRightOther[0] == 0):
                hint = 'Aide : isole la variable de gauche en applicant une operation de chaque cote'
            elif (coeffRightOther[1] != 0 and coeffLeftOther[0] == 0):
                hint = 'Aide : isole la variable de droite en applicant une operation de chaque cote'
            elif (coeffLeftOther[0] != 1 and coeffRightOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote'
            elif (coeffRightOther[0] != 1 and coeffLeftOther[0] == 0):
                hint = 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote'
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
            elif (coeffLeftPrevious[0] != 0 and coeffLeftOther[0] == 0) or (coeffLeftPrevious[0] == 0 and coeffLeftOther[0] != 0):
                return (False, "Aide : le signe d'equivalence n'est pas dans la bon sens")
            if coeffLeftPrevious[1] != 0 and coeffLeftOther[1] != 0:
                if ratio is not None and coeffLeftPrevious[1] / coeffLeftOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
                if ratio is None:
                    ratio = coeffLeftPrevious[1] / coeffLeftOther[1]
            elif (coeffLeftPrevious[1] != 0 and coeffLeftOther[1] == 0) or (coeffLeftPrevious[1] == 0 and coeffLeftOther[1] != 0):
                return (False, "Aide : le signe d'equivalence n'est pas dans la bon sens")
            if coeffRightPrevious[0] != 0 and coeffRightOther[0] != 0:
                if ratio is not None and coeffRightPrevious[0] / coeffRightOther[0] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
                if ratio is None:
                    ratio = coeffRightPrevious[0] / coeffRightOther[0]
            elif (coeffRightPrevious[0] != 0 and coeffRightOther[0] == 0) or (coeffRightPrevious[0] == 0 and coeffRightOther[0] != 0):
                return (False, "Aide : le signe d'equivalence n'est pas dans la bon sens")
            if coeffRightPrevious[1] != 0 and coeffRightOther[1] != 0:
                if ratio is not None and coeffRightPrevious[1] / coeffRightOther[1] != ratio:
                    hint = "Aide : tu n'as pas applique la meme division sur chaque terme"
                    return (False, hint)
            else :
                return (False, "Aide : le signe d'equivalence n'est pas dans la bon sens")
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
        self.equa = sys
        self.sys = [eval(x,transformations=(st+(imp,))) for x in sys]
        self.var = symbols(var)
        self.solution = linsolve(self.sys, self.var)
        var = var.replace(" ","").replace(",","")
        self.variables = []
        i = 0
        while(i<len(var)):
            self.variables.append(var[i])
            i = i+1

    def isEquivalant(self, other):

        leftOther, rightOther, coeffLeftOther, coeffRightOther = other.analyse()
        leftPrevious, rightPrevious, coeffLeftPrevious, coeffRightPrevious = self.analyse()
        hint = None

        if (other.solution == self.solution):
            for k in range(len(self.sys)):
                if (not(str(leftOther[k]).lstrip("-").replace("/", "").isdigit()) and coeffLeftOther[k][0] == 0 and coeffLeftOther[k][1] == 0):
                    hint = "Aide : simplifie a gauche pour l'equation "+str(k+1)
                    return (True, hint)
                elif (not(str(rightOther[k]).lstrip("-").replace("/", "").isdigit()) and coeffRightOther[k][0] == 0 and coeffRightOther[k][1] == 0):
                    hint = "Aide : simplifie a droite pour l'equation "+str(k+1)
                    return (True, hint)
                elif ((coeffLeftOther[k][0] != 0 and coeffRightOther[k][0] != 0) or (coeffLeftOther[k][1] != 0 and coeffRightOther[k][1] != 0)):
                    hint = "Aide : isole la variable en applicant une operation de chaque cote pour l'equation "+str(k+1)
                    return (True, hint)
                elif (coeffLeftOther[k][2] != 0 and coeffRightOther[k][0] == 0 and coeffRightOther[k][1] == 0):
                    hint = "Aide : isole la variable(s) de gauche en applicant une operation de chaque cote pour l'equation "+str(k+1)
                    return (True, hint)
                elif (coeffRightOther[k][2] != 0 and coeffLeftOther[k][0] == 0 and coeffLeftOther[k][1] == 0):
                    hint = "Aide : isole la variable(s) de droite en applicant une operation de chaque cote pour l'equation "+str(k+1)
                    return (True, hint)
                elif ((coeffLeftOther[k][0] != 0 and coeffLeftOther[k][1] != 0) or (coeffRightOther[k][0] != 0 and coeffRightOther[k][1] != 0)):
                    hint = "Aide : isole les variables de chaque cote de l'equation "+str(k+1)
                    return (True,hint)
                elif ((coeffLeftOther[k][0] != 1 and coeffLeftOther[k][0] != 0 and coeffRightOther[k][0] == 0 and coeffRightOther[k][1] == 0 and coeffLeftOther[k][1] == 0)
                      or (coeffLeftOther[k][1] != 1 and coeffLeftOther[k][1] != 0 and coeffRightOther[k][1] == 0 and coeffRightOther[k][0] == 0 and coeffLeftOther[k][0] == 0)):
                    hint = "Aide : reduit le coefficent de la variable de gauche en applicant une operation de chaque cote pour l'equation "+str(k+1)
                    return (True, hint)
                elif ((coeffRightOther[k][0] != 1 and coeffRightOther[k][0] != 0 and coeffLeftOther[k][0] == 0 and coeffLeftOther[k][1] == 0 and coeffRightOther[k][1] == 0)
                      or (coeffRightOther[k][1] != 1 and coeffRightOther[k][1] != 0 and coeffLeftOther[k][1] == 0) and coeffLeftOther[k][0] == 0 and coeffRightOther[k][0] == 0):
                    hint = "Aide : reduit le coefficent de la variable de droite en applicant une operation de chaque cote pour l'equation "+str(k+1)
                    return (True, hint)
                elif ((coeffLeftOther[k][0] != 0 and coeffRightOther[k][1] != 0) or (coeffLeftOther[k][1] != 0 and coeffRightOther[k][0] != 0)):
                    hint = "Aide : remplace la variable d'une equation dans une autre equation"
            return (True, hint)
        else:
            for k in range(len(self.sys)):
                if (coeffLeftPrevious[k][0] == coeffLeftOther[k][0] and coeffLeftPrevious[k][1] == coeffLeftOther[k][1]
                    and coeffLeftOther[k][2] - coeffLeftPrevious[k][2] != coeffRightOther[k][2] - coeffRightPrevious[k][2]):
                    hint = 'Aide : tu as fait +(' + str(coeffLeftOther[k][2] - coeffLeftPrevious[k][2]) + ') a gauche et +(' \
                        + str(coeffRightOther[k][2] - coeffRightPrevious[k][2]) + ") a droite pour l'equation "+str(k+1)
                    return (False, hint)
                ratio = None
                if coeffLeftPrevious[k][0] != 0 and coeffLeftOther[k][0] != 0:
                    ratio = coeffLeftPrevious[k][0] / coeffLeftOther[k][0]
                if coeffLeftPrevious[k][1] != 0 and coeffLeftOther[k][1] != 0:
                    if ratio is not None and coeffLeftPrevious[k][1] / coeffLeftOther[k][1] != ratio:
                        hint = "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation "+str(k+1)
                        return (False, hint)
                    if ratio is None:
                        ratio = coeffLeftPrevious[k][1] / coeffLeftOther[k][1]
                if coeffLeftPrevious[k][2] != 0 and coeffLeftOther[k][2] != 0:
                    if ratio is not None and coeffLeftPrevious[k][2] / coeffLeftOther[k][2] != ratio:
                        hint = "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation "+str(k+1)
                        return (False, hint)
                    if ratio is None:
                        ratio = coeffLeftPrevious[k][2] / coeffLeftOther[k][2]

                if coeffRightPrevious[k][0] != 0 and coeffRightOther[k][0] != 0:
                    if ratio is not None and coeffRightPrevious[k][0] / coeffRightOther[k][0] != ratio:
                        hint = "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation "+str(k+1)
                        return (False, hint)
                    if ratio is None:
                        ratio = coeffRightPrevious[k][0] / coeffRightOther[k][0]
                if coeffRightPrevious[k][1] != 0 and coeffRightOther[k][1] != 0:
                    if ratio is not None and coeffRightPrevious[k][1] / coeffRightOther[k][1] != ratio:
                        hint = "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation "+str(k+1)
                        return (False, hint)
                if coeffRightPrevious[k][2] != 0 and coeffRightOther[k][2] != 0:
                    if ratio is not None and coeffRightPrevious[k][2] / coeffRightOther[k][2] != ratio:
                        hint = "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation "+str(k+1)
                        return (False, hint)

            return (False, hint)

    def isSolution(self, solution): #int solution
        if(len(solution) != len(list(self.solution)[0])):
            return False
        for s in list(self.solution)[0]:
            if(not(s in solution)):
                return False
        return True

    def analyse(self):
        left = ['']*len(self.sys)
        right = ['']*len(self.sys)
        left_crypt = [''] * len(self.sys)
        right_crypt = [''] * len(self.sys)
        coeffLeft = ['']*len(self.sys)
        coeffRight = ['']*len(self.sys)

        k = 0
        while (k<len(self.sys)):
            i = len(self.equa[k])-1
            parenthese = 0
            mid = 0
            while(i>0):
                if(self.equa[k][i] == ')'):
                    parenthese = parenthese + 1
                elif(self.equa[k][i] == '('):
                    parenthese = parenthese - 1
                elif(parenthese == 0):
                    mid = i
                    i = -1
                i = i-1

            i = 0
            while(i<mid):
                left[k] = left[k]+self.equa[k][i]
                i = i+1
            i = mid+2
            while(i<len(self.equa[k])-1):
                right[k] = right[k]+self.equa[k][i]
                i = i+1

            left_crypt = copy.copy(left)
            right_crypt = copy.copy(right)
            left_crypt[k] += '+5231598745' # parce que on veut un tableau [x y 1] et pas juste [x] ou ...
            right_crypt[k] += '+5231598745'
            for v in self.variables:
                left_crypt[k] += '+'+v+'*5231598745'
                right_crypt[k] += '+'+v+'*5231598745'

            coeffLeft[k] = eval(left_crypt[k],transformations=(st+(imp,)))
            coeffRight[k] = eval(right_crypt[k],transformations=(st+(imp,)))

            coeffLeft[k] = Poly(coeffLeft[k]).coeffs()
            coeffRight[k] = Poly(coeffRight[k]).coeffs()

            for i in range(0,len(coeffLeft[k])):
                coeffLeft[k][i] -= 5231598745
            for i in range(0, len(coeffRight[k])):
                coeffRight[k][i] -= 5231598745

            k = k+1

        return left, right, coeffLeft, coeffRight


class Expression:
    def __init__(self, equa):
        self.equa = equa
        self.solution = eval(equa,transformations=(st+(imp,)))

    def isEquivalant(self, other):
        hint = None

        if (self.solution == other.solution and str(other.equa).lstrip("-").replace("/","").isdigit()):
            return (True, hint)
        elif(self.solution == other.solution):
            hint = "Aide : continue!"
            return (True, hint)
        else:
            hint = "Aide : attention a la priorite des operations! D'abord les () puis x ou / et + ou -"
            return (False, hint)



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
#Inequation2 = Inequation('4*a>-1/4','a')
#print Inequation1.isSolution('a>1/16')
#print Inequation1.isEquivalant(Inequation2)


#tests System
#System1 = System(['5*x-(2+3*y)','2*x+y-(x)'], "x,y") # 2x=2 y+x=0
#print System1.isSolution([-1, 1]) # x=-1 y=1 ou l'inverse
#System2 = System(['x-(2/8)','-2/8-(y)'], "x,y") # x=1 x=-y
#print System1.isEquivalant(System2)


#tests Expression
#Expression1 = Expression('(3+5)*2')
#Expression2 = Expression('(8)*2')
#print Expression1.isEquivalant(Expression2)