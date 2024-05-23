from enum import Enum

import chessBoard

class Color(Enum):
    WHITE = "white"
    BLACK = "black"
class possibleMoves:
    def __init__(self, chessBoard):
        self.chessBoard = chessBoard

    
    def possiblePawnMove(self, color):
        if color == Color.WHITE:
            pawnLocations = self.chessBoard.get_whitePawn()
            possibleMoves = (pawnLocations << 8) & self.chessBoard.get_empty()
            
        elif color == Color.BLACK:
            pawnLocations = self.chessBoard.get_blackPawn()
            possibleMoves = (pawnLocations >> 8) & self.chessBoard.get_empty()

        return possibleMoves

    

    def print_possible_moves(self, bitboard):
        print("    a b c d e f g h")
        print("    _______________")
        for rank in range(8):
            row = 8 - rank
            print(row, end=" | ")
            for file in range(8):
                index = rank * 8 + file
                if (bitboard >> (63 - index)) & 1:
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()
        print()



board = chessBoard.chessBoard(
    whitePawn=0x000000000000FF00,
    whiteKnight=0x0000000000000042,
    whiteBishop=0x0000000000000024,
    whiteRook=0x0000000000000081,
    whiteQueen=0x0000000000000008,
    whiteKing=0x0000000000000010,
    blackPawn=0x00FF000000000000,
    blackKnight=0x4200000000000000,
    blackBishop=0x2400000000000000,
    blackRook=0x8100000000000000,
    blackQueen=0x0800000000000000,
    blackKing=0x1000000000000000
)

pawnMoves = possibleMoves(board)

pawnMoves.print_possible_moves(pawnMoves.possiblePawnMove(Color.WHITE))

pawnMoves.print_possible_moves(pawnMoves.possiblePawnMove(Color.BLACK))
    