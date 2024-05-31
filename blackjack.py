import random

# Constants for the game
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Function to handle player and dealer actions
def hit(deck, hand):
    hand.add_card(deck.deal())

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

# Function to handle end of game scenarios
def player_busts(player, dealer):
    print("Player busts! Dealer wins.")

def player_wins(player, dealer):
    print("Player wins!")

def dealer_busts(player, dealer):
    print("Dealer busts! Player wins!")

def dealer_wins(player, dealer):
    print("Dealer wins!")

def push(player, dealer):
    print("It's a tie! Push.")

# Main game logic
def play_blackjack():
    while True:
        print("Welcome to Blackjack!")
        
        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        player_hand = Hand()
        dealer_hand = Hand()

        for _ in range(2):
            hit(deck, player_hand)
            hit(deck, dealer_hand)

        show_some(player_hand, dealer_hand)
        
        while True:
            action = input("\nWould you like to Hit or Stand? Enter 'h' or 's': ").lower()
            if action == 'h':
                hit(deck, player_hand)
                show_some(player_hand, dealer_hand)
                if player_hand.value > 21:
                    player_busts(player_hand, dealer_hand)
                    break
            elif action == 's':
                print("Player stands. Dealer is playing.")
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)
                show_all(player_hand, dealer_hand)
                
                if dealer_hand.value > 21:
                    dealer_busts(player_hand, dealer_hand)
                elif dealer_hand.value > player_hand.value:
                    dealer_wins(player_hand, dealer_hand)
                elif dealer_hand.value < player_hand.value:
                    player_wins(player_hand, dealer_hand)
                else:
                    push(player_hand, dealer_hand)
                break
            else:
                print("Invalid input! Please enter 'h' or 's'.")
        
        new_game = input("\nWould you like to play again? Enter 'y' or 'n': ").lower()
        if new_game != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_blackjack()
