from ribosome import Ribosome
from mrna import MRNA

class State:

    def __init__(self,pos):
        self._mrna = MRNA(pos)
        self._ribos = []
        for ind in pos:
            self._ribos.append(Ribosome(ind))

    @property
    def ribos(self):
        return self._ribos

    @ribos.setter
    def ribos(self, newRibos):
        self._ribos = newRibos

    @property
    def mrna(self):
        return self._mrna

    @mrna.setter
    def mrna(self, newMRNA):
        self._mrna = newMRNA