import unittest
from Factory import *
from InputHandler import *


class TestEquation(unittest.TestCase):
    def test_isEquivalent(self):
        equation1 = Equation("x-(2-2*x)",'x')
        equation2 = Equation("3*x-(2)",'x')
        equation3 = Equation("4*x-(2)",'x')
        equation4 = Equation("x-(2/3)",'x')
        equation5 = Equation("x-(1/3)",'x')
        self.assertTrue(equation1.isEquivalant(equation2)[0])
        self.assertFalse(equation1.isEquivalant(equation3)[0])
        equiv1 = equation1.isEquivalant(equation4)
        self.assertTrue(equiv1[0] and equiv1[1] == None)
        equiv2 = equation1.isEquivalant(equation5)
        self.assertTrue(not(equiv2[0]) and equiv2[1] != None)

    def test_true_hint(self):
        equation1 = Equation("x+2-(2+3)", 'x')
        self.assertTrue(equation1.isEquivalant(equation1)[1] == "Aide : simplifie a droite")
        equation2 = Equation("5+8*2/3-(2*x)", 'x')
        self.assertTrue(equation2.isEquivalant(equation2)[1] == "Aide : simplifie a gauche")
        equation3 = Equation("2*x-(3*x+5)",'x')
        self.assertTrue(equation3.isEquivalant(equation3)[1] == 'Aide : isole la variable en applicant une operation de chaque cote')
        equation4 = Equation("2*y-(3*y+5)",'y')
        self.assertTrue(equation4.isEquivalant(equation4)[1] == 'Aide : isole la variable en applicant une operation de chaque cote')
        equation5 = Equation("2*x+5-(3)",'x')
        self.assertTrue(equation5.isEquivalant(equation5)[1] == 'Aide : isole la variable de gauche en applicant une operation de chaque cote')
        equation6 = Equation("2-(x+3)",'x')
        self.assertTrue(equation6.isEquivalant(equation6)[1] == 'Aide : isole la variable de droite en applicant une operation de chaque cote')
        equation7 = Equation("2*x-(4)",'x')
        self.assertTrue(equation7.isEquivalant(equation7)[1] == 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote')
        equation8 = Equation("5-(1/2*y)",'y')
        self.assertTrue(equation8.isEquivalant(equation8)[1] == 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote')

    def test_false_hint(self):
        equation1 = Equation("2*x+5-((2+3)*2)",'x')
        equation2 = Equation("2*x-(10)",'x')
        self.assertTrue(equation1.isEquivalant(equation2)[1] == 'Aide : tu as fait +(-5) a gauche et +(0) a droite')
        equation3 = Equation("2*x+2-(13)",'x')
        self.assertTrue(equation1.isEquivalant(equation3)[1] == 'Aide : tu as fait +(-3) a gauche et +(3) a droite')
        equation4 = Equation("x+5/2-((2+3)*2)",'x')
        self.assertTrue(equation1.isEquivalant(equation4)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme")
        equation5 = Equation("x/2+5/4-((2+3))",'x')
        self.assertTrue(equation1.isEquivalant(equation5)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme")




class TestInequation(unittest.TestCase):
    def test_isEquivalent(self):
        inequation1 = Inequation("2*x+2>=6",'x')
        inequation2 = Inequation("2*x>=4",'x')
        equiv1 = inequation1.isEquivalant(inequation2)
        self.assertTrue(equiv1[0] and equiv1[1] is not None)
        inequation3 = Inequation("2*x>=3",'x')
        equiv2 = inequation1.isEquivalant(inequation3)
        self.assertFalse(equiv2[0])
        inequation4 = Inequation("2<=x",'x')
        equiv3 = inequation1.isEquivalant(inequation4)
        self.assertTrue(equiv3[0] and equiv3[1] is None)

    def test_true_hint(self):
        inequation1 = Inequation("x+2>2+3", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation1)[1] == "Aide : simplifie a droite")
        inequation2 = Inequation("5+8*2/3<2*x", 'x')
        self.assertTrue(inequation2.isEquivalant(inequation2)[1] == "Aide : simplifie a gauche")
        inequation3 = Inequation("2*x>3*x+5", 'x')
        self.assertTrue(inequation3.isEquivalant(inequation3)[1] == 'Aide : isole la variable en applicant une operation de chaque cote')
        inequation4 = Inequation("2*y<=3*y+5", 'y')
        self.assertTrue(inequation4.isEquivalant(inequation4)[1] == 'Aide : isole la variable en applicant une operation de chaque cote')
        inequation5 = Inequation("2*x+5>=3", 'x')
        self.assertTrue(inequation5.isEquivalant(inequation5)[1] == 'Aide : isole la variable de gauche en applicant une operation de chaque cote')
        inequation6 = Inequation("2<x+3", 'x')
        self.assertTrue(inequation6.isEquivalant(inequation6)[1] == 'Aide : isole la variable de droite en applicant une operation de chaque cote')
        inequation7 = Inequation("2*x>=4", 'x')
        self.assertTrue(inequation7.isEquivalant(inequation7)[1] == 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote')
        inequation8 = Inequation("5<1/2*y", 'y')
        self.assertTrue(inequation8.isEquivalant(inequation8)[1] == 'Aide : reduit le coefficent de la variable en applicant une operation de chaque cote')

    def test_false_hint(self):
        inequation1 = Inequation("2*x+5>(2+3)*2", 'x')
        inequation2 = Inequation("2*x>10", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation2)[1] == 'Aide : tu as fait +(-5) a gauche et +(0) a droite')
        inequation3 = Inequation("2*x+2>13", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation3)[1] == 'Aide : tu as fait +(-3) a gauche et +(3) a droite')
        inequation4 = Inequation("x+5/2>(2+3)*2", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation4)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme")
        inequation5 = Inequation("x/2+5/4>(2+3)", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation5)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme")
        inequation6 = Inequation("2*x<5", 'x')
        self.assertTrue(inequation1.isEquivalant(inequation6)[1] == "Aide : le signe d'equivalence n'est pas dans la bon sens")



class TestSystem(unittest.TestCase):
    def test_isEquivalent(self):
        sys1 = System(["x-(2*y+5)", "y+x-(2)"], 'x,y')
        sys2 = System(["x-5-(2*y)", "y-(2-x)"], 'x,y')
        sys3 = System(["x-4-(2*y)", "y-(2-x)"], 'x,y')
        sys4 = System(["x-(3)", "-1-(y)"], 'x,y')
        equiv1 = sys1.isEquivalant(sys2)
        self.assertTrue(equiv1[0] and equiv1[1] is not None)
        equiv2 = sys1.isEquivalant(sys3)
        self.assertTrue(not(equiv2[0]) and equiv2[1] is not None)
        equiv3 = sys1.isEquivalant(sys4)
        self.assertTrue(equiv3[0] and equiv3[1] == None)

    def test_true_hint(self):
        sys1 = System(["x-(2)", "y-(2+3)"], 'x,y')
        self.assertTrue(sys1.isEquivalant(sys1)[1] == "Aide : simplifie a droite pour l'equation 2")
        sys2 = System(["2+3-(x)", "y-(2)"], 'x,y')
        self.assertTrue(sys2.isEquivalant(sys2)[1] == "Aide : simplifie a gauche pour l'equation 1")
        sys3 = System(["x+2-(2*x)", "y-(2)"], 'x,y')
        self.assertTrue(sys3.isEquivalant(sys3)[1] == "Aide : isole la variable en applicant une operation de chaque cote pour l'equation 1")
        sys4 = System(["x-(2)", "y+x+3-(2)"], 'x,y')
        self.assertTrue(sys4.isEquivalant(sys4)[1] == "Aide : isole la variable(s) de gauche en applicant une operation de chaque cote pour l'equation 2")
        sys5 = System(["1-(x+3)", "y+x+3-(2)"], 'x,y')
        self.assertTrue(sys5.isEquivalant(sys5)[1] == "Aide : isole la variable(s) de droite en applicant une operation de chaque cote pour l'equation 1")
        sys6 = System(["1-(x+y)", "y+x+3-(2)"], 'x,y')
        self.assertTrue(sys6.isEquivalant(sys6)[1] == "Aide : isole les variables de chaque cote de l'equation 1")
        sys7 = System(["x-(2)", "2-(2*y)"], 'x,y')
        self.assertTrue(sys7.isEquivalant(sys7)[1] == "Aide : reduit le coefficent de la variable de droite en applicant une operation de chaque cote pour l'equation 2")
        sys8 = System(["x-(2)", "x-(y)"], 'x,y')
        self.assertTrue(sys8.isEquivalant(sys8)[1] == "Aide : remplace la variable d'une equation dans une autre equation")

    def test_false_hint(self):
        sys1 = System(["x-(2*y+5)", "y+x-(2)"], 'x,y')
        sys2 = System(["x-5-(2*y+5)", "y+x-(2)"], 'x,y')
        self.assertTrue(sys1.isEquivalant(sys2)[1] == "Aide : tu as fait +(-5) a gauche et +(0) a droite pour l'equation 1")
        sys3 = System(["x-(2*y+5)", "y+x-3-(5)"], 'x,y')
        self.assertTrue(sys1.isEquivalant(sys3)[1] == "Aide : tu as fait +(-3) a gauche et +(3) a droite pour l'equation 2")
        sys4 = System(["x/2-(y+5)", "y+x-(2)"], 'x,y')
        self.assertTrue(sys1.isEquivalant(sys4)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation 1")
        sys5 = System(["x-(2*y+5)", "y/2+x-(1)"], 'x,y')
        self.assertTrue(sys1.isEquivalant(sys5)[1] == "Aide : tu n'as pas applique la meme division sur chaque terme pour l'equation 2")

class TestExpression(unittest.TestCase):
    def test_isEquivalent(self):
        exp1 = Expression("(3+10)/2*2**2")
        exp2 = Expression("13/2*2**2")
        exp3 = Expression("52/2")
        exp4 = Expression("1")
        equiv1 = exp1.isEquivalant(exp2)
        equiv2 = exp1.isEquivalant(exp3)
        equiv3 = exp1.isEquivalant(exp4)
        self.assertTrue(equiv1[0] and equiv1[1] is not None)
        self.assertTrue(equiv2[0] and equiv2[1] is None)
        self.assertFalse(equiv3[0])

class TestInputHandler(unittest.TestCase):
    def test_parse(self):
        handler1 = InputHandler("algebraicEquation")
        self.assertTrue(handler1.parse(u'2x+3=5')==(u'2x+3-(5)', u'x'))
        handler2 = InputHandler("algebraicInequation")
        self.assertTrue(handler2.parse(u'2*x<6')==(u'2*x<6', u'x'))
        handler3 = InputHandler("algebraicSystem")
        self.assertTrue(handler3.parse((u'2x+y=5',u'3y=8^2'))==([u'2x+y-(5)', u'3y-(8**2)'], u'x,y'))

class TestMakeEquation(unittest.TestCase):
    def test_make(self):
        handler = InputHandler("algebraicEquation")
        for _ in range(10):
            equa = makeEquation(varRight=False, varLeft=True, minValueVar=-10, maxValueVar=10, minValueSol=0, maxValueSol=5,nameVar='s', division=True, isSolInt=True)
            equationTest = Equation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            self.assertTrue(len(equationTest.solution) == 1)
            self.assertTrue(equationTest.solution[0] >= 0)
            self.assertTrue(equationTest.solution[0] <= 5)
            self.assertTrue(str(equationTest.solution[0]).lstrip("-").isdigit()) #isSolInt
            left, right, coeffLeft, coeffRight = equationTest.analyse()
            self.assertTrue(coeffLeft[0] <= 10 and coeffLeft[0] >= -10 and coeffLeft[1] != 0)
            self.assertTrue(coeffLeft[1] <= 10 and coeffLeft[1] >= -10 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[0] == 0)
            self.assertTrue(coeffRight[1] <= 10 and coeffRight[1] >= -10 and coeffRight[1] != 0)
        for _ in range(10):
            equa = makeEquation(varRight=True, varLeft=True, minValueVar=-4, maxValueVar=3, minValueSol=-9, maxValueSol=8,nameVar='s', division=True, isSolInt=True)
            equationTest = Equation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            self.assertTrue(len(equationTest.solution) == 1)
            self.assertTrue(equationTest.solution[0] >= -9)
            self.assertTrue(equationTest.solution[0] <= 8)
            self.assertTrue(str(equationTest.solution[0]).lstrip("-").isdigit()) #isSolInt
            left, right, coeffLeft, coeffRight = equationTest.analyse()
            self.assertTrue(coeffLeft[0] <= 3 and coeffLeft[0] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffLeft[1] <= 3 and coeffLeft[1] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
        for _ in range(10):
            equa = makeEquation(varRight=True, varLeft=False, minValueVar=-4, maxValueVar=3, minValueSol=-9, maxValueSol=8,nameVar='s', division=True, isSolInt=True)
            equationTest = Equation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            self.assertTrue(len(equationTest.solution) == 1)
            self.assertTrue(equationTest.solution[0] >= -9)
            self.assertTrue(equationTest.solution[0] <= 8)
            self.assertTrue(str(equationTest.solution[0]).lstrip("-").isdigit()) #isSolInt
            left, right, coeffLeft, coeffRight = equationTest.analyse()
            self.assertTrue(coeffLeft[0] == 0)
            self.assertTrue(coeffLeft[1] <= 3 and coeffLeft[1] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)


class TestMakeInequation(unittest.TestCase):
    def test_make(self):
        handler = InputHandler("algebraicInequation")
        for _ in range(10):
            equa = makeInequation(varRight=False, varLeft=True, minValueVar=0, maxValueVar=5, minValueSol=-10, maxValueSol=10, nameVar='s', division=False, isSolInt=True, signeEquation=None)
            equationTest = Inequation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            solution = getSolutionFromAND(str(equationTest.solution))
            self.assertTrue(equationTest.solution != False and equationTest.solution != True)
            self.assertTrue(eval(solution) >= -10 and eval(solution) <= 10)
            self.assertTrue(solution.lstrip("-").isdigit())
            left, right, coeffLeft, coeffRight,condition = equationTest.analyse()
            self.assertTrue(coeffLeft[0] <= 10 and coeffLeft[0] >= -10 and coeffLeft[1] != 0)
            self.assertTrue(coeffLeft[1] <= 10 and coeffLeft[1] >= -10 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[0] == 0)
            self.assertTrue(coeffRight[1] <= 10 and coeffRight[1] >= -10 and coeffRight[1] != 0)
        for _ in range(10):
            equa = makeInequation(varRight=True, varLeft=True, minValueVar=-4, maxValueVar=3, minValueSol=-9, maxValueSol=8,nameVar='s', division=True, isSolInt=True, signeEquation='>=')
            equationTest = Inequation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            solution = getSolutionFromAND(str(equationTest.solution))
            self.assertTrue(equationTest.solution != False and equationTest.solution != True)
            self.assertTrue(eval(solution) >= -9 and eval(solution) <= 8)
            self.assertTrue(solution.lstrip("-").isdigit())
            left, right, coeffLeft, coeffRight, condition = equationTest.analyse()
            self.assertTrue(condition == '>=')
            self.assertTrue(coeffLeft[0] <= 3 and coeffLeft[0] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffLeft[1] <= 3 and coeffLeft[1] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
        for _ in range(10):
            equa = makeInequation(varRight=True, varLeft=False, minValueVar=-4, maxValueVar=3, minValueSol=-9, maxValueSol=8,nameVar='s', division=True, isSolInt=True, signeEquation=None)
            equationTest = Inequation(handler.parse(unicode(equa, "utf-8"))[0], 's')
            solution = getSolutionFromAND(str(equationTest.solution))
            self.assertTrue(equationTest.solution != False and equationTest.solution != True)
            self.assertTrue(eval(solution) >= -9 and eval(solution) <= 8)
            self.assertTrue(solution.lstrip("-").isdigit())
            left, right, coeffLeft, coeffRight, condition = equationTest.analyse()
            self.assertTrue(coeffLeft[0] == 0)
            self.assertTrue(coeffLeft[1] <= 3 and coeffLeft[1] >= -4 and coeffLeft[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)
            self.assertTrue(coeffRight[1] <= 3 and coeffRight[1] >= -4 and coeffRight[1] != 0)

class TestMakeSys(unittest.TestCase):
    def test_make(self):
        handler = InputHandler("algebraicSystem")
        for _ in range(5):
            (equation1,equation2) = makeSys(var1Right1=True, var1Left1=False, var2Right1=False, var2Left1=True, var1Right2=False, var1Left2=True, var2Right2=True, var2Left2=True, minValueVar=-10, maxValueVar=10, minValueSol=-10, maxValueSol=10, nameVar1='y', nameVar2='x', division=True, isSolInt=True)
            systemTest = System(handler.parse((unicode(equation1, "utf-8"),(unicode(equation2, "utf-8"))))[0], "y,x")
            self.assertTrue(len(list(systemTest.solution)) != 0)
            self.assertTrue(list(systemTest.solution)[0][0] >= -10 and list(systemTest.solution)[0][0] <= 10
                            and list(systemTest.solution)[0][1] >= -10 and list(systemTest.solution)[0][1] <= 10)
            self.assertTrue(str(list(systemTest.solution)[0][0]).lstrip("-").isdigit() and str(list(systemTest.solution)[0][1]).lstrip("-").isdigit())
            left, right, coeffLeft, coeffRight = systemTest.analyse()
            self.assertTrue(coeffLeft[0][1] == 0)
            self.assertTrue(coeffRight[1][1] == 0)
            self.assertTrue(coeffRight[0][0] == 0)
            self.assertTrue(coeffRight[0][1] <= 10 and coeffRight[0][1] >= -10 and coeffRight[0][1] != 0)
            self.assertTrue(coeffLeft[0][0] <= 10 and coeffLeft[0][0] >= -10 and coeffLeft[0][0] != 0)
            self.assertTrue(coeffLeft[1][1] <= 10 and coeffLeft[1][1] >= -10 and coeffLeft[1][1] != 0)
            self.assertTrue(coeffRight[1][0] <= 10 and coeffRight[1][0] >= -10 and coeffRight[1][0] != 0)
            self.assertTrue(coeffLeft[1][0] <= 10 and coeffLeft[1][0] >= -10 and coeffLeft[1][0] != 0)


class TestMakeExpression(unittest.TestCase):
    def test_make(self):
        handler = InputHandler("algebraicExpression")
        for _ in range(5):
            expression = makeExpression(nbrTerm=4, maxValue=10, minSol=0, maxSol=100, multiplication=True, exponent=False, division=False, parenthesis=True, isSolInt=True)
            handler.parse(unicode(expression, "utf-8"))
            self.assertTrue(str(eval(expression)).lstrip('-').isdigit())
            self.assertTrue(eval(expression)<=100 and eval(expression)>=0)



if __name__ == '__main__':
    unittest.main()