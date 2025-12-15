import tkinter as tk
from tkinter import Frame, Label, Canvas, font as tkfont
from db_connection import connect_to_db  # Ensure you have a database connection module

class AdminDashboard:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#f0f0f0")

        # Define color scheme
        self.primary_color = "#1f0024"  # Dark purple
        self.secondary_color = "#3e005c"  # Lighter purple
        self.accent_color = "#6a1b9a"  # Purple accent
        self.success_color = "#28a745"  # Green
        self.info_color = "#007BFF"  # Blue (keeping original)
        self.warning_color = "#ffc107"  # Yellow
        self.danger_color = "#dc3545"  # Red
        self.light_bg = "#f0f0f0"  # Light background
        self.card_bg = "#ffffff"  # White for cards
        self.text_color = "#343a40"  # Dark text
        self.text_muted = "#6c757d"  # Muted text

        # Clear existing widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Create main container
        self.main_container = Frame(self.parent, bg=self.light_bg)
        self.main_container.pack(fill="both", expand=True)

        # Create header section
        self.create_header()

        # Create statistics section
        self.create_statistics_section()

    def create_header(self):
        """Create a professional header for the dashboard"""
        header_frame = Frame(self.main_container, bg=self.primary_color, height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Add gradient effect to header
        gradient_frame = Frame(header_frame, bg=self.primary_color)
        gradient_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title and description
        title_label = Label(gradient_frame, text="📊 Admin Dashboard", 
                           font=("Arial", 24, "bold"), 
                           bg=self.primary_color, fg="white")
        title_label.pack(anchor="w")

        desc_label = Label(gradient_frame, text="Monitor and manage your voting system", 
                          font=("Arial", 12), 
                          bg=self.primary_color, fg="#e9ecef")
        desc_label.pack(anchor="w", pady=(5, 0))

        # Add decorative element
        canvas = Canvas(gradient_frame, width=100, height=5, bg=self.primary_color, highlightthickness=0)
        canvas.pack(anchor="w", pady=(10, 0))
        canvas.create_rectangle(0, 0, 100, 5, fill=self.accent_color, outline="")

    def create_statistics_section(self):
        """Create the statistics section with professional cards"""
        # Section title
        section_frame = Frame(self.main_container, bg=self.light_bg)
        section_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        section_title = Label(section_frame, text="System Statistics", 
                             font=("Arial", 18, "bold"), 
                             bg=self.light_bg, fg=self.text_color)
        section_title.pack(anchor="w")
        
        # Statistics container
        stats_container = Frame(self.main_container, bg=self.light_bg)
        stats_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Load statistics
        self.load_statistics(stats_container)

    def load_statistics(self, container):
        """Fetch total counts from the database and display them in professional cards"""
        conn = connect_to_db()
        if not conn:
            error_frame = Frame(container, bg=self.light_bg)
            error_frame.pack(fill="both", expand=True)
            
            error_card = self.create_error_card(error_frame, "Database connection error!")
            return

        cursor = conn.cursor()

        queries = {
            "Total Users": ("SELECT COUNT(*) FROM tbl_users", "👥", self.info_color),
            "Total Candidates": ("SELECT COUNT(*) FROM tbl_candidates", "🏆", self.success_color),
            "Total Elections": ("SELECT COUNT(*) FROM tbl_elections", "🗳️", self.warning_color),
            "Total Votes Polled": ("SELECT COUNT(*) FROM tbl_votes", "📊", self.danger_color)
        }

        # Create a grid layout for statistics cards
        grid_frame = Frame(container, bg=self.light_bg)
        grid_frame.pack(fill="both", expand=True)
        
        # Create two rows
        top_row = Frame(grid_frame, bg=self.light_bg)
        top_row.pack(fill="both", expand=True)
        
        bottom_row = Frame(grid_frame, bg=self.light_bg)
        bottom_row.pack(fill="both", expand=True)
        
        # Execute queries and create cards
        for i, (key, (query, icon, color)) in enumerate(queries.items()):
            cursor.execute(query)
            value = cursor.fetchone()[0]
            
            # Determine which row to place the card in
            row = top_row if i < 2 else bottom_row
            
            # Create statistic card
            self.create_statistic_card(row, key, value, icon, color)
        
        cursor.close()
        conn.close()
        
        # Add additional information section
        self.create_info_section(container)

    def create_statistic_card(self, parent, title, value, icon, color):
        """Create a professional statistic card"""
        # Main card frame with shadow
        card_container = Frame(parent, bg="#e9ecef")
        card_container.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        card = Frame(card_container, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Card header with icon
        header = Frame(card, bg=color, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Icon
        icon_label = Label(header, text=icon, 
                          font=("Arial", 24), 
                          bg=color, fg="white")
        icon_label.pack(pady=20)
        
        # Card body with content
        body = Frame(card, bg=self.card_bg)
        body.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = Label(body, text=title, 
                           font=("Arial", 12, "bold"), 
                           bg=self.card_bg, fg=self.text_muted)
        title_label.pack(anchor="w")
        
        # Value
        value_label = Label(body, text=str(value), 
                           font=("Arial", 24, "bold"), 
                           bg=self.card_bg, fg=color)
        value_label.pack(anchor="w", pady=(5, 0))
        
        # Progress bar (visual element)
        progress_frame = Frame(body, bg=self.card_bg)
        progress_frame.pack(fill="x", pady=(10, 0))
        
        # Background
        bg_canvas = Canvas(progress_frame, height=6, bg="#e9ecef", highlightthickness=0)
        bg_canvas.pack(fill="x")
        
        # Progress (random value for visual effect)
        import random
        progress_width = random.randint(40, 90)
        bg_canvas.create_rectangle(0, 0, progress_width, 6, fill=color, outline="")
        
        return card

    def create_info_section(self, parent):
        """Create an additional information section"""
        info_frame = Frame(parent, bg=self.light_bg)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Create two columns
        left_column = Frame(info_frame, bg=self.light_bg)
        left_column.pack(side="left", fill="both", expand=True, padx=(15, 7))
        
        right_column = Frame(info_frame, bg=self.light_bg)
        right_column.pack(side="right", fill="both", expand=True, padx=(7, 15))
        
        # Recent activity card
        self.create_activity_card(left_column)
        
        # Quick actions card
        self.create_actions_card(right_column)

    def create_activity_card(self, parent):
        """Create a recent activity card"""
        # Main card frame with shadow
        card_container = Frame(parent, bg="#e9ecef")
        card_container.pack(fill="both", expand=True)
        
        card = Frame(card_container, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Card header
        header = Frame(card, bg=self.primary_color, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = Label(header, text="Recent Activity", 
                           font=("Arial", 14, "bold"), 
                           bg=self.primary_color, fg="white")
        title_label.pack(pady=15)
        
        # Card body
        body = Frame(card, bg=self.card_bg)
        body.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sample activities
        activities = [
            "New user registered",
            "Election created",
            "Vote cast",
            "Candidate added"
        ]
        
        for activity in activities:
            activity_frame = Frame(body, bg=self.card_bg)
            activity_frame.pack(fill="x", pady=5)
            
            # Bullet point
            bullet = Canvas(activity_frame, width=10, height=10, bg=self.card_bg, highlightthickness=0)
            bullet.pack(side="left", padx=(0, 10))
            bullet.create_oval(2, 2, 8, 8, fill=self.accent_color, outline="")
            
            # Activity text
            activity_label = Label(activity_frame, text=activity, 
                                 font=("Arial", 11), 
                                 bg=self.card_bg, fg=self.text_color)
            activity_label.pack(side="left")
            
            # Time
            time_label = Label(activity_frame, text="2h ago", 
                             font=("Arial", 10), 
                             bg=self.card_bg, fg=self.text_muted)
            time_label.pack(side="right")

    def create_actions_card(self, parent):
        """Create a quick actions card"""
        # Main card frame with shadow
        card_container = Frame(parent, bg="#e9ecef")
        card_container.pack(fill="both", expand=True)
        
        card = Frame(card_container, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Card header
        header = Frame(card, bg=self.primary_color, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = Label(header, text="Quick Actions", 
                           font=("Arial", 14, "bold"), 
                           bg=self.primary_color, fg="white")
        title_label.pack(pady=15)
        
        # Card body
        body = Frame(card, bg=self.card_bg)
        body.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Action buttons
        actions = [
            ("Create Election", self.success_color),
            ("Add Candidate", self.info_color),
            ("View Reports", self.warning_color),
            ("System Settings", self.secondary_color)
        ]
        
        for action_text, color in actions:
            action_btn = Frame(body, bg=color, relief="flat", bd=0)
            action_btn.pack(fill="x", pady=5)
            
            # Add hover effect
            def on_enter(e, btn=action_btn, original_color=color):
                btn.configure(bg=self.darken_color(original_color))
                
            def on_leave(e, btn=action_btn, original_color=color):
                btn.configure(bg=original_color)
            
            action_btn.bind("<Enter>", on_enter)
            action_btn.bind("<Leave>", on_leave)
            
            # Button text
            btn_label = Label(action_btn, text=action_text, 
                            font=("Arial", 11, "bold"), 
                            bg=color, fg="white")
            btn_label.pack(pady=10)

    def create_error_card(self, parent, message):
        """Create an error card"""
        error_frame = Frame(parent, bg=self.light_bg)
        error_frame.pack(fill="both", expand=True, pady=50)
        
        error_card = Frame(error_frame, bg=self.card_bg, relief="flat", bd=0)
        error_card.pack(fill="both", expand=True, padx=20)
        
        # Add shadow
        shadow = Frame(error_card, bg="#e9ecef", relief="flat", bd=0)
        shadow.pack(fill="both", expand=True, padx=3, pady=3)
        
        card_content = Frame(shadow, bg=self.card_bg, relief="flat", bd=0)
        card_content.pack(fill="both", expand=True)
        
        # Error icon
        icon_frame = Frame(card_content, bg=self.danger_color, height=80)
        icon_frame.pack(fill="x")
        icon_frame.pack_propagate(False)
        
        icon_label = Label(icon_frame, text="⚠️", 
                          font=("Arial", 30), 
                          bg=self.danger_color, fg="white")
        icon_label.pack(pady=15)
        
        # Error message
        msg_frame = Frame(card_content, bg=self.card_bg)
        msg_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        msg_label = Label(msg_frame, text=message, 
                         font=("Arial", 14, "bold"), 
                         bg=self.card_bg, fg=self.danger_color)
        msg_label.pack()
        
        return error_card

    def darken_color(self, color):
        """Darken a color for hover effects"""
        # Simple color darkening for demonstration
        if color == self.success_color:
            return "#218838"
        elif color == self.info_color:
            return "#0056b3"
        elif color == self.warning_color:
            return "#e0a800"
        elif color == self.secondary_color:
            return "#2d0040"
        else:
            return color

# Example Usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("1200x700")
    root.configure(bg="#f0f0f0")
    AdminDashboard(root)
    root.mainloop()