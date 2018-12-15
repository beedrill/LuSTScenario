import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt

MAX_TIME = 86316
def get_carflow_by_direction(filename, resolution):
    carflow = {
            'south_in': [0 for i in range(0, 1+int(MAX_TIME/resolution))],
            'west_in': [0 for i in range(0, 1+int(MAX_TIME/resolution))],
            'east_in': [0 for i in range(0, 1+int(MAX_TIME/resolution))],
            'north_in': [0 for i in range(0, 1+int(MAX_TIME/resolution))]
            }
    tree = ET.parse(filename)
    root = tree.getroot()
    for v in root.findall('vehicle'):
        t = int(float(v.attrib['depart']))
        index = int(t/resolution)
        source = v.findall('route')[0].attrib['edges'].split()[0]
        #print(source)
        #if  not index in carflow[source].keys():
        carflow[source][index] += 1
        
    return carflow
      
def plot_flow(carflow):
    for source in carflow.keys():
        plt.plot(carflow[source])
        
if __name__ == '__main__':
    carflow = get_carflow_by_direction('traffic.rou.xml', 300)
    plot_flow(carflow)
    plt.show()