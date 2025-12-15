import tkinter as tk
from tkinter import Entry, Label, Button, messagebox, Canvas, Frame
import mysql.connector
from db_connection import connect_to_db
import home  # Import home.py for Voter redirection
import admin  # Import admin.py for Admin redirection

class LoginPage(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.master = parent  # Store reference to login popup
        self.main_app = main_app  # Store reference to main application window
        
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
        
        # Create login card
        self.create_login_card()

    def create_login_card(self):
        # Create a card container
        card_frame = Frame(self.main_frame, bg=self.card_bg, relief="flat", bd=0)
        card_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
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
        
        # Draw a lock icon
        logo_canvas.create_rectangle(10, 15, 30, 30, outline="white", width=2)
        logo_canvas.create_arc(10, 15, 30, 30, start=0, extent=180, style="arc", outline="white", width=2)
        logo_canvas.create_line(20, 22, 20, 30, fill="white", width=2)
        
        title_label = Label(header_frame, text="Login", 
                           font=self.title_font, 
                           bg=self.primary_color, fg="white")
        title_label.pack(side="left", padx=10, pady=20)
        
        # Form content
        form_frame = Frame(card_content, bg=self.card_bg)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Create input fields
        self.create_input_field(form_frame, "Username:", "username_entry")
        self.create_input_field(form_frame, "Password:", "password_entry", show="*")
        
        # Login button
        self.login_btn = Button(form_frame, text="Login", 
                               font=self.button_font, 
                               bg=self.primary_color, fg="white",
                               relief="flat", 
                               activebackground=self.secondary_color, 
                               cursor="hand2",
                               command=self.login,
                               borderwidth=0,
                               padx=20, pady=10)
        self.login_btn.pack(fill="x", pady=20)
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg=self.secondary_color))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=self.primary_color))
        
        # Additional options
        options_frame = Frame(form_frame, bg=self.card_bg)
        options_frame.pack(fill="x", pady=10)
        
        forgot_label = Label(options_frame, text="Forgot Password?", 
                            font=self.body_font, 
                            bg=self.card_bg, 
                            fg=self.accent_color,
                            cursor="hand2")
        forgot_label.pack(side="left")
        
        signup_label = Label(options_frame, text="Don't have an account? Sign Up", 
                            font=self.body_font, 
                            bg=self.card_bg, 
                            fg=self.accent_color,
                            cursor="hand2")
        signup_label.pack(side="right")

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

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Both fields are required!")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()

                if user:
                    if user["status"] == "Inactive":
                        messagebox.showwarning("Access Denied", "Your account is inactive. Contact admin.")
                    else:
                        if user["role"] == "Voter":
                            cursor.execute("SELECT approved, name FROM tbl_users WHERE username=%s", (username,))
                            voter_info = cursor.fetchone()

                            if voter_info["approved"] == "No":
                                messagebox.showwarning("Access Denied", "Your account is not approved yet!")
                            else:
                                self.master.destroy()  # Close login popup
                                self.main_app.destroy()  # Close main application
                                home.HomePage(username, voter_info["name"])  # Redirect to home.py
                        else:
                            self.master.destroy()  # Close login popup
                            self.main_app.destroy()  # Close main application
                            admin.AdminPanel()  # Redirect to admin.py
                else:
                    messagebox.showerror("Login Failed", "Invalid Username or Password")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
            finally:
                cursor.close()
                conn.close()