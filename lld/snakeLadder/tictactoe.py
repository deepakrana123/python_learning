from abc import ABC, abstractmethod


class Game(ABC):
    @abstractmethod
    def play(self):
        pass


class Player(ABC):
    @abstractmethod
    def get_names(self) -> str:
        pass


class Board(ABC):
    @abstractmethod
    def display(self):
        pass


class RuleEngine(ABC):
    @abstractmethod
    def is_winner(self, board, player):
        pass

    @abstractmethod
    def is_draw(self, board):
        pass


class TicTacToePlayer(Player):

    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol


class TicTacToeBoard(Board):
    def __init__(self):
        self.grid = [["" for _ in range(3)]]

    def display(self):
        for row in self.grid:
            print("|".join(row))
            print("-" * 5)

    def place_symbol(self, row: int, col: int, symbol):
        if self.grid[row][col] == " ":
            self.grid[row][col] = symbol
            return True
        return False

    def get_cell(self, row, col):
        return self.grid[row][col]

    def is_full(self):
        return all(cell != "" for row in self.grid for cell in row)


class TicTacToRuleEngine(RuleEngine):
    def is_winner(self, board, player) -> bool:
        symbol = player.get_symbol()
        g = board.grid

        for row in g:
            if all(cell == symbol for cell in row):
                return True

        for col in range(3):
            if all(g[row][col] == symbol for row in range(3)):
                return True

        if all(g[i][i] == symbol for i in range(3)):
            return True

        if all(g[i][2 - i] == symbol for i in range(3)):
            return True

        return False

    def is_draw(self, board) -> bool:
        return board.is_full()


class TicTacToeGame(Game):
    def __init__(self):
        self.board = TicTacToeBoard()
        self.players = [TicTacToePlayer("Alice", "X"), TicTacToePlayer("Bob", "O")]
        self.rule_engine = TicTacToRuleEngine()

    def play(self):
        current = 0
        winner = None

        while True:
            player = self.players[current]
            self.board.display()

            try:
                move = input(
                    f"{player.get_name()} ({player.get_symbol()}), enter move (row,col): "
                )
                row, col = map(int, move.strip().split(","))
            except:
                print("Invalid input. Try again.")
                continue

            if not (0 <= row < 3 and 0 <= col < 3):
                print("Move out of bounds. Try again.")
                continue

            if not self.board.place_symbol(row, col, player.get_symbol()):
                print("Cell already taken. Try again.")
                continue

            if self.rule_engine.is_winner(self.board, player):
                self.board.display()
                print(f"🎉 {player.get_name()} wins!")
                break

            if self.rule_engine.is_draw(self.board):
                self.board.display()
                print("It's a draw!")
                break

            current = 1 - current  # Switch turn


class GameFactory:
    @staticmethod
    def create_game(game_type: str):
        # if game_type == "snake_ladder":
        #     return SnakeLadderGame()
        # el
        if game_type == "tic_tac_toe":
            return TicTacToeGame()
        else:
            raise ValueError("Unknown game type")
