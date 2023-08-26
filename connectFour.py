import pygame
import time

HEIGHT, WIDTH = 800, 700
ROWS, COLS = 7, 6
SQUARE_SIZE = WIDTH // COLS
    
PURPLE = (76, 0, 153)
WHITE = (255, 255, 255)
BLUE = (0, 102, 102)
GREEN = (76, 153, 0)
BLACK = (0, 0, 0)
class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.create_board()

    def draw_squares(self, win):
        win.fill(GREEN)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Piece(row, col, WHITE))

    def draw(self, win):
        win.fill(GREEN)
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                piece.draw(win)
        
    def allowsMove(self, col):
        '''return True if the calling Board object can allow a
        move into colmn c.'''
        count = 0
        if 0 <= col <= len(self.board)-1:
            for i in range(len(self.board[col])):
                if self.board[col][i].color == WHITE:
                    count += 1
            if count < ROWS:
                return True
        return False

    def move(self, col, piece_color):
        """Adds a piece of the specified color into the specified column."""
        if self.allowsMove(col):
            for row in range(ROWS - 1, -1, -1):
                if self.board[row][col].color == WHITE:
                    self.board[row][col].set_color(piece_color)
                    break
                
    def get_col_from_mouse(self, pos):
        x = pos
        col = x//SQUARE_SIZE
        return col


    def winsFor(self, ox):
        '''returns True if given checker ("X" or "O") ox has won
        the calling Board, returns False otherwise'''
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.winsFor_helper(row, col, ox):
                    return True
        return False

    def winsFor_helper(self, row, col, piece):
        '''returns True if there are four in a row horizontally, vertically, or diagonally'''
        horizontal = 0
        vertical = 0
        diagonal = 0
        if row + 3 < len(self.board) and col + 3 < len(self.board[0]):
            for h in range(4):
                if self.board[row][col + h].color == piece:
                    horizontal += 1
                elif self.board[row][col + h].color != piece:
                    break
            for v in range(4):
                if self.board[v + row][col].color == piece:
                    vertical += 1
                elif self.board[v + row][col].color != piece:
                    break
            for d in range(4):
                if self.board[row + d][col + d].color == piece:
                    diagonal += 1
                elif self.board[row - d][col - d].color == piece:
                    diagonal += 1
                elif self.board[row + d][col - d].color == piece:
                    diagonal += 1
                elif self.board[row - d][col + d].color == piece:
                    diagonal += 1
                elif self.board[row + d][col + d].color != piece:
                    break
        if horizontal == 4 or vertical == 4 or diagonal == 4:
            return True
                

class Piece:
    def __init__(self, row, col, color):
        self.col = col
        self.row = row
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

    def draw(self, win):
        radius = SQUARE_SIZE//2
        pygame.draw.circle(win, self.color, (self.x, self.y), radius - 10)

    def set_color(self, color):
        self.color = color
        

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CONNECT FOUR")

pygame.init()

def show_winning_message():
    font = pygame.font.Font(None, 36)
    text = font.render("Congratulations! You won!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(10)


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    piece = BLUE
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()[0]
                col = board.get_col_from_mouse(pos)
                board.move(col, piece)
                if board.winsFor(piece):
                    board.draw(WIN)
                    pygame.display.update()
                    show_winning_message()
                    run = False
                    break
                piece = BLUE if piece == PURPLE else PURPLE
        
        WIN.fill(GREEN)
        board.draw(WIN)
        pygame.display.update()
        
    pygame.quit()




if __name__ == "__main__":
    main()
