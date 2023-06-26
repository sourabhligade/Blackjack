import random, sys

HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
BACKSIDE = 'backside'


def main():
    print('''Blackjack, by Al Sweigart al@inventwithpython.com

    Rules:
      Try to get as close to 21 without going over.
      Kings, Queens, and Jacks are worth 10 points.
      Aces are worth 1 or 11 points.
      Cards 2 through 10 are worth their face value.
      (H)it to take another card.
      (S)tand to stop taking cards.
      On your first play, you can (D)ouble down to increase your bet
      but must hit exactly one more time before standing.
      In case of a tie, the bet is returned to the player.
      The dealer stops hitting at 17.''')

    money = 5000
    while True:  # Main game loop.
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print('Thanks for playing!')
            sys.exit()

        print('Money:', money)
        bet = getBet(money)

        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print('Bet:', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break

            move = getMove(playerHand, money - bet)

            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input('Press Enter to continue...')
                print('\n\n')

        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie, the bet is returned to you.")

        input('Press Enter to continue...')
        print('\n\n')


def getBet(maxBet):
    while True:
        print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()

        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue
        elif 1 <= int(bet) <= maxBet:
            return int(bet)


def getDeck():
    deck = []

    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))

        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCard(dealerHand[0])
        print('  ?  ')
        for card in dealerHand[1:]:
            displayCard(card)
    else:
        print('DEALER: ???')
        displayCard(dealerHand[0])
        print('  ?  ')

    print('\n\n')

    print('PLAYER:', getHandValue(playerHand))
    for card in playerHand:
        displayCard(card)


def getHandValue(cards):
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]
        if rank == 'A':
            value += 11
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    while value > 21 and numberOfAces > 0:
        value -= 10
        numberOfAces -= 1

    return value


def displayCard(card):
    rank, suit = card
    print('  -------')
    print(' |{}     |'.format(rank.ljust(2)))
    print(' |       |')
    print(' |   {}   |'.format(suit))
    print(' |       |')
    print(' |     {}|'.format(rank.rjust(2)))
    print('  -------')


def getMove(playerHand, money):
    while True:
        moves = ['(H)it', '(S)tand']

        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        print(', '.join(moves) + '?')
        move = input('> ').upper()
        if move in ('H', 'S'):
            return move
        elif move == 'D' and '(D)ouble down' in moves:
            return move


if __name__ == '__main__':
    main()


