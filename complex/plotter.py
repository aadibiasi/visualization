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
        plt.plot(x,y,color='red',zorder=1)
        ax.hlines(y=0.25, xmin=-1, xmax=278, color='k', linestyle='-', linewidth=3, zorder=8)
        ax.hlines(y=0.25, xmin=25, xmax=91, color='b', linestyle='-', linewidth=9, zorder=9)
        ax.hlines(y=0.25, xmin=232, xmax=277, color='b', linestyle='-', linewidth=9, zorder=9)
        pts = [0,25,91,100,125,150,175,200,232,277]
        for p in pts:
            ax.vlines(x=p, ymin=0.22, ymax=0.28, color='k', linestyle='-', linewidth=1, zorder=10)
            ax.text(p,0.18,f"{p}",size=5,ha='center',zorder=10)
        #TODO stall on 88
        ax.vlines(x=88, ymin=0.16, ymax=0.28, color='k', linestyle='-', linewidth=1, zorder=10)
        ax.text(88,0.12,"stall at 88",size=5,ha='center',zorder=10)
        
        # next let's plot ssus 
        # get ssu image array
        with open(ssus[0].image_path, "rb+") as imfile:
            arr_img_ssu = plt.imread(imfile)
        # put each ssu image on the plot
        for issu,ssu in enumerate(ssus):
            #if ssu.xpos >= 0:
            # make the imagebox
            #z = -1.95*abs(0.5-ssu.ypos)+0.4
            imagebox = OffsetImage(arr_img_ssu, zoom=ssu.zoom)
            imagebox.image.axes = ax
            # make the annotation box
            ab = AnnotationBbox(imagebox, (ssu.xpos, ssu.ypos), frameon=False, zorder=2)
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
            if tc.xpos > 0:
                # make the imagebox
                #imagebox = OffsetImage(arr_img_tc, zoom=0.03)
                #imagebox.image.axes = ax
                # make the annotation box
                #ab = AnnotationBbox(imagebox, (tc.xpos, tc.ypos), frameon=False)
                # add the annotation box to the plot
                #ax.add_artist(ab)
                # plotting for lines and dots
                #z = -245*abs(0.5-tc.ypos)+50
                ax.scatter(tc.xpos, tc.ypos, tc.zoom, 'orange', zorder=3)

        # next let's plot lsus 
        # get lsu image array
        with open(lsus[0].image_path, "rb+") as imfile:
            arr_img_lsu = plt.imread(imfile)
        # put each lsu image on the plot
        for ilsu,lsu in enumerate(lsus):
            if lsu.xpos != -1:
                # make the imagebox
                #z = -1.95*abs(0.5-lsu.ypos)+0.4
                imagebox = OffsetImage(arr_img_lsu, zoom=lsu.zoom)
                imagebox.image.axes = ax
                # make the annotation box
                ab = AnnotationBbox(imagebox, (lsu.xpos, lsu.ypos), frameon=False, zorder=2)
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
                    imagebox = OffsetImage(arr_img_effect, zoom=0.03, zorder=4)
                    imagebox.image.axes = ax
                    # make the annotation box
                    ab = AnnotationBbox(imagebox, (effect.xpos, effect.ypos), frameon=False)
                    # add the annotation box to the plot
                    ax.add_artist(ab)
                    # plotting for lines and dots
                    # ax.plot(ribo.pos, mrna.y, 'o', color = self.colors[iribo],zorder=10)

        # current time
        ax.text(0,-0.05,f'time: {state.time:.2f} seconds', zorder=10)
        # 5' and 3' ends
        ax.text(-6,0.22,f"5'",ha='center',zorder=10)
        ax.text(285,0.22,f"3'",ha='center',zorder=10)
        # ORF
        ax.text(58,0.15,"ORF",ha='center',zorder=10)
        ax.text(254.5,0.15,"ORF",ha='center',zorder=10)
        # set x/y limits
        ax.set_ylim([0,1])
        ax.set_xlim([-10,mrna.xlen+10])
        # removes axis lines
        ax.axis('off')