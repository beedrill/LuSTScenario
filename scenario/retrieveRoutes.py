# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']

new_edge_dict = {
        '--31272#7': 'west_in',
         '-31272#7': 'west_out',
         '-31272#6': 'east_in',
         '--31272#6': 'east_out',
         '-30892#16': 'north_in',
         '--30892#16': 'north_out',
         '--30892#17': 'south_in',
         '-30892#17': 'south_out',
         '--30892#18': 'south_south_in',
         '-31320#0': 'south_west_in',
         '--31272#8': 'west_west_in',
         '--30872#11': 'west_south_in',
         '-30872#10': 'west_north_in',
         '-31272#5': 'east_east_in',
         '-30722': 'east_north_in'
        }

def merge(tree1, tree2):
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    root1.extend(root2)
        
    return tree1
    
def get_types(tree):
    routes = tree.getroot()
    routes.insert(0,ET.Element('vType',
        vClass="passenger",
        id="passenger1",
        color=".8,.2,.2",
        accel="2.6",
        decel="4.5",
        sigma="0.5",
        length="5.0",
        minGap="1.5",
        maxSpeed="70",
        guiShape="passenger/sedan"))

    routes.insert(0,ET.Element('vType',
        vClass="passenger",
        id="passenger2a",
        color=".8,.8,.8",
        accel="3.0",
        decel="4.5",
        sigma="0.5",
        length="4.5",
        minGap="1.5",
        maxSpeed="50",
        guiShape="passenger/hatchback"))

    routes.insert(0,ET.Element('vType',
        vClass="passenger",
        id="passenger2b",
        color=".2,.2,.8",
        accel="2.8",
        decel="4.5",
        sigma="0.5",
        length="4.5",
        minGap="1.0",
        maxSpeed="50",
        guiShape="passenger/hatchback"))

    routes.insert(0,ET.Element( 'vType',
        vClass="passenger",
        id="passenger3",
        color=".3,.3,.3",
        accel="2.7",
        decel="4.5",
        sigma="0.5",
        length="6.0",
        minGap="1.5",
        maxSpeed="70",
        guiShape="passenger/wagon"))

    routes.insert(0,ET.Element('vType',
        vClass="passenger",
        id="passenger4",
        color=".9,.9,.9",
        accel="2.4",
        decel="4.5",
        sigma="0.5",
        length="5.5",
        minGap="1.5",
        maxSpeed="30",
        guiShape="passenger/van"))

    routes.insert(0,ET.Element('vType',
        vClass="passenger",
        id="passenger5",
        color=".8,.8,.0",
        accel="2.3",
        decel="4.5",
        sigma="0.5",
        length="7.0",
        minGap="2.5",
        maxSpeed="30",
        guiShape="delivery"))
    
    routes.insert(0,ET.Element('vType',
        vClass="bus",
        id="bus",
        accel="2.6",
        decel="4.5",
        sigma="0.5",
        length="12.0",
        minGap="3",
        maxSpeed="30",
        guiShape="bus"))
    return tree


def build_new_route_file(filename, tree = None):
    ##give a route file, build a new route file where vehicles go through a special intersection
    if not tree:
        tree = ET.parse(filename)
    root = tree.getroot()
    for child in root.findall('vehicle'):
        child.attrib.pop('departPos')
        #child.attrib.pop('arrivalPos')
        #print(child.tag, child.attrib)
        for r in child:
            #print(r.attrib)
            new_edges = ''
            l = 0 #use l to track how many edges are added to route
            es = r.attrib['edges'].split()
            for e in es:
                if e in from_edge and l == 0:
                    new_edges+=new_edge_dict[e]
                    l+=1
                elif e in to_edge and l == 1:
                    new_edges+=' '
                    new_edges+=new_edge_dict[e]
                    l+=1
                    
        if l == 0:
            root.remove(child)
            #print('removed a vehicle {}'.format(child.attrib['id']))
        else:
            r.set('edges',new_edges)
            #print(r.attrib)
    return tree
                
            
        
        
if __name__ == '__main__':
    tree1 = build_new_route_file('DUERoutes/local.static.0.rou.xml')
    tree1 = get_types(tree1)
    
    tree2 = build_new_route_file('DUERoutes/local.static.1.rou.xml')
    tree3 = build_new_route_file('DUERoutes/local.static.2.rou.xml')
    
    #tree = merge(routes,tree1)
    tree = merge(tree1, tree2)
    tree = merge(tree, tree3)
    tree.write('traffic.rou.xml')