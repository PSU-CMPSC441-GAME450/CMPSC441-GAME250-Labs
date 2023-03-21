import pygame
from pathlib import Path

from lab11.sprite import Sprite
from lab11.turn_combat import CombatPlayer, Combat
from lab11.pygame_ai_player import PyGameAICombatPlayer
from lab11.pygame_human_player import PyGameHumanCombatPlayer

AI_SPRITE_PATH = Path("assets/ai.png")

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


class PyGameComputerCombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        if 30 < self.health < 50:
            self.weapon = 2
        elif self.health < 30:
            self.weapon = 1
        else:
            self.weapon = 0
        return self.weapon


def run_pygame_combat(combat_surface, screen, player_sprite):
    currentGame = Combat()
    player = PyGameHumanCombatPlayer("Legolas")
    """ Add a line below that will reset the player object
    to an instance of the PyGameAICombatPlayer class"""

    opponent = PyGameComputerCombatPlayer("Computer")
    opponent_sprite = Sprite(
        AI_SPRITE_PATH, (player_sprite.sprite_pos[0] - 100, player_sprite.sprite_pos[1])
    )

    players = [player, opponent]

    # Main Game Loop
    while not currentGame.gameOver:
        screen.blit(combat_surface, (0, 0))
        player_sprite.draw_sprite(screen)
        opponent_sprite.draw_sprite(screen)
        text_surface = game_font.render(
            "Choose s-Sword a-Arrow f-Fire!", True, (0, 0, 150)
        )
        screen.blit(text_surface, (50, 50))
        pygame.display.update()

        states = list(reversed([(player.health, player.weapon) for player in players]))
        for current_player, state in zip(players, states):
            current_player.selectAction(state)

        currentGame.newRound()
        currentGame.takeTurn(player, opponent)
        print("%s's health = %d" % (player.name, player.health))
        print("%s's health = %d" % (opponent.name, opponent.health))
        currentGame.checkWin(player, opponent)
