

class InputHandler:
    def __init__(self, type): #type = 0, 1, 2, 3, 4, 5
        self.type = type
    """This function will parse any exercise (equation, inequation, system and expessions).
       An input handler object can only parse one type of exercises so you have to create 4
       different handlers to parse all the exercises."""
    def parse(self, inputString):
        if self.type == "algebraicEquation":
            return self.parseEq(inputString)
        elif self.type == "algebraicInequation":
            return self.parseIneq(inputString)
        elif self.type == "algebraicSystem":
            return self.parseSys(inputString) #tuple of strings
        elif self.type == "algebraicExpression":
            return self.parseExp(inputString)
        else:
            return "Type not found"

    """This function parses a system of equations
       inputString is a list/tuple of two equations"""
    def parseSys(self, inputStrings):
        eq1 = self.parseEq(inputStrings[0]) # parse each equation independently
        eq2 = self.parseEq(inputStrings[1])
        if eq1 == "Trop ou pas de variables" or eq1 == "L'equation n'est pas bien exprimee":
            raise ValueError(eq1)
        elif eq2 == "Trop ou pas de variables" or eq2 == "L'equation n'est pas bien exprimee":
            raise ValueError(eq2)
        elif len(eq1[1]) == 2: # the system needs two variables
            return (([eq1[0], eq2[0]]), eq1[1][0]+","+eq1[1][1])
        elif len(eq2[1]) == 2:
            return (([eq1[0], eq2[0]]), eq2[1][0]+","+eq2[1][1])
        elif len(eq1[1]) == 1 and len(eq2[1]) == 1 and eq1[1][0] != eq2[1][0]:
            return ((eq1[0], eq2[0]), eq1[1][0]+","+eq2[1][0])
        else:
            raise ValueError

    """This function parses an expression
       inputString is the expression as a string"""
    def parseExp(self, inputString):
        inputString = inputString.replace(" ", "")
        bool = self.checkParseErrorExp(list(inputString))
        if bool:
            inputString = inputString.replace("^", "**") # replace exponents for sympy
            return inputString, "a"
        else:
            raise ValueError("L'expression n'est pas bien formee")

    """This function parses an equation
       inputString is the equation as a string"""
    def parseEq(self,inputString):
        inputString = inputString.replace(" ", "") # remove any white space
        s = inputString.split("=") # split the equation in two
        if len(s) == 2:
            listChar1 = list(s[0]) # transform each part in a list of character to check them separately
            listChar2 = list(s[1])
            if len(listChar1) > 0 and len(listChar2) > 0:
                if listChar1[0].isalnum() or listChar1[0] == "(" or listChar1[0] == "-": # check for first character
                    bool1 = self.checkParseError(listChar1) # if first character is ok, then begin checking
                else:
                    bool1 = False

                if listChar2[0].isalnum() or listChar2[0] == "(" or listChar2[0] == "-": # same here for the second part
                    bool2 = self.checkParseError(listChar2)
                else:
                    bool2 = False
            else:
                bool1 = False
                bool2 = False
        else:
            bool1 = False
            bool2 = False
        variables = self.findVariables(inputString) # returns all the alpha character
        if bool1 and bool2 and len(variables)==1: # if only one variable and correctly parsed, then it's fine
            inputString = s[0]+"-("+s[1]+")" # the format for sympy requires no equal in the equation
            #                                  (it considers that the input is equal to zero so return part1 - (part2)
            inputString = inputString.replace("^", "**") # replace exponent for sympy
            return (inputString, variables[0]) # return the input string and the name of the variable
        elif len(variables) > 1 and bool1 and bool2 and self.type == "algebraicEquation":
            raise ValueError("Trop de variables")
        elif len(variables) == 2 and bool1 and bool2 and self.type == "algebraicSystem":
            inputString = s[0] + "-(" + s[1] + ")"
            inputString = inputString.replace("^", "**")
            return (inputString, variables)
        elif self.type == "algebraicSystem":
            raise ValueError("Les equations ne sont pas bien ecrites!")
        else:
            raise ValueError("L'equation n'est pas bien ecrite!")

    """ The function name says it all :) """
    def findVariables(self, inputString):
        variables = []
        for elem in list(inputString):
            if elem.isalpha() and elem not in variables:
                variables.append(elem)
        return variables

    """Same as parseEq but for inequation
       Here we need to return the inequation as such to keep the sign (<, >, <= or >=)"""
    def parseIneq(self,inputString):
        inputString = inputString.replace(" ", "") # remove white space
        listChar = list(inputString) #check every character
        if listChar[0].isalnum() or listChar[0] == "(" or listChar[0] == "-": #check first character
            bool = self.checkParseErrorIneq(listChar)
        else:
            bool = False

        variables = self.findVariables(inputString)
        if bool and len(variables)==1:
            inputString = inputString.replace("^", "**")
            return (inputString, variables[0]) # return inequation and variable
        elif (len(variables) > 1 or len(variables) == 0) and bool:
            raise ValueError("Trop de variables!")
        else:
            raise ValueError("L'inequation n'est pas bien ecrite!") # return a good error to be printed

    """This function is used for equations and systems. It is called in parseSys and parseEq.
       listChar is the list of character to check"""
    def checkParseError(self,listChar, nbPar = 0):
        if not listChar and nbPar == 0:
            return True # no parse error

        if nbPar < 0: # add 1 for open parenthesis "(" and subtract 1 for closed parenthesis ")"
            return False
        if len(listChar) > 1: # if more than 1 character remaining, after checking first and second
            #                   either return false or make a recursive call (after deleting the first element
            #                   the goal is to check every pair of characters to make sure that it is parsed correctly
            if listChar[0].isnumeric(): #if first is numerical
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                else:
                    return False
            elif listChar[0].isalpha(): # if first is a letter
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "+" or listChar[0] == "-" or listChar[0] == "*"  or listChar[0] == "/" or listChar[0] == "^":
                # if first is a math sign
                if listChar[1].isalnum(): # if second is a letter or numeric
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseError(listChar,nbPar)
                else:
                    return False
            elif listChar[0] == "(": # if first is open parenthesis (and so on for the other elif
                if listChar[1].isalnum() or listChar[1] == "(" or listChar[1] == "-":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar+1)
                else:
                    return False
            elif listChar[0] == ")":
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "=" or listChar[1] == "^" or listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseError(listChar,nbPar-1)
                else:
                    return False
            else:
                return False
        elif len(listChar) == 0 and nbPar == 0: # if list empty, all characters ok and if parenthesis well formed
            return True
        else: # if there is only one character left
            if nbPar == 1 and listChar[0] == ")":
                return True
            elif listChar[0].isalnum() and nbPar == 0:
                return True
            else:
                return False

    """This function is the same as checkParseError but for inequation. The principle remains the same"""
    def checkParseErrorIneq(self,listChar, nbPar = 0):
        if not listChar and nbPar == 0:
            return True #no parse error

        if nbPar < 0:
            return False
        if len(listChar) > 1:
            if listChar[0].isnumeric():
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif (listChar[1] == "<" or listChar[1] == ">") and nbPar == 0:
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                else:
                    return False
            elif listChar[0].isalpha():
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif (listChar[1] == "<" or listChar[1] == ">") and nbPar == 0:
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "+" or listChar[0] == "-" or listChar[0] == "*"  or listChar[0] == "/" or listChar[0] == "^":
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                elif listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "(":
                if listChar[1].isalnum() or listChar[1] == "(" or listChar[1] == "-":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar+1)
                else:
                    return False
            elif listChar[0] == ")":
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "<" or listChar[1] == ">" or listChar[1] == "^" or listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar-1)
                else:
                    return False
            elif listChar[0] == "<" or listChar[0] == ">":
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar,nbPar)
                elif listChar[1] == "=" or listChar[1] == "-" or listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "=":
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar,nbPar)
                elif listChar[1] == "-" or listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseErrorIneq(listChar, nbPar)
                else:
                    return False
            else:
                return False
        elif len(listChar) == 0 and nbPar == 0:
            return True
        else:
            if nbPar == 1 and listChar[0] == ")":
                return True
            elif listChar[0].isalnum() and nbPar == 0:
                return True
            else:
                return False

    """Once again, this is the same as checkParseError but for expressions"""
    def checkParseErrorExp(self,listChar, nbPar = 0):
        if not listChar and nbPar == 0:
            return True #no parse error

        if nbPar < 0:
            return False
        if len(listChar) > 1:
            if listChar[0].isnumeric():
                if listChar[1].isnumeric():
                    del listChar[0]
                    return self.checkParseErrorExp(listChar, nbPar)
                elif listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseErrorExp(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseErrorExp(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "+" or listChar[0] == "-" or listChar[0] == "*"  or listChar[0] == "/" or listChar[0] == "^":
                if listChar[1].isnumeric():
                    del listChar[0]
                    return self.checkParseErrorExp(listChar, nbPar)
                elif listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseErrorExp(listChar,nbPar)
                else:
                    return False
            elif listChar[0] == "(":
                if listChar[1].isnumeric() or listChar[1] == "(" or listChar[1] == "-":
                    del listChar[0]
                    return self.checkParseErrorExp(listChar, nbPar+1)
                else:
                    return False
            elif listChar[0] == ")":
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "=" or listChar[1] == "^" or listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseErrorExp(listChar,nbPar-1)
                else:
                    return False
            else:
                return False
        elif len(listChar) == 0 and nbPar == 0:
            return True
        else:
            if nbPar == 1 and listChar[0] == ")":
                return True
            elif listChar[0].isnumeric() and nbPar == 0:
                return True
            else:
                return False
