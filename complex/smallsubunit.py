import os

class SSU:

    def __init__(self,x=-1,y=-1,ltm=-1):
        self.xpos = x
        self.ypos = y
        self.last_time_modified = ltm
        self.image_path = os.path.join(*[
            'C:\\','Users','alexd','Documents','faeder','visualization','complex','40s_blue100.png'
        ])

    def __str__(self):
        return f'POS:{self.xpos}'

    def __repr__(self):
        return str(self)

    def __eq__(self,obj):
        return self.xpos == obj.xpos and self.ypos == obj.ypos

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
    def last_time_modified(self):
        return self._last_time_modified

    @last_time_modified.setter
    def last_time_modified(self,value):
        self._last_time_modified = value