import random
import re

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10,
          'King': 10, 'Ace': 11}

def main():
    """
    Main functions welcomes player and creates 100 chips for him.
    After that it checks if he has enough chips for the game, creates deck,
    shuffles it, asks for a bet, creates hands with two cards and shows them to
    the player.
    Then he's asked if he wants to hit or take card until he's satisfied
    with total value or if he's got too much it automatically continues to the
    evaluation of result.
    At the end it prints the result, adds or subtracts chips and asks player if
    he wants to repeat the game.
    """
    print('Welcome to the game of Blackjack!')
    chips = Chip(100)
    while True:
        if chips.number < 1:
            print('You don\'t have chips!')
            break
        deck = Deck()
        deck.shuffle()
        print(chips)
        bet = makeBet(chips)
        pHand = Hand(deck)
        dHand = Hand(deck)
        print('\nDealer\'s hand:')
        print(f'{dHand.showOne()}\n')
        print('Your hand:')
        print(pHand)
        print('-'*20)
        print(f'Total value: {count(pHand)}\n')

        while True:
            if hitOrCard():
                pHand.takeCard(deck)
                print('\nYour hand:')
                print(pHand)
                print('-'*20)
                print(f'Total value: {count(pHand)}\n')
                if count(pHand) > 21:
                    break
            else:
                break
        pCount = count(pHand)
        dCount = count(dHand)
        while dCount < 17:
            dHand.takeCard(deck)
            dCount = count(dHand)
        print('\n')
        result(pHand, dHand, pCount, dCount, chips, bet)
        if playAgain():
            continue
        else:
            break

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.deck)

    def remove(self, card):
        self.deck.remove(card)

    def __str__(self):
        deck = ''
        for card in self.deck:
            deck += '\n' + card.__str__()
        return deck

class Hand:
    def __init__(self, deck):
        self.hand = [deck.deck.pop() for i in range(2)]

    def takeCard(self, deck):
        card = deck.deck.pop()
        self.hand.append(card)

    def showOne(self):
        card = ''
        firstCard = self.hand[0]
        card += firstCard.__str__()
        return card

    def __str__(self):
        hand = ''
        for card in self.hand:
            hand += card.__str__() + '\n'
        return hand

class Chip:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return f'{self.number} of chips remaining.'

def makeBet(chips):
    """
    Asks player to enter desired number of chips to bet and checks if it is an
    integer and if he owns that much at the time.
    """
    while True:
        try:
            bet = int(input('How much do you want to bet? '))
            if bet > chips.number:
                raise ValueError
            chips.number -= bet
            return bet
        except ValueError:
            print('Please enter correct value!')
            continue


def aceValue(hand, totalValue):
    """
    Checks if there is an ace in the hand and returns True if it should be value of
    1.
    """
    ace = re.compile(r'Ace of (Hearts|Diamonds|Spades|Clubs)')
    if ace in hand.hand and totalValue > 21:
        return True

    return False


def hitOrCard():
    """
    Asks player if he wants an another card and checks correct format.
    """
    while True:
        try:
            q = input('Do you want to hit or take another card? ')
            if q == 'card':
                return True
            elif q == 'hit':
                return False
            else:
                raise ValueError
        except ValueError:
            print('Please enter "hit" or "card".')
            continue

def count(hand):
    """
    Counts total value of cards in the hand and determines correct value of ace
    if it is there.
    """
    totalValue = 0
    for card in hand.hand:
        value = values[card.rank]
        totalValue += value

    if aceValue(hand, totalValue):
        totalValue -= 10

    return totalValue

def result(playersHand, dealersHand, pCount, dCount, chips, bet):
    """
    Prints both hands, total values and evaluates result. Adds or subtract
    chips depending on the result.
    """
    print(f'Your hand:\n{playersHand}')
    print('-'*20)
    print(f'Total value: {count(playersHand)}\n')
    print(f'Dealers\'s hand:\n{dealersHand}')
    print('-'*20)
    print(f'Total value: {count(dealersHand)}\n')
    if (pCount <= 21 and pCount > dCount) or (pCount <= 21 and dCount > 21):
        print('You have won!')
        chips.number += bet*2
        print(chips)
    elif pCount == dCount:
        print('It\'s a tie!')
        chips.number += bet
    else:
        print('You have lost!')
        print(chips)

def playAgain():
    """
    Asks player if he wants to repeat the game and checks the correct format of
    answer.
    """
    while True:
        try:
            q = input('Do you want to play again? y/n ')
            if q == 'y':
                return True
            elif q == 'n':
                return False
            else:
                raise ValueError
        except ValueError:
            print('Please enter "y" or "n".')
            continue

main()
