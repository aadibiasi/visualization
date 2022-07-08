import copy as cp
import pandas as pd
import numpy as np
from alive_progress import alive_bar
from change import Change
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
        self.changes = []
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
    def changes(self):
        return self._changes

    @changes.setter
    def changes(self, newChanges):
        self._changes = newChanges

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
        initialSSUs = [SSU(x=-1,y=ssu_y_base) for i in range(100)]
        initialTCs = [TC(x=-1,y=tc_y_base) for i in range(100)]
        initialLSUs = [LSU(x=-1,y=lsu_y_base) for i in range(100)]
        initialEffects = []
        stateList = [State(0,initialSSUs,initialTCs,initialLSUs,initialEffects)]

        for i in self.firings.index:
            # import ipdb;ipdb.set_trace()
            rxnType = self.firings['rxn'][i]
            try:
                prevSSUs = cp.deepcopy(stateList[i].ssus)
                prevTCs = cp.deepcopy(stateList[i].tcs)
                prevLSUs = cp.deepcopy(stateList[i].lsus)
                prevEffs = cp.deepcopy(stateList[i].effects)

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
                # TCs
                ind = prevTCs.index(TC(x=-1,y=-1))
                beforeTC = cp.copy(prevTCs[ind])
                prevTCs[ind].ypos = tc_y_base
                prevTCs[ind].last_time_modified = time
                afterTC = cp.copy(prevTCs[ind])
                self.changes.append(Change(beforeTC,afterTC))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #tc_mrna_bound_ssu_binding
            if rxnType == f'tc_mrna_bound_ssu_binding_{prevPosStr}':
                # TCs
                ind = prevTCs.index(TC(x=-1,y=-1))
                beforeTC = cp.copy(prevTCs[ind])
                prevTCs[ind].xpos = prevPos
                prevTCs[ind].ypos = tc_y_base
                prevTCs[ind].last_time_modified = time
                afterTC = cp.copy(prevTCs[ind])
                self.changes.append(Change(beforeTC,afterTC))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #bind_cap_pic_0
            if rxnType == 'bind_cap_pic_0':
                # SSUs
                ind = prevSSUs.index(SSU(x=-1,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos = 0
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # TCs
                ind = prevTCs.index(TC(x=-1,y=tc_y_base))
                beforeTC = cp.copy(prevTCs[ind])
                prevTCs[ind].xpos = 0
                prevTCs[ind].last_time_modified = time
                afterTC = cp.copy(prevTCs[ind])
                self.changes.append(Change(beforeTC,afterTC))

                # Effects
                if Effect(x=0,y=ssu_y_base,n='cap') not in prevEffs: # I don't think this line should be needed but it is?
                    prevEffs.append(Effect(x=0,y=ssu_y_base,n='cap',
                        ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','cap.png']))
                        #ip=['C:\\','Users','Akhlore','visualization','complex','cap.png']))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #scan
            if( 
                rxnType == f'scan_{prevPosStr}'
                or rxnType == f'scan_from_scan_collision_{prevPosStr}'
                or rxnType == f'scan_from_elongation_collision_{prevPosStr}'
            ):
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos += 1
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # TCs
                if TC(x=prevPos,y=tc_y_base) in prevTCs:
                    ind = prevTCs.index(TC(x=prevPos,y=tc_y_base))
                    beforeTC = cp.copy(prevTCs[ind])
                    prevTCs[ind].xpos += 1
                    prevTCs[ind].last_time_modified = time
                    afterTC = cp.copy(prevTCs[ind])
                    self.changes.append(Change(beforeTC,afterTC))

                # Effects
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
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos -= 1
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # TCs
                if TC(x=prevPos,y=tc_y_base) in prevTCs:
                    ind = prevTCs.index(TC(x=prevPos,y=tc_y_base))
                    beforeTC = cp.copy(prevTCs[ind])
                    prevTCs[ind].xpos -= 1
                    prevTCs[ind].last_time_modified = time
                    afterTC = cp.copy(prevTCs[ind])
                    self.changes.append(Change(beforeTC,afterTC))

                # Effects
                if prevPos == 30:
                    prevEffs.append(Effect(x=0,y=ssu_y_base,n='cap',
                    ip=['C:\\','Users','alexd','Documents','faeder','visualization','complex','cap.png']))
                    #ip=['C:\\','Users','Akhlore','visualization','complex','cap.png']))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #scan_to_elongate
            if( 
                rxnType == f'scan_to_elongate_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_leading_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_scan_collision_{prevPosStr}'
                or rxnType == f'scan_to_elongate_from_trailing_elongation_collision_{prevPosStr}'
            ):
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].ypos = ssu_y_up
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # TCs
                ind = prevTCs.index(TC(x=prevPos,y=tc_y_base))
                beforeTC = cp.copy(prevTCs[ind])
                prevTCs[ind].xpos = -1
                prevTCs[ind].ypos = -1
                prevTCs[ind].last_time_modified = time
                afterTC = cp.copy(prevTCs[ind])
                self.changes.append(Change(beforeTC,afterTC))

                # LSUs
                ind = prevLSUs.index(LSU(x=-1,y=lsu_y_base))
                beforeLSU = cp.copy(prevLSUs[ind])
                prevLSUs[ind].xpos = prevPos
                prevLSUs[ind].ypos = lsu_y_down
                prevLSUs[ind].last_time_modified = time
                afterLSU = cp.copy(prevLSUs[ind])
                self.changes.append(Change(beforeLSU,afterLSU))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #elongate
            if( 
                rxnType == f'elongate_{prevPosStr}'
                or rxnType == f'elongate_from_scan_collision_{prevPosStr}'
                or rxnType == f'elongate_from_elongation_collision_{prevPosStr}'
            ):
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_up))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos += 3
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # LSUs
                ind = prevLSUs.index(LSU(x=prevPos,y=lsu_y_down))
                beforeLSU = cp.copy(prevLSUs[ind])
                prevLSUs[ind].xpos += 3
                prevLSUs[ind].last_time_modified = time
                afterLSU = cp.copy(prevLSUs[ind])
                self.changes.append(Change(beforeLSU,afterLSU))

                # Effects
                if prevPos >= 27 and prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #terminate - ssu.lsu.mrna -> lsu + ssu.mrna
            if rxnType == f'terminate_{prevPosStr}':
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_up))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].ypos = ssu_y_base
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # LSUs
                ind = prevLSUs.index(LSU(x=prevPos,y=lsu_y_down))
                beforeLSU = cp.copy(prevLSUs[ind])
                prevLSUs[ind].xpos = -1
                prevLSUs[ind].ypos = lsu_y_base
                prevLSUs[ind].last_time_modified = time
                afterLSU = cp.copy(prevLSUs[ind])
                self.changes.append(Change(beforeLSU,afterLSU))

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
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos = -1
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # Effects
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
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_base))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos = -1
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # TCs
                ind = prevTCs.index(TC(x=prevPos,y=tc_y_base))
                beforeTC = cp.copy(prevTCs[ind])
                prevTCs[ind].xpos = -1
                prevTCs[ind].ypos = -1
                prevTCs[ind].last_time_modified = time
                afterTC = cp.copy(prevTCs[ind])
                self.changes.append(Change(beforeTC,afterTC))

                # Effects
                if prevPos < 30:
                    prevEffs.remove(Effect(x=0,y=ssu_y_base,n='cap'))

                stateList.append(State(time,prevSSUs,prevTCs,prevLSUs,prevEffs))
                continue

            #fancy termination - ssu.lsu.mrna -> ssu + lsu + mrna
            if rxnType == f'elong_preterm_no_hit_{prevPosStr}':
                # SSUs
                ind = prevSSUs.index(SSU(x=prevPos,y=ssu_y_up))
                beforeSSU = cp.copy(prevSSUs[ind])
                prevSSUs[ind].xpos = -1
                prevSSUs[ind].ypos = ssu_y_base
                prevSSUs[ind].last_time_modified = time
                afterSSU = cp.copy(prevSSUs[ind])
                self.changes.append(Change(beforeSSU,afterSSU))

                # LSUs
                ind = prevLSUs.index(LSU(x=prevPos,y=lsu_y_down))
                beforeLSU = cp.copy(prevLSUs[ind])
                prevLSUs[ind].xpos = -1
                prevLSUs[ind].ypos = lsu_y_base
                prevLSUs[ind].last_time_modified = time
                afterLSU = cp.copy(prevLSUs[ind])
                self.changes.append(Change(beforeLSU,afterLSU))

                # Effects
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
        state_ind = ind if (t - times[ind-1]) < times[ind] - t else ind
        if state_ind < 0:
            state_ind = 0
        return cp.deepcopy(self.states[state_ind])

    def get_states_from_array(self,time_arr):
        frames = []
        with alive_bar(len(time_arr)) as bar:
            for itime, time in enumerate(time_arr):
                # get the state you want to plot
                S = self.get_state(time)
                S.time = time
                frames.append(S)
                # advance the bar
                bar()
        for ichange, change in enumerate(self.changes):
            beforeObj = change.before
            beforeXPos = change.before.xpos
            beforeYPos = change.before.ypos
            beforeTime = change.before.last_time_modified
            afterObj = change.after
            afterXPos = change.after.xpos
            afterYPos = change.after.ypos
            afterTime = change.after.last_time_modified
            if isinstance(beforeObj,SSU):
                if afterXPos == -1:
                    afterXPos = beforeXPos
                    afterYPos = 1.1
            elif isinstance(beforeObj,TC):
                if beforeXPos == -1 and beforeYPos == -1 and afterXPos > -1:
                    beforeXPos = afterXPos
                    beforeYPos = 1.1
                if afterXPos == -1 and afterYPos == -1:
                    afterXPos = beforeXPos
                    afterYPos = 1.1
            else:
                if beforeXPos == -1:
                    beforeXPos = afterXPos
                    beforeYPos = -0.1
                if afterXPos == -1:
                    afterXPos = beforeXPos
                    afterYPos = -0.1
            totalXDist = afterXPos - beforeXPos
            totalYDist = afterYPos - beforeYPos
            totalTime = afterTime - beforeTime
            badStates = [S for S in frames if S.time > beforeTime and S.time < afterTime]
            for istate, state in enumerate(badStates):
                passedTime = state.time - beforeTime
                fracTime = passedTime / totalTime
                newXPos = beforeXPos + fracTime * totalXDist
                newYPos = beforeYPos + fracTime * totalYDist
                if isinstance(beforeObj,SSU):
                    badList = state.ssus
                elif isinstance(beforeObj,TC):
                    badList = state.tcs
                else:
                    badList = state.lsus
                try:
                    index = badList.index(beforeObj)
                except ValueError as e:
                    import IPython,sys;IPython.embed();sys.exit()
                badList[index].xpos = newXPos
                badList[index].ypos = newYPos
        return frames


if __name__ == '__main__':
    LH = LogicHandler('model_1_tcs.tsv')
    
    #This kinda blows up the terminal because it lists all 100 SSUs and LSUs for every state
    #for i in LH.states:
    #    print(i)