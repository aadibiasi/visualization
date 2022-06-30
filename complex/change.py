from smallsubunit import SSU
from ternarycomplex import TC
from largesubunit import LSU

class Change:

    def __init__(self,b,a):
        self.before = b
        self.after = a

    @property
    def before(self):
        return self._before

    @before.setter
    def before(self,b):
        self._before = b

    @property
    def after(self):
        return self._after

    @after.setter
    def after(self,a):
        self._after = a