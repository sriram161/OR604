# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
import multiprocessing as mp
import random
import time
import sys
"""
The servant file is started second after the queue server and before the
master.  You can start as many servant instances as you want - a command
terminal is a new instance.  So if you wanted to have two servers, you 
would open two additional terminals on your laptop and and issue the command
to start each server instance (on the cloud with multiple servers, you 
would have one terminal open on each server - the example above is for 
running this entirely on your laptop or desktop).  

At the terminal prompt, change directories to where the myServant.py script
is.  Once there, type the following command at the prompt:
python myServant.py xxx.xx.xxx.x y z
where:
    xxx.xx.xxx.x is the private IP of your laptop or desktop (or the 
    AWS server IP if on the cloud).  

    y is the number of parallel processes you want on each instance 

    z is the name/number of the instance/server - you make this up and
    just provide it.  This is just so you can see which instance/server
    is producing the result you have seen.

    Note that there are no quotes around any of the arguments passed in
    and there are no comma's separating the three arguments.  These are
    all mistakes that I was making.

There will be minimal output to the terminal that the servant processes are
running on.  All the meaty processing that happens on the servers 
will be output to the master terminal.
"""
def myWorker(input_queue, output_queue, servantNum, seedNum):

    def make_rList(lb, ub, count):
        random.seed(seedNum)
        myList = random.sample(range(lb, (ub+1)), count)
        time.sleep(.5)
        return myList

    myName = mp.current_process().name    
    while True:
        #read from input queue
        lb, ub, count, x = input_queue.get()
        # check for poison pill
        if lb == None:
            break
        
        # call function
        output_queue.put((x, servantNum, myName, make_rList(lb,ub, count), 'there are %s elements' % count))
    
    return  
    
if __name__ == '__main__':
    myArgs = sys.argv

    myServer = myArgs[1]    
    myAuthKey = b'WarMachineRox'
    myChannel = 50000
    poolsize = int(myArgs[2])    
    print("Server %s has started" % myServer)
    servantNum = int(myArgs[3])
    seedNum = 111111
    
    while True:
        try:
            m = BaseManager(address=(myServer, myChannel), authkey=myAuthKey)
            m.register('input_queue')
            m.register('output_queue')
            m.connect()
            input_queue = m.input_queue()
            output_queue = m.output_queue()
            print("Server %s has connected to the queue" % myServer)
            break
        except:
            print('No queue manager found, waiting')
            time.sleep(1)
                
    processes = [mp.Process(target=myWorker, args = (input_queue, output_queue, servantNum, seedNum)) for x in range(poolsize)]
        
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    for p in processes:
        p.terminate()
    
    print("Server %s has terminated its %s processes and is shutting down" % (myServer, poolsize))

    