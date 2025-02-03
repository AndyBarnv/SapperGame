import pygame
import sqlite3

from consts import DB_NAME
from game_mechanics import Sapper, Difficulties, CellStates, GameStates, Time
from start_page import load_image, terminate


class Counter:
    c0 = "un_000"
    c1 = "un_001"
    c2 = "un_002"
    c3 = "un_003"
    c4 = "un_004"
    c5 = "un_005"
    c6 = "un_006"
    c7 = "un_007"
    c8 = "un_008"
    c9 = "un_009"


COUNTER = {
    "0": Counter.c0,
    "1": Counter.c1,
    "2": Counter.c2,
    "3": Counter.c3,
    "4": Counter.c4,
    "5": Counter.c5,
    "6": Counter.c6,
    "7": Counter.c7,
    "8": Counter.c8,
    "9": Counter.c9,
}


DIR_OBJECTS = {
    CellStates.hidden: "pics/9.png",
    CellStates.hidden_bomb: "pics/9.png",
    CellStates.opened_bomb: "pics/10.png",
    CellStates.marked_cell: "pics/12.png",
    CellStates.marked_bomb: "pics/12.png",
    Counter.c0: "pics/c0.png",
    Counter.c1: "pics/c1.png",
    Counter.c2: "pics/c2.png",
    Counter.c3: "pics/c3.png",
    Counter.c4: "pics/c4.png",
    Counter.c5: "pics/c5.png",
    Counter.c6: "pics/c6.png",
    Counter.c7: "pics/c7.png",
    Counter.c8: "pics/c8.png",
    Counter.c9: "pics/c9.png",
    0: "pics/0.png",
    1: "pics/1.png",
    2: "pics/2.png",
    3: "pics/3.png",
    4: "pics/4.png",
    5: "pics/5.png",
    6: "pics/6.png",
    7: "pics/7.png",
    8: "pics/8.png",
    9: "pics/9.png",
}


class Game:
    def __init__(self, surface, difficult: Difficulties = Difficulties.EASY):
        self.surface = surface
        self.difficult = difficult
        self.sapper = Sapper(difficult)
        self.time = Time()  # Объект класса счётчика времени

        self.init_all()
        self.draw_board()

    def init_all(self):
        self.__init_paddings()
        self.__init_size_square()
        self.__init_counter()
        self.__init_rect_board()
        self.__init_background()
        self.__init_smile()
        self.__init_timer()

    def __init_paddings(self):
        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.left = 18
            self.top = 98

        elif difficult == Difficulties.NORMAL:
            self.left = 31
            self.top = 171

        elif difficult == Difficulties.HARD:
            self.left = 57
            self.top = 164

    def __init_size_square(self):
        # board_rect = pygame.rect.Rect(self.left, self.top, 926 - self.left, 996 - self.top)
        # square_width = board_rect.width // self.sapper.width
        # square_heigt = board_rect.height // self.sapper.height
        #
        # self.size_square = (square_width, square_heigt)

        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.size_square = (29, 29)

        elif difficult == Difficulties.NORMAL:
            self.size_square = (29, 29)

        elif difficult == Difficulties.HARD:
            self.size_square = (27, 27)

    def __init_background(self):
        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.background_image = load_image("pics/background.png")

        elif difficult == Difficulties.NORMAL:
            self.background_image = load_image("pics/background_normal.png")

        elif difficult == Difficulties.HARD:
            self.background_image = load_image("pics/background_hard.png")

        self.width = self.background_image.get_width()
        self.height = self.background_image.get_height()

    def __init_smile(self):
        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.smile_size = (47, 47)

            self.x_smile = self.width // 2 - self.smile_size[0] // 2  # Смайлик будет по середине плашки.
            self.y_smile = 26

        elif difficult == Difficulties.NORMAL:
            self.smile_size = (81, 81)

            self.x_smile = self.width // 2 - self.smile_size[0] // 2  # Смайлик будет по середине плашки.
            self.y_smile = 46

        elif difficult == Difficulties.HARD:
            self.smile_size = (81, 81)

            self.x_smile = self.width // 2 - self.smile_size[0] // 2  # Смайлик будет по середине плашки.
            self.y_smile = 43

        self.smile_rect = pygame.rect.Rect(self.x_smile, self.y_smile, *self.smile_size)

    def __init_counter(self):
        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.x_counter = 27
            self.y_counter = 28
            self.cell_size_counter = (23.5, 42)

        elif difficult == Difficulties.NORMAL:
            self.x_counter = 47
            self.y_counter = 47
            self.cell_size_counter = (43, 76)

        elif difficult == Difficulties.HARD:
            self.x_counter = 87
            self.y_counter = 44
            self.cell_size_counter = (70, 73)

    def __init_timer(self):
        difficult = self.difficult

        if difficult == Difficulties.EASY:
            self.x_timer = 200
            self.y_timer = 27
            self.cell_size_timer = (23.5, 42)

        elif difficult == Difficulties.NORMAL:
            self.x_timer = 350
            self.y_timer = 47
            self.cell_size_timer = (43, 76)

        elif difficult == Difficulties.HARD:
            self.x_timer = 628
            self.y_timer = 44
            self.cell_size_timer = (70, 73)

    def __init_rect_board(self):
        x = self.left
        y = self.top
        width = self.sapper.width * self.size_square[0]
        height = self.sapper.height * self.size_square[1]
        self.rect_board = pygame.rect.Rect(x, y, width, height)

    def draw_board(self):
        self.__draw_background()
        self.__draw_board_easy()
        self.__draw_smile()
        self.draw_counter()
        self.draw_timer()

    def __draw_background(self):
        """
        Отрисовывает фон
        :return:
        """
        self.surface.blit(self.background_image, (0, 0))

    def __draw_board_easy(self):
        _x = self.left
        _y = self.top

        for line in self.sapper.board:
            for item in line:
                image = load_image(DIR_OBJECTS[item])
                image = pygame.transform.scale(image, self.size_square)
                self.surface.blit(image, (_x, _y))
                _x += self.size_square[0]
            _x = self.left
            _y += self.size_square[1]

    def __draw_smile(self):
        state = self.sapper.state
        image = None
        if state == GameStates.GAME:
            image = load_image("pics/start.png")
        elif state == GameStates.END:
            image = load_image("pics/lose.png")
        elif state == GameStates.WIN:
            image = load_image("pics/win.png")
        image = pygame.transform.scale(image, self.smile_size)
        self.surface.blit(image, (self.x_smile, self.y_smile))

    def __get_cell(self, mouse_pos):
        """
        Вернёт координаты клетки, если клик совершён в пределах поля.
        :param mouse_pos:
        :return:
        """
        _x_width = self.sapper.width * self.size_square[0] + self.left
        _y_height = self.sapper.height * self.size_square[1] + self.top

        if (not (self.left <= mouse_pos[0] <= _x_width) or
                not (self.top <= mouse_pos[1] <= _y_height)):
            return None
        x = (mouse_pos[1] - self.top) // self.size_square[1]
        y = (mouse_pos[0] - self.left) // self.size_square[0]
        return int(y), int(x)

    def __on_click(self, cell_coords, btn):
        """
        Даёт реакцию на нажатие клетки.
        :param cell_coords:
        :return:
        """
        x, y = cell_coords
        if btn == 1:
            self.sapper.open_cell(x, y)
        elif btn == 3:
            self.sapper.set_flag(x, y)

        if self.sapper.state == GameStates.END:
            print("Хана. Попал на бомбу.")
            self.time.state = GameStates.END
            self.end_game()
            safe_game(self)  # Сохранение игры в бд.
            # Нужно закончить игру и открыть все бомбы.

        elif self.sapper.state == GameStates.WIN:
            print('Ура, победа!')
            self.time.state = GameStates.WIN
            safe_game(self)  # Сохранение игры в бд.


    def get_click(self, mouse_pos, btn):
        """
        Проверяет
        :param mouse_pos:
        :return:
        """
        cell = self.__get_cell(mouse_pos)
        if cell is None:
            print("Клик совершён вне поля!")
            return None
        self.__on_click(cell, btn)

    def end_game(self):
        """Покажет все не отмеченные флагом бомбы."""

        _x = self.left
        _y = self.top

        for line in self.sapper.board:
            for item in line:
                if item == CellStates.hidden_bomb:
                    image = load_image(DIR_OBJECTS[CellStates.opened_bomb])
                    self.surface.blit(image, (_x, _y))
                _x += self.size_square[0]
            _x = self.left
            _y += self.size_square[1]

        self.sapper.state = GameStates.END

    def draw_timer(self):
        seconds = self.time.seconds

        _x = self.x_timer
        _y = self.y_timer

        number = self.__create_number(seconds)

        for num in number:
            image = load_image(DIR_OBJECTS[num])
            image = pygame.transform.scale(image, self.cell_size_timer)
            self.surface.blit(image, (_x, _y))
            _x += self.cell_size_timer[0]

        self.time.update()  # Обновление счётчика каждый 60-й кадр, т.е. каждую секунду.

    def draw_counter(self):
        _x = self.x_counter
        _y = self.y_counter
        number = self.__create_number(self.sapper.flags_count)
        for num in number:
            image = load_image(DIR_OBJECTS[num])
            image = pygame.transform.scale(image, self.cell_size_counter)
            self.surface.blit(image, (_x, _y))
            _x += self.cell_size_counter[0]

        # self.time.update()  # Обновление счётчика каждый 60-й кадр, т.е. каждую секунду.

    def __create_number(self, n):
        """
        Вспомогательный метод для draw_timer
        :return:
        """
        _number = ""
        if 100 > n >= 10:
            _number = "0" + str(n)

        elif 10 > n > 0:
            _number = ("0" * 2) + str(n)

        else:
            _number = "000"

        return [COUNTER[item] for item in _number]


def safe_game(game):
    """
    Функция сохранения результатов игры в базу данных.
    :param game:
    :return:
    """
    res = 'win' if game.sapper.state == GameStates.WIN else 'failed'
    sec = game.time.seconds
    cells = game.sapper.opened_cells
    if game.difficult == Difficulties.EASY:
        diff = 'easy'
    elif game.difficult == Difficulties.NORMAL:
        diff = 'normal'
    else:
        diff = 'hard'

    # con = sqlite3.connect(DB_NAME) # Так строка, выглядит в итоговом варианте. Пока, чтобы не засорить бд, закомментировал её
    con = sqlite3.connect("C:/Users/Andrew/pythonProjects.game_history.db")
    cur = con.cursor()

    cur.execute("""INSERT INTO games(results,time,opened_cells,difficulty) VALUES(?,?,?,?)""",
                (res, sec, cells, diff))

    con.commit()
    con.close()


def __techinkal_print_board(board: list):
    """
    Печатает поле. Вспомогательная функция
    :param board:
    :return:
    """
    for line in board:
        for item in line:
            print(item.value, end=", ")
        print("\n")


def __set_size_for_difficult(difficult: Difficulties):
    if difficult == Difficulties.EASY:
        size = 298, 377

    elif difficult == Difficulties.NORMAL:
        # size = 501, 580
        size = 523, 663

    elif difficult == Difficulties.HARD:
        size = 927, 626

    return size


def game_page_create(difficult):
    size = __set_size_for_difficult(difficult)
    screen = pygame.display.set_mode(size)
    game_obj = Game(screen, difficult)
    return game_obj


def game_update(Game_obj: Game):
    menu = Game_obj
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event = event.dict
            btn = event["button"]
            if (btn == 1 or btn == 3) and menu.smile_rect.collidepoint(event["pos"]):
                menu = Game(menu.surface, menu.difficult)
                __techinkal_print_board(menu.sapper.board)
            if not menu.sapper.state == GameStates.GAME:
                continue

            if btn == 1 or btn == 3:  # Если нажата левая кнопка мыши
                if menu.rect_board.collidepoint(mouse_pos := event["pos"]):
                    if menu.time.state != GameStates.GAME:
                        menu.time.state = GameStates.GAME
                    menu.get_click(mouse_pos, btn)
    menu.draw_board()
    return menu


if __name__ == '__main__':
    pygame.init()

    size = WIDTH, HEIGHT = 298, 377
    screen = pygame.display.set_mode(size)
    menu = Game(screen)
    __techinkal_print_board(menu.sapper.board)

    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event = event.dict
                btn = event["button"]
                if (btn == 1 or btn == 3) and menu.smile_rect.collidepoint(event["pos"]):
                    menu = Game(screen, menu.difficult)
                    __techinkal_print_board(menu.sapper.board)
                if not menu.sapper.state == GameStates.GAME:
                    continue

                if btn == 1 or btn == 3:  # Если нажата левая кнопка мыши
                    if menu.rect_board.collidepoint(mouse_pos := event["pos"]):
                        if menu.time.state != GameStates.GAME:
                            menu.time.state = GameStates.GAME
                        menu.get_click(mouse_pos, btn)

        menu.draw_board()
        clock.tick(fps)
        pygame.display.flip()

    terminate()
