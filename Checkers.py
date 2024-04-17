# THIS IS MY FULL IMPLEMENTATION AGAINST AN (AI), I will submit another file without the (AI) as a .txt file where you can play with both players, that way
# it would be easier to test functionalities like king captures and double captures. (THIS IS WHAT SHOULD BE GRADED)

import tkinter
from tkinter import messagebox

# =============================================================================================================================================
# Board and Pieces size
BOARD_SIZE = 8
SQUARE_SIZE = 100
PIECE_SIZE = 40

# =============================================================================================================================================
# Colors
BEIGE_SQUARE_COLOR = "#d8a35e"
BROWN_SQUARE_COLOR = "#9d5a13"
BLACK_PIECE_COLOR = "#444444"
RED_PIECE_COLOR = "#c90000"

# =============================================================================================================================================
# trackers for the state of the game
selected_piece = None
selected_row = -1
selected_col = -1
board_state = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 'b'  # black plays first, in my game the player is black and the AI is red
highlighted_squares = []
difficulty = None


# =============================================================================================================================================
def draw_board(canvas):  # Function to draw the board using nested loop by visualizing the board as rows and columns 8x8
    global highlighted_squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
            color = BEIGE_SQUARE_COLOR if (row + col) % 2 == 0 else BROWN_SQUARE_COLOR
            if (row, col) in highlighted_squares:
                canvas.create_rectangle(x1, y1, x2, y2, fill="light green",
                                        outline="light green")  # light green color for the highlighted squares
                # showcasing possible moves
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


# =============================================================================================================================================
def draw_pieces(canvas):  # calling the draw_piece function in a loop to draw the pieces of the board
    pieces_with_moves = find_pieces_with_moves(current_player) if current_player == 'b' else []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board_state[row][col]
            if piece in ['r', 'R']:  # Red pieces, no special outline as it will be the AI
                draw_piece(canvas, row, col, RED_PIECE_COLOR, "black")
            elif piece in ['b', 'B']:  # Black pieces, will have golden outline to show the player what pieces can be
                # moved
                outline_color = "gold" if (row, col) in pieces_with_moves else "black"
                draw_piece(canvas, row, col, BLACK_PIECE_COLOR, outline_color)


# =============================================================================================================================================
def draw_piece(canvas, row, col, color, outline_color):  # Function to draw the individual piece
    # Calculate the center of the square
    cx = col * SQUARE_SIZE + SQUARE_SIZE // 2
    cy = row * SQUARE_SIZE + SQUARE_SIZE // 2
    # Draw the piece
    canvas.create_oval(cx - PIECE_SIZE, cy - PIECE_SIZE, cx + PIECE_SIZE, cy + PIECE_SIZE, fill=color,
                       outline=outline_color)
    # Check if it's a king piece by checking if the character in board_state is uppercase
    piece = board_state[row][col]
    if piece.isupper():  # This means it's a king
        # Draw a crown on the piece
        # Crown dimensions
        crown_width = PIECE_SIZE // 2
        crown_height = PIECE_SIZE // 3
        # Crown spikes
        spike_length = crown_height // 2

        # Base of the crown
        base_y = cy - PIECE_SIZE // 2
        canvas.create_rectangle(cx - crown_width // 2, base_y - crown_height,
                                cx + crown_width // 2, base_y, fill="yellow", outline="black")

        # Crown spikes - drawing 3 spikes
        for i in range(3):
            spike_x = cx - crown_width // 2 + (crown_width // 3) * i
            canvas.create_polygon([spike_x, base_y - crown_height,
                                   spike_x + crown_width // 6, base_y - crown_height - spike_length,
                                   spike_x + crown_width // 3, base_y - crown_height],
                                  fill="yellow", outline="black")


# =============================================================================================================================================
def find_pieces_with_moves(player):  # finds the pieces that have available, moves keep in mind this uses the function
    # get_possible_moves_for_piece which is the main function for moves but this one is used for the redraws
    pieces_with_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board_state[row][col].lower()
            if piece == player and (
                    get_possible_moves_for_piece(row, col, player) or can_capture_from_position(row, col, player)):
                pieces_with_moves.append((row, col))
    return pieces_with_moves


# =============================================================================================================================================
def check_all_captured(player):  # if all pieces are captured ends the game
    opponent = 'r' if player == 'b' else 'b'
    for row in board_state:
        if opponent in ''.join(row).lower():
            return False
    return True


# =============================================================================================================================================
def refresh_board(canvas):  # redraw the board
    draw_board(canvas)
    draw_pieces(canvas)


# =============================================================================================================================================
def switch_player():  # switch between red(AI) and black(Player)
    global current_player
    current_player = 'r' if current_player == 'b' else 'b'


# =============================================================================================================================================
def can_capture(player):  # checks if the piece is in a position to capture another piece
    captures = {}
    opponent = 'r' if player == 'b' else 'b'
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board_state[row][col]
            if piece.lower() == player:  # Check if it's the current player's piece
                # Determine the capture directions based on the piece type
                directions = [-1, 1] if piece.isupper() else ([1] if player == 'r' else [-1])
                for d_row in directions:
                    for d_col in [-1, 1]:  # Check diagonally in both directions
                        end_row = row + 2 * d_row
                        end_col = col + 2 * d_col
                        mid_row = row + d_row
                        mid_col = col + d_col
                        if (0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE and
                                board_state[end_row][end_col] == '' and
                                board_state[mid_row][mid_col].lower() == opponent):
                            if (row, col) not in captures:
                                captures[(row, col)] = []
                            captures[(row, col)].append((end_row, end_col))
    return len(captures) > 0, captures


# =============================================================================================================================================
def is_valid_move(start_row, start_col, end_row, end_col, player):  # validation for the allowed movements
    piece = board_state[start_row][start_col]
    must_capture, captures = can_capture(player)
    if must_capture:
        if (start_row, start_col) in captures and (end_row, end_col) in captures[(start_row, start_col)]:
            return True
        else:
            return False
    # Determine direction of movement based on player and if it's a king
    is_king = piece.isupper()

    # Target square must be empty
    if board_state[end_row][end_col] != '':
        return False

    # For kings, check for valid move in any direction
    if is_king:
        # Kings can move diagonally in any direction by one square
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
            return True
        # Kings capturing move
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            opponent = 'r' if player.lower() == 'b' else 'b'
            if board_state[mid_row][mid_col].lower() == opponent:
                return True
    else:
        # Normal piece movement
        direction = 1 if player == 'r' else -1
        # Normal move
        if (end_row - start_row == direction) and abs(end_col - start_col) == 1:
            return True
        # Capturing move
        if (end_row - start_row == 2 * direction) and abs(end_col - start_col) == 2:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            opponent = 'r' if player.lower() == 'b' else 'b'
            if board_state[mid_row][mid_col].lower() == opponent:
                return True

    return False


# =============================================================================================================================================
def perform_move(start_row, start_col, end_row, end_col, player, track_changes=False):  # how the pieces execute
    # movements
    # Calculate the middle square for captures
    move_details = {
        'captured': False,
        'captured_pos': None,
        'promoted': False,
        'start_pos': (start_row, start_col),
        'end_pos': (end_row, end_col),
        'piece': board_state[start_row][start_col],
    }
    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2
    # Preserve the piece type, checking if it's a king
    piece_type = board_state[start_row][start_col]
    # If it's a capture move, check if the captured piece is a king
    capture_made = False
    if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
        captured_piece = board_state[mid_row][mid_col]
        board_state[mid_row][mid_col] = ''
        capture_made = True
        move_details['captured'] = True
        move_details['captured_pos'] = (mid_row, mid_col)
        move_details['captured_piece'] = captured_piece
        # If the captured piece is a king, promote the capturing piece to a king
        if captured_piece.isupper():
            piece_type = player.upper()
    # Move the selected piece to the new square, using the potentially updated piece type (regular or king)
    board_state[start_row][start_col] = ''
    board_state[end_row][end_col] = piece_type
    # Check for promotion to king (only if it's not already a king)
    # This check now only applies if the piece moves to the far row without capturing a king
    if not piece_type.isupper():  # Only check for promotion if it's not already a king
        if (player == 'r' and end_row == BOARD_SIZE - 1) or \
                (player == 'b' and end_row == 0):
            board_state[end_row][end_col] = player.upper()

    if track_changes:
        return capture_made, move_details
    return capture_made


# =============================================================================================================================================
def can_capture_from_position(row, col, player):  # function for multiple captures if permitted
    captures = []
    piece = board_state[row][col]
    opponent = 'r' if player == 'b' else 'b'
    # Adjust directions based on whether the piece is a king or not
    directions = [-1, 1] if piece.isupper() else ([1] if player == 'r' else [-1])

    for d_row in directions:
        for d_col in [-1, 1]:  # Check diagonally in both directions
            end_row = row + 2 * d_row
            end_col = col + 2 * d_col
            mid_row = row + d_row
            mid_col = col + d_col
            if (0 <= end_row < BOARD_SIZE and 0 <= end_col < BOARD_SIZE and
                    board_state[end_row][end_col] == '' and
                    board_state[mid_row][mid_col].lower() == opponent):
                captures.append((end_row, end_col))
    return captures


# =============================================================================================================================================

def get_possible_moves_for_piece(row, col, player):  # main moves function
    possible_moves = []
    piece = board_state[row][col]
    # First, check for capture moves
    possible_moves.extend(can_capture_from_position(row, col, player))

    # Adjust directions for regular moves based on whether the piece is a king
    directions = [-1, 1] if piece.isupper() or player == 'r' else [1] if player == 'r' else [-1]

    for d_row in directions:
        for d_col in [-1, 1]:
            move_row, move_col = row + d_row, col + d_col
            if 0 <= move_row < BOARD_SIZE and 0 <= move_col < BOARD_SIZE and board_state[move_row][move_col] == '':
                if is_valid_move(row, col, move_row, move_col, player):
                    possible_moves.append((move_row, move_col))

    return possible_moves


# =============================================================================================================================================
def square_clicked(event, canvas):  # most important function in terms of playability, here is where rules like
    # mandatory captures are implemented
    global selected_piece, selected_row, selected_col, current_player, highlighted_squares
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE
    highlighted_squares = []

    # Check for any mandatory captures
    must_capture, captures = can_capture(current_player)
    clicked_piece = board_state[row][col].lower()
    if clicked_piece == current_player:
        # If a piece is already selected, and it's the same player's piece, switch selection
        if selected_piece and (row, col) != (selected_row, selected_col):
            selected_piece = board_state[row][col]
            selected_row = row
            selected_col = col
            # Get all possible moves for the newly selected piece
            if (current_player == 'b' or current_player == 'B'):
                highlighted_squares = get_possible_moves_for_piece(row, col, current_player)
        elif not selected_piece:
            # If no piece is selected yet, select the clicked piece
            selected_piece = board_state[row][col]
            selected_row = row
            selected_col = col
            if (current_player == 'b' or current_player == 'B'):
                highlighted_squares = get_possible_moves_for_piece(row, col, current_player)
        else:
            # Deselect if the same piece is clicked again
            selected_piece = None
            selected_row = -1
            selected_col = -1
    else:

        if must_capture:
            if (row, col) in captures.keys():
                # The player has selected a piece that must capture
                selected_piece = current_player
                selected_row = row
                selected_col = col
                if (current_player == 'b' or current_player == 'B'):
                    highlighted_squares = captures[(row, col)]
            elif selected_piece and (selected_row, selected_col) in captures:
                # Check if the move is a valid capture move
                if (row, col) in captures[(selected_row, selected_col)]:
                    capture_made = perform_move(selected_row, selected_col, row, col, current_player,
                                                track_changes=True)
                    refresh_board(canvas)
                    if capture_made:
                        # After a successful capture, check if the piece can capture again
                        additional_captures = can_capture_from_position(row, col, current_player)
                        if additional_captures:
                            # If additional captures are possible, update selected_row and selected_col
                            # but do NOT switch players
                            selected_row, selected_col = row, col
                            if (current_player == 'b' or current_player == 'B'):
                                highlighted_squares = additional_captures
                        else:
                            # If no additional captures are possible, end the turn
                            selected_piece = None
                            switch_player()
                            refresh_board(canvas)
                    else:
                        # If the move was not a capture, deselect the piece
                        selected_piece = None
                else:
                    # If the selected move is not a valid capture, deselect the piece
                    selected_piece = None
        else:
            # If there are no mandatory captures, proceed with the normal move process
            if selected_piece and current_player == selected_piece.lower():
                # Check if the move is valid
                if is_valid_move(selected_row, selected_col, row, col, current_player):
                    perform_move(selected_row, selected_col, row, col, current_player, track_changes=True)
                    selected_piece = None
                    highlighted_squares = []
                    refresh_board(canvas)
                    switch_player()  # Switch the turn to the other player
                else:
                    # Invalid move, deselect the piece
                    selected_piece = None
            elif board_state[row][col].lower() == current_player and not selected_piece:
                # Select the piece if it's the player's turn and no piece is currently selected
                selected_piece = board_state[row][col]
                selected_row = row
                selected_col = col
                if (current_player == 'b' or current_player == 'B'):
                    highlighted_squares = get_possible_moves_for_piece(row, col, current_player)
    refresh_board(canvas)
    if get_possible_moves_for_piece(row, col, current_player) == None:
        messagebox.showinfo("No more available moves")
    elif check_all_captured('b' if current_player == 'r' else 'r'):
        messagebox.showinfo("Game Over",
                            f"All pieces are captured.GAME OVER")
    else:
        if current_player == 'r':
            canvas.after(1000, lambda: ai_move(canvas))


# =============================================================================================================================================
def evaluate_board():  # evaluation function for the minimax algorithm
    red_score = 0
    black_score = 0
    for row in board_state:
        for piece in row:
            if piece == 'r':
                red_score += 1
            elif piece == 'R':
                red_score += 2  # Kings are more valuable
            elif piece == 'b':
                black_score += 1
            elif piece == 'B':
                black_score += 2
    return red_score - black_score  # Positive if red is winning, negative if black is winning


# =============================================================================================================================================
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):  # minimax using alpha-beta pruning
    if depth == 0 or check_all_captured('r') or check_all_captured('b'):
        return evaluate_board(), None  # evaluate the state of the board

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col].lower() == 'r':  # Find all moves for red pieces
                    possible_moves = get_possible_moves_for_piece(row, col, 'r')
                    for move in possible_moves:
                        capture_made, move_details = perform_move(row, col, move[0], move[1], 'r', track_changes=True)
                        eval, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                        undo_move(move_details)  # undo move after evaluation to get the best move(not in actual game but in search space)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (row, col, move[0], move[1])
                        alpha = max(alpha, eval)  # pruning
                        if beta <= alpha:
                            break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col].lower() == 'b':  # Find all moves for black pieces
                    possible_moves = get_possible_moves_for_piece(row, col, 'b')
                    for move in possible_moves:
                        capture_made, move_details = perform_move(row, col, move[0], move[1], 'r', track_changes=True)
                        eval, _ = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                        undo_move(move_details)
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (row, col, move[0], move[1])
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
        return min_eval, best_move


# =============================================================================================================================================
def undo_move(move_details):  # undo move until the best outcome is achieved
    # Move the piece back to its original position
    board_state[move_details['start_pos'][0]][move_details['start_pos'][1]] = move_details['piece']
    board_state[move_details['end_pos'][0]][move_details['end_pos'][1]] = ''

    if move_details['captured']:
        # Restore the captured piece
        captured_pos = move_details['captured_pos']

        board_state[captured_pos[0]][captured_pos[1]] = move_details['captured_piece']  # Restore the exact piece

    if move_details['promoted']:
        # If the piece was promoted during the move, demote it back
        board_state[move_details['start_pos'][0]][move_details['start_pos'][1]] = move_details['piece'].lower()


# =============================================================================================================================================
def ai_move(canvas):  # how the AI does its move (red player is AI in my game)
    global current_player
    if current_player != 'r':
        return  # Ensure it's red's turn to move

    def make_ai_move(row, col, depth=difficulty):
        # Find the best move using minimax
        _, best_move = minimax_alpha_beta(board_state, depth, float('-inf'), float('inf'), True)
        if best_move:
            start_row, start_col, end_row, end_col = best_move
            capture_made, move_details = perform_move(start_row, start_col, end_row, end_col, 'r', track_changes=True)
            refresh_board(canvas)

            if capture_made:
                additional_captures = can_capture_from_position(end_row, end_col, 'r')
                if additional_captures:
                    # Continue making captures if additional captures are available
                    canvas.after(1000, lambda: make_ai_move(end_row, end_col, depth + 1))
                else:
                    # If no additional captures, switch player
                    switch_player()
            else:
                # If the move was not a capture, switch player
                switch_player()
            refresh_board(canvas)

    make_ai_move(0, 0)  # Initial call to start AI move process


# =============================================================================================================================================
def main():
    pop = tkinter.Tk()
    pop.title("Checkers")
    canvas = tkinter.Canvas(pop, width=SQUARE_SIZE * BOARD_SIZE, height=SQUARE_SIZE * BOARD_SIZE, bg="black")
    canvas.pack()
    initialize_board()
    refresh_board(canvas)
    canvas.bind("<Button-1>", lambda event: square_clicked(event, canvas))  # how pieces are moved
    pop.mainloop()


# =============================================================================================================================================
def initialize_board():
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 != 0:
                board_state[row][col] = 'r'  # Lowercase for regular pieces, king otherwise

    for row in range(5, BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 != 0:
                board_state[row][col] = 'b'


# =============================================================================================================================================
def assign_difficulty(x):  # what the difficulty should be based on the user's input, difficulty=depth in minimax,
    #   keep in mind the higher the difficulty (depth) means more computation, which could make the game slow or even crash
    global difficulty
    if (x == 'EASY'):
        difficulty = 2
    if (x == 'INTERMEDIATE'):
        difficulty = 4
    if (x == 'HARD'):
        difficulty = 7
    if (x == 'EXPERT'):
        difficulty = 10


# =============================================================================================================================================
if __name__ == "__main__":
    x = str(input("Please Enter the difficulty you would like EASY/INTERMEDIATE/HARD/EXPERT\n"))
    assign_difficulty(x.upper())
    main()
