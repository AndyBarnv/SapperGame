import pygame


from start_page import start_page_update, start_screen
from draw_mechanics import game_page_create, game_update, Game
from game_mechanics import Difficulties as Difficult


class AppStatus:
    START = 0
    GAME = 1
    END = 2


FPS = 60
difficult = Difficult.EASY
status = AppStatus.START


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Sapper")
    # размеры окна:
    size = WIDTH, HEIGHT = 501, 501
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    btns = start_screen(screen, *size)
    while True:
        if status == AppStatus.START:
            if difficult := start_page_update(screen, btns, size):
                status = AppStatus.GAME
                game = game_page_create(difficult)
                print(f"Играем. Сложность: {difficult}")

        elif status == AppStatus.GAME:
            game = game_update(game)
            game: Game
        clock.tick(FPS)
        pygame.display.flip()

