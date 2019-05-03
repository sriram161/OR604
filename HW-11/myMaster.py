# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
import time
import random
import sys

"""
The master is the last process to start (after the queue and the servants).
It needs its own terminal as well.  So if you were to have a distributed 
network on your laptop with 2 servants, you would need a total of 4 
terminals (one for the queue, one for the master, and one for each servant)
If you were running this on Amazon, you would want three servers, one for
master and queue (the queue doesn't use a  lot of memory so you could run 
it on the same server as the master - you just need two terminals) and 
then one for each server.

Open the terminal and change directories to where the myMaster.py file is
located.  At the command prompt, enter the following command:
python myMaster.py xxx.xx.xxx.x
Where:
    xxx.xx.xxx.x is the private IP address of your laptop or desktop.  This
    needs to be the same IP address as what you provided when you started
    the servants.

All of the output will go to the main screen terminal.

Something interesting is that if after you have started you want to add 
another servant, it will work.  Give it a try.
"""

def myHandler(input_queue, output_queue, seedNum):
    # fill the queue with working data
    random.seed(seedNum)
    totalNum = random.randint(5000, 10000)
    for x in range(totalNum):
        lb = random.randint(0, 10)
        ub = lb + random.randint(1, 20)
        count = random.randint(1,ub-lb)
        [input_queue.put((lb,ub,count,x))]
    
    # collect the output results from the servants
    counter = 0
    while counter < totalNum:
        try:
            myResults = output_queue.get_nowait()
            counter += 1
            print(myResults)
        except:
            time.sleep(.2)
    
    return totalNum
    
if __name__ == '__main__':
    masterStart = time.time()
    myArgs = sys.argv

    myServer = myArgs[1]
    myAuthKey = b'WarMachineRox'
    myChannel = 50000
    seedNum = 1444441

    # Connect to the queue server and register queues
    # address is the address of queue handler, 50000 is the port
    m = BaseManager(address=(myServer, myChannel), authkey=myAuthKey)
    m.register('input_queue')
    m.register('output_queue')
    m.connect()
    input_queue = m.input_queue()
    output_queue = m.output_queue()
    
    # the actual working processes
    startTime = time.time()
    count = myHandler(input_queue, output_queue, seedNum)
    print('running time is ', time.time()-startTime, ' seconds')
    print('there were %s lists generated' % count)
    print('Total real time (master time):= %s' % str(time.time() - masterStart))    
    print('Done')
    
    #flood the queue
    for i in range(5000): input_queue.put((None,None,None,None))

    time.sleep(2)

    #drain the queue
    for i in range(5000): 
        try:
            input_queue.get_nowait()
        except:
            pass

    print('Total real time (master time):= %s' % str(time.time() - masterStart))    