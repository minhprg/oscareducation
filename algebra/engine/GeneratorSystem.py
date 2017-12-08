from fractions import Fraction
from random import random,choice

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.str import StrPrinter

from Expression import Expression

class GeneratorError(Exception):
    pass


class GeneratorSystem(object):

    _operators = ['-', '+', '*', '/']

    @staticmethod
    def generateSystem(degree=1, ranges=20, domain=S.Reals):
        param = []
        for i in range(0, 6):
            n = choice(range(-ranges, ranges))
            if n >= 0 : param.append("+"+ str(n))
            else : param.append(str(n))
        return [param[0] + "*x" + param[1] + "*y=" + param[2],
                param[3] + "*x" + param[4] + "*y=" + param[5]]



