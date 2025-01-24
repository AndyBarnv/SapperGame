import pygame
import os
import sys


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
                  "Туда сюда,",
                  "Здесь и туда"]

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

    for btn in btns[1:]:
        btn.draw()

    return btns


def start_page(screen, btns):
    """
    Функция, которая обрабатывает события на окне старта.
    :param screen:
    :param btns:
    :return:
    """

    difficult = None
    for btn in btns:
        if btn.is_pressed:
            difficult = btn.text

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event = event.dict
            if event["button"] == 1:  # Если нажата левая кнопка мыши
                for btn in btns:
                    if btn.text == "START" and btn.rect.collidepoint(event["pos"]):
                        return difficult

                    if btn.rect.collidepoint(event["pos"]):
                        btn.is_pressed = True
                        difficult = btn.text
                        btn.draw(is_hovered=True)
                    else:
                        btn.is_pressed = False
                        btn.draw()
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            return difficult  # начинаем игру
