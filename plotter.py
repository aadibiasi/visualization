from logicHandler import LogicHandler
from state import State
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os

class Plotter:
    def __init__(self, options=None):
        self.options = options
        self.colors = ["c", "m", "y", "k", "g", "b", "r", "0.5"]

    def plot(self, state, ax=None):
        ribos = state.ribos
        mrna = state.mrna
        # import IPython;IPython.embed()
        ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3)
        for iribo,ribo in enumerate(ribos):
            if ribo.pos != -1:
                # print(f"Ribo ind: {iribo}, ribo pos: {ribo.pos}")
                ax.plot(ribo.pos, mrna.y, marker="o", color=self.colors[iribo])
        

if __name__ == '__main__':
    # make a logic handler first
    LH = LogicHandler('model.rxns.tsv')
    # make a plotter
    P = Plotter()
    import numpy as np
    for i in np.arange(0,101,0.1):
        # print("###")
        # print(f"current time: {i}")
        # instantiate an axis
        ax = plt.gca()
        # get the state you want to plot
        S = LH.findRibosomes(i)
        # plot the state
        P.plot(S, ax=ax)
        # save the plot
        plt.ylim([0,1])
        plt.xlim([0,101])
        plt.savefig(os.path.join("frames", f"test_{int(i*10):05d}.png"))
        plt.close()
        # break
    # stitch together the movie with mencoder after
    # sample command 
    # ..\..\mplayer\mencoder.exe "mf://*.png" 
    # -mf fps=60:type=png -ovc lavc -lavcopts 
    # vcodec=mpeg4:mbd=2:trell:vbitrate=7000 
    # -vf scale=1024:768 -oac copy -o movie.avi