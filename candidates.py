import tkinter as tk
from tkinter import Label, Button, ttk, messagebox, Toplevel, Entry, Frame, filedialog
from db_connection import connect_to_db

class CandidatesPage:
    def __init__(self, parent):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        Label(self.parent, text="🏆 Candidates Management", font=("Arial", 18, "bold")).pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#1f0024", font=("Arial", 12, "bold"))
        # Styled Table
        self.tree = ttk.Treeview(self.parent, columns=("ID", "Voter ID", "Name", "Election", "Position", "Party", "Symbol", "Candidate Image"), show="headings")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        for col in ("ID", "Voter ID", "Name", "Election", "Position", "Party", "Symbol", "Candidate Image"):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=150, anchor="center")

        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="white")

        self.load_candidates()

        # Button Frame
        btn_frame = Frame(self.parent, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="➕ Add Candidate", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5,
               command=self.add_candidate).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="✏️ Edit Candidate", font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5,
               command=self.edit_candidate).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="🗑 Delete Candidate", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=10, pady=5,
               command=self.delete_candidate).grid(row=0, column=2, padx=5)

    def load_candidates(self):
        self.tree.delete(*self.tree.get_children())
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT c.candidate_id, c.voter_id, c.full_name, e.election_name, 
                       c.position, c.party, c.symbol_img, c.can_img
                FROM tbl_candidates c
                JOIN tbl_elections e ON c.election_id = e.election_id
            """)
            candidates = cursor.fetchall()
            cursor.close()
            conn.close()

            for i, candidate in enumerate(candidates):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=candidate, tags=(tag,))

    def add_candidate(self):
        self.open_candidate_form("Add")

    def edit_candidate(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a candidate to edit.")
            return
        data = self.tree.item(selected)["values"]
        self.open_candidate_form("Edit", data)

    def delete_candidate(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a candidate to delete.")
            return
        candidate_id = self.tree.item(selected)["values"][0]
        
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tbl_candidates WHERE candidate_id=%s", (candidate_id,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Candidate deleted successfully.")
            self.load_candidates()

    def open_candidate_form(self, action, data=None):
        form = Toplevel(self.parent)
        form.title(f"{action} Candidate")
        form.geometry("400x400")

        # Frame for better styling
        form_frame = Frame(form, padx=20, pady=20, bg="#f9f9f9")
        form_frame.pack(fill="both", expand=True)

        # Heading for the Form (centered)
        form_heading = Label(form_frame, text=f"{action} Candidate", font=("Arial", 16, "bold"), bg="#f9f9f9")
        form_heading.grid(row=0, column=0, columnspan=2, pady=10)

        # Form Fields
        Label(form_frame, text="Voter ID:", font=("Arial", 12), bg="#f9f9f9").grid(row=1, column=0, sticky="w", pady=5)
        voter_id = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        voter_id.grid(row=1, column=1, pady=5, sticky="w")

        Label(form_frame, text="Full Name:", font=("Arial", 12), bg="#f9f9f9").grid(row=2, column=0, sticky="w", pady=5)
        full_name = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        full_name.grid(row=2, column=1, pady=5, sticky="w")

        Label(form_frame, text="Election:", font=("Arial", 12), bg="#f9f9f9").grid(row=3, column=0, sticky="w", pady=5)
        election_combo = ttk.Combobox(form_frame, font=("Arial", 12), state="readonly", width=17)
        election_combo.grid(row=3, column=1, pady=5, sticky="w")

        # Fetch election names
        conn = connect_to_db()
        election_dict = {}
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT election_id, election_name FROM tbl_elections WHERE status='Ongoing'")
            elections = cursor.fetchall()
            cursor.close()
            conn.close()

            election_dict = {name: eid for eid, name in elections}
            election_combo["values"] = list(election_dict.keys())

        Label(form_frame, text="Position:", font=("Arial", 12), bg="#f9f9f9").grid(row=4, column=0, sticky="w", pady=5)
        position = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        position.grid(row=4, column=1, pady=5, sticky="w")

        Label(form_frame, text="Party:", font=("Arial", 12), bg="#f9f9f9").grid(row=5, column=0, sticky="w", pady=5)
        party = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        party.grid(row=5, column=1, pady=5, sticky="w")

        Label(form_frame, text="Symbol Image Path:", font=("Arial", 12), bg="#f9f9f9").grid(row=6, column=0, sticky="w", pady=5)
        symbol_img = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        symbol_img.grid(row=6, column=1, pady=5, sticky="w")

        Label(form_frame, text="Candidate Image Path:", font=("Arial", 12), bg="#f9f9f9").grid(row=7, column=0, sticky="w", pady=5)
        can_img = Entry(form_frame, font=("Arial", 12), bd=2, relief="solid")
        can_img.grid(row=7, column=1, pady=5, sticky="w")

        if action == "Edit" and data:
            voter_id.insert(0, data[1])
            full_name.insert(0, data[2])
            election_combo.set(data[3])  # Set election name
            position.insert(0, data[4])
            party.insert(0, data[5])
            symbol_img.insert(0, data[6])
            can_img.insert(0, data[7])

        def select_image(entry_widget):
            filepath = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            if filepath:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, filepath)
        Button(form_frame, text="📂", font=("Arial", 12), bg="#007bff", fg="white", padx=5, pady=3, command=lambda: select_image(symbol_img)).grid(row=6, column=1, pady=5, sticky="w")
        Button(form_frame, text="🖼️", font=("Arial", 12), bg="#007bff", fg="white", padx=5, pady=3, command=lambda: select_image(can_img)).grid(row=7, column=1, pady=5, sticky="w")


        def save():
            selected_election = election_combo.get()
            if selected_election not in election_dict:
                messagebox.showerror("Error", "Please select a valid election.")
                return

            election_id = election_dict[selected_election]

            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                if action == "Add":
                    cursor.execute(
                        "INSERT INTO tbl_candidates (voter_id, full_name, election_id, position, party, symbol_img, can_img) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (voter_id.get(), full_name.get(), election_id, position.get(), party.get(), symbol_img.get(), can_img.get())
                    )
                else:
                    cursor.execute(
                        "UPDATE tbl_candidates SET voter_id=%s, full_name=%s, election_id=%s, position=%s, party=%s, symbol_img=%s, can_img=%s WHERE candidate_id=%s",
                        (voter_id.get(), full_name.get(), election_id, position.get(), party.get(), symbol_img.get(), can_img.get(), data[0])
                    )
                conn.commit()
                cursor.close()
                conn.close()
                self.load_candidates()
                form.destroy()

        Button(form_frame, text="Save", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5, command=save).grid(row=8, column=0, columnspan=2, pady=20)
