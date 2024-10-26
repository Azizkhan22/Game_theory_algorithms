import math

# Initialize the board with None representing empty cells
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

# Determines the current player's turn based on counts of X's and O's on the board
def player_turn(board):
    # Flatten the board to count occurrences of 'X' and 'O'
    flat_board = [cell for row in board for cell in row]
    x_count = flat_board.count('X')
    o_count = flat_board.count('O')
    return 'O' if x_count > o_count else 'X'
    
# Returns a list of available actions (empty cells) on the board
def Actions(board):
    actions = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col is None:
                actions.append((i, j))
    return actions

# Checks if the specified player has won
def winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):  # Row win
            return True
        if all([board[j][i] == player for j in range(3)]):  # Column win
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# Checks if the game is a draw
def draw(board):
    if winner(board, 'X') or winner(board, 'O'):
        return False
    # Flatten board to check if any cells are empty
    flat_board = [cell for row in board for cell in row]
    return all(cell is not None for cell in flat_board)

# Checks if the game is over (terminal state)
def terminal(board):
    return winner(board, 'X') or winner(board, 'O') or draw(board)

# Evaluates the board: +1 for X win, -1 for O win, 0 for draw
def evaluate(board):
    if winner(board, 'X'):
        return 1
    elif winner(board, 'O'):
        return -1
    else:
        return 0

# Minimax maximizer function
def max_value(board):
    if terminal(board):
        return evaluate(board)
    
    v = -math.inf
    for action in Actions(board):
        i, j = action
        board[i][j] = 'X'  # X is the maximizer
        v = max(v, min_value(board))
        board[i][j] = None  # Undo move
    return v

# Minimax minimizer function
def min_value(board):
    if terminal(board):
        return evaluate(board)
    
    v = math.inf
    for action in Actions(board):
        i, j = action
        board[i][j] = 'O'  # O is the minimizer
        v = min(v, max_value(board))
        board[i][j] = None  # Undo move
    return v

# Function to get the best move for the current player using Minimax
def minimax(board):
    current_player = player_turn(board)
    best_action = None
    
    if current_player == 'X':
        best_value = -math.inf
        for action in Actions(board):
            i, j = action
            board[i][j] = 'X'
            move_value = min_value(board)
            board[i][j] = None
            if move_value > best_value:
                best_value = move_value
                best_action = action
    else:
        best_value = math.inf
        for action in Actions(board):
            i, j = action
            board[i][j] = 'O'
            move_value = max_value(board)
            board[i][j] = None
            if move_value < best_value:
                best_value = move_value
                best_action = action
    
    return best_action

# Function to print the current state of the board
def print_board(board):
    for row in board:
        print([cell if cell is not None else '-' for cell in row])
    print()

# Main function to play the game
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'O' and the computer is 'X'.")
    print_board(board)

    while not terminal(board):
        # Player's turn
        if player_turn(board) == 'O':
            print("Your turn! Enter row and column (0, 1, or 2).")
            row = int(input("Row: "))
            col = int(input("Col: "))
            if board[row][col] is None:
                board[row][col] = 'O'
            else:
                print("Cell is already occupied! Try again.")
                continue
        # Computer's turn
        else:
            print("Computer's turn:")
            action = minimax(board)
            if action:
                i, j = action
                board[i][j] = 'X'

        print_board(board)

        # Check for a winner after each move
        if winner(board, 'O'):
            print("Congratulations! You win!")
            return
        elif winner(board, 'X'):
            print("Computer wins!")
            return

    if draw(board):
        print("It's a draw!")

# Run the game
play_game()
