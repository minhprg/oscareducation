class Exercice(object):
    # Create based on class name:
    def factory(type):
        #return eval(type + "()")
        if type == "Equation": return Equation()
        if type == "Inequation": return Inequation()
        if type == "System": return System()
    factory = staticmethod(factory)


class Equation(Shape):
    def isEquivalant(self, other):
        # to complete

    def isSolution(self, solution):
        # to complete


class Inequation(Shape):
    def isEquivalant(self, other):
        # to complete

    def isSolution(self, solution):
        # to complete


class System(Shape):
    def isEquivalant(self, other):
        # to complete

    def isSolution(self, solution):
        # to complete
