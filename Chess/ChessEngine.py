class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # First rank (black)
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # Second rank (black pawns)
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # Third rank (empty)
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # Fourth rank (empty)
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # Fifth rank (empty)
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # Sixth rank (empty)
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # Seventh rank (white pawns)
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],  # Eighth rank (white)
        ]
        self.bitboard = {
            'wp': 0x000000000000FF00,  # White pawns
            'wR': 0x0000000000000081,  # White rooks
            'wN': 0x0000000000000042,  # White knights
            'wB': 0x0000000000000024,  # White bishops
            'wQ': 0x0000000000000008,  # White queen
            'wK': 0x0000000000000010,  # White king
            'bp': 0x00FF000000000000,  # Black pawns
            'bR': 0x8100000000000000,  # Black rooks
            'bN': 0x4200000000000000,  # Black knights
            'bB': 0x2400000000000000,  # Black bishops
            'bQ': 0x0800000000000000,  # Black queen
            'bK': 0x1000000000000000,  # Black king
            "--": 0x0000111111110000
        }
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            pieceMoved = self.board[move.startRow][move.startCol]
            pieceCaptured = self.board[move.endRow][move.endCol]
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = pieceMoved
            startSq = self.squareToBitboardIndex(move.startRow, move.startCol)
            endSq = self.squareToBitboardIndex(move.endRow, move.endCol)
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove
            self.updateBitboards(pieceMoved, pieceCaptured, startSq, endSq)

    def updateBitboards(self, pieceMoved, pieceCaptured, startSq, endSq):
        print(pieceMoved)
        # Remove the piece from the start square
        self.bitboard[pieceMoved] &= ~(1 << (63 - startSq))
        # Place the piece on the end square
        self.bitboard[pieceMoved] |= (1 << (63 - endSq))
        # If a piece was captured, remove it from the bitboard
        if pieceCaptured != "--":
            self.bitboard[pieceCaptured] &= ~(1 << (63 - endSq))

    def squareToBitboardIndex(self, row, col):
        return row * 8 + col

def printBitboard(bitboard):
    for rank in range(8):
        line = ""
        for file in range(8):
            square = rank * 8 + file
            if (bitboard >> (63 - square)) & 1:
                line += "1 "
            else:
                line += ". "
        print(line)
    print()

class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __repr__(self):
        return f"{self.pieceMoved} from {self.getRankFile(self.startRow, self.startCol)} to {self.getRankFile(self.endRow, self.endCol)}, capturing {self.pieceCaptured}"

if __name__ == "__main__":
    gs = GameState()

    print("Before Move White Pawn Board")
    printBitboard(gs.bitboard['wp'])
    move = Move((6, 4), (4, 4), gs.board)  # Example move: e2 to e4
    gs.makeMove(move)
    print("After Move White Pawn Board")
    printBitboard(gs.bitboard['wp'])


    print("Before Move Black Pawn Board")
    printBitboard(gs.bitboard['bp'])
    move = Move((1, 4), (3, 4), gs.board)  # Example move: e7 to e5
    gs.makeMove(move)
    print("After Move Black Pawn Board")
    printBitboard(gs.bitboard['bp'])

    print("Before Move White Knight Board")
    printBitboard(gs.bitboard['wN'])

    move = Move((7, 1), (5, 2), gs.board)  # Example move: Nb1 to Nc3
    gs.makeMove(move)

    print("After Move White Knight Board")
    printBitboard(gs.bitboard['wN'])
