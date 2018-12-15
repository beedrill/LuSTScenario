# -*- coding: utf-8 -*-
import pickle
import xml.etree.cElementTree as ET
class Vehicle():
    def __init__(self, vid, vtype, time):
        self.vid = vid
        self.vtype=vtype
        #self.vfrom = vfrom
        self.time = time
        self.route = []

with open('vehicles-dua.pkl','rb') as f:
    carflow = pickle.load(f)
    #print(carflow)
    
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
direct_roads = [
                'west_in',
         'west_out',
         'east_in',
          'east_out',
         'north_in',
         'north_out',
         'south_in',
         'south_out'
        ]
secondary_roads = [
        'south_south_in',
         'south_west_in',
         'west_west_in',
         'west_south_in',
         'west_north_in',
         'east_east_in',
         'east_north_in']
def check_route(route):
    #print(route)
    if new_edge_dict[route[0]] in secondary_roads and len(route)>1:
       # print('haha')
        if not new_edge_dict[route[1]].endswith('in'):
            return route[1:]
        r = new_edge_dict[route[0]]
        tmp1 = r.split('_')
        r2 = new_edge_dict[route[1]]
        tmp2 = r2.split('_')
        if tmp1[0] == tmp2[0]:
            return route
        else:
            return route[1:]
    return route
def validate_route(route):
    routes = []
    new_route = []
    for e in route:
        if new_edge_dict[e] in secondary_roads:
            new_route = [e]
        elif new_edge_dict[e].endswith('out'):
            
            new_route.append(e)
            routes.append(check_route(new_route))
            new_route = []
        else:
            new_route.append(e)

    return routes
    
def getTimeIndex(time):
    if time<1824:
        index = 0;
    elif time>88223:
        index = 23;
    else:
        index = int((time-1824)/3600)
    return index
def makeRouteName(route,vtype):
    rn = ''
    for r in route:
        rn+=new_edge_dict[r]
        rn+='_'
    rn+=vtype
    return rn
        
class Route():
    def __init__(self, name, route, count, vtype):
        self.route = route
        self.name = name
        self.count = count
        self.vtype = vtype
    
def parseResult():
    parsedcarflow = {}
    for vid in carflow.keys():
        v = carflow[vid]
        time = v.time/1000
        #print(v.time)
        index = getTimeIndex(time)

        routes = validate_route(v.route)
        #if routes == []:
           # print(v.route)
           # print(routes)
        for route in routes:
            routename = makeRouteName(route, v.vtype)
            if not routename in parsedcarflow.keys():
                parsedcarflow[routename] = [Route(routename, list(map(lambda x: new_edge_dict[x], route)), 0, v.vtype) for i in range(0,24)]
        #else:
            #print('haha')
            parsedcarflow[routename][index].count += 1
        #print(index)
        #print(parsedcarflow[routename].count)
    #for k in parsedcarflow.keys():
    #    if not parsedcarflow[k][10].count== 0:
    #        print(parsedcarflow[k][10].count)
    with open('carflow.pkl', 'wb') as f:
        pickle.dump(parsedcarflow, f, pickle.HIGHEST_PROTOCOL)
#print(carflow)
    f.close()

class RouteGenerator():
    def __init__(self, outputfilename):
        self.outputfilename = outputfilename 
        
    def generate_types(self, routes):
        ## routes should be a ET.Element() class
        print('inplement generate_types function in your inherited class')
    def generate_routes_(self, routes,time):
        ## routes should be a ET.Element() class
        print('implement generate_routes_ method in your child class')
    def generate_flow(self, routes, time):
        print('implement generate_flow method in the child class')
        
    def generate_routes(self, time):
        routes = ET.Element('routes')
        self.generate_types(routes)
        self.generate_routes_(routes,time)
        self.generate_flow(routes, time)
        tree = ET.ElementTree(routes)
        tree.write("{}-{}.rou.xml".format(self.outputfilename,time))
    
class LuxembourgDetailedRouteGenerator(RouteGenerator):
    
    def __init__(self, outputfilename, edge_dict = new_edge_dict, inputroutefilename = 'carflow.pkl'):
        RouteGenerator.__init__(self, outputfilename)
        self. edge_dict = edge_dict
        self.inputroutefilename = inputroutefilename
        with open(inputroutefilename,'rb') as f:
            self.routes_dict = pickle.load(f)
        
    def generate_types(self, routes):
        ET.SubElement(routes,'vType',
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

        ET.SubElement(routes,'vType',
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
    
        ET.SubElement(routes, 'vType',
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
    
        ET.SubElement(routes, 'vType',
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
    
        ET.SubElement(routes, 'vType',
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
    
        ET.SubElement(routes, 'vType',
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
        
        ET.SubElement(routes, 'vType',
            vClass="bus",
            id="bus",
            accel="2.6",
            decel="4.5",
            sigma="0.5",
            length="12.0",
            minGap="3",
            maxSpeed="30",
            guiShape="bus")
        
    def build_route_name(self, route):
        tmp = ''
        for r in route:
            tmp+=r
            tmp+='_'
        return tmp
        
    def generate_routes_(self, routes,time):
        exist_edges = []
        for routename in self.routes_dict.keys():
            r = self.routes_dict[routename][time]
            route_edges = self.build_route_edges(r.route)
            if not route_edges in exist_edges:
                ET.SubElement(routes, 'route', id=self.build_route_name(r.route), edges = route_edges)
                exist_edges.append(route_edges)
                
    def generate_flow(self, routes, time):
        denominator = 3600+1824 if time == 0 else 3600
        for routename in self.routes_dict.keys():
            r = self.routes_dict[routename][time]
            #print(r.count)
            prob = float(r.count)/denominator
            if prob == 0:
                continue
            ET.SubElement(routes, 'flow',
                    id="flow_{}".format(routename),
                    type=r.vtype,
                    route=self.build_route_name(r.route),
                    probability=str(prob),
                    depart="1",
                    begin = "0",
                    end = "3600")
         
    def build_route_edges(self, edge_list):
        tmp = ''
        for e in edge_list:
            tmp += e
            tmp += ' '
        return tmp[:-1]
    
            
        
if __name__ == "__main__":
     parseResult()
   # with open('carflow.pkl','rb') as f:
        #routes_dict = pickle.load(f)
    #for k in routes_dict.keys():
     #   print(k, routes_dict[k][1].count)
     rg =LuxembourgDetailedRouteGenerator('LuxembougDetailed-DUE-12408/traffic')
     for i in range(0,24):
         rg.generate_routes(i)
    #rg.generate_routes(7)