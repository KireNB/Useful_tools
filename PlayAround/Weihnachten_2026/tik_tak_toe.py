import math

PLAYER = "X"
AI = "O"

board = [" " for _ in range(9)]


def print_board():
    print()
    for i in range(3):
        row = board[i * 3:(i + 1) * 3]
        print(" | ".join(row))
        if i < 2:
            print("---------")
    print()


def print_positions():
    print("\nPositionen:")
    for i in range(3):
        row = [str(i * 3 + j + 1) for j in range(3)]
        print(" | ".join(row))
        if i < 2:
            print("---------")
    print()


def is_winner(b, player):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(all(b[i] == player for i in combo) for combo in win_combinations)


def is_draw(b):
    return " " not in b


def minimax(b, depth, is_maximizing):
    if is_winner(b, AI):
        return 1
    if is_winner(b, PLAYER):
        return -1
    if is_draw(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = AI
                score = minimax(b, depth + 1, False)
                b[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = PLAYER
                score = minimax(b, depth + 1, True)
                b[i] = " "
                best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    board[move] = AI


def player_move():
    while True:
        try:
            pos = int(input("Dein Zug (1-9): ")) - 1
            if pos < 0 or pos > 8 or board[pos] != " ":
                print("Ungültiger Zug, versuch es erneut.")
            else:
                board[pos] = PLAYER
                break
        except ValueError:
            print("Bitte eine Zahl von 1 bis 9 eingeben.")


def game():
    print("🎮 Tic-Tac-Toe")
    print("Du bist X, Computer ist O")
    print_positions()

    while True:
        print_board()
        player_move()

        if is_winner(board, PLAYER):
            print_board()
            print("🎉 Du hast gewonnen!")
            break
        if is_draw(board):
            print_board()
            print("🤝 Unentschieden!")
            break

        ai_move()

        if is_winner(board, AI):
            print_board()
            print("💻 Computer gewinnt!")
            break
        if is_draw(board):
            print_board()
            print("🤝 Unentschieden!")
            break


if __name__ == "__main__":
    game()
