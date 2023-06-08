import math

import pygame
from game_board import *
ASPECT_RATIO = 1

class ChessPiece:
    """
    Stores info regarding a chess piece
    PAWN = 0
    ROOK = 1
    HORSE = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    BISHOP = 6
    HORSE = 7
    ROOK = 8
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
        self.movementVector = [0,0]
        self.active = True
        self.firstMove = True

        if self.white_piece:
            addon = "white"
        else:
            addon = "black"

        if rank == 0:
            self.img = pygame.image.load("assets/imgs/pawn_" + addon + ".png")
            self.hp = 2
            self.atk = 1
            self.name = "Pawn"
            self.desc = "Temporary Promotion: Temporarily promote to another piece until the end of the turn"
        elif rank == 1 or rank == 8:
            self.img = pygame.image.load("assets/imgs/rook_" + addon + ".png")
            self.hp = 5
            self.atk = 2
            self.name = "Rook"
            self.desc = "Indomitability: Gain invincibility at the end of the turn which lasts until the start of the player's next turn"
        elif rank == 2 or rank == 7:
            self.img = pygame.image.load("assets/imgs/knight_" + addon + ".png")
            self.hp = 3
            self.atk = 2
            self.name = "Knight"
            self.desc = "Heroic Charge: Gain the ability to move twice; double damage if an attack is launched on the second move"
        elif rank == 3 or rank == 6:
            self.img = pygame.image.load("assets/imgs/bishop_" + addon + ".png")
            self.hp = 3
            self.atk = 2
            self.name = "Bishop"
            self.desc = "Healing Prayer: Heal any unit by hp equal to the Bishop's attack value"
        elif rank == 4:
            self.img = pygame.image.load("assets/imgs/queen_" + addon + ".png")
            self.hp = 6
            self.atk = 3
            self.name = "Queen"
            self.desc = "Charismatic Aura: Buffs all visible ally units within range of Queen's observation, by double hp and double attack, for 2 turns"
        elif rank == 5:
            self.img = pygame.image.load("assets/imgs/king_" + addon + ".png")
            self.hp = 9
            self.atk = 1
            self.name = "King"
            self.desc = "Tactical Exchange: Permits positional swap with any single ally unit"

    def render(self, surface):
        if self.active:
            temp_img = pygame.transform.scale(self.img.copy(), (100 * ASPECT_RATIO, 100 * ASPECT_RATIO))
            surface.blit(temp_img, ((self.col - 1) * 100, (self.row - 1) * 100))

    def move(self, posX, posY, gameB, taking_piece = None):
        """
        Moves the piece to the position pos
        :param posX: integer - column number
        :param posY: integer - row number
        :return: null
        """

        # Check for non-valid movement for each rank
        if self.rank == 0:
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []

            # Regardless of White or Black, move piece only in the same column
            if self.col != posX:
                # UNLESS IT'S TO TAKE A PIECE
                if (posY == self.row + 1 and self.white_piece and abs(col_diff) == 1 and taking_piece is not None) or \
                        (posY == self.row - 1 and not self.white_piece and abs(col_diff) == 1 and taking_piece is not None):
                    if taking_piece.white_piece != self.white_piece:
                        taking_piece.hp -= self.atk
                        if taking_piece.hp <= 0:
                            taking_piece.active = False
                    else:
                        return
                else:
                    return
            else:
                # White First move
                if self.firstMove and abs(posY - self.row) > 2:
                    return

                # White Subsequent moves
                if posY != self.row + 1 and self.white_piece and self.row != 2:
                    return
                # Black Subsequent moves
                if posY != self.row - 1 and not self.white_piece and self.row != 7:
                    return

                for tempR in range(0, row_diff, int(row_diff/abs(row_diff))):
                    pathState.append(gameB.boardState[posX - 1][posY - 1 + tempR])

                # Check for Road Blocks
                if pathState.count(None) != len(pathState):
                    return


        if self.rank == 1 or self.rank == 8:
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            # At least one of the row or column has to match the original
            if self.row != posY and self.col != posX:
                return

            for j in range(0, col_diff if col_diff != 0 else 1, 1 if col_diff >= 0 else -1):
                for i in range(0, row_diff if row_diff != 0 else 1, 1 if row_diff >= 0 else -1):
                    pathState.append(gameB.boardState[posX - 1 + j][posY - 1 + i])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                return

            if taking_piece is not None:
                if taking_piece.white_piece != self.white_piece:
                    taking_piece.hp -= self.atk
                    if taking_piece.hp <= 0:
                        taking_piece.active = False

        if self.rank == 2 or self.rank == 7:
            # Hypoteneuse ^ 2 is 5
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            if row_diff ** 2 + col_diff ** 2 != 5:
                return

            pathState.append(gameB.boardState[posX - 1][posY - 1])

            if pathState.count(None) != len(pathState) and taking_piece is not None:
                if taking_piece.white_piece != self.white_piece:
                    taking_piece.hp -= self.atk
                    if taking_piece.hp <= 0:
                        taking_piece.active = False
                else:
                    return

        if self.rank == 3 or self.rank == 6:
            # row_diff and col_diff has to be the same
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []

            if abs(row_diff) != abs(col_diff):
                return

            row_pathing = int(row_diff / abs(row_diff))
            col_pathing = int(col_diff / abs(col_diff))

            for i in range(0, abs(col_diff), 1):
                pathState.append(gameB.boardState[posX - 1 + col_pathing * i][posY - 1 + row_pathing * i])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                # 1 possibility - getting blocked
                return

            if taking_piece is not None:
                if taking_piece.white_piece != self.white_piece:
                    taking_piece.hp -= self.atk
                    if taking_piece.hp <= 0:
                        taking_piece.active = False

        if self.rank == 4:
            # row_diff and col_diff has to be the same or only one gets changed
            row_diff = self.row - posY
            col_diff = self.col - posX
            pathState = []
            if abs(row_diff) != abs(col_diff) and (row_diff != 0 and col_diff != 0):
                return

            theta = math.atan2(-row_diff, col_diff)
            rad = int(math.sqrt(row_diff**2 + col_diff**2))

            for r in range(0, rad):
                row = round(math.sin(theta) * r)
                col = round(math.cos(theta) * r)
                pathState.append(gameB.boardState[posX - 1 + col][posY - 1 - row])

            pathState.pop(0)

            if pathState.count(None) != len(pathState):
                return

            if taking_piece is not None:
                if taking_piece.white_piece != self.white_piece:
                    taking_piece.hp -= self.atk
                    if taking_piece.hp <= 0:
                        taking_piece.active = False


        if self.rank == 5:
            # only 1 square move
            row_diff = self.row - posY
            col_diff = self.col - posX
            if row_diff ** 2 + col_diff ** 2 > 2:
                return

            if taking_piece is not None:
                if taking_piece.white_piece == self.white_piece:
                    return
                else:
                    taking_piece.hp -= self.atk
                    if taking_piece.hp <= 0:
                        taking_piece.active = False

        self.firstMove = False
        if taking_piece is None or taking_piece.active is False:
            gameB.boardState[self.col - 1][self.row - 1] = None
            self.row = posY
            self.col = posX
            gameB.boardState[self.col - 1][self.row - 1] = self
