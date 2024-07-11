class GameState:
    def __init__(self):
        self.bitboard = {
            'wp': 0x000000000000FF00,  # White pawns
            'wR': 0x0000000000000081,  # White rooks
            'wN': 0x0000000000000042,  # White knights
            'wB': 0x0000000000000024,  # White bishops
            'wQ': 0x0000000000000010,  # White queen
            'wK': 0x0000000000000008,  # White king
            'bp': 0x00FF000000000000,  # Black pawns
            'bR': 0x8100000000000000,  # Black rooks
            'bN': 0x4200000000000000,  # Black knights
            'bB': 0x2400000000000000,  # Black bishops
            'bQ': 0x1000000000000000,  # Black queen
            'bK': 0x0800000000000000,  # Black king
            "empty": 0x0000FFFFFFFF0000
        }
        self.constants = {
            'Rank1': 0xFF00000000000000,  # 8th rank
            'Rank2': 0x00FF000000000000,  # 7th rank
            'Rank3': 0x0000FF0000000000,  # 6th rank
            'Rank4': 0x000000FF00000000,  # 5th rank
            'Rank5': 0x00000000FF000000,  # 4th rank
            'Rank6': 0x0000000000FF0000,  # 3rd rank
            'Rank7': 0x000000000000FF00,  # 2nd rank
            'Rank8': 0x00000000000000FF,  # 1st rank

            'FileA': 0x8080808080808080,  # File A
            'FileB': 0x4040404040404040,  # File B
            'FileC': 0x2020202020202020,  # File C
            'FileD': 0x1010101010101010,  # File D
            'FileE': 0x0808080808080808,  # File E
            'FileF': 0x0404040404040404,  # File F
            'FileG': 0x0202020202020202,  # File G
            'FileH': 0x0101010101010101   # File H
        }


        self.whiteToMove = True
        self.moveLog = []
        self.attackedSquares = set()

    def printBitboard(self):
        # Initialize an empty board display
        board_display = [["." for _ in range(8)] for _ in range(8)]

        # Mapping from piece identifiers to display characters
        piece_symbols = {
            'wp': 'P', 'wR': 'R', 'wN': 'N', 'wB': 'B', 'wQ': 'Q', 'wK': 'K',
            'bp': 'p', 'bR': 'r', 'bN': 'n', 'bB': 'b', 'bQ': 'q', 'bK': 'k'
        }

        # Populate the board display with pieces
        for piece, bitboard in self.bitboard.items():
            if piece != "empty":  # Skip the empty bitboard
                symbol = piece_symbols.get(piece, ".")
                for square in range(64):
                    if bitboard & (1 << square):
                        row = 7 - (square // 8)  # Adjust the row to print white at the bottom
                        col = 7 - (square % 8)  # Adjust the column to print a1 at bottom-right
                        board_display[row][col] = symbol

        # Print the board
        for row in board_display:
            print(" ".join(row))



    def makeMove(self, move):
        # Find which piece is moving
        moving_piece = None
        for piece, bitboard in self.bitboard.items():
            if piece != 'empty' and (bitboard & (1 << move.from_square)):
                moving_piece = piece
                break

        if moving_piece:
            # Clear the from square
            self.bitboard[moving_piece] &= ~(1 << move.from_square)

            # Remove any piece that might be at the destination square
            captured_piece = None
            for piece, bitboard in self.bitboard.items():
                if piece != 'empty' and (bitboard & (1 << move.to_square)):
                    captured_piece = piece
                    self.bitboard[piece] &= ~(1 << move.to_square)
                    break

            # Handle castling
            if move.special_move == Move.CASTLE_KINGSIDE:
                if self.whiteToMove:
                    self.bitboard['wR'] &= ~(1 << 7)
                    self.bitboard['wR'] |= (1 << 5)
                else:
                    self.bitboard['bR'] &= ~(1 << 63)
                    self.bitboard['bR'] |= (1 << 61)
            elif move.special_move == Move.CASTLE_QUEENSIDE:
                if self.whiteToMove:
                    self.bitboard['wR'] &= ~(1 << 0)
                    self.bitboard['wR'] |= (1 << 3)
                else:
                    self.bitboard['bR'] &= ~(1 << 56)
                    self.bitboard['bR'] |= (1 << 59)
            else:
                # Set the to square
                self.bitboard[moving_piece] |= (1 << move.to_square)
                # Handle promotions
                if move.special_move == Move.PROMOTION:
                    promotion_piece = ['wN', 'wB', 'wR', 'wQ'][move.promotion_piece] if self.whiteToMove else ['bN', 'bB', 'bR', 'bQ'][move.promotion_piece]
                    self.bitboard[promotion_piece] |= (1 << move.to_square)
                    self.bitboard[moving_piece] &= ~(1 << move.to_square)
            
            # Update the empty bitboard
            self.bitboard["empty"] |= (1 << move.from_square)  # Mark the 'from' square as empty
            self.bitboard["empty"] &= ~(1 << move.to_square)  # Mark the 'to' square as not empty

            # Toggle the turn
            self.whiteToMove = not self.whiteToMove

            self.bitboard["empty"] = ~(empt)
            # Add the move to the log, including information about the captured piece (if any)
            self.moveLog.append((move, captured_piece))

    def unmakeMove(self, move):
        # Find which piece is moving
        moving_piece = None
        for piece, bitboard in self.bitboard.items():
            if piece != 'empty' and (bitboard & (1 << move.to_square)):
                moving_piece = piece
                break

        if moving_piece:
            # Clear the to square
            self.bitboard[moving_piece] &= ~(1 << move.to_square)
            # Restore any piece that might have been captured at the destination square
            if self.moveLog:
                _, captured_piece = self.moveLog.pop()
                if captured_piece:
                    self.bitboard[captured_piece] |= (1 << move.to_square)
            
            # Handle castling
            if move.special_move == Move.CASTLE_KINGSIDE:
                if self.whiteToMove:
                    self.bitboard['wR'] &= ~(1 << 5)
                    self.bitboard['wR'] |= (1 << 7)
                else:
                    self.bitboard['bR'] &= ~(1 << 61)
                    self.bitboard['bR'] |= (1 << 63)
            elif move.special_move == Move.CASTLE_QUEENSIDE:
                if self.whiteToMove:
                    self.bitboard['wR'] &= ~(1 << 3)
                    self.bitboard['wR'] |= (1 << 0)
                else:
                    self.bitboard['bR'] &= ~(1 << 59)
                    self.bitboard['bR'] |= (1 << 56)
            else:
                # Set the from square
                self.bitboard[moving_piece] |= (1 << move.from_square)
            
            # Update the empty bitboard
            self.bitboard["empty"] |= (1 << move.to_square)  # Mark the 'to' square as empty
            self.bitboard["empty"] &= ~(1 << move.from_square)  # Mark the 'from' square as not empty

            # Toggle the turn back
            self.whiteToMove = not self.whiteToMove







    #Move generation
    
    def generateValidMoves(self):
        moves = []
        whitePieces = ['wp','wR','wN','wB','wQ','wK']
        blackPieces = ['bp','wR','bN','bB','bQ','bK']

        if self.whiteToMove:
            for piece in whitePieces:
                if piece == 'wp':
                    moves.extend(self.getPawnMoves())
                elif piece == 'wR':
                    moves.extend(self.getRookMoves())
                elif piece == 'wN':
                    moves.extend(self.getKnightMoves())
                elif piece == 'wB':
                    moves.extend(self.getBishopMoves())
                elif piece == 'wQ':
                    moves.extend(self.getQueenMoves())
                elif piece == 'wK':
                    moves.extend(self.getKingMoves())
                    moves.extend(self.getCastlingMoves())
        else:
            for piece in blackPieces:
                if piece == 'bp':
                    moves.extend(self.getPawnMoves())
                elif piece == 'bR':
                    moves.extend(self.getRookMoves())
                elif piece == 'bN':
                    moves.extend(self.getKnightMoves())
                elif piece == 'bB':
                    moves.extend(self.getBishopMoves())
                elif piece == 'bQ':
                    moves.extend(self.getQueenMoves())
                elif piece == 'bK':
                    moves.extend(self.getKingMoves())
                    moves.extend(self.getCastlingMoves())

        return moves
    

    def popLSB(self, bb):
        lsb = bb & -bb 
        index = lsb.bit_length() - 1  
        bb &= bb - 1 
        return index, bb  

    def getPawnMoves(self):
        moves = []
        empty = self.bitboard["empty"]
        pawnBoard = self.bitboard["wp"] if self.whiteToMove else self.bitboard["bp"]
        double_step_rank = self.constants["Rank7"] if self.whiteToMove else self.constants["Rank2"]
        file_a = self.constants["FileA"]
        file_h = self.constants["FileH"]
        enemy_pieces = self.bitboard["bp"] | self.bitboard['bR'] | self.bitboard['bN'] | \
            self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK'] if self.whiteToMove else \
            self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
            self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK']


        if self.whiteToMove:
            single_push = (pawnBoard << 8) & empty
            double_push = ((pawnBoard & double_step_rank) << 16) & (empty << 8) & empty
            left_captures = (pawnBoard << 9) & enemy_pieces & ~file_h
            right_captures = (pawnBoard << 7) & enemy_pieces & ~file_a
        else:
            single_push = (pawnBoard >> 8) & empty
            double_push = ((pawnBoard & double_step_rank) >> 16) & (empty >> 8) & empty
            left_captures = (pawnBoard >> 9) & enemy_pieces & ~file_a
            right_captures = (pawnBoard >> 7) & enemy_pieces & ~file_h


        move_types_and_shifts = [
            (single_push, 8 if self.whiteToMove else -8),
            (double_push, 16 if self.whiteToMove else -16),
            (left_captures, 9 if self.whiteToMove else -9),
            (right_captures, 7 if self.whiteToMove else -7)
        ]

        for move_bitboard, shift in move_types_and_shifts:
            while move_bitboard:
                to_square, move_bitboard = self.popLSB(move_bitboard)
                from_square = to_square - shift
                if shift == -7 or shift == 7 or shift == 9 or shift == -9:
                    self.attackedSquares.add(to_square)
                if (56 <= to_square <= 63):
                    moves.append(Move(from_square, to_square, promotion_piece= Move.KNIGHT, special_move= Move.PROMOTION))
                    moves.append(Move(from_square, to_square, promotion_piece= Move.BISHOP, special_move= Move.PROMOTION))
                    moves.append(Move(from_square, to_square, promotion_piece= Move.ROOK, special_move= Move.PROMOTION))
                    moves.append(Move(from_square, to_square, promotion_piece= Move.QUEEN, special_move= Move.PROMOTION))
                else:
                    moves.append(Move(from_square, to_square))


        return moves
    
    def getKnightMoves(self):
        knight_offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]  
        
        knight_bitboard = self.bitboard['wN'] if self.whiteToMove else self.bitboard['bN']
        own_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                     self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if self.whiteToMove else \
                     self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                     self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
        
        moves = []
        for square in range(64):
            if knight_bitboard & (1 << square):
                x, y = divmod(square, 8)
                for dx, dy in knight_offsets:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        target_square = nx * 8 + ny
                        if not (1 << target_square) & own_pieces: 
                            self.attackedSquares.add(target_square) 
                            moves.append(Move(square, target_square))

        return moves
    
    def getBishopMoves(self):
        bishop_bitboard = self.bitboard['wB'] if self.whiteToMove else self.bitboard['bB']
        own_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
        opponent_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if not self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']

        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for square in range(64):
            if bishop_bitboard & (1 << square):
                x, y = divmod(square, 8)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        target_square = nx * 8 + ny
                        if own_pieces & (1 << target_square):
                            break
                        moves.append(Move(square, target_square))
                        self.attackedSquares.add(target_square)
                        if opponent_pieces & (1 << target_square):
                            break
                        nx += dx
                        ny += dy
        return moves

    
    def getRookMoves(self):
        rook_bitboard = self.bitboard['wR'] if self.whiteToMove else self.bitboard['bR']
        own_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
        opponent_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if not self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']

        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for square in range(64):
            if rook_bitboard & (1 << square):
                x, y = divmod(square, 8)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        target_square = nx * 8 + ny
                        if own_pieces & (1 << target_square):
                            break
                        moves.append(Move(square, target_square))
                        self.attackedSquares.add(target_square)
                        if opponent_pieces & (1 << target_square):
                            break
                        nx += dx
                        ny += dy
        return moves
    def getQueenMoves(self):
        queen_bitboard = self.bitboard['wQ'] if self.whiteToMove else self.bitboard['bQ']
        own_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
        opponent_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if not self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']

        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),  # Rook directions
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Bishop directions

        for square in range(64):
            if queen_bitboard & (1 << square):
                x, y = divmod(square, 8)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        target_square = nx * 8 + ny
                        if own_pieces & (1 << target_square):
                            break
                        moves.append(Move(square, target_square))
                        self.attackedSquares.add(target_square)
                        if opponent_pieces & (1 << target_square):
                            break
                        nx += dx
                        ny += dy
        return moves
    def getKingMoves(self):
        king_bitboard = self.bitboard['wK'] if self.whiteToMove else self.bitboard['bK']
        own_pieces = self.bitboard['wp'] | self.bitboard['wR'] | self.bitboard['wN'] | \
                    self.bitboard['wB'] | self.bitboard['wQ'] | self.bitboard['wK'] if self.whiteToMove else \
                    self.bitboard['bp'] | self.bitboard['bR'] | self.bitboard['bN'] | \
                    self.bitboard['bB'] | self.bitboard['bQ'] | self.bitboard['bK']
                    

        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),  # Horizontal and vertical
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal

        for square in range(64):
            if king_bitboard & (1 << square):
                x, y = divmod(square, 8)
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        target_square = nx * 8 + ny
                        if not (own_pieces & (1 << target_square)):
                            moves.append(Move(square, target_square))
                            self.attackedSquares.add(target_square)
        return moves



    #Castling Determining


    def can_castle_kingside(self):
        if self.whiteToMove:
            king_position = 3
            rook_position = 0
            clear_path = 0x0000000000000060  # Bits that must be clear between the Rook at H1 and King at E1
        else:
            king_position = 59
            rook_position = 56
            clear_path = 0x0600000000000000  # Bits that must be clear between the Rook at H8 and King at E8

        if self.moveLog:  # Check if the king or rook has moved or captured
            moved_positions = {pos for move, _ in self.moveLog for pos in (move.from_square, move.to_square)}
            if king_position in moved_positions or rook_position in moved_positions:
                return False
        print(clear_path)
        # Check if the squares between the king and rook are empty
        if self.bitboard['empty'] & clear_path == clear_path:
            return True
        return False


    def can_castle_queenside(self):
        if self.whiteToMove:
            king_position = 4
            rook_position = 0
            clear_path = 0x000000000000000E  # Bits that must be clear between the Rook at A1 and King at E1
        else:
            king_position = 60
            rook_position = 56
            clear_path = 0x0E00000000000000  # Bits that must be clear between the Rook at A8 and King at E8

        if self.moveLog:  # Check if the king or rook has moved or captured
            moved_positions = {pos for move, _ in self.moveLog for pos in (move.from_square, move.to_square)}
            if king_position in moved_positions or rook_position in moved_positions:
                return False

        # Check if the squares between the king and rook are empty
        if self.bitboard['empty'] & clear_path == clear_path:
            return True
        return False

    
    def getCastlingMoves(self):
        moves = []
        print(self.can_castle_kingside())
        if self.can_castle_kingside():
            if self.whiteToMove:
                moves.append(Move(4, 6, special_move=Move.CASTLE_KINGSIDE))  # E1 to G1 for white
            else:
                moves.append(Move(60, 62, special_move=Move.CASTLE_KINGSIDE))  # E8 to G8 for black
        if self.can_castle_queenside():
            if self.whiteToMove:
                moves.append(Move(4, 2, special_move=Move.CASTLE_QUEENSIDE))  # E1 to C1 for white
            else:
                moves.append(Move(60, 58, special_move=Move.CASTLE_QUEENSIDE))  # E8 to C8 for black
        return moves



                    

                
                
        




    
class Move:
    NORMAL = 0
    CASTLE_KINGSIDE = 1
    CASTLE_QUEENSIDE = 2
    PROMOTION = 3

    KNIGHT = 0
    BISHOP = 1
    ROOK = 2
    QUEEN = 3

    def __init__(self, from_square, to_square, promotion_piece=0, special_move=NORMAL):
        self.from_square = from_square
        self.to_square = to_square
        self.promotion_piece = promotion_piece
        self.special_move = special_move

    def encode(self):
        return (self.from_square | 
                (self.to_square << 6) | 
                (self.promotion_piece << 12) | 
                (self.special_move << 14))

    @staticmethod
    def decode(move):
        from_square = move & 0x3F
        to_square = (move >> 6) & 0x3F
        promotion_piece = (move >> 12) & 0x3
        special_move = (move >> 14) & 0x3
        return Move(from_square, to_square, promotion_piece, special_move)

    def __eq__(self, other):
        return (self.from_square == other.from_square and 
                self.to_square == other.to_square and 
                self.promotion_piece == other.promotion_piece and 
                self.special_move == other.special_move)

    def __repr__(self):
        return (f"Move(from {self.from_square}, to {self.to_square}, " +
                f"promotion {self.promotion_piece}, special {self.special_move})")


gs = GameState()

gs.printBitboard()
print("")
whiteMoves = gs.generateValidMoves()

gs.makeMove(whiteMoves[3])
print("")
gs.printBitboard()

blackMoves = gs.generateValidMoves()
gs.makeMove(blackMoves[3])
print("")

gs.printBitboard()

bishMoves = gs.getBishopMoves()


gs.makeMove(bishMoves[3])

gs.printBitboard()

secondBlackMove = gs.generateValidMoves()

gs.makeMove(secondBlackMove[0])

gs.printBitboard()

knightMoves = gs.getKnightMoves()

gs.makeMove(knightMoves[0])

gs.makeMove(gs.generateValidMoves()[0])

gs.printBitboard()

print(gs.getCastlingMoves()[0])


