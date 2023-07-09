import pygame
import time
from chess_piece import *
from game_board import *
from enum import IntEnum
from MainMenu import *

ASPECT_RATIO = 1
INDEX_TO_GRID = ["A","B","C","D","E","F","G","H"]
CYAN = (0, 255, 255)
TAN = (210, 180, 140)
NEW_BROWN = (107, 62, 30)
BROWN = (139, 80, 39)
BLACK = (0, 0, 0)
all_pieces = []
white_timer = 60.0
black_timer = 60.0
game_started = False

class STATE(IntEnum):
    MENU = 1
    OPTION = 2
    STRATEGY = 3
    GAME = 4
    QUIT = 5


def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variables and load all necessary Packages
    """
    # Preload all Packages
    pygame.init()

    # Declaration of Global Variables
    global WHITE, BLACK, test_piece, board, NEW_BROWN, turnCounter, currentState, globalClock
    global white_timer, black_timer

    WHITE = (255, 255, 255)
    NEW_BROWN = (107, 62, 30)
    BLACK = (0, 0, 0)

    globalClock = pygame.time.Clock()
    currentState = STATE.MENU
    turnCounter = 0
    board = GameBoard()

    white_timer = 600
    black_timer = 600

    # Load in-game music
    # pygame.mixer.music.load("assets/sfx/bgm.mp3")
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.play(-1)
    print("------------------------------------------------------------------------------------")
    print("Input 'p' to pause the music")
    print("Input 'r' to resume the music")

    for i in range(1, 9, 1):
        # Load the white pawns
        tempPiece = ChessPiece(2, i, 0, True)
        all_pieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the white backline
        tempPiece = ChessPiece(1, i, i, True)
        all_pieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the black pawns
        tempPiece = ChessPiece(7, i, 0, False)
        all_pieces.append(tempPiece)
        board.addPiece(tempPiece)

        # Load the black backline
        tempPiece = ChessPiece(8, i, i, False)
        all_pieces.append(tempPiece)
        board.addPiece(tempPiece)

# Description display
def desc(text, pos):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font_stats.size(' ')[0]  # The width of a space.
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
        y += word_height  # Start on new row

if __name__ == "__main__":
    init()
    size = (int((800 + 300) * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    pygame.display.set_icon(pygame.image.load("assets/ogImgs/king_black.png").copy())
    HP = pygame.image.load("assets/ogImgs/HP.png")
    SWORD = pygame.image.load("assets/ogImgs/SWORD.png")
    INCREASE = pygame.image.load("assets/imgs/increase.png")
    screen = pygame.display.set_mode(size)
    center_align = (screen.get_width() + 800 * ASPECT_RATIO) / 2
    increaseRect = pygame.rect.Rect(center_align - 130 * ASPECT_RATIO, 310 * ASPECT_RATIO, INCREASE.get_width(), INCREASE.get_height())

# In-game Parameters
selectedPiece = None

while currentState != STATE.QUIT:
    if currentState == STATE.MENU:
        currentState = STATE(main_menu(screen))
        continue
    elif currentState == STATE.OPTION:
        currentState = STATE(options(screen))
        continue

    # Check for mouseDown Event
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            currentState = STATE.QUIT
        if e.type == pygame.KEYDOWN:
            for line in board.board_obs:
                print(line)
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
            rowNum = int(mouseY / (100 * ASPECT_RATIO))
            colNum = int(mouseX / (100 * ASPECT_RATIO))
            # print("Row Clicked: " + str(rowNum + 1))
            # print("Column Clicked: " + str(colNum + 1))
            if rowNum not in range(0, 8, 1) or colNum not in range(0, 8, 1):
                piece = None
            else:
                piece = board.boardState[colNum][rowNum]
            """
            3 Cases:
                1. First selection (identified by -1 values in selectPos)
                2. Deselection (identified by the same position as selectPos)
                3. Final selection (identified by a non-negative selectPos and a negative dropPos)
            """
            if currentState == STATE.STRATEGY:
                if piece is not None:
                    if selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum): # Case 2
                        selectedPiece = None
                    else:
                        selectedPiece = piece

                if selectedPiece is not None:
                    if increaseRect.collidepoint(mouseX, mouseY):
                        selectedPiece.adjustAtk(1)


            elif currentState == STATE.GAME:
                if piece is not None and piece.active:

                    if selectedPiece is None: # Case 1
                        if piece.white_piece is (turnCounter % 2 == 0):
                            if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                                selectedPiece = piece
                    elif selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum): # Case 2
                        selectedPiece = None
                    else:
                        # If the move lands on another piece
                        if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                            # print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row) \
                            #       + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                            if selectedPiece.move(colNum + 1, rowNum + 1, board, piece):
                                selectedPiece = None
                                turnCounter += 1

                elif piece is None and selectedPiece is not None: # Case 3
                    # If the move lands on an empty square
                    print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row)\
                          + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                    if selectedPiece.move(colNum + 1, rowNum + 1, board):
                        turnCounter += 1
                        if not game_started:
                            globalClock.tick()
                            game_started = True

                    selectedPiece = None



    board.Update(all_pieces)

    for i in range(len(all_pieces)):
        if not all_pieces[i].active:
            continue
        # Check for King-Checks
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
                pygame.draw.rect(screen, BROWN, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            else:
                pygame.draw.rect(screen, TAN, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))

    for piece in all_pieces:
        piece.render(screen)

    if selectedPiece is not None:
        pygame.draw.rect(screen, CYAN, pygame.Rect((selectedPiece.col - 1) * 100 * ASPECT_RATIO, (selectedPiece.row - 1) * 100 * ASPECT_RATIO,
                                                   100 * ASPECT_RATIO, 100 * ASPECT_RATIO), 5)

    # Piece Info-chart
    pygame.draw.rect(screen, NEW_BROWN,
                     pygame.Rect(799 * ASPECT_RATIO, 0, math.ceil(302 * ASPECT_RATIO), 800 * ASPECT_RATIO))
    pygame.draw.rect(screen, WHITE,
                     pygame.Rect(799 * ASPECT_RATIO, 700 * ASPECT_RATIO, 151 * ASPECT_RATIO, 102 * ASPECT_RATIO))
    pygame.draw.rect(screen, BLACK, pygame.Rect(math.ceil(948 * ASPECT_RATIO), 700 * ASPECT_RATIO, 153 * ASPECT_RATIO,
                                                math.ceil(101 * ASPECT_RATIO)))
    pygame.draw.line(screen, WHITE, (799 * ASPECT_RATIO, 250 * ASPECT_RATIO), (screen.get_width(), 250 * ASPECT_RATIO))
    pygame.draw.line(screen, WHITE, (799 * ASPECT_RATIO, 400 * ASPECT_RATIO), (screen.get_width(), 400 * ASPECT_RATIO))

    mouse_pos = pygame.mouse.get_pos()
    mouse_col = math.floor(mouse_pos[0] / (100 * ASPECT_RATIO))
    mouse_row = math.floor(mouse_pos[1] / (100 * ASPECT_RATIO))
    try:
        located_piece = board.boardState[mouse_col][mouse_row]
    except:
        located_piece = None

    if selectedPiece is not None:
        located_piece = selectedPiece

    if located_piece is not None and located_piece.active:
        # Image rescaling
        rescaled_piece_img = pygame.transform.scale(located_piece.img, (145 * ASPECT_RATIO, 145 * ASPECT_RATIO))
        rescaled_HP_img = pygame.transform.scale(HP, (92 * ASPECT_RATIO, 92 * ASPECT_RATIO))
        rescaled_SWORD_img = pygame.transform.scale(SWORD, (92 * ASPECT_RATIO, 92 * ASPECT_RATIO))

        # Text type
        pygame.font.init()
        font_stats = pygame.font.SysFont('Calibri', int(50 * ASPECT_RATIO))
        font_desc = pygame.font.SysFont('Calibri', int(26 * ASPECT_RATIO))
        piece_name = font_stats.render(located_piece.name, False, (0, 0, 0))
        piece_hp = font_stats.render(str(int(located_piece.hp)), False, (0, 0, 0))
        piece_atk = font_stats.render(str(int(located_piece.atk)), False, (0, 0, 0))

        # Image display
        center_align = (screen.get_width() + 800 * ASPECT_RATIO) / 2
        screen.blit(rescaled_piece_img,
                    (center_align - rescaled_piece_img.get_width() / 2, 90 * ASPECT_RATIO))  # Piece type
        screen.blit(piece_name, ((screen.get_width() / 2 - piece_name.get_width() / 2) + (400 * ASPECT_RATIO),
                                 (screen.get_height() / 2 - piece_name.get_width() / 2) - (317 * ASPECT_RATIO)))
        screen.blit(piece_hp, (center_align - 30 * ASPECT_RATIO, 300 * ASPECT_RATIO))  # Piece hp stat
        screen.blit(rescaled_HP_img, (center_align - 130 * ASPECT_RATIO, 280 * ASPECT_RATIO))
        screen.blit(piece_atk, (center_align + 100 * ASPECT_RATIO, 300 * ASPECT_RATIO))  # Piece atk stat
        screen.blit(rescaled_SWORD_img, (center_align + 5 * ASPECT_RATIO, 280 * ASPECT_RATIO))

        desc(located_piece.desc, (800 * ASPECT_RATIO + (7 * ASPECT_RATIO), 800 * ASPECT_RATIO - (235 * ASPECT_RATIO)))

        if located_piece == selectedPiece:
            screen.blit(INCREASE, (center_align - 130 * ASPECT_RATIO, 310 * ASPECT_RATIO))

    # Timer
    font_win = pygame.font.SysFont('Calibri', int(100 * ASPECT_RATIO))
    white_win = font_win.render("WHITE WON", False, (255, 255, 255))
    black_win = font_win.render("BLACK WON", False, (0, 0, 0))
    font_time = pygame.font.SysFont("sans", int(48 * ASPECT_RATIO))

    new_white_timer = font_time.render(str(time.strftime("%M:%S", time.gmtime(white_timer))), False, (0, 0, 0))
    screen.blit(new_white_timer,
                (screen.get_width() / 2 - new_white_timer.get_width() / 2 + (325 * ASPECT_RATIO), 724 * ASPECT_RATIO))
    new_black_timer = font_time.render(str(time.strftime("%M:%S", time.gmtime(black_timer))), False, (255, 255, 255))
    screen.blit(new_black_timer,
                (screen.get_width() / 2 - new_black_timer.get_width() / 2 + (475 * ASPECT_RATIO), 724 * ASPECT_RATIO))

    if game_started:
        globalClock.tick()
        if turnCounter % 2 == 0:
            white_timer -= float(globalClock.get_time()) / 1000.0
        if turnCounter % 2 == 1:
            black_timer -= float(globalClock.get_time()) / 1000.0
        if white_timer < 0:  # Black wins due to time
            screen.blit(black_win, (400 * ASPECT_RATIO - white_win.get_width() / 2, screen.get_height() / 2 -
                                    white_win.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(5000)
            current_state = STATE.QUIT
        if black_timer < 0:  # White wins due to time
            screen.blit(white_win, ((400 * ASPECT_RATIO - white_win.get_width() / 2, screen.get_height() / 2 -
                                     white_win.get_height() / 2)))
            pygame.display.flip()
            pygame.time.wait(5000)
            current_state = STATE.QUIT

    pygame.display.flip()
