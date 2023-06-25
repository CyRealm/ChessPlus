import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        self.image = image
        self.posX = pos[0]
        self.posY = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.posX, self.posY))
        self.text_rect = self.text.get_rect(center=(self.posX, self.posY))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)

#Options
def options(screen):
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    screen.fill("white")
    font = pygame.font.SysFont('Calibri', 45)
    options_text = font.render("This is the OPTIONS screen", True, "Black")
    screen.blit(options_text, (0,0))

    options_back = Button(image = None, pos = (640, 460), text_input = "BACK",
                          font = pygame.font.SysFont('Calibri', 35), base_colour = "Black", hovering_colour = "Green")

    options_back.changeColor(OPTIONS_MOUSE_POS)
    options_back.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 4
        if event.type == pygame.MOUSEBUTTONDOWN:
            if options_back.checkForInput(OPTIONS_MOUSE_POS):
                return 1

    pygame.display.update()
    return 2

#Main Menu
def main_menu(screen):
    menu_mouse_pos = pygame.mouse.get_pos()
    pygame.font.init()
    font = pygame.font.SysFont('Calibri', 65)
    menu_text = font.render("CHESS+", True, (0, 0, 0))
    screen.blit(menu_text, (0,0))

    play_button = Button(image = pygame.image.load("assets/ogImgs/Play.png"), pos = (200, 0), text_input ="PLAY",
                         font = pygame.font.SysFont('Calibri', 35), base_colour = "#d7fcd4", hovering_colour = "White")
    options_button = Button(image = pygame.image.load("assets/ogImgs/Options.png"), pos = (200, 410), text_input="OPTIONS",
                            font = pygame.font.SysFont('Calibri', 35), base_colour = "#d7fcd4", hovering_colour = "White")
    quit_button = Button(image = pygame.image.load("assets/ogImgs/Quit.png"), pos = (200, 800), text_input="QUIT",
                         font = pygame.font.SysFont('Calibri', 35), base_colour = "#d7fcd4", hovering_colour = "White")

    for button in [play_button, options_button, quit_button]:
        button.changeColor(menu_mouse_pos)
        button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 4
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.checkForInput(menu_mouse_pos):
                return 3
            if options_button.checkForInput(menu_mouse_pos):
                return 2
            if quit_button.checkForInput(menu_mouse_pos):
                return 4

    pygame.display.flip()
    return 1