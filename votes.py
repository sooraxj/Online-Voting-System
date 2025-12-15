import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the required classes
from db_connection import connect_to_db

class VotesPage:
    def __init__(self, parent_frame, username):
        self.username = username
        self.root = parent_frame  # Use the existing parent frame
        self.user_id = self.get_user_id(username)  # Fetch user_id based on username
        
        self.content_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        self.content_frame.pack(fill="both", expand=True)
        
        self.load_ongoing_elections()

    def get_user_id(self, username):
        """Fetch user ID based on the username."""
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM tbl_users WHERE username=%s", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    def load_ongoing_elections(self):
        """Load and display all ongoing elections."""
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT election_id, election_name FROM tbl_elections WHERE status='Ongoing'")
        elections = cursor.fetchall()
        conn.close()

        if elections:
            # Create buttons for each ongoing election
            for election_id, election_name in elections:
                btn = tk.Button(self.content_frame, text=election_name, font=("Arial", 14), width=20, height=2,
                                bg="#1f0024", fg="white", command=lambda election_id=election_id: self.show_candidates(election_id))
                btn.pack(pady=10)
        else:
            messagebox.showinfo("No Ongoing Elections", "There are no ongoing elections at the moment.")

    def load_image(self, img_path):
        """Helper method to load images using Pillow."""
        try:
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize the image
            return ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None  # Return None if the image can't be loaded




    def show_candidates(self, election_id):
        """Show candidates for the selected election."""
        self.clear_frame()

        # Fetch the election name
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT election_name FROM tbl_elections WHERE election_id=%s", (election_id,))
        election_name = cursor.fetchone()
        conn.close()

        if election_name:
            election_header = tk.Label(self.content_frame, text=election_name[0], font=("Arial", 18, "bold"), bg="white", fg="black")
            election_header.pack(fill="x", pady=10)

        # Fetch candidates
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.candidate_id, c.full_name, c.position, c.party, c.symbol_img, c.can_img 
            FROM tbl_candidates c
            WHERE c.election_id=%s
        """, (election_id,))
        candidates = cursor.fetchall()
        conn.close()

        if candidates:
            # Main container for grid alignment
            table_frame = tk.Frame(self.content_frame, bg="white")
            table_frame.pack(fill="x", padx=10, pady=5)

            headers = ["Candidate", "Position", "Party", "Symbol", "Photo", "Vote"]
            col_widths = [20, 15, 15, 10, 10, 10]

            # Configure columns for center alignment
            for col in range(len(headers)):
                table_frame.grid_columnconfigure(col, weight=1)  # Equal space for each column

            # Header row
            for col, (header, width) in enumerate(zip(headers, col_widths)):
                tk.Label(table_frame, text=header, font=("Arial", 14, "bold"), width=width, bg="#1f0024", 
                        fg="white", padx=5, pady=5, anchor="center").grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

            # Candidate details rows
            for idx, candidate in enumerate(candidates, start=1):
                candidate_id, full_name, position, party, symbol_img, can_img = candidate

                tk.Label(table_frame, text=full_name, font=("Arial", 12), width=20, padx=5, bg="white", anchor="center").grid(row=idx, column=0, sticky="nsew")
                tk.Label(table_frame, text=position, font=("Arial", 12), width=15, padx=5, bg="white", anchor="center").grid(row=idx, column=1, sticky="nsew")
                tk.Label(table_frame, text=party, font=("Arial", 12), width=15, padx=5, bg="white", anchor="center").grid(row=idx, column=2, sticky="nsew")

                # Symbol Image
                symbol_label = tk.Label(table_frame, bg="white")
                symbol_label.grid(row=idx, column=3, padx=5, sticky="nsew")
                symbol = self.load_image(symbol_img)
                if symbol:
                    symbol_label.config(image=symbol)
                    symbol_label.image = symbol
                else:
                    symbol_label.config(text="No Image", width=10, anchor="center")

                # Candidate Image
                photo_label = tk.Label(table_frame, bg="white")
                photo_label.grid(row=idx, column=4, padx=5, sticky="nsew")
                photo = self.load_image(can_img)
                if photo:
                    photo_label.config(image=photo)
                    photo_label.image = photo
                else:
                    photo_label.config(text="No Image", width=10, anchor="center")

                # Vote Button
                vote_btn = tk.Button(table_frame, text="Vote", font=("Arial", 12), bg="green", fg="white",
                                    command=lambda cid=candidate_id, eid=election_id: self.vote(cid, eid))
                vote_btn.grid(row=idx, column=5, padx=5, sticky="nsew")

        else:
            messagebox.showinfo("No Candidates", "There are no candidates for this election.")


    def vote(self, candidate_id, election_id):
        """Cast the vote for the selected candidate."""
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Check if the user has already voted in this election
        cursor.execute("""
            SELECT * FROM tbl_votes WHERE user_id=%s AND election_id=%s
        """, (self.user_id, election_id))
        existing_vote = cursor.fetchone()
        
        if existing_vote:
            messagebox.showwarning("Already Voted", "You have already voted in this election.")
        else:
            # Record the vote in the tbl_votes table
            cursor.execute("""
                INSERT INTO tbl_votes (user_id, election_id, candidate_id)
                VALUES (%s, %s, %s)
            """, (self.user_id, election_id, candidate_id))
            conn.commit()
            messagebox.showinfo("Vote Cast", "Your vote has been successfully cast!")
        
        conn.close()

    def clear_frame(self):
        """Clear the content frame before showing new content."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
