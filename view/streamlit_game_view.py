import streamlit as st
from model.game import Game
from model.player import Player
from model.player_color import color_to_symbol
from view.console_board_view import ConsoleBoardView

class ConsoleGameView():
    def __init__(self, game: Game) -> None:
        self.game = game
        self.board = self.game.board.board
        self.size = self.board.size
        self.board_view = ConsoleBoardView(game.board)

        st.title("Reversi Website: ")

        n = st.number_input("Enter the board size you would like:", min_value=4, value=4, step=2)

        self.create_grid(n)

    def create_grid(self):
        self.col_list = st.columns(self.size)
        for i in range(self.size):
            for j in range(self.size):
                button_id = f'button_{i}_{j}'
                if self.col_list[i].button(label= color_to_symbol[self.board[i][j]], key=button_id, help=f'Row: {i}, Column: {j}'):
                    st.write(f'Button at row {i} and column {j} was clicked!')
