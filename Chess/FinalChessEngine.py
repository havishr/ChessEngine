STARTING_WHITE_KING = (7,4)
STARTING_BLACK_KING = (0,4)
class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],

            ['..', '..', '..', '..', '..', '..', '..', '..'],

            ['..', '..', '..', '..', '..', '..', '..', '..'],

            ['..', '..', '..', '..', '..', '..', '..', '..'],

            ['..', '..', '..', '..', '..', '..', '..', '..'],

            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],

            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.enPassantPossible = ()

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.pieceOffsets = {
            "N" : [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
            "B" : [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            "R" : [(-1, 0), (1, 0), (0, -1), (0, 1)],
            "Q" : [(-1, -1), (-1, 1), (1, -1), (1, 1),(-1, 0), (1, 0), (0, -1), (0, 1)],
            "K" : [(-1, -1), (-1, 1), (1, -1), (1, 1),(-1, 0), (1, 0), (0, -1), (0, 1)]
        }


        self.whiteKingSideCastle = True
        self.whiteQueenSideCastle = True

        self.blackKingSideCastle = True
        self.blackQueenSideCastle = True


    def makeMove(self, move, color):
        fromSquare, toSquare = move.fromSquare, move.toSquare
        pieceMoved = self.board[fromSquare[0]][fromSquare[1]]

        # Update the board with the move
        self.board[fromSquare[0]][fromSquare[1]], self.board[toSquare[0]][toSquare[1]] = "..", pieceMoved

        # Update King location if the king is moved
        if pieceMoved[1] == "K":
            if color == "w":
                self.whiteKingLocation = toSquare
                # Revoke castling rights for white
                self.whiteKingSideCastle = False
                self.whiteQueenSideCastle = False
            else:
                self.blackKingLocation = toSquare
                # Revoke castling rights for black
                self.blackKingSideCastle = False
                self.blackQueenSideCastle = False

        # Handle castling move
        if move.castle:
            if toSquare[1] == 6:  # King-side castling
                self.board[toSquare[0]][5], self.board[toSquare[0]][7] = color + "R", ".."
            elif toSquare[1] == 2:  # Queen-side castling
                self.board[toSquare[0]][3], self.board[toSquare[0]][0] = color + "R", ".."

        # Handle en passant move
        if move.enPassant:
            if color == "w":
                self.board[toSquare[0] + 1][toSquare[1]] = ".."  # Remove the captured pawn
            else:
                self.board[toSquare[0] - 1][toSquare[1]] = ".."  # Remove the captured pawn

        # Handle pawn promotion
        if move.promotionPiece:
            self.board[toSquare[0]][toSquare[1]] = color + move.promotionPiece

        # Revoke castling rights if a rook moves from its starting position
        if pieceMoved == "wR":
            if fromSquare == (7, 0):  # White Queen-side rook
                self.whiteQueenSideCastle = False
            elif fromSquare == (7, 7):  # White King-side rook
                self.whiteKingSideCastle = False
        elif pieceMoved == "bR":
            if fromSquare == (0, 0):  # Black Queen-side rook
                self.blackQueenSideCastle = False
            elif fromSquare == (0, 7):  # Black King-side rook
                self.blackKingSideCastle = False

        # Update en passant possible square
        if pieceMoved[1] == "p" and abs(fromSquare[0] - toSquare[0]) == 2:
            self.enPassantPossible = ((fromSquare[0] + toSquare[0]) // 2, fromSquare[1])
        else:
            self.enPassantPossible = ()

        # Log the move
        self.moveLog.append(move)

        # Change turn
        self.whiteToMove = not self.whiteToMove


    

    def unmakeMove(self, move, previousEnPassant, previousCastlingRights):
        fromSquare, toSquare = move.fromSquare, move.toSquare
        pieceMoved = self.board[toSquare[0]][toSquare[1]]
        
        # Undo the move by moving the piece back to its original square
        self.board[fromSquare[0]][fromSquare[1]] = pieceMoved
        self.board[toSquare[0]][toSquare[1]] = move.capturedPiece
        
        # If the piece was a king, reset its position
        if pieceMoved[1] == "K":
            if pieceMoved[0] == "w":
                self.whiteKingLocation = fromSquare
            else:
                self.blackKingLocation = fromSquare
        
        # Undo castling
        if move.castle:
            if toSquare[1] == 6:  # King-side castling
                self.board[toSquare[0]][7], self.board[toSquare[0]][5] = pieceMoved[0] + "R", ".."
            elif toSquare[1] == 2:  # Queen-side castling
                self.board[toSquare[0]][0], self.board[toSquare[0]][3] = pieceMoved[0] + "R", ".."
        
        # Undo en passant
        if move.enPassant:
            if pieceMoved[0] == "w":
                self.board[toSquare[0] + 1][toSquare[1]] = "bp"  # Restore the captured pawn
            else:
                self.board[toSquare[0] - 1][toSquare[1]] = "wp"  # Restore the captured pawn
            self.board[toSquare[0]][toSquare[1]] = ".."
        
        # Undo pawn promotion
        if move.promotionPiece:
            self.board[fromSquare[0]][fromSquare[1]] = pieceMoved[0] + "p"  # Revert to a pawn
        
        # Restore the en passant square and castling rights
        self.enPassantPossible = previousEnPassant
        self.whiteKingSideCastle, self.whiteQueenSideCastle, self.blackKingSideCastle, self.blackQueenSideCastle = previousCastlingRights
        
        # Remove the move from the move log
        self.moveLog.pop()

        # Revert the turn
        self.whiteToMove = not self.whiteToMove









    
    #Move Generation
    def generatePawnMove(self, r, c, color):
        moves = []
        if color == "w":
            if self.board[r - 1][c] == "..":
                if r - 1 == 0:
                    moves.append(Move( (r,c),(r - 1,c), None, "N"))
                    moves.append(Move( (r,c),(r - 1,c), None, "B"))
                    moves.append(Move( (r,c),(r - 1,c), None, "R"))
                    moves.append(Move( (r,c),(r - 1,c), None, "Q"))
                else:
                    moves.append(Move((r,c),(r - 1,c)))

                if r == 6 and self.board[r-2][c] == "..":
                    moves.append(Move((r,c),(r-2,c)))

            if c + 1 < 8 and self.board[r - 1][c + 1] != "..":
                capturedPiece = self.board[r-1][c+1]
                if r - 1 == 0:
                    moves.append(Move( (r,c), (r-1,c+1), capturedPiece, "N"))
                    moves.append(Move( (r,c), (r-1,c+1), capturedPiece, "B"))
                    moves.append(Move( (r,c), (r-1,c+1), capturedPiece, "R"))
                    moves.append(Move( (r,c), (r-1,c+1), capturedPiece, "Q"))
                else:
                    moves.append(Move((r,c),(r-1,c+1), capturedPiece))

            if c - 1 >= 0 and self.board[r - 1][c - 1] != "..":
                capturedPiece = self.board[r-1][c-1]
                if r - 1 == 0:
                    moves.append(Move( (r,c), (r-1,c-1), capturedPiece, "N"))
                    moves.append(Move( (r,c), (r-1,c-1), capturedPiece, "B"))
                    moves.append(Move( (r,c), (r-1,c-1), capturedPiece, "R"))
                    moves.append(Move( (r,c), (r-1,c-1), capturedPiece, "Q"))
                else:
                    moves.append(Move((r,c),(r-1,c-1)))  

            if (r-1, c+1) == self.enPassantPossible:
                moves.append(Move((r,c), (r-1,c+1), None, None, True))
            
            elif (r-1,c-1) == self.enPassantPossible:
                moves.append(Move((r,c), (r-1,c-1), None, None, True))



        else:


            if self.board[r + 1][c] == "..":
                if r + 1 == 7:
                    moves.append(Move( (r,c),(r + 1,c), None, "N"))
                    moves.append(Move( (r,c),(r + 1,c), None, "B"))
                    moves.append(Move( (r,c),(r + 1,c), None, "R"))
                    moves.append(Move( (r,c),(r + 1,c), None, "Q"))
                else:
                    moves.append(Move( (r,c),(r + 1,c)))


                if r == 1 and self.board[r+2][c] == "..":
                    moves.append(Move((r,c),(r+2,c)))


            if c + 1 < 8 and self.board[r + 1][c + 1] != "..":
                capturedPiece = self.board[r+1][c+1]
                if r + 1 == 0:
                    moves.append(Move( (r,c), (r+1,c+1), capturedPiece, "N"))
                    moves.append(Move( (r,c), (r+1,c+1), capturedPiece, "B"))
                    moves.append(Move( (r,c), (r+1,c+1), capturedPiece, "R"))
                    moves.append(Move( (r,c), (r+1,c+1), capturedPiece, "Q"))
                else:
                    moves.append(Move((r,c),(r+1,c+1),capturedPiece))

            if c - 1 >= 0 and self.board[r + 1][c - 1] != "..":
                capturedPiece = self.board[r+1][c-1]
                if r - 1 == 0:
                    moves.append(Move( (r,c), (r+1,c-1), capturedPiece, "N"))
                    moves.append(Move( (r,c), (r+1,c-1), capturedPiece, "B"))
                    moves.append(Move( (r,c), (r+1,c-1), capturedPiece, "R"))
                    moves.append(Move( (r,c), (r+1,c-1), capturedPiece, "Q"))
                else:
                    moves.append(Move((r,c),(r+1,c-1),capturedPiece))  
                        
            if (r-1, c+1) == self.enPassantPossible:
                moves.append(Move((r,c), (r+1,c+1), "..", enPassant=True))
            
            elif (r-1,c-1) == self.enPassantPossible:
                moves.append(Move((r,c), (r+1,c-1), "..", enPassant=True))
            
        return moves


    def generateKnightMove(self, r, c, color):
        moves = []
        offsets = self.pieceOffsets["N"]
        opponentPiece = ""
        if color == "w":
            opponentPiece = "b"
        else:
            opponentPiece = "w"

        for rowAdj, colAdj in offsets:
            newRow, newCol = r + rowAdj, c + colAdj
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.board[newRow][newCol][0] == opponentPiece or self.board[newRow][newCol][0] == ".":
                    moves.append(Move((r,c),(newRow,newCol), self.board[newRow][newCol]))
        return moves

        

    def generateSlidingMoves(self, r, c, piece, color):
        moves = []
        offsets = self.pieceOffsets[piece]
        opponentPiece = ""
        if color == "w":
            opponentPiece = "b"
        else:
            opponentPiece = "w"
        
        for rowAdj, colAdj in offsets:
            newRow, newCol = r + rowAdj, c + colAdj
            while 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.board[newRow][newCol][0] == ".":
                    moves.append(Move((r,c),(newRow,newCol), self.board[newRow][newCol]))
                    newRow, newCol = newRow + rowAdj, newCol + colAdj
                else:
                    if self.board[newRow][newCol][0] == opponentPiece:
                        moves.append(Move((r,c),(newRow,newCol), self.board[newRow][newCol]))
                    break
        return moves
    



    def generateKingMove(self, r, c, color):
        moves = []
        offsets = self.pieceOffsets["K"]
        opponentPiece = ""
        if color == "w":
            opponentPiece = "b"
        else:
            opponentPiece = "w"
        
        for rowAdj, colAdj in offsets:
            newRow, newCol = r + rowAdj, c + colAdj
            if 0 <= newRow < 8 and 0 <= newCol < 8:
                if self.board[newRow][newCol][0] == opponentPiece or self.board[newRow][newCol] == "..":
                    moves.append(Move((r,c),(newRow,newCol), self.board[newRow][newCol]))
        return moves
    
    
    def generateCastlingMoves(self, r, c, color):
        moves = []
        if self.whiteKingLocation == STARTING_WHITE_KING and color == "w":

            illegalSquares = self.generateAttackedSquares("b")

            if (r,c) not in illegalSquares and (r,c+1) not in illegalSquares and (r,c+2) not in illegalSquares and self.board[r][c+1] == ".." and self.board[r][c+2] == ".." and self.whiteKingSideCastle:

                moves.append(Move((r,c),(r,c + 2), self.board[r][c+2], castle= True))

            if (r,c) not in illegalSquares and (r,c-1) not in illegalSquares and (r,c-2) not in illegalSquares and (r,c-3) not in illegalSquares and self.board[r][c-1] == ".." and self.board[r][c-2] == ".." and self.board[r][c-3] == ".." and self.whiteQueenSideCastle:
                
                moves.append(Move((r,c),(r,c - 2), self.board[r][c-2], castle= True))


        elif self.blackKingLocation == STARTING_BLACK_KING and color == "b":

            illegalSquares = self.generateAttackedSquares("w")

            if (r,c) not in illegalSquares and (r,c+1) not in illegalSquares and (r,c+2) not in illegalSquares and self.board[r][c+1] == ".." and self.board[r][c+2] == ".." and self.whiteKingSideCastle:

                moves.append(Move((r,c),(r,c + 2), self.board[r][c+2], castle= True))

            if (r,c) not in illegalSquares and (r,c-1) not in illegalSquares and (r,c-2) not in illegalSquares and (r,c-3) not in illegalSquares and self.board[r][c-1] == ".." and self.board[r][c-2] == ".." and self.board[r][c-3] == ".." and self.whiteQueenSideCastle:
                
                moves.append(Move((r,c),(r,c - 2), self.board[r][c-2], castle= True))

        return moves

    

    def generateAttackedSquares(self, color):
        squares = set()
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece[0] == color:
                    pieceType = piece[1]
                    if pieceType == 'p':
                        if color == 'w':  
                            if r - 1 >= 0:
                                if c - 1 >= 0:
                                    squares.add((r - 1, c - 1))
                                if c + 1 < 8:
                                    squares.add((r - 1, c + 1))
                        else: 
                            if r + 1 < 8:
                                if c - 1 >= 0:
                                    squares.add((r + 1, c - 1))
                                if c + 1 < 8:
                                    squares.add((r + 1, c + 1))
                    else:
                        if pieceType == 'N':
                            moves = self.generateKnightMove(r, c, color)
                        elif pieceType in ('B', 'R', 'Q'):
                            moves = self.generateSlidingMoves(r, c, pieceType, color)
                        elif pieceType == 'K':
                            moves = self.generateKingMove(r, c, color)
                        for move in moves:
                            squares.add(move.toSquare)
        return squares





         
    

class Move:
    def __init__(self, fromSquare, toSquare, capturedPiece = "..", promotionPiece = None, enPassant = False, castle = False):
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.capturedPiece = capturedPiece
        self.promotionPiece = promotionPiece
        self.enPassant = enPassant
        self.castle = castle

    def __repr__(self):
        return (f"(Move(from {self.fromSquare}, to {self.toSquare}, " +
                f" Moved: {self.capturedPiece}, " +
                f" Promotion Piece: {self.promotionPiece}))")
        

gs = GameState()

print(gs.generateAttackedSquares("w"))