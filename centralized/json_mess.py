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
# add the simulation dictionary to mmu object
dmuObj.addElm("simDict", simDict)
dmuObj.addElm("voltage_dict", voltage_dict)

########################################################################################################
#########################  Section for Receiving Signal  ###############################################
########################################################################################################

def voltage_input(data,  *args):
    voltage_dict = {}  
    dmuObj.setDataSubset(data,"voltage_dict")
    logging.debug("voltage received")
    logging.debug(data)

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

try:
    while True:
        voltage_value = dmuObj.getDataSubset("voltage_dict")
        
        time.sleep(1.0)
except (KeyboardInterrupt, SystemExit):
    print('simulation finished')

