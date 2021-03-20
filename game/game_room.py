from game.snake_eyes import SnakeEyes
from game.black_jack import BlackJack

class GameRoom:
    # Save players and room_id upon initialization
    def __init__(self, players, room_id):
        # Save players in current game lobby
        self.players = players

        # game room id
        self.room_id = room_id

        # game object for the specific game player
        self.gameInstance = None

    # Process input passed by bot
    def process_input(self, message):

        # Check message and act on it
        if message.content[1:5] == "play":
            if message.content[6:] == "SnakeEyes":
                self.gameInstance = SnakeEyes(players=self.players)
                print(f'{self.room_id}: Snake Eyes game has started')
                return "Snake Eyes game has started!"
            if message.content[6:] == "BlackJack":
                self.gameInstance = BlackJack(players=self.players)
                print(f'{self.room_id}: Snake Eyes game has started')
                return "Black Jack game has started!"
        elif message.content[1:5] == "stop":
            self.gameInstance = None
            print(f'{self.room_id}: Game has been ended')
            return "Game has been ended!"
        else:
            if self.gameInstance is not None:
                output = self.gameInstance.process_input(message)
                # If '!' returned at start of output, means game has finished
                if output[0:1] == '!':
                    output = output[1:] + ". Game has ended!"
                    self.gameInstance = None
                print(f'{self.room_id}: {output}')
                return output
            else:
                print(f'{self.room_id}: game instance is null so command is ignored')
                return "Unknown command :("
