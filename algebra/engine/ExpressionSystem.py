"""TODO"""

from collections import Sequence
from abc import ABCMeta
from sympy import S, symbols, sympify, degree
from . import Expression, ExpressionError

# ============================================================================
# ============================ Expression System =============================
# ============================================================================

class ExpressionSystem(Expression):
    """TODO"""

    __metaclass__ = ABCMeta

    def __init__(self, expressions, operators=None, domain=S.Reals):
        if isinstance(expressions, basestring):
            raise ExpressionError("A sequence is needed for equation systems")
        elif not isinstance(expressions, Sequence):
            raise ExpressionError("A sequence is needed for equation systems")

        self._symbols = []
        self._operators = []
        self._left_operands = []
        self._right_operands = []
        self._domain = domain

        for i, expression in enumerate(expressions):

            self._symbols.extend(
                [symbols(sym) for sym in self._symbols_of(expression)]
            )

            lo, op, ro = self._split(expression)
            self._operators.extend(op)

            lo = self._sanitize(lo)
            ro = self._sanitize(ro)

            try:

                lcs = {}
                for sym in self._symbols: lcs[str(sym)] = sym
                self._left_operands.append(sympify(lo, locals=lcs))
                self._right_operands.append(sympify(ro, locals=lcs))

            except Exception as e:

                raise ExpressionError(
                    'Invalid expression syntax, expression: ' +
                    expression + "\nLeft operand: " + lo +
                    '\nRIght operand: ' + ro
                )

            lod = degree(self._left_operands[i])  if self._has_symbol(lo) else 0
            rod = degree(self._right_operands[i]) if self._has_symbol(ro) else 0
            self._degree = lod if lod > rod else rod

        self._symbols = set(self._symbols)
        self._solution = self.resolve()

    def resolve(self):
        raise NotImplementedError("Call to abstract method")

# ============================================================================
