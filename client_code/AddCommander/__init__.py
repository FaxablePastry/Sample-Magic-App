from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._anvil_designer import AddCommanderTemplate

class AddCommander(AddCommanderTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.commander.set_event_handler('pressed_enter', self.commander_pressed_enter)
        self.white.set_event_handler('change', self.white_change)
        self.blue.set_event_handler('change', self.blue_change)
        self.black.set_event_handler('change', self.black_change)
        self.red.set_event_handler('change', self.red_change)
        self.green.set_event_handler('change', self.green_change)
        self.colourless.set_event_handler('change', self.colourless_change)
        self.builder.set_event_handler('change', self.builder_change)
        self.deck_button.set_event_handler('click', self.deck_button_click)
    
    def commander_pressed_enter(self, **event_args):
        pass

    def white_change(self, **event_args):
        pass

    def blue_change(self, **event_args):
        pass

    def black_change(self, **event_args):
        pass

    def red_change(self, **event_args):
        pass

    def green_change(self, **event_args):
        pass

    def colourless_change(self, **event_args):
        pass

    def builder_change(self, **event_args):
        pass

    def deck_button_click(self, **event_args):
        # Retrieve the values from the form components
        commander_name = self.commander.text
        white = self.white.checked
        blue = self.blue.checked
        black = self.black.checked
        red = self.red.checked
        green = self.green.checked
        colourless = self.colourless.checked
        builder = self.builder.selected_value
        
        # Save the values to the "commanders" table
        app_tables.commanders.add_row(
            Commander=commander_name,
            White=white,
            Blue=blue,
            Black=black,
            Red=red,
            Green=green,
            Colourless=colourless,
            Builder=builder
        )
        
        # Clear the form fields
        self.commander.text = ""
        self.white.checked = False
        self.blue.checked = False
        self.black.checked = False
        self.red.checked = False
        self.green.checked = False
        self.colourless.checked = False
        self.builder.selected_value = None

    def button_1_click(self, **event_args):
        open_form('Home')

    def button_2_click(self, **event_args):
        open_form('AddMatch')

    def button_3_click(self, **event_args):
        open_form('AddCommander')
