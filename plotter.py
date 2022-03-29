from logicHandler import LogicHandler
from state import State
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class Plotter:
    def __init__(self, options=None):
        self.options = options

    def plot(self, state, ax=None):
        ribos = state.ribos
        mrna = state.mrna
        # import IPython;IPython.embed()
        ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3)
        for ribo in ribos:
            if ribo.pos != -1:
                ax.plot(ribo.pos, mrna.y, 'ro')
        

if __name__ == '__main__':
    # make a logic handler first
    LH = LogicHandler('model.rxns.tsv')
    # make a plotter
    P = Plotter()
    for i in [1,10,100]:
        # instantiate an axis
        ax = plt.gca()
        # get the state you want to plot
        S = LH.findRibosomes(i)
        # plot the state
        P.plot(S, ax=ax)
        # save the plot
        plt.ylim([0,1])
        plt.xlim([0,101])
        plt.savefig(f"test_{i:04d}.png")