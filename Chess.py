import pygame
import time

from ChessPiece import *
from GameBoard import *
from enum import IntEnum
from MainMenu import *

class state(IntEnum):
    menu = 1
    option = 2
    game = 3
    quit = 4

aspect_ratio = 0.8
index_to_grid =["A", "B", "C", "D", "E", "F", "G", "H"]

def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variables and load all necessary Packages
    """
    # Preload all Packages
    pygame.init()

    # Declaration of Global Variables
    global WHITE, BLACK, BROWN, NEW_BROWN, TAN, CHARTREUSE, all_pieces, current_state, turnCounter, board, \
        selected_piece, clock, white_timer, black_timer, game_started
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BROWN = (139, 80, 39)
    NEW_BROWN = (107, 62, 30)
    TAN = (210, 180, 140)
    CHARTREUSE = (127, 255, 0)
    all_pieces = []
    current_state = state.menu
    turnCounter = 0
    board = GameBoard()
    clock = pygame.time.Clock()
    selected_piece = None
    white_timer = 5
    black_timer = 5
    game_started = False

    # Load in-game music
    # pygame.mixer.music.load("assets/sfx/bgm.mp3")
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(-1)
    print("------------------------------------------------------------------------------------")
    print("Input 'p' to pause the music")
    print("Input 'r' to resume the music")

    for i in range(1, 9, 1):
        # Load the white pawns
        temp_piece = ChessPiece(2, i, 0, True)
        all_pieces.append(temp_piece)
        board.addPiece(temp_piece)

        # Load the white backline
        temp_piece = ChessPiece(1, i, i, True)
        all_pieces.append(temp_piece)
        board.addPiece(temp_piece)

        # Load the black pawns
        temp_piece = ChessPiece(7, i, 0, False)
        all_pieces.append(temp_piece)
        board.addPiece(temp_piece)

        # Load the black backline
        temp_piece = ChessPiece(8, i, i, False)
        all_pieces.append(temp_piece)
        board.addPiece(temp_piece)

    pygame.display.set_icon(pygame.image.load("assets/KnightW.png").copy())
    pygame.display.set_caption("Chess+")

if __name__ == "__main__":
    init()
    size = (int((1100) * aspect_ratio), int(800 * aspect_ratio))
    HP = pygame.image.load("assets/HP.png")
    SWORD = pygame.image.load("assets/SWORD.png")
    screen = pygame.display.set_mode(size)


while current_state != state.quit:
    if current_state == state.menu:
        current_state = state(main_menu(screen))
        continue
    elif current_state == state.option:
        current_state = state(options(screen))
        continue

    global new_white_timer
    if game_started:
        clock.tick()
        if turnCounter % 2 == 0:
            white_timer -= float(clock.get_time()) / 1000.0
        if turnCounter % 2 == 1:
            black_timer -= float(clock.get_time()) / 1000.0
        if white_timer < 0:
            current_state = state.quit
            print("black won")
        if black_timer < 0:
            current_state = state.quit
            print("white won")

    # Check for mouseDown Event
    for e in pygame.event.get():
        if e.type == pygame.quit:
            current_state = state.quit
        if e.type == pygame.KEYDOWN:
            # Music Controls
            if e.key == pygame.K_p:
                pygame.mixer.music.pause()
                print('music paused')
            if e.key == pygame.K_r:
                pygame.mixer.music.unpause()
                print('music resumed')

        if pygame.event.event_name(e.type) == "MouseButtonDown":
            # Identify the row and column of our click
            # Get x and get y
            mouseX = e.pos[0]
            mouseY = e.pos[1]
            rowNum = int(mouseY / (100 * aspect_ratio))
            colNum = int(mouseX / (100 * aspect_ratio))
            # print("Row Clicked: " + str(rowNum + 1))
            # print("Column Clicked: " + str(colNum + 1))
            if rowNum not in range(0, 8, 1) or colNum not in range(0, 8, 1):
                continue
            piece = board.boardState[colNum][rowNum]
            """
            3 Cases:
                1. First selection (identified by -1 values in selectPos)
                2. Deselection (identified by the same position as selectPos)
                3. Final selection (identified by a non-negative selectPos and a negative dropPos)
            """
            if piece is not None and piece.active:

                if selected_piece is None: # Case 1
                    if piece.white_piece is (turnCounter % 2 == 0):
                        if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                            selected_piece = piece
                            """print("Selected Piece " + str(index_to_grid[colNum]) + str(rowNum + 1))"""
                elif selected_piece is not None and (selected_piece.col - 1, selected_piece.row - 1) == (colNum, rowNum): # Case 2
                    selected_piece = None
                    """print("Deselected Piece")"""
                else:
                    # If the move lands on another piece
                    if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                        """print("Moved Piece from " + str(index_to_grid[selected_piece.col - 1]) + str(selected_piece.row) \
                              + " to " + str(index_to_grid[colNum]) + str(rowNum + 1))"""
                        if selected_piece.move(colNum + 1, rowNum + 1, board, piece):
                            selected_piece = None
                            turnCounter += 1

            elif piece is None and selected_piece is not None: # Case 3
                # If the move lands on an empty square
                """print("Moved Piece from " + str(index_to_grid[selected_piece.col - 1]) + str(selected_piece.row)\
                      + " to " + str(index_to_grid[colNum]) + str(rowNum + 1))"""
                if selected_piece.move(colNum + 1, rowNum + 1, board):
                    turnCounter += 1

                    if not game_started:
                        clock.tick()
                        game_started = True

                selected_piece = None

    board.Update(all_pieces)

    for i in range(len(all_pieces)):
        if not all_pieces[i].active:
            continue

        # Check for King-checks
        if all_pieces[i].rank == 5 and all_pieces[i].white_piece:
            if board.board_obs[all_pieces[i].col - 1][all_pieces[i].row - 1] % 1 != 0:
                print("White King is Under Check")
        elif all_pieces[i].rank == 5 and not all_pieces[i].white_piece:
            if board.board_obs[all_pieces[i].col - 1][all_pieces[i].row - 1] > 1:
                print("Black King is Under Check")

        # Check if the pawn reaches the promotion condition
        if all_pieces[i].rank == 0 and all_pieces[i].white_piece:
            if all_pieces[i].row == 8:
                all_pieces[i] = ChessPiece(all_pieces[i].row, all_pieces[i].col, 4, True)
        elif all_pieces[i].rank == 0 and not all_pieces[i].white_piece:
            if all_pieces[i].row == 1:
                all_pieces[i] = ChessPiece(all_pieces[i].row, all_pieces[i].col, 4, False)

    # Draw Grid
    for i in range(8): # Start i at 1, reach up to 8, increase i by 1 each loop
        for j in range(8):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                pygame.draw.rect(screen, BROWN, pygame.Rect(j * 100 * aspect_ratio, i * 100 * aspect_ratio,
                                                            100 * aspect_ratio, 100 * aspect_ratio + 1))
            else:
                pygame.draw.rect(screen, TAN, pygame.Rect(j * 100 * aspect_ratio, i * 100 * aspect_ratio,
                        100 * aspect_ratio, 100 * aspect_ratio + 1))

    # Piece Info-chart
    pygame.draw.rect(screen, NEW_BROWN, pygame.Rect(800 * aspect_ratio - 1, 0, screen.get_width() - 800 * aspect_ratio + 5
                                                    , 800 * aspect_ratio))
    pygame.draw.line(screen, WHITE, (800 * aspect_ratio - 1, 250 * aspect_ratio), (screen.get_width(), 250 * aspect_ratio))
    pygame.draw.line(screen, WHITE, (800 * aspect_ratio - 1, 400 * aspect_ratio), (screen.get_width(), 400 * aspect_ratio))
    pygame.draw.line(screen, WHITE, (800 * aspect_ratio - 1, 600 * aspect_ratio), (screen.get_width(), 600 * aspect_ratio))
    font = pygame.font.SysFont("sans", 36)
    new_white_timer = font.render(str(int(white_timer)), False, (0, 0, 0))
    screen.blit(new_white_timer, (800, 600))

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] < 800 * aspect_ratio:
        mouse_col = math.floor(mouse_pos[0] / (100 * aspect_ratio))
        mouse_row = math.floor(mouse_pos[1] / (100 * aspect_ratio))
        located_piece = board.boardState[mouse_col][mouse_row]

        if located_piece is not None and located_piece.active:
            # Image rescaling
            rescaled_piece_img = pygame.transform.scale(located_piece.img, (145 * aspect_ratio, 145 * aspect_ratio))
            rescaled_HP_img = pygame.transform.scale(HP, (92 * aspect_ratio, 92 * aspect_ratio))
            rescaled_SWORD_img = pygame.transform.scale(SWORD, (92 * aspect_ratio, 92 * aspect_ratio))

            # Text type
            pygame.font.init()
            font = pygame.font.SysFont('Calibri', int(50 * aspect_ratio))
            font_desc = pygame.font.SysFont('Calibri', int(29 * aspect_ratio))
            piece_name = font.render(located_piece.name, False, (0, 0, 0))
            piece_hp = font.render(str(int(located_piece.hp)), False, (0, 0, 0))
            piece_atk = font.render(str(int(located_piece.atk)), False, (0, 0, 0))

            # Image display
            center_align = (screen.get_width() + 800 * aspect_ratio) / 2
            screen.blit(rescaled_piece_img, (center_align - rescaled_piece_img.get_width() / 2, 90 * aspect_ratio))  # Piece type
            screen.blit(piece_name, ((screen.get_width() / 2 - piece_name.get_width() / 2) + (400 * aspect_ratio),
                                    (screen.get_height() / 2 - piece_name.get_width() / 2) - (317 * aspect_ratio)))
            screen.blit(piece_hp, (center_align - 30 * aspect_ratio, 300 * aspect_ratio))  # Piece hp stat
            screen.blit(rescaled_HP_img, (center_align - 130 * aspect_ratio, 280 * aspect_ratio))
            screen.blit(piece_atk, (center_align + 100 * aspect_ratio, 300 * aspect_ratio))  # Piece atk stat
            screen.blit(rescaled_SWORD_img, (center_align + 5 * aspect_ratio, 280 * aspect_ratio))

            # Description display
            def desc(text, pos):
                words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
                space = font.size(' ')[0]  # The width of a space.
                max_width, max_height = screen.get_size()
                x, y = pos
                for line in words:
                    for word in line:
                        text = font_desc.render(word, False, (0, 0, 0))
                        word_width, word_height = text.get_size()
                        if x + word_width >= max_width:
                            x = pos[0]  # Reset the x.
                            y += word_height  # Start on new row.
                        screen.blit(text, (x, y))
                        x += word_width + space
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
            desc(located_piece.desc, (800 * aspect_ratio + (7 * aspect_ratio), 800 * aspect_ratio - (185 * aspect_ratio)))

    # Selected Piece Outline
    if selected_piece is not None:
        pygame.draw.rect(screen, CHARTREUSE, pygame.Rect((selected_piece.col - 1) * 100 * aspect_ratio,
                                                         (selected_piece.row - 1) * 100 * aspect_ratio,
                                                         100 * aspect_ratio, 100 * aspect_ratio), 5)

    for piece in all_pieces:
        piece.render(screen)

    pygame.display.flip()
