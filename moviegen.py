import matplotlib.pyplot as plt
import os, subprocess, argparse
from logicHandler import LogicHandler
from plotter import Plotter

# these are unnecessary for now
# import matplotlib as mpl
# import matplotlib.lines as mlines
# import matplotlib.animation as animation

class MovieGen:
    def __init__(self) -> None:
        # parse our command line arguments
        self.args = self.parse_args()
        # we need the absolute paths, so we'll do this for now
        # TODO: find a better way to do this
        self.input = os.path.abspath(self.args.input)
        self.output = os.path.abspath(self.args.output)
        self.mencoder_path = os.path.abspath(self.args.mencoder_path)

    def parse_args(self):
        parser = argparse.ArgumentParser()

        # we need path to mencoder 
        parser.add_argument('-mp','--mencoder_path', type=str, 
                            default=os.path.join(*["..","mplayer","mencoder.exe"]),
                            help='Path to mencoder')

        # we need path to data file
        parser.add_argument('-i', '--input', type=str, 
                            default="model.rxns.tsv",
                            help='Path to input file')

        # we need path to output file
        parser.add_argument('-o','--output', type=str, 
                            default="frames",
                            help='Path to output folder')

        return parser.parse_args()
        
    def run(self):
        # make a logic handler first
        LH = LogicHandler(self.input)
        # make a plotter
        P = Plotter()

        # if our output folder doesn't exist, create it
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        # get our current folder to go back to after we're done
        curr_dir = os.getcwd()
        # move to our folder
        os.chdir(self.output)
        
        # TODO: we need to determine this from the data
        print("Generating frames")
        for i in range(1,1011,1):
            # TODO: we should probably report the progress here with a progress bar
            #print("###")
            #print(f"current time: {i/100.}")
            # instantiate an axis
            ax = plt.gca()
            # get the state you want to plot
            S = LH.findRibosomes(i/10.)
            # plot the state
            P.plot(S, ax=ax)
            # current time
            plt.text(70,0.9,f'time: {i/10} seconds')
            # vertical ticks for each ribosome spot
            for x in range(0,101,1):
                plt.axvline(x,ymin=0.49,ymax=0.51,color='black',zorder=0)
            # sets x/y limits
            plt.ylim([0,1])
            plt.xlim([0,100])
            # removes axis lines
            ax.axes.yaxis.set_visible(False)
            ax.axes.xaxis.set_visible(False)
            # save the current frame
            plt.savefig(f"frame_{i:04d}.png")
            # close current frame to plot the next one
            plt.close()
        
        # check mencoder path
        if self.mencoder_path is None:
            print("Please provide path to mencoder if you " + 
                "want to generate a movie."
            )
        else:
            # generate a movie
            
            # sample command to run
            # ..\..\mplayer\mencoder.exe "mf://*.png" 
            # -mf fps=60:type=png -ovc lavc -lavcopts 
            # vcodec=mpeg4:mbd=2:trell:vbitrate=7000 
            # -vf scale=1024:768 -oac copy -o movie.avi
            
            # make our command list for subprocess
            command = [self.mencoder_path, 'mf://*.png', 
                '-mf', 'fps=60:type=png', '-ovc', 'lavc', 
                '-lavcopts', 'vcodec=mpeg4:mbd=2:trell:vbitrate=7000', 
                '-oac', 'copy', '-o', 'movie.avi'
            ]
            print("Attempting to generate movie")
            try:
                rc = subprocess.run(command, capture_output=True)
                if rc.returncode != 0:
                    print("error generating movie")
                    print("stderr was:")
                    print(rc.stderr)
                    print("stdout was:")
                    print(rc.stdout)
            except PermissionError as e:
                print("Permission error, most likely you are running windows.")
                print("Please make sure to run the terminal with admin " +
                    "privilages if you want to generate a movie directly"
                )
        # let's go back to where we were
        os.chdir(curr_dir)

if __name__ == '__main__':
    movie_gen = MovieGen()
    movie_gen.run()

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