class ChessAI:
    from ChessEngineNoBit import GameState
    def __init__(self, game_state):
        self.game_state = game_state
        self.piece = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}
        self.pst = {
            'p': (   0,   0,   0,   0,   0,   0,   0,   0,
                    78,  83,  86,  73, 102,  82,  85,  90,
                    7,  29,  21,  44,  40,  31,  44,   7,
                -17,  16,  -2,  15,  14,   0,  15, -13,
                -26,   3,  10,   9,   6,   1,   0, -23,
                -22,   9,   5, -11, -10,  -2,   3, -19,
                -31,   8,  -7, -37, -36, -14,   3, -31,
                    0,   0,   0,   0,   0,   0,   0,   0),
            'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
                    -3,  -6, 100, -36,   4,  62,  -4, -14,
                    10,  67,   1,  74,  73,  27,  62,  -2,
                    24,  24,  45,  37,  33,  41,  25,  17,
                    -1,   5,  31,  21,  22,  35,   2,   0,
                -18,  10,  13,  22,  18,  15,  11, -14,
                -23, -15,   2,   0,   2,   0, -23, -20,
                -74, -23, -26, -24, -19, -35, -22, -69),
            'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
                -11,  20,  35, -42, -39,  31,   2, -22,
                    -9,  39, -32,  41,  52, -10,  28, -14,
                    25,  17,  20,  34,  26,  25,  15,  10,
                    13,  10,  17,  23,  17,  16,   0,   7,
                    14,  25,  24,  15,   8,  25,  20,  15,
                    19,  20,  11,   6,   7,   6,  20,  16,
                    -7,   2, -15, -12, -14, -15, -10, -10),
            'R': (  35,  29,  33,   4,  37,  33,  56,  50,
                    55,  29,  56,  67,  55,  62,  34,  60,
                    19,  35,  28,  33,  45,  27,  25,  15,
                    0,   5,  16,  13,  18,  -4,  -9,  -6,
                -28, -35, -16, -21, -13, -29, -46, -30,
                -42, -28, -42, -25, -25, -35, -26, -46,
                -53, -38, -31, -26, -29, -43, -44, -53,
                -30, -24, -18,   5,  -2, -18, -31, -32),
            'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
                    14,  32,  60, -10,  20,  76,  57,  24,
                    -2,  43,  32,  60,  72,  63,  43,   2,
                    1, -16,  22,  17,  25,  20, -13,  -6,
                -14, -15,  -2,  -5,  -1, -10, -20, -22,
                -30,  -6, -13, -11, -16, -11, -16, -27,
                -36, -18,   0, -19, -15, -15, -21, -38,
                -39, -30, -31, -13, -31, -36, -34, -42),
            'K': (   4,  54,  47, -99, -99,  60,  83, -62,
                -32,  10,  55,  56,  56,  55,  10,   3,
                -62,  12, -57,  44, -67,  28,  37, -31,
                -55,  50,  11,  -4, -19,  13,   0, -49,
                -55, -43, -52, -28, -51, -47,  -8, -50,
                -47, -42, -43, -79, -64, -32, -29, -32,
                    -4,   3, -14, -50, -57, -18,  13,   4,
                    17,  30,  -3, -14,   6,  -1,  40,  18),
        }

    def findBestMove(self, depth):
        def minimax(depth, alpha, beta, maximizingPlayer):
            if depth == 0 or self.game_state.isCheckmate() or self.game_state.isStalemate():
                return self.evaluate_board()

            if maximizingPlayer:
                maxEval = -float('inf')
                for move in self.order_moves(self.game_state.generateValidMoves()):
                    self.game_state.makeMove(move)
                    eval = minimax(depth - 1, alpha, beta, False)
                    self.game_state.unmakeMove(move)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return maxEval
            else:
                if depth >= 3 and not self.game_state.isInCheck():
                    self.game_state.whiteToMove = not self.game_state.whiteToMove
                    eval = -minimax(depth - 3, -beta, -beta + 1, True)
                    self.game_state.whiteToMove = not self.game_state.whiteToMove
                    if eval >= beta:
                        return beta

                minEval = float('inf')
                for move in self.order_moves(self.game_state.generateValidMoves()):
                    self.game_state.makeMove(move)
                    eval = minimax(depth - 1, alpha, beta, True)
                    self.game_state.unmakeMove(move)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return minEval

        best_move = None
        best_score = -float('inf') if self.game_state.whiteToMove else float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in self.order_moves(self.game_state.generateValidMoves()):
            self.game_state.makeMove(move)
            score = minimax(depth - 1, alpha, beta, not self.game_state.whiteToMove)
            self.game_state.unmakeMove(move)

            if self.game_state.whiteToMove:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)

        return best_move

    def evaluate_board(self):
        piece_values = {
            'K': 0,
            'Q': 9,
            'R': 5,
            'B': 3,
            'N': 3,
            'p': 1
        }

        score = 0
        for r in range(len(self.game_state.board)):
            for c in range(len(self.game_state.board[r])):
                piece = self.game_state.board[r][c]
                if piece != '..':
                    piece_type = piece[1]
                    value = piece_values[piece_type]
                    if piece[0] == 'w':
                        score += value + self.pst[piece[1]][r * 8 + c]
                    else:
                        score -= value + self.pst[piece[1]][r * 8 + c]

        if self.game_state.isCheckmate():
            if self.game_state.whiteToMove:
                score -= 1000
            else:
                score += 1000
        elif self.game_state.isStalemate():
            score = 0

        return score

    def order_moves(self, moves):
        def move_value(move):
            start_row, start_col = move.from_square
            end_row, end_col = move.to_square
            piece = self.game_state.board[start_row][start_col]
            if piece in self.pst:
                return self.pst[piece[1]][end_row * 8 + end_col] - self.pst[piece[1]][start_row * 8 + start_col]
            return 0
        return sorted(moves, key=move_value, reverse=True)
    
    def make_opponent_move(self, move):
        self.game_state.makeMove(move)



