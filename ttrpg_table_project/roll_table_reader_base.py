
import json
from pathlib import Path 
import random
from mdutils.mdutils import MdUtils 
from roll_table_generator import CRollTableInterface 


#TODO: 4 add error handeling  
#TODO: Is CTableLibrary a Repository?  

class CRollTable:   #Holds data related to the table 
    def __init__(self,  name, columns, entries, id, description, tags, diceType, rangeMode, rollExpression, folderId, created_at):
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

        self.rti = CRollTableInterface()

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

    def markdown_render(self, task: str = 'create_file'):  #Either create a file or only write the table in md
        md = MdUtils(file_name=self.name) 
        if task == 'create_file' or task == 'output_txt_wth_header':
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
        
        if task == 'output_txt' or task == 'output_txt_wth_header':
            return md.get_md_text()
        
        if task == 'create_file':
            md.create_md_file()

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
        max = len(self.entries) -1
        return random.randint(0, max)

    def _roll_value(self, n):
        return self._unpack_list(self.entries[n]['results'])
    
#~

class CTableLibrary:    #contains an list of CRollTables
    def __init__(self, fp= Path( "./tables/rollTableLibrary.json")):
        self.rti = CRollTableInterface(fp=fp)  
        self.fp = fp
        self.RollTables = [] 
        self._Rolltable_Loader() 

    def _open_roll_table_library(self): 
            if self.fp.is_file():  
                with open(self.fp, 'r') as f: 
                    loaded_dict = json.load(f) 
    
                return loaded_dict  
            else:
                #print(f"File {fp} doesn't exist . Giving empty dict")   
                return {} 
            
    def _Rolltable_Loader(self):    #load the tables from self.table_dict one at a time creating a list of CRolltable 
        #first check the dict is a "type": "rollTableLibrary"
        d = self._open_roll_table_library() 
        if d['type'] == 'rollTableLibrary': 
            self._proccess_RolltableLibrary(d)

    def get_RollTables(self):
        return self.RollTables 

    def _proccess_RolltableLibrary(self, d: dict): 
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

        def _is_text_fp(): 
            if Path(txt).suffix == '.csv' or Path(txt).suffix =='.txt':
                return Path(txt).is_file()
            else:
                return False

        if _is_text_fp():
            fp = Path(txt) 
            self.rti.create_from_file(list_fp=fp) #CRollTableInterface
        else:
            self.rti.create_from_text_entry(text = txt)#''' CRollTableInterface

    def del_table(self, table_id: str, RollTables_filtered: list):
        removed, _ = self.rti.remove_table_from_library(table_id)#CRollTableInterface
        if removed: 
            return self._remove_table(table_id, RollTables_filtered)  #CTableLibrary    

    def _remove_table(self, table_id:str, RollTables_filtered:list):
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
                  
    def matches_search(self, search: str, input_tables: list = None): #pass in None for first call, re pass in the output for sequential calls to filter down with more terms
        filtered_RollTables = []
        
        if input_tables is None: #Assume whole list 
            for rt in self.RollTables:   
                filtered_RollTables.append(rt)
        else:
            for rt in input_tables:  
                if rt.matches_txt(txt = search):    # only tables matching the txt -non case sensitive- will be displayed others hidden. 
                    filtered_RollTables.append(rt)
                

        return filtered_RollTables 

#~

'''def main():
    CTableLibrary()  
    print(self.tl.matches_search("", RollTables_filtered))


if __name__ == "__main__":
    main()'''

