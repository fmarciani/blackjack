# PASTE AND RUN THE FOLLOWING CODE IN HTTP://WWW.CODESKULPTOR.ORG

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
result = ""
score = 0
card_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = [] # create Hand object

    def __str__(self):
        hand_list = ""
        for i in self.cards:
            hand_list = hand_list + str(i) + " "
        return "Hand contains " + hand_list
    
    def add_card(self, card):
        self.cards.append(card) # add a card object to a hand

    def get_value(self):
    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    # compute the value of the hand, see Blackjack video
        hand_value = 0
        num_aces = 0
        for value in self.cards:
            hand_value += VALUES[value.get_rank()]
            if value.get_rank() == "A":
                num_aces += 1
        if num_aces > 0 and hand_value + 10 <= 21:
            hand_value += 10
            return hand_value
        else:
            return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 85	

# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                deck = Card(suit, rank)
                self.deck.append(deck)
   
    def __str__(self):
        deck_stack = ""
        for i in self.deck:
            deck_stack = deck_stack + str(i) + " "
        return "Deck contains " + deck_stack 
    
    def shuffle(self):
        return random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
#define event handlers for buttons
def deal():
    global outcome, in_play, my_deck, my_hand, dealer_hand, score, result
    outcome = "Hit or stand?"
    result = ""
    my_deck = Deck()
    my_deck.shuffle()
    my_hand = Hand()
    dealer_hand = Hand()
    my_hand.add_card(my_deck.deal_card())
    my_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    if in_play == True:
        score -= 1
        result = "Game was in progress; you lose."
        outcome = "Hit or stand?"
    in_play = True

def hit():
    global in_play, score, outcome, result
    # if the hand is in play, hit the player
    if in_play == True:
        my_hand.add_card(my_deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if my_hand.get_value() > 21:
            result = "You busted and lost."
            outcome = "New deal?"
            score -= 1
            in_play = False
       
def stand():
    global in_play, outcome, score, result
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if my_hand.get_value() > 21:
        result = "You've already busted."
        in_play = False
    # assign a message to outcome, update in_play and score
    elif in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
        
        if dealer_hand.get_value() > 21:
            outcome = "New deal?"
            result = "Dealer has busted. You win!"
            score += 1
            in_play = False
        else:
            if my_hand.get_value() <= dealer_hand.get_value():
                outcome = "New deal?"
                result = "Dealer wins."
                score -= 1
                in_play = False
            elif my_hand.get_value() > dealer_hand.get_value():
                outcome = "New deal?"
                result = "You win!"
                score += 1
                in_play = False

# draw handler    
def draw(canvas):
    global score, outcome, result, in_play
    # test to make sure that card.draw works, replace with your code below
    dealer_card_pos = [40, 200]
    player_card_pos = [dealer_card_pos[0], dealer_card_pos[1] + 200]
    dealer_hand.draw(canvas, dealer_card_pos)
    my_hand.draw(canvas, player_card_pos)
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (76, 248), CARD_BACK_SIZE)
        
    canvas.draw_text("Blackjack", (200, 50), 50, "Yellow")
    canvas.draw_text("Dealer:", (40, 170), 30, "Black")
    canvas.draw_text("Player:", (40, 370), 30, "Black")
    canvas.draw_text(result, (180, 170), 30, "Black")
    canvas.draw_text(outcome, (180, 370), 30, "Black")
    canvas.draw_text("SCORE: " + str(score), (235, 90), 30, "White")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()