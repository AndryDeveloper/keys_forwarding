import tkinter as tk

def ctrlEvent(event):
    if(12==event.state and event.keysym=='c' ):
        return
    else:
        return "break"

root = tk.Tk()
readOnlyText = tk.Text(root)
readOnlyText.insert(1.0,"ABCDEF")
readOnlyText.bind("<Key>", lambda e: ctrlEvent(e))
readOnlyText.pack()

root.mainloop()