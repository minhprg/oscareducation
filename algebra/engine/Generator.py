from fractions import Fraction
from random import choice
import re as reg

from sympy import S, sympify, expand

class GeneratorError(Exception):
    pass


class Generator(object):

    _operators = ['-', '+', '*', '/']

    def __init__(self):
        raise GeneratorError("Cannot instanciate Generator object")

    @staticmethod
    def generate(e_degree=2, e_range=20, domain=S.Reals):
        from algebra.engine import Expression
        expression = ""
        for solution in Generator.solution(e_degree, e_range):
            expression += "(x+" + str(-solution) + ")*"
        expression = expression[0:-1]
        sexpr = expand(sympify(expression))
        return Expression.pretty(str(sexpr))

    @staticmethod
    def complexify(expression, e_range):

        comparison = reg.compile('(<=)|(=<)|(>=)|(=>)|=|<|>')
        comparison_match = comparison.search(expression)
        comparison_op = lo = ro = ""

        if comparison_match is None:
            lo = expression
            comparison_op = "="
            ro = "0"
        else:
            comparison_op = comparison_match.group()
            lo, ro = expression.split(comparison_op)

        modification = choice(Generator._operators)
        modification_n = choice(range(-e_range, e_range))
        lo = "(" + lo + ")" + modification + str(modification_n)
        ro = "(" + ro + ")" + modification + str(modification_n)

        return lo + comparison_op + ro

    @staticmethod
    def solution(e_degree, e_range, fraction=False):
        solutions = []

        for i in range(0, e_degree):
            solutions.append(choice(range(-e_range, e_range)))

        return tuple(solutions)
