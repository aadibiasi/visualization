class MRNA:

    def __init__(self,pos):
        self._riboPos = pos

    @property
    def riboPos(self):
        return self._riboPos

    @riboPos.setter
    def riboPos(self, value):
        self._riboPos = value