import pygame as p
from ChessEngineNoBit import GameState, Move

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
                        move = Move(from_square, to_square, Move.MOVE, gs.board[from_square[0]][from_square[1]], gs.board[to_square[0]][to_square[1]])
                        if move in valid_moves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = None
                            playerClicks = []
                            valid_moves = gs.generateValidMoves()
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

if __name__ == "__main__":
    main()
