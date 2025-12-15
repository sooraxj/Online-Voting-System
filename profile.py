import tkinter as tk
from tkinter import Label, Frame
import mysql.connector
from db_connection import connect_to_db  # Your DB connection file

class ProfilePage:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username

        self.display_profile()

    def display_profile(self):
        """Fetch user details from database and display them in a professional layout"""
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            query = "SELECT username, name, voter_id, status, approved FROM tbl_users WHERE username = %s"
            cursor.execute(query, (self.username,))
            user_data = cursor.fetchone()

            cursor.close()
            conn.close()

            # Clear previous content
            for widget in self.parent.winfo_children():
                widget.destroy()

            if user_data:
                username, name, voter_id, status, approved = user_data

                # Profile Heading
                Label(self.parent, text="User Profile", font=("Arial", 22, "bold"), fg="#2C3E50", bg="white").pack(pady=20)

                # Profile Card Frame
                profile_frame = Frame(self.parent, bg="#ECF0F1", padx=30, pady=25, bd=2, relief="ridge")
                profile_frame.pack(pady=10, padx=15)

                # User Information Fields
                details = [
                    ("👤 Username:", username),
                    ("📛 Name:", name),
                    ("🆔 Voter ID:", voter_id),
                    ("🔄 Status:", status),
                    ("🗳️ Approved to Vote:", "✅ Yes" if approved == 'Yes' else "❌ No")
                ]

                for i, (label_text, value_text) in enumerate(details):
                    Label(profile_frame, text=label_text, font=("Arial", 14, "bold"), fg="#2C3E50", bg="#ECF0F1").grid(row=i, column=0, sticky="w", padx=10, pady=8)
                    Label(profile_frame, text=value_text, font=("Arial", 14), fg="#16A085", bg="#ECF0F1").grid(row=i, column=1, sticky="w", padx=10, pady=8)

            else:
                Label(self.parent, text="❌ User not found!", font=("Arial", 16, "bold"), fg="red", bg="white").pack(pady=20)

        except mysql.connector.Error as err:
            Label(self.parent, text=f"Database Error: {err}", font=("Arial", 14), fg="red", bg="white").pack(pady=20)

