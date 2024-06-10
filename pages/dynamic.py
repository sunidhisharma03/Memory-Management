import tkinter as tk
from tkinter import messagebox
import csv
import os

class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size

class Memory:
    def __init__(self, total_size):
        self.total_size = total_size
        self.free_memory = [{'start': 0, 'size': total_size}]
        self.allocated_memory = {}
        self.initialize_csv()

    def add_process(self, process, strategy='first_fit'):
        if strategy == 'first_fit':
            success = self.first_fit(process)
        elif strategy == 'best_fit':
            success = self.best_fit(process)
        elif strategy == 'worst_fit':
            success = self.worst_fit(process)
        else:
            success = False

        if success:
            self.log_memory_state()

        return success

    def remove_process(self, pid):
        if pid in self.allocated_memory:
            memory_block = self.allocated_memory.pop(pid)
            self.free_memory.append(memory_block)
            self.merge_free_memory()
            self.log_memory_state()
            return True
        return False

    def first_fit(self, process):
        for i, block in enumerate(self.free_memory):
            if block['size'] >= process.size:
                self.allocated_memory[process.pid] = {'start': block['start'], 'size': process.size}
                block['start'] += process.size
                block['size'] -= process.size
                if block['size'] == 0:
                    self.free_memory.pop(i)
                return True
        return False

    def best_fit(self, process):
        best_index = -1
        best_size = float('inf')
        for i, block in enumerate(self.free_memory):
            if block['size'] >= process.size and block['size'] < best_size:
                best_index = i
                best_size = block['size']
        if best_index != -1:
            block = self.free_memory[best_index]
            self.allocated_memory[process.pid] = {'start': block['start'], 'size': process.size}
            block['start'] += process.size
            block['size'] -= process.size
            if block['size'] == 0:
                self.free_memory.pop(best_index)
            return True
        return False

    def worst_fit(self, process):
        worst_index = -1
        worst_size = 0
        for i, block in enumerate(self.free_memory):
            if block['size'] >= process.size and block['size'] > worst_size:
                worst_index = i
                worst_size = block['size']
        if worst_index != -1:
            block = self.free_memory[worst_index]
            self.allocated_memory[process.pid] = {'start': block['start'], 'size': process.size}
            block['start'] += process.size
            block['size'] -= process.size
            if block['size'] == 0:
                self.free_memory.pop(worst_index)
            return True
        return False

    def merge_free_memory(self):
        self.free_memory.sort(key=lambda x: x['start'])
        i = 0
        while i < len(self.free_memory) - 1:
            if self.free_memory[i]['start'] + self.free_memory[i]['size'] == self.free_memory[i + 1]['start']:
                self.free_memory[i]['size'] += self.free_memory[i + 1]['size']
                self.free_memory.pop(i + 1)
            else:
                i += 1

    def total_free_memory(self):
        return sum(block['size'] for block in self.free_memory)

    def initialize_csv(self):
        if not os.path.isfile('memory_log.csv'):
            with open('memory_log.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Memory'])

    def log_memory_state(self):
        total_free_memory = self.total_free_memory()

        # Read existing CSV data
        rows = []
        with open('memory_log.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Update the row with 'dynamic'
        for row in rows:
            if row[0] == 'dynamic':
                row[1] = str(total_free_memory)
                break
        else:
            rows.append(['dynamic', total_free_memory])  # Add a new row if 'dynamic' was not found

        # Write the updated rows back to the CSV
        with open('memory_log.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

class MemoryManagerGUIDynamic:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator - Dynamic")

        self.total_size_label = tk.Label(root, text="Total Memory Size:")
        self.total_size_label.pack(pady=(20, 0))
        self.total_size_entry = tk.Entry(root)
        self.total_size_entry.pack()

        self.set_memory_button = tk.Button(root, text="Set Memory", command=self.set_memory)
        self.set_memory_button.pack()

        self.strategy_label = tk.Label(root, text="Memory Allocation Strategy:")
        self.strategy_label.pack()
        self.strategy_var = tk.StringVar(value='first_fit')
        self.first_fit_radio = tk.Radiobutton(root, text="First Fit", variable=self.strategy_var, value='first_fit')
        self.first_fit_radio.pack()
        self.best_fit_radio = tk.Radiobutton(root, text="Best Fit", variable=self.strategy_var, value='best_fit')
        self.best_fit_radio.pack()
        self.worst_fit_radio = tk.Radiobutton(root, text="Worst Fit", variable=self.strategy_var, value='worst_fit')
        self.worst_fit_radio.pack()

        self.process_id_label = tk.Label(root, text="Process ID:")
        self.process_id_label.pack()
        self.process_id_entry = tk.Entry(root)
        self.process_id_entry.pack()
        self.process_size_label = tk.Label(root, text="Process Size:")
        self.process_size_label.pack()
        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.pack()
        self.add_process_button = tk.Button(root, text="Add Process", command=self.add_process)
        self.add_process_button.pack()
        self.remove_process_button = tk.Button(root, text="Remove Process", command=self.remove_process)
        self.remove_process_button.pack()

        self.memory = None

        self.initialize_csv()

    def initialize_csv(self):
        if not os.path.isfile('memory_log.csv'):
            with open('memory_log.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Memory'])

    def set_memory(self):
        try:
            total_size = int(self.total_size_entry.get())
            self.memory = Memory(total_size)
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for total memory size.")

    def add_process(self):
        if self.memory:
            try:
                pid = int(self.process_id_entry.get())
                size = int(self.process_size_entry.get())
                process = Process(pid, size)
                if self.memory.add_process(process, self.strategy_var.get()):
                    self.update_display()
                else:
                    messagebox.showwarning("Memory Full", "Not enough memory to allocate for the process.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", "Please enter valid integers for process ID and size.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def remove_process(self):
        if self.memory:
            try:
                pid = int(self.process_id_entry.get())
                if self.memory.remove_process(pid):
                    self.update_display()
                else:
                    messagebox.showwarning("Process Not Found", "Process ID not found in allocated processes.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for process ID.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def update_display(self):
        if self.memory:
            allocated_text = "Allocated Memory:\n"
            for pid, block in self.memory.allocated_memory.items():
                allocated_text += f"Process {pid}: Start Address = {block['start']}, Size = {block['size']}\n"

            free_text = "Free Memory:\n"
            for block in self.memory.free_memory:
                free_text += f"Start Address = {block['start']}, Size = {block['size']}\n"

            self.display_text.set(allocated_text + "\n" + free_text)

    def run(self):
        self.display_text = tk.StringVar()
        self.display_label = tk.Label(self.root, textvariable=self.display_text)
        self.display_label.pack()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = MemoryManagerGUIDynamic(root)
    app.run()
