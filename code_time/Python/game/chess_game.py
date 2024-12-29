#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import chess
from collections import Counter

PIECE_SYMBOLS = {
    'P': '\u2659', 'R': '\u2656', 'N': '\u2658',
    'B': '\u2657', 'Q': '\u2655', 'K': '\u2654',
    'p': '\u265F', 'r': '\u265C', 'n': '\u265E',
    'b': '\u265D', 'q': '\u265B', 'k': '\u265A'
}

PIECE_NAMES = {
    chess.PAWN: "Pawn",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.ROOK: "Rook",
    chess.QUEEN: "Queen",
    chess.KING: "King"
}

THEMES = {
    "Classic": ["#F0D9B5", "#B58863"],
    "Dark": ["#769656", "#eeeed2"],
    "Blue": ["#a9a9a9", "#6495ED"],
    "Green": ["#98fb98", "#2e8b57"],
    "Red": ["#ff9999", "#990000"],
    "Grey": ["#d3d3d3", "#808080"],
    "Purple": ["#dda0dd", "#4b0082"],
    "Orange": ["#ffcc80", "#ff8c00"]
}

class ChessApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Chess Game - Captures Only on Taken Pieces")
        self.board = chess.Board()
        self.selected_square = None
        self.current_theme = "Classic"
        self.captured_white = []
        self.captured_black = []
        self.move_history = []
        self.current_move_index = 0
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.side_menu = tk.Frame(self.master, width=240, bg="#f0f0f0")
        self.side_menu.grid(row=0, column=0, sticky="ns")
        self.side_menu.grid_propagate(False)
        self.create_theme_selection()
        self.create_control_buttons()
        self.create_captured_display()
        self.create_move_history_display()
        self.status_label = tk.Label(self.side_menu, text="White's turn", font=("Arial", 14), bg="#f0f0f0")
        self.status_label.pack(pady=20)
        self.board_frame = tk.Frame(self.master, bg="#FFFFFF")
        self.board_frame.grid(row=0, column=1, sticky="nsew")
        self.board_frame.rowconfigure(0, weight=1)
        self.board_frame.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.board_frame, bg="#FFFFFF")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_click)
        self.master.bind("<Configure>", self.on_resize)
        self.draw_board()
        self.draw_pieces()
        self.update_captured_display()

    def create_theme_selection(self):
        tk.Label(self.side_menu, text="Choose Theme:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        for theme in THEMES:
            tk.Button(self.side_menu, text=theme, width=15, command=lambda t=theme: self.change_theme(t)).pack(pady=2)

    def create_control_buttons(self):
        tk.Button(self.side_menu, text="Reset Game", width=15, command=self.reset_game, font=("Arial", 10)).pack(pady=5)
        tk.Button(self.side_menu, text="Hint", width=15, command=self.show_hint, font=("Arial", 10)).pack(pady=5)
        tk.Button(self.side_menu, text="Undo Move", width=15, command=self.undo_move, font=("Arial", 10)).pack(pady=5)

    def create_captured_display(self):
        f = tk.Frame(self.side_menu, bg="#f0f0f0")
        f.pack(pady=10, fill="x")
        tk.Label(f, text="Captured Pieces", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
        tk.Label(f, text="White Pieces Lost:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(5,0))
        self.captured_white_label = tk.Label(f, text="", bg="#f0f0f0", font=("Arial", 9), justify="left")
        self.captured_white_label.pack(anchor="w")
        tk.Label(f, text="Black Pieces Lost:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(5,0))
        self.captured_black_label = tk.Label(f, text="", bg="#f0f0f0", font=("Arial", 9), justify="left")
        self.captured_black_label.pack(anchor="w")

    def create_move_history_display(self):
        f = tk.Frame(self.side_menu, bg="#f0f0f0")
        f.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(f, text="Move History:", font=("Arial", 10), bg="#f0f0f0").pack()
        scrollbar = tk.Scrollbar(f)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.move_history_listbox = tk.Listbox(f, width=20, height=10, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.move_history_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.move_history_listbox.yview)

    def draw_board(self):
        self.canvas.delete("square", "highlight", "coord", "piece")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.coord_margin = 30
        board_size = min(w - 2*self.coord_margin, h - 2*self.coord_margin)
        self.square_size = board_size / 8
        self.start_x = (w - board_size) / 2
        self.start_y = (h - board_size) / 2
        light_color, dark_color = THEMES[self.current_theme]
        for row in range(8):
            for col in range(8):
                x1 = self.start_x + col*self.square_size
                y1 = self.start_y + row*self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = light_color if (row + col) % 2 == 0 else dark_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tags="square")
        for col in range(8):
            file_label = chess.FILE_NAMES[col]
            x = self.start_x + col*self.square_size + self.square_size/2
            y = self.start_y + 8*self.square_size + self.coord_margin/2
            self.canvas.create_text(x, y, text=file_label, font=("Arial", 8), tags="coord")
        for row in range(8):
            rank_label = str(8 - row)
            x = self.start_x - self.coord_margin/2
            y = self.start_y + row*self.square_size + self.square_size/2
            self.canvas.create_text(x, y, text=rank_label, font=("Arial", 8), tags="coord")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for sq in chess.SQUARES:
            p = self.board.piece_at(sq)
            if p:
                f_ = chess.square_file(sq)
                r_ = chess.square_rank(sq)
                row = 7 - r_
                x = self.start_x + f_*self.square_size + self.square_size/2
                y = self.start_y + row*self.square_size + self.square_size/2
                sym = PIECE_SYMBOLS[p.symbol()]
                c = "black" if p.color == chess.BLACK else "white"
                self.canvas.create_text(x, y, text=sym, font=("Arial", int(self.square_size / 1.5)), fill=c, tags="piece")

    def on_click(self, event):
        col = int((event.x - self.start_x) // self.square_size)
        row = int((event.y - self.start_y) // self.square_size)
        if not (0 <= col <= 7 and 0 <= row <= 7):
            return
        r_ = 7 - row
        sq = chess.square(col, r_)
        sq_name = chess.square_name(sq)
        if self.selected_square:
            move_uci = self.selected_square + sq_name
            try:
                move = chess.Move.from_uci(move_uci)
            except ValueError:
                messagebox.showerror("Invalid Move", f"Invalid move format: {move_uci}")
                self.reset_selection()
                return
            if move in self.board.legal_moves:
                piece = self.board.piece_at(move.from_square)
                if piece and piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
                    promotion_piece = self.prompt_promotion()
                    if not promotion_piece:
                        self.reset_selection()
                        return
                    move.promotion = getattr(chess, promotion_piece.upper())
                is_capture = self.board.is_capture(move)
                is_en_passant = self.board.is_en_passant(move)
                if is_capture:
                    if is_en_passant:
                        cap_file = chess.square_file(move.to_square)
                        cap_rank = chess.square_rank(move.from_square)
                        cap_sq = chess.square(cap_file, cap_rank)
                    else:
                        cap_sq = move.to_square
                    cap_piece = self.board.piece_at(cap_sq)
                else:
                    cap_piece = None
                san_move = self.board.san(move)
                self.move_history.append(san_move)
                self.board.push(move)
                self.update_move_history_listbox()
                if cap_piece:
                    if cap_piece.color == chess.WHITE:
                        self.captured_white.append(cap_piece.piece_type)
                    else:
                        self.captured_black.append(cap_piece.piece_type)
                self.update_captured_display()
                self.update_status()
                self.reset_selection()
                self.draw_board()
                self.draw_pieces()
                if self.board.is_game_over():
                    self.end_game()
            else:
                msg = "You cannot make a move that leaves your king in check." if self.board.is_check() else "That move is not legal."
                messagebox.showerror("Invalid Move", msg)
                self.reset_selection()
        else:
            p = self.board.piece_at(sq)
            if p and p.color == self.board.turn:
                self.selected_square = sq_name
                self.highlight_moves(sq)

    def highlight_moves(self, sq):
        self.canvas.delete("highlight")
        self.highlighted_squares = []
        for move in self.board.legal_moves:
            if move.from_square == sq:
                to_sq = chess.square_name(move.to_square)
                self.highlight_square(to_sq)
                self.highlighted_squares.append(to_sq)

    def highlight_square(self, sq_name):
        s = chess.parse_square(sq_name)
        f_ = chess.square_file(s)
        r_ = chess.square_rank(s)
        row = 7 - r_
        x1 = self.start_x + f_*self.square_size
        y1 = self.start_y + row*self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2, tags="highlight")

    def reset_selection(self):
        self.selected_square = None
        self.canvas.delete("highlight")
        self.highlighted_squares = []

    def update_move_history_listbox(self):
        move_number = (len(self.move_history) + 1) // 2
        if len(self.move_history) % 2 == 1:
            txt = f"{move_number}. {self.move_history[-1]}"
        else:
            txt = f"{move_number}. ... {self.move_history[-1]}"
        self.move_history_listbox.insert(tk.END, txt)
        self.move_history_listbox.yview_moveto(1)

    def prompt_promotion(self):
        w = tk.Toplevel(self.master)
        w.title("Pawn Promotion")
        w.geometry("200x100")
        w.resizable(False, False)
        w.grab_set()
        tk.Label(w, text="Choose promotion piece:", font=("Arial", 10)).pack(pady=5)
        selected_piece = tk.StringVar()
        bf = tk.Frame(w)
        bf.pack(pady=5)
        for piece_ in ['Q', 'R', 'B', 'N']:
            tk.Button(bf, text=piece_, width=5, command=lambda p=piece_: self.select_promotion(p, selected_piece, w)).pack(side=tk.LEFT, padx=2)
        self.master.wait_window(w)
        return selected_piece.get()

    def select_promotion(self, piece, selected_piece, window):
        selected_piece.set(piece.lower())
        window.destroy()

    def update_captured_display(self):
        wc = Counter(self.captured_white)
        bc = Counter(self.captured_black)
        wl = []
        for pt, c in wc.items():
            symbol_char = {chess.PAWN:'P', chess.KNIGHT:'N', chess.BISHOP:'B', chess.ROOK:'R', chess.QUEEN:'Q', chess.KING:'K'}[pt]
            sym = PIECE_SYMBOLS[symbol_char]
            nm = PIECE_NAMES[pt]
            wl.append(f"{sym} {nm} x{c}")
        if not wl:
            wl.append("(None)")
        self.captured_white_label.config(text="\n".join(wl))
        bl = []
        for pt, c in bc.items():
            symbol_char = {chess.PAWN:'p', chess.KNIGHT:'n', chess.BISHOP:'b', chess.ROOK:'r', chess.QUEEN:'q', chess.KING:'k'}[pt]
            sym = PIECE_SYMBOLS[symbol_char]
            nm = PIECE_NAMES[pt]
            bl.append(f"{sym} {nm} x{c}")
        if not bl:
            bl.append("(None)")
        self.captured_black_label.config(text="\n".join(bl))

    def update_status(self):
        if self.board.is_checkmate():
            w = "Black" if self.board.turn == chess.WHITE else "White"
            s = f"Checkmate! {w} wins."
        elif self.board.is_stalemate():
            s = "Stalemate! It's a draw."
        elif self.board.is_insufficient_material():
            s = "Insufficient material! It's a draw."
        else:
            s = "White's turn" if self.board.turn == chess.WHITE else "Black's turn"
            if self.board.is_check():
                s += " - Check!"
        self.status_label.config(text=s)

    def end_game(self):
        if self.board.is_checkmate():
            w = "Black" if self.board.turn == chess.WHITE else "White"
            messagebox.showinfo("Game Over", f"Checkmate! {w} wins.")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Insufficient material! It's a draw.")

    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.canvas.delete("highlight")
        self.highlighted_squares = []
        self.captured_white.clear()
        self.captured_black.clear()
        self.move_history.clear()
        self.move_history_listbox.delete(0, tk.END)
        self.draw_board()
        self.draw_pieces()
        self.update_captured_display()
        self.update_status()

    def change_theme(self, theme):
        self.current_theme = theme
        self.draw_board()
        self.draw_pieces()
        self.update_captured_display()
        self.update_status()

    def show_hint(self):
        ob = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6", "d2d3", "f8c5"]
        if self.current_move_index >= len(ob):
            messagebox.showinfo("Hint", "No more hints available in the opening book.")
            return
        nm = ob[self.current_move_index]
        try:
            mv = chess.Move.from_uci(nm)
        except ValueError:
            messagebox.showerror("Invalid Move", f"The move {nm} is invalid.")
            return
        if mv in self.board.legal_moves:
            fsq = chess.square_name(mv.from_square)
            tsq = chess.square_name(mv.to_square)
            p = self.board.piece_at(mv.from_square)
            if p and p.piece_type == chess.PAWN and chess.square_rank(mv.to_square) in [0, 7]:
                ht = f"Suggested: {fsq} to {tsq} (Promote to Queen)"
            else:
                ht = f"Suggested: {fsq} to {tsq}"
            messagebox.showinfo("Hint", ht)
            self.highlight_square(fsq)
            self.highlight_square(tsq)
            self.current_move_index += 1
        else:
            messagebox.showinfo("Hint", "No valid hint available.")

    def undo_move(self):
        if not self.board.move_stack:
            messagebox.showinfo("Undo Move", "No moves to undo.")
            return
        lm = self.board.pop()
        if self.board.is_capture(lm):
            is_en_passant = self.board.is_en_passant(lm)
            if is_en_passant:
                cf = chess.square_file(lm.to_square)
                cr = chess.square_rank(lm.from_square)
                cs = chess.square(cf, cr)
            else:
                cs = lm.to_square
            up = self.board.piece_at(cs)
            if up:
                if up.color == chess.WHITE and self.captured_white:
                    self.captured_white.pop()
                elif up.color == chess.BLACK and self.captured_black:
                    self.captured_black.pop()
        if self.move_history:
            self.move_history.pop()
            self.move_history_listbox.delete(tk.END)
        self.draw_board()
        self.draw_pieces()
        self.update_captured_display()
        self.update_status()

    def on_resize(self, event):
        self.draw_board()
        self.draw_pieces()
        self.update_captured_display()

def main():
    root = tk.Tk()
    root.geometry("900x600")
    ChessApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
