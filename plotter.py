from telnetlib import IP
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class Plotter:
    def __init__(self, options=None):
        self.options = options
        self.colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']

    def plot(self, state, ax=None, fig=None):
        ribos = state.ribos
        mrna = state.mrna
        
        # plot mrna
        # get mrna image array
        with open(mrna.image_path, "rb+") as imfile:
            mrna_arr_img = plt.imread(imfile)
        imagebox = OffsetImage(mrna_arr_img, zoom=0.2)
        imagebox.image.axes = ax
        
        ab = AnnotationBbox(imagebox, (38, mrna.y),
                            xycoords='data',
                            boxcoords="offset points",
                            frameon=False,
                            pad=0.5,
                            )

        ax.add_artist(ab)
        # ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3,zorder=5)
        
        # plot ribosomes 
        # get ribo image array
        ex_ribo = ribos[0]
        with open(ex_ribo.image_path, "rb+") as imfile:
            arr_img = plt.imread(imfile)
        # put each ribosome image on the plot
        for iribo,ribo in enumerate(ribos):
            if ribo.pos != -1:
                imagebox = OffsetImage(arr_img, zoom=0.05)
                imagebox.image.axes = ax

                ab = AnnotationBbox(imagebox, (ribo.pos, mrna.y),
                                    xycoords='data',
                                    boxcoords="offset points",
                                    frameon=False,
                                    pad=0.5,
                                    )

                ax.add_artist(ab)
                # print(f"Ribo ind: {iribo}, ribo pos: {ribo.pos}")
                # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)
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
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)


        # Annotate the 2nd position with another image (a Grace Hopper portrait)
