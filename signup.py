import tkinter as tk
from tkinter import messagebox, Canvas, Frame, Label, Entry, Button  # Added Label, Entry, Button to the imports
import mysql.connector
from db_connection import connect_to_db

class SignupPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Color scheme matching main app
        self.primary_color = "#1f0024"  # Dark purple
        self.secondary_color = "#3e005c"  # Lighter purple
        self.accent_color = "#6a1b9a"  # Purple accent
        self.success_color = "#28a745"  # Green
        self.light_bg = "#f8f9fa"  # Light background
        self.card_bg = "#ffffff"  # White for cards
        self.text_color = "#343a40"  # Dark text
        self.text_muted = "#6c757d"  # Muted text
        
        # Fonts
        self.title_font = ("Segoe UI", 24, "bold")
        self.heading_font = ("Segoe UI", 18, "bold")
        self.body_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 12, "bold")
        
        # Configure window
        self.master.configure(bg=self.light_bg)
        self.pack(fill="both", expand=True)
        
        # Create main container
        self.main_frame = Frame(self, bg=self.light_bg)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create signup card
        self.create_signup_card()

    def create_signup_card(self):
        # Create a card container
        card_frame = Frame(self.main_frame, bg=self.card_bg, relief="flat", bd=0)
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=850)
        
        # Add shadow effect with a border
        shadow = Frame(card_frame, bg="#e9ecef", relief="flat", bd=0)
        shadow.pack(fill="both", expand=True, padx=5, pady=5)
        
        card_content = Frame(shadow, bg=self.card_bg, relief="flat", bd=0)
        card_content.pack(fill="both", expand=True)
        
        # Header with icon
        header_frame = Frame(card_content, bg=self.primary_color, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Create a simple logo using Canvas
        logo_canvas = Canvas(header_frame, width=40, height=40, bg=self.primary_color, highlightthickness=0)
        logo_canvas.pack(side="left", padx=20, pady=20)
        
        # Draw a user icon
        logo_canvas.create_oval(10, 10, 30, 30, outline="white", width=2)
        logo_canvas.create_arc(10, 25, 30, 45, start=0, extent=180, style="arc", outline="white", width=2)
        
        title_label = Label(header_frame, text="Sign Up", 
                           font=self.title_font, 
                           bg=self.primary_color, fg="white")
        title_label.pack(side="left", padx=10, pady=20)
        
        # Form content
        form_frame = Frame(card_content, bg=self.card_bg)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Create input fields
        self.create_input_field(form_frame, "Full Name:", "name_entry")
        self.create_input_field(form_frame, "Username:", "username_entry")
        self.create_input_field(form_frame, "Voter ID:", "voter_id_entry")
        self.create_input_field(form_frame, "Password:", "password_entry", show="*")
        
        # Terms and conditions
        terms_frame = Frame(form_frame, bg=self.card_bg)
        terms_frame.pack(fill="x", pady=10)
        
        terms_label = Label(terms_frame, text="By signing up, you agree to our Terms and Conditions", 
                           font=self.body_font, 
                           bg=self.card_bg, 
                           fg=self.text_muted)
        terms_label.pack()
        
        # Signup button
        self.signup_btn = Button(form_frame, text="Register", 
                                font=self.button_font, 
                                bg=self.success_color, fg="white",
                                relief="flat", 
                                activebackground="#218838", 
                                cursor="hand2",
                                command=self.signup,
                                borderwidth=0,
                                padx=20, pady=10)
        self.signup_btn.pack(fill="x", pady=20)
        self.signup_btn.bind("<Enter>", lambda e: self.signup_btn.config(bg="#218838"))
        self.signup_btn.bind("<Leave>", lambda e: self.signup_btn.config(bg=self.success_color))
        
        # Login option
        login_frame = Frame(form_frame, bg=self.card_bg)
        login_frame.pack(fill="x", pady=10)
        
        login_label = Label(login_frame, text="Already have an account? Login", 
                           font=self.body_font, 
                           bg=self.card_bg, 
                           fg=self.accent_color,
                           cursor="hand2")
        login_label.pack()

    def create_input_field(self, parent, label_text, entry_attr, show=None):
        """Reusable function for input fields"""
        frame = Frame(parent, bg=self.card_bg)
        frame.pack(fill="x", pady=10)
        
        label = Label(frame, text=label_text, font=self.body_font, bg=self.card_bg, fg=self.text_color)
        label.pack(anchor="w")
        
        entry = Entry(frame, font=self.body_font, show=show, relief="flat", bd=0)
        entry.pack(fill="x", ipady=10, pady=(5, 0))
        
        # Add a bottom border
        border = Frame(frame, height=1, bg="#e9ecef")
        border.pack(fill="x", pady=(0, 5))
        
        setattr(self, entry_attr, entry)

    def signup(self):
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        voter_id = self.voter_id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (name and username and voter_id and password):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM tbl_users WHERE username = %s OR voter_id = %s", (username, voter_id))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or Voter ID already exists!")
            else:
                cursor.execute("INSERT INTO tbl_login (username, password, role, status) VALUES (%s, %s, 'Voter', 'Active')",
                               (username, password))
                cursor.execute("INSERT INTO tbl_users (username, voter_id, name, status, approved) VALUES (%s, %s, %s, 'Inactive', 'No')",
                               (username, voter_id, name))
                conn.commit()
                messagebox.showinfo("Success", "Signup Successful! Wait for admin approval.")
                self.master.destroy() 
 
        finally:
            cursor.close()
            conn.close()

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.voter_id_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)