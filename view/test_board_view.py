import tkinter as tk
from tkinter import messagebox
from model.game import Game
from model.player import Player
from model.player_color import color_to_symbol

class BoardView():
    def __init__(self, game: Game):
        self.game = game
        self.size = self.game.size
        self.root = tk.Tk()
        self.root.title("Reversi")
        self.current_player_label = tk.Label(self.root, text=f"Current Player: {color_to_symbol[self.game.get_current_player_color()]}")
        self.current_player_label.grid(row=self.size, columnspan=self.size)
        self.current_moves = tk.Label(self.root, text = "test")
        self.current_moves.grid(row = self.size + 1, columnspan = self.size)
        self.pass_button = tk.Button(self.root, text = "Pass", width = 2, height = 1, command = lambda: self.make_move("p", None))
        self.pass_button.grid(row = self.size, column = self.size+1)
        self.buttons = [[None for i in range(game.size)] for i in range(game.size)]
        self.create_board_buttons()
        self.display_board()

    def create_board_buttons(self):
        for row in range(self.size):
            for col in range(self.size):
                self.buttons[row][col] = tk.Button(self.root, text="", width=2, height=1,
                                                    command=lambda r=row, c=col: self.make_move(r,c))
                self.buttons[row][col].grid(row=row, column=col)

    def make_move(self, row, col):
        if row == "p":
            self.game.swap_turns()
        else:
            t = self.game.make_move(row,col)
            if not t:
                self.display_illegal_move_message()
        self.update_current_player()
        self.display_board()
        self.end_game()

    def end_game(self):
        if self.game.game_over():
            tk.messagebox.showinfo(title = None, message = "Game Over!")
            self.root.destroy()

    def update_current_player(self):
        self.current_player_label.config(text=f"Current Player: {color_to_symbol[self.game.get_current_player_color()]}")

    def display_illegal_move_message(self):
        tk.messagebox.showinfo(title = None, message = "Illegal Move. Try Again")

    def display_winner(self, winner: Player):
        tk.messagebox.showinfo(title = None, message = f"Player {color_to_symbol[winner.get_color()]} won!")

    def display_draw_message(self):
        tk.messagebox.showinfo(title = None, message = 'Game has ended in a draw.')

    def display_legal_moves(self):
        moves = self.game.find_legal_moves()

        if not moves:
            self.current_moves.config(text = "No legal moves available :(")
            self.game.swap_turns()
            self.update_current_player()
            return

        s = ""
        for move in moves:
            row, col = move
            s += (f'{row}, {col} \n')
        self.current_moves.config(text = "Current Legal Moves (row, col):\n" + s)

    def display_board(self):
        for row in range(self.size):
            for col in range(self.size):
                cell_state = color_to_symbol[self.game.board.get_board()[row][col]]
                self.buttons[row][col].config(text=str(cell_state))
        self.display_legal_moves()
