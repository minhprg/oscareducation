

class InputHandler:
    def __init__(self, type): #type = 0, 1, 2, 3, 4, 5
        self.type = type
    def parse(self, inputString):
        if self.type == "algebraicEquation":
            return self.parseEq(inputString)
        elif self.type == "algebraicInequation":
            return self.parseIneq(inputString)
        elif self.type == "algebraicSystem":
            return self.parseSys(inputString) #tuple of strings
        else:
            return "Type not found"

    def parseSys(self, inputStrings):
        eq1 = self.parseEq(inputStrings[0])
        eq2 = self.parseEq(inputStrings[1])
        if eq1 == "Trop ou pas de variables" or eq1 == "L'equation n'est pas bien exprimee":
            raise ValueError(eq1)
        elif eq2 == "Trop ou pas de variables" or eq2 == "L'equation n'est pas bien exprimee":
            raise ValueError(eq2)
        elif len(eq1[1]) == 2:
            return ([eq1[0], eq2[0]], eq1[1][0]+","+eq1[1][1])
        elif len(eq2[1]) == 2:
            return ([eq1[0], eq2[0]], eq2[1][0]+","+eq2[1][1])
        elif len(eq1[1]) == 1 and len(eq2[1]) == 1 and eq1[1][0] != eq2[1][0]:
            return (eq1[0], eq2[0], eq1[1][0]+","+eq2[1][0])
        else:
            raise ValueError

    def parseEq(self,inputString):
        inputString = inputString.replace(" ", "")
        s = inputString.split("=")
        if len(s) == 2:
            listChar1 = list(s[0])
            listChar2 = list(s[1])
            if len(listChar1) > 0 and len(listChar2) > 0:
                if listChar1[0].isalnum() or listChar1[0] == "(" or listChar1[0] == "-":
                    bool1 = self.checkParseError(listChar1)
                else:
                    bool1 = False

                if listChar2[0].isalnum() or listChar2[0] == "(" or listChar2[0] == "-":
                    bool2 = self.checkParseError(listChar2)
                else:
                    bool2 = False
            else:
                bool1 = False
                bool2 = False
        else:
            bool1 = False
            bool2 = False
        variables = self.findVariables(inputString)
        if bool1 and bool2 and len(variables)==1:
            inputString = s[0]+"-("+s[1]+")"
            inputString = inputString.replace("^", "**")
            return (inputString, variables[0]) #appler exercice avec inputString correctement parser
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

    def findVariables(self, inputString):
        variables = []
        for elem in list(inputString):
            if elem.isalpha() and elem not in variables:
                variables.append(elem)
        return variables

    def parseIneq(self,inputString):
        inputString = inputString.replace(" ", "")
        listChar = list(inputString)
        if listChar[0].isalnum() or listChar[0] == "(" or listChar[0] == "-":
            bool = self.checkParseErrorIneq(listChar)
        else:
            bool = False

        variables = self.findVariables(inputString)
        if bool and len(variables)==1:
            inputString = inputString.replace("^", "**")
            return (inputString, variables[0]) #appler exercice avec inputString correctement parser
        elif (len(variables) > 1 or len(variables) == 0) and bool:
            raise ValueError("Trop de variables!")
        else:
            raise ValueError("L'inequation n'est pas bien ecrite!") #print parse error

    def checkParseError(self,listChar, nbPar = 0):
        if not listChar and nbPar == 0:
            return True #no parse error

        if nbPar < 0:
            return False
        if len(listChar) > 1:
            if listChar[0].isnumeric():
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
            elif listChar[0].isalpha():
                if listChar[1] == "+" or listChar[1] == "-" or listChar[1] == "*" or listChar[1] == "/" or listChar[1] == "^":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == ")":
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                else:
                    return False
            elif listChar[0] == "+" or listChar[0] == "-" or listChar[0] == "*"  or listChar[0] == "/" or listChar[0] == "^":
                if listChar[1].isalnum():
                    del listChar[0]
                    return self.checkParseError(listChar, nbPar)
                elif listChar[1] == "(":
                    del listChar[0]
                    return self.checkParseError(listChar,nbPar)
                else:
                    return False
            elif listChar[0] == "(":
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
        elif len(listChar) == 0 and nbPar == 0:
            return True
        else:
            if nbPar == 1 and listChar[0] == ")":
                return True
            elif listChar[0].isalnum() and nbPar == 0:
                return True
            else:
                return False

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
