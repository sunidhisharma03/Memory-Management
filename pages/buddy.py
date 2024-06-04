import tkinter as tk
from tkinter import messagebox


class Process:import tkinter as tk
from tkinter import messagebox


class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size


class MemoryBlock:
    def __init__(self, size, start_address):
        self.size = size
        self.start_address = start_address
        self.end_address = start_address + size - 1
        self.is_allocated = False
        self.left_child = None
        self.right_child = None
        self.parent = None


class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.root_block = MemoryBlock(total_size, 0)

    def allocate_memory(self, process_size):
        block = self._find_block(self.root_block, process_size)
        if block:
            print("Found block:", block.start_address, block.size)  # Debugging print statement
            self._split_block(block, process_size)
            block.is_allocated = True
            return block.start_address
        else:
            print("No suitable block found")  # Debugging print statement
            return -1

    def deallocate_memory(self, start_address):
        block = self._find_block_by_address(self.root_block, start_address)
        if block:
            block.is_allocated = False
            self._merge_block(block)

    def _find_block(self, node, process_size):
        if node.is_allocated or node.size < process_size:
            return None
        if node.size == process_size:
            return node
        left_block = self._find_block(node.left_child, process_size)
        if left_block:
            return left_block
        return self._find_block(node.right_child, process_size)

    def _split_block(self, block, process_size):
        while block.size > process_size:
            block.left_child = MemoryBlock(block.size // 2, block.start_address)
            block.right_child = MemoryBlock(block.size // 2, block.start_address + block.size // 2)
            block.left_child.parent = block
            block.right_child.parent = block
            block.right_child.start_address = block.start_address + block.size // 2  # Fix
            block = block.left_child if process_size <= block.size // 2 else block.right_child

    def _merge_block(self, block):
        while block.parent and not block.parent.left_child.is_allocated and not block.parent.right_child.is_allocated:
            block.parent.left_child = None
            block.parent.right_child = None
            block = block.parent
    def _find_block(self, node, process_size):
        if node is None:
            return None
        if node.is_allocated or node.size < process_size:
            return None
        if node.size == process_size:
            return node
        left_block = None
        right_block = None
        if node.left_child:
            left_block = self._find_block(node.left_child, process_size)
        if node.right_child:
            right_block = self._find_block(node.right_child, process_size)
        return left_block if left_block else right_block




class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator - Buddy")

        self.total_size_label = tk.Label(root, text="Total Memory Size:")
        self.total_size_label.pack()
        self.total_size_entry = tk.Entry(root)
        self.total_size_entry.pack()

        self.set_memory_button = tk.Button(root, text="Set Memory", command=self.set_memory)
        self.set_memory_button.pack()

        self.process_size_label = tk.Label(root, text="Process Size:")
        self.process_size_label.pack()
        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.pack()
        self.add_process_button = tk.Button(root, text="Allocate Memory", command=self.add_process)
        self.add_process_button.pack()
        self.remove_process_button = tk.Button(root, text="Deallocate Memory", command=self.remove_process)
        self.remove_process_button.pack()

        self.memory_manager = None

    def set_memory(self):
        try:
            total_size = int(self.total_size_entry.get())
            self.memory_manager = MemoryManager(total_size)
            messagebox.showinfo("Memory Set", f"Memory set successfully with total size {total_size}.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for total memory size.")

    def add_process(self):
        if self.memory_manager:
            try:
                size = int(self.process_size_entry.get())
                start_address = self.memory_manager.allocate_memory(size)
                if start_address != -1:
                    messagebox.showinfo("Memory Allocated", f"Memory allocated at address {start_address}.")
                else:
                    messagebox.showwarning("Memory Full", "Not enough memory to allocate for the process.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for process size.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def remove_process(self):
        if self.memory_manager:
            try:
                start_address = int(self.process_size_entry.get())
                self.memory_manager.deallocate_memory(start_address)
                messagebox.showinfo("Memory Deallocated", "Memory deallocated successfully.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for memory address.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    app.run()
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size


class MemoryBlock:
    def __init__(self, size, start_address):
        self.size = size
        self.start_address = start_address
        self.end_address = start_address + size - 1
        self.is_allocated = False
        self.left_child = None
        self.right_child = None
        self.parent = None


class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.root_block = MemoryBlock(total_size, 0)

    def allocate_memory(self, process_size):
        block = self._find_block(self.root_block, process_size)
        if block:
            print("Found block:", block.start_address, block.size)  # Debugging print statement
            self._split_block(block, process_size)
            block.is_allocated = True
            return block.start_address
        else:
            print("No suitable block found")  # Debugging print statement
            return -1

    def deallocate_memory(self, start_address):
        block = self._find_block_by_address(self.root_block, start_address)
        if block:
            block.is_allocated = False
            self._merge_block(block)

    def _find_block(self, node, process_size):
        if node.is_allocated or node.size < process_size:
            return None
        if node.size == process_size:
            return node
        left_block = self._find_block(node.left_child, process_size)
        if left_block:
            return left_block
        return self._find_block(node.right_child, process_size)

    def _split_block(self, block, process_size):
        while block.size > process_size:
            block.left_child = MemoryBlock(block.size // 2, block.start_address)
            block.right_child = MemoryBlock(block.size // 2, block.start_address + block.size // 2)
            block.left_child.parent = block
            block.right_child.parent = block
            block.right_child.start_address = block.start_address + block.size // 2  # Fix
            block = block.left_child if process_size <= block.size // 2 else block.right_child

    def _merge_block(self, block):
        while block.parent and not block.parent.left_child.is_allocated and not block.parent.right_child.is_allocated:
            block.parent.left_child = None
            block.parent.right_child = None
            block = block.parent
    def _find_block(self, node, process_size):
        if node is None:
            return None
        if node.is_allocated or node.size < process_size:
            return None
        if node.size == process_size:
            return node
        left_block = None
        right_block = None
        if node.left_child:
            left_block = self._find_block(node.left_child, process_size)
        if node.right_child:
            right_block = self._find_block(node.right_child, process_size)
        return left_block if left_block else right_block




class  MemoryManagerGUIBuddy:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")

        self.total_size_label = tk.Label(root, text="Total Memory Size:")
        self.total_size_label.pack()
        self.total_size_entry = tk.Entry(root)
        self.total_size_entry.pack()

        self.set_memory_button = tk.Button(root, text="Set Memory", command=self.set_memory)
        self.set_memory_button.pack()

        self.process_size_label = tk.Label(root, text="Process Size:")
        self.process_size_label.pack()
        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.pack()
        self.add_process_button = tk.Button(root, text="Allocate Memory", command=self.add_process)
        self.add_process_button.pack()
        self.remove_process_button = tk.Button(root, text="Deallocate Memory", command=self.remove_process)
        self.remove_process_button.pack()

        self.memory_manager = None

    def set_memory(self):
        try:
            total_size = int(self.total_size_entry.get())
            self.memory_manager = MemoryManager(total_size)
            messagebox.showinfo("Memory Set", f"Memory set successfully with total size {total_size}.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for total memory size.")

    def add_process(self):
        if self.memory_manager:
            try:
                size = int(self.process_size_entry.get())
                start_address = self.memory_manager.allocate_memory(size)
                if start_address != -1:
                    messagebox.showinfo("Memory Allocated", f"Memory allocated at address {start_address}.")
                else:
                    messagebox.showwarning("Memory Full", "Not enough memory to allocate for the process.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for process size.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def remove_process(self):
        if self.memory_manager:
            try:
                start_address = int(self.process_size_entry.get())
                self.memory_manager.deallocate_memory(start_address)
                messagebox.showinfo("Memory Deallocated", "Memory deallocated successfully.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for memory address.")
        else:
            messagebox.showerror("No Memory Set", "Please set the total memory size first.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400") 
    app =  MemoryManagerGUIBuddy(root)
    app.run()
