from networktables import NetworkTables as nt

table_name = ["ball_data", "ps_data", "team_data"]
key_list = ["midpoint", "width"]

nt.initialize(server="laptop")

class Table:
    
    def __init__(self, table):
        self.table = nt.getTable(table_name[table])

    def updateNumber(self, midpoint, key = 0):
        table = self.table
    
        try:
            table.putString(key_list[key], str(midpoint))
        except Exception as e:
            print(e)


#https://robotpy.readthedocs.io/projects/pynetworktables/en/stable/examples.html
