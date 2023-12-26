import tkinter as tk
from tkinter import ttk
from src.database import Database  # Import your Database class from database.py

class EditUserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Users")
        self.db = Database()

        self.setup_ui()
        self.populate_users()

    def setup_ui(self):
        # Treeview to display users
        self.user_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Email", "Password"), show="headings")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Name", text="Name")
        self.user_tree.heading("Email", text="Email")
        self.user_tree.heading("Password", text="Password")

        self.user_tree.pack(pady=10)

        # Remove Button
        self.remove_button = ttk.Button(self.root, text="Remove", command=self.remove_selected_user)
        self.remove_button.pack(pady=10)

    def populate_users(self):
        # Clear existing data in the treeview
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # Fetch all users from the database
        users = self.db.get_all_users()

        # Populate the treeview with user details
        for user in users:
            self.user_tree.insert("", "end", values=user)

    def remove_selected_user(self):
        # Get the selected item in the treeview
        selected_item = self.user_tree.selection()

        if not selected_item:
            # No user selected
            return

        # Extract the user ID from the selected item
        user_id = self.user_tree.item(selected_item, "values")[0]

        # Remove the selected user from the database
        self.db.remove_user(user_id)

        # Refresh the treeview
        self.populate_users()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditUserApp(root)
    root.mainloop()
