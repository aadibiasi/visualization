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
        stateList = [State()]

        for i in self.firings.index:
            prevSSUs = cp.copy(stateList[i].ssus)
            prevLSUs = cp.copy(stateList[i].lsus)
            time = self.firings['time'][i]
            rxnType = self.firings['rxn'][i]

            #bind_tc_free_ssu
            if rxnType == 'bind_tc_free_ssu':
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
            prevPos = int(rxnSpl[len(rxnSpl)-1])

            #scan
            if len(rxnSpl) == 2 and rxnSpl[0] == 'scan':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevSSUs.append(SSU(x=prevPos+1,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #backward_scan
            if len(rxnSpl) == 3 and rxnSpl[0] == 'backward':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevSSUs.append(SSU(x=prevPos-1,y=0.5,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #scan_to_elongate
            if len(rxnSpl) == 4 and rxnSpl[0] == 'scan':
                prevSSUs.remove(SSU(x=prevPos,y=0.5,tc=1))
                prevSSUs.append(SSU(x=prevPos,y=0.6,tc=0))
                prevLSUs.append(LSU(x=prevPos,y=0.4))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #elongate
            if len(rxnSpl) == 2 and rxnSpl[0] == 'elongate':
                prevSSUs.remove(SSU(x=prevPos,y=0.6,tc=0))
                prevLSUs.remove(LSU(x=prevPos,y=0.4))
                prevSSUs.append(SSU(x=prevPos+3,y=0.6,tc=0))
                prevLSUs.append(LSU(x=prevPos+3,y=0.4))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

        return stateList

if __name__ == '__main__':
    LH = LogicHandler('test.tsv')