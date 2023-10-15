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

        if player not in player_stats_dict:
            player_stats_dict[player] = {'games_played': 0, 'games_won': 0}
            player_winstreaks[player] = {'current_winstreak': 0, 'longest_winstreak': 0}

        player_stats_dict[player]['games_played'] += 1
        if player_position == 1:
            player_stats_dict[player]['games_won'] += 1
            player_winstreaks[player]['current_winstreak'] += 1
            # Check if the current winstreak exceeds the longest winstreak
            if player_winstreaks[player]['current_winstreak'] > player_winstreaks[player]['longest_winstreak']:
                player_winstreaks[player]['longest_winstreak'] = player_winstreaks[player]['current_winstreak']
        else:
            player_winstreaks[player]['current_winstreak'] = 0  # Reset winstreak on loss

    # Calculate the win rate and include winstreak information for each player
    for player, stats in player_stats_dict.items():
        games_played = stats['games_played']
        games_won = stats['games_won']
        win_rate = (games_won / games_played) * 100 if games_played > 0 else 0
        win_rate = round(win_rate, 2)

        # Include winstreak information in the player statistics
        player_stat = {
            'Player': player,
            'GamesPlayed': games_played,
            'GamesWon': games_won,
            'WinRate': win_rate,
            'CurrentWinstreak': player_winstreaks[player]['current_winstreak'],
            'LongestWinstreak': player_winstreaks[player]['longest_winstreak']
        }
        player_stats.append(player_stat)

    # Sort the player_stats list by WinRate in descending order
    player_stats.sort(key=lambda x: x['WinRate'], reverse=True)

    return player_stats

  def display_player_positions(self):
    # Retrieve all the records from the match_results table
    records = app_tables.match_results.search()
    
    # Create a dictionary to count player positions
    player_positions = {}
    
    # Count player positions
    for record in records:
        player = record['Player']
        position = record['PlayerPosition']
        
        if player not in player_positions:
            player_positions[player] = {1: 0, 2: 0, 3: 0, 4: 0}  # Initialize positions with 0 counts
        
        player_positions[player][position] += 1
    
    # Sort the player_positions dictionary by the count of first places (position 1)
    sorted_player_positions = dict(sorted(player_positions.items(), key=lambda item: item[1][1], reverse=True))
    
    # Create a string to display player positions
    player_positions_text = ""
    
    for player, positions in sorted_player_positions.items():
        player_positions_text += f"Player: {player}, Positions: "
        for position in range(1, 5):  # Iterate from 1 to 4
            count = positions.get(position, 0)  # Get the count for the position or default to 0 if not found
            player_positions_text += f"{position}: {count}, "
        player_positions_text = player_positions_text.rstrip(', ')  # Remove the trailing comma and space
        player_positions_text += "\n"
    
    # Set the text of the label to display player positions
    self.label_1.text = player_positions_text

  def display_player_positions_data_grid(self):
      # Retrieve all the records from the match_results table
      print("Getting the player data")
      records = app_tables.match_results.search()

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

      # Clear the RepeatingPanel
      self.repeating_panel_1.items = []
      print(sorted_player_positions)

      # Populate the RepeatingPanel
      for player, positions in sorted_player_positions.items():
          row = {'column_1': player, 'column_2': positions[1], 'column_3': positions[2], 'column_4': positions[3], 'column_5': positions[4]}
          self.repeating_panel_1.items.append(row)

  
  def form_show(self, **event_args):
      self.display_player_positions()
      self.display_player_positions_data_grid()

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