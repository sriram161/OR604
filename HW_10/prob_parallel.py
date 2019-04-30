import multiprocessing as mp 
import logging
import traceback
import random
import time
import gurobipy as grb

def get_game_vars(nfl_vars) -> dict:
    games = {} 
    for var in nfl_vars:
        if var.varName[:2] == 'GO':
            games[var.varName] = var
    return games

def get_bounds_vars(nfl_vars) -> tuple:
    free_vars = {} # Free variabls can be 0 or 1.
    var_bounds = {}
    for var in nfl_vars:
        if var.varName[:2] == 'GO':
            temp = var.varName.split('_')
            if 'PRIME' in temp:
                free_vars[tuple(temp[1:])] = var
                var_bounds[tuple(temp[1:])] = (var.LB, var.UB)
    return var_bounds, free_vars

def is_hard_constr(row) -> bool:
    for r in range(row.size()):
        if not row.getVar(r).VarName.startswith('GO'):
            return False
    return True

def write_csv(var_bounds) -> None:
    import csv
    with open('mycsvfile.csv', 'w') as f:  
        csv_dict = csv.DictWriter(f, ['away', 'home', 'day', 'slot', 'network', 'week', 'lb', 'ub'])
        csv_dict.writeheader()
        for k, v in var_bounds.items():
            csv_dict.writerow({'away': k[0],'home':k[1], 'day':k[2], 'slot':k[3], 'network':k[4], 'week':k[5], 'lb': v[0], 'ub':v[1]})

def clean_up(var_bounds, free_vars) -> tuple:
    remove_keys = []
    for v in var_bounds:
        if var_bounds[v][0] == var_bounds[v][1]: #upper == lower
            if free_vars.get(v):
                free_vars.pop(v)
                remove_keys.append(v)

    for v in remove_keys:
        var_bounds.pop(v)
    return var_bounds, free_vars

def set_constrain_vars_bounds(my_Constrs, games, var_bounds) -> tuple:
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

def get_model(filename='nfl_probe.lp')-> object:
    nfl = grb.Model()
    nfl = grb.read(filename)
    nfl.setParam('timelimit', 10)
    nfl.setParam('OutputFlag', 0)
    return nfl

def var_prob(in_q, out_q, v_shelf, filename):
    nfl = get_model(filename)
    var_bounds, free_vars = get_bounds_vars(nfl_vars)
    var = in_q.get()


    return 

def main(process_count = 4):
    from itertools import count
    epoch_counter = count(1)
    #nfl.write('nfl_probe.lp')
    # STOP = False
    # while not STOP:
    #     STOP = False
    with mp.Manager() as resource_manager:
        output_queue = resource_manager.Queue()
        input_queue = resource_manager.Queue()
        var_shelf = resource_manager.dict()
        # should I use synchronizing primitives????
        # populate_input_queue(input_queue)

        tasks = [mp.Process(target=var_prob, args=(input_queue, output_queue, var_shelf, 'nfl_probe.lp')) for _ in range(process_count)]


if __name__ == '__main__':
    random.seed(1234)
    main()
