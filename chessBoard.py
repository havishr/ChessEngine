class ChessBoard:
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

    def whitePawn(self):
        return self._whitePawn

    def whitePawn(self, value):
        self._whitePawn = value

    def whiteKnight(self):
        return self._whiteKnight

    def whiteKnight(self, value):
        self._whiteKnight = value

    def whiteBishop(self):
        return self._whiteBishop

    def whiteBishop(self, value):
        self._whiteBishop = value

    def whiteRook(self):
        return self._whiteRook

    def whiteRook(self, value):
        self._whiteRook = value

    def whiteQueen(self):
        return self._whiteQueen

    def whiteQueen(self, value):
        self._whiteQueen = value

    def whiteKing(self):
        return self._whiteKing

    def whiteKing(self, value):
        self._whiteKing = value

    def blackPawn(self):
        return self._blackPawn

    def blackPawn(self, value):
        self._blackPawn = value

    def blackKnight(self):
        return self._blackKnight

    def blackKnight(self, value):
        self._blackKnight = value

    def blackBishop(self):
        return self._blackBishop

    def blackBishop(self, value):
        self._blackBishop = value

    def blackRook(self):
        return self._blackRook

    def blackRook(self, value):
        self._blackRook = value

    def blackQueen(self):
        return self._blackQueen

    def blackQueen(self, value):
        self._blackQueen = value

    def blackKing(self):
        return self._blackKing

    def blackKing(self, value):
        self._blackKing = value
