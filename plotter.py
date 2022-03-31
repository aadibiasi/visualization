class Plotter:
    def __init__(self, options=None):
        self.options = options
        self.colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']

    def plot(self, state, ax=None):
        ribos = state.ribos
        mrna = state.mrna
        ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3,zorder=5)
        for iribo,ribo in enumerate(ribos):
            if ribo.pos != -1:
                # print(f"Ribo ind: {iribo}, ribo pos: {ribo.pos}")
                ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)
        # current time
        ax.text(70,0.9,f'time: {state.time:.2f} seconds')
        # vertical ticks for each ribosome spot
        # for x in range(0,101,1):
        #     ax.axvline(x,ymin=0.49,ymax=0.51,color='black',zorder=0)
        # sets x/y limits
        ax.set_ylim([0,1])
        ax.set_xlim([0,100])
        # removes axis lines
        ax.axes.yaxis.set_visible(False)
        ax.axes.xaxis.set_visible(False)