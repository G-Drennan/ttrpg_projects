import os 
import json
from pathlib import Path 
import uuid 
import time
import pandas as pd

class CRollTableImporter:
    def __init__(self, list_fp: Path, fp = Path("./tables/rollTableLibrary.json")):
            self.fp = fp
            self.table_library_dict = self._open_dict() 
            self.tr = CTableReaderFactory.create(list_fp) #to get the lsit and name
 
            '''temp_list =  self._extract_mlist()
            temp_name = self._extract_name() 
            self.rt = CRollTableFactory(mlist=temp_list, name=temp_name)'''

            #main flow  
            self._open_dict()
            self._add_table()
            self._save() 

    def _extract_mlist(self):
         #call tr
         temp_list = self.tr.get_mlist() 
         return temp_list
    
    def _extract_name(self):  
             #call tr
             temp_name = self.tr.get_file_name()
             return temp_name 

    def _open_dict(self): #Reads source data
                
                if self.fp.is_file():  
                    with open(self.fp, 'r') as f: 
                        loaded_dict = json.load(f) 
        
                    return loaded_dict  
                else:
                    #print(f"File {fp} doesn't exist. Giving empty dict")   
                    return  self._create_empty_library()

    def _create_empty_library(self):
        return {
                "version": 1,
                "type": "rollTableLibrary",
                "tables": [],
                "folders": []
            }
         
    def _add_table(self): 
        self.table_library_dict["tables"].append(self.rtf.get_table()) 

    def _save(self):  #Add data into json  
            
            with open(self.fp, 'w') as f: 
                json.dump(self.table_library_dict, f, indent=4) 
            return self.fp


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



class CTableReaderFactory:
    def __init__(self):
        pass 

    def create(self, fp: Path): 
        tr = CTableReader(fp)
        fp_end = tr.get_file_name() 
        if fp_end == 'csv':
            return CCsvTableReader(fp)
        elif fp_end == 'txt':
            return CCsvTableReader(fp)


class CTableReader: 
    def __init__(self, fp: Path):
        self.fp = fp
        self.input = None

    def get_mlist(self): 
        return self._parse_file()  

    def _parse_file(self): #example return value, will be over written
        return ['a', 'b', 'c', 'd']

    def get_file_name(self): 
         #file name file off the path and file type
         s = str(self.fp)
         l = s.split('.')
         return l[-1] 
    
    def _parse_file(self):
         pass 

    def _read(self): #default cna be overwritten
            f1 = open(self.fp, "r", encoding="utf-8")
            text = f1.read()
            f1.close()  
            self.input =  text

class CCsvTableReader(CTableReader):

    def _parse_file(self):

        ori = self._detect_orientation()

        if ori == 'r':
            return self._parse_row_based()
        
        elif ori == 'c':
            return self._parse_col_based() 

    def _detect_orientation(self):
        self._read_csv() 
        self._read()
        l = len(self.input.split(',')) 

        if l > 1:
            return 'c' 
        else:
             return 'r' 

    def _parse_row_based(self):
        return self.df.iloc[:,0] 
    
    def _parse_col_based(self):
        return self.df.iloc[0] #grab the first row

    def _read_csv(self):  
        self.df =  pd.read_csv(self.fp) 
            

class CTxtTableReader(CTableReader): 

    def _parse_file(self):
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



def main(): #TODO: args to the program should be a lsit of str for csv and txt to convert to tables 
    fp = Path("./Temperature.csv") 
    tr = CCsvTableReader(fp) 
    print(tr.get_mlist()) 
    #CRollTableImporter(list_fp=fp)  


if __name__ == "__main__":
    main()