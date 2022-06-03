import os

class Effect:

    def __init__(self,x=-1,y=-1,n='',ip=[]):
        self.xpos = x
        self.ypos = y
        self.name = n
        if len(ip) > 0:
            self.image_path = os.path.join(*ip)
        else:
            self.image_path = None
        #self.lifetime = 1

    def __str__(self):
        return f'POS:{self.xpos} , Name:{self.name}'

    def __repr__(self):
        return str(self)

    def __eq__(self,obj):
        return self.xpos == obj.xpos and self.ypos == obj.ypos and self.name == obj.name

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
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value

    @property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self,value):
        self._image_path = value