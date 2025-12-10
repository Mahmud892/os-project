
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# Disk Scheduling Algorithms
def fcfs(requests, head):
    sequence = [head] + requests
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

def sstf(requests, head):
    sequence = [head]
    reqs = requests.copy()
    while reqs:
        closest = min(reqs, key=lambda x: abs(head - x))
        sequence.append(closest)
        head = closest
        reqs.remove(closest)
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

def scan(requests, head, disk_size):
    left = [r for r in requests if r < head]
    right = [r for r in requests if r > head]
    left.sort(reverse=True)
    right.sort()
    sequence = [head] + right + [disk_size - 1] + left
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

def cscan(requests, head, disk_size):
    left = [r for r in requests if r < head]
    right = [r for r in requests if r > head]
    left.sort()
    right.sort()
    sequence = [head] + right + [disk_size - 1, 0] + left
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

def look(requests, head):
    left = [r for r in requests if r < head]
    right = [r for r in requests if r > head]
    left.sort(reverse=True)
    right.sort()
    sequence = [head] + right + left
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

def clook(requests, head):
    left = [r for r in requests if r < head]
    right = [r for r in requests if r > head]
    left.sort()
    right.sort()
    sequence = [head] + right + left
    movement = sum(abs(sequence[i+1] - sequence[i]) for i in range(len(sequence)-1))
    return sequence, movement

# GUI Implementation
class DiskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Algorithm Visualizer")
        self.root.geometry("700x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Request Queue (comma separated):").pack(pady=5)
        self.entry_requests = tk.Entry(self.root, width=50)
        self.entry_requests.pack(pady=5)

        tk.Label(self.root, text="Initial Head Position:").pack(pady=5)
        self.entry_head = tk.Entry(self.root, width=20)
        self.entry_head.pack(pady=5)

        tk.Label(self.root, text="Disk Size:").pack(pady=5)
        self.entry_disk = tk.Entry(self.root, width=20)
        self.entry_disk.insert(0, "200")
        self.entry_disk.pack(pady=5)

        tk.Label(self.root, text="Select Algorithm:").pack(pady=5)
        self.algorithm = ttk.Combobox(self.root, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"])
        self.algorithm.current(0)
        self.algorithm.pack(pady=5)

        tk.Button(self.root, text="Run", command=self.run_algorithm, bg="lightgreen").pack(pady=10)
        tk.Button(self.root, text="Clear Plot", command=self.clear_plot, bg="lightcoral").pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = None

    def run_algorithm(self):
        try:
            requests = list(map(int, self.entry_requests.get().split(',')))
            head = int(self.entry_head.get())
            disk_size = int(self.entry_disk.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")
            return

        algo = self.algorithm.get()
        if algo == "FCFS":
            seq, move = fcfs(requests, head)
        elif algo == "SSTF":
            seq, move = sstf(requests, head)
        elif algo == "SCAN":
            seq, move = scan(requests, head, disk_size)
        elif algo == "C-SCAN":
            seq, move = cscan(requests, head, disk_size)
        elif algo == "LOOK":
            seq, move = look(requests, head)
        else:
            seq, move = clook(requests, head)

        self.show_plot(seq, move)

    def show_plot(self, seq, move):
        self.ax.clear()
        self.ax.plot(seq, range(len(seq)), marker='o')
        self.ax.set_title(f"Head Movement: {move}")
        self.ax.set_xlabel("Cylinder Number")
        self.ax.set_ylabel("Sequence Step")
        plt.gca().invert_yaxis()
        plt.show()

    def clear_plot(self):
        self.ax.clear()
        plt.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulerApp(root)
    root.mainloop()
