import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox

# Extra tools
# https://github.com/alejandroautalan/pygubu

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Tkinter App")
        self.root.geometry("600x400")  # Set initial window size
        
        # Initialize the UI
        self.__create_menu()
        self.__create_widgets()

        # Initialize tkinter variables
        self.string_var = tk.StringVar()
        self.bool_var = tk.BooleanVar()

    def start(self):
        self.__setup_keybind()

        self.root.mainloop()

    # UI related
    def __setup_keybind(self):
        # Special action
        self.root.bind("<Control-w>", lambda event: self.root.quit())

    def __create_menu(self):
        """Creates a menu bar with some basic options."""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.__new_file)
        file_menu.add_command(label="Open", command=self.__open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.__show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Attach the menu to the window
        self.root.config(menu=menubar)
        
    def __create_widgets(self):
        """Creates the main widgets for the app."""
        # TODO: Change here for custom UI
        self.label = ttk.Label(self.root, text="Hello, Tkinter!", font=("Arial", 16))
        self.label.pack(pady=20)
        
        self.button = ttk.Button(self.root, text="Click Me", command=self.__on_button_click)
        self.button.pack(pady=10)
        
        self.entry = ttk.Entry(self.root, width=40)
        self.entry.pack(pady=10)
    
    # Helper function
    def __create_entry(self, label_text, variable):
        """Helper method to create labeled entry fields."""
        self.root.call(
            "grid",
            ttk.Label(self.root, text=label_text),
            ttk.Entry(self.root, textvariable=variable),
            "-padx",
            "10",
            "-pady",
            "5",
        )

    def __create_combobox(self, label_text, variable, values, default=None):
        """Helper method to create labeled entry fields."""
        label = ttk.Label(self.root, text=label_text)
        combobox = AutocompleteCombobox(self.root, textvariable=variable, completevalues=values)
        self.root.call("grid", label, combobox, "-padx", "10", "-pady", "5")

        if default:
            combobox.set(default)

    # Menu event related function
    def __new_file(self):
        """Event handler for the 'New' menu item."""
        messagebox.showinfo("New File", "Create a new file.")

    def __open_file(self):
        """Event handler for the 'Open' menu item."""
        messagebox.showinfo("Open File", "Open an existing file.")
        
    def __show_about(self):
        """Event handler for the 'About' menu item."""
        messagebox.showinfo("About", "This is a sample Tkinter app template.")

    # Widget event related function
    def __on_button_click(self):
        """Event handler for the sample button."""
        text = self.entry.get()
        if text:
            messagebox.showinfo("Input", f"You entered: {text}")
        else:
            messagebox.showwarning("Warning", "Please enter some text.")
            

if __name__ == "__main__":
    app = MyApp()
    app.start()
