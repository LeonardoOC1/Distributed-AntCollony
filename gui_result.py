# gui_result.py

import tkinter as tk
from tkinter import ttk
import pickle
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

RESULT_FILE = "aco_result.pkl"  # Salvo pelo servidor

class ACOResultGUI:
    def __init__(self, master):
        self.master = master
        master.title("Resultado ACO Distribuído")

        self.label = ttk.Label(master, text="Melhor Caminho Encontrado:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.text = tk.Text(master, height=5, width=50, font=("Consolas", 10))
        self.text.pack(padx=10, pady=5)

        self.canvas_frame = ttk.Frame(master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.load_and_display_result()

    def load_and_display_result(self):
        try:
            with open(RESULT_FILE, "rb") as f:
                nodes, tour, distance = pickle.load(f)
        except:
            self.text.insert(tk.END, "Arquivo de resultado não encontrado.")
            return

        self.text.insert(tk.END, " -> ".join(str(i) for i in tour) + f"\n\nDistância Total: {distance:.2f}")

        fig, ax = plt.subplots()
        x = [nodes[i][0] for i in tour] + [nodes[tour[0]][0]]
        y = [nodes[i][1] for i in tour] + [nodes[tour[0]][1]]

        ax.plot(x, y, marker='o')
        for i in range(len(tour)):
            ax.annotate(str(tour[i]), (nodes[tour[i]][0], nodes[tour[i]][1]))
        ax.set_title("Melhor Caminho ACO")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x500")
    app = ACOResultGUI(root)
    root.mainloop()
