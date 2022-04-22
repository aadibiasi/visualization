import os 

class MRNA:
    def __init__(self,y=0.5,max_ribos=100):
        self.y = y
        self.max_ribos = max_ribos
        self.image_path = os.path.join(*[
            'C:\\','Users','Akhlore','visualization','mrna.jpg'
        ])

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def max_ribos(self):
        return self._max_ribos

    @max_ribos.setter
    def max_ribos(self, value):
        self._max_ribos = value