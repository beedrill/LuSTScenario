import pickle
import xml.etree.cElementTree as ET
with open('carflow.pkl','rb') as f:
    carflow = pickle.load(f)
#print(carflow)
#west, north, east, south
from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
from_edge_new = ['west_in','north_in','east_in', 'south_in']
to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']
to_edge_new = ['west_out','north_out','east_out', 'south_out']
vtype = ["passenger1","passenger2a","passenger2b","passenger3","passenger4","passenger5", "bus"]
def generateRoute(name, hour):
    routes = ET.Element('routes')
    vtype1 = ET.SubElement(routes,'vType',
        vClass="passenger",
        id="passenger1",
        color=".8,.2,.2",
        accel="2.6",
        decel="4.5",
        sigma="0.5",
        length="5.0",
        minGap="1.5",
        maxSpeed="70",
        guiShape="passenger/sedan")

    vtype2a = ET.SubElement(routes,'vType',
        vClass="passenger",
        id="passenger2a",
        color=".8,.8,.8",
        accel="3.0",
        decel="4.5",
        sigma="0.5",
        length="4.5",
        minGap="1.5",
        maxSpeed="50",
        guiShape="passenger/hatchback")

    vtype2b = ET.SubElement(routes, 'vType',
        vClass="passenger",
        id="passenger2b",
        color=".2,.2,.8",
        accel="2.8",
        decel="4.5",
        sigma="0.5",
        length="4.5",
        minGap="1.0",
        maxSpeed="50",
        guiShape="passenger/hatchback")

    vtype3 = ET.SubElement(routes, 'vType',
        vClass="passenger",
        id="passenger3",
        color=".3,.3,.3",
        accel="2.7",
        decel="4.5",
        sigma="0.5",
        length="6.0",
        minGap="1.5",
        maxSpeed="70",
        guiShape="passenger/wagon")

    vtype4 = ET.SubElement(routes, 'vType',
        vClass="passenger",
        id="passenger4",
        color=".9,.9,.9",
        accel="2.4",
        decel="4.5",
        sigma="0.5",
        length="5.5",
        minGap="1.5",
        maxSpeed="30",
        guiShape="passenger/van")

    vtype5 = ET.SubElement(routes, 'vType',
        vClass="passenger",
        id="passenger5",
        color=".8,.8,.0",
        accel="2.3",
        decel="4.5",
        sigma="0.5",
        length="7.0",
        minGap="2.5",
        maxSpeed="30",
        guiShape="delivery")

    vtypebus = ET.SubElement(routes, 'vType',
        vClass="bus",
        id="bus",
        accel="2.6",
        decel="4.5",
        sigma="0.5",
        length="12.0",
        minGap="3",
        maxSpeed="30",
        guiShape="bus")
        #####generate routes:
    denominator = 3600+1824 if hour == 0 else 3600
    for index_in, (fr_e,fr_e_n) in enumerate(zip(from_edge, from_edge_new)):
        for index_out, (to_e,to_e_n) in enumerate(zip(to_edge, to_edge_new)):
            if index_in == index_out:
                continue
            ET.SubElement(routes, 'route', id="{}_{}".format(fr_e_n,to_e_n), edges = fr_e_n+' '+to_e_n)


    for index_in, (fr_e,fr_e_n) in enumerate(zip(from_edge, from_edge_new)):
        for index_out, (to_e,to_e_n) in enumerate(zip(to_edge, to_edge_new)):
            if index_in == index_out:
                continue
            for vt in vtype:
                if carflow[fr_e][to_e][vt][hour] == 0:
                    prob = 0.00001
                else:
                    prob = float(carflow[fr_e][to_e][vt][hour])/denominator
                ET.SubElement(routes, 'flow',
                    id="flow_{}_{}_{}".format(fr_e_n,to_e_n,vt),
                    type=vt,
                    route="{}_{}".format(fr_e_n,to_e_n),
                    probability=str(prob),
                    depart="1",
                    begin = "0",
                    end = "3600")

    tree = ET.ElementTree(routes)
    tree.write("{}.rou.xml".format(name))

if __name__=='__main__':
    folder = 'whole-day-training-flow-LuST-12408'
    for hour in range(0,24):
        generateRoute(folder+'/traffic-{}'.format(hour), hour)
