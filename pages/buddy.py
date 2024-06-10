import tkinter as tk
from tkinter import ttk
import csv
import os

class BuddySystem:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.allocated_blocks = {}
        self.free_blocks = {total_memory: [0]}
        self.initialize_csv()

    def allocate(self, process_id, size):
        block_size = min((s for s in self.free_blocks if s >= size), default=None)
        if block_size is None:
            return "Error: Not enough memory."

        address = self.free_blocks[block_size].pop()
        if not self.free_blocks[block_size]:
            del self.free_blocks[block_size]

        while block_size > 2 * size:
            block_size //= 2
            if block_size not in self.free_blocks:
                self.free_blocks[block_size] = []
            self.free_blocks[block_size].append(address + block_size)

        self.allocated_blocks[process_id] = (address, size)
        self.log_memory_state()
        return f"Allocated {size} memory to process {process_id}."
    
    def deallocate(self, process_id):
        if process_id not in self.allocated_blocks:
            return "Error: Process not found."
        address, size = self.allocated_blocks.pop(process_id)
        if size not in self.free_blocks:
            self.free_blocks[size] = []
        self.free_blocks[size].append(address)
        self.log_memory_state()
        return f"Deallocated memory from process {process_id}."

    def get_free_blocks(self):
        return self.free_blocks

    def get_allocated_blocks(self):
        return self.allocated_blocks

    def total_free_memory(self):
        return sum(size * len(addresses) for size, addresses in self.free_blocks.items())

    def initialize_csv(self):
        if not os.path.isfile('memory_log.csv'):
            with open('memory_log.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Memory'])

    def log_memory_state(self):
        total_free_memory = self.total_free_memory()
        rows = []
        updated = False

        # Read the current content of the CSV file
        if os.path.isfile('memory_log.csv'):
            with open('memory_log.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)

        # Update the memory value for "buddy" if the row exists
        for row in rows:
            if row[0] == 'buddy':
                row[1] = total_free_memory
                updated = True

        # If "buddy" row does not exist, add it
        if not updated:
            rows.append(['buddy', total_free_memory])

        # Write the updated content back to the CSV file
        with open('memory_log.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buddy System Memory Management")
        self.geometry("700x400")
        self.buddy_system = None
        self.create_widgets()

    def create_widgets(self):
        self.memory_label = ttk.Label(self, text="Total Memory:")
        self.memory_label.grid(column=0, row=0)
        self.memory_entry = ttk.Entry(self)
        self.memory_entry.grid(column=1, row=0)
        self.memory_button = ttk.Button(self, text="Set Memory", command=self.set_memory)
        self.memory_button.grid(column=2, row=0)

        self.process_label = ttk.Label(self, text="Process ID:")
        self.process_label.grid(column=0, row=1)
        self.process_entry = ttk.Entry(self)
        self.process_entry.grid(column=1, row=1)

        self.size_label = ttk.Label(self, text="Size:")
        self.size_label.grid(column=0, row=2)
        self.size_entry = ttk.Entry(self)
        self.size_entry.grid(column=1, row=2)

        self.allocate_button = ttk.Button(self, text="Allocate", command=self.allocate_memory)
        self.allocate_button.grid(column=2, row=1)
        self.deallocate_button = ttk.Button(self, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.grid(column=2, row=2)

        self.message_label = ttk.Label(self, text="")
        self.message_label.grid(column=0, row=3, columnspan=3)

        self.memory_text = tk.Text(self)
        self.memory_text.grid(column=0, row=4, columnspan=3)

    def set_memory(self):
        try:
            total_memory = int(self.memory_entry.get())
            self.buddy_system = BuddySystem(total_memory)
            self.message_label.config(text=f"Total memory set to {total_memory}.")
            self.update_memory_text()
        except ValueError:
            self.message_label.config(text="Error: Please enter a valid integer for total memory.")

    def allocate_memory(self):
        try:
            process_id = self.process_entry.get()
            size = int(self.size_entry.get())
            message = self.buddy_system.allocate(process_id, size)
            self.message_label.config(text=message)
            self.update_memory_text()
        except ValueError:
            self.message_label.config(text="Error: Please enter a valid integer for size.")

    def deallocate_memory(self):
        process_id = self.process_entry.get()
        message = self.buddy_system.deallocate(process_id)
        self.message_label.config(text=message)
        self.update_memory_text()

    def update_memory_text(self):
        if self.buddy_system:
            self.memory_text.delete(1.0, tk.END)
            free_blocks = self.buddy_system.get_free_blocks()
            allocated_blocks = self.buddy_system.get_allocated_blocks()
            self.memory_text.insert(tk.END, "Free Blocks:\n")
            for size, addresses in sorted(free_blocks.items()):
                self.memory_text.insert(tk.END, f"Size {size}: {sorted(addresses)}\n")
            self.memory_text.insert(tk.END, "\nAllocated Blocks:\n")
            for process_id, (address, size) in sorted(allocated_blocks.items()):
                self.memory_text.insert(tk.END, f"Process {process_id}: Address {address}, Size {size}\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
