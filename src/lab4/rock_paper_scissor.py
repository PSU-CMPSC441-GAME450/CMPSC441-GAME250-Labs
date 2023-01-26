# From https://codereview.stackexchange.com/questions/237601/simple-python-turn-based-battle-game
""" Lab 4: Rock-Paper-Scissor AI Agent
In this lab you will build one AI for Rock-Paper-Scissors that defeat a few opponent AI's.
You will update the AI agent class to create your first AI agent for this course, 
using the precept sequence to find out which opponent agent you are facing, 
so that it can beat these three opponent agents:

    Agent Single:  this agent picks a weapon at random at the start, 
                   and always plays that weapon.  
                   For example: 2,2,2,2,2,2,2,.....

    Agent Switch:  this agent picks a weapon at random at the start,
                   and randomly picks a weapon once every 10 rounds (could happen to be the same one).  
                   For example:  2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,...

    Agent Mimic:  this agent picks a weapon at random in the first round, 
                  and then always does what you did the previous round.  
                  For example:  if you played 1,2,0,1,2,0,1,2,0,...  
                   then this agent would play 0,1,2,0,1,2,0,1,2,...

Discussions in lab:  You don't know ahead of time which opponent you will be facing, 
so the first few rounds will be used to figure this out.   How?

Once you've figured out the opponent, apply rules against that opponent. 
A model-based reflex agent uses rules (determined by its human creator) to decide which action to take.

If your AI is totally random, you should be expected to win about 33% of the time, so here is the requirement:  
In 100 rounds, you should consistently win at least 85 rounds to be considered a winner.
"""
import random
weapons = ["Rock", "Paper", "Scissor"]

def console_weapon_select():
    """
    It takes a list of weapons, prints them out, and returns the user's choice
    :return: The weapon that the user has chosen.
    """
    weapons_list = [f'{i+1}-{w}' for i, w in enumerate(weapons)]
    choice = int(input(f'Choose your weapon {", ".join(weapons_list)}:  '))
    weapon = choice - 1
    return weapon

def random_weapon_select():
    choice = random.randint(1, 3)
    weapon = choice - 1
    return weapon

# > The `Player` class is a blueprint for creating objects that represent a player in the game
class Player:
    def __init__(self, name):
        self.name = name
        self.my_choices = []
        self.opponent_choices = []

    def selectWeapon(self, last_opponent_move):
        """
        > The function takes in the opponent's last move, updates the player's history of opponent's moves,
         and then updates the player's history of their own moves
        
        :param last_opponent_move: The weapon that the opponent played in the previous round
        """
        # ** Previous round update **
        if last_opponent_move is not None:
            self.opponent_choices.append(last_opponent_move)

        # ** Current round update **
        self.weapon = self.weapon_selecting_strategy()
        self.my_choices.append(self.weapon)
    
    def weapon_selecting_strategy(self):
        return console_weapon_select()
    

# Child class of player with override methods for weapon
class ComputerPlayer(Player):
    def __init__(self,name, computer_agent=-1):
        super().__init__(name)
        if computer_agent == -1:
            self.agent = random.randint(0, 2)
        else:
            self.agent = computer_agent
        self.initial_weapon = random_weapon_select()
        self.print_agent()

    def print_agent(self):
        if self.agent == 0:
            print("Agent: Single")
        elif self.agent == 1:
            print("Agent: Switch")
        elif self.agent == 2:
            print("Agent: Mimic")

    def agent_single(self):
        return self.initial_weapon

    def agent_switch(self):
        """
        > The agent will switch to a random weapon every 10 turns
        :return: The initial weapon is being returned.
        """
        if len(self.opponent_choices)%10 == 0:
            self.initial_weapon = random_weapon_select()
        return self.initial_weapon

    def agent_mimic(self):
        """
        > The agent will mimic the opponent's last choice
        :return: The last choice of the opponent.
        """
        if len(self.opponent_choices) == 0:
            return self.initial_weapon

        return self.opponent_choices[-1]

    def weapon_selecting_strategy(self):
        if self.agent == 0:
            return self.agent_single()
        if self.agent == 1:
            return self.agent_switch()
        if self.agent == 2:
            return self.agent_mimic()

        raise ValueError("Agent not found")


class Game:
    def __init__(self, players):
        self.gameOver = False
        self.round = 0
        self.players = players
        self.players_tally = {player:0 for player in players}

    def newRound(self):
        self.round += 1
        print(f'\n***   Round: {self.round}   ***\n')  

    def updateWin(self, result):
        if result != 0:
            self.players_tally[result] += 1

    def displayResult(self, player, opponent, winner):
        print(f'{player.name} used a {weapons[player.weapon]}, {opponent.name} used a {weapons[opponent.weapon]}')
        if winner == 0:
            print("*** Draw ***")
        else:
            print(f'{weapons[winner.weapon]} beats {weapons[player.weapon if opponent == winner else opponent.weapon]}')

    def takeTurn(self, player, opponent):

        # Decision Array
        #
        #           Rock|  Paper |  Scissor
        #           ______|________|_______
        # Rock:    0 |  2  |  1
        # Paper:    1  |  0 |  2   
        # Scissor:    2  |  1  |  0

        decisionArray = [[0, 2, 1], [1, 0, 2], [2, 1, 0]]
        print(f"\n{player.name} used a {weapons[player.weapon]}, {opponent.name} used a {weapons[opponent.weapon]}")
        winner = 0
        if decisionArray[player.weapon][opponent.weapon] == 1:
            winner = player
        elif decisionArray[player.weapon][opponent.weapon] == 2:
            winner = opponent
        elif decisionArray[player.weapon][opponent.weapon] == 0:
            winner = 0
        self.displayResult(player, opponent, winner)
        return winner


# Setup Game Objects
def run_game(agent, n_rounds=3, computer_agent=-1):
    """
    > The function `run_game` takes in an agent, number of rounds to play and a computer agent, 
    and plays a game of rock-paper-scissors with them for the specified number of rounds.
    
    :param agent: The agent you want to play against the computer
    :param n_rounds: The number of rounds to play, defaults to 3 (optional)
    :param computer_agent: The agent that the computer will use, defaults to -1 meaning a randomly selected agent (optional)
    """
    last_opponent_move = [None, None] 
    computer = ComputerPlayer("Computer", computer_agent)

    players = [agent, computer]
    currentGame = Game(players)

    # Main Game Loop
    for _ in range(n_rounds):
        currentGame.newRound()
        for player, last_opp_move in zip(players, last_opponent_move):
            player.selectWeapon(last_opponent_move=last_opp_move)
        currentGame.updateWin(currentGame.takeTurn(*players))
        last_opponent_move = [players[1].weapon, players[0].weapon]

    # Display Results
    print("\n***   Game Over   ***\n")
    computer.print_agent()
    for player, score in currentGame.players_tally.items():
        print(f'{player.name} won {score} rounds')
    
    
if __name__ == '__main__':
    human = Player("Mark")
    run_game(human)