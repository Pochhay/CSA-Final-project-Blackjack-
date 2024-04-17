import random

# Function to deal a card from the deck
def dealCard(deck):
    return deck.pop()

# Deal hand cards
def deal_hand(deck):
    player_hand = [dealCard(deck)]
    dealer_hand = [dealCard(deck)]
    player_hand.append(dealCard(deck))
    dealer_hand.append(dealCard(deck))
    return player_hand, dealer_hand


# Function to calculate the total score of all cards in the list
def calculateTotal(hand, card_values):
    total = sum(card_values[card] for card in hand)
    # Adjust for Aces
    for card in hand:
        if card in ['sA', 'dA', 'cA', 'hA'] and total > 21:
            total -= 10
    return total

# Function to handle player's turn
def playerTurn(deck, player_hand, card_values):
    while True:
        player_choice = input("Hit or Stand: ").lower()
        if player_choice == 'hit':
            player_hand.append(dealCard(deck))
            print("Player hand")
            print(player_hand)
            player_score = calculateTotal(player_hand, card_values)
            print("Player score: ", player_score)
            if player_score == 21:
                return 2
            elif player_score > 21:
                print("Player busts! Dealer wins!")
                return -1
            return True
        elif player_choice == 'stand':
            return False
        else:
            print("Invalid input. Please try again.")

# Function to handle dealer's turn
def dealerTurn(deck, dealer_hand, card_values, counter):
    dealer_score = calculateTotal(dealer_hand, card_values)
    if counter == 0:
        print("Dealer hand:")
        print(dealer_hand)
        print("Dealer score: ", dealer_score)
    if dealer_score < 17:
        print("Dealer hit")
        dealer_hand.append(dealCard(deck))
        dealer_score = calculateTotal(dealer_hand, card_values)
        print("Dealer hand:")
        print(dealer_hand)
        print("Dealer score: ", dealer_score)
        if dealer_score > 21:
            print("Dealer busts! Player wins!")
            return -1
        return True

    else:
        print("Dealer stand")
        return False

# Function to cycle dealing card
def DealingCycle(deck, player_hand, dealer_hand, card_values):
    player_turn = True
    dealer_turn = True
    counter = 0
    while True:
        if calculateTotal(player_hand, card_values) == 21:
            print("Player hit Black Jack!")
            break
        if player_turn:
            player_turn = playerTurn(deck, player_hand, card_values)
            if player_turn == -1:
                break
            if player_turn == 2:
                continue
        if dealer_turn:
            dealer_turn = dealerTurn(deck, dealer_hand, card_values, counter)
            counter += 1
            if dealer_turn == -1:
                break
        if calculateTotal(dealer_hand, card_values) == 21:
            print("Dealer hit Black Jack!")
            break
        if player_turn == False and dealer_turn == False:
            break

# Function to determine the winner
def determineWinner(player_score, dealer_score):
    if player_score > 21:
        print("Dealer wins!")
    elif dealer_score > 21:
        print("Player wins!")
    elif player_score > dealer_score:
        print("Player wins!")
    elif dealer_score > player_score:
        print("Dealer wins!")
    else:
        print("It's a tie!")

# Main function
def main():
    while True:
        # Create a deck of cards
        card_values = {'s2': 2, 's3': 3, 's4': 4, 's5': 5, 's6': 6, 's7': 7, 's8': 8, 's9': 9, 's10': 10, 'sJ': 10, 'sQ': 10, 'sK': 10, 'sA': 11,
                        'd2': 2, 'd3': 3, 'd4': 4, 'd5': 5, 'd6': 6, 'd7': 7, 'd8': 8, 'd9': 9, 'd10': 10, 'dJ': 10, 'dQ': 10, 'dK': 10, 'dA': 11,
                        'c2': 2, 'c3': 3, 'c4': 4, 'c5': 5, 'c6': 6, 'c7': 7, 'c8': 8, 'c9': 9, 'c10': 10, 'cJ': 10, 'cQ': 10, 'cK': 10, 'cA': 11,
                        'h2': 2, 'h3': 3, 'h4': 4, 'h5': 5, 'h6': 6, 'h7': 7, 'h8': 8, 'h9': 9, 'h10': 10, 'hJ': 10, 'hQ': 10, 'hK': 10, 'hA': 11,}
        spades   = ['s2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 'sJ', 'sQ', 'sK', 'sA']
        diamonds = ['d2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'dJ', 'dQ', 'dK', 'dA']
        clubs    = ['c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'cJ', 'cQ', 'cK', 'cA']
        hearts   = ['h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'hJ', 'hQ', 'hK', 'hA']
        deck     = spades + diamonds + clubs + hearts
        random.shuffle(deck)
        # Greeting
        print("\nWelcome to blackjack game\n")

        player_hand, dealer_hand = deal_hand(deck)

        print("Player hand:")
        print(player_hand)
        player_score = calculateTotal(player_hand, card_values)
        print(f"Player score: {player_score}", len(deck))
        print("Dealer hand:")
        print(f"['{dealer_hand[0]}', ?]")
        
        # card dealing cycle
        DealingCycle(deck, player_hand, dealer_hand, card_values)

        # Determine winner
        player_score = calculateTotal(player_hand, card_values)
        dealer_score = calculateTotal(dealer_hand, card_values)
        determineWinner(player_score, dealer_score)

        game_loop = input("Continue?(Y/N): ")
        if game_loop.lower() == 'n':
            break

if __name__ == '__main__':
    main()
