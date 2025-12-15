import tkinter as tk
from tkinter import Label, Button, ttk, messagebox, Toplevel, Entry, StringVar, OptionMenu, Frame
from db_connection import connect_to_db

class ElectionsPage:
    def __init__(self, parent):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        Label(self.parent, text="🏆 Elections Management", font=("Arial", 18, "bold"), fg="#333").pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#1f0024", font=("Arial", 12, "bold"))
        self.tree = ttk.Treeview(self.parent, columns=("ID", "Election Name", "Status"), show="headings")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        for col in ("ID", "Election Name", "Status"):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=200, anchor="center")

        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="white")

        self.load_elections()

        btn_frame = Frame(self.parent, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="➕ Add Election", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5,
               command=self.add_election).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="✏️ Edit Election", font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5,
               command=self.edit_election).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="🗑 Delete Election", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=10, pady=5,
               command=self.delete_election).grid(row=0, column=2, padx=5)

    def load_elections(self):
        self.tree.delete(*self.tree.get_children())
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT election_id, election_name, status FROM tbl_elections")
            elections = cursor.fetchall()
            cursor.close()
            conn.close()

            for i, election in enumerate(elections):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=election, tags=(tag,))

    def add_election(self):
        self.open_election_form("Add")

    def edit_election(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an election to edit.")
            return
        data = self.tree.item(selected)["values"]
        self.open_election_form("Edit", data)

    def delete_election(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an election to delete.")
            return
        election_id = self.tree.item(selected)["values"][0]

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tbl_elections WHERE election_id=%s", (election_id,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Election deleted successfully.")
            self.load_elections()

    def open_election_form(self, action, data=None):
        form = Toplevel(self.parent)
        form.title(f"{action} Election")
        form.geometry("400x250")
        form.config(bg="#f8f9fa")

        Label(form, text="Election Name:", font=("Arial", 12, "bold"), bg="#f8f9fa").pack(pady=(10, 0))
        election_name = Entry(form, font=("Arial", 12), bd=2, relief="solid", width=30)
        election_name.pack(pady=5)

        Label(form, text="Status:", font=("Arial", 12, "bold"), bg="#f8f9fa").pack(pady=(10, 0))
        status_var = StringVar()
        status_options = ["Ongoing", "Completed"]
        status_menu = OptionMenu(form, status_var, *status_options)
        status_menu.config(font=("Arial", 12), width=20, bd=2, relief="solid")
        status_menu.pack(pady=5)

        if action == "Edit" and data:
            election_name.insert(0, data[1])
            status_var.set(data[2])

        def save():
            name = election_name.get().strip()
            status = status_var.get().strip()
            
            if not name or not status:
                messagebox.showerror("Error", "All fields are required!")
                return

            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                if action == "Add":
                    cursor.execute("INSERT INTO tbl_elections (election_name, status) VALUES (%s, %s)", (name, status))
                else:
                    cursor.execute("UPDATE tbl_elections SET election_name=%s, status=%s WHERE election_id=%s", (name, status, data[0]))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_elections()
                form.destroy()

        Button(form, text="Save", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5, width=10, command=save).pack(pady=10)
