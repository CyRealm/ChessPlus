import pygame

ASPECT_RATIO = 0.7

class ChessPiece:
    """
    Stores info regarding a chess piece
    PAWN = 0
    ROOK = 1 and 8
    HORSE = 2 and 7
    BISHOP = 3 and 6
    QUEEN = 4
    KING = 5
    """

    def __init__(self, row, col, rank, white_piece):
        """
        Constructor
        :param row: Integer - row number
        :param col: Integer - col number
        :param rank: Integer - Piece type
        :param white_piece: Boolean - white or black piece
        """
        self.row = row
        self.col = col
        self.rank = rank
        self.white_piece = white_piece

        if self.white_piece:
            addon = "W"
        else:
            addon = "B"

        if rank == 0:
            self.img = pygame.image.load("assets/Pawn" + addon + ".png")
        elif rank == 1 or rank == 8:
            self.img = pygame.image.load("assets/Rook" + addon + ".png")
        elif rank == 2 or rank == 7:
            self.img = pygame.image.load("assets/Knight" + addon + ".png")
        elif rank == 3 or rank == 6:
            self.img = pygame.image.load("assets/Bishop" + addon + ".png")
        elif rank == 4:
            self.img = pygame.image.load("assets/Queen" + addon + ".png")
        elif rank == 5:
            self.img = pygame.image.load("assets/King" + addon + ".png")

    def render(self, surface):
        temp_img = pygame.transform.scale(self.img.copy(), (53, 53))
        surface.blit(temp_img, ((self.col - 1) * 100 * ASPECT_RATIO + 9, (self.row - 1) * 100 * ASPECT_RATIO + 10))

    def move(self, posX, posY):
        """
        Moves the piece to the position pos
        :param posX: integer - column number
        :param posY: integer - row number
        :return: null
        """
        #Check for non-valid movement for each rank
        if self.rank == 0:
            #White First Move
            if self.row == 2 and posY - self.row > 2:
                return
            # Black First Move
            if self.row == 7 and self.row - posY > 2:
                return

            # White Subsequent Moves
            if posY != self.row + 1 and self.white_piece and self.row != 2:
                return
            # Black Subsequent Moves
            if posY != self.row - 1 and self.white_piece == False and self.row != 7:
                return


        self.row = posY
        self.col = posX