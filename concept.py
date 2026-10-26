
import tkinter as tk
from tkinter import messagebox
import math

HUMAN = "X"
AI = "O"

board = [""] * 9
human_wins = 0
ai_wins = 0
draws = 0
game_over = False

def check_winner(b):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, c, d in wins:
        if b[a] == b[c] == b[d] != "":
            return b[a]

    if "" not in b:
        return "Draw"

    return None


def minimax(b, is_ai):
    result = check_winner(b)

    if result == AI:
        return 1
    if result == HUMAN:
        return -1
    if result == "Draw":
        return 0

    if is_ai:
        best_score = -math.inf
        for i in range(9):
            if b[i] == "":
                b[i] = AI
                score = minimax(b, False)
                b[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == "":
                b[i] = HUMAN
                score = minimax(b, True)
                b[i] = ""
                best_score = min(best_score, score)
        return best_score


def finish_game():
    global human_wins, ai_wins, draws, game_over

    result = check_winner(board)

    if result is None:
        return False

    game_over = True

    if result == HUMAN:
        human_wins += 1
        status.config(text="You win!")
    elif result == AI:
        ai_wins += 1
        status.config(text="AI wins!")
    else:
        draws += 1
        status.config(text="It's a draw!")

    score.config(
        text=f"You: {human_wins}   AI: {ai_wins}   Draws: {draws}"
    )
    return True


def ai_move():
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = AI
            score_value = minimax(board, False)
            board[i] = ""

            if score_value > best_score:
                best_score = score_value
                best_move = i

    if best_move is not None:
        board[best_move] = AI
        buttons[best_move].config(text=AI, state="disabled")

    finish_game()


def player_move(i):
    if board[i] != "" or game_over:
        return

    board[i] = HUMAN
    buttons[i].config(text=HUMAN, state="disabled")

    if finish_game():
        return

    ai_move()


def restart():
    global board, game_over

    board = [""] * 9
    game_over = False
    status.config(text="Your turn (X)")

    for button in buttons:
        button.config(text="", state="normal")


root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("350x440")
root.resizable(False, False)

tk.Label(
    root, text="Tic-Tac-Toe AI",
    font=("Arial", 20, "bold")
).pack(pady=10)

status = tk.Label(root, text="Your turn (X)", font=("Arial", 12))
status.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

buttons = []

for i in range(9):
    button = tk.Button(
        frame,
        text="",
        font=("Arial", 24, "bold"),
        width=4,
        height=2,
        command=lambda i=i: player_move(i)
    )
    button.grid(row=i // 3, column=i % 3, padx=3, pady=3)
    buttons.append(button)

score = tk.Label(
    root, text="You: 0   AI: 0   Draws: 0",
    font=("Arial", 11)
)
score.pack(pady=10)

tk.Button(
    root, text="Restart Game",
    font=("Arial", 11),
    command=restart
).pack(pady=5)

root.mainloop()
