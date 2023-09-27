from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
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

   
    def populate_data_grid(self):
        try:
            commander_stats = self.get_commander_stats()
            stats_text = ""
            for stat in commander_stats:
                stats_text += f"{stat['Commander']}, Played: {stat['GamesPlayed']}, Won: {stat['GamesWon']}, Win Rate: {stat['WinRate']}%\n"
    
            self.text_box_1.text = stats_text
        except Exception as e:
            print(f"Error occurred while populating data grid: {str(e)}")


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


    def populate_player_data_grid(self):
        try:
            commander_stats = self.get_commander_stats()
            player_stats = self.calculate_player_stats()
            stats_text = ""
            for stat in player_stats:
                stats_text += f"{stat['Player']}, Played: {stat['GamesPlayed']}, Won: {stat['GamesWon']}, Win Rate: {stat['WinRate']:.2f}%\n"
    # Sort the commander_stats list alphabetically by Commander
            commander_stats.sort(key=lambda x: x['Commander'])
    
            stats_text_alphabetical = ""
            for stat in commander_stats:
                stats_text_alphabetical += f"{stat['Commander']}, Played: {stat['GamesPlayed']}, Won: {stat['GamesWon']}, Win Rate: {stat['WinRate']}%\n"
    
            self.player_textbox.text = stats_text
            self.text_box_2.text = stats_text_alphabetical
        except Exception as e:
            print(f"Error occurred while populating player data grid: {str(e)}")

      
    def populate_commander_played_data(self):
        try:
            commander_stats = self.get_commander_stats()
    
            # Sort the commander_stats list by the number of times a deck has been played in descending order
            commander_stats.sort(key=lambda x: x['GamesPlayed'], reverse=True)
    
            stats_text = ""
            for stat in commander_stats:
                commander = stat['Commander']
                games_played = stat['GamesPlayed']
                games_won = stat['GamesWon']
                win_rate = stat['WinRate']
    
                stats_text += f"{commander}, Played: {games_played}, Won: {games_won}, Win Rate: {win_rate}%\n"
    
            self.commander_textbox.text = stats_text
        except Exception as e:
            print(f"Error occurred while populating commander played data: {str(e)}")
    
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

    def populate_player_grid(self):
      try:
            player_stats = self.calculate_player_stats()
            data = [{'player_name': stat['Player'], 'player_played': stat['GamesPlayed'], 'player_won': stat['GamesWon'], 'player_rate': f"{stat['WinRate']:.2f}%"} for stat in player_stats]
            self.repeating_panel_2.items = data
      except Exception as e:
            print(f"Error occurred while populating player data grid: {str(e)}")

          
    def get_colour_counts(self):
        color_counts = {'White': 0, 'Blue': 0, 'Black': 0, 'Red': 0, 'Green': 0, 'Colourless': 0}
    
        # Retrieve all the records from the commanders table
        records = app_tables.commanders.search()
    
        # Count the colors for each commander
        for record in records:
            white = record['White']
            blue = record['Blue']
            black = record['Black']
            red = record['Red']
            green = record['Green']
            colourless = record['Colourless']
            # Update the total counts
            color_counts['White'] += white
            color_counts['Blue'] += blue
            color_counts['Black'] += black
            color_counts['Red'] += red
            color_counts['Green'] += green
            color_counts['Colourless'] += colourless
    
        return color_counts

    def display_colour_count(self):
        try:
            color_counts = self.get_colour_counts()
            stats_text = ""
            for color, count in color_counts.items():
                stats_text += f"{color}: {count}\n"
    
            self.colour_counts.text = stats_text
        except Exception as e:
            print(f"Error occurred while populating colour data: {str(e)}")



  
    def display_most_played_and_best_deck(self):
        try:
            records = app_tables.match_results.search()
    
            player_stats = {}
            deck_play_counts = {}
            deck_win_counts = {}
    
            for record in records:
                player = record['Player']
                deck = record['Commander']
                player_position = record['PlayerPosition']
    
                if player not in player_stats:
                    player_stats[player] = {
                        'total_played': 0,
                        'position_1_count': 0,
                        'win_rate': 0,
                        'decks': {}
                    }
    
                if deck not in player_stats[player]['decks']:
                    player_stats[player]['decks'][deck] = {
                        'played_count': 0,
                        'win_count': 0,
                        'win_rate': 0
                    }
    
                player_stats[player]['decks'][deck]['played_count'] += 1
                player_stats[player]['total_played'] += 1
    
                if player_position == 1:
                    player_stats[player]['decks'][deck]['win_count'] += 1
                    player_stats[player]['position_1_count'] += 1
    
            for player, stats in player_stats.items():
                games_played = stats['total_played']
                games_won = stats['position_1_count']
                win_rate = (games_won / games_played) * 100 if games_played > 0 else 0
                stats['win_rate'] = win_rate
    
            most_played_decks = {}
            best_performing_decks = {}
    
            for player, stats in player_stats.items():
                most_played_deck = max(stats['decks'], key=lambda x: stats['decks'][x]['played_count'])
                win_rate_most_played = (stats['decks'][most_played_deck]['win_count'] / stats['decks'][most_played_deck]['played_count']) * 100
                played_count_most_played = stats['decks'][most_played_deck]['played_count']
                most_played_decks[player] = (most_played_deck, played_count_most_played, win_rate_most_played)
    
                best_performing_deck = max(stats['decks'], key=lambda x: (stats['decks'][x]['win_count'] / stats['decks'][x]['played_count']) * 100)
                win_rate_best_performing = (stats['decks'][best_performing_deck]['win_count'] / stats['decks'][best_performing_deck]['played_count']) * 100
                played_count_best_performing = stats['decks'][best_performing_deck]['played_count']
                best_performing_decks[player] = (best_performing_deck, played_count_best_performing, win_rate_best_performing)
    
            # Display the player's most played deck and its win rate
            stats_text = ""
            for player, (most_played_deck, played_count_most_played, win_rate_most_played) in most_played_decks.items():
                best_performing_deck, played_count_best_performing, win_rate_best_performing = best_performing_decks[player]
                stats_text += f"Player: {player}\n"
                stats_text += f"Most Played Deck: {most_played_deck}, Played: {played_count_most_played}, Win Rate: {win_rate_most_played:.2f}%\n"
                stats_text += f"Best Performing Deck: {best_performing_deck}, Played: {played_count_best_performing}, Win Rate: {win_rate_best_performing:.2f}%\n"
                stats_text += "\n"
    
            self.player_deck.text = stats_text
    
        except Exception as e:
            print(f"Error occurred while displaying player deck stats: {str(e)}")



    def form_show(self, **event_args):
        self.populate_data_grid()
        self.populate_player_data_grid()
        self.populate_commander_played_data()
        self.get_colour_stats()
        self.display_most_played_and_best_deck()
        self.display_colour_count()
        self.populate_commander_grid()
        self.populate_player_grid()

    def button_1_click(self, **event_args):
        open_form('Home')

    def button_2_click(self, **event_args):
        open_form('AddMatch')

    def button_3_click(self, **event_args):
        open_form('AddCommander')

    def text_box_2_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

