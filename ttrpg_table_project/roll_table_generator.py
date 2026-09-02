import json
from pathlib import Path 
import uuid 
import time 
import pandas as pd
from datetime import datetime
import shutil
import random as rand
import hashlib 

class CRollTableInterface:
    def __init__(self, fp = Path("./tables/rollTableLibrary.json")): # 
            self.fp = fp
            self.table_library_dict = self.open_table_library() 

    def update_json(self, id: str, updated_table: dict):
        #replace a table with its new version
        tables = [] 
        updated = False
        tables = self.table_library_dict["tables"] 
        for i,t in enumerate(tables):
            if t['id'] == id:
                #tables.append(updated_table)
                tables[i] = updated_table
                updated = True
                break
        self.table_library_dict["tables"] = tables
        self.save_table_to_library() 
        return updated

    def remove_table_from_library(self, id: str): #e.g             "id": "2185e775-cde0-4565-936c-d5dae2fe25a4", 
        removed = False
        tables = [] 
        tables = self.table_library_dict["tables"] 
        removed_section = None
        for t in tables:
            if t['id'] == id:
                #print(tables) 
                tables.remove(t) 
                removed = True
                removed_section = t
        self.table_library_dict["tables"] = tables
        self.save_table_to_library() 
        return removed, removed_section
             
    def create_table_from_file(self, list_fp: Path):
        trf = CTableReaderFactory() 
        tr = trf.create_CTableReader(fp = list_fp) #to get the lsit and name
        name = tr.get_file_name()
        mlist = tr.get_mlist() 
        self.rtf = CRollTableFactory(mlist, name)
        self.add_table()
        self.save_table_to_library()  
        return self.rtf.get_id() 

    def create_table_from_text_entry(self, text):
        name = None
        mlist = None
        if isinstance(text, tuple):
            try:
                name, txt = text 
                mlist = [x.strip() for x in txt.split(",") if x.strip()]
            except:
                            name = None
                            mlist = None 
        if isinstance(text, str):
            try:
                name, txt = text.split(';', 1) #only split at the first ;
                mlist = [x.strip() for x in txt.split(",") if x.strip()] 
            except:
                name = None
                mlist = None   
        if not mlist: 
            mlist = None  
        if name is not None and mlist is not None: 
            self.rtf = CRollTableFactory(mlist, name)
            self.add_table()
            self.save_table_to_library() 
            return self.rtf.get_id() 

    def open_table_library(self): #Reads source data
                
                if self.fp.is_file():  
                    with open(self.fp, 'r') as f: 
                        try:
                            loaded_dict = json.load(f) 
                            return loaded_dict  

                        except:
                            return  self.create_empty_library()

        
                else:
                    #print(f"File {fp} doesn't exist. Giving empty dict")   
                    return  self.create_empty_library()

    def create_empty_library(self, corrupt = False):
        if corrupt:
            self._corrupt_file_handler()
        empty_lib = {
            "version": 1,
            "type": "rollTableLibrary",
            "tables": [],
            "folders": []
        }
        return empty_lib


    def _corrupt_file_handler(self): 
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")   
        with open(self.fp, "rb") as f:
            source_data = f.read()
        source_hash = hashlib.md5(source_data).hexdigest()
        corrupt_fp = (
            self.fp.parent /
            f"{self.fp.stem}_{timestamp}.corrupt{self.fp.suffix}"
        )
        #check the  last corrupt_fp is not the same contence as the one about to be made
        if corrupt_fp.exists():
            with open(corrupt_fp, "rb") as f:
                corrupt_hash = f.read()
            corrupt_hash = hashlib.md5(corrupt_hash).hexdigest()
            if source_hash != corrupt_hash:
                corrupt_fp += str(rand())

        shutil.copy2(self.fp, corrupt_fp)
   
         
    def add_table(self):  
        self.table_library_dict["tables"].append(self.rtf.get_table()) 

    def save_table_to_library(self):  #Add data into json  
            #atomic save
            try:
                temp_fp = self.fp.with_suffix(".tmp")
                with open(temp_fp, 'w') as f: 
                    json.dump(self.table_library_dict, f, indent=4)
                temp_fp.replace(self.fp) 
                return True 
            except:
                return False



class CRollTableFactory:        #converts given list into the required json format
    def __init__(self, mlist, name):
        self.mlist = mlist 
        self.name=name
        self.table_created = False
        #self.table_data = ["name", "columns", "entries", "id", 'description', "tags", "diceType", "rangeMode", "rollExpression", "folderId", "created_at"]
        self.diceType = "d" + str(len(self.mlist)) 

    def get_id(self):
        if self.table_created:
            return self.table['id']
        else:
            return str(-1)   

    def get_table(self):
        return self._construct_table() 

    def _construct_table(self):
        if self.mlist is None:
            return-1 
        
        self.table = { 
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
        self.table_created = True
        return self.table 

    def _generate_id(self):
        return str(uuid.uuid4())  

    def _create_cols(self):
       return [ 
            {
            "id": self._generate_id(), #random created in fucntion _generate_id
            "name": self.diceType #assumption
            }
        ]

    def _create_entries(self):
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

    def create_CTableReader(self, fp: Path): 
        tr = CTableReader(fp)
        fp_end = tr.get_file_type() 
        if fp_end == 'csv':
            return CCsvTableReader(fp)
        elif fp_end == 'txt':
            return CTxtTableReader(fp) 

class CTableReader: 
    def __init__(self, fp: Path):
        self.fp = fp
        self.input = None

    def get_mlist(self): 
        return self._parse_file()  

    def _parse_file(self): #example return value, will be over written
        return ['a', 'b', 'c', 'd']

    def get_file_name(self):
        return self.fp.stem
          
    def get_file_type(self): 

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
        #print(self.df.columns) 
        return self.df.iloc[:,0].to_list()  
    
    def _parse_col_based(self):
        return self.df.iloc[0].to_list() #grab the first row

    def _read_csv(self):  
        self.df =  pd.read_csv(self.fp, header=None)  
            
class CTxtTableReader(CTableReader): 

    def _parse_file(self):
        self._read()  
        return self.input.splitlines() #expects form "roll 1.\nroll 2.\nroll 3\n ect..."
