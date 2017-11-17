from . import Expression

from sympy import Poly, solve_poly_inequality

# ============================================================================
# ================================ Inequation ================================
# ============================================================================

@Expression.register
class Inequation(Expression):
    """
    Inequation representation, solves any kind of inequality. Tested for the
    first and second degree.

    :warning: The inequation does not handle unknown-composed denominator as
    of 7 nov. 2017. A fix to the problem is currently being searched.
    """

    _db_type = "IN"

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
