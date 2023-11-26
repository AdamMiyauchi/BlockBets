from ._anvil_designer import BetBookTemplate
from anvil import *
import anvil.js.window as window
from ..SmartContract import SmartContract

class BetBook(BetBookTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.connect_metamask()

  def connect_metamask(self):
    ## Connect to metamask, get account balance, address, and list of active matches to bet on.
    if window.web3 or window.ethereum:
      self.metamask_connected = True
      try:
        self.smart_contract = SmartContract()
        self.match_list_error_msg.visible = False
        self.connect_metamask_btn.visible = False
      
        # get list of acitve matches
        self.matches = self.smart_contract.get_active_matches()
        self.match_list.items = self.matches
        
        # get user balance
        self.balance = self.smart_contract.get_balance()
        self.address =self.smart_contract.get_address()
        address = self.address[:5] + '..' + self.address[-3:]
        self.balance_label.text = f'Connected Address: {address}     Balace: {str(self.balance)} ETH'
      except Exception as e:
        print(e)
        # error help messages
        self.metamask_connected = False     
        self.match_list_error_msg.visible = True
        self.connect_metamask_btn.visible = True
        alert(
          title='Metamask extension error: please connect to MetaMask extension.',
          large=True
        )
    else:
      # error help messages
      self.metamask_connected = False
      self.match_list.items = []
      self.match_list_error_msg.visible = True
      self.connect_metamask_btn.visible = True
      alert(
        title='You must install the Metamask extension.',
        large=True
      )

  def mybets_click(self, **event_args):
    # hangle navigate to my bets page
    if not self.metamask_connected:
      alert(
        title='You need to install or connect to MetaMask extension before viewing your bets.',
        large=True
      )
    else:
      open_form('MyBets')

  def betbook_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('BetBook')

  def connect_metamask_btn_click(self, **event_args):
    self.connect_metamask()
    
