import streamlit as st
import numpy as np

class Gameboard:
    def __init__(self, rows, cols):
        self.board = np.zeros((rows, cols), dtype=int)

    def get_board(self):
        return self.board

    def update_cell(self, row, col, player):
        if self.board[row, col] == 0:
            self.board[row, col] = player

def gameboard(rows, cols, board_state, key):
    board = board_state.get_board()
    cols_in_row = st.columns(cols)  # Create columns for the grid layout

    for i in range(rows):
        with cols_in_row[i]:
            for j in range(cols):
                button_label = ' '  # Default label for empty cells
                if board[i, j] == 1:
                    button_label = 'X'
                elif board[i, j] == 2:
                    button_label = 'O'
                
                if st.button(button_label, key=f'{key}_{i}_{j}'):
                    if board[i, j] == 0 and st.session_state.current_player:
                        board_state.update_cell(i, j, st.session_state.current_player)
                        st.session_state.current_player = 3 - st.session_state.current_player
                        st.session_state.victory = check_win(st.session_state.game.get_board())
                    st.experimental_rerun()

st.title('Tic Tac Toe')

def reset_game():
    st.session_state.victory = 0
    st.session_state.game = Gameboard(3, 3)
    st.session_state.current_player = 1

def initialize():
    if 'game' not in st.session_state:
        reset_game()
    if 'victory' not in st.session_state:
        st.session_state.victory = 0
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 1

def check_win(board):
    for i in range(3):
        if np.all(board[i, :] == 1):
            return 1
        if np.all(board[i, :] == 2):
            return 2
    for j in range(3):
        if np.all(board[:, j] == 1):
            return 1
        if np.all(board[:, j] == 2):
            return 2
    if np.all(np.diag(board) == 1) or np.all(np.diag(np.fliplr(board)) == 1):
        return 1
    if np.all(np.diag(board) == 2) or np.all(np.diag(np.fliplr(board)) == 2):
        return 2
    if np.all(board != 0):
        return -1
    return 0

initialize()

with st.sidebar:
    st.header("Player Settings")
    st.button('Reset game', on_click=reset_game)
    player1 = st.text_input('Player 1', 'Player 1', key='player1')
    color1 = st.color_picker('Player 1 Color', '#3A5683', key='color1')
    alpha1 = st.slider("Player 1 Alpha", 30, 255, 255, key='alpha1')
    player2 = st.text_input('Player 2', 'Player 2', key='player2')
    color2 = st.color_picker('Player 2 Color', '#73956F', key='color2')
    alpha2 = st.slider("Player 2 Alpha", 30, 255, 255, key='alpha2')

    color1 = f'{color1[1:]}{alpha1:02x}'.upper()
    color2 = f'{color2[1:]}{alpha2:02x}'.upper()
    players = {player1: color1, player2: color2}

st.session_state.victory = check_win(st.session_state.game.get_board())

if st.session_state.victory != 0:
    if st.session_state.victory == 1:
        st.success(f'{player1} wins!')
    elif st.session_state.victory == 2:
        st.success(f'{player2} wins!')
    elif st.session_state.victory == -1:
        st.success('It\'s a tie!')

gameboard(3, 3, st.session_state.game, key='game')

