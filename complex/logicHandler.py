import copy as cp
import pandas as pd
import numpy as np
from alive_progress import alive_bar
from state import State
from mrna import MRNA
from smallsubunit import SSU
from ternarycomplex import TC
from largesubunit import LSU
from effect import Effect

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
        ssu_y_up = 0.55
        tc_y_base = 0.475
        lsu_y_base = 0.5
        lsu_y_down = 0.45

        #TODO remove this hardcode
        initialSSUs = 100 * [SSU(x=-1,y=ssu_y_base)]
        initialTCs = 100 * [TC(x=-1,y=tc_y_base)]
        initialLSUs = 100 * [LSU(x=-1,y=lsu_y_base)]
        initialEffects = []
        stateList = [State(0,initialSSUs,initialTCs,initialLSUs,initialEffects)]

        for i in self.firings.index:
            rxnType = self.firings['rxn'][i]
            try:
                prevSSUs = cp.copy(stateList[i].ssus)
                prevTCs = cp.copy(stateList[i].tcs)
                prevLSUs = cp.copy(stateList[i].lsus)
                prevEffs = cp.copy(stateList[i].effects)

            except IndexError:
                print(rxnType)
                print(i)
                print("couldn't parse a reaction, quitting")
                break
            time = self.firings['time'][i]
            rxnType = self.firings['rxn'][i]
            rxnSpl = rxnType.split('_')
            if rxnType != 'tc_free_ssu_binding':
                prevPos = int(rxnSpl[-1])
                prevPosStr = rxnSpl[-1]

            #remove collisions
            if ('from' in rxnType) and ('collision' in rxnType):
                #no collision lost: scan_to_elongate
                #-15 collision lost: scan, elongate, recycle_from_trailing, scan_terminate_from_scan_collision_5_hit, scan_terminate_from_elongation_collision_5_hit
                #+15 collision lost: backward_scan, recycle_from_leading, scan_terminate_from_scan_collision_3_hit, scan_terminate_from_elongation_collision_3_hit
                #+-15 collision lost: scan_terminate_from_collision_both_hit
                if(
                    rxnType == f'scan_from_scan_collision_{prevPosStr}'
                    or rxnType == f'scan_from_elongation_collision_{prevPosStr}'
                    or rxnType == f'elongate_from_scan_collision_{prevPosStr}'
                    or rxnType == f'elongate_from_elongation_collision_{prevPosStr}'
                    or 'recycle_from_trailing' in rxnType
                    or '5_hit' in rxnType
                    or 'both_hit' in rxnType
                ):
                    prevEffs.remove(Effect(x=prevPos-15,y=ssu_y_base,n='collision'))

                if(
                    rxnType == f'backward_scan_from_scan_collision_{prevPosStr}'
                    or rxnType == f'backward_scan_from_elongation_collision_{prevPosStr}'
                    or 'recycle_from_leading' in rxnType
                    or '3_hit' in rxnType
                    or 'both_hit' in rxnType
                ):
                    prevEffs.remove(Effect(x=prevPos+15,y=ssu_y_base,n='collision'))

            #tc_free_ssu_binding
            if rxnType == 'tc_free_ssu_binding':
                prevTCs.remove(TC(x=-1,y=-1))
                prevTCs.append(TC(x=-1,y=tc_y_base))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #tc_mrna_bound_ssu_binding
            if rxnType == f'tc_mrna_bound_ssu_binding_{prevPosStr}':
                prevTCs.remove(TC(x=-1,y=-1))
                prevTCs.append(TC(x=prevPos,y=tc_y_base))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #bind_cap_pic_0
            if rxnType == 'bind_cap_pic_0':
                prevSSUs.remove(SSU(x=-1,y=ssu_y_base))
                prevTCs.remove(TC(x=-1,y=tc_y_base))
                prevSSUs.append(SSU(x=0,y=ssu_y_base))
                prevTCs.append(TC(x=0,y=tc_y_base))
                if Effect(x=0,y=ssu_y_base,n='cap') not in prevEffs: # I don't think this line should be needed but it is?
                    prevEffs.append(Effect(x=0,y=ssu_y_base,n='cap',
                        ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','cap.png']))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #scan
            if( 
                rxnType == f'scan_{prevPosStr}'
                or rxnType == f'scan_from_scan_collision_{prevPosStr}'
                or rxnType == f'scan_from_elongation_collision_{prevPosStr}'
            ):
                # index, first copy, change, second copy
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base))
                prevSSUs.append(SSU(x=prevPos+1,y=ssu_y_base))
                if TC(x=prevPos,y=tc_y_base) in prevTCs:
                    prevTCs.remove(TC(x=prevPos,y=tc_y_base))
                    prevTCs.append(TC(x=prevPos+1,y=tc_y_base))
                if prevPos == 29:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #backward_scan
            if(
                rxnType == f'backward_scan_{prevPosStr}'
                or rxnType == f'backward_scan_from_scan_collision_{prevPosStr}'
                or rxnType == f'backward_scan_from_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base))
                prevSSUs.append(SSU(x=prevPos-1,y=ssu_y_base))
                if TC(x=prevPos,y=tc_y_base) in prevTCs:
                    prevTCs.remove(TC(x=prevPos,y=tc_y_base))
                    prevTCs.append(TC(x=prevPos-1,y=tc_y_base))
                if prevPos == 30:
                    prevEffs.append(Effect(x=0,y=ssu_y_base,n='cap',
                     ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','cap.png']))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #scan_to_elongate
            if( 
                rxnType == f'scan_to_elongate_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_leading_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_scan_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base))
                prevTCs.remove(TC(x=prevPos,y=tc_y_base))
                prevLSUs.remove(LSU(x=-1,y=ssu_y_base))
                prevSSUs.append(SSU(x=prevPos,y=ssu_y_up))
                prevTCs.append(TC(x=-1,y=-1))
                prevLSUs.append(LSU(x=prevPos,y=lsu_y_down))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #elongate
            if( 
                rxnType == f'elongate_{prevPosStr}'
                or rxnType == f'elongate_from_scan_collision_{prevPosStr}'
                or rxnType == f'elongate_from_elongation_collision_{prevPosStr}'
            ):
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=prevPos+3,y=ssu_y_up))
                prevLSUs.append(LSU(x=prevPos+3,y=lsu_y_down))
                if prevPos >= 27 and prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #terminate - ssu.lsu.mrna -> lsu + ssu.mrna
            if rxnType == f'terminate_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=prevPos,y=ssu_y_base))
                prevLSUs.append(LSU(x=-1,y=lsu_y_base))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
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
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base))
                if prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
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
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_base))
                prevTCs.remove(TC(x=prevPos,y=tc_y_base))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base))
                prevTCs.append(TC(x=-1,y=-1))
                if prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #fancy termination - ssu.lsu.mrna -> ssu + lsu + mrna
            if rxnType == f'elong_preterm_no_hit_{prevPosStr}':
                prevSSUs.remove(SSU(x=prevPos,y=ssu_y_up))
                prevLSUs.remove(LSU(x=prevPos,y=lsu_y_down))
                prevSSUs.append(SSU(x=-1,y=ssu_y_base))
                prevLSUs.append(LSU(x=-1,y=lsu_y_base))
                if prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #collisions
            if 'collide' in rxnType:
                if 'backward' in rxnType:
                    prevEffs.append(Effect(x=prevPos-15,y=ssu_y_base,n='collision',
                        ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','star.png']))
                else:
                    prevEffs.append(Effect(x=prevPos+15,y=ssu_y_base,n='collision',
                        ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','star.png']))
                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #TODO add ssu.lsu binding sites pointing to each other
            #L = LSU(x=pos); S = SSU(x=pos); L.isbi = S; S.isbi = L
            #Confirm pointer by id(L.isbi) == id(S) and id(S.isbi) == id(L)

        return stateList
    
    def get_state(self,t):
        times = self.firings['time'].to_numpy()
        ind = np.digitize(t,times)
        state_ind = ind-1 if (t - times[ind-1]) < times[ind] - t else ind
        return self.states[state_ind]

    def get_states_from_array(self,time_arr):
        frames = []
        with alive_bar(len(time_arr)) as bar:
            for itime, time in enumerate(time_arr):
                # get the state you want to plot
                S = LH.get_state(time)
                frames.append(S)
                # advance the bar
                bar()
        return frames


if __name__ == '__main__':
    LH = LogicHandler('model_1.rxns_mod.tsv')
    
    #This kinda blows up the terminal because it lists all 100 SSUs and LSUs for every state
    #for i in LH.states:
    #    print(i)