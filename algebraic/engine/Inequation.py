from . import Expression

from sympy import Poly, solve_poly_inequality

# ============================================================================
# ================================ Inequation ================================
# ============================================================================

class Inequation(Expression):
    """Class for the expressions of the category Inequation
    An Inequation object can be created with the args : 
        - expr (the inequation in a String), 
        - sym (the variable of  the inequation, the default value is x)"""

    # --------------------------------------------------------- Static methods

    @staticmethod
    def generate(two_sided, degree):
        raise NotImplementedError()

    # --------------------------------------------------------- Actual methods

    def resolve(self):
        """ return value of the solution of the inequation in a String"""
        results = []
        for sym in self._symbols:
            a = Poly(self._left_operand, sym)
            b = Poly(self._right_operand, sym)
            expr = a - b
            result = solve_poly_inequality(expr, self._operator)

            results.append(result)

        return results

# ============================================================================

Expression.register(Inequation)
