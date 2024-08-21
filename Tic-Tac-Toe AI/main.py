import math


# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)


# Function to check if there's a winner
def check_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


# Function to check if the board is full
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)


# Minimax algorithm with optional Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    # Base cases
    if check_winner(board, 'O'):  # AI wins
        return 10 - depth
    if check_winner(board, 'X'):  # Human wins
        return depth - 10
    if is_full(board):  # Draw
        return 0

    # Maximizing player (AI)
    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    # Minimizing player (Human)
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval


# Function to find the best move for the AI
def find_best_move(board):
    best_move = None
    best_value = -math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_value = minimax(board, 0, False)
                board[i][j] = ' '
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
    return best_move


# Main function to play the game
def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    human_turn = True

    while True:
        print_board(board)

        if human_turn:
            # Human player's move
            move = input("Enter your move (row and column from 1-3, e.g., '1 2'): ").split()
            row, col = int(move[0]) - 1, int(move[1]) - 1
            if board[row][col] != ' ':
                print("Invalid move, try again.")
                continue
            board[row][col] = 'X'
        else:
            # AI's move
            print("AI is making a move...")
            row, col = find_best_move(board)
            board[row][col] = 'O'

        # Check for a winner or a draw
        if check_winner(board, 'X'):
            print_board(board)
            print("Congratulations! You win!")
            break
        elif check_winner(board, 'O'):
            print_board(board)
            print("AI wins! Better luck next time.")
            break
        elif is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch turns
        human_turn = not human_turn


if __name__ == "__main__":
    play_game()
