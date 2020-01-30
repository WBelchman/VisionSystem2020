import threading
import time

import ball
from networktables import NetworkTables as nt

ip = "laptop"

nt.initialize(server=ip)
table = nt.getTable("chooser_data")

sem = threading.BoundedSemaphore(value=1)
stop_message = [0]

def start_ball():
    ball.main(stop_message, sem)

#Listens to networktable, runs when a value is changed
def valueChanged(table, key, value, isNew):
    print("Value changed:", table, key, value)
    # 0 stops everything
    # 1 stops everything but ball detector
    value = int(value)
    stop_message[0] = value
    
    if value != 0: 

        t = threading.Thread(target=target_list[value])
        sem.acquire() #Decrements semaphore value, waits for other scripts to stop

        print("[*]Starting thread: {}".format(value))
        t.start() #Starts thread

#Watches the connection to the networktables server
def connectionListener(info, connected):
    print(info, "Connected:", connected)

target_list=[0, start_ball]

nt.addConnectionListener(connectionListener)

table.addEntryListener(valueChanged)

while True:
    time.sleep(5)
