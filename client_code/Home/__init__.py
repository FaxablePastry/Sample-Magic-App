from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.data_grid_1.items = self.get_commander_stats()
        self.calculate_commander_win_rates()  # Call the method here
        self.form_show()
        self.populate_data_grid()
        self.other_form()

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

            # Create a dictionary with the commander statistics
            commander_stat = {
                'Commander': commander,
                'GamesPlayed': games_played,
                'GamesWon': games_won
            }
            commander_stats.append(commander_stat)

        return commander_stats

  
    def populate_data_grid(self):
        commander_stats = self.get_commander_stats()
        print(f"Commander stats: {commander_stats}")  # Print the commander statistics
    
        # Clear existing rows in the data grid
        self.data_grid_1.items = []
    
        # Populate data grid with commander statistics
        for stat in commander_stats:
            print(f"Processing stat: {stat}")  # Print the current stat being processed
            row = {
                'Commander': stat['Commander'],
                'GamesPlayed': stat['GamesPlayed'],
                'GamesWon': stat['GamesWon']
            }
    
            # Calculate and add WinRate if GamesPlayed and GamesWon are present
            if 'GamesPlayed' in stat and 'GamesWon' in stat:
                games_played = stat['GamesPlayed']
                games_won = stat['GamesWon']
                win_rate = self.calculate_win_rate(games_played, games_won)
                row['WinRate'] = win_rate
    
            print(f"Appending row: {row}")  # Print the row being appended to the data grid
            self.data_grid_1.items.append(row)
          
        print(f"Data grid items: {self.data_grid_1.items}")  # Print the items bound to the data grid



    def form_show(self, **event_args):
        commander_stats = self.get_commander_stats()
        print(commander_stats)
        self.data_grid_1.items = commander_stats
      
    def other_form(self, **event_args):
      print("Form is being shown")  # Add this print statement
      self.populate_data_grid()

    def button_1_click(self, **event_args):
        open_form('Home')

    def button_2_click(self, **event_args):
        open_form('AddMatch')

    def button_3_click(self, **event_args):
        open_form('AddCommander')
