import tkinter as tk

class MainPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.geometry("250x300+100+100")

        label = tk.Label(root, text="Welcome to the Main Page!")
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    main_page_gui = MainPageGUI(root)
    root.mainloop()
