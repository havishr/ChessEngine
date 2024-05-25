class ChessBoard:
    def __init__(self, pawns, knights, bishops, rooks, queens, kings, white_pieces, black_pieces):
        self._pawns = pawns
        self._knights = knights
        self._bishops = bishops
        self._rooks = rooks
        self._queens = queens
        self._kings = kings
        self._white_pieces = white_pieces
        self._black_pieces = black_pieces
        self._update_all_pieces()
        self._update_empty()

    def _update_all_pieces(self):
        self._all_pieces = self._white_pieces | self._black_pieces

    def _update_empty(self):
        self._empty = ~self._all_pieces & 0xFFFFFFFFFFFFFFFF

    def set_piece(self, piece_bitboard, piece_type, color):
        if color == 'white':
            self._white_pieces &= ~getattr(self, f"_{piece_type}")
            self._white_pieces |= piece_bitboard
        else:
            self._black_pieces &= ~getattr(self, f"_{piece_type}")
            self._black_pieces |= piece_bitboard

        setattr(self, f"_{piece_type}", piece_bitboard)
        self._update_all_pieces()
        self._update_empty()

    def get_piece(self, piece_type):
        return getattr(self, f"_{piece_type}")

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
