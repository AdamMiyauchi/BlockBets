from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.js.window as window
from ...PlaceBet import PlaceBet

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  def win_opponent1_click(self, **event_args):
    # open popup form for betting on opponent A winning
    pb_form = PlaceBet(match_id=self.item['match_id'], prediction=0)
    pb_form.match_time.text = 'Match Time: ' + self.item['match_time']
    pb_form.opponentA.text = self.item['opponentA']
    pb_form.opponentA_image.source = self.item['opponentA_image']
    pb_form.opponentB.text = self.item['opponentB']
    pb_form.opponentB_image.source = self.item['opponentB_image']
    pb_form.bet_type.text = 'Win ' + self.item['opponentA']
    pb_form.odds.text = 'Odds: ' + str(self.item['odds_A'])
    
    alert(
      pb_form,
      large=True,
      buttons=None
    )

  def draw_click(self, **event_args):
    # open popup form for betting on draw
    pb_form = PlaceBet(match_id=self.item['match_id'], prediction=1)
    pb_form.match_time.text = 'Match Time: ' + self.item['match_time']
    pb_form.opponentA.text = self.item['opponentA']
    pb_form.opponentA_image.source = self.item['opponentA_image']
    pb_form.opponentB.text = self.item['opponentB']
    pb_form.opponentB_image.source = self.item['opponentB_image']
    pb_form.bet_type.text = 'Draw'
    pb_form.odds.text = 'Odds: ' + str(self.item['odds_draw'])
    
    alert(
      pb_form,
      large=True,
      buttons=None
    )

  def win_opponent2_click(self, **event_args):
    # open popup form for betting on opponent B winning
    pb_form = PlaceBet(match_id=self.item['match_id'], prediction=2)
    pb_form.match_time.text = 'Match Time: ' + self.item['match_time']
    pb_form.opponentA.text = self.item['opponentA']
    pb_form.opponentA_image.source = self.item['opponentA_image']
    pb_form.opponentB.text = self.item['opponentB']
    pb_form.opponentB_image.source = self.item['opponentB_image']
    pb_form.bet_type.text = 'Win ' + self.item['opponentB']
    pb_form.odds.text = 'Odds: ' + str(self.item['odds_B'])
    
    alert(
      pb_form,
      large=True,
      buttons=None
    )

