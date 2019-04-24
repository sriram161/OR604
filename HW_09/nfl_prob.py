import gurobipy as grb

filename = r"OR604 Model File v2.lp"
nfl = grb.Model()
nfl = grb.read(filename)

#STEP1->1 Nfl get variables for nfl model.
nfl_vars = nfl.getVars()

#STEP->2 load game variablse to games dict.
def get_game_vars(nfl_vars):
    games = {} 
    for var in nfl_vars:
        if var.varName[:2] == 'GO':
            games[var.varName] = var
    return games
games = get_game_vars(nfl_vars)

#STEP->3 get prime time free vars.
def get_bounds_vars(nfl_vars):
    free_vars = {} # Free variabls can be 0 or 1.
    var_bounds = {}
    for var in nfl_vars:
        if var.varName[:2] == 'GO':
            temp = var.varName.split('_')
            if 'PRIME' in temp:
                free_vars[tuple(temp[1:])] = var
                var_bounds[tuple(temp[1:])] = (var.LB, var.UB)
    return var_bounds, free_vars

var_bounds, free_vars = get_bounds_vars(nfl_vars)

# STEP->4 Find the  
# Remove lowerbond == upperbound from free_vars and var_bounds.
def clean_up(var_bounds, free_vars):
    remove_keys = []
    for v in var_bounds:
        if var_bounds[v][0] == var_bounds[v][1]: #upper == lower
            if free_vars.get(v):
                free_vars.pop(v)
                remove_keys.append(v)

    for v in remove_keys:
        var_bounds.pop(v)
    return var_bounds, free_vars

var_bounds, free_vars = clean_up(var_bounds, free_vars)

#STEP->5 Function to check hard or soft constraint.
def is_hard_constr(row):
    for r in range(row.size()):
        if not row.getVar(r).VarName.startswith('GO'):
            return False
    return True

def write_csv(var_bounds):
    import csv
    with open('mycsvfile.csv', 'w') as f:  
        csv_dict = csv.DictWriter(f, ['away', 'home', 'day', 'slot', 'network', 'week', 'lb', 'ub'])
        csv_dict.writeheader()
        for k, v in var_bounds.items():
            csv_dict.writerow({'away': k[0],'home':k[1], 'day':k[2], 'slot':k[3], 'network':k[4], 'week':k[5], 'lb': v[0], 'ub':v[1]})

#STEP->3 load constaints.
my_Constrs = nfl.getConstrs()

def set_constrain_vars_bounds(my_Constrs, games, var_bounds):
    for con in my_Constrs:
        if con.sense == '<' and con.RHS == 0:
            row = nfl.getRow(con) # To find panelty variables.
            if is_hard_constr(row):
                for r in range(row.size()): # Force them to zero
                    var = row.getVar(r) 
                    var.lb == 0 # KO the variables to zero.
                    var.ub == 0 # KO the variables to zero.
                    if 'PRIME' in var.VarName:
                        games[tuple(var.VarName.split('_')[1:])] = var
                        var_bounds[tuple(var.VarName.split('_')[1:])] = (0, 0)
    return games, var_bounds

games, var_bounds = set_constrain_vars_bounds(my_Constrs, games, var_bounds)
nfl.update()

from itertools import count
epoch_counter = count(1)
nfl.setParam('timelimit', 10)
nfl.setParam('OutputFlag', 0)
# nfl.setParam('logtoconsole', 0)
# nfl.setParam('threadlimit', 1)
STOP = False
nfl.write('nfl_probe.lp')
while not STOP:
    STOP = True
    var_counter = count(1)
    for v in free_vars:
        free_vars[v].lb = 1
        nfl.update()
        nfl.optimize()
        if nfl.status == grb.GRB.INFEASIBLE:
            STOP = False
            print('probe iteration infeasible: ', next(var_counter), 'Total free vars: ', sum(v.ub for k, v in free_vars.items()))
            var_bounds[v] = (0, 0)
            free_vars[v].ub = 0 # Record all upper bound changed to zero to csv.
            free_vars[v].lb = 0
        else:
            print('probe iteration feasible: ', next(var_counter), 'Total free vars: ', sum(v.ub for k, v in free_vars.items()))
            free_vars[v].lb = 0
        nfl.update()
        # nfl.write('nfl_probe.lp')
        # write_csv(var_bounds)
    var_bounds, free_vars = clean_up(var_bounds, free_vars)
    print('Probe epoch: ', next(epoch_counter), 'Total free vars: ', sum(v.ub for k, v in free_vars.items()))
    write_csv(var_bounds)
    nfl.write('nfl_probe.lp')
    
    nfl = grb.Model()
    nfl = grb.read('nfl_probe.lp')
    nfl_vars = nfl.getVars()
    var_bounds, free_vars = get_bounds_vars(nfl_vars)
    my_Constrs = nfl.getConstrs()
    games, var_bounds = set_constrain_vars_bounds(my_Constrs, get_game_vars(nfl_vars), var_bounds)
    nfl.setParam('timelimit', 10)
    nfl.setParam('OutputFlag', 0)

write_csv(var_bounds)
nfl.write('nfl_probe_final.lp')