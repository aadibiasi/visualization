import os

class SSU:

    def __init__(self,x=-1,y=-1,tc=0):
        self.xpos = x
        self.ypos = y
        self.tcsite = tc
        self.image_path = os.path.join(*[
            'C:\\','Users','alexd','Documents','faeder','complex','40s_blue.jpg'
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

        @property
        def tcsite(self):
            return self._tcsite

        @tcsite.setter
        def tcsite(self,value):
            self._tcsite = value