# Mini-project #6 - Blackjack

import simplegui
import random

## load card sprite - 2020 x 960
CARD_SIZE = (146, 225)
CARD_CENTER = (80, 120)
card_image = simplegui.load_image("http://i.imgur.com/4WsZrCS.png")

## load back_card sprite - 146 x 225
CARD_BACK_SIZE = (146, 225)
CARD_BACK_CENTER = (78, 118)
card_back = simplegui.load_image("http://i.imgur.com/UT0y8Kb.png")    

# load card sprite - 936x384 - source: jfitz.com
#CARD_SIZE = (72, 96)
#CARD_CENTER = (36, 48)
#card_image = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
#
#CARD_BACK_SIZE = (72, 96)
#CARD_BACK_CENTER = (36, 48)
#card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


# initialize some useful global variables
in_play = True
outcome = ""
score = 0
game_round = 0
player = None
dealer = None

# define globals for cards
SUITS = ('S', 'H', 'C', 'D')
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
        self.rotation = random.randrange(-2,2) * 0.05
            
    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

#   def draw(self, canvas, pos):
#        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
#                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
#        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def draw(self, canvas, loc):
        i = RANKS.index(self.rank)
        j = SUITS.index(self.suit)
        card_pos = [CARD_CENTER[0] + i * (CARD_SIZE[0]+8.2),
                    CARD_CENTER[1] + j * (CARD_SIZE[1]+11.6)]
        canvas.draw_image(card_image, card_pos, CARD_SIZE, loc, CARD_SIZE, self.rotation)

# define hand class
class Hand:
    def __init__(self):
        self.collection = [] # create Hand object
        
    def __str__(self):
        code = ""
        for i in range(len(self.collection)):
            code += str(self.collection[i]) + " "
        return "Hand contains " + str(code)
        #return self.collection # return a string representation of a hand
        
    def add_card(self, card):
        self.card = card
        self.collection.append(self.card)	# add a card object to a hand

    def get_value(self):
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.hand_value = 0	# compute the value of the hand, see Blackjack video
        ace_count = 0
        if len(self.collection) > 0:
            for i in self.collection: # i is each card in the hand
                if str(i)[1] == 'A':
                    ace_count += 1
                for rank, value in VALUES.items(): # Comparing values
                    if str(i)[1] == rank:
                        self.hand_value += value # Adding values
                if str(i)[1] == 'A' and self.hand_value + 10 <= 21:
                    self.hand_value += 10
                elif str(i)[1] == 'A' and self.hand_value + 10 <= 21 and len(self.collection) > 2:
                    return
                elif str(i)[1] == 'A' and ace_count > 1 and self.hand_value + 10 > 21 and len(self.collection) > 2:
                    self.hand_value -= 10
            
        else:
            self.hand_value = 0
        return self.hand_value

    def draw(self, canvas, top, rotation):
        count = 0
        for card in self.collection:
            pos = [150 + count * 155, top]
            card.draw(canvas, pos)
            count += 1
            
# define deck class 
class Deck:
    def __init__(self):
        self.card_deck = []	# create a Deck object
        for i in SUITS:
            for j in RANKS:
                self.card_deck.append(Card(i,j))
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_deck)    # use random.shuffle()

    def deal_card(self):
        return self.card_deck.pop(-1) # deal a card object from the deck
    
    def __str__(self):
        code = ""
        for i in range(len(self.card_deck)):
            code += str(self.card_deck[i]) + " "
        return "Deck contains " + code

#define event handlers for buttons
def deal():
    global outcome, in_play, card_deck, player, dealer, score, game_round
    # your code goes here
    outcome = "Hit or stand?"
    if in_play == True and game_round > 0:
        outcome = "You lost the round"
        score -= 1
    else:
        outcome = "Hit or stand?"
    in_play = True
    game_round += 1
    card_deck = Deck() # Initiate deck
    card_deck.shuffle() # Shuffle

    player = Hand() # Player
    player.add_card(card_deck.deal_card()) # Player picks a card

    dealer = Hand() # Dealer
      
def hit():
    global in_play, score, outcome, card_rotation
    if in_play == False:
        outcome = "New Deal?"
        return
    else:
        outcome = "Hit or stand?"
    
    player.add_card(card_deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        dealer.add_card(card_deck.deal_card()) # Dealer picks a card
        outcome = "You have busted! New Deal?"
        in_play = False
        score -= 1

def stand():
    global outcome, in_play, score
    if in_play == False:
        return
    
    dealer.add_card(card_deck.deal_card()) # Dealer picks a card
    
    while dealer.get_value() < 17:
        dealer.add_card(card_deck.deal_card())
        in_play = False
   
    if dealer.get_value() > 21:
        outcome = "The dealer has busted. New Deal?"
        score += 1
    
    elif player.get_value() <= dealer.get_value():
        outcome = "The dealer wins. New Deal?"
        score -= 1
        
    else:
        outcome = "The player wins. New Deal?"
        score += 1

# draw handler    
def draw(canvas):
    global dealer, player

    canvas.draw_text('Welcome to', (400, 20), 15, 'Black')
    canvas.draw_text('the Curse of', (379, 39), 20, 'Black')
    canvas.draw_text('BlackJack', (340, 72), 40, 'Black')
    canvas.draw_text('BlackJack', (337, 70), 40, 'Red')
    # test to make sure that card.draw works, replace with your code below
    
    dealer.draw(canvas, 250, 0)
#    dealer.draw(canvas, 250)
    player.draw(canvas, 500, 0)
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (150, 250), (146, 225))
       
    canvas.draw_text(outcome, (420 - ((len(outcome)/2)* 9), 120), 20, 'Navy')
    canvas.draw_text("Your score is: ", (680, 120), 20, 'Black')
    canvas.draw_text(str(score), (850, 120), 20, 'Black')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 900, 700)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
