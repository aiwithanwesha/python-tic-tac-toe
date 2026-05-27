from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

# ==========================================
# Project: Tic-Tac-Toe Game
# Developer: Anwesha Santra
# Created On: 24 May 2026
# Last Updated: 27 May 2026
# ==========================================

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("TIC-TAC-TOE GAME ")
        #self.root.title("Made by ANWESHA SANTRA")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e24")
        #self.root.iconbitmap("icon.ico")

        # Game Variables
        self.current_player = "X"
        self.count = 0
        self.scores = {"X": 0, "O": 0}
        self.board_state = [""] * 9
        self.game_mode = "🤖 vs Computer (AI)"

        self.color_x = "#00f0ff"    
        self.color_o = "#ff007f"    
        self.color_btn = "#2a2a35"

        # Create GUI Components
        self.create_mode_selector() 
        self.create_score_board()
        self.create_grid()
        self.create_restart_button()

    def create_mode_selector(self):
        self.mode_frame = Frame(self.root, bg="#1e1e24", pady=5)
        self.mode_frame.pack(fill="x")

        title_lbl = Label(self.mode_frame, text="✨ Developed by Anwesha Santra ✨", font=('Arial', 10, 'italic', 'bold'), fg="#00f0ff", bg="#1e1e24", pady=5)
        title_lbl.pack(anchor="center")

        lbl = Label(self.mode_frame, text="Game Mode:", font=('Arial', 10, 'bold'), fg="white", bg="#1e1e24")
        lbl.pack(side="left", padx=(15, 5))

        self.mode_box = ttk.Combobox(self.mode_frame, values=["🤖 vs Computer (AI)", "👥 Local 2 Players"], state="readonly", width=28)
        self.mode_box.pack(side="left", padx=(0, 15))
        self.mode_box.set(self.game_mode)
        #self.mode_box.pack(side="left")
        self.mode_box.bind("<<ComboboxSelected>>", self.on_mode_change)

    def on_mode_change(self, event):
        self.game_mode = self.mode_box.get()
        self.scores = {"X": 0, "O": 0}
        self.update_scores()
        self.reset()
    
    def create_score_board(self):

        self.score_frame = Frame(self.root, bg="#1e1e24", pady=5)
        self.score_frame.pack(fill="x")

        self.lbl_score_x = Label(self.score_frame, text="Player X: 0", font=('Arial', 11, 'bold'), fg=self.color_x, bg="#1e1e24")
        self.lbl_score_x.pack(side="left", expand=True, padx=20)

        self.lbl_score_o = Label(self.score_frame, text="Computer: 0", font=('Arial', 11, 'bold'), fg=self.color_o, bg="#1e1e24")
        self.lbl_score_o.pack(side="right", expand=True, padx=20)

        self.status_frame = Frame(self.root, bg="#1e1e24", pady=5)
        self.status_frame.pack(fill="x")

        self.lbl_status = Label(self.status_frame, text="X's Turn", font=('Arial', 12, 'bold'), fg="white", bg="#1e1e24")
        self.lbl_status.pack(anchor="center")

    def create_grid(self):
        self.grid_frame = Frame(self.root, bg="#1e1e24")
        self.grid_frame.pack(padx=10, pady=5)

        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            btn = Button(self.grid_frame, text=" ", font=('Arial', 20, 'bold'), 
                height=2, width=5, bg=self.color_btn, fg="white",
                activebackground="#3a3a4a", activeforeground="white",
                bd=2, relief="groove",
                command=lambda idx=i: self.btn_click(idx)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)
    
    def create_restart_button(self):
        self.restart_btn = Button(
            self.root, text="Restart Game", font=('Arial', 12, 'bold'), 
            bg="#dc3545", fg="white", activebackground="#c82333", activeforeground="white",
            bd=0, pady=8, command=self.reset
        )
        self.restart_btn.pack(fill="x", padx=13, pady=15)
        
        footer_lbl = Label(self.root, text="© Play. Win. Repeat. | Last Committed: May 27, 2026", font=('Arial', 8, 'bold'), fg="#6c757d", bg="#1e1e24")
        footer_lbl.pack(side="bottom", pady=(0, 5))

    def btn_click(self, idx):
        if self.board_state[idx] == "":
            self.make_move(idx, self.current_player)
            
            if not self.check_if_won():
                if self.game_mode == "👥 Local 2 Players":
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.lbl_status.config(text=f"{self.current_player}'s Turn")
                else:
                    self.lbl_status.config(text="Computer thinking...")
                    self.root.after(400, self.computer_move)

    def make_move(self, idx, player):
        self.board_state[idx] = player
        color = self.color_x if player == "X" else self.color_o
        self.buttons[idx].config(text=player, fg=color, state=DISABLED, disabledforeground=color)
        self.count += 1

    def computer_move(self):
        if "" not in self.board_state or self.check_winner_logic(self.board_state):
            return

        move = self.get_smart_move()

        if move is None:
            empty_slots = [i for i, val in enumerate(self.board_state) if val == ""]
            move = random.choice(empty_slots)

        self.make_move(move, "O")
        
        if not self.check_if_won():
            self.current_player = "X"
            self.lbl_status.config(text="X's Turn")

    def get_smart_move(self):
        for player in ["O", "X"]:
            for i in range(9):
                if self.board_state[i] == "":
                    temp_board = list(self.board_state)
                    temp_board[i] = player
                    if self.check_winner_logic(temp_board):
                        return i
        return None

    def check_winner_logic(self, board):
        winning_positions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for pos in winning_positions:
            if board[pos[0]] == board[pos[1]] == board[pos[2]] != "":
                return board[pos[0]]
        return None

    def show_custom_message(self, title, message):
    
        msg_box = Toplevel(self.root)
        msg_box.title(title)
        msg_box.configure(bg="#1e1e24")
        msg_box.resizable(False, False)
        msg_box.geometry("300x150")
        
        lbl_msg = Label(
            msg_box, text=message, font=('Arial', 12, 'bold'), 
            fg="white", bg="#1e1e24", wraplength=250, justify="center"
        )
        lbl_msg.pack(expand=True, pady=(20, 10))
        
        btn_ok = Button(
            msg_box, text="OK", font=('Arial', 10, 'bold'), 
            bg="#28a745", fg="white", activebackground="#218838", activeforeground="white",
            bd=0, width=10, pady=5, command=msg_box.destroy
        )
        btn_ok.pack(pady=(0, 20))
        
        msg_box.transient(self.root)
        msg_box.grab_set()
        self.root.wait_window(msg_box)

    def check_if_won(self):
        winning_positions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for pos in winning_positions:
            if self.board_state[pos[0]] == self.board_state[pos[1]] == self.board_state[pos[2]] != "":
                for index in pos:
                    self.buttons[index].config(bg="#28a745")
                
                winner = self.board_state[pos[0]]
                self.scores[winner] += 1
                self.update_scores()
                
                self.lbl_status.config(text=f"{winner} Wins!")
                self.disable_all_buttons()
                
                self.show_custom_message("Game Over", f"Player {winner} wins this round!")
                return True

        if "" not in self.board_state:
            self.lbl_status.config(text="It's a Tie!")
            
            self.show_custom_message("Game Over", "It's a Tie!")
            return True
        return False

    def update_scores(self):
        o_label = "Computer" if self.game_mode == "🤖 vs Computer (AI)" else "Player O"
        self.lbl_score_x.config(text=f"Player X: {self.scores['X']}")
        self.lbl_score_o.config(text=f"{o_label}: {self.scores['O']}")

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state=DISABLED)

    def reset(self):
        self.current_player = "X"
        self.count = 0
        self.board_state = [""] * 9
        self.lbl_status.config(text="X's Turn")
        for btn in self.buttons:
            btn.config(text=" ", bg=self.color_btn, state=NORMAL)

if __name__ == "__main__":
    root = Tk()
    app = TicTacToe(root)
    root.mainloop()