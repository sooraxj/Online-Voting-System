import tkinter as tk
from tkinter import ttk, Frame, Label
from db_connection import connect_to_db  # Ensure db_connection is available

import tkinter as tk
from tkinter import ttk, Label
from db_connection import connect_to_db

class VoteView:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="white")

        # Destroy previous widgets in the parent frame
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header Label
        Label(self.parent, text="🏆 Election Results", font=("Arial", 18, "bold"), bg="white").pack(pady=20)

        # Table Columns
        columns = ("Election Name", "Total Votes", "Candidate Name", "Votes Received", "Position", "Winner")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=180, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Style rows
        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="white")

        # Load election results from the database
        self.load_results()

    def load_results(self):
        """Fetch election results from the database and display them."""
        self.tree.delete(*self.tree.get_children())  # Clear table first

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            # Query to get total votes per election
            cursor.execute("""
                SELECT e.election_id, e.election_name, COUNT(v.vote_id) AS total_votes
                FROM tbl_votes v
                JOIN tbl_elections e ON v.election_id = e.election_id
                GROUP BY e.election_id, e.election_name
            """)
            total_votes_per_election = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

            # Query to get votes per candidate along with position
            cursor.execute("""
                SELECT e.election_name, COUNT(v.vote_id) AS candidate_votes, c.full_name, c.position, c.election_id
                FROM tbl_votes v
                JOIN tbl_candidates c ON v.candidate_id = c.candidate_id
                JOIN tbl_elections e ON v.election_id = e.election_id
                GROUP BY e.election_name, c.full_name, c.position, c.election_id
                ORDER BY e.election_name, candidate_votes DESC
            """)
            results = cursor.fetchall()

            # Identify winners per election
            winners = {}
            for election_name, candidate_votes, candidate_name, position, election_id in results:
                if election_id not in winners or winners[election_id][1] < candidate_votes:
                    winners[election_id] = (candidate_name, candidate_votes)

            cursor.close()
            conn.close()

            # Insert fetched data into the Treeview
            for i, (election_name, candidate_votes, candidate_name, position, election_id) in enumerate(results):
                total_votes = total_votes_per_election.get(election_id, (election_name, 0))[1]
                winner_text = "🏅 Winner" if winners[election_id][0] == candidate_name else ""
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=(election_name, total_votes, candidate_name, candidate_votes, position, winner_text), tags=(tag,))

