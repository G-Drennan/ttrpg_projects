import os 
import json
from pathlib import Path 
import uuid 
import time

class CRollTableImporter:
    def __init__(self):
        pass

    #Reads source data

    #Add data into json

class CRollTableFactory:        #converts given list into the required json format
    def __init__(self, mlist, name):
        self.mlist = mlist 
        self.name=name
        #self.table_data = ["name", "columns", "entries", "id", 'description', "tags", "diceType", "rangeMode", "rollExpression", "folderId", "created_at"]
        self.diceType = "d" + str(len(self.mlist)) 


    def get_table(self):
        return self._construct_table() 

    def _construct_table(self):
        if self.mlist is None:
            return-1 
        
        table = { 
            "id": self._generate_id(),
            "name": self.name,
            "description": "",
            "tags": [],#leave empty for user to modify
            "diceType": self.diceType,
            "rangeMode": False, 
            "rollExpression": self.diceType,
            "columns": self._create_cols(),
            "entries": self._create_entries(),
            "folderId": None,  
            "created_at": int(time.time()*1000)  
        }

        return table 

    def _generate_id(self):
        return str(uuid.uuid4())  

    def _create_cols(self):
       return [ 
            {
            "id": self._generate_id(), #random created in fucntion _generate_id
            "name": self.diceType #assumption
            }
        ]

    def _create_entries(self, ):
        #use mlsit to fill in results
        entries = []
        for i, item in enumerate(self.mlist):
            e = {
                "id": self._generate_id(),
                "minRoll": i+1, #assign based off count
                "maxRoll": i+1, 
                "results": [item] 

            }
            entries.append(e)
        return entries 



class CTableReader:
    def __init__(self):
        pass

    #input csv or txt use inheritance from table reader
    """
    a
    b
    c
    d
    e
    f
    g
    h
    """

    """a,b,c,d,e,f,g,h""" 

    #output
    """
    [
    "a",
    "b",
    "c"... ect 
    ]
    """



def main():
    lsit = ['a', 'b', 'c', 'd'] 
    name = "Letters" 
    print(f"{name}: {lsit}") 
    rtf = CRollTableFactory(mlist=lsit, name = name) 
    print(rtf.get_table())  

if __name__ == "__main__":
    main()