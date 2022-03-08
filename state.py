from ribosome import Ribosome
from mrna import MRNA

class State:

    def __init__(self,pos):
        self.mrna = MRNA(pos)
        self.ribos = []
        for ind in pos:
            self.ribos.append(Ribosome(pos[ind]))

    @property
    def ribos(self):
        return self.ribos

    @property
    def mrna(self):
        return self.mrna