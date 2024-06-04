import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size

class Memory:
    def __init__(self, partitions):
        self.partitions = [{'start': sum(partitions[:i]), 'size': partitions[i], 'free': True} for i in range(len(partitions))]
        self.allocated_partitions = {}

    def add_process(self, process, strategy='first_fit'):
        if strategy == 'first_fit':
            return self.first_fit(process)
        elif strategy == 'best_fit':
            return self.best_fit(process)
        elif strategy == 'worst_fit':
            return self.worst_fit(process)
        return False

    def remove_process(self, pid):
        if pid in self.allocated_partitions:
            index = self.allocated_partitions.pop(pid)
            self.partitions[index]['free'] = True
            return True
        return False

    def first_fit(self, process):
        for i, partition in enumerate(self.partitions):
            if partition['free'] and partition['size'] >= process.size:
                self.allocated_partitions[process.pid] = i
                partition['free'] = False
                return True
        return False

    def best_fit(self, process):
        best_index = -1
        best_size = float('inf')
        for i, partition in enumerate(self.partitions):
            if partition['free'] and partition['size'] >= process.size and partition['size'] < best_size:
                best_index = i
                best_size = partition['size']
        if best_index != -1:
            self.allocated_partitions[process.pid] = best_index
            self.partitions[best_index]['free'] = False
            return True
        return False

    def worst_fit(self, process):
        worst_index = -1
        worst_size = 0
        for i, partition in enumerate(self.partitions):
            if partition['free'] and partition['size'] >= process.size and partition['size'] > worst_size:
                worst_index = i
                worst_size = partition['size']
        if worst_index != -1:
            self.allocated_partitions[process.pid] = worst_index
            self.partitions[worst_index]['free'] = False
            return True
        return False

class MemoryManagerGUIFixed:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator - Fixed")

        self.memory_type_label = tk.Label(root, text="Memory Type:")
        self.memory_type_label.pack(pady=(20,0))
        self.memory_type_var = tk.StringVar(value='equal')
        self.equal_radio = tk.Radiobutton(root, text="Equal Fixed Size Partitions", variable=self.memory_type_var, value='equal', command=self.toggle_memory_type)
        self.equal_radio.pack()
        self.unequal_radio = tk.Radiobutton(root, text="Unequal Fixed Size Partitions", variable=self.memory_type_var, value='unequal', command=self.toggle_memory_type)
        self.unequal_radio.pack()

        self.total_size_label = tk.Label(root, text="Total Memory Size:")
        self.total_size_label.pack()
        self.total_size_entry = tk.Entry(root)
        self.total_size_entry.pack()
        
        self.partition_size_label = tk.Label(root, text="Partition Size (for equal partitions):")
        self.partition_size_label.pack()
        self.partition_size_entry = tk.Entry(root)
        self.partition_size_entry.pack()
        
        self.partitions_label = tk.Label(root, text="Partition Sizes (comma-separated for unequal partitions):")
        self.partitions_label.pack()
        self.partitions_entry = tk.Entry(root)
        self.partitions_entry.pack()
        
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

    def toggle_memory_type(self):
        if self.memory_type_var.get() == 'equal':
            self.partition_size_label.pack()
            self.partition_size_entry.pack()
            self.partitions_label.pack_forget()
            self.partitions_entry.pack_forget()
        else:
            self.partition_size_label.pack_forget()
            self.partition_size_entry.pack_forget()
            self.partitions_label.pack()
            self.partitions_entry.pack()

    def set_memory(self):
        try:
            if self.memory_type_var.get() == 'equal':
                total_size = int(self.total_size_entry.get())
                partition_size = int(self.partition_size_entry.get())
                if total_size % partition_size != 0:
                    raise ValueError("Total size must be a multiple of partition size.")
                partitions = [partition_size] * (total_size // partition_size)
            else:
                partitions = list(map(int, self.partitions_entry.get().split(',')))
                total_size = sum(partitions)
            self.memory = Memory(partitions)
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def add_process(self):
        if self.memory:
            try:
                pid = int(self.process_id_entry.get())
                size = int(self.process_size_entry.get())
                max_partition_size = max(partition['size'] for partition in self.memory.partitions)
                if size > max_partition_size:
                    raise ValueError("Process size must be less than or equal to the largest partition size.")
                process = Process(pid, size)
                if self.memory.add_process(process, self.strategy_var.get()):
                    self.update_display()
                else:
                    messagebox.showwarning("Memory Full", "Not enough memory to allocate for the process.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
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
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for process ID.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def update_display(self):
        if self.memory:
            allocated_text = "Allocated Partitions:\n"
            for pid, index in self.memory.allocated_partitions.items():
                partition = self.memory.partitions[index]
                allocated_text += f"Process {pid}: Start Address = {partition['start']}, Size = {partition['size']}\n"

            free_text = "Free Partitions:\n"
            for partition in self.memory.partitions:
                if partition['free']:
                    free_text += f"Start Address = {partition['start']}, Size = {partition['size']}\n"

            self.display_text.set(allocated_text + "\n" + free_text)

    def run(self):
        self.display_text = tk.StringVar()
        self.display_label = tk.Label(self.root, textvariable=self.display_text)
        self.display_label.pack()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x700")
    app = MemoryManagerGUIFixed(root)
    app.run()