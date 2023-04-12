import random

class Chomp:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[True for _ in range(cols)] for _ in range(rows)]

    def valid_move(self, row, col):
        return self.board[row][col]

    def apply_move(self, row, col):
        for r in range(row, self.rows):
            for c in range(col, self.cols):
                self.board[r][c] = False

    def game_finished(self):
        return not self.board[0][0]

    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.game_finished():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.valid_move(row, col):
                        temp_board = [row.copy() for row in self.board]
                        self.apply_move(row, col)
                        eval = self.minimax(depth - 1, False, alpha, beta)
                        self.board = temp_board
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.valid_move(row, col):
                        temp_board = [row.copy() for row in self.board]
                        self.apply_move(row, col)
                        eval = self.minimax(depth - 1, True, alpha, beta)
                        self.board = temp_board
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def evaluate_board(self):
        return random.random()

    def optimal_move(self, depth):
        best_move = None
        best_value = float('-inf')

        for row in range(self.rows):
            for col in range(self.cols):
                if self.valid_move(row, col):
                    temp_board = [row.copy() for row in self.board]
                    self.apply_move(row, col)
                    move_value = self.minimax(depth - 1, False, float('-inf'), float('inf'))
                    self.board = temp_board

                    if move_value > best_value:
                        best_value = move_value
                        best_move = (row, col)

        return best_move