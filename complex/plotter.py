import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

class Plotter:
    def __init__(self, options=None):
        self.options = options
        # colors for lines and dots style plotting
        # self.colors = ['red','green','blue','yellow','magenta','cyan','gray','brown']

    def plot(self, state, ax=None, fig=None):
        # get mrna
        mrna = state.mrna
        # get ribosomes
        ssus = state.ssus
        lsus = state.lsus
        # get tcs
        tcs = state.tcs
        # get effects
        effects = state.effects
        
        # first let's plot mrna
        
        # # get mrna image array
        # with open(mrna.image_path, "rb+") as imfile:
        #     mrna_arr_img = plt.imread(imfile)
        # # make an image box
        # imagebox = OffsetImage(mrna_arr_img, zoom=0.145)
        # #TODO make zoom attributes to objects
        # #TODO make visible attribute to objects
        # imagebox.image.axes = ax
        # # make the annotation box
        # ab = AnnotationBbox(imagebox, ((mrna.xlen/2.0)-5, mrna.y), frameon=False)
        # # add annotation box to the plot
        # ax.add_artist(ab)
        # # plotting for lines and dots
        # ax.axhline(y=mrna.y, color='k', linestyle='-', linewidth=3,zorder=5)
        x = np.linspace(-10,300,1000)
        y = 0.01 * np.sin(np.pi/3 * x) + 0.5
        plt.plot(x,y,color='red')
        
        # next let's plot ssus 
        # get ssu image array
        with open(ssus[0].image_path, "rb+") as imfile:
            arr_img_ssu = plt.imread(imfile)
        # put each ssu image on the plot
        for issu,ssu in enumerate(ssus):
            if ssu.xpos != -1:
                # make the imagebox
                imagebox = OffsetImage(arr_img_ssu, zoom=0.4)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (ssu.xpos, ssu.ypos), frameon=False)
                # add the annotation box to the plot
                ax.add_artist(ab)
                # plotting for lines and dots
                # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)

        # next let's plot tcs 
        # get tc image array
        with open(tcs[0].image_path, "rb+") as imfile:
            arr_img_tc = plt.imread(imfile)
        # put each tc image on the plot
        for itc,tc in enumerate(tcs):
            if tc.xpos != -1:
                # make the imagebox
                imagebox = OffsetImage(arr_img_tc, zoom=0.03)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (tc.xpos, tc.ypos), frameon=False)
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
                imagebox = OffsetImage(arr_img_lsu, zoom=0.4)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (lsu.xpos, lsu.ypos), frameon=False)
                # add the annotation box to the plot
                ax.add_artist(ab)
                # plotting for lines and dots
                # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)

        # next let's plot effects 
        # get effect image array
        if len(effects) != 0:
            # put each effect image on the plot
            for ieffect,effect in enumerate(effects):
                with open(effects[ieffect].image_path, "rb+") as imfile:
                    arr_img_effect = plt.imread(imfile)
                if effect.xpos != -1:
                    # make the imagebox
                    imagebox = OffsetImage(arr_img_effect, zoom=0.03)
                    imagebox.image.axes = ax
                    # make the annotation box
                    ab = AnnotationBbox(imagebox, (effect.xpos, effect.ypos), frameon=False)
                    # add the annotation box to the plot
                    ax.add_artist(ab)
                    # plotting for lines and dots
                    # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)

        # current time
        ax.text(230,0.99,f'time: {state.time:.2f} seconds')
        # 5' and 3' ends
        ax.text(-5,0.75,f"5'")
        ax.text(270,0.75,f"3'")
        # set x/y limits
        ax.set_ylim([0,1])
        ax.set_xlim([0,mrna.xlen+1])
        # removes axis lines
        ax.axis('off')