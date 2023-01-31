
# > The `Player` class is a blueprint for creating objects that represent a player in the game
class Player:
    def __init__(self, name, strategy=lambda : 1):
        self.name = name
        self.my_choices = []
        self.opponent_choices = []
        self.strategy = strategy

    def selectAction(self, percept):
        """
        > The function takes in the opponent's last move, updates the player's history of opponent's moves,
         and then updates the player's history of their own moves
        
        :param percept: The weapon that the opponent played in the previous round
        """
        # ** Previous round update **
        if percept is not None:
            self.opponent_choices.append(percept)

        # ** Current round update **
        self._action = self.weapon_selecting_strategy()
        self.my_choices.append(self.action)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action
    
    def weapon_selecting_strategy(self):
        return self.strategy()