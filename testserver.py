import time
from networktables import NetworkTables as nt

nt.initialize()

table = nt.getTable("chooser_data")
table2 = nt.getTable("tape_data")
table3 = nt.getTable("ball_data")

def valueChanged(table, key, value, isNew):
	print("Changed:", table, key, value)

def connectionListener(info, connected):
    print("Connected:", info, "Connection:", connected[0],"-",connected[1])

nt.addConnectionListener(connectionListener)

table.addEntryListener(valueChanged)
table2.addEntryListener(valueChanged)
table3.addEntryListener(valueChanged)

while True:
	time.sleep(5)
