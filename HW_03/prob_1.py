import yaml
import gurobipy as grb

with open("prob1settings.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Model
casino = grb.Model()
casino.modelSense = grb.GRB.MAXIMIZE

# Decision variables
machine_count = {}
for floor in cfg['floors']:
    for machine_type in cfg['slottype']:
        machine_count[floor, machine_type] = casino.addVar(obj=cfg['exrevenue'][machine_type] - cfg['opcost'][machine_type], name=f'x{floor}_{machine_type}')

# Constraints
my_constr = {}
for floor in cfg['floors']:
    cname = f'{floor}'
    my_constr[cname] = casino.addConstr(grb.quicksum(machine_count[floor, machine_type]*cfg['area'][machine_type] for machine_type in cfg['slottype']) <= cfg['floors'][floor] , name=cname)

my_constr['hours'] = casino.addConstr(grb.quicksum(machine_count[floor, machine_type]*cfg['maintenance'][machine_type]
                        for machine_type in cfg['slottype'] for floor in cfg['floors']) <= cfg['totalhr'], name='hours')

for machine_type in cfg['slottype']:
    cname = f'handon_{machine_type}'
    my_constr[cname] = casino.addConstr(grb.quicksum(machine_count[floor, machine_type]
                        for floor in cfg['floors']) <= cfg['onhand'][machine_type], name=cname)

casino.update()
casino.write('casino.lp')

casino.optimize()
casino.update()
casino.write('casino.sol')

import csv

with open('casino_optimal_value.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['floor', 'slot_type', 'machine_count'])
    writer.writeheader()

    for item, value in machine_count.items():
        writer.writerow({'floor':item[0], 'slot_type':item[1], 'machine_count':value.X})

# casino.ObjVal give the profit value.