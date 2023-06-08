import pygame
from chess_piece import *
from game_board import *
ASPECT_RATIO = 1
INDEX_TO_GRID = ["A","B","C","D","E","F","G","H"]
CYAN = (0, 255, 255)
BLACK_CHESS_IMGS = []
WHITE_CHESS_IMGS = []
PAWN = [1,2,3,4,5,6,7,8]
ROOK = [1,8]
all_pieces = []
QUIT = False


def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variables and load all necessary Packages
    """
    # Preload all Packages
    pygame.init()

    # Declaration of Global Variables
    global WHITE, BLACK, test_piece, board, NEW_BROWN
    WHITE = (255, 255, 255)
    NEW_BROWN = (107, 62, 30)
    BLACK = (0, 0, 0)

    board = GameBoard()

    # Load in-game music
    pygame.mixer.music.load("../../../assets/sfx/bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
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


if __name__ == "__main__":
    init()
    size = (int((800 + 300) * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    pygame.display.set_icon(pygame.image.load("../../../assets/imgs/king_black.png").copy())
    HP = pygame.image.load("../../../assets/imgs/HP.png")
    SWORD = pygame.image.load("../../../assets/imgs/SWORD.png")
    screen = pygame.display.set_mode(size)

# In-game Parameters
selectedPiece = None

while not QUIT:
    # Check for mouseDown Event
    e = pygame.event.wait()
    if e.type == pygame.QUIT:
        exit()
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


        """
        3 Cases:
            1. First selection (identified by -1 values in selectPos)
            2. Deselection (identified by the same position as selectPos)
            3. Final selection (identified by a non-negative selectPos and a negative dropPos)
        """
        for piece in all_pieces:
            if not piece.active:
                continue
            if selectedPiece is None: # Case 1
                if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                    selectedPiece = piece
                    print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                    break
            elif selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum): # Case 2
                selectedPiece = None
                print("Deselected Piece")
                break
            else: # Case 3
                # If the move lands on another piece
                if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                    print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row)\
                          + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                    selectedPiece.move(colNum + 1, rowNum + 1, board, piece)
                    selectedPiece = None
                    break

                # If the move lands on an empty square
                if all_pieces.index(piece) == len(all_pieces) - 1:
                    print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row)\
                          + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                    selectedPiece.move(colNum + 1, rowNum + 1, board)
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
                pygame.draw.rect(screen, WHITE, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            else:
                pygame.draw.rect(screen, BLACK, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))

    for piece in all_pieces:
        piece.render(screen)

    if selectedPiece is not None:
        pygame.draw.rect(screen, CYAN, pygame.Rect((selectedPiece.col - 1) * 100 * ASPECT_RATIO, (selectedPiece.row - 1) * 100 * ASPECT_RATIO,
                                                   100 * ASPECT_RATIO, 100 * ASPECT_RATIO), 5)

    pygame.draw.rect(screen, NEW_BROWN, pygame.Rect(800 * ASPECT_RATIO - 1, 0, screen.get_width() - 800 * ASPECT_RATIO, 800 * ASPECT_RATIO))
    pygame.draw.line(screen, WHITE, (800 * ASPECT_RATIO - 1, 176 * ASPECT_RATIO), (screen.get_width(), 176 * ASPECT_RATIO))
    pygame.draw.line(screen, WHITE, (800 * ASPECT_RATIO - 1, 280 * ASPECT_RATIO), (screen.get_width(), 280 * ASPECT_RATIO))
    pygame.draw.line(screen, WHITE, (800 * ASPECT_RATIO - 1, 420 * ASPECT_RATIO), (screen.get_width(), 420 * ASPECT_RATIO))

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] < 800 * ASPECT_RATIO:
        mouse_col = math.floor(mouse_pos[0] / (100 * ASPECT_RATIO))
        mouse_row = math.floor(mouse_pos[1] / (100 * ASPECT_RATIO))
        located_piece = board.boardState[mouse_col][mouse_row]
        if located_piece is not None:
            # Image rescaling
            rescaled_piece_img = pygame.transform.scale(located_piece.img, (100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            rescaled_HP_img = pygame.transform.scale(HP, (64 * ASPECT_RATIO, 64 * ASPECT_RATIO))
            rescaled_SWORD_img = pygame.transform.scale(SWORD, (64 * ASPECT_RATIO, 64 * ASPECT_RATIO))

            # Text type
            pygame.font.init()
            my_font = pygame.font.SysFont('Calibri', 35)
            my_font_desc = pygame.font.SysFont('Calibri', 12)
            piece_name = my_font.render(located_piece.name, False, (0, 0, 0))
            piece_hp = my_font.render(str(located_piece.hp), False, (0, 0, 0))
            piece_atk = my_font.render(str(located_piece.atk), False, (0, 0, 0))
            piece_desc = my_font_desc.render(located_piece.desc, False, (0, 0, 0))

            # Image display
            center_align = (screen.get_width() + 800 * ASPECT_RATIO) / 2
            screen.blit(rescaled_piece_img, (center_align - rescaled_piece_img.get_width() / 2, 20 * ASPECT_RATIO))  # Piece type
            screen.blit(piece_name, (center_align - piece_name.get_width() / 2, 135 * ASPECT_RATIO))
            screen.blit(piece_hp, (center_align - 50 * ASPECT_RATIO, 210 * ASPECT_RATIO))  # Piece hp stat
            screen.blit(rescaled_HP_img, (center_align - 130 * ASPECT_RATIO, 195 * ASPECT_RATIO))
            screen.blit(piece_atk, (center_align + 100 * ASPECT_RATIO, 210 * ASPECT_RATIO))  # Piece atk stat
            screen.blit(rescaled_SWORD_img, (center_align + 20 * ASPECT_RATIO, 195 * ASPECT_RATIO))
            screen.blit(piece_desc, (655, 440))

    pygame.display.flip()
