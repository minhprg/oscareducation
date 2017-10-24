class Exercises_factory

    def __init__(self):
        #??

    def createEx(self,type,parseInput,ed):
        if type=="Equation" :
            return Equation(parseInput)
        elif type=="Inequation" :
            return Inequation(parseInput)
        elif type=="System" :
            return System(parseInput)

