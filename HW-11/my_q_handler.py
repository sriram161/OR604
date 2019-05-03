# -*- coding: utf-8 -*
"""
The queue handler must be started first, then the servants, then the master
There are no arguments for the queue handler.  Open a terminal and change 
directories to the one in which the queue handler, servant, and master
are located.  Open a terminal.  In that terminal enter the following 
command at the prompt:  python my_q_handler.py

That's it.  Now go to the MyServant module...
"""
from multiprocessing.managers import BaseManager
from queue import Queue

input_queue = Queue()
output_queue = Queue()

manager = BaseManager(address=('',50000), authkey = b'WarMachineRox')
manager.register('input_queue', callable = lambda:input_queue)
manager.register('output_queue', callable = lambda:output_queue)

print('queues started')
server = manager.get_server()
server.serve_forever()


