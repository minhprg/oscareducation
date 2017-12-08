"""TODO"""

from sympy import solve_poly_system, Poly

from . import Expression, ExpressionError, ExpressionSystem

# ============================================================================
# ============================= Equation System ==============================
# ============================================================================

@Expression.register
class EquationSystem(ExpressionSystem):
    """
    Equation system representation, takes an array of expressions with
    different unknowns and resolves the system.

    :see: Expression
    """

    _db_type = "ES"

    def __init__(self, expressions):
        ExpressionSystem.__init__(self, expressions, ['='])

    def resolve(self):
        expressions = []

        for i in range(0, len(self._left_operands)):
            lo = Poly(self._left_operands[i], self._symbols)
            ro = Poly(self._right_operands[i], self._symbols)
            expressions.append(lo - ro)
        solutions = solve_poly_system(expressions, self._symbols)

        return [list(x) for x in zip(*solutions)]

# ============================================================================
