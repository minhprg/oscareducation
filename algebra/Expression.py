# -*- coding: utf-8 -*-

import sys
import re as reg
from sympy import *
from abc import ABCMeta

#---------------------------------------------
#--- Expression
#---------------------------------------------

class ExpressionError(Exception):
    pass

class Expression:
    """
    General class defining an arithmetique expression
    An Expression object can be created with the args : 
        - expr (the expression in a String), 
        - sym (the variable of  the expression, the default value is x)
    """
        
    __metaclass__ = ABCMeta

    # --------------------------------------------------------- Magich methods

    def __init__(self, expr, sym='x'):
        expr = self._sanitize(expr)
        self.symbols = symbols(sym)
        self.leftOperand, self.operator, self.rightOperand = expr_split(expr)

        if verifEncode(self.leftOperand) or verifEncode(self.rightOperand):
            self.solution = self.resolve()
        else:
            raise ExpressionError('Invalid expression')

    def __str__(self):
        return self.leftOperand + self.operator + self.rightOperand

    def __eq__(self, other):
        return self.solution == other.solution

    # --------------------------------------------------------- Actual methods

    @staticmethod
    def _sanitize(expression):
        expression = expression.replace(' ', '')

        symbol = reg.compile('[a-zA-Z]')
        operator = reg.compile('[+\-*/%]') # add operators here
        targets = []

        for character in symbol.finditer(expression):
            before = expression[character.start() - 1]
            after = expression[character.start() + (
                0 if character.start() == len(expression) else 1
            )]

            if (operator.match(before) or 0 == character.start()) \
            and (operator.match(after) or character.start() == len(expression)):
                continue
            if not operator.match(before):
                targets.append(character.start() - 1)
            if not operator.match(after):
                targets.append(character.start() + 1)

        for i, target in enumerate(targets):
            expression = expression[0:target + 1] + '*' + expression[target + 1:len(expression)]
            targets[i+1:] = map(lambda x: x+ 1, targets[i+1:])

        return expression

    def resolve(self):
        raise NotImplementedError("Call to abstract method")


#---------------------------------------------
#--- Equation
#---------------------------------------------


class Equation(Expression):
    """Class for the expressions of the category Equation
    An Equation object can be created with the args : 
        - expr (the equation in a String), 
        - sym (the variable of  the equation, the default value is x)"""

    def resolve(self):
        """ return value of the solution of the equation in a String"""
        x = self.symbols
        str_Left = self.leftOperand
        str_Right = self.rightOperand
        print "LEFT : " + str_Left + "\n"
        print "RIGHT : " + str_Right + "\n"
        
        exprLeft = sympify(str_Left)
        exprRight = sympify(str_Right)
        globalExpression = exprLeft - exprRight
        return str(solveset(globalExpression, x))

    def is_equation(self):
        """return true if this is a correct inequation"""
        return self.operator == '=' and verifEncode(self.leftOperand) and verifEncode(self.rightOperand)



#---------------------------------------------
#--- Inequation
#---------------------------------------------


class Inequation(Expression):
    """Class for the expressions of the category Inequation
    An Inequation object can be created with the args : 
        - expr (the inequation in a String), 
        - sym (the variable of  the inequation, the default value is x)"""

    
    def resolve(inexpressionLeft, inexpressionRight, operator):
        """ return value of the solution of the inequation in a String"""
        globalInexpression = sympify(inexpressionLeft) - sympify(inexpressionRight)
        result = list(solveset(globalInexpression, x))
        strTab = solve_poly_inequality(Poly(globalInexpression, x), operator)

        i = 0
        for element in strTab :
            strTab[i]= str(element.inf)+" < "+"x"+" < "+str(element.sup)
            strTab[i] = strTab[i].replace("-oo < ", "")
            strTab[i] = strTab[i].replace(" < oo", "")
            i+=1

        return strTab

    def is_inequation(self):
        """return true if this is a correct inequation"""
        return self.operator in ('<','>','<=','>=') and verifEncode(self.leftOperand) and verifEncode(self.rightOperand)


#---------------------------------------------
#--- Equation System
#---------------------------------------------
    
class EquationSystem(Expression):
    """Class for the expressions of the category System of two Equations
    An EquationSystem object can be created with the args : 
        - expr (An array of two Strings with the equations), 
        - sym (the variables of  the expression, the default values are x and y)"""

    def __init__(self, expr, sym = 'x y'):
        self.equation1 = Equation(expr[0])
        self.equation2 = Equation(expr[1])
        self.x, self.y = symbols(sym)
        self.solution = self.resolve

    # TO DO
    def resolve(self):
        pass




#---------------------------------------------
#--- complementary functions
#---------------------------------------------


# compare un systeme de deux equation et dit si elle sont egales
def compare_expr(expressionLeft, expressionRight):
    x, y, z = symbols("x y z")
    str_Left = expressionLeft
    str_Right = expressionRight
    exprLeft = sympify(str_Left)
    exprRight = sympify(str_Right)
    return str(solveset(Eq(exprLeft, exprRight)))


def expr_split(exp):
    left = ''
    right= ''
    flag = False
    x = 0
    op = ''

    while x < len(exp): 
        if exp[x] == '=' :
            if exp[x+1] == '<' :
                op = '<='; x += 2; flag = True
            elif exp[x+1] == '>' :
                op = '>='; x += 2; flag = True
            else : op = '='; x += 1; flag = True
        elif exp[x] == '<' :
            if exp[x+1] == '=' : 
                op = '<='; x += 2; flag = True
            else : op = '<'; x += 1; flag = True
        elif exp[x] == '>' :
            if exp[x+1] == '=' : 
                op = '>='; x += 2; flag = True
            else : op = '>'; x += 1; flag = True
        if not flag : left +=  exp[x] 
        else : right += exp[x]
        x += 1
    if op is None : raise ExpressionError('Unknown operand')
    return left, op, right


def verifEncode(expression):
    if expression is None : return False
    try:
        str_expr = expression
        expr = sympify(str_expr)
        return true
    except ValueError:
        return false


def simplification_oneSide_equation(expression):
    x, y, z = symbols("x y z")
    str_expr = expression
    expr = sympify(str_expr)
    return str(simplify(expr))