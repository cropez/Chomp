import tkinter as tk
from chomp import Chomp
from tkinter import messagebox

class ChompGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Chomp")
        self.geometry("400x400")
        self.create_widgets()
        self.is_player_turn = True

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        cell_width = 400 // self.game.cols
        cell_height = 400 // self.game.rows
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x0 = col * cell_width
                y0 = row * cell_height
                x1 = (col + 1) * cell_width
                y1 = (row + 1) * cell_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", tags=f"{row}-{col}")
                self.canvas.tag_bind(f"{row}-{col}", "<Button>", self.on_cell_click)

    def on_cell_click(self, event):
        if not self.is_player_turn:
            return

        clicked = self.canvas.find_withtag("current")
        row, col = map(int, self.canvas.gettags(clicked)[0].split("-"))

        if self.game.valid_move(row, col):
            self.game.apply_move(row, col)
            for r in range(row, self.game.rows):
                for c in range(col, self.game.cols):
                    self.canvas.itemconfigure(f"{r}-{c}", fill="green")

            if self.game.game_finished():
                self.canvas.unbind("<Button>")
                messagebox.showinfo("Spēle beigusies","Spēlētājs uzvar!" )
                return

            self.is_player_turn = False
            self.after(500, self.computer_move)

    def computer_move(self):
        row, col = self.game.optimal_move(3)
        if self.game.valid_move(row, col):
            self.game.apply_move(row, col)
            for r in range(row, self.game.rows):
                for c in range(col, self.game.cols):
                    self.canvas.itemconfigure(f"{r}-{c}", fill="green")

            if self.game.game_finished():
                self.canvas.unbind("<Button>")
                messagebox.showinfo("Spēle beigusies", "Dators uzvar!")
                return

            self.is_player_turn = True
        else:
            self.computer_move()


if __name__ == "__main__":
    game = Chomp(8, 8)
    app = ChompGUI(game)
    app.mainloop()