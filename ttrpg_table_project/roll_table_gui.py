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
        input_password = st.text_input(label='Dev Password', type='password', key='3') 
        password = 'W1z@rd5'  
        password_entered = False
        if password == input_password:
             password_entered = True
        if password_entered:
            new_table_txt = st.text_input(label = 'Table entry:     Delimeter include the first \';\' and every \',\' afterwards e.g - Table Name; entry 1, entry 2, entry 3, entry 4', type='default', key='2')
            if st.button("Create New Table", key='4'): 
                self.tl._create_new_table(txt = new_table_txt)  #CTableLibrary
                st.rerun() 
        
        RollTables_filtered = self._search_bar(search_text) 
        self._display_tables(RollTables_filtered, password_entered)      
    


    def _search_bar(self, search_input: str):
            items = search_input.split(' ')
            #RollTables_filtered = self.tl.matches_search(search_input)  #CTableLibrary
            RollTables_filtered = [] 
            for i in items: 
                RollTables_filtered = self.tl.matches_search(i, RollTables_filtered)

            return RollTables_filtered    

    def _display_tables(self, RollTables_filtered: list, password_entered = False): #displayes given tables, enalbes control of what tables are displayed.
        for rt in RollTables_filtered:  #CRolTable
            self._GUI_fragment_roll_display_print(rt)  

            self._GUI_fragment_tags(rt, password_entered)

            self._GUI_fragment_del(rt, RollTables_filtered, password_entered) 

    def _GUI_fragment_del(self, rt: CRollTable, RollTables_filtered: list, password_entered = False):#""" 
            if password_entered:
                if st.button("Delete Table", key=rt.get_id()+'5'):
                    table_id = rt.get_id() #CRolTable
                    self.tl.del_table(table_id, RollTables_filtered) 
                    st.rerun() 

    def _GUI_fragment_tags(self, rt: CRollTable, password_entered = False):
        if password_entered: 
            new_tags = st.text_input(label='Enter New Tags: Delimeter is \',\' e.g Tag 1, Tag 2', type='default', key=rt.get_id()+'6') 
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
                        text = rt.markdown_render(task = 'output_txt') #CRolTable 
                        st.markdown(text)  
    
            st.download_button("Print md", key=rt.get_id()+'3', data = rt.markdown_render(task='output_txt_wth_header'), file_name=f"{rt.name}.md", mime="text/markdown")    

 

def main():
    CGUI_streamlit()  

if __name__ == "__main__":
    main()
