import os

class LSU:

    def __init__(self,x=-1,y=-1):
        self.xpos = x
        self.ypos = y
        self.image_path = os.path.join(*[
            'C:\\','Users','alexd','Documents','faeder','complex','60s_green.jpg'
        ])

        @property
        def xpos(self):
            return self._xpos

        @xpos.setter
        def xpos(self,value):
            self._xpos = value

        @property
        def ypos(self):
            return self._ypos

        @ypos.setter
        def ypos(self,value):
            self._ypos = value