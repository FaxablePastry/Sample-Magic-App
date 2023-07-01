from ._anvil_designer import HomeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def calculate_win_rate(self, games_played, games_won):
    if games_played == 0:
        return 0
    return (games_won / games_played) * 100

  def calculate_commander_win_rates():
      commanders = {}
      
      # Retrieve all the records from the match_results table
      records = app_tables.match_results.search()
      
      # Iterate over the records and update the win rates for each commander
      for record in records:
          commander = record['Commander']
          player_position = record['PlayerPosition']
          
          # Increment the games played count for the commander
          commanders.setdefault(commander, {'games_played': 0, 'games_won': 0})
          commanders[commander]['games_played'] += 1
          
          # Increment the games won count if the player position is 1
          if player_position == 1:
              commanders[commander]['games_won'] += 1
      
      # Calculate and update the win rate percentage for each commander
      for commander, stats in commanders.items():
          games_played = stats['games_played']
          games_won = stats['games_won']
          win_rate = calculate_win_rate(games_played, games_won)
          
          # Update the win rate percentage in the commanders table
          commander_record = app_tables.commanders.get(Commander=commander)
          commander_record['Percentage'] = win_rate
      
      # Save the changes to the commanders table
      app_tables.commanders.update(records)
  
  
  def button_1_click(self, **event_args):
    open_form('Home')

  def button_2_click(self, **event_args):
    open_form('AddMatch')

  def button_3_click(self, **event_args):
    open_form('AddCommander')
