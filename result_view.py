import tkinter as tk
from tkinter import Label, Frame, messagebox
from db_connection import connect_to_db

class ResultView:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="white")

        # Clear previous widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header
        Label(self.parent, text="📊 Election Results", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        # Table Frame
        self.table_frame = Frame(self.parent, bg="white")
        self.table_frame.pack(fill="both", padx=10, pady=5, expand=True)

        headers = ["Election Name", "Winner", "Party", " Winner Vote", "Total Votes", "Participant & Votes"]
        col_widths = [20, 20, 15, 12, 15, 45]

        for col, (header, width) in enumerate(zip(headers, col_widths)):
            Label(self.table_frame, text=header, font=("Arial", 14, "bold"), width=width, anchor="center",
                  bg="#1f0024", fg="white", padx=5, pady=5).grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        for i in range(len(headers)):
            self.table_frame.columnconfigure(i, weight=1)

        # Load results
        self.load_results()

    def load_results(self):
        conn = connect_to_db()
        if not conn:
            messagebox.showerror("Error", "Database connection error!")
            return

        cursor = conn.cursor()

        # Get declared results along with total votes polled
        cursor.execute("""
            SELECT e.election_name, c.full_name, c.party, COUNT(v.vote_id) AS total_votes, e.election_id,
                (SELECT COUNT(*) FROM tbl_votes WHERE election_id = e.election_id) AS total_votes_polled
            FROM tbl_results r
            JOIN tbl_elections e ON r.election_id = e.election_id
            JOIN tbl_candidates c ON r.candidate_id = c.candidate_id
            LEFT JOIN tbl_votes v ON e.election_id = v.election_id AND c.candidate_id = v.candidate_id
            WHERE r.status = 'Declared'
            GROUP BY e.election_id, c.candidate_id
            ORDER BY e.election_name;
        """)
        results = cursor.fetchall()

        for idx, (election, winner, party, total_votes, election_id, total_votes_polled) in enumerate(results, start=1):
            # Get all participants & votes
            cursor.execute("""
                SELECT c.full_name, COUNT(v.vote_id) AS votes
                FROM tbl_candidates c
                LEFT JOIN tbl_votes v ON c.candidate_id = v.candidate_id
                WHERE c.election_id = %s
                GROUP BY c.candidate_id
                ORDER BY votes DESC;
            """, (election_id,))
            participants = cursor.fetchall()

            participant_text = "\n".join([f"{name} ({votes})" for name, votes in participants])

            # Add to table
            Label(self.table_frame, text=election, font=("Arial", 12), width=20, bg="white").grid(row=idx, column=0, sticky="nsew")
            Label(self.table_frame, text=winner, font=("Arial", 12), width=20, bg="white").grid(row=idx, column=1, sticky="nsew")
            Label(self.table_frame, text=party, font=("Arial", 12), width=15, bg="white").grid(row=idx, column=2, sticky="nsew")
            Label(self.table_frame, text=str(total_votes), font=("Arial", 12), width=12, bg="white").grid(row=idx, column=3, sticky="nsew")
            Label(self.table_frame, text=str(total_votes_polled), font=("Arial", 12), width=15, bg="white").grid(row=idx, column=4, sticky="nsew")
            Label(self.table_frame, text=participant_text, font=("Arial", 12), width=45, bg="white", justify="left", anchor="w").grid(row=idx, column=5, sticky="nsew", padx=5, pady=2)

        cursor.close()
        conn.close()
