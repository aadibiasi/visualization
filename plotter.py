import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class Plotter:
    def __init__(self, options=None):
        self.options = options\
        # colors for lines and dots style plotting
        # self.colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']

    def plot(self, state, ax=None, fig=None):
        # get ribosomes
        ribos = state.ribos
        # get mrna
        mrna = state.mrna
        
        # first let's plot mrna
        
        # get mrna image array
        with open(mrna.image_path, "rb+") as imfile:
            mrna_arr_img = plt.imread(imfile)
        # make an image box
        imagebox = OffsetImage(mrna_arr_img, zoom=0.15)
        imagebox.image.axes = ax
        # make the annotation box
        ab = AnnotationBbox(imagebox, (50, mrna.y), frameon=False)
        # add annotation box to the plot
        ax.add_artist(ab)
        # plotting for lines and dots
        # ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3,zorder=5)
        
        # next let's plot ribosomes 
        # get ribo image array
        with open(ribos[0].image_path, "rb+") as imfile:
            arr_img = plt.imread(imfile)
        # put each ribosome image on the plot
        for iribo,ribo in enumerate(ribos):
            if ribo.pos != -1:
                # make the imagebox
                imagebox = OffsetImage(arr_img, zoom=0.011)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (ribo.pos, mrna.y), frameon=False)
                # add the annotation box to the plot
                ax.add_artist(ab)
                # plotting for lines and dots
                # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)
        # current time
        ax.text(70,0.9,f'time: {state.time:.2f} seconds')
        # set x/y limits
        ax.set_ylim([0,1])
        ax.set_xlim([0,100])
        # removes axis lines
        ax.axis('off')