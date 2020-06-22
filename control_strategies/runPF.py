from pypower.api import *
from pypower.ext2int import ext2int
from pypower.idx_brch import F_BUS, T_BUS, TAP, BR_R, BR_X, BR_B, RATE_A, PF, QF, PT, QT
from pypower.idx_bus import BUS_TYPE, REF, PD, QD, VM, VA, VMAX, VMIN
from pypower.idx_gen import GEN_BUS, PG, QG, PMAX, PMIN, QMAX, QMIN, VG
from pypower.int2ext import int2ext
import numpy as np
from pypower.ppoption import ppoption
import csv
import os


class runPF:

    def __init__(self, name, profiles):
        # Input Data
        # =============================================================
        self.ppc = name
        self.pvproduction = profiles[0]
        self.demandprofile_P = profiles[1]

        # Problem parameters
        # =============================================================
        self.nb = 0.0
        self.ng = 0.0
        self.c = []

        self.q = []
        self.v_gen = [0.0]

        self.t = []

        self.bus = []
        self.gen = []
        self.baseMVA = 0.0
        self.branch = []
        self.pcc = 0.0


    def system_info(self):
        self.ppc = ext2int(self.ppc)      # convert to continuous indexing starting from 0
        BUS_TYPE = 1

        # Gather information about the system
        # =============================================================
        self.baseMVA, self.bus, self.gen, self.branch, cost, VMAX, VMIN = \
            self.ppc["baseMVA"], self.ppc["bus"], self.ppc["gen"], self.ppc["branch"], self.ppc["gencost"], self.ppc["VMAX"], self.ppc["VMIN"]

        self.nb = self.bus.shape[0]                        # number of buses
        self.ng = self.gen.shape[0]                        # number of generators
        self.nbr = self.branch.shape[0]                    # number of branches

        for i in range(int(self.nb)):
            if self.bus[i][BUS_TYPE] == 3.0:
                self.pcc = i
            else:
                pass
        
        for i in range(self.ng):                           # list of microgenerators
            if self.gen[i][0] == self.pcc:
                pass
            else:
                self.c.append(self.gen[i][0])
        print("Number of Reactive Power Compensator = ",int(len(self.c)))
               
        # initialize vectors
        # =====================================================================
        self.q = [0.0] * int(len(self.c))
        self.p = []

        return [self.bus, self.baseMVA, self.branch, self.pcc, self.nb,self.ng,self.nbr, self.c]


    def run_Power_Flow(self,k, pv_production, reactive_power, active_power_battery, P_load, active_power_PV):
        self.k = k  # iterations
        self.pvproduction = pv_production
        self.v_gen = []
        self.v_bat = []
        self.q = reactive_power
        self.p_batt_array = active_power_battery
        self.P_load = P_load
        self.p = []
        self.p_PV = active_power_PV

        ############## SET THE ACTUAL LOAD AND GEN VALUES ###############-+
        for i in range(int(self.nb)-1):
            self.bus[i][PD] = self.P_load[k][i] - self.p_batt_array[i]
            self.bus[i][QD] = 0.0

        for i in range(int(len(self.c))):
            self.gen[i+1][QG] = self.q[i]
            self.gen[i+1][PG] = self.pvproduction[k][i] + self.p_PV[i]

        self.ppc['bus'] = self.bus
        self.ppc['gen'] = self.gen
        ppc = int2ext(self.ppc)


        ############# RUN PF ########################
        opt = ppoption(VERBOSE=0, OUT_ALL=0, UT_SYS_SUM=0)
        results = runpf(ppc, opt)
        bus_results = results[0]['bus']

        for i in range(int(len(self.c))):
            self.v_gen.append(bus_results[int(self.c[i])][VM])
            self.p.append(self.gen[i][PG])
        
        return self.v_gen, self.p, self.q, self.p_batt_array, bus_results[:,VM]