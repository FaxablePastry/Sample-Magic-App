from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.tables import app_tables
from ._anvil_designer import PlayerPositionsTemplate
class PlayerPositions(PlayerPositionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.form_show()

  def calculate_player_stats(self):
      player_stats = []
  
      # Retrieve all the records from the match_results table
      records = app_tables.match_results.search()
  
      # Count the games played and games won for each player
      player_stats_dict = {}
      player_winstreaks = {}  # Dictionary to track winstreaks
      for record in records:
          player = record['Player']
          player_position = record['PlayerPosition']
          player_count = record['PlayerCount']
  
          if player not in player_stats_dict:
              player_stats_dict[player] = {'games_played': 0, 'games_won': 0, 'points': 0}
              player_winstreaks[player] = {'current_winstreak': 0, 'longest_winstreak': 0}
  
          player_stats_dict[player]['games_played'] += 1
          if player_position == 1:
              player_stats_dict[player]['games_won'] += 1
              player_winstreaks[player]['current_winstreak'] += 1
              # Check if the current winstreak exceeds the longest winstreak
              if player_winstreaks[player]['current_winstreak'] > player_winstreaks[player]['longest_winstreak']:
                  player_winstreaks[player]['longest_winstreak'] = player_winstreaks[player]['current_winstreak']
  
          # Calculate points based on player position and the number of players
          if player_position == 1 and player_count == 4:
              player_stats_dict[player]['points'] += 6
          elif player_position == 2 and player_count == 4:
              player_stats_dict[player]['points'] += 4
          elif player_position == 3 and player_count == 4:
              player_stats_dict[player]['points'] += 2
          elif player_position == 4 and player_count == 4:
              player_stats_dict[player]['points'] += 1
          elif player_position == 1 and player_count == 3:
              player_stats_dict[player]['points'] += 5
          elif player_position == 2 and player_count == 3:
              player_stats_dict[player]['points'] += 3
          elif player_position == 3 and player_count == 3:
              player_stats_dict[player]['points'] += 1
  
      # Calculate the win rate and include winstreak information for each player
      for player, stats in player_stats_dict.items():
          games_played = stats['games_played']
          games_won = stats['games_won']
          win_rate = (games_won / games_played) * 100 if games_played > 0 else 0
          win_rate = round(win_rate, 2)
          player_points = stats['points']
  
          # Include winstreak and points information in the player statistics
          player_stat = {
              'Player': player,
              'GamesPlayed': games_played,
              'GamesWon': games_won,
              'WinRate': win_rate,
              'Points': player_points,
              'CurrentWinstreak': player_winstreaks[player]['current_winstreak'],
              'LongestWinstreak': player_winstreaks[player]['longest_winstreak']
          }
          player_stats.append(player_stat)
          print(f"{player}: Points = {player_points}")
      # Sort the player_stats list by Points and then by WinRate in descending order
      player_stats.sort(key=lambda x: (x['Points'], x['WinRate']), reverse=True)
  
      return player_stats


  def populate_player_positions_repeating_panel(self):
      # Retrieve all the records from the match_results table
      records = app_tables.match_results.search()
      player_stats = self.calculate_player_stats()
  
      # Create a dictionary to count player positions
      player_positions = {}
      for record in records:
          player = record['Player']
          position = record['PlayerPosition']
          
          if player not in player_positions:
              player_positions[player] = {1: 0, 2: 0, 3: 0, 4: 0}
          
          player_positions[player][position] += 1
      
      # Sort the player_positions dictionary by the count of first places (position 1)
      sorted_player_positions = dict(sorted(player_positions.items(), key=lambda item: item[1][1], reverse=True))
      
      # Create a list of dictionaries for the RepeatingPanel
      data = []
      for player, positions in sorted_player_positions.items():
          data.append({
              'Player': player,
              '1st Place': positions[1],
              '2nd Place': positions[2],
              '3rd Place': positions[3],
              '4th Place': positions[4]
          })
      # Set the RepeatingPanel items to the list of dictionaries
      data = [{'column_1': player, 'column_2': positions[1], 'column_3': positions[2], 'column_4': positions[3], 'column_5': positions[4], 'column_6':player_stats[player_points] } for player, positions in sorted_player_positions.items()]
      self.repeating_panel_1.items = data

  
  def form_show(self, **event_args):
      self.calculate_player_stats()
      self.populate_player_positions_repeating_panel()

  def button_1_click(self, **event_args):
      open_form('Home')

  def button_2_click(self, **event_args):
      open_form('AddMatch')

  def button_3_click(self, **event_args):
      open_form('AddCommander')

  def button_4_click(self, **event_args):
      open_form('CommanderStats')


  def button_5_click(self, **event_args):
      open_form('PlayerPositions')