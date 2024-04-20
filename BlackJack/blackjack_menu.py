import pygame, sys, random
from button import Button
from pygame import mixer

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Blackjack♠️♦️♣️♥️")

BG_menu = pygame.image.load("BlackJack/assets/Background.png")

mixer.music.load("BlackJack/assets/The 'In' Crowd.wav")
mixer.music.play(-1)

button_sound = mixer.Sound("BlackJack/assets/Button⧸Plate Click (Minecraft Sound).wav")
card_sound = mixer.Sound("BlackJack/assets/card_deck_flick_click.mp3")
silence = "BlackJack/assets/silence.wav"

def get_font(size): 
    return pygame.font.Font("BlackJack/assets/font.ttf", size)

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

# function to create buttons for deal card and hit or stand
def draw_game(act, PLAY_MOUSE_POS):
    button_list = []
    if not act:
        Deal_button = Button(image=pygame.transform.scale(pygame.image.load("BlackJack/assets/Play Rect.png"),(150, 50)), pos=(645, 360), text_input="DEAL", font=get_font(25), base_color="Yellow", hovering_color="Green")
        Deal_button.changeColor(PLAY_MOUSE_POS)
        Deal_button.update(SCREEN)
        button_list.append(Deal_button)
    elif act:
        Hit_button = Button(image=pygame.transform.scale(pygame.image.load("BlackJack/assets/Play Rect.png"),(150, 50)), pos=(560, 670), text_input="HIT", font=get_font(25), base_color="Yellow", hovering_color="Green")
        Hit_button.changeColor(PLAY_MOUSE_POS)
        Hit_button.update(SCREEN)
        Stand_button = Button(image=pygame.transform.scale(pygame.image.load("BlackJack/assets/Play Rect.png"),(150, 50)), pos=(730, 670), text_input="STAND", font=get_font(25), base_color="Yellow", hovering_color="Green")
        Stand_button.changeColor(PLAY_MOUSE_POS)
        Stand_button.update(SCREEN)
        button_list.append(Stand_button)
        button_list.append(Hit_button)
    return button_list

# Function to calculate score of cards in hand
def calculateTotal(hand, card_values):
    total = sum(card_values[card] for card in hand)
    # Adjust for Aces
    for card in hand:
        if card in ['spades_A', 'diamonds_A', 'clubs_A', 'hearts_A'] and total > 21:
            total -= 10
    return total

# Function to determine the winner
def determineWinner(player_score, dealer_score):
    if player_score > 21:
        text2 = "Dealer wins!"
    elif dealer_score > 21:
        text2 = "Player wins!"
    elif player_score > dealer_score:
        text2 = "Player wins!"
    elif dealer_score > player_score:
        text2 = "Dealer wins!"
    else:
        text2 = "It's a tie!"
    return text2

def play():
    active = False
    deal_start = False
    player_hit = False
    player_stand = False
    hide_card = True
    dealer_hit = False
    player_bj = False
    dealer_bj = False
    player_bust = False
    dealer_bust = False
    dealer_turn = False
    end_game = False
    dealer_stand = False
    player_score = 0
    dealer_score = 0
    text = ''
    text2 = ''
    card_values = {
        'spades_2': 2, 'spades_3': 3, 'spades_4': 4, 'spades_5': 5, 'spades_6': 6, 'spades_7': 7, 'spades_8': 8, 'spades_9': 9, 'spades_10': 10, 'spades_J': 10, 'spades_Q': 10, 'spades_K': 10, 'spades_A': 11,
        'diamonds_2': 2, 'diamonds_3': 3, 'diamonds_4': 4, 'diamonds_5': 5, 'diamonds_6': 6, 'diamonds_7': 7, 'diamonds_8': 8, 'diamonds_9': 9, 'diamonds_10': 10, 'diamonds_J': 10, 'diamonds_Q': 10, 'diamonds_K': 10, 'diamonds_A': 11,
        'clubs_2': 2, 'clubs_3': 3, 'clubs_4': 4, 'clubs_5': 5, 'clubs_6': 6, 'clubs_7': 7, 'clubs_8': 8, 'clubs_9': 9, 'clubs_10': 10, 'clubs_J': 10, 'clubs_Q': 10, 'clubs_K': 10, 'clubs_A': 11,
        'hearts_2': 2, 'hearts_3': 3, 'hearts_4': 4, 'hearts_5': 5, 'hearts_6': 6, 'hearts_7': 7, 'hearts_8': 8, 'hearts_9': 9, 'hearts_10': 10, 'hearts_J': 10, 'hearts_Q': 10, 'hearts_K': 10, 'hearts_A': 11
    }
    spades = ['spades_2', 'spades_3', 'spades_4', 'spades_5', 'spades_6', 'spades_7', 'spades_8', 'spades_9', 'spades_10', 'spades_J', 'spades_Q', 'spades_K', 'spades_A']
    diamonds = ['diamonds_2', 'diamonds_3', 'diamonds_4', 'diamonds_5', 'diamonds_6', 'diamonds_7', 'diamonds_8', 'diamonds_9', 'diamonds_10', 'diamonds_J', 'diamonds_Q', 'diamonds_K', 'diamonds_A']
    clubs = ['clubs_2', 'clubs_3', 'clubs_4', 'clubs_5', 'clubs_6', 'clubs_7', 'clubs_8', 'clubs_9', 'clubs_10', 'clubs_J', 'clubs_Q', 'clubs_K', 'clubs_A']
    hearts = ['hearts_2', 'hearts_3', 'hearts_4', 'hearts_5', 'hearts_6', 'hearts_7', 'hearts_8', 'hearts_9', 'hearts_10', 'hearts_J', 'hearts_Q', 'hearts_K', 'hearts_A']
    deck = spades + diamonds + clubs + hearts
    random.shuffle(deck)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        SCREEN.blit(pygame.image.load("BlackJack/assets/green table.jpg"), (0,0))

        DEALER_HAND_TEXT = get_font(20).render("Dealer's Hand", True, "White")
        DH_RECT = DEALER_HAND_TEXT.get_rect(center=(490, 40))
        SCREEN.blit(DEALER_HAND_TEXT, DH_RECT)

        PLAYER_HAND_TEXT = get_font(20).render("Player's Hand", True, "White")
        PH_RECT = PLAYER_HAND_TEXT.get_rect(midleft=(50, 515))
        SCREEN.blit(PLAYER_HAND_TEXT, PH_RECT)

        DECK_TEXT = get_font(20).render(f"Deck: {len(deck)}", True, "White")
        DECK_RECT = DECK_TEXT.get_rect(center=(150, 138))
        SCREEN.blit(DECK_TEXT, DECK_RECT)

        card_width = 146
        card_height = 204
        card_xpos = 335
        card_ypos_d = 80
        card_ypos_p = 418
        card_arrange = card_width + 11

        # deck 
        back_light = pygame.image.load("BlackJack/assets/playing-cards-master/back_light.png")
        SCREEN.blit(pygame.transform.scale(back_light, (card_width, card_height)), (70, 158))

        if deal_start:
            player_hand, dealer_hand = deal_hand(deck)
            card_sound.play()
            deal_start = False
        
        if player_hit:
            player_hand.append(dealCard(deck))
            card_sound.play()
            player_hit = False

        if dealer_hit:
            dealer_hand.append(dealCard(deck))
            card_sound.play()
            dealer_hit = False
        
        if player_stand:
            dealer_turn = True
            if dealer_stand:
                end_game = True
            
        if active:
            # show player hand
            for i, card in enumerate(player_hand):
                SCREEN.blit(pygame.transform.scale(pygame.image.load(f"BlackJack/assets/playing-cards-master/{card}.png"), (card_width, card_height)), (card_xpos + card_arrange * i, card_ypos_p))
            player_score = calculateTotal(player_hand, card_values)
            PLAYER_SCORE_TEXT = get_font(20).render(f"Score: {player_score}", True, "White")
            PS_RECT = PLAYER_SCORE_TEXT.get_rect(midleft=(50, 545))
            SCREEN.blit(PLAYER_SCORE_TEXT, PS_RECT)
            if player_score == 21:
                player_bj = True
            if player_score > 21:
                player_bust = True
            # show dealer hand
            if hide_card:
                SCREEN.blit(pygame.transform.scale(pygame.image.load(f"BlackJack/assets/playing-cards-master/back_light.png"), (card_width, card_height)), (card_xpos + card_arrange * 1, card_ypos_d))
                SCREEN.blit(pygame.transform.scale(pygame.image.load(f"BlackJack/assets/playing-cards-master/{dealer_hand[0]}.png"), (card_width, card_height)), (card_xpos + card_arrange * 0, card_ypos_d))
                DEALER_HAND_TEXT = get_font(20).render(f"Score: {card_values[dealer_hand[0]]} + ?", True, "White")
                DH_RECT = DEALER_HAND_TEXT.get_rect(midleft=(660, 40))
                SCREEN.blit(DEALER_HAND_TEXT, DH_RECT)
            elif not hide_card: 
                for i, card in enumerate(dealer_hand):
                    SCREEN.blit(pygame.transform.scale(pygame.image.load(f"BlackJack/assets/playing-cards-master/{card}.png"), (card_width, card_height)), (card_xpos + card_arrange * i, card_ypos_d))
                dealer_score = calculateTotal(dealer_hand, card_values)
                DEALER_HAND_TEXT = get_font(20).render(f"Score: {dealer_score}", True, "White")
                DH_RECT = DEALER_HAND_TEXT.get_rect(midleft=(660, 40))
                SCREEN.blit(DEALER_HAND_TEXT, DH_RECT)
                if player_stand and dealer_score >= player_score:
                    dealer_stand = True
                elif dealer_score < 17 and dealer_turn == True:
                    dealer_hit = True
                    dealer_turn = False
                if dealer_score == 21:
                    dealer_bj = True
                if dealer_score > 21:
                    dealer_bust = True
                if dealer_score >= 17:
                    dealer_stand = True


        if player_bust:
            text = 'Player bust!'
            end_game = True
        elif player_bj:
            text = 'Blackjack!'
            end_game = True
        if dealer_bust:
            text = 'Dealer bust!'
            end_game = True
        elif dealer_bj:
            text = 'Blackjack!'
            end_game = True
        RIGHT_TEXT = get_font(20).render(f"{text}", True, "White")
        RT_RECT = RIGHT_TEXT.get_rect(midright=(1240, 360))
        SCREEN.blit(RIGHT_TEXT, RT_RECT)

        button_list = draw_game(active, PLAY_MOUSE_POS)

        if end_game:
            dealer_stand = True
            dealer_turn = False
            dealer_hit = False
            hide_card = False
            SCREEN.blit(pygame.transform.scale(pygame.image.load("BlackJack/assets/Play Rect.png"),(1280, 720)), (0,0))
            text2 = determineWinner(player_score, dealer_score)
            Again_button = Button(image=pygame.transform.scale(pygame.image.load("BlackJack/assets/Play Rect.png"),(150, 50)), pos=(645, 380), text_input="AGAIN", font=get_font(25), base_color="Yellow", hovering_color="Green")
            Again_button.changeColor(PLAY_MOUSE_POS)
            Again_button.update(SCREEN)

        CENTER_TEXT = get_font(20).render(f"{text2}", True, "White")
        CT_RECT = CENTER_TEXT.get_rect(center=(640, 320))
        SCREEN.blit(CENTER_TEXT, CT_RECT)    

        PLAY_BACK = Button(image=None, pos=(30, 30), text_input="<—", font=get_font(25), base_color="White", hovering_color="Red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    button_sound.play()
                    main_menu()
                if active:
                    if button_list[1].checkForInput(PLAY_MOUSE_POS):
                        player_hit = True
                        hide_card = False
                        dealer_turn = True
                    elif button_list[0].checkForInput(PLAY_MOUSE_POS):
                        button_sound.play()
                        player_stand = True
                        hide_card = False  
                if not active:
                    if button_list[0].checkForInput(PLAY_MOUSE_POS):
                        button_sound.play()
                        active = True
                        deal_start = True
                if end_game:
                    if Again_button.checkForInput(PLAY_MOUSE_POS):
                        button_sound.play()
                        play()

        pygame.display.update()

music_status = True
status = ['ON', 'OFF']
sfx_status = True

def options():
    global music_status
    global sfx_status
    global button_sound
    global card_sound
    sfx_tick = True
    music_tick = True
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("OPTIONS", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        MUSIC_TEXT = get_font(45).render("MUSIC:", True, "White")
        MUSIC_RECT = MUSIC_TEXT.get_rect(center=(320, 260))
        SCREEN.blit(MUSIC_TEXT, MUSIC_RECT)

        if music_status:
            MUSIC_BUTTON = Button(image=None, pos=(550, 260), text_input=f"{status[0]}", font=get_font(45), base_color="White", hovering_color="Green")
        elif not music_status:
            MUSIC_BUTTON = Button(image=None, pos=(550, 260), text_input=f"{status[1]}", font=get_font(45), base_color="White", hovering_color="Red")
        MUSIC_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        MUSIC_BUTTON.update(SCREEN)

        SFX_TEXT = get_font(45).render("SOUND:", True, "White")
        SFX_RECT = SFX_TEXT.get_rect(center=(320, 420))
        SCREEN.blit(SFX_TEXT, SFX_RECT)

        if sfx_status:
            SFX_BUTTON = Button(image=None, pos=(550, 420), text_input=f"{status[0]}", font=get_font(45), base_color="White", hovering_color="Green")
        elif not sfx_status:
            SFX_BUTTON = Button(image=None, pos=(550, 420), text_input=f"{status[1]}", font=get_font(45), base_color="White", hovering_color="Red")
        SFX_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        SFX_BUTTON.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(30, 30), text_input="<—", font=get_font(25), base_color="White", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        if not music_status and music_tick:
            mixer.music.pause()
            music_tick = False
        elif music_status and not music_tick:
            mixer.music.unpause()
            music_tick = True
        if not sfx_status and sfx_tick:
            button_sound = mixer.Sound(f"{silence}")
            card_sound = mixer.Sound(f"{silence}")
            sfx_tick = False
        elif sfx_status and not sfx_tick:
            button_sound = mixer.Sound("BlackJack/assets/Button⧸Plate Click (Minecraft Sound).wav")
            card_sound = mixer.Sound("BlackJack/assets/card_deck_flick_click.mp3")
            sfx_tick = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    main_menu()
                if MUSIC_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    music_status = not music_status
                if SFX_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    sfx_status = not sfx_status

        pygame.display.update()

def main_menu():
    clock = pygame.time.Clock()
    global music_status
    global sfx_status
    while True:
        clock.tick(60)
        SCREEN.blit(BG_menu, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("BLACKJACK", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("BlackJack/assets/Play Rect.png"), pos=(640, 250), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("BlackJack/assets/Options Rect.png"), pos=(640, 400), text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("BlackJack/assets/Quit Rect.png"), pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main_menu()
