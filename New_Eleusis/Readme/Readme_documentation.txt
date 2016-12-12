'''
Team Name : Neurons
Code Version : Phase I
Team Members : 
Anusha Dudi
Kaushik Velusamy
Mounica Kalavakuri
Ethan Hein
'''
Notes:
The exception in new_eleusis.py evaluate function is commented out.



Description/ Overview:

Our player implements a CSP solver using forward chaining. We first generate a list of all onecard, two-card, or three-card rules, depending on how many cards are initially provided. For two- and three-card domains, this list is massive, but we immediately eliminate any rule that does not match the given card(s). 

Forward chaining then comes from continuing to eliminate impossible rules as more cards are played, which very quickly narrows down the possible set of rules. To pick a card, we first pick a current rule, which is just the first rule in the list of (legal) rules. We then pick and play a card satisfying that rule. If successful, we increase our confidence for that rule, and if not, then that rule (and usually many others) is eliminated in forward chaining, and we pick a new rule to use the next time we play a card.


How to use the code for Phase I:
Go to Phase-I folder and just run main.py to start the game.

How to use the code for Phase II:
Go to Phase-II folder and just run game.py to start the game.

Major Changes in Phase-II:
Bug fixes in phase I and more domain knowledge

Additionally,
1. Each adversary will play after you play, going cyclically. At any point, any player (including your scientist!) may announce that they  are ready to guess a rule. At this point,  the game ends, and all players must return a best guess at the  current rule. [Announce the current best hypothesis once game ended.]

2. Throughout the game we will be having 14 cards. 
After playing one card, just that one card will be replaced by another random card with the previous 13 remaining.

3. Take the closest card matching our hypothesis in our 14 cards to play, even if one does not exist. 

4. score(player) : 
Returns the score for the selected player’s most recent round. (Low is better!)  calculate by  adding points as follows:
+1 for every successful play over 20 and under 200;
+2  for every failed play; 
+15 for a rule that is not equivalent to the correct rule;
+30 for a rule that does not describe all cards on the board.

Each player that guesses the correct rule (or its logical equivalent), with no extra terms, receives an  additional  bonus of -75 points.
If the player that ended the game gives the correct rule, it receives an additional -25 points.

5. documentation for implementation and usage