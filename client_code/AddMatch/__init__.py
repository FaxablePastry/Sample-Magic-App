from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._anvil_designer import AddMatchTemplate
from anvil import TextBox, DropDown

class AddMatch(AddMatchTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.selected_value = 0
        self.drop_down_1.set_event_handler('change', self.drop_down_1_change)
        self.update_dropdowns()

    def drop_down_1_change(self, **event_args):
        selected_value = self.drop_down_1.selected_value
        
        if selected_value is not None:
            self.selected_value = int(selected_value)
        
        print("Selected Value:", self.selected_value)
        
        self.update_dropdowns()

    def update_dropdowns(self):
        print("Update Dropdowns: Selected Value:", self.selected_value)
        
        self.flow_panel_1.clear()
        
        # Fetch the commander names from the "commanders" table
        commander_names = self.get_commander_names_from_table()
        
        # Create rows and add dropdowns to each row
        for row in range(self.selected_value):
            row_panel = FlowPanel(role="row-panel")
            
            # Create dropdowns for player name, commander name, and player position
            player_name_dropdown = DropDown(items=['Benas', 'Evan', 'Jed', 'Nils'], include_placeholder=True, placeholder='Choose a Player')
            commander_name_dropdown = DropDown(items=commander_names, include_placeholder=True, placeholder='Choose a Commander')
            player_position_dropdown = DropDown(items=['1', '2', '3', '4'], include_placeholder=True, placeholder='Position')
            
            # Add the dropdowns to the row panel
            row_panel.add_component(player_name_dropdown)
            row_panel.add_component(commander_name_dropdown)
            row_panel.add_component(player_position_dropdown)
            
            self.flow_panel_1.add_component(row_panel)

    def text_box_1_pressed_enter(self, **event_args):
        pass

    def button_1_click(self, **event_args):
        open_form('Home')

    def button_2_click(self, **event_args):
        open_form('AddMatch')

    def button_3_click(self, **event_args):
        open_form('AddCommander')
    
    def get_commander_names_from_table(self):
        commander_names = []
        
        # Fetch the commander names from the "commanders" table
        records = app_tables.commanders.search()
        for record in records:
            commander_name = record['Commander']
            commander_names.append(commander_name)
        
        return commander_names

    def button_4_click(self, **event_args):
        # Iterate over the rows in the flow panel and save the values to the table
        for row_panel in self.flow_panel_1.get_components():
            player_name = row_panel.get_components()[0].selected_value
            commander_name = row_panel.get_components()[1].selected_value
            player_position = int(row_panel.get_components()[2].selected_value)  # Convert to integer
          
            # Save the values to the table
            app_tables.match_results.add_row(Player=player_name, Commander=commander_name, PlayerPosition=player_position)
              # Clear the form fields
        self.clear_form_fields()
    
    def clear_form_fields(self):
        # Clear the selected values of the dropdowns
        for row_panel in self.flow_panel_1.get_components():
            row_panel.get_components()[0].selected_value = None
            row_panel.get_components()[1].selected_value = None
            row_panel.get_components()[2].selected_value = None