class GameState:
    def __init__(self):
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
            "--": 0x0000FFFFFFFF0000
        }
        self.constants = {
            'Rank1': 0x00000000000000FF,  # 1st rank
            'Rank2': 0x000000000000FF00,  # 2nd rank
            'Rank3': 0x0000000000FF0000,  # 3rd rank
            'Rank4': 0x00000000FF000000,  # 4th rank
            'Rank5': 0x000000FF00000000,  # 5th rank
            'Rank6': 0x0000FF0000000000,  # 6th rank
            'Rank7': 0x00FF000000000000,  # 7th rank
            'Rank8': 0xFF00000000000000,  # 8th rank

            'FileA': 0x0101010101010101,  # File A
            'FileB': 0x0202020202020202,  # File B
            'FileC': 0x0404040404040404,  # File C
            'FileD': 0x0808080808080808,  # File D
            'FileE': 0x1010101010101010,  # File E
            'FileF': 0x2020202020202020,  # File F
            'FileG': 0x4040404040404040,  # File G
            'FileH': 0x8080808080808080   # File H
        }

        self.whiteToMove = True
        self.moveLog = []


    def squareToBitboardIndex(self, row, col):
        return row * 8 + col
    
    def generateValidMoves(self):
        moves = []
        whitePieces = ['wp','wR','wN','wB','wQ','wK']
        blackPieces = ['bp','wR','bN','bB','bQ','bK']

        if self.whiteToMove:
            for piece in whitePieces:
                if piece == 'wp':
                    moves.extend(self.getPawnMoves(isWhite=True))
                elif piece == 'wR':
                    moves.extend(self.getRookMoves(isWhite=True))
                elif piece == 'wN':
                    moves.extend(self.getKnightMoves(isWhite=True))
                elif piece == 'wB':
                    moves.extend(self.getBishopMoves(isWhite=True))
                elif piece == 'wQ':
                    moves.extend(self.getQueenMoves(isWhite=True))
                elif piece == 'wK':
                    moves.extend(self.getKingMoves(isWhite=True))
        else:
            for piece in blackPieces:
                if piece == 'bp':
                    moves.extend(self.getPawnMoves(isWhite=False))
                elif piece == 'bR':
                    moves.extend(self.getRookMoves(isWhite=False))
                elif piece == 'bN':
                    moves.extend(self.getKnightMoves(isWhite=False))
                elif piece == 'bB':
                    moves.extend(self.getBishopMoves(isWhite=False))
                elif piece == 'bQ':
                    moves.extend(self.getQueenMoves(isWhite=False))
                elif piece == 'bK':
                    moves.extend(self.getKingMoves(isWhite=False))

        return moves
    def popLSB(board):
        lsb_index = (bb & -bb).bit_length() - 1  # Find the index of the LSB
        bb &= bb - 1  # Clear the LSB
        return lsb_index, bb







    def getPawnMoves(self):
        moves = []
        empty = self.bitboard["--"]

        if self.whiteToMove:
            pawnBoard = self.bitboard["wp"]
            enemyPieces = self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
            singlePush = (pawnBoard << 8) & empty
            doublePush = ((pawnBoard & self.constants["Rank2"]) << 16) & empty & (empty << 8)
            leftCaptures = (pawnBoard << 9) & ~self.constants["FileA"] & enemyPieces
            rightCaptures = (pawnBoard << 7) & ~self.constants["FileH"] & enemyPieces

            while singlePush:
                toSquare, singlePush = self.popLSB(singlePush)
                fromSquare = toSquare - 8
                moves.append(Move(fromSquare, toSquare))

            while doublePush:
                toSquare, doublePush = self.popLSB(doublePush)
                fromSquare = toSquare - 16
                moves.append(Move(fromSquare, toSquare))

            while leftCaptures:
                toSquare, leftCaptures = self.popLSB(leftCaptures)
                fromSquare = toSquare - 9
                moves.append(Move(fromSquare, toSquare))

            while rightCaptures:
                toSquare, rightCaptures = self.popLSB(rightCaptures)
                fromSquare = toSquare - 7
                moves.append(Move(fromSquare, toSquare))
            print(moves)
        else:
            pawnBoard = self.bitboard["bp"]
            enemyPieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK']
            singlePush = (pawnBoard >> 8) & empty
            doublePush = ((pawnBoard & self.constants["Rank7"]) >> 16) & empty & (empty >> 8)
            leftCaptures = (pawnBoard >> 9) & ~self.constants["FileH"] & enemyPieces
            rightCaptures = (pawnBoard >> 7) & ~self.constants["FileA"] & enemyPieces

            while singlePush:
                toSquare, singlePush = self.popLSB(singlePush)
                fromSquare = toSquare + 8

                moves.append(Move(fromSquare, toSquare))

            while doublePush:
                toSquare, doublePush = self.popLSB(doublePush)
                fromSquare = toSquare + 16

                moves.append(Move(fromSquare, toSquare))

            while leftCaptures:
                toSquare, leftCaptures = self.popLSB(leftCaptures)
                fromSquare = toSquare + 9

                moves.append(Move(fromSquare, toSquare))

            while rightCaptures:
                toSquare, rightCaptures = self.popLSB(rightCaptures)
                fromSquare = toSquare + 7

                moves.append(Move(fromSquare, toSquare))

        return moves

 


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
    def __init__(self, from_square, to_square, promotion_piece=0):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion_piece = promotion_piece
    
    def encode(self):
        return self.from_square | (self.to_square << 6) | (self.promotion_piece << 12)

    @staticmethod
    def decode(move):
        from_square = move & 0x3F           # Extract bits 0-5
        to_square = (move >> 6) & 0x3F      # Extract bits 6-11
        promotion_piece = (move >> 12) & 0xF # Extract bits 12-15
        return Move(from_square, to_square, promotion_piece)

    def __repr__(self):
        return f"Move(from {self.from_square}, to {self.to_square}, promotion {self.promotion_piece})"

gs = GameState()

gs.getPawnMoves()