import tkinter as tk
from pages.dynamic import MemoryManagerGUIDynamic
from pages.fixed import MemoryManagerGUIFixed
from pages.page import MemoryManagerGUIPaging
from pages.buddy import MemoryManagerGUIBuddy

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator Launcher")
        self.root.geometry("400x400") 
          

        self.memory_type_label = tk.Label(root, text="Choose Memory Management Type:",)
        self.memory_type_label.pack(pady=(60, 10))

        self.memory_type_var = tk.StringVar(value='dynamic')
        self.dynamic_radio = tk.Radiobutton(root, text="Dynamic Memory Allocation", variable=self.memory_type_var, value='dynamic',justify='right')
        self.dynamic_radio.pack( pady=(0, 10))
        self.fixed_radio = tk.Radiobutton(root, text="Fixed Partition Memory Allocation", variable=self.memory_type_var, value='fixed',justify='left')
        self.fixed_radio.pack(pady=(0, 10))
        self.page_radio = tk.Radiobutton(root, text="Paging Memory Allocation", variable=self.memory_type_var, value='page',justify='left')
        self.page_radio.pack(pady=(0, 10))
        self.page_radio = tk.Radiobutton(root, text="Buddy Memory Allocation", variable=self.memory_type_var, value='buddy',justify='left')
        self.page_radio.pack(pady=(0, 10))

        self.launch_button = tk.Button(root, text="Launch", command=self.launch_program, fg="black", bg="lightblue")
        self.launch_button.pack(anchor="center", ipadx=10, ipady=5)

    def launch_program(self):
        memory_type = self.memory_type_var.get()

        if memory_type == 'dynamic':
            root_dynamic = tk.Toplevel()
            root_dynamic.geometry("400x600")
            app_dynamic = MemoryManagerGUIDynamic(root_dynamic)
            app_dynamic.run()
        elif memory_type == 'fixed':
            root_fixed = tk.Toplevel()
            root_fixed.geometry("400x700")
            app_fixed = MemoryManagerGUIFixed(root_fixed)
            app_fixed.run()
        elif memory_type == 'page':
            root_page = tk.Toplevel()
            root_page.geometry("400x600")
            app_page = MemoryManagerGUIPaging(root_page)
            app_page.run()
        elif memory_type == 'buddy':
            root_buddy = tk.Toplevel()
            root_buddy.geometry("400x700")
            app_buddy = MemoryManagerGUIBuddy(root_buddy)
            app_buddy.run()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
