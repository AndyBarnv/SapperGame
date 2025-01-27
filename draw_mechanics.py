import pygame

from game_mechanics import Sapper, Difficulties, CellStates, GameStates, Time
from startPage import load_image, terminate


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


class Menu:
    def __init__(self, surface, difficult: Difficulties = Difficulties.EASY):
        self.left = 18
        self.top = 98
        self.surface = surface
        self.difficult = difficult
        self.size_square = (29, 29)
        self.sapper = Sapper(difficult)
        self.time = Time()  # Объект класса счётчика времени

        self.init_all()
        self.draw_board()

    def init_all(self):
        self.__init_timer()
        self.__init_rect_board()
        self.__init_background()
        self.__init_smile()

    def __init_background(self):
        self.background_image = load_image("pics/background.png")
        self.width = self.background_image.get_width()
        self.height = self.background_image.get_height()

    def __init_smile(self):
        self.smile_size = (47, 47)

        self.x_smile = self.width // 2 - self.smile_size[0] // 2    # Смайлик будет по середине плашки.
        self.y_smile = 26

        self.smile_rect = pygame.rect.Rect(self.x_smile, self.y_smile, *self.smile_size)

    def __init_timer(self):
        self.cell_size_timer = (23.5, 42)

        if self.difficult == Difficulties.EASY:
            self.x_timer = 27
            self.y_timer = 28
        #   Ну и для остальных сложностей тоже надо расписать.

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
        return y, x

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
            # Нужно закончить игру и открыть все бомбы.

        elif self.sapper.state == GameStates.WIN:
            print('Ура, победа!')
            self.time.state = GameStates.WIN

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
        _x = self.x_timer
        _y = self.y_timer
        number = self.__create_number()
        for num in number:
            image = load_image(DIR_OBJECTS[num])
            self.surface.blit(image, (_x, _y))
            _x += self.cell_size_timer[0]

        self.time.update() # Обновление счётчика каждый 60-й кадр, т.е. каждую секунду.

    def __create_number(self):
        """
        Вспомогательный метод для draw_timer
        :return:
        """
        _number = ""
        count = self.sapper.flags_count
        if 100 > count >= 10:
            _number = "0" + str(self.sapper.flags_count)

        elif 10 > count > 0:
            _number = ("0" * 2) + str(self.sapper.flags_count)

        else:
            _number = "000"

        return [COUNTER[item] for item in _number]


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


if __name__ == '__main__':
    pygame.init()

    size = WIDTH, HEIGHT = 298, 377
    screen = pygame.display.set_mode(size)
    menu = Menu(screen)
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
                    menu = Menu(screen)
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