import os

class MRNA:
    
    def __init__(self,yinit=0.5):
        self.xlen = 278
        self.y = yinit
        self.image_path = os.path.join(*[
             'C:\\','Users','Akhlore','visualization','complex','mrnared.png'
        ])

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        self._y = value