import streamlit as st      #python -m streamlit run roll_table_gui.py 
from roll_table_reader_base import CTableLibrary, CRollTable


class CGUI_streamlit:
    def __init__(self):
        self.tl = CTableLibrary()

        self.main_page()

    def main_page(self):
        st.markdown("# ROLL TABLE LIBRARY") 
        self.gui_main() #tables and search bar
 
    def gui_main(self):
       
        search_text = st.text_input(label='Search', type='search', key='1') 
        new_table_txt = st.text_input(label = 'Table entry', type='default', key='2')
        if st.button("Create New Table", key='4'):
            self.tl._create_new_table(txt = new_table_txt)  #CTableLibrary
            st.rerun() 

        RollTables_filtered = self.tl._matches_search(search_text)  #CTableLibrary
        self._display_tables(RollTables_filtered)        

    def _display_tables(self, RollTables_filtered: list): #displayes given tables, enalbes control of what tables are displayed.
        for rt in RollTables_filtered:  #CRolTable
            self._GUI_fragment_roll_display_print(rt)  

            self._GUI_fragment_tags(rt)

            self._GUI_fragment_del(rt, RollTables_filtered) 

    def _GUI_fragment_del(self, rt: CRollTable, RollTables_filtered: list):#""" 
            if st.button("Delete Table", key=rt.get_id()+'5'):
                table_id = rt.get_id() #CRolTable
                self.tl.del_table(table_id, RollTables_filtered) 
                st.rerun() 

    def _GUI_fragment_tags(self, rt: CRollTable):
        new_tags = st.text_input(label='Enter New Tags', type='default', key=rt.get_id()+'6') 
        if st.button("Modify Tags", key=rt.get_id()+'4'):
            rt.add_tags(new_tags) #CRolTable
            #TODO: modify the json at CRollTable level
            st.rerun() 

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

 

def main():
    CGUI_streamlit()  

if __name__ == "__main__":
    main()

