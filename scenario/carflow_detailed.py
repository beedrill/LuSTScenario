# -*- coding: utf-8 -*-
import pickle
import os, sys, subprocess
if 'SUMO_HOME' in os.environ:
 tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
 sys.path.append(tools)
else:
 sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"
#sumoCmd = [sumoBinary, "-c", "dua.static.sumocfg"]

import traci

roads = ['--31272#7', '-30892#16', '-31272#6', '--30892#17', '-31272#7', '--30892#16', '--31272#6', '-30892#17', '-30872#10', '--31272#8', '--30872#11', '--30892#18', '-31320#0', '-31272#5', '-30722']

v_id_list =[]
v_list = {}

class Vehicle():
    def __init__(self, vid, vtype, time):
        self.vid = vid
        self.vtype=vtype
        #self.vfrom = vfrom
        self.time = time
        self.route = []

sumoProcess = subprocess.Popen("%s %s" % (sumoBinary, "due.static.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(port=8813, numRetries=10, host='localhost', label='default')


while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    for e in roads:
        for vid in traci.edge.getLastStepVehicleIDs(e):
            if not vid in v_id_list:
                v_id_list.append(vid)
                v_list[vid] = Vehicle(vid,traci.vehicle.getTypeID(vid), traci.simulation.getCurrentTime())

            if not e in v_list[vid].route:
                v_list[vid].route.append(e)

with open('vehicles.pkl', 'wb') as f:
    pickle.dump(v_list, f, pickle.HIGHEST_PROTOCOL)
#print(carflow)
f.close()
#use this to read from saved file:
with open('vehicles.pkl','rb') as f:
    carflow = pickle.load(f)
    print(carflow)
