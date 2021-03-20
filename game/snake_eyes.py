import random

# Snake Eyes game.
# Rules: Winner - first person to 21 points or snake eyes
class SnakeEyes:

    def __init__(self, players):
        self.players = players
        self.scores = {}

        # Used to allow each player a roll per round to each player
        self.turn_left = {}

        # Setup score dictionary for each player
        for player in players:
            self.scores[player.id] = 0
            self.turn_left[player.id] = True

    def process_input(self, message):
        # Find player who called the command
        player = None
        for p in self.players:
            if p.id == message.author.id:
                player = p
                break

        # Check the player is in the player list
        if player is not None:

            # Deal with the command
            if message.content[1:] == "roll":
                # Check if player is allowed to roll
                allowed_turn = self.turn_left.get(player.id)
                if allowed_turn is None:
                    return player.name + " has lost, wait for game to finish..."
                if allowed_turn is True:
                    # Update turn list
                    self.turn_left[player.id] = False

                    # Roll twice
                    roll1 = random.randint(1,6)
                    roll2 = random.randint(1,6)
                    # Get players score and add on rolls, and update list
                    player_score = self.scores.get(player.id)
                    player_score = player_score + roll1 + roll2
                    self.scores[player.id] = player_score

                    # Output message
                    output = str(player.name) + " has rolled - " + str(roll1) + ", " + str(roll2) + ". Final score: " + str(player_score)

                    # Check the score
                    if roll1 == 1 and roll2 == 1:
                        output = "!" + str(player.name) + " has rolled snake eyes, player wins"
                    if player_score == 21:
                        output = "!" + output + ", player has won"
                    elif player_score > 21:
                        output = output + ", player has lost"
                        # Remove player from turn list
                        self.turn_left.pop(player.id)

                    # Check if all but one has lost
                    if len(self.turn_left) == 1:
                        # Get last key (player.id)
                        for key in self.turn_left:
                            # Find who the key belongs to
                            for p in self.players:
                                if p.id == key:
                                    # Include previous output
                                    return "!" + output + ". " + str(p.name) + " is last one standing, default win"

                    # Update round if needed
                    self.new_round()

                    # Return output
                    return output
                else:
                    return player.name + " is over, wait for others to finish their turn..."
            else:
                return "Command not recognized by snake eyes"

        else:
            print("Player was not found")
            return None

    def new_round(self):
        # Check that all players have finished their turn
        round_over = True
        for key in self.turn_left:
            if self.turn_left.get(key):
                round_over = False
                break

        # If all players are done, update round
        if round_over:
            for key in self.turn_left:
                self.turn_left[key] = True