import os
from Chess_piece import *

ASPECT_RATIO = 0.7
INDEX_TO_GRID = ["A", "B", "C", "D", "E", "F", "G", "H"]


def init():
    """
    This is an initialization Function
    :return: Null
    Establish the parameters / Variable and load all necessary packages
    :return:
    """
    # Preload all packages
    pygame.init()

    # Declaration of global variables

    global WHITE
    global BROWN
    global TAN
    global CHARTREUSE
    global PawnW1, PawnW2, PawnW3, PawnW4, PawnW5, PawnW6, PawnW7, PawnW8, RookW1, RookW2, KnightW1, \
        KnightW2, BishopW1, BishopW2, QueenW, KingW, PawnB1, PawnB2, PawnB3, PawnB4, PawnB5, PawnB6, \
        PawnB7, PawnB8, RookB1, RookB2, KnightB1, KnightB2, BishopB1, BishopB2, QueenB, KingB

    WHITE = (255, 255, 255)
    BROWN = (139, 69, 1)
    TAN = (210, 180, 140)
    CHARTREUSE = (127, 255, 0)

    PawnW1 = ChessPiece(2, 1, 0, True)
    PawnW2 = ChessPiece(2, 2, 0, True)
    PawnW3 = ChessPiece(2, 3, 0, True)
    PawnW4 = ChessPiece(2, 4, 0, True)
    PawnW5 = ChessPiece(2, 5, 0, True)
    PawnW6 = ChessPiece(2, 6, 0, True)
    PawnW7 = ChessPiece(2, 7, 0, True)
    PawnW8 = ChessPiece(2, 8, 0, True)
    RookW1 = ChessPiece(1, 1, 1, True)
    RookW2 = ChessPiece(1, 8, 1, True)
    KnightW1 = ChessPiece(1, 2, 2, True)
    KnightW2 = ChessPiece(1, 7, 2, True)
    BishopW1 = ChessPiece(1, 3, 3, True)
    BishopW2 = ChessPiece(1, 6, 3, True)
    QueenW = ChessPiece(1, 5, 4, True)
    KingW = ChessPiece(1, 4, 5, True)
    PawnB1 = ChessPiece(7, 1, 0, False)
    PawnB2 = ChessPiece(7, 2, 0, False)
    PawnB3 = ChessPiece(7, 3, 0, False)
    PawnB4 = ChessPiece(7, 4, 0, False)
    PawnB5 = ChessPiece(7, 5, 0, False)
    PawnB6 = ChessPiece(7, 6, 0, False)
    PawnB7 = ChessPiece(7, 7, 0, False)
    PawnB8 = ChessPiece(7, 8, 0, False)
    RookB1 = ChessPiece(8, 1, 1, False)
    RookB2 = ChessPiece(8, 8, 1, False)
    KnightB1 = ChessPiece(8, 2, 2, False)
    KnightB2 = ChessPiece(8, 7, 2, False)
    BishopB1 = ChessPiece(8, 3, 3, False)
    BishopB2 = ChessPiece(8, 6, 3, False)
    QueenB = ChessPiece(8, 5, 4, False)
    KingB = ChessPiece(8, 4, 5, False)

    pygame.display.set_icon(pygame.image.load(os.path.join("assets", "KnightW.png")).copy())
    pygame.display.set_caption("ChessPlus")


# ChessPieces
Pawn_White = pygame.image.load(os.path.join("assets", "PawnW.png"))
Rook_White = pygame.image.load(os.path.join("assets", "RookW.png"))
Knight_White = pygame.image.load(os.path.join("assets", "KnightW.png"))
Bishop_White = pygame.image.load(os.path.join("assets", "BishopW.png"))
King_White = pygame.image.load(os.path.join("assets", "KingW.png"))
Queen_White = pygame.image.load(os.path.join("assets", "QueenW.png"))

Pawn_Black = pygame.image.load(os.path.join("assets", "PawnB.png"))
Rook_Black = pygame.image.load(os.path.join("assets", "RookB.png"))
Knight_Black = pygame.image.load(os.path.join("assets", "KnightB.png"))
Bishop_Black = pygame.image.load(os.path.join("assets", "BishopB.png"))
King_Black = pygame.image.load(os.path.join("assets", "KingB.png"))
Queen_Black = pygame.image.load(os.path.join("assets", "QueenB.png"))

if __name__ == "__main__":
    init()
    size = (int(800 * ASPECT_RATIO), int(800 * ASPECT_RATIO))
    screen = pygame.display.set_mode(size)

    # In-game parameters
    global selectedPiece
    selectedPiece = None

while True:
    # Check for mouse click event
    e = pygame.event.wait()
    if pygame.event.event_name(e.type) == "MouseButtonDown":
        # Identify the row and column of our click
        # Get x and get y
        mouseX = e.pos[0]
        mouseY = e.pos[1]
        rowNum = int(mouseY / (100 * ASPECT_RATIO))
        colNum = int(mouseX / (100 * ASPECT_RATIO))
        # print("Row clicked: " + str(rowNum + 1))
        # print("Column clicked: " + str(colNum + 1))

        """
        3 cases: 
            1. First selection (Identified by -1 values by selectPos)
            2. Deselection (Identified by the same position as in the selectPos)
            3. Final selection (Identified by a non-negative selectPos and negativePos)
        """

        if selectedPiece is None:  # Case 1
            if PawnW1.row - 1 == rowNum and PawnW1.col - 1 == colNum:
                selectedPiece = PawnW1
                print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
        elif selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum):  # Case 2
            selectedPiece = None
            print("Deselected Piece ")
        else:  # Case 3
            print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col]) + str(selectedPiece.row + 1) \
                  + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
            selectedPiece.move(colNum + 1, rowNum + 1)
            selectedPiece = None

    # Draw board colours

    for i in range(8):  # Start at 1, reach up to 8, increase by 1
        for j in range(0, 8, 1):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                pygame.draw.rect(screen, TAN,
                                 pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO,
                                             100 * ASPECT_RATIO))
            else:
                pygame.draw.rect(screen, BROWN,
                                 pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO,
                                             100 * ASPECT_RATIO))

    PawnW1.render(screen)
    PawnW2.render(screen)
    PawnW3.render(screen)
    PawnW4.render(screen)
    PawnW5.render(screen)
    PawnW6.render(screen)
    PawnW7.render(screen)
    PawnW8.render(screen)
    RookW1.render(screen)
    RookW2.render(screen)
    KnightW1.render(screen)
    KnightW2.render(screen)
    BishopW1.render(screen)
    BishopW2.render(screen)
    QueenW.render(screen)
    KingW.render(screen)
    PawnB1.render(screen)
    PawnB2.render(screen)
    PawnB3.render(screen)
    PawnB4.render(screen)
    PawnB5.render(screen)
    PawnB6.render(screen)
    PawnB7.render(screen)
    PawnB8.render(screen)
    RookB1.render(screen)
    RookB2.render(screen)
    KnightB1.render(screen)
    KnightB2.render(screen)
    BishopB1.render(screen)
    BishopB2.render(screen)
    QueenB.render(screen)
    KingB.render(screen)


    def init(self, row, col, rank, white_piece):

        if rank == 0:
            self.img(pygame.image.load(os.path.join("assets", "PawnW.png")))
        elif rank == 1:
            self.img(pygame.image.load(os.path.join("assets", "KnightW.png")))
        elif rank == 2:
            self.img(pygame.image.load(os.path.join("assets", "BishopW.png")))
        elif rank == 3:
            self.img(pygame.image.load(os.path.join("assets", "RookW.png")))
        elif rank == 4:
            self.img(pygame.image.load(os.path.join("assets", "QueenW.png")))
        elif rank == 5:
            self.img(pygame.image.load(os.path.join("assets", "KingW.png")))


    if selectedPiece is not None:
        pygame.draw.rect(screen, CHARTREUSE, pygame.Rect((selectedPiece.col - 1) * 100 * ASPECT_RATIO,
                                                         (selectedPiece.row - 1) * 100 * ASPECT_RATIO,
                                                         100 * ASPECT_RATIO, 100 * ASPECT_RATIO), 4)

    pygame.display.flip()

    pass
