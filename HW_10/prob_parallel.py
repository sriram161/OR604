import multiprocessing as mp
import logging
import traceback
import random
import time
import gurobipy as grb
from itertools import count

logger = mp.log_to_stderr()
logger.setLevel(logging.INFO)
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
        if var.varName.startswith('GO'):
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

def write_csv(var_bounds, filename) -> None:
    import csv
    with open(filename, 'w',  newline='') as f:  
        csv_dict = csv.DictWriter(f, fieldnames=['away', 'home', 'day', 'slot', 'network', 'week', 'lb', 'ub'])
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

def set_constrain_vars_bounds(nfl, my_Constrs, var_bounds) -> tuple:
    games = dict()
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
    return games , var_bounds

def get_model(filename='nfl_probe.lp')-> object:
    nfl = grb.Model()
    nfl = grb.read(filename)
    nfl.setParam('timelimit', 10)
    nfl.setParam('OutputFlag', 0)
    return nfl

def get_var_status_record(nfl, var, var_count)-> dict:
    count_ = next(var_count)
    if nfl.status == grb.GRB.INFEASIBLE:
        logger.info('var_count: {1} probe iteration infeasible: {0}'.format('_'.join(var), count_))
        return {'name': var, 'lb': 0, 'ub': 0, 'run_flag': True}
    else:
        logger.info('var_count: {1} probe iteration feasible: {0}'.format('_'.join(var), count_))
        return {'name': var, 'lb': 0, 'ub': 1, 'run_flag': False}

def var_prob(in_q, v_shelf, filename):
    var_count = count(1)
    nfl = get_model(filename)
    free_vars = get_bounds_vars(nfl.getVars())[1]
    cache = set()

    while True:
        #STEP-1: Check managed shelf for var status updates which are not cached.
        infeasible_var_count = sum(1 for _ in v_shelf.values() if _.get('run_flag'))
        logger.info('Total infeasible vars in shelf: {0}'.format(infeasible_var_count))
        var_to_update = set(v_shelf.keys()) - cache
        #STEP-2: Updated var bounds in models with the updated from shelf.
        for name in var_to_update:
            free_vars[name].lb = v_shelf[name].get('lb')
            free_vars[name].ub = v_shelf[name].get('ub')
            cache.add(name)
        nfl.update()
        #STEP-3: Get var from Queue set model bound to 1.
        if in_q.empty():
            return
        var = in_q.get()
        # STEP-4: Set and Upatee var bounds from queue to model.
        free_vars[var].lb = 1
        free_vars[var].ub = 1
        nfl.update()
        # STEP-5: optimize.
        nfl.optimize()
        # STEP-5: Report var status on the managed dict shelf.
        record = get_var_status_record(nfl, var, var_count)
        free_vars[var].lb = record.get('lb')
        free_vars[var].ub = record.get('ub')
        # Post the report on managed shelf.
        v_shelf[record.get('name')] = record
        # STEP-6: Cache the var name.
        cache.add(record.get('name'))
        nfl.update()

def populate_input_queue(in_q, filename, var_shelf):
    nfl = get_model(filename)
    my_Constrs = nfl.getConstrs()
    games = get_game_vars(nfl.getVars())
    var_bounds, free_vars = get_bounds_vars(nfl.getVars())
    games, var_bounds = set_constrain_vars_bounds(nfl, my_Constrs, var_bounds)
    for game in games:
        lb, ub = var_bounds[game]
        var_shelf[game] = {'name': game, 'lb': lb, 'ub': ub, 'run_flag': False}
    for item in free_vars:
        if games.get(item):
            continue
        in_q.put(item)

def update_shelf_to_model(var_shelf, free_vars):
    for var_key, item in var_shelf.items():
        if free_vars.get(var_key):
            free_vars[var_key].lb = item.get('lb')
            free_vars[var_key].ub = item.get('ub')

def main(process_count = 4):
    filename = 'nfl_probe.lp'
    epoch_count = count(1)
    run_flag = True
    with mp.Manager() as resource_manager:
        while(run_flag):
            input_queue = resource_manager.Queue()
            var_shelf = resource_manager.dict()
            populate_input_queue(input_queue, filename, var_shelf)

            tasks = [mp.Process(target=var_prob, args=(input_queue, var_shelf, filename)) for _ in range(process_count)]

            for task in tasks:
                task.start()
            
            for task in tasks:
                task.join()

            for task in tasks:
                task.terminate()

            # Write lp file.
            nfl = grb.Model()
            nfl = grb.read(filename)
            nfl_vars = nfl.getVars()
            my_Constrs = nfl.getConstrs()
            var_bounds, free_vars = get_bounds_vars(nfl_vars)
            update_shelf_to_model(var_shelf, free_vars)
            nfl.update()
            
            # games, var_bounds = set_constrain_vars_bounds(nfl, my_Constrs, var_bounds)
            nfl.update()

            # Write csv file.
            write_csv(var_bounds, filename='nfl_probe_temp_vars.csv')
            
            # Write lp file.
            filename='nfl_probe_temp.lp'
            nfl.write(filename)

            # loop with run flag.
            infeasible_var_count = sum(1 for _ in var_shelf.values() if _.get('run_flag'))
            if infeasible_var_count:
                logger.info('Dr.C you are a great teacher! {1} variables infeasbile, I am going for a spin: {0} count'.format(next(epoch_count), infeasible_var_count))
                run_flag = True
            else:
                logger.info('Task Completed!!!')
                run_flag = False

if __name__ == '__main__':
    random.seed(1234)
    main()
