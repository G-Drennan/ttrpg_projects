import streamlit as st      #python -m streamlit run roll_table_gui.py
from roll_table_reader_base import CTableLibrary, CRollTable



class CGUI_streamlit:
    def __init__(self):
        self.tl = CTableLibrary()

        self.main_page()

    def main_page(self):
        st.markdown("# ROLL TABLE LIBRARY") 
        self._gui_main() #tables and search bar
 
    def _gui_main(self):
       
        search_text = st.text_input(label='Search', type='search', key='1')  
        input_password = st.text_input(label='Dev Password - required for adding tables, removing tables and editing tags.', type='password', key='3') 
        dev_mode_password = 'W1z@rd5'  
        self.password_entered = False
        if dev_mode_password == input_password:
             self.password_entered = True 
        if self.password_entered:
            new_table_txt = st.text_input(
                label="Create New Roll Table",
                placeholder="Table Name; Entry 1, Entry 2, Entry 3",
                key="2"
            )

            st.caption("""
            Format:

            • Manual entry: Table Name; Entry 1, Entry 2, Entry 3

            • File input: Enter the full file path.
            The file name will be used as the table name.

            • Text file (.txt): One entry per line.

            • CSV file (.csv): Entries only, no header required.


            """)            
            if st.button("Create New Table", key='4'): 
                self.tl._create_new_table(txt = new_table_txt)  #CTableLibrary
                st.rerun() 
        
        self._display_tables(self.tl.search_bar(search_text))    #CTableLibrary  
    

    def _display_tables(self, RollTables_filtered: list[CRollTable]): #displayes given tables - a list of #CRolTable-, enalbes control of what tables are displayed.
        for rt in RollTables_filtered:  #CRollTable
            self._GUI_fragment_roll_display_print(rt)  

            self._GUI_fragment_tags(rt)

            self._GUI_fragment_del(rt, RollTables_filtered) 

    def _GUI_fragment_del(self, rt: CRollTable, RollTables_filtered: list[CRollTable]):#""" #CRollTable 
            if self.password_entered:
                if st.button("Delete Table", key=rt.get_id()+'5'):
                    table_id = rt.get_id() #CRollTable
                    self.tl.del_table(table_id, RollTables_filtered) 
                    st.rerun() 

    def _GUI_fragment_tags(self, rt: CRollTable):#CRollTable 
        if self.password_entered: 
            new_tags = st.text_input(label='Enter New Tags: Delimeter is \',\' e.g Tag 1, Tag 2', type='default', key=rt.get_id()+'6') 
            if st.button("Modify Tags", key=rt.get_id()+'4'):
                self.tl.add_tags(new_tags, rt=rt) #CTableLibrary
                st.rerun() 

            if st.button("Remove Tags", key=rt.get_id()+'7'):
                self.tl.remove_tags(rt=rt)  #CTableLibrary
                st.rerun() 
    
    def _GUI_fragment_roll_display_print(self, rt: CRollTable):  #CRollTable 
    
            st.markdown(f"## {rt.name}")
            tab = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
            st.markdown(f"*Tags: {rt.get_unpacked_tags(rt.tags)}{tab}-{tab}Dice Type: {rt.rollExpression}*") #CRolTable
    
            if st.button("🎲 Roll", key=rt.get_id()+'1'): 
                
                st.write(rt.roll_value()) #CRollTable  
    
            if st.button("Display Table", key=rt.get_id()+'2'): 
                        text = rt.markdown_render(task = 'output_txt') #CRolTable 
                        st.markdown(text)  
    
            st.download_button("Print md", key=rt.get_id()+'3', data = rt.markdown_render(task='output_txt_wth_header'), file_name=f"{rt.name}.md", mime="text/markdown")    

 

def main():
    CGUI_streamlit()  

if __name__ == "__main__":
    main()
