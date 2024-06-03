import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self, pid, size, page_size):
        self.pid = pid
        self.size = size
        self.pages = [(i, min(page_size, size - i * page_size)) for i in range((size + page_size - 1) // page_size)]

class Memory:
    def __init__(self, total_size, page_size):
        self.total_size = total_size
        self.page_size = page_size
        self.num_frames = total_size // page_size
        self.free_frames = list(range(self.num_frames))
        self.allocated_frames = {}
        self.page_table = {}

    def add_process(self, process):
        num_pages = len(process.pages)
        if num_pages > len(self.free_frames):
            return False

        self.allocated_frames[process.pid] = []
        self.page_table[process.pid] = {}

        for page_num, page_size in process.pages:
            frame_num = self.free_frames.pop(0)
            self.allocated_frames[process.pid].append(frame_num)
            self.page_table[process.pid][page_num] = frame_num

        return True

    def remove_process(self, pid):
        if pid in self.allocated_frames:
            frames = self.allocated_frames.pop(pid)
            self.free_frames.extend(frames)
            self.page_table.pop(pid)
            return True
        return False

class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator - Paging")

        self.total_size_label = tk.Label(root, text="Total Memory Size:")
        self.total_size_label.pack()
        self.total_size_entry = tk.Entry(root)
        self.total_size_entry.pack()

        self.page_size_label = tk.Label(root, text="Page Size:")
        self.page_size_label.pack()
        self.page_size_entry = tk.Entry(root)
        self.page_size_entry.pack()

        self.set_memory_button = tk.Button(root, text="Set Memory", command=self.set_memory)
        self.set_memory_button.pack()

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

    def set_memory(self):
        try:
            total_size = int(self.total_size_entry.get())
            page_size = int(self.page_size_entry.get())
            self.memory = Memory(total_size, page_size)
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter valid integers for total memory size and page size.")

    def add_process(self):
        if self.memory:
            try:
                pid = int(self.process_id_entry.get())
                size = int(self.process_size_entry.get())
                process = Process(pid, size, self.memory.page_size)
                if self.memory.add_process(process):
                    self.update_display()
                else:
                    messagebox.showwarning("Memory Full", "Not enough memory to allocate for the process.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", "Please enter valid integers for process ID and size.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size and page size first.")

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
            messagebox.showerror("No Memory Set", "Please set the total memory size and page size first.")

    def update_display(self):
        if self.memory:
            allocated_text = "Allocated Frames:\n"
            for pid, frames in self.memory.allocated_frames.items():
                allocated_text += f"Process {pid} Page Table:\n"
                for page_num, frame_num in self.memory.page_table[pid].items():
                    allocated_text += f"Page {page_num}: Frame {frame_num}\n"
                allocated_text += "\n"

            free_text = "Free Frames:\n"
            free_text += f"{self.memory.free_frames}\n"

            self.display_text.set(allocated_text + free_text)

    def run(self):
        self.display_text = tk.StringVar()
        self.display_label = tk.Label(self.root, textvariable=self.display_text)
        self.display_label.pack()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    app.run()
