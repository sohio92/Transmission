from tkinter import *
from Window import Window

if __name__ == '__main__':
    root = Tk()

    app = Window(root)

    root.resizable(False, False)
    root.mainloop()