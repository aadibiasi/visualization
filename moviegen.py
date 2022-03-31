import matplotlib.pyplot as plt
import os, subprocess, argparse
from logicHandler import LogicHandler
from plotter import Plotter
import numpy as np

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
        self.ffmpeg_path = os.path.abspath(self.args.ffmpeg_path)

    def parse_args(self):
        parser = argparse.ArgumentParser()

        # we need path to ffmpeg 
        parser.add_argument('-ffp','--ffmpeg_path', type=str, 
                            default=os.path.join(*['C:\\','Program Files','ImageMagick-7.1.0-Q16-HDRI','ffmpeg.exe']),
                            help='Path to ffmpeg_')

        # we need path to data file
        parser.add_argument('-i', '--input', type=str, 
                            default="model.rxns.tsv",
                            help='Path to input file')

        # we need path to output file
        parser.add_argument('-o','--output', type=str, 
                            default="frames",
                            help='Path to output folder')

        # we need path to output file
        parser.add_argument('-nf','--number_of_frames', type=int, 
                            default=1000,
                            help='Number of frames to output')

        # we need path to output file
        parser.add_argument('-dt','--delta_t', type=int, 
                            default=None,
                            help='Time between frames (this will override number of frames argument)')
        
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
        
        tmax, tmin = LH.tmax, LH.tmin
        if self.args.delta_t is None:
            dt = (tmax - tmin) / self.args.number_of_frames
        else:
            dt = self.args.delta_t
        # TODO: we need to determine this from the data
        print("Generating frames")
        for itime, time in enumerate(np.arange(tmin,tmax,dt)):
            # TODO: we should probably report the progress here with a progress bar
            #print("###")
            #print(f"current time: {i/100.}")
            if os.path.exists(f"{itime:05d}.png"):
                continue
            # instantiate an axis
            ax = plt.gca()
            fig = plt.gcf()
            # get the state you want to plot
            S = LH.get_state(time)
            # plot the state
            P.plot(S, ax=ax, fig=fig)
            # save the current frame
            plt.savefig(f"{itime:05d}.png")
            # close current frame to plot the next one
            plt.close()
            # import sys;sys.exit()
        
        # check ffmpeg_path path
        if self.ffmpeg_path is None:
            print("Please provide path to ffmpeg if you " + 
                "want to generate a movie."
            )
        else:
            # generate a movie
            # ffmpeg command to generate a movie compatible with quick time
            command = [
                self.ffmpeg_path,
                '-i', '%05d.png', '-f', 'mp4', '-pix_fmt', 'yuv420p', 
                '-vcodec', 'h264', 'movie.mp4'
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
                    raise Exception("error generating movie")
            except PermissionError as e:
                print("Permission error, ffmpeg path might be incorrect or you are running windows.")
                print("Please try to run the terminal with admin privileges if mencoder path is correct.")
                raise e
            print("Movie generated, file name is 'movie.mp4' by default")
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