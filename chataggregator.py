import tklib
import tkinter as tk

root = tk.Tk()
root.title("Chatbox")
config = tklib.models.Config()
gui = tklib.main.MainWindow(root, config)
gui.grid()
root.mainloop()