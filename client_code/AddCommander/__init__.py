from ._anvil_designer import AddCommanderTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AddCommander(AddCommanderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    open_form('Home')

  def button_2_click(self, **event_args):
    open_form('AddMatch')

  def button_3_click(self, **event_args):
    open_form('AddCommander')