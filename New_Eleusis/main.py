import Scientist_Merged
import new_eleusis
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
                  "Example of valid list of cards is '3H 7D 2H' or '7D 2H' or '3S' [Do not enter quotes '']\n" \
                  "Play again" %(index+1)
            exit()

    initial_number_of_cards = len(cards_on_table)
    if initial_number_of_cards == 1:
        print "Cool, You have entered %d card and the card is" %(initial_number_of_cards)
        print cards_on_table
    else:
        print "Cool, You have entered %d cards and the cards are" % (initial_number_of_cards)
        print cards_on_table

    cards_on_the_boards_state = []
    for index, card in enumerate(cards_on_table):
        cardintuple = (card,) + ([],)
        cards_on_the_boards_state.append(cardintuple)


    print "Enter the Rule which the game should follow. \n " \
          "Not your Rule will not be opened during the game. \n " \
          "Examples of rules can be like this. \n" \
          "1. equal(color(current), R) ==> All cards should be red in color \n" \
          "2. iff(equal(color(previous), B), equal(color(current), R), True) ==> Red card follow Black card \n" \
          "\n\n copy and paste the below rule for testing \n equal(color(current), B)\n"

    gods_rule = raw_input("==>")
    gods_rule = str(gods_rule)
    print "\n \n Your Entered Rule is ==> ", gods_rule, "\n"

    print "Before the game starts, check if the passed card obey's the rule else quit the game here. Implement this later \n "
    Scientist_Merged.scientist(cards_on_the_boards_state, initial_number_of_cards, gods_rule)


"""
    p = new_eleusis.parse(gods_rule)
    if p.evaluate(cards_on_the_boards_state):
        print "The initial cards that you provided matches your Rule\n" \
              "Proceeding with the New Eleusis Game\n.\n.\n."
    else:
        print "The initial cards that you provided DOES NOT match your Rule. \n " \
              "Check if your initial inputs and the rule. \n" \
              "Check if your rule matches the required format \n" \
              "Game aborting due to false play by God \n" \
              "Try again\n"
        exit()
"""



if __name__ == "__main__":
    main()
