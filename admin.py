import tkinter as tk
from tkinter import Frame, Label, Button, Canvas
from users import UsersPage
from candidates import CandidatesPage  # Import CandidatesPage
from elections import ElectionsPage  # Import ElectionsPage
from vote_view import VoteView
from results import ElectionResults
from dash import AdminDashboard  

import subprocess

class AdminPanel(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Admin Panel - Online Voting System")
        self.state('zoomed')  
        self.configure(bg="#f0f0f0")

        # Define color scheme
        self.primary_color = "#1f0024"  # Dark purple
        self.secondary_color = "#3e005c"  # Lighter purple
        self.accent_color = "#6a1b9a"  # Purple accent
        self.success_color = "#28a745"  # Green
        self.info_color = "#17a2b8"  # Blue
        self.warning_color = "#ffc107"  # Yellow
        self.danger_color = "#dc3545"  # Red
        self.light_bg = "#f0f0f0"  # Light background
        self.card_bg = "#ffffff"  # White for cards
        self.text_color = "#343a40"  # Dark text
        self.text_muted = "#6c757d"  # Muted text

        # ========== TOP NAVBAR ==========
        self.navbar = Frame(self, bg=self.primary_color, height=70)
        self.navbar.pack(side="top", fill="x")
        self.navbar.pack_propagate(False)

        # Logo and title in navbar
        logo_frame = Frame(self.navbar, bg=self.primary_color)
        logo_frame.pack(side="left", padx=20, pady=15)

        # Create a simple logo using Canvas
        logo_canvas = Canvas(logo_frame, width=40, height=40, bg=self.primary_color, highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 10))
        
        # Draw a simple admin icon
        logo_canvas.create_oval(10, 5, 30, 25, outline="white", width=2)
        logo_canvas.create_arc(10, 20, 30, 40, start=0, extent=180, outline="white", width=2, style="arc")
        logo_canvas.create_line(20, 25, 20, 35, fill="white", width=2)
        
        title_label = Label(logo_frame, text="Admin Panel", fg="white", bg=self.primary_color, 
                           font=("Arial", 16, "bold"))
        title_label.pack(side="left", padx=5)

        # User info and logout in navbar
        user_frame = Frame(self.navbar, bg=self.primary_color)
        user_frame.pack(side="right", padx=20, pady=15)

        Label(user_frame, text="Administrator", fg="white", bg=self.primary_color, 
              font=("Arial", 12)).pack(side="left", padx=10)
        
        logout_btn = Button(user_frame, text="Logout", bg=self.danger_color, fg="white", 
                           font=("Arial", 12, "bold"), relief="flat", 
                           activebackground="#c82333", command=self.logout,
                           cursor="hand2", padx=15, pady=5)
        logout_btn.pack(side="left", padx=5)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#c82333"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg=self.danger_color))

        # Add a professional line at the bottom of the navbar
        navbar_line = Frame(self, bg=self.accent_color, height=2)
        navbar_line.pack(fill="x")

        # ========== SIDEBAR ==========
        self.sidebar = Frame(self, bg=self.primary_color, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)



        # ========== CONTENT FRAME ==========
        self.content_frame = Frame(self, bg="white")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # Sidebar Buttons
        buttons = [
            ("🏠 Home", self.show_home),
            ("👥 Users", self.show_users),
            ("🏆 Elections", self.show_elections),
            ("🗳 Candidates", self.show_candidates),
            ("📊 Votes", self.show_votes), 
            ("🏅 Results", self.show_results),
        ]

        for text, command in buttons:
            btn_frame = Frame(self.sidebar, bg=self.primary_color)
            btn_frame.pack(fill="x", padx=10, pady=5)
            
            btn = Button(btn_frame, text=text, bg=self.primary_color, fg="white", 
                        font=("Arial", 12, "bold"), relief="flat", 
                        activebackground=self.secondary_color, command=command,
                        cursor="hand2", pady=10)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.secondary_color))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.primary_color))

        # Add a professional line at the bottom of the sidebar
        sidebar_line = Frame(self.sidebar, bg=self.accent_color, height=2)
        sidebar_line.pack(side="bottom", fill="x")

        self.show_home()

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Loads the admin dashboard."""
        self.clear_frame()
        AdminDashboard(self.content_frame)

    def show_users(self):
        self.clear_frame()
        UsersPage(self.content_frame)

    def show_candidates(self):
        self.clear_frame()
        CandidatesPage(self.content_frame)

    def show_elections(self):
        self.clear_frame()
        ElectionsPage(self.content_frame)

    def show_votes(self):
        self.clear_frame()
        VoteView(self.content_frame)  

    def show_results(self):
        self.clear_frame()
        ElectionResults(self.content_frame)

    def logout(self):
        self.destroy()
        subprocess.run(["python", "index.py"])

if __name__ == "__main__":
    app = AdminPanel()
    app.mainloop()