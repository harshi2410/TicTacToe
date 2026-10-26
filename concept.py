
import tkinter as tk

board = [""] * 9
game_over = False

def winner():
    lines = [(0,1,2), (3,4,5), (6,7,8),
             (0,3,6), (1,4,7), (2,5,8),
             (0,4,8), (2,4,6)]

    for a, b, c in lines:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def minimax(is_ai):
    result = winner()

    if result == "O":
        return 1
    if result == "X":
        return -1
    if result == "Draw":
        return 0

    scores = []

    for i in range(9):
        if board[i] == "":
            board[i] = "O" if is_ai else "X"
            scores.append((minimax(not is_ai), i))
            board[i] = ""

    if is_ai:
        return max(scores)[0]
    return min(scores)[0]


def ai_move():
    best_score = -999
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        play(move, "O")


def play(i, symbol):
    global game_over

    board[i] = symbol
    buttons[i].config(text=symbol, state="disabled")

    result = winner()

    if result:
        game_over = True
        status.config(text="It's a draw!" if result == "Draw"
                      else result + " wins!")
        return

    if symbol == "X":
        ai_move()


def click(i):
    if not game_over and board[i] == "":
        play(i, "X")


def replay():
    global board, game_over

    board = [""] * 9
    game_over = False
    status.config(text="Your turn (X)")

    for button in buttons:
        button.config(text="", state="normal")


root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("300x390")

status = tk.Label(root, text="Your turn (X)", font=("Arial", 14))
status.pack(pady=10)

buttons = []

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    b = tk.Button(frame, text="", width=5, height=2,
                  font=("Arial", 20),
                  command=lambda i=i: click(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

tk.Button(root, text="Replay", command=replay,
          font=("Arial", 12)).pack(pady=15)

root.mainloop()
