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
        self.tmax, self.tmin = self.firings['time'].max(), self.firings['time'].min()

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
        ssu_y_base = 0.5
        ssu_y_up = 0.565
        lsu_y_base = 0.5
        lsu_y_down = 0.45

        #TODO remove this hardcode
        initialSSUs = 100 * [SSU(x=-1,y=0.5,tc=1)]
        #initialSSUs += [SSU(x=200,y=0.5,tc=0),SSU(x=230,y=0.5,tc=0)]
        initialLSUs = 100 * [LSU(x=-1,y=0.5)]
        #initialLSUs += [LSU(x=200,y=0.4),LSU(x=230,y=0.4)]
        stateList = [State(0,initialSSUs,initialLSUs)]

        for i in self.firings.index:
            rxnType = self.firings['rxn'][i]
            try:
                prevSSUs = cp.copy(stateList[i].ssus)
                prevLSUs = cp.copy(stateList[i].lsus)
            except IndexError:
                print(rxnType)
                print(i)
                print("couldn't parse a reaction, quitting")
                break
            time = self.firings['time'][i]
            rxnType = self.firings['rxn'][i]

            #bind_tc_free_ssu
            if rxnType == 'tc_free_ssu_binding':
                prevSSUs.remove(SSU(x=-1,y=ssu_y_base,tc=0))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #bind_cap_pic_0
            if rxnType == 'bind_cap_pic_0':
                prevSSUs.remove(SSU(x=-1,y=ssu_y_base,tc=1))
                prevSSUs.append(SSU(x=0,y=ssu_y_base,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue
            
            rxnSpl = rxnType.split('_')
            prevPos = int(rxnSpl[-1])
            prevPosStr = rxnSpl[-1]

            #scan
            if( 
                rxnType == f'scan_{prevPosStr}'
                or rxnType == f'scan_from_scan_collision_{prevPosStr}'
                or rxnType == f'scan_from_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base,tc=1))
                prevSSUs.append(SSU(x=prevPos+1,y=ssu_y_base,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #backward_scan
            if(
                rxnType == f'backward_scan_{prevPosStr}'
                or rxnType == f'backward_scan_from_scan_collision_{prevPosStr}'
                or rxnType == f'backward_scan_from_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base,tc=1))
                prevSSUs.append(SSU(x=prevPos-1,y=ssu_y_base,tc=1))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #scan_to_elongate
            if( 
                rxnType == f'scan_to_elongate_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_leading_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_scan_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base,tc=1))
                prevLSUs.remove(LSU(x=-1,y=ssu_y_base))
                prevSSUs.append(SSU(x=prevPos,y=ssu_y_up,tc=0))
                prevLSUs.append(LSU(x=prevPos,y=lsu_y_down))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #elongate
            if( 
                rxnType == f'elongate_{prevPosStr}'
                or rxnType == f'elongate_from_scan_collision_{prevPosStr}'
                or rxnType == f'elongate_from_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up,tc=0))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=prevPos+3,y=ssu_y_up,tc=0))
                prevLSUs.append(LSU(x=prevPos+3,y=lsu_y_down))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #terminate - ssu.lsu.mrna -> lsu + ssu.mrna
            if rxnType == f'terminate_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up,tc=0))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=prevPos,y=ssu_y_base,tc=0))
                prevLSUs.append(LSU(x=-1,y=0.5))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #recycle - ssu.mrna -> ssu + mrna
            if( 
                rxnType == f'recycle_{prevPosStr}'
                or rxnType == f'recycle_from_trailing_collision_{prevPosStr}'
                or rxnType == f'recycle_from_leading_collision_{prevPosStr}'
                or rxnType == f'recycle_from_both_collision_{prevPosStr}'
                or rxnType == f'scan_terminate_no_hit_{prevPosStr}'
                or rxnType == f'scan_terminate_from_scan_collision_3_hit_{prevPosStr}'
                or rxnType == f'scan_terminate_from_scan_collision_5_hit_{prevPosStr}'
                or rxnType == f'scan_terminate_from_elongation_collision_3_hit_{prevPosStr}'
                or rxnType == f'scan_terminate_from_elongation_collision_5_hit_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_scanning_scanning_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_elongating_scanning_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_scanning_elongating_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_elongating_elongating_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base,tc=0))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base,tc=0))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue
            
            #recycle part 2 - ssu.tc.mrna -> ssu + tc + mrna
            if(
                rxnType == f'scan_terminate_no_hit_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_scan_collision_3_hit_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_scan_collision_5_hit_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_elongation_collision_3_hit_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_elongation_collision_5_hit_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_scanning_scanning_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_elongating_scanning_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_scanning_elongating_tc_ejects_{prevPosStr}'
                or rxnType == f'scan_terminate_from_collision_both_hit_elongating_elongating_tc_ejects_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base,tc=1))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base,tc=0))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #fancy termination - ssu.lsu.mrna -> ssu + lsu + mrna
            if rxnType == f'elong_preterm_no_hit_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up,tc=0))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base,tc=0))
                prevLSUs.append(LSU(x=-1,y=0.5))
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #trivial collisions
            if( 
                rxnType == f'collide_upon_scanning_{prevPosStr}'
                or rxnType == f'collide_upon_backward_scanning_{prevPosStr}'
                or rxnType == f'collide_upon_elongation_{prevPosStr}'
            ):
                stateList.append(State(time,prevSSUs,prevLSUs))
                continue

            #TODO add tc as a separate object
            #TODO add ssu.lsu binding sites pointing to each other
            #L = LSU(x=pos); S = SSU(x=pos); L.isbi = S; S.isbi = L
            #Confirm pointer by id(L.isbi) == id(S) and id(S.isbi) == id(L)

        return stateList
    
    def get_state(self,t):
        times = self.firings['time'].to_numpy()
        ind = np.digitize(t,times)
        state_ind = ind-1 if (t - times[ind-1]) < times[ind] - t else ind
        return self.states[state_ind]

if __name__ == '__main__':
    LH = LogicHandler('model_1.rxns_mod.tsv')
    
    #This kinda blows up the terminal because it lists all 100 SSUs and LSUs for every state
    #for i in LH.states:
    #    print(i)