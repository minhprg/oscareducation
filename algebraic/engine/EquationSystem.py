from . import Expression, Equation

from sympy import symbols

# ============================================================================
# ============================= Equation System ==============================
# ============================================================================
    
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
      #  self._operator = '='

    # TO DO
    def resolve(self):
        pass

# ============================================================================

Expression.register(EquationSystem)
