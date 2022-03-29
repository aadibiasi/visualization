from logicHandler import LogicHandler
from state import State

class Plotter:

    def __init__(self,tsvFileName):
        self._logic = LogicHandler(tsvFileName)

    @property
    def logic(self):
        return self._logic

    def plot(self,t):
        state = self._logic.findRibosomes(t)
        ribos = state.ribos
        mrna = state.mrna
        for r in ribos:
            print(r.pos)

if __name__ == '__main__':
    p = Plotter("model.rxns.tsv")
    p.plot(101)