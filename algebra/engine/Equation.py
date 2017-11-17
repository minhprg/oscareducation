"""TODO"""

from sympy import solveset
from . import Expression

# ============================================================================
# ================================  Equation =================================
# ============================================================================

@Expression.register
class Equation(Expression):
    """
    Simplest expression available. Solves equation(s) of any degree.

    :see: Expression
    """

    _db_type = "EQ"

    # ---------------------------------------------------------- Magic methods

    def __init__(self, expression):
        Expression.__init__(self, expression, '=')

    # --------------------------------------------------------- Static methods

    @staticmethod
    def generate(two_sided, degree):
        raise NotImplementedError()

    # --------------------------------------------------------- Actual methods

    def resolve(self):
        solutions = []
        for symbol in self._symbols:
            expr = self._left_operand - self._right_operand
            solutions.append(list(solveset(expr, symbol, self._domain)))
        print(solutions)
        return solutions

# ============================================================================
