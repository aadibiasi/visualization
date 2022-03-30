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