import numpy as np 
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
    "voltage_node" : []
}

voltage_dict = {}
active_power_dict = {}

# add the simulation dictionary to mmu object
dmuObj.addElm("simDict", simDict)
dmuObj.addElm("voltage_dict", voltage_dict)
dmuObj.addElm("active_power_dict", active_power_dict)

########################################################################################################
#########################  Section for Receiving Signal  ###############################################
########################################################################################################

def voltage_input(data,  *args):
    voltage_dict = {}  
    dmuObj.setDataSubset(data,"voltage_dict")

def api_cntr_input(data,  *args):
    
    tmpData = []
    logging.debug("RECEIVED EXTERNAL CONTROL")
    logging.debug(data)       
    dmuObj.setDataSubset(data,"simDict", "active_nodes")

# Receive from external Control
dmuObj.addElm("nodes", dict_ext_cntr)
dmuObj.addRx(api_cntr_input, "nodes", "data_nodes")

# Receive voltage
dmuObj.addElm("voltage", simDict)
dmuObj.addRx(voltage_input, "voltage", "voltage_node")

########################################################################################################
#########################  Section for Sending Signal  #################################################
########################################################################################################

def control_output(data, *args):

    reqData = {}
    reqData["data"] =  data
    logging.debug("##DATA##")
    logging.debug(data)
    headers = {'content-type': 'application/json'}
    try:
        jsonData = (json.dumps(reqData)).encode("utf-8")
    except:
        logging.warn("Malformed json")
    for key in data.keys():
        if key == "active_power":
            result = requests.post("http://powerflow:8000/set/active_power/active_power_control/", data=jsonData, headers=headers)

dmuObj.addRx(control_output,"active_power_dict")


try:
    while True:
        active_power_dict = {}
        voltage_value = dmuObj.getDataSubset("voltage_dict")
        voltage_meas = voltage_value.get("voltage_measurements", None)
        logging.debug("voltage received")
        logging.debug(voltage_meas)

        if voltage_value:
            active_power = [1.0]*len(list(voltage_meas.values()))            
            k = 0
            for key in voltage_meas.keys():
                active_power_dict[key] = active_power[k]
                k+=1
            dmuObj.setDataSubset({"active_power":active_power_dict},"active_power_dict")
        else:
            pass

        time.sleep(1.0)

except (KeyboardInterrupt, SystemExit):
    print('simulation finished')

