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
        stateList = []
        stateList.append(State())
        for i in self.firings.index:
            prevSSUs = cp.copy(stateList[i].ssus)
            prevLSUs = cp.copy(stateList[i].lsus)
            time = self.firings['time'][i]
            rxnType = self.firings['rxn'][i]

            #bind_tc_free_ssu
            if(rxnType == 'bind_tc_free_ssu'):
                prevSSUs.append(SSU(x=0,y=0.25,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #bind_cap_pic_0
            if(rxnType == 'bind_cap_pic_0'):
                prevSSU = SSU(x=-1,y=0.25,tc=1)
                newSSU = SSU(x=0,y=0.5,tc=1)
                stateList.remove(prevSSU)
                stateList.append(newSSU)
                continue

            rxnSpl = rxnType.split('_')
            pos = int(rxnSpl[len(rxnSpl)-1])

            #scan
            if len(rxnSpl) == 2 and rxnSpl[0] == 'scan':
                prevSSU = SSU(x=pos-1)

            #backward_scan

            #scan_to_elongate

            #elongate

if __name__ == '__main__':
    LH = LogicHandler('model.tsv')