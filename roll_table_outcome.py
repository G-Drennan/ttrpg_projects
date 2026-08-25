
import os 
import json
from pathlib import Path 


class CTableLibrary: #contains an arr of CRollTables
    def __init__(self, fp: Path):
        self.table_dict = self._open_dict(fp) 
        self.RollTables = []
        self._Rolltable_Loader() 

    def _open_dict(self, fp: Path):  #pf is relative to the py ./tables/rollTableLibrary.json
            if fp.is_file():  
                with open(fp, 'r') as f: 
                    loaded_dict = json.load(f) 
    
                return loaded_dict  
            else:
                    #print(f"File {fp} doesn't exist. Giving empty dict")   
                return {}
    def _Rolltable_Loader(self):
        #load the tables from self.table_dict one at a time creating a CRolltable that holds each of the features of the dict
        #first check the dict is a "type": "rollTableLibrary"
        d = self.table_dict
        if d['type'] == 'rollTableLibrary': 
            self._proccess_RolltableLibrary()

    def get_RollTables(self):
        return self.RollTables 
        

    def _proccess_RolltableLibrary(self):
        list = self.table_dict['tables'] #list of dicts
        for d in list:
            rt = self._makeRollTable(d)
            self.RollTables.append(rt) 

    def _makeRollTable(self, d):
        name = d.get('name') 
        columns = d.get('columns')
        entries = d.get('entries')
        table_id = d.get('id')
        description = d.get('description')
        tags = d.get('tags')
        diceType = d.get('diceType')
        rangeMode = d.get('rangeMode')

        rollExpression = d.get('rollExpression')

        folderId = d.get('folderId')
        created_at = d.get('created_at') 

        return CRollTable(name, columns, entries, table_id, description, tags, diceType, rangeMode, rollExpression, folderId, created_at)

class CRollTable:
    def __init__(self,  name, columns, entries, id, description, tags, diceType, rangeMode, rollExpression, folderId, created_at):
        self.name = name
        self.columns = columns
        self.entries = entries
        self.id = id
        self.description=description
        self.tags = tags
        self.diceType = diceType
        self.rangeMode = rangeMode
        self.rollExpression = rollExpression
        self.folderId = folderId
        self.created_at = created_at

      

def main():
    fp = Path("./tables/rollTableLibrary.json")
    tl = CTableLibrary(fp) 

    for rt in tl.get_RollTables():
        print(vars(rt)) 



if __name__ == "__main__":
    main()