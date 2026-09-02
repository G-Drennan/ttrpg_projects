import os
import json
from pathlib import Path 
import random
from mdutils.mdutils import MdUtils 
from roll_table_generator import CRollTableInterface 

#TODO: develop a backup method for tables to allow the user to fallback on past json that are not corrupt. 
    #write library.tmp success? write library.json #atomic save pattern 

class CRollTable:   #Holds data related to the table 
    def __init__(self,  name:str, columns:list, entries: list, id: str, description: str, tags: list, diceType: str, rangeMode:bool, rollExpression:str, folderId:str, created_at:str):
        self.name = name 
        self.columns = columns
        self.entries = entries
        self.id = id
        self.description=description
        self.tags = tags
        self.diceType = diceType    #The dice rolled
        self.rangeMode = rangeMode #Table has entires with a range e.g 1-3, 4-6, 8-10
        self.rollExpression = rollExpression    #What is displayed
        self.folderId = folderId
        self.created_at = created_at

    def refresh_me(self): #returns
        return { 
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "diceType": self.diceType,
            "rangeMode": self.rangeMode,
            "rollExpression": self.rollExpression,
            "columns": self.columns,
            "entries": self.entries,
            "folderId": self.folderId,
            "created_at": self.created_at
        }
    

    def get_tags(self):
        return self.tags

    def get_unpacked_tags(self):
            return self._unpack_list(self.tags)

    def get_id(self):
        return self.id

    def matches_txt(self, txt: str):    # only tables matching the txt -non case sensitive- will return true.
        txt = txt.lower()
        if txt in self.name.lower(): 
            return True
        if self.tags is not None: 
            for tag in self.tags:  
                if txt in tag.lower():
                    return True 
        return False

    def markdown_render(self, task: str = 'output_txt'):  #Either write the table in md
        md = MdUtils(file_name=self.name) 
        if  task == 'output_txt_wth_header':
            md.new_header(level=1, title=self.name)
        table_text = [] 
        tableHeader = ["Roll", "Name"]
        row_entries = self._extract_enties()
        table_text.extend(tableHeader) 
        table_text.extend(row_entries)

        md.new_table(
            columns=2,
            rows=len(self.entries)+1,  
            text= table_text
        ) 
        
        return md.get_md_text()

    def _extract_enties(self):  #Puts enteries into a list for md
        row_entries = []
        for d in self.entries:
            if d['minRoll'] != d['maxRoll']:
                roll = str(d['minRoll']) + " - " + str(d['maxRoll'])
            else:
                roll = str(d['minRoll']) 
            row_entries.append(roll)

            result = self._unpack_list(d['results'])

            row_entries.append(result)  
        return row_entries 

    def _unpack_list(self, mlist):  #coverts [a,b,c] to a,b,c or [a] to a 
        mstring = ""
        tog = len(mlist) > 0 
        count = 0
        for e in mlist:
            if count == len(mlist)-1: 
                mstring += e
            else:
                 mstring += e + ", "
            count +=1 
                 
        return mstring

    def _roll(self):    #genrate a number from 0 to len(self.entries)
        max = 0
        if len(self.entries) >=1:
            max = len(self.entries) -1
        elif len(self.entries) == 0:
            return -1
        return random.randint(0, max) 



    def roll_value(self):
        n = self._roll() 

        if n == -1:
            return "No entires in the table"
        return self._unpack_list(self.entries[n]['results'])
    
#~

class CTableLibrary:    #contains an list of CRollTables
    def __init__(self, fp= Path("./tables/rollTableLibrary.json")):  
        #check the path exists if not creaet the file
        if not fp.parent.exists(): #file will always exist 
            fp.parent.mkdir(parents=True, exist_ok=True)
            
        self.rti = CRollTableInterface(fp=fp)  
        self.fp = fp
        self.RollTables = [] 
        self._Rolltable_Loader() 
    
    def search_bar(self, search_input: str):
        items = search_input.split(' ')  
        corrected_items = []
        for i in items:
            if len(i) > 0: #remove empty str
                corrected_items.append(i) 

        if len(corrected_items) > 0:
                items = corrected_items 
    
        RollTables_filtered = None   
        for i in items:  
            RollTables_filtered = self._matches_search(i, RollTables_filtered)

        return RollTables_filtered  #CRolTable

    def _open_roll_table_library(self): #always returns a valid dict
            if self.fp.is_file():  
                try:
                    with open(self.fp, 'r') as f: 
                        loaded_dict = json.load(f) 
        
                    return loaded_dict 
                except:
                    return self.rti.create_empty_library(corrupt=True)   
            else:
                #print(f"File {fp} doesn't exist . Giving empty dict")   
                return self.rti.create_empty_library() 
            
    def _Rolltable_Loader(self):    #load the tables from self.table_dict one at a time creating a list of CRolltable 
        #first check the dict is a "type": "rollTableLibrary"
        d = self._open_roll_table_library() 
        if 'type' in d:
            if d['type'] == 'rollTableLibrary': 
                self._proccess_RolltableLibrary(d)  #if not called self.RollTables remains empty. 

    def get_RollTables(self):
        return self.RollTables 

    def _proccess_RolltableLibrary(self, d: dict): 
        if 'tables' in d: #else silent failure 
            mlist = d['tables'] #list of dicts
            for d in mlist:
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

    def _create_new_table(self, txt: str): #debug 

        fp = Path(txt)
        if fp.suffix == '.csv' or fp.suffix =='.txt':
            self.rti.create_table_from_file(list_fp=fp) #CRollTableInterface
        else:
            self.rti.create_table_from_text_entry(text = txt)#''' CRollTableInterface

    def del_table(self, table_id: str, RollTables_filtered: list[CRollTable]):
        removed, _ = self.rti.remove_table_from_library(table_id)#CRollTableInterface
        if removed: 
            return self._remove_table(table_id, RollTables_filtered)  #CTableLibrary    

    def _remove_table(self, table_id:str, RollTables_filtered:list[CRollTable]):
        #rt: CRollTable
        for rt in RollTables_filtered: 
            if rt.get_id() == table_id:
                self.RollTables.remove(rt) 
        return self.RollTables 

    
    def add_tags(self, new_tags: str, rt: CRollTable):
        rt.tags.extend(new_tags.split(','))
        self._update_json(rt) 

    def remove_tags(self, rt: CRollTable):
        rt.tags = [] 
        self._update_json(rt)  

    def _update_json(self, rt: CRollTable):
        self.rti.update_json(id = rt.get_id(), updated_table= rt.refresh_me()) 
                  
    def _matches_search(self, search: str, input_tables: list[CRollTable] = None): #pass in None for first call, re pass in the output for sequential calls to filter down with more terms
        filtered_RollTables = []

        search_set = self.RollTables if input_tables is None else input_tables
        #rt: CRollTable
        for rt in search_set:  
            if rt.matches_txt(txt = search):    # only tables matching the txt -non case sensitive- will be displayed others hidden. 
                filtered_RollTables.append(rt)
        return filtered_RollTables 

#~

'''
def main(): 
    CTableLibrary()  

if __name__ == "__main__":
    main()'''

