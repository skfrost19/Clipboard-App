import tkinter as tk
from tkinter import filedialog
import pyperclip

class ClipboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.clipboard_text = []
        self.title("Clipboard Example")
        self.iconphoto(False, tk.PhotoImage(file='/media/skfrost19/New Volume/Clipboard-GUI/clipboard.png'))
        self.geometry("1000x600")
        # craete a navbar menu
        self.create_menu()

        # Create the listbox widget
        self.listbox = tk.Listbox(self)
        # self.listbox.config(bg="black", fg="white")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the scrollbar and connect it to the listbox
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Set up clipboard listener
        self.after(1000, self.check_clipboard)

    def check_clipboard(self):
        # Get the clipboard contents
        clipboard_data = pyperclip.paste()

        # If the clipboard contains text and it is not already in the list, add it
        if isinstance(clipboard_data, str) and clipboard_data not in self.clipboard_text:
            self.clipboard_text.append(clipboard_data)
            # add new text on top
            self.listbox.insert(0, clipboard_data)

        # Check the clipboard again in 1 second
        self.after(1000, self.check_clipboard)

    def clear_list(self):
        # Clear the listbox and the clipboard_text list
        self.listbox.delete(0, tk.END)
        self.clipboard_text = []

    def create_menu(self):
        # Create a menu bar
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # Create a File menu
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.destroy)

        # Create an Edit menu
        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.file_menu.add_command(label="Export", command=self.export)
        self.edit_menu.add_command(label="Clear", command=self.clear_list)
    
    def export(self):
        # save the file
        file_path = filedialog.asksaveasfilename(initialdir='/', title='Save File', defaultextension='.txt')
        if file_path:
            count = 1
            with open(file_path, 'w') as f:
                for item in self.clipboard_text:
                    f.write(f"\t\tClipboard {count}\t\t")
                    f.write("\n=====================================\n")
                    f.write(item)
                    f.write("\n=====================================\n\n")
                    count += 1
            f.close()
        else:
            print("File not saved")

    def toggle_saved_clipboard(self, event):
        if self.clipboard_text:
            # select the item that was clicked on 
            index = self.listbox.curselection()[0]
            # get the text of the item
            item = self.listbox.get(index)
            pyperclip.copy(item)
            self.clipboard_text = []
            self.listbox.delete(0, tk.END)
        else:
            clipboard_data = pyperclip.paste()
            if isinstance(clipboard_data, str):
                self.clipboard_text.append(clipboard_data)
                # add new text on top
                self.listbox.insert(0, clipboard_data)


if __name__ == "__main__":
    app = ClipboardApp()
    app.mainloop()