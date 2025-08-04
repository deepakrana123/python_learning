import random
from abc import ABC, abstractmethod
from collections import deque


class Dice(ABC):
    @abstractmethod
    def roll(self) -> int:
        pass


class SingleDice(Dice):
    def __init__(self, faces=6):
        self.faces = faces

    def roll(self) -> int:
        return random.randint(1, self.faces)


class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0

    def get_position(self) -> int:
        return self.position

    def set_position(self, position: int):
        self.position = position

    def __str__(self):
        return f"{self.name} (Position: {self.position})"


class Board:
    def __init__(self, size: int, snakes: dict, ladders: dict):
        self.size = size
        self.snakes = snakes
        self.ladders = ladders

    def get_final_position(self, position: int):
        if position in self.snakes:
            return self.snakes[position]

        elif position in self.ladders:
            return self.ladders[position]
        else:
            return position


class RuleEngine:
    def __init__(self, board: Board):
        self.board = board

    def move_player(self, player, dice_roll):
        current = player.get_position()
        tentative = current + dice_roll
        if tentative > self.board.size:
            print(f"{player.name} rolled {dice_roll}")
            return current
        final = self.board.get_final_position(tentative)
        return final

    def is_winner(self, player) -> bool:
        return player.get_position() == self.board.size


class Game:
    def __init__(self, board, players, dice, rule_engine):
        self.board = board
        self.players = deque(players)
        self.dice = dice
        self.rule_engine = rule_engine
        self.is_over = False

    def play(self):
        while not self.is_over:
            player = self.players.popleft()
            dice_roll = self.dice.roll()
            new_position = self.rule_engine.move_player(player, dice_roll)
            player.set_position(new_position)

            if self.rule_engine.is_winner(player):
                print(f"🎉 {player.name} wins the game!")
                self.is_over = True
            else:
                self.players.append(player)


def main():
    snakes = {99: 10, 90: 50, 75: 32}
    ladders = {4: 25, 13: 46, 40: 89}
    board = Board(size=100, snakes=snakes, ladders=ladders)

    players = [Player("Alice"), Player("Bob")]
    dice = SingleDice(6)
    rule_engine = RuleEngine(board)

    game = Game(board, players, dice, rule_engine)
    game.play()


if __name__ == "__main__":
    main()
