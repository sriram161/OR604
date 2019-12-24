""" Integer programming problem to minimizie the cost to produces a 
a set of drink kegs to meet the demand.

Decision variables:
---------------------
Number of kags of brew geneate for each blend.

Given parameters:
--------------------
brewery 
Distriution 
distances

"""
import gurobipy as grb

# Gurobi Model preparation.
char_brew = grb.Model()
char_brew.modelSense = grb.GRB.MINIMIZE
char_brew.update()

import csv

brewery  = ['ric', 'sav', 'rxv', 'cle']
distribution = ['char', 'orx', ..., 'cha']
miles = { (b, d) : ...}
cost = {b: }
demand = {d: }
supply = {b: }

# Decision Variables.
kags = {}
for b in brewery:
    for d in distribution:
       kegs[b,d] = char_brew.addVar(obj = cost[b] * miles[b,d], name=f'k{b}{d}')

for d in distribution:
    cName = f'demand {d}'
    my_constr[cname] = char_brew.addConstr(grb.quicksum(kags[b,d] for b in brewery) >= demand[d], name=cname)

char_brew.update()
char_brew.write('test.lp')
char_brew.optimize() 