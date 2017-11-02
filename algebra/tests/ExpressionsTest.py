#!/usr/bin/env python2

import os
import unittest2 as unittest
import json
from fractions import Fraction

from ..engine import Equation, Inequation, EquationSystem 

class ExpressionsTest(unittest.TestCase):
    """
    Main algebra engine tester. Test the 3 main algebra engine abilities
    """

    def setUp(self):
        pwd = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(os.path.join(pwd, "expressions.json"), "r") as equation_file:
                self.pool = json.loads(equation_file.read())
                self.pool = self.pool["expressions"]
        except IOError as e:
            raise IOError("Unable to open expression description file")    

# ===================================================================== GENERAL EXPRESSIONS CHECKS

    def test_expression_string_integrity(self):
        """
        TODO
        """
        for expression_def in self.pool:
            expression = globals()[expression_def["type"]](expression_def["string"])

            self.assertEqual(expression_def["string"], str(expression))

    def test_expression_components(self):
        """
        TODO
        """
        for expression_def in self.pool:
            expression = globals()[expression_def["type"]](expression_def["string"])
            self.assertEqual(expression._operator, expression_def["operator"])

    def expressions(self, type, degree, two_sided):
        """
        TODO
        """
        f = lambda x: x["type"] == type and x["degree"] == degree and x["two_sided"] == two_sided
        for z in filter(f, self.pool): yield z

    def format(self, thing):
        return ["%.4f" % float(Fraction(s).limit_denominator(4)) for s in thing]

# =============================================================================== EQUATIONS CHECKS

    #1
    def test_first_degree_one_sided_equation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Equation", 1, False):
            equation = Equation(expression["string"])
            self.assertEquals(
                self.format(equation.solution), 
                self.format(expression["solution"])
            )

    #2
    def test_first_degree_two_sided_equation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Equation", 1, True):
            equation = Equation(expression["string"])
            self.assertEquals(
                self.format(equation.solution),
                self.format(expression["solution"])
            )

    #3
    def test_second_degree_one_sided_equation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Equation", 2, False):
            equation = Equation(expression["string"])
            self.assertEquals(
                [self.format(s) for s in equation.solution],
                [self.format(s) for s in expression["solution"]]
            )

    #4
    def test_second_degree_two_sided_equation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Equation", 2, True):
            equation = Equation(expression["string"])
            self.assertEquals(
                [self.format(s) for s in equation.solution],
                [self.format(s) for s in expression["solution"]]
            )

    # TOTAL = 6

# ============================================================================= INEQUATIONS CHECKS

    #1
    def test_first_degree_one_sided_inequation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Inequation", 1, False):
            inequation = Inequation(expression["string"])
            self.assertEquals(inequation.solution, expression["solution"])

    #2
    def test_first_degree_two_sided_inequation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Inequation", 1, True):
            inequation = Inequation(expression["string"])
            self.assertEquals(inequation.solution, expression["solution"])

    #3
    def test_second_degree_one_sided_inequation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Inequation", 2, False):
            inequation = Inequation(expression["string"])
            self.assertEquals(inequation.solution, expression["solution"])

    #4
    def test_second_degree_two_sided_inequation_solution(self):
        """
        TODO
        """
        for expression in self.expressions("Inequation", 2, True):
            inequation = Inequation(expression["string"])
            self.assertEquals(inequation.solution, expression["solution"])
    
    # TOTAL = 6 + 4

# ======================================================================== EQUATION SYSTEMS CHECKS

    #1
    def test_first_degree_one_sided_equation_system_solution(self):
        """
        TODO
        """
        for expression in self.expressions("EquationSystem", 1, False):
            equation_system = EquationSystem(expression["string"])
            self.assertEqual(equation_system.solution, expression["solution"])
    
    #2
    def test_first_degree_two_sided_equation_system_solution(self):
        """
        TODO
        """
        for expression in self.expressions("EquationSystem", 1, True):
            equation_system = EquationSystem(expression["string"])
            self.assertEqual(equation_system.solution, expression["solution"])

    #3
    def test_second_degree_one_sided_equation_system_solution(self):
        """
        TODO
        """
        for expression in self.expressions("EquationSystem", 2, False):
            equation_system = EquationSystem(expression["string"])
            self.assertEqual(equation_system.solution, expression["solution"])

    #4
    def test_second_degree_two_sided_equation_system_solution(self):
        """
        TODO
        """
        for expression in self.expressions("EquationSystem", 2, True):
            equation_system = EquationSystem(expression["string"])
            self.assertEqual(equation_system.solution, expression["solution"])

    # TOTAL = 6 + 4 + 4

if __name__ == "__main__":

    unittest.main()
