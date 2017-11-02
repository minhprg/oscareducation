from . import Expression

from sympy import solveset

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
        """return value of the solution of the equation in a String"""
        solutions = []
        for symbol in self._symbols:
            expr = self._left_operand - self._right_operand
            solutions.append(list(solveset(expr, symbol, self._domain)))

        return solutions

# ============================================================================

Expression.register(Equation)
