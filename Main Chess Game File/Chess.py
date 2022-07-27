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
    global all_pieces

    WHITE = (255, 255, 255)
    BROWN = (139, 69, 1)
    TAN = (210, 180, 140)
    CHARTREUSE = (127, 255, 0)
    all_pieces = []

    for i in range(1,9,1):
        #Load all White Pawns
        all_pieces.append(ChessPiece(2, i, 0, True))
        #Load White Backlines
        all_pieces.append(ChessPiece(1, i, i, True))
        # Load Black Pawns
        all_pieces.append(ChessPiece(7, i, 0, False))
        # Load Black Backlines
        all_pieces.append(ChessPiece(8, i, i, False))

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

        for piece in (all_pieces):
            if selectedPiece is None:  # Case 1
                if piece.row - 1 == rowNum and piece.col - 1 == colNum:
                    selectedPiece = piece
                    print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                    break
            elif selectedPiece is not None and (selectedPiece.col - 1, selectedPiece.row - 1) == (colNum, rowNum):  # Case 2
                selectedPiece = None
                print("Deselected Piece ")
                break
            else:  # Case 3
                print("Moved Piece from " + str(INDEX_TO_GRID[selectedPiece.col - 1]) + str(selectedPiece.row - 1) \
                      + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
                selectedPiece.move(colNum + 1, rowNum + 1)
                selectedPiece = None
                break

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

    for piece in (all_pieces):
        piece.render(screen)

    if selectedPiece is not None:
        pygame.draw.rect(screen, CHARTREUSE, pygame.Rect((selectedPiece.col - 1) * 100 * ASPECT_RATIO,
                                                         (selectedPiece.row - 1) * 100 * ASPECT_RATIO,
                                                         100 * ASPECT_RATIO, 100 * ASPECT_RATIO), 4)

    pygame.display.flip()

    pass
