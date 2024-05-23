class chessBoard:
    def __init__(self, whitePawn, whiteKnight, whiteBishop, whiteRook, whiteQueen, whiteKing,
                 blackPawn, blackKnight, blackBishop, blackRook, blackQueen, blackKing):
        self._whitePawn = whitePawn
        self._whiteKnight = whiteKnight
        self._whiteBishop = whiteBishop
        self._whiteRook = whiteRook
        self._whiteQueen = whiteQueen
        self._whiteKing = whiteKing
        self._blackPawn = blackPawn
        self._blackKnight = blackKnight
        self._blackBishop = blackBishop
        self._blackRook = blackRook
        self._blackQueen = blackQueen
        self._blackKing = blackKing
        self._update_empty()

    def _update_empty(self):
        all_pieces = (self._whitePawn | self._whiteKnight | self._whiteBishop | self._whiteRook | self._whiteQueen | self._whiteKing |
                      self._blackPawn | self._blackKnight | self._blackBishop | self._blackRook | self._blackQueen | self._blackKing)
        self._empty = ~all_pieces & 0xFFFFFFFFFFFFFFFF

    def get_whitePawn(self):
        return self._whitePawn

    def set_whitePawn(self, value):
        self._whitePawn = value
        self._update_empty()

    def get_whiteKnight(self):
        return self._whiteKnight

    def set_whiteKnight(self, value):
        self._whiteKnight = value
        self._update_empty()

    def get_whiteBishop(self):
        return self._whiteBishop

    def set_whiteBishop(self, value):
        self._whiteBishop = value
        self._update_empty()

    def get_whiteRook(self):
        return self._whiteRook

    def set_whiteRook(self, value):
        self._whiteRook = value
        self._update_empty()

    def get_whiteQueen(self):
        return self._whiteQueen

    def set_whiteQueen(self, value):
        self._whiteQueen = value
        self._update_empty()

    def get_whiteKing(self):
        return self._whiteKing

    def set_whiteKing(self, value):
        self._whiteKing = value
        self._update_empty()

    def get_blackPawn(self):
        return self._blackPawn

    def set_blackPawn(self, value):
        self._blackPawn = value
        self._update_empty()

    def get_blackKnight(self):
        return self._blackKnight

    def set_blackKnight(self, value):
        self._blackKnight = value
        self._update_empty()

    def get_blackBishop(self):
        return self._blackBishop

    def set_blackBishop(self, value):
        self._blackBishop = value
        self._update_empty()

    def get_blackRook(self):
        return self._blackRook

    def set_blackRook(self, value):
        self._blackRook = value
        self._update_empty()

    def get_blackQueen(self):
        return self._blackQueen

    def set_blackQueen(self, value):
        self._blackQueen = value
        self._update_empty()

    def get_blackKing(self):
        return self._blackKing

    def set_blackKing(self, value):
        self._blackKing = value
        self._update_empty()

    def get_empty(self):
        return self._empty

    def print_bitboard(self, bitboard):
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
board = chessBoard(
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

# Print the bitboard for white pawns
print("White Pawns:")
board.print_bitboard(board.get_whitePawn())

# Print the bitboard for empty squares
print("Empty squares:")
board.print_bitboard(board.get_empty())
