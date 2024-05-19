from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._anvil_designer import AddPlayerTemplate
from anvil import TextBox, DropDown
import time


class AddPlayer(AddPlayerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.selected_value = 0

  def button_1_click(self, **event_args):
    open_form("Home")

  def button_2_click(self, **event_args):
    open_form("AddMatch")

  def button_2_copy_click(self, **event_args):
    open_form('AddPlayer')

  def button_3_click(self, **event_args):
    open_form("AddCommander")

  def button_4_click(self, **event_args):
    open_form("CommanderStats")

  def button_5_click(self, **event_args):
    open_form("PlayerPositions")

  def get_player_names_from_table(self):
    player_names = []

    # Fetch the player names from the "names" table
    records = app_tables.names.search()
    for record in records:
      player_name = record["PlayerName"]
      player_names.append(player_name)

    # Sort the player names alphabetically
    player_names.sort()

    return player_names


  def add_player_button_click(self, **event_args):
    player_name = self.player_name_textbox.text.strip()
            
    if player_name:
        # Check if the player name already exists
        existing_player = app_tables.names.get(player_name=player_name)
        if existing_player:
            alert("Player name already exists.", title="Error")
        else:
            # Add the new player name to the "names" table
            app_tables.names.add_row(player_name=player_name)
            alert("Player added successfully!", title="Success")
            self.player_name_textbox.text = ""
    else:
        alert("Player name cannot be empty.", title="Error")


  def clear_form_fields(self):
    # Clear the selected values of the dropdowns
    for row_panel in self.flow_panel_1.get_components():
      row_panel.get_components()[0].selected_value = None
      row_panel.get_components()[1].selected_value = None
      row_panel.get_components()[2].selected_value = None
    # Show a success message as a popup