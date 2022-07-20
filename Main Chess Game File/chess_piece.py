import pygame

ASPECT_RATIO = 0.7

class ChessPiece:
    """
    Stores info regarding a chess piece
    PAWN = 0
    ROOK = 1
    HORSE = 2
    BISHOP = 3
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
        elif rank == 1:
            self.img = pygame.image.load("assets/imgs/rook_" + addon + ".png")
        elif rank == 2:
            self.img = pygame.image.load("assets/imgs/horse_" + addon + ".png")
        elif rank == 3:
            self.img = pygame.image.load("assets/imgs/bishop_" + addon + ".png")
        elif rank == 4:
            self.img = pygame.image.load("assets/imgs/queen_" + addon + ".png")
        elif rank == 5:
            self.img = pygame.image.load("assets/imgs/king_" + addon + ".png")

    def render(self, surface):
        temp_img = pygame.transform.scale(self.img.copy(), (int(100 * ASPECT_RATIO), int(100 * ASPECT_RATIO)))
        surface.blit(temp_img, ((self.col - 1) * 100 * ASPECT_RATIO, (self.row - 1) * 100 * ASPECT_RATIO))

    def move(self, posX, posY):
        """
        Moves the piece to the position pos
        :param posX: integer - column number
        :param posY: integer - row number
        :return: null
        """
        self.row = posY
        self.col = posX