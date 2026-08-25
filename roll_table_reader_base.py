
import os 
import json
from pathlib import Path 

#from markdownify import markdownify #Converts HTML → Markdown.
from mdutils.mdutils import MdUtils 


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

    def render(self,render_type: str):

        if render_type is 'md': 
            for rt in self.RollTables:
                    rt.markdown_render()

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

    def markdown_render(self, ): 
        md = MdUtils(file_name=self.name)

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

        md.create_md_file()

    def _extract_enties(self):
        row_entries = []
        for d in self.entries:
            if d['minRoll'] is not d['maxRoll']:
                roll = str(d['minRoll']) + " - " + str(d['maxRoll'])
            else:
                roll = str(d['minRoll']) 
            row_entries.append(roll)

            result = self._unpack_list(d['results'])

            row_entries.append(result) 
        return row_entries 

    def _unpack_list(self, mlist):
        mstring = ""
        for e in mlist:
            mstring += e
        return mstring


      

def main():
    fp = Path("./tables/rollTableLibrary.json")
    tl = CTableLibrary(fp) 

    tl.render(render_type = 'md') 

if __name__ == "__main__":
    main()