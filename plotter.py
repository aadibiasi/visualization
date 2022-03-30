from logicHandler import LogicHandler
from state import State
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.animation as animation

class Plotter:
    def __init__(self, options=None):
        self.options = options

    def plot(self, state, ax=None):
        ribos = state.ribos
        mrna = state.mrna
        # import IPython;IPython.embed()
        ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3,zorder=5)
        colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']
        for iribo,ribo in enumerate(ribos):
            if ribo.pos != -1:
                # print(f"Ribo ind: {iribo}, ribo pos: {ribo.pos}")
                ax.plot(ribo.pos, mrna.y, 'o', color = colors[iribo],zorder=10)
        

if __name__ == '__main__':
    # make a logic handler first
    LH = LogicHandler('model.rxns.tsv')
    # make a plotter
    P = Plotter()
    for i in range(1,1011,1):
        #print("###")
        #print(f"current time: {i/100.}")
        # instantiate an axis
        ax = plt.gca()
        # get the state you want to plot
        S = LH.findRibosomes(i/10.)
        # plot the state
        P.plot(S, ax=ax)
        # save the plot
        plt.text(70,0.9,f'time: {i/10} seconds')
        for x in range(0,101,1):
            plt.axvline(x,ymin=0.49,ymax=0.51,color='black',zorder=0)
        plt.ylim([0,1])
        plt.xlim([0,100])
        ax.axes.yaxis.set_visible(False)
        ax.axes.xaxis.set_visible(False)
        plt.savefig(f"test_{i:04d}.png")
        plt.close()
        # break

# if __name__ == '__main__':
#     LH = LogicHandler('model.rxns.tsv')
#     P = Plotter()

#     def helper(i):
#         state = LH.findRibosomes(i)
#         return P.plot(state,ax)

#     fig,ax = plt.subplots()
#     movie = animation.FuncAnimation(
#         fig,helper,save_count=101
#     )
#     writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     movie.save("movie.mp4", writer=writer)
#     plt.show()