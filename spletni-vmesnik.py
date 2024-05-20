import tkinter as tk
from tkinter import ttk
import numpy as np
import nashpy as nash

class GameInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Izračun ravnovesij v bimatrični igri")
        
        self.choice_var = tk.StringVar()
        self.choice_var.set("Izberi možnost")
        
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self, text="Izberi možnost:").grid(row=0, column=0, padx=5, pady=5)
        self.choice_menu = ttk.OptionMenu(self, self.choice_var, "Izberi možnost", "Vnesi igro", "Naključno generiraj igro", command=self.show_options)
        self.choice_menu.grid(row=0, column=1, padx=5, pady=5)
        
        self.matrix_frame = ttk.Frame(self)
        self.matrix_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
    def show_options(self, choice):
        if choice == "Vnesi igro":
            self.show_input_fields()
        elif choice == "Naključno generiraj igro":
            self.show_random_game()
            
    def show_input_fields(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.matrix_frame, text="Vnesi za igralca 1:", anchor="center").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.matrix_frame, text="Vnesi za igralca 2:", anchor="center").grid(row=0, column=2, padx=5, pady=5)
    
        self.player1_matrix = []
        self.player2_matrix = []
        for i in range(2):
            player1_row = []
            player2_row = []
        
            # Polja za igralca 1
            for j in range(2):
                player1_entry = ttk.Entry(self.matrix_frame, width=5)
                player1_entry.grid(row=i+1, column=j, padx=5, pady=5)
                player1_row.append(player1_entry)
        
            # Prostor med igralci
            ttk.Label(self.matrix_frame, text="").grid(row=i+1, column=2, padx=5, pady=5)
        
            # Polja za igralca 2
            for j in range(2):
                player2_entry = ttk.Entry(self.matrix_frame, width=5)
                player2_entry.grid(row=i+1, column=j+3, padx=5, pady=5)
                player2_row.append(player2_entry)
        
            self.player1_matrix.append(player1_row)
            self.player2_matrix.append(player2_row)
        
    def show_random_game(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        game_matrix = np.random.randint(0, 11, size=(2, 2))
        ttk.Label(self.matrix_frame, text="Igra igralec 1:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.matrix_frame, text=str(game_matrix[0])).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.matrix_frame, text="Igra igralec 2:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.matrix_frame, text=str(game_matrix[1])).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.matrix_frame, text="Izračunaj", command=self.calculate).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
    def calculate(self):
        player1_game = np.array(eval(self.player1_entry.get()))
        player2_game = np.array(eval(self.player2_entry.get()))
        game = nash.Game(player1_game, player2_game)
        nash_eq = game.vertex_enumeration()
        # Tukaj lahko naredite karkoli želite s podatki o ravnotežjih
        
if __name__ == "__main__":
    app = GameInterface()
    app.mainloop()
