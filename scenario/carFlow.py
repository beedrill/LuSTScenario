import os, sys, subprocess
if 'SUMO_HOME' in os.environ:
 tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
 sys.path.append(tools)
else:
 sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"
#sumoCmd = [sumoBinary, "-c", "dua.static.sumocfg"]

import traci

#west north east south
#from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
#to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']
##for intersection 22640

from_edge = ['-31496#9', '-32776#8', '--31496#10', '--32776#9']
to_edge = ['--31496#9', '--32776#8', '-31496#10', '-32776#9']
v_list = {}
v_id_list =[]

class Vehicle():
    def __init__(self, vid, vtype, vfrom, time):
        self.vid = vid
        self.vtype=vtype
        self.vfrom = vfrom
        self.time = time


sumoProcess = subprocess.Popen("%s %s" % (sumoBinary, "dua.static.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(port=8813, numRetries=10, host='localhost', label='default')


while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    for e in from_edge:
        for vid in traci.edge.getLastStepVehicleIDs(e):
            if not vid in v_id_list:
                v_id_list.append(vid)
                v_list[vid] = Vehicle(vid,traci.vehicle.getTypeID(vid), e, traci.simulation.getCurrentTime())

    for e in to_edge:
        for vid in traci.edge.getLastStepVehicleIDs(e):
            if vid in v_id_list:
                v_list[vid].vto=e

f = open('result.txt', 'w')
for vid in v_id_list:
    v = v_list[vid]
    if hasattr(v,'vto')==False:
        print('warning: vehicle {} has no vto'.format(v.vid))
        continue
    f.write('{}\t{}\t{}\t{}\t{}\n'.format(v.vid,v.vtype,v.vfrom,v.vto,v.time))
f.close()

traci.close()
