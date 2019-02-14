import yaml
import gurobipy as grb

with open("prob1settings.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

casino = grb.Model()
casino.modelSense = grb.GRB.MAXIMIZE

machine_count = {}
for floor in cfg['floors']:
    for machine_type in cfg['slottype']:
        machine_count[floor, machine_type] = casino.addVar(obj=cfg['exrevenue'][machine_type] - cfg['opcost'][machine_type], name=f'x{floor}_{machine_type}')

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
casino.write("filename.mst") 

# TODO: Find the optimized values and write them to CSV.
