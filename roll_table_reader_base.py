
import os 
import json
from pathlib import Path 
import random
from mdutils.mdutils import MdUtils 
import streamlit as st   #python -m streamlit run roll_table_reader_base.py


class CTableLibrary: #contains an list of CRollTables
    def __init__(self, fp: Path):
        self.table_dict = self._open_dict(fp) 
        self.RollTables = []
        self._Rolltable_Loader() 

    def _open_dict(self, fp: Path):
            if fp.is_file():  
                with open(fp, 'r') as f: 
                    loaded_dict = json.load(f) 
    
                return loaded_dict  
            else:
                #print(f"File {fp} doesn't exist. Giving empty dict")   
                return {} 
            
    def _Rolltable_Loader(self):
        #load the tables from self.table_dict one at a time creating a list of CRolltable that holds each of the features of the dict
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

        if render_type == 'md': 
            for rt in self.RollTables:
                    rt.markdown_render() 
        if render_type == 'GUI':
            #st.markdown("# ROLL TABLE LIBRARY") 
            search_text = st.text_input(label='Search', type='search') 
            RollTables = self._matches_search(search_text)  
            self.display_tables(RollTables)

                #Stack all tables together, add a search bar that searches name and tags of the CRollTable, 
                # only tables matching the search -non case sensitive- will be displayed others hidden.  
    
    def display_tables(self, RollTables: list):
        for rt in RollTables:
                        rt._GUI_fragment() 
    
    def _matches_search(self, search: str):
        #search = search.lower() 
        filtered_RollTables = []
        for rt in self.RollTables:  
            if rt.matches_txt(txt = search):  
                filtered_RollTables.append(rt)
        return filtered_RollTables



    #search rolltable names

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


    def matches_txt(self, txt: str):
        txt = txt.lower()
        if txt in self.name.lower(): 
            return True
        if self.tags is not None: 
            for tag in self.tags:  
                if txt in tag.lower():
                    return True 
        return False

    def get_name(self): #str
        return self.name
    def get_tags(self): #list
        return self.tags 

    def markdown_render(self, create_file=True, output_txt=False):
        md = MdUtils(file_name=self.name) 
        t_header = not output_txt
        if t_header:
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
        
        if output_txt:
            return md.get_md_text()
        
        if create_file:
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
        tog = len(mlist) > 0 
        count = 0
        for e in mlist:
            if count == len(mlist)-1: 
                mstring += e
            else:
                 mstring += e + ", "
            count +=1 
                 
        return mstring

    def _roll(self):
        #genrate a number from 0 to len(self.entries)
        max = len(self.entries) -1
        return random.randint(0, max)

    def _roll_value(self, n):
        return self._unpack_list(self.entries[n]['results'])
    
    def _GUI_fragment(self): 

        st.markdown(f"## {self.name}")
        tab = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        st.markdown(f"*Tags: {self._unpack_list(self.tags)}{tab}-{tab}Dice Type: {self.diceType}*") 

        if st.button("🎲 Roll", key=self.id+'1'): 
            
            st.write(self._roll_value(self._roll())) 

        if st.button("Display Table", key=self.id+'2'): 
                    text = self.markdown_render(create_file = False, output_txt = True)
                    st.markdown(text)  

        if st.button("Print md", key=self.id+'3'): 
             self.markdown_render() 

    

def main():
    fp = Path("./tables/rollTableLibrary.json")
    tl = CTableLibrary(fp) 

    tl.render(render_type = 'GUI') 

if __name__ == "__main__":
    main()

