import unittest
from Factory import *


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

if __name__ == '__main__':
    unittest.main()