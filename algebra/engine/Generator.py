
from fractions import Fraction
from random import choice


class GeneratorError(Exception):
    pass


class Generator(object):

    _operators = ['-', '+', '*', '/']

    def __init__(self, coef_range=20, fraction=True, degree=2):
        self._type = Fraction if fraction else int
        self._range = list([x for x in range(-coef_range, coef_range)])
        self._degree = degree

    def coefficients(self, nb=3):
        try:
            return [c for c in self._coefficient(nb)]
        except ZeroDivisionError:
            return self.coefficients(nb)

    def _coefficient(self, nb):
        i = 0
        while i < nb:
            yield self._type(self.fraction())
            i += 1

    def fraction(self):
        return Fraction(choice(self._range), choice(self._range))

    def product(self, a, b, operator=None):
        return str(a) + (choice(self._operators) if operator is None else operator) + str(b)

    def elevate(self, expression):
        return "(" + str(expression) + ")" + "^" + choice([n for n in range(1, self._degree)])

    def generate(self):
        expression = ""

        coefs = self.coefficients(self._degree + 1)

        i = 0
        for coef in coefs:
            if i > 0: expression += choice(self._operators) 
            expression += "x^" + str(len(coefs) - i - 1)
            expression += "(" + str(coef) + ")"
            i += 1

        return expression
