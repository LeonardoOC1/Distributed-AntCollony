import tkinter as tk
from tkinter import ttk
import pickle
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

RESULT_FILE = "aco_result.pkl"

class ACOResultGUI:
    def __init__(self, master):
        self.master = master
        master.title("Comparação: Grafo Original vs Melhor Caminho")

        self.label = ttk.Label(master, text="Melhor Caminho Encontrado:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.text = tk.Text(master, height=5, width=70, font=("Consolas", 10))
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

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Grafo Original
        ax1.set_title("Grafo Original")
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                x = [nodes[i][0], nodes[j][0]]
                y = [nodes[i][1], nodes[j][1]]
                ax1.plot(x, y, color='gray', linestyle='dotted', linewidth=0.8)
        for i, (x, y) in enumerate(nodes):
            ax1.plot(x, y, 'o')
            ax1.text(x + 1, y, str(i), fontsize=9)

        # Melhor Caminho
        ax2.set_title("Melhor Caminho ACO")
        x = [nodes[i][0] for i in tour] + [nodes[tour[0]][0]]
        y = [nodes[i][1] for i in tour] + [nodes[tour[0]][1]]
        ax2.plot(x, y, marker='o')
        for i in range(len(tour)):
            ax2.annotate(str(tour[i]), (nodes[tour[i]][0], nodes[tour[i]][1]))

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("900x600")
    app = ACOResultGUI(root)
    root.mainloop()