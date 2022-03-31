from ribosome import Ribosome
from mrna import MRNA

class State:

    def __init__(self,pos,time):
        self.time = time
        self.mrna = MRNA()
        self.ribos = []
        for ind in pos:
            self.ribos.append(Ribosome(ind))

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
    
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value