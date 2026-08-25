

#Junk

    '''def _html_fragment(self): 

        template = Template("""
        <div class="roll-table"
            data-table-id="{{ table_id }}">

            <h2>{{ table_name }}</h2>

            {{ roll_button }}

            {{ roll_script }}

            {{ roll_display }} 

        </div>
        """)

        return template.render(
            table_id=self.id,
            table_name=self.name,
            roll_button=self._html_roll_button(),
            roll_script=self._html_roll_script(),
            roll_display=self._html_display_roll()
        )

    def _html_roll_button(self): 
        template = Template("""
            <button
                class="roll-btn"
                data-table-id="{{ table_id }}">
                🎲 Roll
            </button>
            """) 

        return template.render(table_id=self.id)

    def _html_display_roll(self): 
        template = Template("""
        <div
            class="roll-result"
            id="result-{{ table_id }}">

            No roll yet     

        </div>
        """) #

        return template.render(
            table_id=self.id
        )

    def _html_roll_script(self):
        template = Template("""
        <script>
        function roll_{{ table_id_safe }}()
        {
            const maxRoll = {{ max_roll }};
            const roll = Math.floor(Math.random() * maxRoll);

            console.log(
                "Table:",
                "{{ table_name }}",
                "Roll:",
                roll
            );
        }
        </script>
        """)

        return template.render(
            table_id_safe=self.id.replace("-", "_"),
            table_name=self.name,
            max_roll=len(self.entries)-1
        )'''