from . import Expression, Equation

from sympy import symbols

# ============================================================================
# ============================= Equation System ==============================
# ============================================================================

@Expression.register
class EquationSystem(Expression):
    """
    Equation system representation, takes an array of expressions with
    different unknowns and resolves the system.

    :see: Expression
    """

    _db_type = "ES"

    def __init__(self, expr, sym = 'x y'):
        self.equation1 = Equation(expr[0])
        self.equation2 = Equation(expr[1])
        self.x, self.y = symbols(sym)
        self._solution = self.resolve

    # TO DO
    def resolve(self):
        pass

# ============================================================================
