class MRNA:

    def __init__(self,pos):
        self.riboPos = pos

    @property
    def riboPos(self):
        return self._r

    @riboPos.setter
    def riboPos(self, value):
        self._r = value