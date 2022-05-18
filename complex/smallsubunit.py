import os

class SSU:

    def __init__(self,x=-1,y=-1,tc=0):
        self.xpos = x
        self.ypos = y
        self.tcsite = tc
        self.image_path = os.path.join(*[
            'C:\\','Users','alexd','Documents','faeder','complex','40s_blue.jpg'
        ])

    def __str__(self):
        print(f'POS:{self.xpos} TC:{self.tcsite}')

    def __repr__(self):
        return str(self)

    def __eq__(self,obj):
        return self.xpos == obj.xpos and self.ypos == obj.ypos and self.tcsite == obj.tcsite

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