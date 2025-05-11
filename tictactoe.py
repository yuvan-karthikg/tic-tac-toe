import streamlit as st
import math

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner = None

def is_winner(brd, player):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(brd[i] == brd[j] == brd[k] == player for i, j, k in wins)

def is_board_full(brd):
    return ' ' not in brd

def minimax(brd, depth, is_maximizing):
    if is_winner(brd, 'O'):
        return 1
    elif is_winner(brd, 'X'):
        return -1
    elif is_board_full(brd):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = 'O'
                score = minimax(brd, depth+1, False)
                brd[i] = ' '
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = 'X'
                score = minimax(brd, depth+1, True)
                brd[i] = ' '
                best = min(best, score)
        return best

def ai_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if st.session_state.board[i] == ' ':
            st.session_state.board[i] = 'O'
            score = minimax(st.session_state.board, 0, False)
            st.session_state.board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        st.session_state.board[move] = 'O'

def check_game_status():
    if is_winner(st.session_state.board, 'X'):
        st.session_state.game_over = True
        st.session_state.winner = 'You'
    elif is_winner(st.session_state.board, 'O'):
        st.session_state.game_over = True
        st.session_state.winner = 'AI'
    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = 'Draw'

# UI
st.title("🤖 Tic Tac Toe with Minimax AI")
st.write("You are **X**, AI is **O**")

cols = st.columns(3)
for i in range(3):
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            if st.button(st.session_state.board[idx] if st.session_state.board[idx] != ' ' else ' ', key=idx, use_container_width=True, disabled=st.session_state.board[idx] != ' ' or st.session_state.game_over):
                st.session_state.board[idx] = 'X'
                check_game_status()
                if not st.session_state.game_over:
                    ai_move()
                    check_game_status()

# Show status
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.success("It's a draw! 🤝")
    else:
        st.success(f"🎉 {st.session_state.winner} won!")

if st.button("🔁 Restart Game"):
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner = None
