# -*- coding: utf-8 -*-

import sys
import re as reg
from sympy import symbols, sympify, solveset, degree, solve_poly_inequality, Poly
from abc import ABCMeta


class ExpressionError(Exception):
    pass


# ============================================================================
# ================================ Expression ================================
# ============================================================================

class Expression(object):
    """
    General class defining an arithmetique expression
    An Expression object can be created with the args :
        - expr (the expression in a String),
        - sym (the variable of  the expression, the default value is x)
    """

    __metaclass__ = ABCMeta

    # ---------------------------------------------------------- Magic methods

    def __init__(self, expression, operator=None):
        self._expression_string = expression
        self._symbols = [symbols(sym) for sym in self._symbols_of(expression)]

        lo, self._operator, ro = self._split(expression, operator)
        lo = self._sanitize(lo)
        ro = self._sanitize(ro)
        try:
            self._left_operand = sympify(lo)
            self._right_operand = sympify(ro)
        except Exception as e:
            raise ExpressionError('Invalid expression syntax, expression: ' +
                                  expression + "\nLeft operand: " + lo +
                                  "\nRIght operand: " + ro)
            print(lo)
            print(ro)

        lod = degree(self._left_operand)  if self._has_symbol(lo) else 0
        rod = degree(self._right_operand) if self._has_symbol(ro) else 0
        self._degree = lod if lod > rod else rod

        self._solution = self.resolve()

    def __str__(self):
        return self._expression_string

    def __eq__(self, other):
        return self._solution == other._solution

    # --------------------------------------------------------- Static methods

    @staticmethod
    def _symbols_of(expression):
        symbol = reg.compile('[a-zA-Z]')
        return set([c.group() for c in symbol.finditer(expression)])

    @staticmethod
    def _sanitize(expression):
        e = expression.replace(' ', '')

        sym = reg.compile('[a-zA-Z(]')
        op = reg.compile('[-+*^/%=)(]') # add operators here
        targets = []

        start = lambda r: r.start() == 0
        end = lambda r, expr: r.start() == len(expr) -1

        for c in sym.finditer(e):
            if (start(c) or op.match(e[c.start() - 1])) \
            and (end(c, e) or op.match(e[c.start() + 1])):
                continue
            
            if not start(c) and not op.match(e[c.start() - 1]):
                targets.append(c.start() - 1)
            
            if not end(c, e) and not op.match(e[c.start() + 1]):
                if not c.group() == "(":
                    targets.append(c.start() + 1)

        for i, target in enumerate(targets):
            e = e[0:target + 1] + '*' + e[target + 1:len(e)]
            targets[i+1:] = map(lambda x: x + 1, targets[i+1:])

        return e

    @staticmethod
    def _has_symbol(expression):
        s = reg.compile('[a-zA-Z]')
        return s.search(expression) != None

    @staticmethod
    def _pretty(expression):
        expr = expression.replace('*', '')
        operator = reg.compile('[+*^/%=-]')

        chars = set([(op.start(), op.group()) for op in operator.finditer(expr)])
        for c in chars:
            replacement = ''
            if expr[c[0] - 1] != ' ' and c[0] != 0:
                replacement += ' '
            replacement += c[1]
            if expr[c[0] + 1] != ' ' and c[0] != len(expr) - 1:
                replacement += ' '

            expr = expr.replace(c[1], replacement)

        return expr

    @staticmethod
    def _split(expression, operator=None):
        operator = '(<=)|(=<)|(>=)|(=>)|=|<|>' if operator is None else operator
        op_reg = reg.compile(operator)

        op = op_reg.search(expression)
        if not op:
            raise ExpressionError("Unable to split expression: " + expression)
        left, right = expression.split(op.group())

        return left, op.group(), right

    # --------------------------------------------------------- Actual methods

    def resolve(self):
        raise NotImplementedError("Call to abstract method")

    # ------------------------------------------------------------- Properties

    @property
    def solution(self):
        return self._solution

    @property
    def operator(self):
        return self._operator

    @property
    def degree(self):
        return int(self._degree)

# ============================================================================
# ================================  Equation =================================
# ============================================================================


class Equation(Expression):
    """
    Class for the expressions of the category Equation
    An Equation object can be created with the args :
        - expr (the equation in a String),
        - sym (the variable of  the equation, the default value is x)
    """

    def __init__(self, expression):
        Expression.__init__(self, expression, '=')

    def resolve(self):
        """return value of the solution of the equation in a String"""
        solutions = []
        for symbol in self._symbols:
            expr = self._left_operand - self._right_operand
            solutions.append(str(solveset(expr, symbol)).strip("{").strip("}"))

        return solutions

    def is_equation(self):
        """return true if this is a correct inequation"""
        return self._operator == '='


# ============================================================================
# ================================ Inequation ================================
# ============================================================================


class Inequation(Expression):
    """Class for the expressions of the category Inequation
    An Inequation object can be created with the args : 
        - expr (the inequation in a String), 
        - sym (the variable of  the inequation, the default value is x)"""

    
    def resolve(self):
        """ return value of the solution of the inequation in a String"""
        results = []
        expr = self._left_operand - self._right_operand

        for sym in self._symbols:
            result = solve_poly_inequality(Poly(expr, sym), self._operator)

            results.append(result)

        return results

    def is_inequation(self):
        """return true if this is a correct inequation"""
        return self.operator in ('<','>','<=','>=') and verifEncode(self.leftOperand) and verifEncode(self.rightOperand)


#---------------------------------------------
#--- Equation System
#---------------------------------------------
    
class EquationSystem(Expression):
    """Class for the expressions of the category System of two Equations
    An EquationSystem object can be created with the args : 
        - expr (An array of two Strings with the equations), 
        - sym (the variables of  the expression, the default values are x and y)"""

    def __init__(self, expr, sym = 'x y'):
        self.equation1 = Equation(expr[0])
        self.equation2 = Equation(expr[1])
        self.x, self.y = symbols(sym)
        self._solution = self.resolve

    # TO DO
    def resolve(self):
        pass




#---------------------------------------------
#--- complementary functions
#---------------------------------------------


# compare un systeme de deux equation et dit si elle sont egales
def compare_expr(expressionLeft, expressionRight):
    x, y, z = symbols("x y z")
    str_Left = expressionLeft
    str_Right = expressionRight
    exprLeft = sympify(str_Left)
    exprRight = sympify(str_Right)
    return str(solveset(Eq(exprLeft, exprRight)))


def simplification_oneSide_equation(expression):
    x, y, z = symbols("x y z")
    str_expr = expression
    expr = sympify(str_expr)
    return str(simplify(expr))