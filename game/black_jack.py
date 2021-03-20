import random

class BlackJack:
    def __init__(self, players):
        self.players = players

        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.cards = {
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            'ten': 10,
            'jack': 10,
            'queen': 10,
            'king': 10,
            'Ace': 11
        }
        self.used_cards = []

    def process_input(self, message):
        output = ""

        if message.content[1:] == "hit":
            while True:
                drawn_suit = random.choice(self.suits)
                drawn_card, card_value = random.choice(list(self.cards.items()))

                if(drawn_card+drawn_suit) not in self.used_cards:
                    break

            self.used_cards.append(drawn_card+drawn_suit)

            # Add on the score

            # Check if the score is bust or 21
                # If you drew a Ace and bust, make it 1 then check again

                # if you bust end your turn
                #if you win end your turn, force other non bust players to draw until they lose or win

            # 

            output = f'{message.author.name} drew a {drawn_card} of {drawn_suit}'
        else:
            output = "Command unknown"

        return output