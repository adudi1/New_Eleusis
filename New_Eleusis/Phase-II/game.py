#Put your program name in place of program_name

from Scientist_phase2 import *
from random import randint
from new_eleusis import *

global game_ended
game_ended = False

def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[randint(0, len(values)-1)] + suits[randint(0, len(suits)-1)]

class Player(object):
    def __init__(self, scientist):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self, cards):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
        Your scientist should play a card out of its given hand OR return a rule, not both.
        'game_ended' parameter is a flag that is set to True once the game ends. It is False by default
        """
        return scientist.scientist(cards, self.hand, game_ended)


class Adversary(object):
    def __init__(self):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
        Your scientist should play a card out of its given hand.
        """
        # Return a rule with a probability of 1/14
        prob_list = [i for i in range(14)]
        prob = prob_list[randint(0, 13)]
        if prob == 4:
            # Generate a random rule
            rule = ""
            conditions = ["equal", "greater"]
            properties = ["suit", "value"]
            cond = conditions[randint(0,len(properties)-1)]
            if cond == "greater":
                prop = "value"
            else:
                prop = properties[randint(0,len(properties)-1)]

            rule += cond + "(" + prop + "(current), " + prop + "(previous)), "
            return rule[:-2]+")"
        else:
            return self.hand[randint(0, len(self.hand)-1)]


# The players in the game
scientist = Scientist()
player = Player(scientist)
adversary1 = Adversary()
adversary2 = Adversary()
adversary3 = Adversary()

# Set a rule for testing
rule = "equal(is_royal(current), False)"
scientist.setRule(rule)

# The three cards that adhere to the rule
cards = ["10H", "2C", "4S"]

"""
In each round scientist is called and you need to return a card or rule.
The cards passed to scientist are the last 3 cards played.
Use these to update your board state.
"""
for round_num in range(14):
    # Each player plays a card or guesses a rule
    print "\n Round Number: {} ".format(round_num)
    try:
        #Player 1 plays
        print "Player 1 : Scientist's Turn"
        player_card_rule = player.play()
        if is_card(player_card_rule):
            del cards[0]
            cards.append(player_card_rule)
        else:
            raise Exception('')
        

        #Adversary 1 plays
        ad1_card_rule = adversary1.play()
        print "Adversary 1's Turn: {} ".format(ad1_card_rule) #print cards
        if is_card(ad1_card_rule):
            del cards[0]
            cards.append(ad1_card_rule)
        else:
            raise Exception('')

        #Adversary 2 plays
        ad2_card_rule = adversary2.play()
        print "Adversary 2's Turn: {} ".format(ad2_card_rule)  #print cards
        if is_card(ad2_card_rule):
            del cards[0]
            cards.append(ad2_card_rule)
        else:
            raise Exception('')

        #Adversary 3 plays
        print "Adversary 3's Turn: "
        ad3_card_rule = adversary3.play()
        print "Adversary 3's Turn: {} ".format(ad3_card_rule)  # print cards
        if is_card(ad3_card_rule):
            del cards[0]
            cards.append(ad3_card_rule)
        else:
            raise Exception('')

    except:
        print "game_ended", game_ended
        game_ended = True
        break

# Everyone has to guess a rule
rule_player = player.play(cards)

# Check if the guessed rule is correct and print the score
scientist.score()
