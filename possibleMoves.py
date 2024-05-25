from enum import Enum
from chessBoard import ChessBoard

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class possibleMoves:
    def __init__(self, chessBoard):
        self.chessBoard = chessBoard

    def possiblePawnMove(self, color):
        if color == Color.WHITE:
            pawnLocations = self.chessBoard.get_piece("pawns") & self.chessBoard._white_pieces
            possiblePushes = (pawnLocations << 8) & self.chessBoard.get_empty()
            possibleCaptures = ((pawnLocations << 7) & self.chessBoard._black_pieces) | (pawnLocations << 9) & self.chessBoard._black_pieces
        elif color == Color.BLACK:
            pawnLocations = self.chessBoard.get_piece("pawns") & self.chessBoard._black_pieces
            possiblePushes = (pawnLocations >> 8) & self.chessBoard.get_empty()
            possibleCaptures = (((pawnLocations >> 7)) & self.chessBoard._white_pieces) | (pawnLocations << 9) & self.chessBoard._white_pieces
        return possiblePushes | possibleCaptures 

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

# Example usage
board = ChessBoard(
    pawns=0x00FF800000007F00,
    knights=0x4200000000000042,
    bishops=0x2400000000000024,
    rooks=0x8100000000000081,
    queens=0x0800000000000008,
    kings=0x1000000000000010,
    white_pieces=0x0000800000007FFF,
    black_pieces=0xFFFF000000000000
)


pawnMoves = possibleMoves(board)

print("All Pawn Bitboard")
board.print_bitboard(board.get_piece("pawns"))

board.print_bitboard(board.get_empty())

board.print_bitboard(board._white_pieces)

pawnMoves.print_possible_moves(pawnMoves.possiblePawnMove(Color.WHITE))
print("printed the white pieces")
pawnMoves.print_possible_moves(pawnMoves.possiblePawnMove(Color.BLACK))
