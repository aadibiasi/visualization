from mrna import MRNA
from smallsubunit import SSU
from ternarycomplex import TC
from largesubunit import LSU
from effect import Effect

class State:

    def __init__(self,t=0,s=[],tc=[],l=[],e=[]):
        self.time = t
        self.mrna = MRNA()
        self.ssus = s
        self.tcs = tc
        self.lsus = l
        self.effects = e

    def __str__(self):
        return f'Time: {self.time}\nSSUs: {self.ssus}\nLSUs: {self.lsus}'

    def __repr__(self):
        return str(self)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self,t):
        self._time = t

    @property
    def mrna(self):
        return self._mrna

    @mrna.setter
    def mrna(self, newMRNA):
        self._mrna = newMRNA

    @property
    def ssus(self):
        return self._ssus

    @ssus.setter
    def ssus(self, newSSUs):
        self._ssus = newSSUs

    @property
    def tcs(self):
        return self._tcs

    @tcs.setter
    def tcs(self, newTCs):
        self._tcs = newTCs

    @property
    def lsus(self):
        return self._lsus

    @lsus.setter
    def lsus(self, newLSUs):
        self._lsus = newLSUs

    @property
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, newEffects):
        self._effects = newEffects