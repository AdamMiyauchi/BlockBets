// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BetApp {
    // Owner logic
    address public owner;
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }
    constructor() payable {
        owner = msg.sender;
    }

    // Matches
    struct Match {
        string[3] data;
        uint16[3] odds;
        bool isActive;
    }
    Match[] private matches;

    function addMatch(string[3] memory _data, uint16[3] memory _odds) external onlyOwner {
        Match memory newMatch = Match({
            data: _data,
            odds: _odds,
            isActive: true
        });
        matches.push(newMatch);
    }

    function getActiveMatches() external view returns (uint256[] memory, Match[] memory) {
        uint256 count = 0;
        uint256 len = matches.length;
        for (uint256 i = 0; i < len; i++) {
            if (matches[i].isActive) {
                count++;
            }
        }

        // Create a new array to store the filtered objects
        uint256[] memory indexes = new uint256[](count);
        Match[] memory result = new Match[](count);
        uint256 resultIndex = 0;

        // Populate the result array with filtered objects
        for (uint256 i = 0; i < len; i++) {
            if (matches[i].isActive) {
                indexes[resultIndex] = i;
                result[resultIndex] = matches[i];
                resultIndex++;
            }
        }

        return (indexes, result);
    }

    // Bets
    struct Bet {
        address payable userAddress;
        uint16 matchId;
        uint8 prediction;
        uint8 outcome;
        uint256 amount;
    }
    mapping(address => Bet[]) private betsByUser;
    mapping(uint16 => Bet[]) private betsByMatch;

    // Payment logic
    receive() external payable {}

    // Function for placing the bets
    function placeBet(address payable userAddress, uint16 _matchId, uint8 _prediction) external payable {
        require(msg.value > 0, "Amount must be greater than 0");
        require(matches[_matchId].isActive, "The match must be currently available for betting");

        Bet memory newBet = Bet({
            userAddress: userAddress,
            matchId: _matchId,
            prediction: _prediction,
            outcome: 3,
            amount: msg.value
        });

        betsByUser[msg.sender].push(newBet);
        betsByMatch[_matchId].push(newBet);
    }

    // Function to get all bets placed by a specific user
    function getBetsByUser() external view returns (Bet[] memory) {
        return betsByUser[msg.sender];
    }

    // Function used to receive results and handle the payouts
    function resolveMatch(uint16 _matchId, uint8 _outcome) external onlyOwner {
        matches[_matchId].isActive = false;
        uint16 coef = matches[_matchId].odds[_outcome];
        for (uint256 i = 0; i < betsByMatch[_matchId].length; i++) {
            Bet memory betMatch = betsByMatch[_matchId][i];
            if(betMatch.prediction == _outcome) {
                uint256 payout = betMatch.amount * coef / 100 * 95 / 100;
                require(address(this).balance >= payout, "Insufficient balance in the contract");
                betMatch.userAddress.transfer(payout);
            }
            // TODO: Add transaction too
            address userAddress = betMatch.userAddress;
            for (uint256 j = 0; j < betsByUser[userAddress].length; j++) {
                if(betsByUser[userAddress][j].matchId == _matchId) {
                    Bet storage betUser = betsByUser[userAddress][j];
                    betUser.outcome = _outcome;
                }
            }
        }
    }
}