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
        self.enPassantPossible = ()

    def printBoard(self):
        for row in self.board:
            print("  ".join(row))
    
    def makeMove(self, move):
        piece = self.board[move.from_square[0]][move.from_square[1]]
        self.board[move.from_square[0]][move.from_square[1]] = '..'
        if move.move_type == Move.PROMOTION:
            self.board[move.to_square[0]][move.to_square[1]] = move.promotion_piece
        else:
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
            self.board[move.from_square[0]][move.to_square[1]] = '..'  # Remove the captured pawn
        elif abs(move.to_square[0] - move.from_square[0]) == 2 and piece[1] == 'p':
            # Set enPassantPossible if a pawn moved two squares
            self.enPassantPossible = ((move.from_square[0] + move.to_square[0]) // 2, move.from_square[1])
        else:
            self.enPassantPossible = ()

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def unmakeMove(self, move):
        self.board[move.from_square[0]][move.from_square[1]] = move.piece_moved
        if move.move_type == Move.PROMOTION:
            self.board[move.to_square[0]][move.to_square[1]] = '..'
            self.board[move.from_square[0]][move.from_square[1]] = 'wp' if self.whiteToMove else 'bp'
        else:
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
        # Reset enPassantPossible to the state before the move
        if self.moveLog:
            lastMove = self.moveLog[-1]
            if lastMove.move_type == Move.MOVE and abs(lastMove.to_square[0] - lastMove.from_square[0]) == 2 and lastMove.piece_moved[1] == 'p':
                self.enPassantPossible = ((lastMove.from_square[0] + lastMove.to_square[0]) // 2, lastMove.from_square[1])
            else:
                self.enPassantPossible = ()
        else:
            self.enPassantPossible = ()

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
                if r-1 == 0:
                    self.addPromotionMoves(r, c, r-1, c, moves, 'wp')
                else:
                    moves.append(Move((r, c), (r-1, c), Move.MOVE, 'wp'))
                    if r == 6 and self.board[r-2][c] == '..':
                        moves.append(Move((r, c), (r-2, c), Move.MOVE, 'wp'))
            if c-1 >= 0:  # Capture to the left
                if self.board[r-1][c-1][0] == 'b':
                    if r-1 == 0:
                        self.addPromotionMoves(r, c, r-1, c-1, moves, 'wp', self.board[r-1][c-1])
                    else:
                        moves.append(Move((r, c), (r-1, c-1), Move.CAPTURE, 'wp', self.board[r-1][c-1]))
                elif (r-1, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), Move.EN_PASSANT, 'wp', 'bp'))
            if c+1 <= 7:  # Capture to the right
                if self.board[r-1][c+1][0] == 'b':
                    if r-1 == 0:
                        self.addPromotionMoves(r, c, r-1, c+1, moves, 'wp', self.board[r-1][c+1])
                    else:
                        moves.append(Move((r, c), (r-1, c+1), Move.CAPTURE, 'wp', self.board[r-1][c+1]))
                elif (r-1, c+1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), Move.EN_PASSANT, 'wp', 'bp'))
        else:
            if self.board[r+1][c] == '..':
                if r+1 == 7:
                    self.addPromotionMoves(r, c, r+1, c, moves, 'bp')
                else:
                    moves.append(Move((r, c), (r+1, c), Move.MOVE, 'bp'))
                    if r == 1 and self.board[r+2][c] == '..':
                        moves.append(Move((r, c), (r+2, c), Move.MOVE, 'bp'))
            if c-1 >= 0:  # Capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    if r+1 == 7:
                        self.addPromotionMoves(r, c, r+1, c-1, moves, 'bp', self.board[r+1][c-1])
                    else:
                        moves.append(Move((r, c), (r+1, c-1), Move.CAPTURE, 'bp', self.board[r+1][c-1]))
                elif (r+1, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), Move.EN_PASSANT, 'bp', 'wp'))
            if c+1 <= 7:  # Capture to the right
                if self.board[r+1][c+1][0] == 'w':
                    if r+1 == 7:
                        self.addPromotionMoves(r, c, r+1, c+1, moves, 'bp', self.board[r+1][c+1])
                    else:
                        moves.append(Move((r, c), (r+1, c+1), Move.CAPTURE, 'bp', self.board[r+1][c+1]))
                elif (r+1, c+1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), Move.EN_PASSANT, 'bp', 'wp'))

    def addPromotionMoves(self, r, c, end_row, end_col, moves, piece_moved, piece_captured='..'):
        promotion_pieces = ['Q', 'R', 'B', 'N']
        for p in promotion_pieces:
            moves.append(Move((r, c), (end_row, end_col), Move.PROMOTION, piece_moved, piece_captured, 'w' + p if self.whiteToMove else 'b' + p))

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
        enemy_color = 'b' if self.whiteToMove else 'w'
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece[0] == enemy_color:
                    piece_type = piece[1]
                    if piece_type == 'p':
                        if enemy_color == 'w':  # white pawns attack diagonally up
                            if (r-1, c-1) == square or (r-1, c+1) == square:
                                return True
                        else:  # black pawns attack diagonally down
                            if (r+1, c-1) == square or (r+1, c+1) == square:
                                return True
                    elif piece_type == 'R':
                        if self.rookAttacks(r, c, square):
                            return True
                    elif piece_type == 'N':
                        if self.knightAttacks(r, c, square):
                            return True
                    elif piece_type == 'B':
                        if self.bishopAttacks(r, c, square):
                            return True
                    elif piece_type == 'Q':
                        if self.rookAttacks(r, c, square) or self.bishopAttacks(r, c, square):
                            return True
                    elif piece_type == 'K':
                        if abs(r - square[0]) <= 1 and abs(c - square[1]) <= 1:
                            return True
        return False


    def rookAttacks(self, r, c, square):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if (end_row, end_col) == square:
                    return True
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if self.board[end_row][end_col] != '..':
                        break
                else:
                    break
        return False

    def knightAttacks(self, r, c, square):
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for m in knight_moves:
            if (r + m[0], c + m[1]) == square:
                return True
        return False

    def bishopAttacks(self, r, c, square):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if (end_row, end_col) == square:
                    return True
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if self.board[end_row][end_col] != '..':
                        break
                else:
                    break
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
        return (f"(Move(from {self.from_square}, to {self.to_square}, " +
                f"Move Type: {self.move_type} Moved: {self.piece_moved}, " +
                f"Captured Piece: {self.piece_captured}, Promotion Piece: {self.promotion_piece}))")

gs = GameState()

print(gs.countPositions(6))