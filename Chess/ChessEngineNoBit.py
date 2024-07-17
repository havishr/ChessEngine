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
        self.attackedSquares = set()

    def printBoard(self):
        for row in self.board:
            print("  ".join(row))
    
    def makeMove(self, move):
        piece = self.board[move.from_square[0]][move.from_square[1]]
        self.board[move.from_square[0]][move.from_square[1]] = '..'
        self.board[move.to_square[0]][move.to_square[1]] = piece

        if move.move_type == Move.CASTLE_KINGSIDE:
            if self.whiteToMove:
                self.board[7][5], self.board[7][7] = self.board[7][7], '..'
            else:
                self.board[0][5], self.board[0][7] = self.board[0][7], '..'
        elif move.move_type == Move.CASTLE_QUEENSIDE:
            if self.whiteToMove:
                self.board[7][3], self.board[7][0] = self.board[7][0], '..'
            else:
                self.board[0][3], self.board[0][0] = self.board[0][0], '..'
        elif move.move_type == Move.EN_PASSANT:
            self.board[move.to_square[0]][move.to_square[1]] = move.piece_moved
            self.board[move.from_square[0]][move.from_square[1]] = '..'
            self.board[move.from_square[0]][move.to_square[1]] = '..'  # Remove the captured pawn

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def unmakeMove(self, move):
        self.board[move.from_square[0]][move.from_square[1]] = move.piece_moved
        self.board[move.to_square[0]][move.to_square[1]] = move.piece_captured

        if move.move_type == Move.CASTLE_KINGSIDE:
            if self.whiteToMove:
                self.board[7][5], self.board[7][7] = '..', 'wR'
            else:
                self.board[0][5], self.board[0][7] = '..', 'bR'
        elif move.move_type == Move.CASTLE_QUEENSIDE:
            if self.whiteToMove:
                self.board[7][3], self.board[7][0] = '..', 'wR'
            else:
                self.board[0][3], self.board[0][0] = '..', 'bR'
        elif move.move_type == Move.EN_PASSANT:
            self.board[move.from_square[0]][move.from_square[1]] = move.piece_moved
            self.board[move.to_square[0]][move.to_square[1]] = '..'
            self.board[move.from_square[0]][move.to_square[1]] = move.piece_captured  # Restore the captured pawn

        self.moveLog.pop()
        self.whiteToMove = not self.whiteToMove


    def generateValidMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece != '..':
                    color = 'w' if self.whiteToMove else 'b'
                    if piece[0] == color:
                        self.getPieceMoves(r, c, moves)
        return moves

    def getPieceMoves(self, r, c, moves):
        piece = self.board[r][c][1]
        if piece == 'p':
            self.getPawnMoves(r, c, moves)
        elif piece == 'R':
            self.getRookMoves(r, c, moves)
        elif piece == 'N':
            self.getKnightMoves(r, c, moves)
        elif piece == 'B':
            self.getBishopMoves(r, c, moves)
        elif piece == 'Q':
            self.getQueenMoves(r, c, moves)
        elif piece == 'K':
            self.getKingMoves(r, c, moves)

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '..':
                moves.append(Move((r, c), (r-1, c), Move.MOVE, 'wp'))
                if r == 6 and self.board[r-2][c] == '..':
                    moves.append(Move((r, c), (r-2, c), Move.MOVE, 'wp'))
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r, c), (r-1, c-1), Move.CAPTURE, 'wp', self.board[r-1][c-1]))
            if c+1 <= 7 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r, c), (r-1, c+1), Move.CAPTURE, 'wp', self.board[r-1][c+1]))
        else:
            if self.board[r+1][c] == '..':
                moves.append(Move((r, c), (r+1, c), Move.MOVE, 'bp'))
                if r == 1 and self.board[r+2][c] == '..':
                    moves.append(Move((r, c), (r+2, c), Move.MOVE, 'bp'))
            if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r, c), (r+1, c-1), Move.CAPTURE, 'bp', self.board[r+1][c-1]))
            if c+1 <= 7 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r, c), (r+1, c+1), Move.CAPTURE, 'bp', self.board[r+1][c+1]))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '..':
                        moves.append(Move((r, c), (end_row, end_col), Move.MOVE, self.board[r][c]))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), Move.CAPTURE, self.board[r][c], end_piece))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in knight_moves:
            end_row, end_col = r + m[0], c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if end_piece == '..':
                        moves.append(Move((r, c), (end_row, end_col), Move.MOVE, self.board[r][c]))
                    else:
                        moves.append(Move((r, c), (end_row, end_col), Move.CAPTURE, self.board[r][c], end_piece))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '..':
                        moves.append(Move((r, c), (end_row, end_col), Move.MOVE, self.board[r][c]))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), Move.CAPTURE, self.board[r][c], end_piece))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        king_moves = [
            (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in king_moves:
            end_row, end_col = r + m[0], c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if end_piece == '..':
                        moves.append(Move((r, c), (end_row, end_col), Move.MOVE, self.board[r][c]))
                    else:
                        moves.append(Move((r, c), (end_row, end_col), Move.CAPTURE, self.board[r][c], end_piece))
        self.getCastlingMoves(r, c, moves)

    def getCastlingMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.canCastleKingside():
                moves.append(Move((7, 4), (7, 6), Move.CASTLE_KINGSIDE, 'wK'))
            if self.canCastleQueenside():
                moves.append(Move((7, 4), (7, 2), Move.CASTLE_QUEENSIDE, 'wK'))
        else:
            if self.canCastleKingside():
                moves.append(Move((0, 4), (0, 6), Move.CASTLE_KINGSIDE, 'bK'))
            if self.canCastleQueenside():
                moves.append(Move((0, 4), (0, 2), Move.CASTLE_QUEENSIDE, 'bK'))

    def canCastleKingside(self):
        if self.whiteToMove:
            return (self.board[7][5] == '..' and self.board[7][6] == '..' and
                    not self.isUnderAttack((7, 4)) and not self.isUnderAttack((7, 5)) and not self.isUnderAttack((7, 6)))
        else:
            return (self.board[0][5] == '..' and self.board[0][6] == '..' and
                    not self.isUnderAttack((0, 4)) and not self.isUnderAttack((0, 5)) and not self.isUnderAttack((0, 6)))

    def canCastleQueenside(self):
        if self.whiteToMove:
            return (self.board[7][1] == '..' and self.board[7][2] == '..' and self.board[7][3] == '..' and
                    not self.isUnderAttack((7, 2)) and not self.isUnderAttack((7, 3)) and not self.isUnderAttack((7, 4)))
        else:
            return (self.board[0][1] == '..' and self.board[0][2] == '..' and self.board[0][3] == '..' and
                    not self.isUnderAttack((0, 2)) and not self.isUnderAttack((0, 3)) and not self.isUnderAttack((0, 4)))

    def isUnderAttack(self, square):
        for move in self.generateValidMoves():
            if move.to_square == square:
                return True
        return False
    

    def countPositions(self, depth):
        if depth == 0:
            return 1

        num_positions = 0
        moves = self.generateValidMoves()
        for move in moves:
            self.makeMove(move)
            num_positions += self.countPositions(depth - 1)
            self.unmakeMove(move)
        return num_positions


class Move:
    MOVE = 'move'
    CAPTURE = 'capture'
    CASTLE_KINGSIDE = 'castle_kingside'
    CASTLE_QUEENSIDE = 'castle_queenside'
    EN_PASSANT = 'en_passant'
    PROMOTION = 'promotion'

    def __init__(self, from_square, to_square, move_type, piece_moved, piece_captured='..', promotion_piece=None):
        self.from_square = from_square
        self.to_square = to_square
        self.move_type = move_type
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.promotion_piece = promotion_piece

    def __eq__(self, other):
        return (self.from_square == other.from_square and
                self.to_square == other.to_square and
                self.move_type == other.move_type and
                self.piece_moved == other.piece_moved and
                self.piece_captured == other.piece_captured and
                self.promotion_piece == other.promotion_piece)

    def __repr__(self):
        return (f"Move(from {self.from_square}, to {self.to_square}, " +
                f"type {self.move_type}, moved {self.piece_moved}, " +
                f"captured {self.piece_captured}, promotion {self.promotion_piece})")

gs = GameState()

num_positions = gs.countPositions(4)
print(f"Number of positions after 4 moves: {num_positions}")

