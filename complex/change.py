from smallsubunit import SSU
from ternarycomplex import TC
from largesubunit import LSU

class Change:

    def __init__(self,b,a):
        self.before = b
        self.after = a

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"before: {self.before}, after: {self.after}"

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