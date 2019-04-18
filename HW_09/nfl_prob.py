import gurobipy as grb

filename = r"OR604 Model File v2.lp"
nfl = grb.Model()
nfl = grb.read(filename)

#STEP1->1 Nfl get variables for nfl model.
nfl_vars = nfl.getVars()

#STEP->2 load game variablse to games dict.
games = {} 
for var in nfl_vars:
    if var.varName[:2] == 'GO':
        games[var.varName] = var

# get prime time free vars
free_vars = {} # Free variabls can be 0 or 1.
var_status = {}
for var in nfl_vars:
    if var.varName[:2] == 'GO':
        temp = var.varName.split('_')
        if 'PRIME' in temp:
            free_vars[tuple(temp[1:])] = var
            var_status[tuple(temp[1:])] = (var.LB, var.UB)

# Remove lowerbond == upperbound from free_vars and var_status.
remove_keys = []
for v in var_status:
    if var_status[v][0] == var_status[v][1]: #upper == lower
        if free_vars.get(v):
            free_vars.pop(v)
            remove_keys.append(v)

for v in remove_keys:
    var_status.pop(v)

#STEP->3 load constaints.
remove_cons_keys = []
my_Constrs = nfl.getConstrs()
for con in my_Constrs:
    if con.sense == '<' and con.RHS == 0:
        # print(con.constrName, con.RHS)
        remove_cons_keys.append(con.constrName)
        row = nfl.getRow(con)
        for r in range(row.size()): # Force them to zero
            print(row.getVar(r))
            row.getVar(r).lb == 0 # KO the variables to zero.
            row.getVar(r).ub == 0 # KO the variables to zero.

nfl.setParam('timelimit', 10)
STOP = False
while not STOP:
    STOP = True
    for v in free_vars:
        free_vars[v].lb = 1
        nfl.update()
        nfl.optimize()
        if nfl.status == grb.GRB.INFEASIBLE:
            STOP = False
            var_status[v] = (0, 0)
            free_vars[v].ub = 0 # Record all upper bound changed to zero to csv.
        else:
            free_vars[v].lb = 0
        nfl.update()


# write all variables to a csv file.
# varible_name, lower_boud, upper_bound.
import csv
with open('mycsvfile.csv', 'w') as f:  
    csv_dict = csv.DictWriter(f, ['var', 'lb', 'ub'])
    csv_dict.writeheader()
        for k, v in var_status.items():
            csv_dict.writerow({'var': k, 'lb': v[0], 'ub':v[1]})

nfl.save('nfl_probe.lp')