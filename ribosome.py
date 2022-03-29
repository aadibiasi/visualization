class Ribosome:

    def __init__(self,p = -1):
        self.pos = p

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value