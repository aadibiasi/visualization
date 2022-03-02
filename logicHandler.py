import pandas as pd
import numpy as np
from ribosome import Ribosome

class LogicHandler:

    def __init__(self,tsvFileName = ""):
        self.tsv = tsvFileName
        self.firings = self.genFirings()
        self.numRibosomes = self.firings['rxn'].value_counts().initiate
        self.ribosomePos = self.genPositions()

    @property
    def tsv(self):
        return self.tsv

    @tsv.setter
    def tsv(self, newFileName):
        self.__init__(newFileName)

    @property
    def firings(self):
        return self._p

    @property
    def numRibosomes(self):
        return self._p

    @property
    def ribosomePos(self):
        return self._p

    def genFirings(self):
        return pd.read_csv(self.tsv,sep='\t')

    def genPositions(self):
        df = pd.DataFrame(index=range(self.firings['line'].max()),columns=range(self.numRibosomes)).fillna(-1)
        df.insert(len(df.columns),'time',self.firings.time)
        for ind in self.firings.index:
            rxnType = self.firings['rxn'][ind]
            if rxnType[0] == 'i':
                pos = 0
            elif rxnType[0] == 't':
                pos = 100
            else:
                pos = int(rxnType[9:])
            row = df.iloc[ind,:]
            colNum  = -1
            for col in row:
                colNum += 1
                if col == pos-1:
                    df[colNum][ind:] = pos
                    break
        return df

    def findRibosomes(self,t):
        times = self.firings['time'].to_numpy()
        ind = np.digitize(t,times) - 1
        return self.ribosomePos.iloc[ind]
