import pygame
import os
import sys
import sqlite3

from consts import DB_NAME
from game_mechanics import Difficulties


DIFFICULTIES_DIR = {
    "EASY": Difficulties.EASY,
    "NORMAL": Difficulties.NORMAL,
    "HARD": Difficulties.HARD
}


class Button:
    def __init__(self, surface, color: str, hover_color: str, text: str, rect: pygame.rect.Rect):
        self.color = pygame.color.Color(color)
        self.hover_color = pygame.color.Color(hover_color)
        self.text = text
        self.rect = rect
        self.surface = surface
        self.is_pressed = False

    def draw(self, is_hovered=False):
        color = self.hover_color if is_hovered else self.color
        draw_button(self.surface, self.text, self.rect, color)


def draw_button(surface, text, rect, color):
    """
    Вспомогательная функция. Отрисовывает прямоугольник с текстом поверх.
    :param surface:
    :param text:
    :param rect:
    :param color:
    :return:
    """
    font = pygame.font.Font(None, 30)
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, pygame.color.Color("white"))
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def start_render_text(screen, WIDTH, HEIGHT):
    """
    Рендерит нужный текст в нужном месте. Вспомогательная функция.
    :param screen:
    :param WIDTH:
    :param HEIGHT:
    :return:
    """
    intro_text = ["САПЁР",
                  "Правила игры",
                  "Для победы необходимо найти все", "мины на игровом поле,",
                  "используя числовые подсказки."]

    fon = pygame.transform.scale(load_image('img/background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 70
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def load_image(name, colorkey=None):
    """
    Передаваемый файл ищется в директории "data".
    :param name:
    :param colorkey:
    :return:
    """
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    """
    Завершает приложение.
    :return:
    """
    pygame.quit()
    sys.exit()


def start_screen(screen, width, height):
    """
    Функция, которая формирует кадр. Стартовую страницу.
    :param screen:
    :param width:
    :param height:
    :return:
    """
    start_render_text(screen, width, height)

    btn_width, btn_height = (100, 50)
    indent = 10

    btn_x, btn_y = (width // 2 - (btn_width + indent) * 3 // 2, 230)
    btns = []
    btn_texts = ["EASY", "NORMAL", "HARD"]

    for text in btn_texts:
        rect = pygame.rect.Rect(btn_x, btn_y, btn_width, btn_height)

        btn = Button(screen, "black", "red", text, rect)
        btns.append(btn)
        btn_x += btn_width + indent

    btns[0].is_pressed = True
    btns[0].draw(is_hovered=True)   # По дефолту ставим сложность "EASY"

    btn_rect = pygame.rect.Rect((width // 2 - btn_width // 2, 300), (80, 50))
    btn = Button(screen, "black", "red", "START", btn_rect)
    btns.append(btn)

    btn_rect = pygame.rect.Rect((width // 2 - 75, 360), (150, 50))
    btn = Button(screen, "black", "red", "VIEW HISTORY", btn_rect)
    btns.append(btn)

    for btn in btns[1:]:
        btn.draw()

    return btns


def start_page_update(screen, btns, size):
    """
    Функция, которая обрабатывает события на окне старта.
    :param screen:
    :param btns:
    :param size:
    :return:
    """

    difficult = None
    for btn in btns:
        if btn.is_pressed:
            difficult = DIFFICULTIES_DIR[btn.text]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event = event.dict
            if event["button"] == 1:  # Если нажата левая кнопка мыши
                for btn in btns:
                    if btn.text == "START" and btn.rect.collidepoint(event["pos"]):
                        return difficult
                    elif btn.text == "VIEW HISTORY" and btn.rect.collidepoint(event["pos"]):
                        view_history(screen, *size)
                        continue

                    if btn.rect.collidepoint(event["pos"]):
                        btn.is_pressed = True
                        difficult = btn.text
                        btn.draw(is_hovered=True)
                    else:
                        btn.is_pressed = False
                        btn.draw()
        elif event.type == pygame.KEYDOWN:
            event = event.dict
            if event['key'] == 13:
                btns = start_screen(screen, *size)


def view_history(screen, width, height):
    """
    Функция для отрисовки истории игр из БД.
    :param screen:
    :param width:
    :param height:
    :return:
    """

    fon = pygame.transform.scale(load_image('img/background.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    history_data = cur.execute("SELECT * FROM games").fetchall()[-1:-15:-1]
    con.close()

    text = ['История игр:', 'Чтобы вернуться в меню, нажмите ESCAPE.', 'ID', 'Итог',
            'Время', 'Открытые ячейки', 'Сложность', 'Никнейм']

    lbl_font = pygame.font.Font(None, 30)
    lbl = lbl_font.render(text[0], True, 'white')
    screen.blit(lbl, (10, 10))

    x_title = 10
    y_title = 40
    title_font = pygame.font.Font(None, 25)
    for t in text[2:]:
        title = title_font.render(t, True, 'white')
        screen.blit(title, (x_title, y_title))
        x_title += title.get_width() + 10

    cell_font = pygame.font.Font(None, 20)
    x_cells = [10, 37, 85, 147, 307, 410, 492]
    y_cell = 60
    for i in range(len(history_data)):
        for j in range(len(history_data[i])):
            cell = cell_font.render(str(history_data[i][j]), True, 'white')
            screen.blit(cell, (x_cells[j], y_cell))
        y_cell += 20

    warn = lbl_font.render(text[1], True, 'white')
    screen.blit(warn, (10, 450))
