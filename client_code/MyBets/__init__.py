from ._anvil_designer import MyBetsTemplate
from anvil import *
from ..SmartContract import SmartContract

class MyBets(MyBetsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.get_contract_info()
    
  def get_contract_info(self):
    ## gets the users balance, address, and list of bets they have placed
    try:
      self.smart_contract = SmartContract()
  
      # get user balance
      self.balance = self.smart_contract.get_balance()
      self.address =self.smart_contract.get_address()
      address = self.address[:5] + '..' + self.address[-3:]
      self.balance_label.text = f'Connected Address: {address}     Balance: {str(self.balance)} ETH'
      
      # get user bets
      users_bets = self.smart_contract.get_bets_by_user()
      self.bet_log_rows.items = users_bets
  
      # get summary stats
      self.total_winnings.text = 'Total winnings: $111' 
      self.total_bets.text = f'Total bets: {len(users_bets)}'
    except Exception as e:
      print(e)
      alert(
        title='There was an error fetching your bets. Please reconnect your wallet and try again later.',
        large=True
      )
    
  def mybets_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('MyBets')

  def betbook_click(self, **event_args):
    # navigate back to the bet book page
    open_form('BetBook')



