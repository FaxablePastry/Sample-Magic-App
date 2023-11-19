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
        self.show_previous_game()

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
            player_name_dropdown = DropDown(items=['Benas', 'Evan', 'Jed', 'Nils','Bev'], include_placeholder=True, placeholder='Choose a Player')
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
      
    def button_4_copy_click(self, **event_args):
        open_form('CommanderStats')
 
    def button_5_click(self, **event_args):
        open_form('PlayerPositions')

    def get_commander_names_from_table(self):
        commander_names = []
        
        # Fetch the commander names from the "commanders" table
        records = app_tables.commanders.search()
        for record in records:
            commander_name = record['Commander']
            commander_names.append(commander_name)

        # Sort the commander names alphabetically
        commander_names.sort()
        
        return commander_names

    def button_4_click(self, **event_args):
        # Retrieve all rows from the match_results table
        all_rows = app_tables.match_results.search()
    
        # Find the maximum game_ID
        last_used_game_ID = max(row['game_ID'] for row in all_rows) if all_rows else 0
    
        # Iterate over the rows in the flow panel and save the values to the table
        for row_panel in self.flow_panel_1.get_components():
            player_name = row_panel.get_components()[0].selected_value
            commander_name = row_panel.get_components()[1].selected_value
            player_position = int(row_panel.get_components()[2].selected_value)  # Convert to integer
            player_count = int(self.drop_down_1.selected_value)
    
            # Increment the game_ID
            new_game_ID = last_used_game_ID + 1
    
            # Save the values to the table
            app_tables.match_results.add_row(Player=player_name, Commander=commander_name, PlayerPosition=player_position, PlayerCount=player_count, game_ID=new_game_ID)
    
        # Clear the form fields
        self.clear_form_fields()
        self.show_previous_game()
        # Show a success message as a popup
        anvil.server.alert("Commander added successfully!", title="Success")

  
    def show_previous_game(self):
        # Retrieve all rows from the match_results table, ordered by 'game_ID' in descending order
        all_rows = app_tables.match_results.search(tables.order_by('game_ID', ascending=False))
    
        if all_rows:
            # Display details of the highest game_ID
            highest_game = all_rows[0]
            previous_game_text = "Previous Game:\n"
    
            # Loop through all rows with the highest game_ID
            for entry in all_rows:
                if entry['game_ID'] == highest_game['game_ID']:
                    previous_game_text += f"Player: {entry['Player']}, Commander: {entry['Commander']}, Position: {entry['PlayerPosition']}\n"
    
            self.previous_game.text = previous_game_text
        else:
            # No previous game found
            self.previous_game.text = "No previous game available."

    
    def clear_form_fields(self):
        # Clear the selected values of the dropdowns
        for row_panel in self.flow_panel_1.get_components():
            row_panel.get_components()[0].selected_value = None
            row_panel.get_components()[1].selected_value = None
            row_panel.get_components()[2].selected_value = None
        # Show a success message as a popup
        PlayerPositionsanvil.server.alert("Game added successfully!", title="Success")

    def button_6_click(self, **event_args):
    # Retrieve all rows from the match_results table, ordered by 'game_ID' in descending order
      all_rows = app_tables.match_results.search(tables.order_by('game_ID', ascending=False))
  
      if all_rows:
          # Find the highest game_ID
          highest_game = all_rows[0]
  
          # Delete all rows with the highest game_ID
          for entry in all_rows:
              if entry['game_ID'] == highest_game['game_ID']:
                  entry.delete_row()
  
          # Refresh the displayed game after deletion
          self.show_previous_game()