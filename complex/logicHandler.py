import copy as cp
import pandas as pd
import numpy as np
from state import State
from mrna import MRNA
from smallsubunit import SSU
from largesubunit import LSU

class LogicHandler:

    def __init__(self,tsvFileName=""):
        self.tsv = tsvFileName
        self.firings = self.genFirings()
        self.states = self.genStates()

    @property
    def tsv(self):
        return self._tsv

    @tsv.setter
    def tsv(self, newFileName):
        self._tsv = newFileName

    @property
    def firings(self):
        return self._firings

    @firings.setter
    def firings(self, newFirings):
        self._firings = newFirings

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, newStates):
        self._states = newStates

    def genFirings(self):
        return pd.read_csv(self.tsv,sep='\t')

    def genStates(self):
        initialSSUs = 100 * [SSU(x=-1,y=0.5,tc=0)]
        initialLSUs = 100 * [SSU(x=-1,y=0.5)]
        stateList = [State(0,initialSSUs,initialLSUs)]

        for i in self.firings.index:
            prevSSUs = cp.copy(stateList[i].ssus)
            prevLSUs = cp.copy(stateList[i].lsus)
            time = self.firings['time'][i]
            rxnType = self.firings['rxn'][i]

            #bind_tc_free_ssu
            if rxnType == 'bind_tc_free_ssu':
                prevSSUs.remove(SSU(x=-1,y=0.5,tc=0))
                prevSSUs.append(SSU(x=-1,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #bind_cap_pic_0
            if rxnType == 'bind_cap_pic_0':
                prevSSUs.remove(SSU(x=-1,y=0.5,tc=1))
                prevSSUs.append(SSU(x=0,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue
            
            rxnSpl = rxnType.split('_')
            prevPos = int(rxnSpl[-1])
            prevPosStr = rxnSpl[-1]

            #scan
            if rxnType == f'scan_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevSSUs.append(SSU(x=prevPos+1,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #backward_scan
            if rxnType == f'backward_scan_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevSSUs.append(SSU(x=prevPos-1,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #scan_to_elongate
            if rxnType == f'scan_to_elongate_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevLSUs.remove(LSU(x=-1,y=0.5))
                prevSSUs.append(SSU(x=prevPos,y=0.6,tc=0))
                prevLSUs.append(LSU(x=prevPos,y=0.4))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #elongate
            if rxnType == f'elongate_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=0.6,tc=0))
                prevLSUs.remove(LSU(x=prevPos,y=0.4))
                prevSSUs.append(SSU(x=prevPos+3,y=0.6,tc=0))
                prevLSUs.append(LSU(x=prevPos+3,y=0.4))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #TODO terminate and recycling

        return stateList

if __name__ == '__main__':
    LH = LogicHandler('test.tsv')
    
    #This kinda blows up the terminal because it lists all 100 SSUs and LSUs for every state
    #for i in LH.states:
    #    print(i)