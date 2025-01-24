import pygame


from startPage import start_page, start_screen


class Difficult:
    EASE = 0
    NORMAL = 1
    HARD = 2


class AppStatus:
    START = 0
    GAME = 1
    END = 2


FPS = 50
difficult = Difficult.EASE
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
            if difficult := start_page(screen, btns):
                status = AppStatus.GAME

        elif status == AppStatus.GAME:
            print(f"Играем. Сложность: {difficult}")

        pygame.display.flip()
        clock.tick(FPS)

