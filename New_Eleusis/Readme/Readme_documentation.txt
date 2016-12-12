'''
Team Name : Neurons
Code Version : Phase I
Team Members : 
Anusha Dudi
Kaushik Velusamy
Mounica Kalavakuri
Ethan Hein
'''

Description/ Overview:

Our player implements a CSP solver using forward chaining. We first generate a list of all onecard, two-card, or three-card rules, depending on how many cards are initially provided. For two- and three-card domains, this list is massive, but we immediately eliminate any rule that does not match the given card(s). 

Forward chaining then comes from continuing to eliminate impossible rules as more cards are played, which very quickly narrows down the possible set of rules. To pick a card, we first pick a current rule, which is just the first rule in the list of (legal) rules. We then pick and play a card satisfying that rule. If successful, we increase our confidence for that rule, and if not, then that rule (and usually many others) is eliminated in forward chaining, and we pick a new rule to use the next time we play a card.


How to use the code for Phase I:
Go to Phase-I folder and just run main.py to start the game.

How to use the code for Phase II:
Go to Phase-II folder and just run game.py to start the game.
