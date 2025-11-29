import tkinter as tk
from blogging.gui.blogging_gui import BloggingGUI

def main():
    root = tk.Tk()
    gui = BloggingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
