# -*- coding: utf-8 -*-

import random
import re as reg

from datetime import datetime
from abc import ABCMeta

from sympy import symbols, sympify, degree, S
from algebra.models import AlgebraicExercice

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
    __children__ = set()

    class Solution(object):
        pass

    # ---------------------------------------------------------- Magic methods

    def __init__(self, expression, operator=None, domain=S.Reals):
        self._symbols = [symbols(sym) for sym in self._symbols_of(expression)]
        self._domain = domain

        lo, self._operator, ro = self._split(expression, operator)
        lo = self._sanitize(lo)
        ro = self._sanitize(ro)
        try:
            locals = {}
            for sym in self._symbols: locals[str(sym)] = sym
            self._left_operand = sympify(lo, locals=locals)
            self._right_operand = sympify(ro, locals=locals)
        except Exception as e:
            raise ExpressionError('Invalid expression syntax, expression: ' +
                                  expression + "\nLeft operand: " + lo +
                                  "\nRIght operand: " + ro)

        lod = degree(self._left_operand)  if self._has_symbol(lo) else 0
        rod = degree(self._right_operand) if self._has_symbol(ro) else 0
        self._degree = lod if lod > rod else rod

        self._solution = self.resolve()

    def __str__(self):
        return self._pretty(
            str(self._left_operand).strip(' ') + ' ' +
            self._operator + ' ' +
            str(self._right_operand).strip(' ')
        )

    def __eq__(self, other):
        return self._solution == other._solution

    # --------------------------------------------------------- Static methods

    @staticmethod
    def register(cls):
        Expression.__children__.add(cls)

    @staticmethod
    def generate(two_sided, degree):
        r = random.randint(0, len(Expression.children))
        return Expression.children[r].generate()        

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
        expr = expression.replace('**', '^')
        expr = expr.replace('*', '')
        operator = reg.compile('[+*/%=1-9-]')

        chars = set([(op.start(), op.group()) for op in operator.finditer(expr)])
        for c in chars:
            replacement = c[1]
            if c[0] != len(expr) - 1 and expr[c[0] + 1] != ' ':
                replacement += ' '

            expr = expr.replace(c[1], replacement)

        return expr.strip(' ')

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

    @property
    def symbols(self):
        return self._symbols

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, dom):
        self._domain = dom

    @property
    def model(self):
        created = datetime.now()
        return AlgebraicExercice(
            expression=str(self),
            expression_type=self._db_type,
            created=created,
            updated=created,
            solution=str(self.solution),
            level=-1
        )

# ============================================================================
