
import os 
import json
from pathlib import Path 
import random
from mdutils.mdutils import MdUtils 
import streamlit as st      #python -m streamlit run roll_table_reader_base.py
from roll_table_generator import CRollTableInterface


#TODO: 1 move st out of CTableLibrary and CRollTable 
#TODO: 2 add error handeling  
#TODO: 3 Is CTableLibrary a Repository?  


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

    def add_tags(self, new_tags: str):
        self.tags.extend(new_tags.split(','))
        self._update_json()

    def remove_tags(self):
        self.tags = []
        self._update_json()


    def _update_json(self):
        me = self.refresh_me()
        self.rti.update_json(id = self.id, updated_table= me) 


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
    


class CGUI_streamlit:
    def __init__(self):
        self.tl = CTableLibrary()
        #self.rti = CRollTableInterface() #should only know CTableLibrary, have that call the tables and interface 
        #self.rt = CRollTable #but each rolltable has its own buttons, should the GUI know the rolltables? 
        self.main_page()

    def main_page(self):
        st.markdown("# ROLL TABLE LIBRARY")
        self.tl.gui_main() #tables and search bar

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

    def gui_main(self):
       
        search_text = st.text_input(label='Search', type='search', key='1') 
        new_table_txt = st.text_input(label = 'Table entry', type='default', key='2')
        if st.button("Create New Table", key='4'):
            self._create_new_table(txt = new_table_txt)  #CTableLibrary
            st.rerun() 

        RollTables_filtered = self._matches_search(search_text)  #CTableLibrary
        self._display_tables(RollTables_filtered)        #CTableLibrary

    def _display_tables(self, RollTables_filtered: list): #displayes given tables, enalbes control of what tables are displayed.
        for rt in RollTables_filtered:  #CRolTable
            self._GUI_fragment_roll_display_print(rt)  

            self._GUI_fragment_tags(rt)

            #"""
            self._GUI_fragment_del(rt, RollTables_filtered) 
            st.rerun() 

    def _GUI_fragment_del(self, rt: CRollTable, RollTables_filtered: list):#""" 
            if st.button("Delete Table", key=rt.get_id()+'5'):
                            table_id = rt.get_id() #CRolTable
                            removed, _ = self.rti.remove_table_from_library(table_id)#CRollTableInterface
                            if removed:
                                return self._remove_table(table_id, RollTables_filtered)  #CTableLibrary

    def _GUI_fragment_tags(self, rt: CRollTable):
        new_tags = st.text_input(label='Enter New Tags', type='default', key=rt.get_id()+'6') 
        if st.button("Modify Tags", key=rt.get_id()+'4'):
            rt.add_tags(new_tags) #CRolTable
            #TODO: modify the json at CRollTable level
            st.rerun() #'''
        if st.button("Remove Tags", key=rt.get_id()+'7'):
            rt.remove_tags()
            st.rerun() 
    
    def _GUI_fragment_roll_display_print(self, rt: CRollTable):  
    
            st.markdown(f"## {rt.name}")
            tab = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            st.markdown(f"*Tags: {rt._unpack_list(rt.tags)}{tab}-{tab}Dice Type: {rt.rollExpression}*") #CRolTable
    
            if st.button("🎲 Roll", key=rt.get_id()+'1'): 
                
                st.write(rt._roll_value(rt._roll())) #CRolTable
    
            if st.button("Display Table", key=rt.get_id()+'2'): 
                        text = rt.markdown_render(create_file = False, output_txt = True) #CRolTable
                        st.markdown(text)  
    
            if st.button("Print md", key=rt.get_id()+'3'):  
                 rt.markdown_render() #CRolTable      


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
    

    def _remove_table(self, table_id:str, RollTables_filtered:list):
        for rt in RollTables_filtered: 
            if rt.get_id == table_id:
                self.RollTables.remove(rt) 
        return self.RollTables 
                  
    def _matches_search(self, search: str):
        filtered_RollTables = []
        for rt in self.RollTables:  
            if rt.matches_txt(txt = search):    # only tables matching the txt -non case sensitive- will be displayed others hidden. 
                filtered_RollTables.append(rt)
                
        return filtered_RollTables

#~

          

def main():
    CGUI_streamlit()  

if __name__ == "__main__":
    main()

