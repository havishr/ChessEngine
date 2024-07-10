import pygame as p
from ChessEngine import GameState, Move

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
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    valid_moves = gs.generateValidMoves()
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
                row = 7 - (location[1] // SQ_SIZE)
                clicked_square = row * 8 + col
                if 0 <= clicked_square < 64:  # Ensure clicked_square is valid
                    if sqSelected is None:
                        sqSelected = clicked_square
                        playerClicks = [sqSelected]
                    else:
                        playerClicks.append(clicked_square)
                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1])
                            if move in valid_moves:
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = None
                                playerClicks = []
                                valid_moves = gs.generateValidMoves()
                            else:
                                playerClicks = [sqSelected]  # Allow reselection
                else:
                    print("Invalid click location")

        if moveMade:
            print("Switching Turn")
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, (7 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, gs):
    for piece, bitboard in gs.bitboard.items():
        if piece != "empty":
            for square in range(64):
                if bitboard & (1 << square):
                    row = 7 - (square // 8)  # Adjust row for bottom-to-top display
                    col = square % 8
                    screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
