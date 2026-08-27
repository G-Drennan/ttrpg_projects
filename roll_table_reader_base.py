
import os 
import json
from pathlib import Path 
import random
from mdutils.mdutils import MdUtils 
import streamlit as st      #python -m streamlit run roll_table_reader_base.py
from roll_table_generator import CRollTableInterface

class CGUI_streamlit:
    def __init__(self):
        self.tl = CTableLibrary()
        self.main_page()

    def main_page(self):
        st.markdown("# ROLL TABLE LIBRARY")
        self.tl.gui_main() #tables and search bar


class CTableLibrary:    #contains an list of CRollTables 
    def __init__(self, fp= Path( "./tables/rollTableLibrary.json")):
        self.rti = CRollTableInterface(fp=fp)  
        self.table_dict = self._open_roll_table_library(fp) 
        self.RollTables = []
        self._Rolltable_Loader() 

    def _open_roll_table_library(self, fp: Path):
            if fp.is_file():  
                with open(fp, 'r') as f: 
                    loaded_dict = json.load(f) 
    
                return loaded_dict  
            else:
                #print(f"File {fp} doesn't exist. Giving empty dict")   
                return {} 
            
    def _Rolltable_Loader(self):    #load the tables from self.table_dict one at a time creating a list of CRolltable 
        #first check the dict is a "type": "rollTableLibrary"
        d = self.table_dict
        if d['type'] == 'rollTableLibrary': 
            self._proccess_RolltableLibrary()

    def get_RollTables(self):
        return self.RollTables 

    def _proccess_RolltableLibrary(self):
        mlist = self.table_dict['tables'] #list of dicts
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

    def render(self,render_type: str):  #How the tables are displayed. 

        if render_type == 'md': 
            for rt in self.RollTables:
                    rt.markdown_render() 
        if render_type == 'GUI':    #Stack all tables together in st, add a search bar that searches name and tags of the CRollTable
            self.gui_main()

    def gui_main(self):
       
        search_text = st.text_input(label='Search', type='search') 
        RollTables = self._matches_search(search_text)  
        self.display_tables(RollTables)        
    
    def display_tables(self, RollTables: list): #displayes given tables, enalbes control of what tables are displayed.
        for rt in RollTables:  
            rt._GUI_fragment() 
            if st.button("Delete Table", key=rt.get_id()+'4'):
                self.rti.remove_table_from_library(self.id)
    
    def _matches_search(self, search: str):
        filtered_RollTables = []
        for rt in self.RollTables:  
            if rt.matches_txt(txt = search):    # only tables matching the txt -non case sensitive- will be displayed others hidden. 
                filtered_RollTables.append(rt)
                
        return filtered_RollTables

#~

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

    def markdown_render(self, create_file=True, output_txt=False):  #Either create a file or only write the table in md
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

    def _extract_enties(self):  #Puts enteries into a list for md
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
    
    def _GUI_fragment(self):  

        st.markdown(f"## {self.name}")
        tab = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        st.markdown(f"*Tags: {self._unpack_list(self.tags)}{tab}-{tab}Dice Type: {self.rollExpression}*") 

        if st.button("🎲 Roll", key=self.id+'1'): 
            
            st.write(self._roll_value(self._roll())) 

        if st.button("Display Table", key=self.id+'2'): 
                    text = self.markdown_render(create_file = False, output_txt = True)
                    st.markdown(text)  

        if st.button("Print md", key=self.id+'3'):  
             self.markdown_render() 
          

    

def main():
    CGUI_streamlit() 

if __name__ == "__main__":
    main()

