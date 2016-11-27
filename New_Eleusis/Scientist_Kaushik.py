import new_eleusis
from random import *


class Board_State:
    def __init__(self, cards_on_table_passed_to_board_state, initial_number_of_cards_passed_to_board_state):
        self.cards_on_table_passed_to_board_state = cards_on_table_passed_to_board_state
        self.initial_number_of_cards_passed_to_board_state = initial_number_of_cards_passed_to_board_state

    def guess(self):

        self.possible_rulebook = self.build_domain()#This will give you all possible rules for the given input cards

            #Everytime guess function is called, it should do 3 things
            #1. Mark the old rule failed,
            #2. prune the rules related to the failed rule from the possible_rulebook
            #3. pop the next card which matches the next possible rule in the possible_rulebook
        #self.new_top_rule = self.possible_rulebook.pop()
            #generate a card which matches the new_top_rule
        pass
        #return self.generate_a_card_fortheguessed_rule(self.new_top_rule)
                    # set scope or static or global and make sure the possible_rulebook.pop() gives a new rule
                    # from the stack, everytime it is called from the while loop.

    def build_domain(self):
        self.domain_1card_rules()
        #append the possible rules to the end of the possible_rule book
        if self.initial_number_of_cards_passed_to_board_state == 2:
            self.domain_2card_rules()
            #append the possible rules to the end of the possible_rule book
        if self.initial_number_of_cards_passed_to_board_state == 3:
            self.domain_3card_rules()
            # append the possible rules to the end of the possible_rule book
        else:
            pass #future work
        #return the possible_rulebook to the guess fucntion

    def domain_1card_rules(self):
        pass

    def domain_2card_rules(self):
        pass

    def domain_3card_rules(self):
        pass

    def generate_a_card_fortheguessed_rule(self, current_top_rule):
        pass
        #return a card which matches the current_top_rule


    def score(self):
        pass




#The New_Eleusis project starts here.
def main():
    print "\n \n Welcome to the New Eleusis Game. \n" \
          "===================================" \
          "\n Player Name: Scientist Neuron. \n " \
          "Agent Neuron will guess the next card and the rule you frame. \n " \
          "The rule you frame will not be opened during the game. \n\n " \
          "Enter the initial cards on the table. You can Enter any number of cards. \n Example '3H 7D 2H' [Do not enter quotes '']\n"
    global cards_on_table
    cards_on_table = raw_input("==>")
    cards_on_table = str(cards_on_table).split()

    if not cards_on_table:
        print "You should atleast enter 1 card. \n Play Again."
        exit()

    for index, card in enumerate(cards_on_table):
        if not new_eleusis.is_card(card):
            print "Your card number %i is not a valid card. \n " \
                  "Example of valid list of cards is '3H 7D 2H' or '7D 2H' or '2H' [Do not enter quotes '']\n" \
                  "Play again" %(index+1)
            exit()

    initial_number_of_cards = len(cards_on_table)
    if initial_number_of_cards == 1:
        print "Cool, You have entered %d card and the card is" %(initial_number_of_cards)
        print cards_on_table
    else:
        print "Cool, You have entered %d cards and the cards are" % (initial_number_of_cards)
        print cards_on_table

    print "Enter the Rule which the game should follow. \n " \
          "Not your Rule will not be opened during the game. \n " \
          "Examples of rules can be like this. \n" \
          "1. equal(color(current), R) ==> All cards should be red in color \n" \
          "2. iff(equal(color(previous), B), equal(color(current), R), True) ==> Red card follow Black card \n" \
          "\n\n copy and paste the below rule for testing \n equal(color(current), R)\n"

    gods_rule = raw_input("==>")
    gods_rule = str(gods_rule)
    print "\n \n Your Entered Rule is ==> ", gods_rule, "\n"

    print "Checking if your Entered cards obey your rule \n "

    p = new_eleusis.parse(gods_rule)
    if p.evaluate(cards_on_table):
        print "The initial cards that you provided matches your Rule\n" \
              "Proceeding with the New Eleusis Game\n.\n.\n."
    else:
        print "The initial cards that you provided DOES NOT match your Rule. \n " \
              "Check if your initial inputs and the rule. \n" \
              "Check if your rule matches the required format \n" \
              "Game aborting due to false play by God \n" \
              "Try again\n"
        exit()


    bs = Board_State(cards_on_table, initial_number_of_cards)
    #You don't have to take the gods rule to our board_state class to guess it.
    #Don't touch the gods_rule unless you want to test your guessed card
    attempt_count = 1
    while True:
        guessed_number_from_board_state = bs.guess()
        if p.evaluate(guessed_number_from_board_state):
            print "Guessed Number Accepted by the God Rule\n"
            break
        if attempt_count == 200:
            print "I Quit. You Win."
            exit()
        else:
            attempt_count += 1
            print "Attempting Again to Guess " ,attempt_count

        #break when your guess is accepted by the God rule.

    # make multiple checking with the same rule and different generated card which satisfy the guessed rule
    # to reverify your guess is correct and increase your confidence score.
        #get the rule which got accepted.
        #Store it

    #throw the rule to the god to check what you guessed is the same as the god's rule
        #if accepted game completed
        #else # prune and continue


if __name__ == "__main__":
    main()
