import tkinter as tk
from tkinter import Label, Button, ttk, messagebox, Toplevel, Entry, StringVar, OptionMenu
from db_connection import connect_to_db

class UsersPage:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="white")

        Label(self.root, text="👥 User Management", font=("Arial", 20, "bold"), bg="white", fg="#333").pack(pady=15)

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#1f0024", font=("Arial", 12, "bold"))
        self.tree = ttk.Treeview(self.root, columns=("Username", "Voter ID", "Name", "Status", "Approved"), show="headings", height=10)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Table Headings
        for col in ("Username", "Voter ID", "Name", "Status", "Approved"):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=150, anchor="center")

        self.tree.tag_configure("evenrow", background="#f9f9f9")
        self.tree.tag_configure("oddrow", background="white")

        self.load_users()

        # Buttons Frame
    
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="✅ Approve", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5,
            command=self.approve_user).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="❌ Unapprove", font=("Arial", 12, "bold"), bg="#ffc107", fg="black", padx=10, pady=5,
            command=self.unapprove_user).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="✏️ Edit", font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5,
            command=self.edit_user).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="🗑 Delete", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=10, pady=5,
            command=self.delete_user).grid(row=0, column=3, padx=5)

    def load_users(self):
        """Fetches user data and populates the table"""
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, voter_id, name, status, approved FROM tbl_users")
            users = cursor.fetchall()
            cursor.close()
            conn.close()

            for i, user in enumerate(users):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=user, tags=(tag,))

    def approve_user(self):
        """Approves a selected user"""
        selected = self.tree.selection()
        if selected:
            user = self.tree.item(selected, "values")
            username = user[0]

            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tbl_users SET approved='Yes', status='Active' WHERE username=%s", (username,))
                conn.commit()
                cursor.close()
                conn.close()
                self.refresh_table()

    def unapprove_user(self):
        """Unapproves a selected user"""
        selected = self.tree.selection()
        if selected:
            user = self.tree.item(selected, "values")
            username = user[0]

            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tbl_users SET approved='No', status='Inactive' WHERE username=%s", (username,))
                conn.commit()
                cursor.close()
                conn.close()
                self.refresh_table()

    def edit_user(self):
        """Opens a pop-up window to edit selected user details"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to edit.")
            return

        user = self.tree.item(selected, "values")
        username, voter_id, name, status, approved = user

        edit_window = Toplevel(self.root)
        edit_window.title("Edit User")
        edit_window.geometry("350x400")
        edit_window.configure(bg="white")

        Label(edit_window, text="Edit User Details", font=("Arial", 14, "bold"), bg="white", fg="#333").pack(pady=10)

        fields = [("Name:", name), ("Voter ID:", voter_id)]
        entries = {}

        for field, value in fields:
            Label(edit_window, text=field, font=("Arial", 12), bg="white").pack(pady=5)
            entry = Entry(edit_window, font=("Arial", 12), bg="#f0f0f0", width=25)
            entry.pack(pady=5)
            entry.insert(0, value)
            entries[field] = entry

        status_var = StringVar(edit_window)
        status_var.set(status)
        Label(edit_window, text="Status:", font=("Arial", 12), bg="white").pack(pady=5)
        status_dropdown = OptionMenu(edit_window, status_var, "Active", "Inactive")
        status_dropdown.pack(pady=5)

        def save_changes():
            new_name = entries["Name:"].get()
            new_voter_id = entries["Voter ID:"].get()
            new_status = status_var.get()

            if new_name and new_voter_id and new_status:
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tbl_users SET name=%s, voter_id=%s, status=%s WHERE username=%s",
                                   (new_name, new_voter_id, new_status, username))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    edit_window.destroy()
                    self.refresh_table()
            else:
                messagebox.showerror("Error", "All fields are required.")

        Button(edit_window, text="💾 Save Changes", font=("Arial", 12, "bold"), bg="green", fg="white", width=20, command=save_changes).pack(pady=15)

    def delete_user(self):
        """Deletes a selected user"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete.")
            return

        user = self.tree.item(selected, "values")
        username = user[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user '{username}'?")
        if confirm:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tbl_users WHERE username=%s", (username,))
                conn.commit()
                cursor.close()
                conn.close()
                self.refresh_table()

    def refresh_table(self):
        """Clears and reloads the user table"""
        self.tree.delete(*self.tree.get_children())
        self.load_users()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Users Management")
    root.geometry("850x550")
    UsersPage(root)
    root.mainloop()
