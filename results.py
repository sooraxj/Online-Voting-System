import tkinter as tk
from tkinter import Label, Button, messagebox
from db_connection import connect_to_db

class ElectionResults:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="white")
        
        # Destroy previous widgets in the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header Label
        Label(self.parent, text="🏆 Election Results", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        # Create the results table layout
        self.create_table()
        
        # Load results
        self.load_results()

    def create_table(self):
        """Creates a grid-based table layout."""
        self.table_frame = tk.Frame(self.parent, bg="white")
        self.table_frame.pack(fill="both", padx=10, pady=5, expand=True)
        
        headers = ["Election Name", "Candidate", "Party", "Votes", "Status", "Declare"]
        col_widths = [20, 20, 15, 10, 10, 10]
        
        for col, (header, width) in enumerate(zip(headers, col_widths)):
            Label(self.table_frame, text=header, font=("Arial", 14, "bold"), width=width, anchor="center", 
                  bg="#1f0024", fg="white", padx=5, pady=5).grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        for i in range(len(headers)):
            self.table_frame.columnconfigure(i, weight=1)

    def load_results(self):
        """Fetch election results and display them in a table layout."""
        conn = connect_to_db()
        if not conn:
            messagebox.showerror("Error", "Database connection error!")
            return

        cursor = conn.cursor()
        
        cursor.execute("""
            WITH RankedCandidates AS (
                SELECT 
                    e.election_name, 
                    c.candidate_id, 
                    c.full_name, 
                    c.party,
                    COUNT(v.vote_id) AS total_votes, 
                    r.status,
                    RANK() OVER (PARTITION BY e.election_id ORDER BY COUNT(v.vote_id) DESC) AS rank
                FROM tbl_votes v
                JOIN tbl_candidates c ON v.candidate_id = c.candidate_id
                JOIN tbl_elections e ON v.election_id = e.election_id
                LEFT JOIN tbl_results r ON e.election_id = r.election_id AND r.candidate_id = c.candidate_id
                GROUP BY e.election_name, c.candidate_id
            )
            SELECT election_name, candidate_id, full_name, party, total_votes, status 
            FROM RankedCandidates 
            WHERE rank = 1
            ORDER BY election_name;
        """)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for idx, (election, candidate_id, candidate_name, party, votes, status) in enumerate(results, start=1):
            status = status if status else "Pending"
            
            Label(self.table_frame, text=election, font=("Arial", 12), width=20, anchor="center", bg="white").grid(row=idx, column=0, sticky="nsew")
            Label(self.table_frame, text=candidate_name, font=("Arial", 12), width=20, anchor="center", bg="white").grid(row=idx, column=1, sticky="nsew")
            Label(self.table_frame, text=party, font=("Arial", 12), width=15, anchor="center", bg="white").grid(row=idx, column=2, sticky="nsew")
            Label(self.table_frame, text=str(votes), font=("Arial", 12), width=10, anchor="center", bg="white").grid(row=idx, column=3, sticky="nsew")
            Label(self.table_frame, text=status, font=("Arial", 12), width=10, anchor="center", bg="white").grid(row=idx, column=4, sticky="nsew")
            
            declare_btn = Button(self.table_frame, text="Declare", font=("Arial", 12), bg="green", fg="white", 
                                 command=lambda e=election, c=candidate_name: self.declare_results(e, c))
            declare_btn.grid(row=idx, column=5, padx=5, sticky="nsew")
    
    def declare_results(self, election_name, candidate_name):
        """Marks the highest-voted candidate in an election as the winner and updates election status."""
        conn = connect_to_db()
        if not conn:
            messagebox.showerror("Error", "Database connection error!")
            return

        cursor = conn.cursor()

        # Get election_id
        cursor.execute("SELECT election_id FROM tbl_elections WHERE election_name = %s", (election_name,))
        election_id = cursor.fetchone()[0]

        # Get candidate_id
        cursor.execute("SELECT candidate_id FROM tbl_candidates WHERE full_name = %s AND election_id = %s", 
                       (candidate_name, election_id))
        candidate_id = cursor.fetchone()[0]

        # Check if results are already declared
        cursor.execute("SELECT COUNT(*) FROM tbl_results WHERE election_id = %s", (election_id,))
        result_exists = cursor.fetchone()[0]

        if result_exists > 0:
            messagebox.showinfo("Info", f"Results for '{election_name}' have already been declared.")
        else:
            # Insert result if not already declared
            cursor.execute("""
                INSERT INTO tbl_results (election_id, candidate_id, status) 
                VALUES (%s, %s, 'Declared')
            """, (election_id, candidate_id))

            cursor.execute("""
                UPDATE tbl_elections 
                SET status = 'Completed' 
                WHERE election_id = %s
            """, (election_id,))

            conn.commit()
            messagebox.showinfo("Success", f"Results declared! Winner: {candidate_name}\nElection status updated to Completed.")

        cursor.close()
        conn.close()
        self.load_results()
