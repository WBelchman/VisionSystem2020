from networktables import NetworkTables as nt

table_list = ["tape_data", "ball_data"]
key_list = ["midpoint", "width"]

class Table:
    
    def __init__(self, table_number):
        nt.initialize(server='10.31.51.43')
        self.table = nt.getTable(table_list[table_number])

    def updateNumber(self, midpoint, key = 0):
        table = self.table
    
        try:
            table.putString(key_list[key],str(midpoint))
        except Exception as e:
            print(e)


#https://robotpy.readthedocs.io/projects/pynetworktables/en/stable/examples.html
