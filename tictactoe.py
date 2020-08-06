import copy

# create the board
gameBoard = {7: ' ' , 8: ' ' , 9: ' ' ,
         4: ' ' , 5: ' ' , 6: ' ' ,
         1: ' ' , 2: ' ' , 3: ' ' }

# lists for the possible moves, corner and middle square positions
possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
corners = {1:9, 3:7, 7:3, 9:1}
middle_squares = [2, 4, 6, 8]

def print_board(board):
    """ prints the board in a more readable format """
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])

def switch_turn(turn):
    """ switches the turn from X to O and viceverse """
    return "X" if turn == "O" else "O"

def board_copy(board):
    """ gets a copy of the board by value  """
    return copy.deepcopy(board)

def is_available(move):
    """ checks if a given move is allowed """
    if gameBoard[move] == " ":
        return True
    return False

def check_if_won(left, mid, right, board):
    """ checks if someone won """
    if board[left] == board[mid] == board[right] != " ":
                return True
    else:
        return False

def check_all_combinations(board):
    """ helper method that checks all the combinations possible for a win """
    return (check_if_won(7, 8, 9, board) or check_if_won(4, 5, 6, board)
        or check_if_won(1, 2, 3, board) or check_if_won(1, 4, 7, board)
        or check_if_won(2, 5, 8, board) or check_if_won(3, 6, 9, board)
        or check_if_won(7, 5, 3, board) or check_if_won(1, 5, 9, board))

def winning_move(board, turn):
    """ checks which moves will result in a win and returns a list with them """
    copy = board_copy(board)
    winning_moves = [0]

    # loop through all possible moves
    for move in possible_moves:
        # check it's available first
        if is_available(move):
            copy[move] = turn
            # check if it'll result in a win
            if check_all_combinations(copy):
                winning_moves.append(move)
            copy[move] = " "
    return winning_moves

def blocking_move(board, turn):
    """ checks if a possible move will block the opponent from winning """
    turn = switch_turn(turn)

    copy = board_copy(board)
    blocking_moves = [0]
    for move in possible_moves:
        if is_available(move):
            copy[move] = turn

            if check_all_combinations(copy):
                blocking_moves.append(move)
            copy[move] = " "
    return blocking_moves

def check_fork(board, turn):
    """ checks if a move will result in a fork (two possible winning moves) """
    copy = board_copy(board)
    fork_moves = [0]
    for move in possible_moves:
        if is_available(move):
            copy[move] = turn
            if len(winning_move(copy, turn)) > 2:
                fork_moves.append(move)
            copy[move] = ' '
    return fork_moves

def block_fork(board, turn):
    """ checks if a move will stop the opponent from making a fork
    uses the helper method above after switching the turn """
    turn = switch_turn(turn)
    return check_fork(board, turn)

def check_opposite_corners(board, turn):
    """ checks if the opposite corners of the opponent are empty """
    turn = switch_turn(turn)
    moves = [0]
    for corner in corners.keys():
        if board[corner] == turn and corners[corner] == ' ':
            moves.append(corners[corner])
    return moves

def check_empty(board, filters):
    """ checks if the corners or middle squares are empty based on the parameter """
    moves = [0]
    for filter in filters:
        if board[filter] == ' ':
            moves.append(filter)
    return moves

def getTurn():
    turn = input("Would you like to be X or O? ")
    while turn.upper() not in ["X", "O"]:
        turn = input("Please enter one of the two options. X, O ")
    return turn.upper()

def getFirst():
    choice = input("Would you like to play first? (y/n) ")
    if choice.lower() == "y":
        return True
    else:
        return False

def game():
    """ starts the game """
    playerTurn = getTurn()
    if getFirst():
        turn = playerTurn
    else:
        turn = switch_turn(playerTurn)
    count = 0

    for i in range(9):
        print_board(gameBoard)
        print("It's your turn: " + turn)


        if turn == playerTurn:
            move = int(input("What move would you like to do? "))
            while not is_available(move):
                move = int(input("Please enter a valid move: "))

            gameBoard[move] = turn
            count += 1
        else:
            # check all possible scenarios for computer move and pick the best one
            if winning_move(gameBoard, turn).pop() != 0:
                gameBoard[winning_move(gameBoard, turn).pop()] = turn
            elif blocking_move(gameBoard, turn).pop() != 0:
                gameBoard[blocking_move(gameBoard, turn).pop()] = turn
            elif check_fork(gameBoard, turn).pop() != 0:
                gameBoard[check_fork(gameBoard, turn).pop()] = turn
            elif block_fork(gameBoard, turn).pop() != 0:
                gameBoard[block_fork(gameBoard, turn).pop()] = turn
            elif gameBoard[5] == ' ':
                gameBoard[5] = turn
            elif check_opposite_corners(gameBoard, turn).pop() != 0:
                gameBoard[check_opposite_corners(gameBoard, turn).pop()] = turn
            elif check_empty(gameBoard, corners).pop() != 0:
                gameBoard[check_empty(gameBoard, corners).pop()] = turn
            elif check_empty(gameBoard, middle_squares).pop() != 0:
                gameBoard[check_empty(gameBoard, middle_squares).pop()] = turn
            count += 1

        # check if someone won already
        if count >= 5:
            if check_all_combinations(gameBoard):
                print_board(gameBoard)
                print("Game Over!")
                print(turn + " won!")
                break
        # check if game is over
        if count == 9:
            print("Game Over!")
            print("It's a tie!")

        # switch turns for the next turn
        turn = switch_turn(turn)

    # ask if user wants to play again
    play_again = input("Do you want to play again? (y/n) ")

    if play_again.lower() == 'y':
        for key in gameBoard:
            gameBoard[key] = " "
        game()

if __name__ == "__main__":
    game()
