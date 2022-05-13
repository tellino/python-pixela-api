import requests

from threading import Thread
from datetime import datetime
from webbrowser import open_new
from tkinter import messagebox

PIXELA_ENDPOINT = "https://pixe.la/v1/users"


def open_tos(*args):
    open_new(args[0])


def check(string, type_):
    numbers = "0123456789"
    valid_char = "abcdefghijklmnopqrstuvwxyz" + numbers

    if type_ == "username":
        username = string

        if not 1 <= len(username) <= 32:
            return False, "Username length must be 1 to 32 characters."

        if username[0] in numbers:
            return False, "Username cannot start with a digit."

        for char in username:
            if char not in valid_char:
                return False, "Username cannot contain special characters."

        return True, None

    elif type_ == "token":
        token = string

        if not 8 <= len(token) <= 128:
            return False, "Token length must be 8 to 128 characters."

        return True, None

    elif type_ == "id":
        _id = string

        if not 1 <= len(_id) <= 16:
            return False, "ID length must be 1 to 16 characters."

        if _id[0] in numbers:
            return False, "ID cannot start with a digit."

        for char in _id:
            if char not in valid_char:
                return False, "ID cannot contain special characters."

        return True, None


def update_login(*args):
    main = args[0]
    username = args[1]
    token = args[2]

    try:
        graph = args[3]
        if graph is None:
            main.graph_selected.config(text="No graph")
            main.graph = graph

        else:
            main.graph_selected.config(text=graph)

    except IndexError:
        pass

    try:
        graph_type = args[4]
        if graph_type is None:
            main.graph_type = graph_type

    except IndexError:
        pass

    main.user_selected.config(text=username)
    main.user = username
    main.token = token


def update_graph(*args):
    main = args[0]
    graph_name = args[1]
    graph_type = args[2]

    if graph_name is None:
        main.graph_selected.config(text="No graph")

    else:
        main.graph_selected.config(text=graph_name)

    main.graph = graph_name
    main.graph_type = graph_type


def monitor(self, thread, window_name, info_text, fun=None, *fun_args):
    if thread.is_alive():
        self.root.after(100, lambda: monitor(self, thread, window_name, info_text, fun, *fun_args))

    else:
        if thread.status_code == 200:
            messagebox.showinfo(window_name, info_text)
            if fun is not None:
                fun(*fun_args)

            self.root.destroy()

        elif thread.status_code == 400:
            messagebox.showerror("Error", f"The credentials aren't correct.")

        else:
            messagebox.showerror("Error", f"An error occurred.\nError code: {thread.status_code}.")


def get_graph_name(user, token, id_):
    url = f"{PIXELA_ENDPOINT}/{str(user)}/graphs"
    headers = {"X-USER-TOKEN": str(token)}

    response = requests.get(url, headers=headers)
    graphs = response.json()['graphs']

    for graph in graphs:
        if graph["id"] == id_:
            return graph["name"]

    return None


def get_graph_type(user, token, id_):
    url = f"{PIXELA_ENDPOINT}/{str(user)}/graphs"
    headers = {"X-USER-TOKEN": str(token)}

    response = requests.get(url, headers=headers)
    graphs = response.json()['graphs']

    for graph in graphs:
        if graph["id"] == id_:
            return graph["type"]

    return None


def get_graph_id(user, token, name):
    url = f"{PIXELA_ENDPOINT}/{str(user)}/graphs"
    headers = {"X-USER-TOKEN": str(token)}

    response = requests.get(url, headers=headers)
    graphs = response.json()['graphs']

    for graph in graphs:
        if graph["name"] == name:
            return graph["id"]

    return None


def is_int(string):
    try:
        int(string)
        return True

    except ValueError:
        return False


def is_float(string):
    if "." not in string:
        return False

    else:
        try:
            float(string)
            return True

        except ValueError:
            return False


def create_user(self):
    user_check = check(self.username_entry.get(), "username")

    if user_check[0]:
        token_check = check(self.token_entry.get(), "token")

        if token_check[0]:
            if self.not_minor_value.get() == 1:
                if self.tos_check_value.get() == 1:

                    params = {
                        "token": self.token_entry.get(),
                        "username": self.username_entry.get(),
                        "agreeTermsOfService": "yes",
                        "notMinor": "yes"
                    }

                    new_user_thread = AsyncRequest(action="create_user", params=params)
                    new_user_thread.start()

                    monitor(self, new_user_thread, "Success", f"User {self.username_entry.get()} has been created!")

                else:
                    messagebox.showerror("TOS Not accepted", "You must accept the TOS to use Pixela API.")

            else:
                messagebox.showerror("Invalid age", "You must be an adult to use Pixela API.")

        else:
            messagebox.showerror("Invalid Token", f"Token is not valid.\n{token_check[1]}")

    else:
        messagebox.showerror("Invalid Username", f"Username is not valid.\n{user_check[1]}")


def login_user(self):
    user_check = check(self.username_entry.get(), "username")

    if user_check[0]:
        token_check = check(self.token_entry.get(), "token")

        if token_check[0]:
            headers = {
                "X-USER-TOKEN": self.token_entry.get()
            }

            params = {
                "newToken": self.token_entry.get()
            }

            login_user_thread = AsyncRequest(action="login_user", params=params, headers=headers, user=self.username_entry.get())
            login_user_thread.start()

            monitor(self, login_user_thread, "Success", f"Logged as {self.username_entry.get()}!", update_login, self.main_root, self.username_entry.get(), self.token_entry.get())

        else:
            messagebox.showerror("Invalid Token", f"Token is not valid.\n{token_check[1]}")

    else:
        messagebox.showerror("Invalid Username", f"Username is not valid.\n{user_check[1]}")


def delete_user(self):
    user_check = check(self.username_entry.get(), "username")

    if user_check[0]:
        token_check = check(self.token_entry.get(), "token")

        if token_check[0]:
            headers = {
                "X-USER-TOKEN": self.token_entry.get()
            }

            params = {
                "newToken": self.token_entry.get()
            }

            login_user_thread = AsyncRequest(action="delete_user", params=params, headers=headers, user=self.username_entry.get())
            login_user_thread.start()

            monitor(self, login_user_thread, "Success", f"User {self.username_entry.get()} deleted!", update_login, self.main_root, None, None, None, None)

        else:
            messagebox.showerror("Invalid Token", f"Token is not valid.\n{token_check[1]}")

    else:
        messagebox.showerror("Invalid Username", f"Username is not valid.\n{user_check[1]}")


def create_graph(self):
    if self.main_root.user is not None:
        if len(self.graph_name_entry.get()) > 0:
            id_check = check(self.graph_id_entry.get(), "id")

            if id_check[0]:
                if len(self.graph_unit_entry.get()) > 0:

                    if self.graph_type_value.get() == "Integer Number":
                        type_ = "int"

                    else:
                        type_ = "float"

                    if self.graph_color_value.get() == "Green":
                        color = "shibafu"

                    elif self.graph_color_value.get() == "Red":
                        color = "momiji"

                    elif self.graph_color_value.get() == "Blue":
                        color = "sora"

                    elif self.graph_color_value.get() == "Yellow":
                        color = "ichou"

                    elif self.graph_color_value.get() == "Purple":
                        color = "ajisai"

                    else:
                        color = "kuro"

                    params = {
                        "id": self.graph_id_entry.get(),
                        "name": self.graph_name_entry.get(),
                        "unit": self.graph_unit_entry.get(),
                        "type": type_,
                        "color": color
                    }

                    headers = {
                        "X-USER-TOKEN": self.main_root.token
                    }

                    create_graph_thread = AsyncRequest(action="create_graph", params=params, headers=headers, user=self.main_root.user)
                    create_graph_thread.start()

                    monitor(self, create_graph_thread, "Success", f"Graph {self.graph_name_entry.get()} created!")

                else:
                    messagebox.showerror("Invalid Unit.", f"Unit field cannot be empty.")

            else:
                messagebox.showerror("Invalid ID.", f"ID is not valid.\n{id_check[1]}")

        else:
            messagebox.showerror("Name Error.", "The name field cannot be empty.")

    else:
        messagebox.showerror("Not Logged.", "You must be logged for create a graph.")


def select_graph(self):
    id_check = check(self.graph_id_entry.get(), "id")

    if self.main_root.user is not None:
        if id_check[0]:
            headers = {"X-USER-TOKEN": self.main_root.token}

            select_graph_thread = AsyncRequest(action="select_graph", headers=headers, user=self.main_root.user, id_=self.graph_id_entry.get(), main_root=self.main_root, window=self)
            select_graph_thread.start()

        else:
            messagebox.showerror("Invalid ID", f"ID is not valid\n{id_check[1]}")

    else:
        messagebox.showerror("Not Logged.", "You must be logged for create a graph.")


def delete_graph(self):
    id_check = check(self.graph_id_entry.get(), "id")

    if self.main_root.user is not None:
        if id_check[0]:
            headers = {"X-USER-TOKEN": self.main_root.token}

            delete_graph_thread = AsyncRequest(action="delete_graph", headers=headers, user=self.main_root.user, id_=self.graph_id_entry.get(), main_root=self.main_root, window=self)
            delete_graph_thread.start()

        else:
            messagebox.showerror("Invalid ID", f"ID is not valid\n{id_check[1]}")

    else:
        messagebox.showerror("Not Logged.", "You must be logged for create a graph.")


def create_pixel(self):
    if len(self.root.day_entry.get()) == 0:
        messagebox.showerror("Day Error", "Day field cannot be empty.")

    else:
        try:
            day = int(self.root.day_entry.get())

            if 1 <= day <= 31:
                if len(self.root.month_entry.get()) == 0:
                    messagebox.showerror("Month Error", "Month field cannot be empty.")

                else:
                    try:
                        month = int(self.root.month_entry.get())

                        if 1 <= month <= 12:
                            if len(self.root.year_entry.get()) == 0:
                                messagebox.showerror("Year Error", "Year field cannot be empty.")

                            else:
                                try:
                                    year = int(self.root.year_entry.get())

                                    if 2000 <= year <= datetime.now().year:
                                        quantity = self.root.quantity_entry.get()

                                        if len(quantity) == 0:
                                            messagebox.showerror("Quantity Error", "Quantity field cannot be empty.")

                                        else:
                                            if self.main_root.graph_type == "int":
                                                if is_int(quantity):

                                                    headers = {"X-USER-TOKEN": self.main_root.token}

                                                    json = {
                                                        "date": f"{year}{str(month).zfill(2)}{str(day).zfill(2)}",
                                                        "quantity": quantity
                                                    }

                                                    create_pixel_thread = AsyncRequest(action="create_pixel", params=json, headers=headers, user=self.main_root.user, id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                                    create_pixel_thread.start()

                                                    monitor(self, create_pixel_thread, "Success", f"Pixel registered!")

                                                else:
                                                    messagebox.showerror("Quantity Error", "This graph accepts only integer quantities.")

                                            elif self.main_root.graph_type == "float":
                                                if is_float(quantity):

                                                    headers = {"X-USER-TOKEN": self.main_root.token}
                                                    json = {
                                                        "date": f"{year}{str(month).zfill(2)}{str(day).zfill(2)}",
                                                        "quantity": quantity
                                                    }

                                                    create_pixel_thread = AsyncRequest(action="create_pixel", params=json, headers=headers, user=self.main_root.user, id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                                    create_pixel_thread.start()

                                                    monitor(self, create_pixel_thread, "Success", f"Pixel Registered!")

                                                else:
                                                    messagebox.showerror("Quantity Error", "This graph accepts only floating point quantities.")

                                            else:
                                                messagebox.showerror("Graph Type Error", f"The graph type is {self.main_root.graph_type}.")

                                    else:
                                        messagebox.showerror("Year Error", f"Year must be between 2000 and {datetime.now().year}.")

                                except ValueError:
                                    messagebox.showerror("Year Error", "Year must be an integer.")

                        else:
                            messagebox.showerror("Month Error", "Month must be between 1 and 12.")

                    except ValueError:
                        messagebox.showerror("Month Error", "Month must be an integer.")

            else:
                messagebox.showerror("Day Error", "Day must be between 1 and 31.")

        except ValueError:
            messagebox.showerror("Day Error", "Day must be an integer.")


def update_pixel(self):
    if len(self.root.day_entry.get()) == 0:
        messagebox.showerror("Day Error", "Day field cannot be empty.")

    else:
        try:
            day = int(self.root.day_entry.get())

            if 1 <= day <= 31:
                if len(self.root.month_entry.get()) == 0:
                    messagebox.showerror("Month Error", "Month field cannot be empty.")

                else:
                    try:
                        month = int(self.root.month_entry.get())

                        if 1 <= month <= 12:
                            if len(self.root.year_entry.get()) == 0:
                                messagebox.showerror("Year Error", "Year field cannot be empty.")

                            else:
                                try:
                                    year = int(self.root.year_entry.get())

                                    if 2000 <= year <= datetime.now().year:
                                        quantity = self.root.quantity_entry.get()

                                        if len(quantity) == 0:
                                            messagebox.showerror("Quantity Error", "Quantity field cannot be empty.")

                                        else:
                                            if self.main_root.graph_type == "int":
                                                if is_int(quantity):

                                                    headers = {"X-USER-TOKEN": self.main_root.token}

                                                    json = {
                                                        "quantity": quantity
                                                    }

                                                    create_pixel_thread = AsyncRequest(action="update_pixel", params=json, headers=headers, user=self.main_root.user, date=f"{year}{str(month).zfill(2)}{str(day).zfill(2)}", id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                                    create_pixel_thread.start()

                                                    monitor(self, create_pixel_thread, "Success", f"Pixel updated!")

                                                else:
                                                    messagebox.showerror("Quantity Error", "This graph accepts only integer quantities.")

                                            elif self.main_root.graph_type == "float":
                                                if is_float(quantity):

                                                    headers = {"X-USER-TOKEN": self.main_root.token}
                                                    json = {
                                                        "quantity": quantity
                                                    }

                                                    create_pixel_thread = AsyncRequest(action="update_pixel", params=json, headers=headers, user=self.main_root.user, date=f"{year}{str(month).zfill(2)}{str(day).zfill(2)}", id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                                    create_pixel_thread.start()

                                                    monitor(self, create_pixel_thread, "Success", f"Pixel updated!")

                                                else:
                                                    messagebox.showerror("Quantity Error", "This graph accepts only floating point quantities.")

                                            else:
                                                messagebox.showerror("Graph Type Error", f"The graph type is {self.main_root.graph_type}.")

                                    else:
                                        messagebox.showerror("Year Error", f"Year must be between 2000 and {datetime.now().year}.")

                                except ValueError:
                                    messagebox.showerror("Year Error", "Year must be an integer.")

                        else:
                            messagebox.showerror("Month Error", "Month must be between 1 and 12.")

                    except ValueError:
                        messagebox.showerror("Month Error", "Month must be an integer.")

            else:
                messagebox.showerror("Day Error", "Day must be between 1 and 31.")

        except ValueError:
            messagebox.showerror("Day Error", "Day must be an integer.")


def delete_pixel(self):
    if len(self.root.day_entry.get()) == 0:
        messagebox.showerror("Day Error", "Day field cannot be empty.")

    else:
        try:
            day = int(self.root.day_entry.get())

            if 1 <= day <= 31:
                if len(self.root.month_entry.get()) == 0:
                    messagebox.showerror("Month Error", "Month field cannot be empty.")

                else:
                    try:
                        month = int(self.root.month_entry.get())

                        if 1 <= month <= 12:
                            if len(self.root.year_entry.get()) == 0:
                                messagebox.showerror("Year Error", "Year field cannot be empty.")

                            else:
                                try:
                                    year = int(self.root.year_entry.get())

                                    if 2000 <= year <= datetime.now().year:
                                        if self.main_root.graph_type == "int":

                                            headers = {"X-USER-TOKEN": self.main_root.token}

                                            create_pixel_thread = AsyncRequest(action="delete_pixel", headers=headers, user=self.main_root.user, date=f"{year}{str(month).zfill(2)}{str(day).zfill(2)}", id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                            create_pixel_thread.start()

                                            monitor(self, create_pixel_thread, "Success", f"Pixel updated!")

                                        elif self.main_root.graph_type == "float":

                                            headers = {"X-USER-TOKEN": self.main_root.token}

                                            create_pixel_thread = AsyncRequest(action="delete_pixel", headers=headers, user=self.main_root.user, date=f"{year}{str(month).zfill(2)}{str(day).zfill(2)}", id_calc=(self.main_root.user, self.main_root.token, self.main_root.graph))
                                            create_pixel_thread.start()

                                            monitor(self, create_pixel_thread, "Success", f"Pixel updated!")

                                        else:
                                            messagebox.showerror("Graph Type Error", f"The graph type is {self.main_root.graph_type}.")

                                    else:
                                        messagebox.showerror("Year Error", f"Year must be between 2000 and {datetime.now().year}.")

                                except ValueError:
                                    messagebox.showerror("Year Error", "Year must be an integer.")

                        else:
                            messagebox.showerror("Month Error", "Month must be between 1 and 12.")

                    except ValueError:
                        messagebox.showerror("Month Error", "Month must be an integer.")

            else:
                messagebox.showerror("Day Error", "Day must be between 1 and 31.")

        except ValueError:
            messagebox.showerror("Day Error", "Day must be an integer.")


class AsyncRequest(Thread):
    def __init__(self, params=None, headers=None, action="", user="", **kwargs):
        super().__init__()

        if headers is None:
            headers = {}
        if params is None:
            params = {}

        self.params = params
        self.headers = headers
        self.action = action
        self.user = user

        self.kwargs = kwargs

        self.status_code = None

    def run(self):
        if self.action == "create_user":
            response = requests.post(PIXELA_ENDPOINT, json=self.params)
            self.status_code = response.status_code

        elif self.action == "login_user":
            response = requests.put(f"{PIXELA_ENDPOINT}/{self.user}", json=self.params, headers=self.headers)
            self.status_code = response.status_code

        elif self.action == "delete_user":
            response = requests.delete(f"{PIXELA_ENDPOINT}/{self.user}", headers=self.headers)
            self.status_code = response.status_code

        elif self.action == "create_graph":
            response = requests.post(f"{PIXELA_ENDPOINT}/{self.user}/graphs", json=self.params, headers=self.headers)
            self.status_code = response.status_code

        elif self.action == "select_graph":
            graph_name = get_graph_name(self.user, self.headers["X-USER-TOKEN"], self.kwargs["id_"])
            graph_type = get_graph_type(self.user, self.headers["X-USER-TOKEN"], self.kwargs["id_"])

            self.params = {"name": graph_name}

            response = requests.put(f"{PIXELA_ENDPOINT}/{self.user}/graphs/{self.kwargs['id_']}", json=self.params, headers=self.headers)
            self.status_code = response.status_code

            monitor(self.kwargs["window"], self, "Success", f"Graph {graph_name} selected.", update_graph, self.kwargs["main_root"], graph_name, graph_type)

        elif self.action == "delete_graph":
            graph_name = get_graph_name(self.user, self.headers["X-USER-TOKEN"], self.kwargs["id_"])

            response = requests.delete(f"{PIXELA_ENDPOINT}/{self.user}/graphs/{self.kwargs['id_']}", json=self.params, headers=self.headers)
            self.status_code = response.status_code

            monitor(self.kwargs["window"], self, "Success", f"Graph {graph_name} deleted.", update_graph, self.kwargs["main_root"], None, None)

        elif self.action == "create_pixel":
            id_ = get_graph_id(*self.kwargs["id_calc"])

            url = f"{PIXELA_ENDPOINT}/{self.user}/graphs/{id_}"

            response = requests.post(url, headers=self.headers, json=self.params)
            self.status_code = response.status_code

        elif self.action == "update_pixel":
            id_ = get_graph_id(*self.kwargs["id_calc"])

            url = f"{PIXELA_ENDPOINT}/{self.user}/graphs/{id_}/{self.kwargs['date']}"

            response = requests.put(url, headers=self.headers, json=self.params)
            self.status_code = response.status_code

        elif self.action == "delete_pixel":
            id_ = get_graph_id(*self.kwargs["id_calc"])

            url = f"{PIXELA_ENDPOINT}/{self.user}/graphs/{id_}/{self.kwargs['date']}"

            response = requests.delete(url, headers=self.headers)

            self.status_code = response.status_code