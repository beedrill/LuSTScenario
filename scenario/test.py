# -*- coding: utf-8 -*-
## use this code to get car flow of the intersection from the carflow.pkl
#==============================================================================
# import pickle
# 
# with open('carflow-12408-DUA.pkl','rb') as f:
#     carflow = pickle.load(f)
# 
# from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
# 
# to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']
# 
# vtype = ["passenger1","passenger2a","passenger2b","passenger3","passenger4","passenger5", "bus"]
# 
# overall_flow = [0 for i in range(0,24)]
# 
# for idx_fr, fr_e in enumerate(from_edge):
#     for idx_to, to_e in enumerate(to_edge):
#         for vt in vtype:
#             overall_flow = [x+y for x,y in zip(carflow[fr_e][to_e][vt], overall_flow)]
# 
# print(overall_flow)
# 
#==============================================================================
##use this to get car flow of a certain resolution 

#==============================================================================
# resolution = 300
# 
# f = open('result-12408-DUA.txt', 'r')
# line = f.readline()
# 
# from_edge = ['--31272#7', '-30892#16', '-31272#6', '--30892#17']
# to_edge = ['-31272#7', '--30892#16', '--31272#6', '-30892#17']
# vtype = ["passenger1","passenger2a","passenger2b","passenger3","passenger4","passenger5", "bus"]
# 
# flow = {}
# max_index = 0
# 
# 
# while line:
#     ## here add stuffs
#     temp = line.split()
#     vid = temp[0]
#     vtype = temp[1]
#     vfrom = temp[2]
#     vto = temp[3]
#     time = temp[4]
#     time = int(time)/1000
#     index = int(time/resolution)
#     if not index in flow.keys():
#         flow[index] = 1
#     else:
#         flow[index] += 1
#     if max_index < index:
#         max_index = index
# 
#     line=f.readline()
# with open('carflow-12408-resolution-{}.txt'.format(resolution), 'w') as f:
#     for i in range(0,max_index+1):
#         if not i in flow.keys():
#             f.write('{}\n'.format(0))
#         else:
#             f.write('{}\n'.format(flow[i]))
# 
#==============================================================================
