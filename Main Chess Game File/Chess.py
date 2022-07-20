import pygame
import os
from chess_piece import *

ASPECT_RATIO = 0.7
INDEX_TO_GRID = ["A", "B", "C", "D", "E", "F", "G", "H"]

def init():
    """
    This is an initialization Function
    :return: Null
    Establish the paramters / Variable and load all necessary packages
    :param init:
    :return:
    """
    #Preload all pacakges
    pygame.init()

    #Declaration of global variables

    global WHITE
    global BROWN
    global TAN
    global test_piece
    WHITE = (255, 255, 255)
    BROWN = (139,69,1)
    TAN = (210,180,140)

    test_piece = ChessPiece(1, 1, 0, True)

    pygame.display.set_icon(pygame.image.load(os.path.join("assets", "KnightW.png")).copy())
    pygame.display.set_caption("ChessPlus")

#ChessPieces
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
    selectPos = (-1, -1)
    dropPos = (-1, -1)

while True:
    #Check for mouse click event
    e = pygame.event.wait()
    if pygame.event.event_name(e.type) == "MouseButtonDown":
    #Identify the row and column of our click
    #Get x and get y
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

        if (selectPos[0] < 0): # Case 1
            selectPos = (colNum, rowNum)
            print("Selected Piece " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
        elif (selectPos[0] >= 0 and selectPos == (colNum, rowNum)): # Case 2
            selectPos = (-1, -1)
            print("Deselected Piece ")
        else: # Case 3
            dropPos = (colNum, rowNum)
            print("Moved Piece from " + str(INDEX_TO_GRID[selectPos[0]]) + str(selectPos[1] + 1) \
                  + " to " + str(INDEX_TO_GRID[colNum]) + str(rowNum + 1))
            test_piece.move(colNum + 1, rowNum + 1)
            selectPos = (-1, -1)
            dropPos = (-1, -1)

    #Draw board colours

    for i in range(8): #Start at 1, reach up to 8, increase by 1
        for j in range(0,8,1):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                pygame.draw.rect(screen, TAN, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            else:
                pygame.draw.rect(screen, BROWN, pygame.Rect(j * 100 * ASPECT_RATIO, i * 100 * ASPECT_RATIO, 100 * ASPECT_RATIO, 100 * ASPECT_RATIO))

    ##White Pieces
    temp_img = pygame.transform.scale(Pawn_White, (53,53))
    PawnPositions = [(9,430), (79,430), (149,430), (219,430), (289,430), (359,430), (429,430), (499,430)]
    position = ()
    for position in PawnPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Rook_White, (42, 54))
    RookPositions = [(14, 502), (504, 502)]
    position = ()
    for position in RookPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Knight_White, (57, 57))
    KnightPositions = [(75, 500), (425, 500)]
    position = ()
    for position in KnightPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Bishop_White, (55, 55))
    BishopPositions = [(145, 503), (357, 503)]
    position = ()
    for position in BishopPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Queen_White, (55, 55))
    screen.blit(temp_img, (219, 499))

    temp_img = pygame.transform.scale(King_White, (60, 60))
    screen.blit(temp_img, (286, 497))

    ##Black Pieces

    mx = pygame.mouse.get_pos()
    print(mx)

    temp_img = pygame.transform.scale(Pawn_Black, (53, 53))
    PawnPositions = [(8, 80), (78, 80), (148, 80), (218, 80), (288, 80), (358, 80), (428, 80), (500, 80)]
    position = ()
    for position in PawnPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Rook_Black, (35, 55))
    RookPositions = [(17, 12), (507, 12)]
    position = ()
    for position in RookPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Knight_Black, (57, 85))
    KnightPositions = [(75, -5), (425, -5)]
    position = ()
    for position in KnightPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Bishop_Black, (55, 55))
    BishopPositions = [(145, 13), (357, 13)]
    position = ()
    for position in BishopPositions:
        screen.blit(temp_img, position)

    temp_img = pygame.transform.scale(Queen_Black, (55, 55))
    screen.blit(temp_img, (219, 8))

    temp_img = pygame.transform.scale(King_Black, (60, 60))
    screen.blit(temp_img, (286, 6))

    test_piece.render(screen)

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

    pygame.display.flip()

    pass
