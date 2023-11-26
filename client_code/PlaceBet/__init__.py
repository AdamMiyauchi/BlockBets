from ._anvil_designer import PlaceBetTemplate
from anvil import *
import anvil.server
from ..SmartContract import SmartContract

class PlaceBet(PlaceBetTemplate):
  # form to place bets
  def __init__(self, **properties):
    self.init_components(**properties)
    self.match_id = properties['match_id']
    self.prediction = properties['prediction']
    self.smart_contract = SmartContract()

  def cancel_click(self, **event_args):
    # close alert window
    self.raise_event("x-close-alert")

  def place_bet_click(self, **event_args):
    ## verify the bet amount and send bet to blockchain
    try:
      self.sc_error.visible = False
      if self.bet_amount.text and float(self.bet_amount.text) > 0:     # non empty and positive bet
        self.error_label.visible = False
        self.smart_contract.place_bet(self.match_id, self.prediction, float(self.bet_amount.text))
        open_form('MyBets')
        self.raise_event("x-close-alert")
        Notification('Success. Sending your bet to the blockchain.', timeout=3).show()
      else:
        self.error_label.visible = True
    except Exception as e:
      print(e)
      self.sc_error.visible = True

