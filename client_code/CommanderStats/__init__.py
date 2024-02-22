from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.tables import app_tables
from ._anvil_designer import CommanderStatsTemplate
class CommanderStats(CommanderStatsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.form_show()

    def calculate_win_rate(self, games_played, games_won):
        if games_played == 0:
            return 0
        return (games_won / games_played) * 100

    def calculate_commander_win_rates(self):
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

        # Calculate and print the win rate for each commander
        for commander, stats in commanders.items():
            games_played = stats['games_played']
            games_won = stats['games_won']
            win_rate = self.calculate_win_rate(games_played, games_won)

            print(f"Commander: {commander}, Win Rate: {win_rate}")

    def get_commander_stats(self):
        commander_stats = []
    
        # Retrieve all the records from the match_results table
        records = app_tables.match_results.search()
        print(f"Number of records: {len(records)}")  # Print the number of records retrieved
    
        # Count the games played and games won for each commander
        commander_stats_dict = {}
        for record in records:
            commander = record['Commander']
            player_position = record['PlayerPosition']
    
            if commander not in commander_stats_dict:
                commander_stats_dict[commander] = {'games_played': 0, 'games_won': 0}
    
            commander_stats_dict[commander]['games_played'] += 1
            if player_position == 1:
                commander_stats_dict[commander]['games_won'] += 1
    
        # Calculate the win rate for each commander
        for commander, stats in commander_stats_dict.items():
            games_played = stats['games_played']
            games_won = stats['games_won']
            win_rate = (games_won / games_played) * 100 if games_played > 0 else 0
            win_rate = round(win_rate, 2)
    
            # Create a dictionary with the commander statistics
            commander_stat = {
                'Commander': commander,
                'GamesPlayed': games_played,
                'GamesWon': games_won,
                'WinRate': win_rate
            }
            commander_stats.append(commander_stat)
    
        # Sort the commander_stats list by WinRate in descending order
        commander_stats.sort(key=lambda x: x['WinRate'], reverse=True)
    
        return commander_stats



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

    
    def get_colour_stats(self):
        colour_stats = []
    
        # Retrieve all the records from the commanders table
        records = app_tables.commanders.search()
    
        # Extract the color combination for each commander
        for record in records:
            commander = record['Commander']
            white = record['White']
            blue = record['Blue']
            black = record['Black']
            red = record['Red']
            green = record['Green']
            colourless = record['Colourless']
    
            color_combination = []
            if white > 0:
                color_combination.append('White')
            if blue > 0:
                color_combination.append('Blue')
            if black > 0:
                color_combination.append('Black')
            if red > 0:
                color_combination.append('Red')
            if green > 0:
                color_combination.append('Green')
            if colourless > 0:
                color_combination.append('Colourless')
    
            colour_stat = {
                'Commander': commander,
                'ColorCombination': color_combination
            }
    
            colour_stats.append(colour_stat)


        print(colour_stats)
        return colour_stats
        
    def populate_commander_grid(self):
      try:
            commander_stats = self.get_commander_stats()
            data = [{'commander_name': stat['Commander'], 'commander_played': stat['GamesPlayed'], 'commander_won': stat['GamesWon'], 'commander_win': stat['WinRate']} for stat in commander_stats]
            self.repeating_panel_1.items = data
      except Exception as e:
            print(f"Error occurred while populating commander data grid: {str(e)}")



    def form_show(self, **event_args):
        self.populate_commander_grid()



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

    def button_7_click(self, **event_args):
      open_form('OneVOnes')

    def button_6_click(self, **event_args):
      open_form('ColourPage')