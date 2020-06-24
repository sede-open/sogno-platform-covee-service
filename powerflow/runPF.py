from pypower.api import *
from pypower.ext2int import ext2int
from pypower.idx_brch import F_BUS, T_BUS, TAP, BR_R, BR_X, BR_B, RATE_A, PF, QF, PT, QT
from pypower.idx_bus import BUS_TYPE, REF, PD, QD, VM, VA, VMAX, VMIN
from pypower.idx_gen import GEN_BUS, PG, QG, PMAX, PMIN, QMAX, QMIN, VG
from pypower.int2ext import int2ext

from cases.case_10_nodes import case_10_nodes
from csv_files.read_profiles import read_profiles

import numpy as np
from pypower.ppoption import ppoption
import csv
import os
import coloredlogs, logging, threading
from threading import Thread
from submodules.dmu.dmu import dmu
from submodules.dmu.httpSrv import httpSrv
import time
import sys
import requests
import json
import csv
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--ext_port', nargs='*', required=True)
args = vars(parser.parse_args())
ext_port = args['ext_port'][0]


coloredlogs.install(level='DEBUG',
fmt='%(asctime)s %(levelname)-8s %(name)s[%(process)d] %(message)s',
field_styles=dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', bold=True),
    programname=dict(color='cyan'),
    name=dict(color='blue')))
logging.info("Program Start")


def initialize( name, profiles):
    # Input Data
    # =============================================================
    ppc = name
    pvproduction = profiles[0]
    demandprofile_P = profiles[1]

def run_Power_Flow(ppc, active_nodes):

    ppc = ext2int(ppc)      # convert to continuous indexing starting from 0
    BUS_TYPE = 1

    # Gather information about the system
    # =============================================================
    baseMVA, bus, gen, branch, cost, VMAX, VMIN = \
        ppc["baseMVA"], ppc["bus"], ppc["gen"], ppc["branch"], ppc["gencost"], ppc["VMAX"], ppc["VMIN"]

    nb = bus.shape[0]                        # number of buses
    ng = gen.shape[0]                        # number of generators
    nbr = branch.shape[0]                    # number of branches

    for i in range(int(nb)):
        if bus[i][BUS_TYPE] == 3.0:
            pcc = i
        else:
            pass

    c = active_nodes
    for i in range(1,ng):
        if gen[i][0] in c:
            pass
        else:
            np.delete(ppc["gen"],(i),axis=0)       

    print("Number of Reactive Power Compensator = ",int(len(c)))
            
    # initialize vectors
    # =====================================================================
    q = [0.0] * int(len(c))
    p = []
    v_gen = []

    ############## SET THE ACTUAL LOAD AND GEN VALUES ###############-+
    for i in range(int(nb)-1):
        bus[i][PD] = 0.3 #- p_batt_array[i]
        bus[i][QD] = 0.0

    for i in range(int(len(c))):
        gen[i+1][QG] = 0.0#q[i]
        gen[i+1][PG] = 1.0 #+ p_PV[i]

    ppc['bus'] = bus
    ppc['gen'] = gen
    ppc = int2ext(ppc)


    ############# RUN PF ########################
    opt = ppoption(VERBOSE=0, OUT_ALL=0, UT_SYS_SUM=0)
    results = runpf(ppc, opt)
    bus_results = results[0]['bus']

    for i in range(int(len(c))):
        v_gen.append(bus_results[int(c[i]-1)][VM])
        p.append(gen[i+1][PG])
    
    return v_gen,p,c


############################ Start the Server #######################################################

''' Initialize objects '''
dmuObj = dmu()

''' Start http server '''
httpSrvThread1 = threading.Thread(name='httpSrv',target=httpSrv, args=("0.0.0.0", 8000 ,dmuObj,))
httpSrvThread1.start()

httpSrvThread2 = threading.Thread(name='httpSrv',target=httpSrv, args=("0.0.0.0", int(ext_port) ,dmuObj,))
httpSrvThread2.start()
time.sleep(2.0)
#######################################################################################################


########################################################################################################
#########################  Section for Defining the Dictionaries  ######################################
########################################################################################################

dict_ext_cntr = {
    "data_cntr" : [],
    "data_nodes" : []
}

simDict = {
    "active_nodes" : [],
    "output_voltage": []
}

voltage_dict = {}

# add the simulation dictionary to mmu object
dmuObj.addElm("simDict", simDict)
dmuObj.addElm("voltage_dict", voltage_dict)


########################################################################################################
#########################  Section for Receiving Signal  ###############################################
########################################################################################################

def ext_cntr_input(data,  *args):
    
    tmpData = []
    for key in data.keys():
        value = data[key][0]
        tmpData.append(value)        
        dmuObj.setDataSubset(value,"dataDict", key)

def api_cntr_input(data,  *args):
    
    tmpData = []
    logging.debug("RECEIVED EXTERNAL CONTROL")
    logging.debug(data)       
    dmuObj.setDataSubset(data,"simDict", "active_nodes")

# Receive from external Control
dmuObj.addElm("nodes", dict_ext_cntr)
dmuObj.addRx(api_cntr_input, "nodes", "data_nodes")

########################################################################################################
#########################  Section for Sending Signal  #################################################
########################################################################################################

def measurement_output(data, *args):

    reqData = {}
    reqData["data"] =  data
    logging.debug("voltage sent")
    logging.debug(data)

    headers = {'content-type': 'application/json'}
    try:
        jsonData = (json.dumps(reqData)).encode("utf-8")
    except:
        logging.warn("Malformed json")
    result = requests.post("http://centralized:8000/set/voltage/voltage_node/", data=jsonData, headers=headers)

dmuObj.addRx(measurement_output,"voltage_dict")




# read profiles from CSV files
# =======================================================================
profiles = read_profiles()
[PV_list, P_load_list] = profiles.read_csv()

ppc = case_10_nodes()
initialize(ppc, [PV_list, P_load_list])

try:
    while True:
        voltage_dict = {}
        active_nodes = dmuObj.getDataSubset("simDict","active_nodes")
        if not active_nodes:
            logging.debug("no input received")
            active_nodes = list(np.array(np.matrix(ppc["gen"])[:,0]).flatten())
            active_nodes = active_nodes[1:len(active_nodes)]
        else:
            active_nodes = list(active_nodes.values())[0]
        logging.debug("active nodes")
        logging.debug(active_nodes)

        [v_gen,p,c] = run_Power_Flow(ppc,active_nodes)
        # logging.debug("v_gen, p, c")
        # logging.debug([v_gen,p,c])
               
        for i in range(len(c)):
            voltage_dict["output_voltage_node_"+str(active_nodes[i])] = v_gen[i]
        dmuObj.setDataSubset(voltage_dict,"voltage_dict")


        time.sleep(1.0)
except (KeyboardInterrupt, SystemExit):
    print('simulation finished')