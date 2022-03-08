from logicHandler import LogicHandler
from state import State

class Plotter:

    def __init__(self,tsvFileName):
        self.logic = LogicHandler(tsvFileName)

    @property
    def logic(self):
        return self.logic

    def plot(self,t):
        state = self.logic.findRibosomes(t)
        ribos = state.ribos()
        mrna = state.mrna()
        print(ribos[t])

if __name__ == '__main__':
    p = Plotter("model.rxns.tsv")
    p.plot(3)