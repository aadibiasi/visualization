import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class Plotter:
    def __init__(self, options=None):
        self.options = options\
        # colors for lines and dots style plotting
        # self.colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']

    def plot(self, state, ax=None, fig=None):
        # get ribosomes
        ssus = state.ssus
        lsus = state.lsus
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
        
        # next let's plot ssus 
        # get ssu image array
        with open(ssus[0].image_path, "rb+") as imfile:
            arr_img_ssu = plt.imread(imfile)
        # put each ssu image on the plot
        for issu,ssu in enumerate(ssus):
            if ssu.xpos != -1:
                # make the imagebox
                imagebox = OffsetImage(arr_img_ssu, zoom=0.02)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (ssu.xpos, ssu.ypos), frameon=False)
                # add the annotation box to the plot
                ax.add_artist(ab)
                # plotting for lines and dots
                # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)

        # next let's plot lsus 
        # get lsu image array
        with open(lsus[0].image_path, "rb+") as imfile:
            arr_img_lsu = plt.imread(imfile)
        # put each lsu image on the plot
        for ilsu,lsu in enumerate(lsus):
            if lsu.xpos != -1:
                # make the imagebox
                imagebox = OffsetImage(arr_img_lsu, zoom=0.02)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (lsu.xpos, lsu.ypos), frameon=False)
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