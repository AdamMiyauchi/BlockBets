import anvil.server
import anvil.js
import anvil.js.window as window
from anvil.js.window import ethereum, Web3

CONTRACT_ADDRESS = '0x5C20cDbAd7bC4F32F0F9493F54ce2dd79E6a55e5'
CONTRACT_ABI = [{"inputs": [{"internalType": "string[3]","name": "_data","type": "string[3]"},{"internalType": "uint16[3]","name": "_odds","type": "uint16[3]"}],"name": "addMatch","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address payable","name": "userAddress","type": "address"},{"internalType": "uint16","name": "_matchId","type": "uint16"},{"internalType": "uint8","name": "_prediction","type": "uint8"}],"name": "placeBet","outputs": [],"stateMutability": "payable","type": "function"},{"inputs": [{"internalType": "uint16","name": "_matchId","type": "uint16"},{"internalType": "uint8","name": "_outcome","type": "uint8"}],"name": "resolveMatch","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"stateMutability": "payable","type": "constructor"},{"stateMutability": "payable","type": "receive"},{"inputs": [],"name": "getActiveMatches","outputs": [{"internalType": "uint256[]","name": "","type": "uint256[]"},{"components": [{"internalType": "string[3]","name": "data","type": "string[3]"},{"internalType": "uint16[3]","name": "odds","type": "uint16[3]"},{"internalType": "bool","name": "isActive","type": "bool"}],"internalType": "struct BetApp.Match[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "getBetsByUser","outputs": [{"components": [{"internalType": "address payable","name": "userAddress","type": "address"},{"internalType": "uint16","name": "matchId","type": "uint16"},{"internalType": "uint8","name": "prediction","type": "uint8"},{"internalType": "uint8","name": "outcome","type": "uint8"},{"internalType": "uint256","name": "amount","type": "uint256"}],"internalType": "struct BetApp.Bet[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "owner","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"}]


class SmartContract:
  ## Interface for interacting with the blockchain smart contract. Uses Web3.js library and Metamask
  def __init__(self):
    ## verify Metamask extension is installed and connected
    if window.ethereum:
      window.web3 = anvil.js.new(Web3, window.ethereum)
      window.ethereum.enable()
    elif window.web3:
      window.web3 = anvil.js.new(Web3, window.web3.currentProvider);
    else:
      print('metamask extension not installed')

    self.contract_address = CONTRACT_ADDRESS
    self.contract_abi = CONTRACT_ABI
    self.contract = anvil.js.new(window.web3.eth.Contract, self.contract_abi, self.contract_address)

    # team logo lookup
    self.image_lookup = {
      'Manchester City': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/1200px-Manchester_City_FC_badge.svg.png',
      'Juventus': 'https://creativereview.imgix.net/content/uploads/2017/01/Juve-sq.jpg',
      'Barcelona': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/1200px-FC_Barcelona_%28crest%29.svg.png',
      'Chelsea': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/1200px-Chelsea_FC.svg.png',
      'Ajax': 'https://upload.wikimedia.org/wikipedia/en/7/79/Ajax_Amsterdam.svg',
      'Real Madrid': 'https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg',
      'Red Star': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Red_Star_FC_logo.svg/1200px-Red_Star_FC_logo.svg.png',
      'Bayern Munich': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Logo_FC_Bayern_M%C3%BCnchen_%282002%E2%80%932017%29.svg/600px-Logo_FC_Bayern_M%C3%BCnchen_%282002%E2%80%932017%29.svg.png',
      'no_image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1q1aAwmDtcIvQkgpM-OyW2gNCEqvE2yAxFg&usqp=CAU',
    }
  
  def get_address(self, idx=0):
    ## gets the adress of the connected Metamask account
    accounts = window.web3.eth.getAccounts()
    return accounts[idx]
    
  def get_balance(self):
    ## get the balance of the connected Metamask account
    address = self.get_address()
    balance = window.web3.eth.getBalance(address)
    balance = window.web3.utils.fromWei(balance, 'ether')
    balance = round(float(balance), 4)
    return balance
  
  def get_active_matches(self):
    ## gets a list of active matches to bet on
    active_matches = self.contract.methods.getActiveMatches().call()
    # print(active_matches)
    # print()
    active_matches_index = list(active_matches['0'])
    active_matches_matches = list(active_matches['1'])
    # print(active_matches_index)
    # print(active_matches_matches)

    # parse the list of matches to fit the required format of the frontend
    parsed_matches = []
    for idx in active_matches_index:
      match = dict(active_matches_matches[idx])
      if match['isActive']:   
        opponentA, opponentB, match_time = list(match['data'])
        odds_A, odds_draw, odds_B = list(match['odds'])
        # print(opponentA, opponentB, match_time)
        # print(odds_A, odds_draw, odds_B)
        # print()
        parsed_matches.append({
          'match_id': idx,
          'match_time': match_time, 
          'opponentA': opponentA, 
          'opponentA_image': self.image_lookup[opponentA] if opponentA in self.image_lookup else self.image_lookup['no_image'],
          'opponentB': opponentB, 
          'opponentB_image':  self.image_lookup[opponentB] if opponentB in self.image_lookup else self.image_lookup['no_image'],
          'odds_A': odds_A,
          'odds_draw': odds_draw,
          'odds_B': odds_B,
        })
  
    return tuple(parsed_matches)

  def get_bets_by_user(self):
    ## gets a list of all bets the connected address has betted on
    user_addr = self.get_address()
    user_bets = self.contract.methods.getBetsByUser().call({'from': user_addr})
    matches = self.get_active_matches()

    # parase the list of bets to a format used by the frontend
    parsed_user_bets = []
    for bet in user_bets:
      match = self._find_dict_in_tuple('match_id', bet['matchId'], matches)
      
      bet_amount = window.web3.utils.fromWei(bet['amount'], 'finney')
      if bet['prediction'] == 0:
        bet_type = f"Win {match['opponentA']} \n Odds: {str(match['odds_A'])} - Bet: {bet_amount}" 
      elif bet['prediction'] == 1:
        bet_type = f"Draw {match['opponentA']} vs {match['opponentB']} \n Odds: {str(match['odds_draw'])} Bet: {bet_amount}" 
      else:
        bet_type = f"Win {match['opponentB']} \n Odds: {str(match['odds_B'])} Bet: {bet_amount}" 

      if bet['outcome'] == 3:
        result = 'Match still in progress'
      elif bet['outcome'] == bet['prediction']:
        result = 'Bet won!'
      else:
        result = 'Bet lost'
      
      parsed_user_bets.append({
        'wallet': bet['userAddress'][:5] + '...' + bet['userAddress'][-3:],
        'match_time': match['match_time'],
        'match_opponents': match['opponentA'] + ' VS ' + match['opponentB'],
        'bet_type': bet_type,
        'result': result
      })
      
    return tuple(parsed_user_bets)

  def place_bet(self, match_id, prediction, bet_amount):
    ## places a new bet on the blockchain with the given match, prediction, and bet. 
    user_addr = self.get_address()
    self.contract.methods.placeBet(user_addr, match_id, prediction).send({
      'from': user_addr,
      'value': window.web3.utils.toWei(bet_amount, 'finney')
    })
    self.get_bets_by_user()

  def _find_dict_in_tuple(self, target_key, target_value, my_tuple):
    ## util function
    return next((my_dict for my_dict in my_tuple if target_key in my_dict and my_dict[target_key] == target_value), None)
