import tkinter as tk
from tkinter import Frame, Label, Button

class HomePage:
    def __init__(self, username, name):
        self.username = username
        self.name = name

        self.root = tk.Tk()
        self.root.title("Voter Dashboard")
        self.root.geometry("800x500")
        self.root.configure(bg="white")
        self.root.state("zoomed")

        # Navbar
        self.navbar_frame = Frame(self.root, bg="#1f0024", height=60)
        self.navbar_frame.pack(fill="x")

        # Navigation Buttons (Centered)
        nav_frame = Frame(self.navbar_frame, bg="#1f0024")
        nav_frame.place(relx=0.5, rely=0.5, anchor="center")

        for text, command in [
            ("Home", self.show_home),
            ("About", self.show_about),
            ("Contact", self.show_contact),
            ("Election", self.show_election),
            ("Results", self.show_results)  # <-- added

        ]:
            btn = Button(nav_frame, text=text, bg="#1f0024", fg="white", font=("Arial", 12, "bold"),
                         relief="flat", activebackground="#3e005c", command=command, width=12, height=2)
            btn.pack(side="left", padx=20)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3e005c"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1f0024"))

        # Profile & Logout (Top-Right)
        self.create_nav_button("Profile", 0.85, "black", self.show_profile)
        self.create_nav_button("Logout", 0.92, "red", self.logout)

        # Content Frame (Main Display Area)
        self.content_frame = Frame(self.root, bg="white", padx=50, pady=50)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_home()  # Show Home Page on Start

        self.root.mainloop()

    def create_nav_button(self, text, relx, bg_color, command):
        """Creates a navbar button with professional styling."""
        btn = Button(self.navbar_frame, text=text, bg=bg_color, fg="white", font=("Arial", 12, "bold"),
                     width=10, height=2, command=command)
        btn.place(relx=relx, y=10, width=100, height=40)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#555"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=bg_color))

    def clear_frame(self):
        """Removes all widgets from content_frame before displaying new content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Displays Home Page with User's Name"""
        self.clear_frame()
        welcome_text = f"✅ Welcome, {self.name}!"
        Label(self.content_frame, text=welcome_text, font=("Arial", 22, "bold"), bg="white").pack(pady=20)
        Label(self.content_frame, text="Your Voting Dashboard", font=("Arial", 16), bg="white").pack()

    def show_about(self):
        """Displays About Page"""
        self.clear_frame()
        Label(self.content_frame, text="About Us", font=("Arial", 22, "bold"), bg="white").pack(pady=20)
        Label(self.content_frame, text="We provide a secure and transparent voting system.", font=("Arial", 16), bg="white").pack()

    def show_contact(self):
        """Displays Contact Page"""
        self.clear_frame()
        Label(self.content_frame, text="Contact Us", font=("Arial", 22, "bold"), bg="white").pack(pady=20)
        Label(self.content_frame, text="Email: support@votingsystem.com\nPhone: +1234567890",
              font=("Arial", 16), bg="white").pack()

    def show_election(self):
        """Displays Election Page"""
        self.clear_frame()
        from votes import VotesPage
        VotesPage(self.content_frame, self.username)

    def show_profile(self):
        """Displays Profile Page"""
        self.clear_frame()
        from profile import ProfilePage
        ProfilePage(self.content_frame, self.username)
    
    def show_results(self):
        """Displays Election Results Page"""
        self.clear_frame()
        from result_view import ResultView
        ResultView(self.content_frame)


    def logout(self):
        """Logs the user out and redirects to index.py"""
        self.root.destroy()
        import subprocess
        subprocess.run(["python", "index.py"])  # Reopen index.py

if __name__ == "__main__":
    HomePage(username="user123", name="John Doe")
