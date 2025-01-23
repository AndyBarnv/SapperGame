import random
import enum


class Difficulties(enum.Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


class CellStates(enum.Enum):
    hidden = -1
    hidden_bomb = 10
    opened_bomb = 11
    is_opened = [0, 1, 2, 3, 4, 5, 6, 7, 8]


class GameStates(enum.Enum):
    GAME = 1
    WIN = 2
    END = 3


class Sapper:
    def __init__(self, difficulty=Difficulties.EASY):
        if difficulty == Difficulties.EASY:
            self.width = 9
            self.height = 9
            self.mines = 10
        elif difficulty == Difficulties.NORMAL:
            self.width = 16
            self.height = 16
            self.mines = 40
        elif difficulty == Difficulties.HARD:
            self.width = 30
            self.height = 16
            self.mines = 99

        self.state = GameStates.GAME
        self.board = [[CellStates.hidden] * self.width for _ in range(self.height)]
        self.bombs = []
        self.opened_cells = 0
        self.safe_cells = self.width * self.height - self.mines

        for i in range(self.mines):
            x, y = random.randrange(self.width), random.randrange(self.height)
            if self.board[y][x] == CellStates.hidden_bomb:
                while self.board[y][x] == CellStates.hidden_bomb:
                    x, y = random.randrange(self.width), random.randrange(self.height)
            self.board[y][x] = CellStates.hidden_bomb
            self.bombs.append((x, y))

    def search_mines(self, x, y):
        mines = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if j < 0 or j >= self.width or i < 0 or i >= self.height or (i == y and j == x):
                    continue
                if self.board[i][j] == CellStates.hidden_bomb:
                    mines += 1
        return mines

    def open_cell(self, x, y):
        if self.board[y][x] == CellStates.hidden_bomb:
            for (x, y) in self.bombs:
                self.board[y][x] = CellStates.opened_bomb
            self.state = GameStates.END
        elif self.board[y][x] == CellStates.hidden:
            mines = self.search_mines(x, y)
            self.board[y][x] = mines
            self.opened_cells += 1
            if not mines:
                for i in range(y - 1, y + 2):
                    for j in range(x - 1, x + 2):
                        if j < 0 or j >= self.width or i < 0 or i >= self.height or (i == y and j == x):
                            continue
                        if self.board[i][j] == CellStates.hidden:
                            self.open_cell(j, i)
            if self.opened_cells == self.safe_cells:
                self.state = GameStates.WIN
