import numpy as np 
import time
import sys
import requests
import json
import csv

reqData = {
    "data": {
        "nodes": [7,8,9,10,21,22],
    }
}

headers = {'content-type': 'application/json'}
try:
    jsonData = (json.dumps(reqData)).encode("utf-8")
except:
    logging.warn("Malformed json")
result = requests.post("http://172.17.0.1:7070/set/nodes/data_nodes/", data=jsonData, headers=headers)
