import pygame as p
from ChessEngineNoBit import GameState, Move

WIDTH = HEIGHT = 512  # Standard dimensions for the board
DIMENSION = 8  # Chessboard is 8x8
SQ_SIZE = HEIGHT // DIMENSION  # Size of each square
MAX_FPS = 15  # For smooth animations
IMAGES = {}
PROMOTION_WINDOW_SIZE = (200, 200)  # Size of the promotion pop-up window

def loadImages():
    """ Loads images of chess pieces into a dictionary """
    pieces = ["wK", "wQ", "wR", "wB", "wN", "wp", "bK", "bQ", "bR", "bB", "bN", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def selectPromotionPiece(whiteToMove):
    promotion_window = p.display.set_mode(PROMOTION_WINDOW_SIZE)
    promotion_window.fill(p.Color("white"))
    pieces = ['Q', 'R', 'B', 'N']
    color = 'w' if whiteToMove else 'b'
    for i, piece in enumerate(pieces):
        promotion_window.blit(IMAGES[color + piece], p.Rect(50, i * 50, 50, 50))
    p.display.flip()

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                selected_row = location[1] // 50
                if 0 <= selected_row < 4:
                    return pieces[selected_row]

def main():
    # Initialize pygame
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # Get the game state
    gs = GameState()
    valid_moves = gs.generateValidMoves()
    for move in valid_moves:
        print(move)
    # Set basic starting variables
    moveMade = False
    loadImages()
    running = True
    sqSelected = None
    playerClicks = []
    pendingMove = None

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected is None:
                    sqSelected = (row, col)
                    playerClicks = [sqSelected]
                else:
                    playerClicks.append((row, col))
                    if len(playerClicks) == 2:
                        from_square = (playerClicks[0][0], playerClicks[0][1])
                        to_square = (playerClicks[1][0], playerClicks[1][1])
                        move_type = Move.MOVE
                        piece_moved = gs.board[from_square[0]][from_square[1]]
                        piece_captured = gs.board[to_square[0]][from_square[1]]

                        # Check for castling
                        if piece_moved == 'wK' or piece_moved == 'bK':
                            if from_square[1] - to_square[1] == -2:
                                move_type = Move.CASTLE_KINGSIDE
                            elif from_square[1] - to_square[1] == 2:
                                move_type = Move.CASTLE_QUEENSIDE

                        if piece_captured != '..':
                            move_type = Move.CAPTURE

                        # Check for en passant
                        if piece_moved == 'wp' or piece_moved == 'bp':
                            if from_square[1] != to_square[1] and piece_captured == '..':
                                move_type = Move.EN_PASSANT
                                piece_captured = 'bp' if gs.whiteToMove else 'wp'

                        # Check for Promotion
                        if piece_moved == 'wp' or piece_moved == 'bp':
                            if to_square[0] == 0 or to_square[0] == 7:
                                move_type = Move.PROMOTION

                        move = Move(from_square, to_square, move_type, piece_moved, piece_captured)

                        print(move)

                        if move.move_type == Move.PROMOTION:
                            promotion_piece = selectPromotionPiece(gs.whiteToMove)
                            move.promotion_piece = 'w' + promotion_piece if gs.whiteToMove else 'b' + promotion_piece
                        if move in valid_moves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = None
                            playerClicks = []
                            print("Next moves")
                            valid_moves = gs.generateValidMoves()
                            for move in valid_moves:
                                print(move)
                        else:
                            print("move not valid")
                            playerClicks = []  # Allow reselection
                            sqSelected = None

        if moveMade:
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '..':
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def isPromotionMove(move):
    if move.piece_moved == 'wp' and move.to_square[0] == 0:
        return True
    if move.piece_moved == 'bp' and move.to_square[0] == 7:
        return True
    return False

if __name__ == "__main__":
    main()
