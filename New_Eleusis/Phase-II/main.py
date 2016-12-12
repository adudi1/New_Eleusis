'''
Team Name : Neurons
Anusha Dudi
Kaushik Velusamy
Mounica Kalavakuri
Ethan Hein
'''


from Scientist_phase2 import *
from random import *

def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[randint(0, len(values) - 1)] + suits[randint(0, len(suits) - 1)]

def main():
    player = Scientist()
    rule = str(raw_input("Set God's rule: "))
    cards_str = raw_input("Enter 3 legal cards")
    cards = str(cards_str).split()
    k = int(raw_input("Number of adversaries: "))
    n = int(raw_input("Adversary end's game at (play number): "))

    hand = [generate_random_card() for i in range(14)]

    player.setRule(rule)
    player.scientist(cards, hand, False)
    for i in range(2, n,1):
        player.scientist([generate_random_card() for i in range(k)], None, False)
    player.scientist([generate_random_card() for i in range(k)], None, True)


if __name__ == "__main__":
    main()
