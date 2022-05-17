import os

class MRNA:
    
    def __init__(self,yinit=0.5):
        self.y = yinit
        self.image_path = os.path.join(*[
            'C:\\','Users','alexd','Documents','faeder','complex','mrna.jpg'
        ])

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        self._y = value