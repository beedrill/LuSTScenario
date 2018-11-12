import pickle

f = open('result.txt', 'r')
line = f.readline()
#west, north, east, south
from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']
vtype = ["passenger1","passenger2a","passenger2b","passenger3","passenger4","passenger5", "bus"]

carflow = {}
for idx_fr, fr_e in enumerate(from_edge):
    carflow[fr_e] = {}
    for idx_to, to_e in enumerate(to_edge):
        #if idx_fr == idx_to:
        #    continue
        carflow[fr_e][to_e] = {}
        for vt in vtype:
            carflow[fr_e][to_e][vt] = [0 for i in range(0,24)]


while line:
    ## here add stuffs
    temp = line.split()
    vid = temp[0]
    vtype = temp[1]
    vfrom = temp[2]
    vto = temp[3]
    time = temp[4]
    time = int(time)/1000
    if time<1824:
        index = 0;
    elif time>88223:
        index = 23;
    else:
        index = int((time-1824)/3600)
    #print('from edge:', vfrom, 'to edge:', vto)
    carflow[vfrom][vto][vtype][index] += 1

    line=f.readline()
with open('carflow.pkl', 'wb') as f:
    pickle.dump(carflow, f, pickle.HIGHEST_PROTOCOL)
print(carflow)
f.close()
