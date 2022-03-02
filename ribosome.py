class Ribosome:

    def __init__(self,p = -1):
        self.pos = p

    @property
    def pos(self):
        return self._p

    @pos.setter
    def pos(self, value):
        self._p = value

if __name__ == '__main__':
    r = Ribosome()
    print(r.pos)