import tkinter as tk
from tkinter import messagebox

from functions import open_tos
from functions import create_user
from functions import login_user
from functions import delete_user
from functions import create_graph
from functions import select_graph
from functions import delete_graph
from functions import create_pixel
from functions import update_pixel
from functions import delete_pixel

ENTRY_COLOR = "#297F87"

MAIN_COLOR = "#22577A"

_1_COLOR = "#38A3A5"
_2_COLOR = "#57CC99"
_3_COLOR = "#80ED99"

BUTTON_FONT = ("Roboto", 20)
TEXT_FONT = ("Roboto", 15, "bold")
OPTION_MENU_FONT = ("Roboto", 18)


class MainRoot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Progress Checker")
        self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
        self.root.iconbitmap("images/Pixela Logo.ico")
        self.root.resizable(False, False)

        self.user = None
        self.token = None

        self.graph = None
        self.graph_type = None

        self.top_logo = tk.PhotoImage(file="images/Pixela Logo.png")

        self.canvas_top_image = tk.Canvas(height=162, width=606, bg=MAIN_COLOR, highlightthickness=0)
        self.canvas_top_image.grid(column=0, row=0, columnspan=3, pady=20)
        self.canvas_top_image.create_image(303, 81, image=self.top_logo)

        self.create_user_button = tk.Button(text="Create User", bg=_1_COLOR, bd=0, font=BUTTON_FONT, width=20, command=CreateUserRoot)
        self.create_user_button.grid(column=0, row=1, padx=10, pady=10)

        self.select_user_button = tk.Button(text="Select User", bg=_2_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: LoginUserRoot(self))
        self.select_user_button.grid(column=1, row=1, padx=10, pady=10)

        self.delete_user_button = tk.Button(text="Delete User", bg=_3_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: DeleteUserRoot(self))
        self.delete_user_button.grid(column=2, row=1, padx=10, pady=10)

        self.create_graph_button = tk.Button(text="Create Graph", bg=_1_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: CreateGraphRoot(self))
        self.create_graph_button.grid(column=0, row=2, padx=10, pady=10)

        self.select_graph_button = tk.Button(text="Select Graph", bg=_2_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: SelectGraphRoot(self))
        self.select_graph_button.grid(column=1, row=2, padx=10, pady=10)

        self.delete_graph_button = tk.Button(text="Delete Graph", bg=_3_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: DeleteGraphRoot(self))
        self.delete_graph_button.grid(column=2, row=2, padx=10, pady=10)

        self.create_pixel_button = tk.Button(text="Create Pixel", bg=_1_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: CreatePixelRoot(self))
        self.create_pixel_button.grid(column=0, row=3, padx=10, pady=10)

        self.select_pixel_button = tk.Button(text="Update Pixel", bg=_2_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: UpdatePixelRoot(self))
        self.select_pixel_button.grid(column=1, row=3, padx=10, pady=10)

        self.delete_pixel_button = tk.Button(text="Delete Pixel", bg=_3_COLOR, bd=0, font=BUTTON_FONT, width=20, command=lambda: DeletePixelRoot(self))
        self.delete_pixel_button.grid(column=2, row=3, padx=10, pady=10)

        self.check_user = tk.Label(text="Logged as:", bg=MAIN_COLOR, font=TEXT_FONT, fg=_1_COLOR)
        self.check_user.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        self.user_selected = tk.Label(text="No login", bg=MAIN_COLOR, font=TEXT_FONT, fg=_3_COLOR)
        self.user_selected.grid(column=1, row=4, columnspan=2, padx=10)

        self.check_graph = tk.Label(text="Current Graph:", bg=MAIN_COLOR, font=TEXT_FONT, fg=_1_COLOR)
        self.check_graph.grid(column=0, row=5, columnspan=2, padx=10)

        self.graph_selected = tk.Label(text="No graph", bg=MAIN_COLOR, font=TEXT_FONT, fg=_3_COLOR)
        self.graph_selected.grid(column=1, row=5, columnspan=2, padx=10, pady=10)


class CreateUserRoot:
    def __init__(self):
        self.root = tk.Toplevel()

        self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
        self.root.title("New User")
        self.root.iconbitmap("images/Pixela Logo.ico")
        self.root.resizable(False, False)
        self.root.grab_set()
        self.tos_check_value = tk.IntVar()
        self.not_minor_value = tk.IntVar()

        self.username_label = tk.Label(self.root, text="Username", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.username_label.grid(column=0, row=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.username_entry.grid(column=1, row=0, padx=10, pady=10)

        self.token_label = tk.Label(self.root, text="Token", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.token_label.grid(column=0, row=1, padx=10, pady=10)

        self.token_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.token_entry.grid(column=1, row=1, padx=10, pady=10)

        self.not_minor_label = tk.Label(self.root, text="Adult", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.not_minor_label.grid(column=0, row=2, padx=10, pady=10)

        self.not_minor_checkbox = tk.Checkbutton(self.root, bg=MAIN_COLOR, bd=0, activebackground=MAIN_COLOR, selectcolor=MAIN_COLOR, fg="White", variable=self.not_minor_value)
        self.not_minor_checkbox.grid(column=1, row=2, padx=10, pady=10, sticky="W")

        self.tos_label = tk.Label(self.root, text="Agree TOS", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR, cursor="hand2")
        self.tos_label.grid(column=1, row=2, padx=10, pady=10)
        self.tos_label.bind("<Button-1>", lambda fun: open_tos("https://github.com/a-know/Pixela/wiki/Terms-of-Service"))

        self.tos_checkbox = tk.Checkbutton(self.root, bg=MAIN_COLOR, bd=0, activebackground=MAIN_COLOR, selectcolor=MAIN_COLOR, fg="White", variable=self.tos_check_value)
        self.tos_checkbox.grid(column=1, row=2, padx=10, pady=10, sticky="E")

        self.create_user_button = tk.Button(self.root, text="Create New User", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: create_user(self))
        self.create_user_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="EW")


class LoginUserRoot:
    def __init__(self, main_root):
        self.root = tk.Toplevel()
        self.main_root = main_root

        self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
        self.root.title("Login User")
        self.root.iconbitmap("images/Pixela Logo.ico")
        self.root.resizable(False, False)
        self.root.grab_set()

        self.username_label = tk.Label(self.root, text="Username", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.username_label.grid(column=0, row=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.username_entry.grid(column=1, row=0, padx=10, pady=10)

        self.token_label = tk.Label(self.root, text="Token", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.token_label.grid(column=0, row=1, padx=10, pady=10)

        self.token_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.token_entry.grid(column=1, row=1, padx=10, pady=10)

        self.login_user_button = tk.Button(self.root, text="Login User", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: login_user(self))
        self.login_user_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="EW")


class DeleteUserRoot:
    def __init__(self, main_root):
        self.root = tk.Toplevel()
        self.main_root = main_root

        self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
        self.root.title("Delete User")
        self.root.iconbitmap("images/Pixela Logo.ico")
        self.root.resizable(False, False)
        self.root.grab_set()

        self.username_label = tk.Label(self.root, text="Username", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.username_label.grid(column=0, row=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.username_entry.grid(column=1, row=0, padx=10, pady=10)

        self.token_label = tk.Label(self.root, text="Token", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
        self.token_label.grid(column=0, row=1, padx=10, pady=10)

        self.token_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
        self.token_entry.grid(column=1, row=1, padx=10, pady=10)

        self.login_user_button = tk.Button(self.root, text="Delete User", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: delete_user(self))
        self.login_user_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="EW")


class CreateGraphRoot:
    def __init__(self, main_root):

        if main_root.user is not None:
            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Create Graph")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.graph_name_label = tk.Label(self.root, text="Name", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_name_label.grid(column=0, row=0, padx=10, pady=10)

            self.graph_name_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.graph_name_entry.grid(column=1, row=0, padx=10, pady=10)

            self.graph_id_label = tk.Label(self.root, text="ID", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_id_label.grid(column=0, row=1, padx=10, pady=10)

            self.graph_id_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.graph_id_entry.grid(column=1, row=1, padx=10, pady=10)

            self.graph_unit_label = tk.Label(self.root, text="Unit", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_unit_label.grid(column=0, row=2, padx=10, pady=10)

            self.graph_unit_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.graph_unit_entry.grid(column=1, row=2, padx=10, pady=10)

            self.graph_type_label = tk.Label(self.root, text="Type", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_type_label.grid(column=0, row=3, padx=10, pady=10)

            self.graph_type_options = ["Integer Number", "Floating Point Number"]
            self.graph_type_value = tk.StringVar(self.root)
            self.graph_type_value.set(self.graph_type_options[0])

            self.graph_type_option = tk.OptionMenu(self.root, self.graph_type_value, *self.graph_type_options)
            self.graph_type_option.config(bd=0, bg=ENTRY_COLOR, activebackground=ENTRY_COLOR, highlightthickness=0, font=OPTION_MENU_FONT)
            self.graph_type_option.grid(column=1, row=3, padx=10, pady=10, sticky="EW")

            self.graph_color_label = tk.Label(self.root, text="Color", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_color_label.grid(column=0, row=4, padx=10, pady=10)

            self.graph_color_options = ["Green", "Red", "Blue", "Yellow", "Purple", "Black"]
            self.graph_color_value = tk.StringVar(self.root)
            self.graph_color_value.set(self.graph_color_options[0])

            self.graph_color_option = tk.OptionMenu(self.root, self.graph_color_value, *self.graph_color_options)
            self.graph_color_option.config(bd=0, bg=ENTRY_COLOR, activebackground=ENTRY_COLOR, highlightthickness=0, font=OPTION_MENU_FONT)
            self.graph_color_option.grid(column=1, row=4, padx=10, pady=10, sticky="EW")

            self.login_user_button = tk.Button(self.root, text="Create Graph", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: create_graph(self))
            self.login_user_button.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("Not Logged.", "You must be logged for create a graph.")


class SelectGraphRoot:
    def __init__(self, main_root):

        if main_root.user is not None:
            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Select Graph")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.graph_id_label = tk.Label(self.root, text="Graph ID", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_id_label.grid(column=0, row=0, padx=10, pady=10)

            self.graph_id_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.graph_id_entry.grid(column=1, row=0, padx=10, pady=10)

            self.select_graph_button = tk.Button(self.root, text="Select Graph", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: select_graph(self))
            self.select_graph_button.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("Not Logged.", "You must be logged for select a graph.")


class DeleteGraphRoot:
    def __init__(self, main_root):

        if main_root.user is not None:
            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Delete Graph")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.graph_id_label = tk.Label(self.root, text="Graph ID", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.graph_id_label.grid(column=0, row=0, padx=10, pady=10)

            self.graph_id_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.graph_id_entry.grid(column=1, row=0, padx=10, pady=10)

            self.select_graph_button = tk.Button(self.root, text="Delete Graph", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: delete_graph(self))
            self.select_graph_button.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("Not Logged.", "You must be logged for delete a graph.")


class CreatePixelRoot:
    def __init__(self, main_root):

        if main_root.graph is not None:

            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Create Pixel")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.root.day_label = tk.Label(self.root, text="Day", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.day_label.grid(column=0, row=0, padx=10, pady=10)

            self.root.day_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.day_entry.grid(column=1, row=0, padx=10, pady=10)

            self.root.month_label = tk.Label(self.root, text="Month", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.month_label.grid(column=0, row=1, padx=10, pady=10)

            self.root.month_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.month_entry.grid(column=1, row=1, padx=10, pady=10)

            self.root.year_label = tk.Label(self.root, text="Year", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.year_label.grid(column=0, row=2, padx=10, pady=10)

            self.root.year_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.year_entry.grid(column=1, row=2, padx=10, pady=10)

            self.root.quantity_label = tk.Label(self.root, text="Quantity", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.quantity_label.grid(column=0, row=3, padx=10, pady=10)

            self.root.quantity_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.quantity_entry.grid(column=1, row=3, padx=10, pady=10)

            self.select_graph_button = tk.Button(self.root, text="Create Pixel", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: create_pixel(self))
            self.select_graph_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("No graph selected.", "You must select a graph for create a pixel.")


class UpdatePixelRoot:
    def __init__(self, main_root):
        if main_root.graph is not None:

            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Update Pixel")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.root.day_label = tk.Label(self.root, text="Day", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.day_label.grid(column=0, row=0, padx=10, pady=10)

            self.root.day_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.day_entry.grid(column=1, row=0, padx=10, pady=10)

            self.root.month_label = tk.Label(self.root, text="Month", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.month_label.grid(column=0, row=1, padx=10, pady=10)

            self.root.month_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.month_entry.grid(column=1, row=1, padx=10, pady=10)

            self.root.year_label = tk.Label(self.root, text="Year", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.year_label.grid(column=0, row=2, padx=10, pady=10)

            self.root.year_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.year_entry.grid(column=1, row=2, padx=10, pady=10)

            self.root.quantity_label = tk.Label(self.root, text="Quantity", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.quantity_label.grid(column=0, row=3, padx=10, pady=10)

            self.root.quantity_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.quantity_entry.grid(column=1, row=3, padx=10, pady=10)

            self.select_graph_button = tk.Button(self.root, text="Update Pixel", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: update_pixel(self))
            self.select_graph_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("No graph selected.", "You must select a graph for update a pixel.")


class DeletePixelRoot:
    def __init__(self, main_root):
        if main_root.graph is not None:

            self.root = tk.Toplevel()
            self.main_root = main_root

            self.root.config(bg=MAIN_COLOR, padx=20, pady=20)
            self.root.title("Delete Pixel")
            self.root.iconbitmap("images/Pixela Logo.ico")
            self.root.resizable(False, False)
            self.root.grab_set()

            self.root.day_label = tk.Label(self.root, text="Day", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.day_label.grid(column=0, row=0, padx=10, pady=10)

            self.root.day_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.day_entry.grid(column=1, row=0, padx=10, pady=10)

            self.root.month_label = tk.Label(self.root, text="Month", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.month_label.grid(column=0, row=1, padx=10, pady=10)

            self.root.month_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.month_entry.grid(column=1, row=1, padx=10, pady=10)

            self.root.year_label = tk.Label(self.root, text="Year", font=BUTTON_FONT, bg=MAIN_COLOR, fg=_2_COLOR)
            self.root.year_label.grid(column=0, row=2, padx=10, pady=10)

            self.root.year_entry = tk.Entry(self.root, bd=0, font=BUTTON_FONT, justify="center", bg=ENTRY_COLOR)
            self.root.year_entry.grid(column=1, row=2, padx=10, pady=10)

            self.select_graph_button = tk.Button(self.root, text="Delete Pixel", font=BUTTON_FONT, bg=_3_COLOR, bd=0, command=lambda: delete_pixel(self))
            self.select_graph_button.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="EW")

        else:
            messagebox.showerror("No graph selected.", "You must select a graph for delete a pixel.")
