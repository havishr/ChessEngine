import pygame as p
from ChessEngineNoBit import GameState, Move

PROMOTION_WINDOW_SIZE = (200, 200)  # Size of the promotion pop-up window
WIDTH = HEIGHT = 512  # Standard dimensions for the board
DIMENSION = 8  # Chessboard is 8x8
SQ_SIZE = HEIGHT // DIMENSION  # Size of each square
MAX_FPS = 15  # For smooth animations
IMAGES = {}

def loadImages():
    """ Loads images of chess pieces into a dictionary """
    pieces = ["wK", "wQ", "wR", "wB", "wN", "wp", "bK", "bQ", "bR", "bB", "bN", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

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
                        piece_captured = gs.board[to_square[0]][to_square[1]]

                        # Check for castling
                        if piece_moved == 'wK' or piece_moved == 'bK':
                            if from_square[1] - to_square[1] == -2:
                                move_type = Move.CASTLE_KINGSIDE
                            elif from_square[1] - to_square[1] == 2:
                                move_type = Move.CASTLE_QUEENSIDE

                        # Check for en passant
                        if piece_moved == 'wp' or piece_moved == 'bp':
                            if from_square[1] != to_square[1] and piece_captured == '..':
                                move_type = Move.EN_PASSANT
                                piece_captured = 'wp' if gs.whiteToMove else 'bp'

                        # Check for capture
                        if piece_captured != '..':
                            move_type = Move.CAPTURE

                        # Check for Promotion
                        if piece_moved == 'wp' or piece_moved == 'bp':
                            if to_square[0] == 0 or to_square[0] == 7:
                                move_type = Move.PROMOTION

                        move = Move(from_square, to_square, move_type, piece_moved, piece_captured)

                        if move.move_type == Move.PROMOTION:
                            move.promotion_piece = selectPromotionPiece(gs.whiteToMove)
                            move.promotion_piece = 'w' + move.promotion_piece if gs.whiteToMove else 'b' + move.promotion_piece
                            print(move)
                        if move in valid_moves:
                            print(move)
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


if __name__ == "__main__":
    main()
