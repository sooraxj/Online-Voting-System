import tkinter as tk
from tkinter import Frame, Label, Button, Toplevel, Canvas, font as tkfont
from login import LoginPage
from signup import SignupPage

class VotingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Online Voting System")
        self.geometry("1200x700")
        self.configure(bg="#f8f9fa")
        self.state('zoomed')
        
        # Custom color scheme (keeping your original purple as primary)
        self.primary_color = "#1f0024"  # Dark purple (your original)
        self.secondary_color = "#3e005c"  # Lighter purple
        self.accent_color = "#6a1b9a"  # Purple accent
        self.success_color = "#28a745"  # Green
        self.info_color = "#17a2b8"  # Blue
        self.warning_color = "#ffc107"  # Yellow
        self.danger_color = "#dc3545"  # Red
        self.light_bg = "#f8f9fa"  # Light background
        self.card_bg = "#ffffff"  # White for cards
        self.text_color = "#343a40"  # Dark text
        self.text_muted = "#6c757d"  # Muted text
        
        # Fonts
        self.title_font = ("Segoe UI", 32, "bold")
        self.heading_font = ("Segoe UI", 24, "bold")
        self.subheading_font = ("Segoe UI", 18, "bold")
        self.body_font = ("Segoe UI", 14)
        self.small_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 12, "bold")
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_container = Frame(self, bg=self.light_bg)
        self.main_container.pack(fill="both", expand=True)
        
        # Navbar
        self.create_navbar()
        
        # Content Frame (Main Display Area)
        self.content_frame = Frame(self.main_container, bg=self.light_bg)
        self.content_frame.pack(fill="both", expand=True)
        
        # Footer
        self.create_footer()
        
        # Show home page
        self.show_home()
    
    def configure_styles(self):
        """Configure styles for widgets"""
        self.option_add("*TButton*background", self.primary_color)
        self.option_add("*TButton*foreground", "white")
        self.option_add("*TButton*borderWidth", 0)
        self.option_add("*TButton*font", self.button_font)
        self.option_add("*TButton*relief", "flat")
    
    def create_navbar(self):
        """Create professional navbar"""
        self.navbar_frame = Frame(self.main_container, bg=self.primary_color, height=80)
        self.navbar_frame.pack(fill="x")
        self.navbar_frame.pack_propagate(False)
        
        # Logo/Title
        logo_frame = Frame(self.navbar_frame, bg=self.primary_color)
        logo_frame.pack(side="left", padx=30, pady=20)
        
        # Create a more sophisticated logo using Canvas
        logo_container = Frame(logo_frame, bg=self.primary_color)
        logo_container.pack(side="left")
        
        logo_canvas = Canvas(logo_container, width=50, height=50, bg=self.primary_color, highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 15))
        
        # Draw a more sophisticated voting box icon with gradient effect
        logo_canvas.create_rectangle(10, 15, 40, 35, outline="white", width=2)
        logo_canvas.create_line(25, 15, 25, 35, fill="white", width=2)
        logo_canvas.create_polygon(25, 10, 20, 15, 30, 15, fill="white")
        
        # Add hover effect to logo
        def on_logo_enter(e):
            logo_canvas.create_rectangle(5, 5, 45, 45, outline=self.accent_color, width=1, tags="hover")
            
        def on_logo_leave(e):
            logo_canvas.delete("hover")
            
        logo_canvas.bind("<Enter>", on_logo_enter)
        logo_canvas.bind("<Leave>", on_logo_leave)
        
        title_label = Label(logo_container, text="VOTE SECURE", 
                           font=("Segoe UI", 18, "bold"), 
                           bg=self.primary_color, fg="white")
        title_label.pack(side="left")
        
        # Navigation Buttons (Centered)
        nav_frame = Frame(self.navbar_frame, bg=self.primary_color)
        nav_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a container for nav buttons with consistent styling
        nav_container = Frame(nav_frame, bg=self.primary_color)
        nav_container.pack()
        
        for text, command in [("Home", self.show_home), 
                             ("About", self.show_about), 
                             ("Contact", self.show_contact),
                             ("Features", self.show_features)]:
            btn_frame = Frame(nav_container, bg=self.primary_color)
            btn_frame.pack(side="left", padx=5)
            
            btn = Button(btn_frame, text=text, 
                        bg=self.primary_color, fg="white", 
                        font=self.button_font,
                        relief="flat", 
                        activebackground=self.secondary_color, 
                        command=command, 
                        width=10, 
                        cursor="hand2",
                        borderwidth=0)
            btn.pack()
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
        
        # Login & Sign Up (Top-Right)
        auth_frame = Frame(self.navbar_frame, bg=self.primary_color)
        auth_frame.pack(side="right", padx=30, pady=20)
        
        login_btn = Button(auth_frame, text="Login", 
                          bg="#3e005c", fg="white", 
                          font=self.button_font,
                          relief="flat", 
                          activebackground=self.secondary_color, 
                          command=self.open_login, 
                          width=8,
                          cursor="hand2",
                          borderwidth=0)
        login_btn.pack(side="left", padx=5)
        login_btn.bind("<Enter>", lambda e, b=login_btn: self.on_enter(e, b))
        login_btn.bind("<Leave>", lambda e, b=login_btn: self.on_leave(e, b))
        
        signup_btn = Button(auth_frame, text="Sign Up", 
                           bg=self.success_color, fg="white", 
                           font=self.button_font,
                           relief="flat", 
                           activebackground="#218838", 
                           command=self.open_signup, 
                           width=8,
                           cursor="hand2",
                           borderwidth=0)
        signup_btn.pack(side="left", padx=5)
        signup_btn.bind("<Enter>", lambda e, b=signup_btn: b.config(bg="#218838"))
        signup_btn.bind("<Leave>", lambda e, b=signup_btn: b.config(bg=self.success_color))
        
        # Add a professional line at the bottom of the navbar
        navbar_line = Frame(self.main_container, bg=self.accent_color, height=2)
        navbar_line.pack(fill="x")
    
    def create_footer(self):
        """Create professional footer"""
        self.footer_frame = Frame(self.main_container, bg=self.primary_color, height=60)
        self.footer_frame.pack(fill="x", side="bottom")
        self.footer_frame.pack_propagate(False)
        
        footer_content = Frame(self.footer_frame, bg=self.primary_color)
        footer_content.pack(expand=True)
        
        footer_text = Label(footer_content, text="© 2023 Online Voting System. All rights reserved.", 
                           font=self.small_font, 
                           bg=self.primary_color, fg="white")
        footer_text.pack(side="left", padx=30)
        
        social_frame = Frame(footer_content, bg=self.primary_color)
        social_frame.pack(side="right", padx=30)
        
        # Simple social media icons
        for icon in ["f", "t", "in"]:
            icon_label = Label(social_frame, text=icon, 
                              font=("Segoe UI", 14, "bold"), 
                              bg="#2c2c2c", fg="white", 
                              width=3, height=1, 
                              relief="flat", 
                              cursor="hand2")
            icon_label.pack(side="left", padx=5)
            icon_label.bind("<Enter>", lambda e, l=icon_label: l.config(bg=self.accent_color))
            icon_label.bind("<Leave>", lambda e, l=icon_label: l.config(bg="#2c2c2c"))
    
    def create_card(self, parent, title, content, button_text=None, button_command=None, icon=None):
        """Create a card widget for content display"""
        card = Frame(parent, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add shadow effect with a border
        shadow = Frame(card, bg="#e9ecef", relief="flat", bd=0)
        shadow.pack(fill="both", expand=True, padx=3, pady=3)
        
        card_content = Frame(shadow, bg=self.card_bg, relief="flat", bd=0)
        card_content.pack(fill="both", expand=True)
        
        # Card header with gradient effect
        header = Frame(card_content, bg=self.primary_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Add icon if provided
        if icon:
            icon_label = Label(header, text=icon, 
                              font=("Segoe UI", 20), 
                              bg=self.primary_color, fg="white")
            icon_label.pack(side="left", padx=15, pady=15)
        
        title_label = Label(header, text=title, 
                           font=self.subheading_font, 
                           bg=self.primary_color, fg="white")
        title_label.pack(side="left", padx=15, pady=15)
        
        # Card body
        body = Frame(card_content, bg=self.card_bg)
        body.pack(fill="both", expand=True, padx=25, pady=25)
        
        content_label = Label(body, text=content, 
                             font=self.body_font, 
                             bg=self.card_bg, 
                             justify="left",
                             fg=self.text_color)
        content_label.pack(fill="both", expand=True)
        
        # Card footer with button if provided
        if button_text and button_command:
            footer = Frame(card_content, bg=self.card_bg)
            footer.pack(fill="x", padx=25, pady=(0, 25))
            
            button = Button(footer, text=button_text, 
                           bg=self.accent_color, fg="white", 
                           font=self.button_font,
                           relief="flat", 
                           activebackground=self.secondary_color, 
                           command=button_command,
                           cursor="hand2",
                           borderwidth=0,
                           padx=20, pady=10)
            button.pack(side="right")
            button.bind("<Enter>", lambda e, b=button: b.config(bg=self.secondary_color))
            button.bind("<Leave>", lambda e, b=button: b.config(bg=self.accent_color))
        
        return card
    
    def create_feature_card(self, parent, icon_text, title, description):
        """Create a feature card for the features page"""
        card = Frame(parent, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add shadow effect with a border
        shadow = Frame(card, bg="#e9ecef", relief="flat", bd=0)
        shadow.pack(fill="both", expand=True, padx=3, pady=3)
        
        card_content = Frame(shadow, bg=self.card_bg, relief="flat", bd=0)
        card_content.pack(fill="both", expand=True)
        
        # Icon with circular background
        icon_frame = Frame(card_content, bg=self.accent_color, height=80)
        icon_frame.pack(fill="x")
        icon_frame.pack_propagate(False)
        
        icon_label = Label(icon_frame, text=icon_text, 
                          font=("Segoe UI", 30), 
                          bg=self.accent_color, fg="white")
        icon_label.pack(pady=15)
        
        # Content
        content_frame = Frame(card_content, bg=self.card_bg)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = Label(content_frame, text=title, 
                           font=self.subheading_font, 
                           bg=self.card_bg,
                           fg=self.text_color)
        title_label.pack(anchor="w", pady=(0, 10))
        
        desc_label = Label(content_frame, text=description, 
                          font=self.body_font, 
                          bg=self.card_bg, 
                          justify="left",
                          fg=self.text_muted)
        desc_label.pack(fill="both", expand=True)
        
        return card
    
    def create_stat_card(self, parent, value, label, icon):
        """Create a statistics card"""
        card = Frame(parent, bg=self.card_bg, relief="flat", bd=0)
        card.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add shadow effect with a border
        shadow = Frame(card, bg="#e9ecef", relief="flat", bd=0)
        shadow.pack(fill="both", expand=True, padx=3, pady=3)
        
        card_content = Frame(shadow, bg=self.card_bg, relief="flat", bd=0)
        card_content.pack(fill="both", expand=True)
        
        # Icon and value
        content_frame = Frame(card_content, bg=self.card_bg)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        icon_label = Label(content_frame, text=icon, 
                          font=("Segoe UI", 24), 
                          bg=self.card_bg, fg=self.accent_color)
        icon_label.pack(anchor="w")
        
        value_label = Label(content_frame, text=value, 
                           font=("Segoe UI", 28, "bold"), 
                           bg=self.card_bg,
                           fg=self.text_color)
        value_label.pack(anchor="w", pady=(5, 0))
        
        label_text = Label(content_frame, text=label, 
                          font=self.body_font, 
                          bg=self.card_bg, 
                          fg=self.text_muted)
        label_text.pack(anchor="w")
        
        return card
    
    def on_enter(self, event, button):
        """Handle button hover enter"""
        button.config(bg=self.secondary_color)
    
    def on_leave(self, event, button):
        """Handle button hover leave"""
        button.config(bg=self.primary_color)
    
    def clear_frame(self):
        """Removes all widgets from content_frame before displaying new content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Displays Home Page"""
        self.clear_frame()
        
        # Hero section with gradient effect
        hero_frame = Frame(self.content_frame, bg=self.primary_color)
        hero_frame.pack(fill="x")
        
        hero_content = Frame(hero_frame, bg=self.primary_color)
        hero_content.pack(pady=40)
        
        hero_title = Label(hero_content, text="Welcome to Online Voting System", 
                           font=self.title_font, 
                           bg=self.primary_color, fg="white")
        hero_title.pack(pady=(0, 10))
        
        hero_subtitle = Label(hero_content, text="Cast your vote securely and easily!", 
                             font=self.subheading_font, 
                             bg=self.primary_color, fg="#e9ecef")
        hero_subtitle.pack(pady=(0, 30))
        
        # CTA buttons
        cta_frame = Frame(hero_content, bg=self.primary_color)
        cta_frame.pack()
        
        cta_btn1 = Button(cta_frame, text="Get Started", 
                         bg=self.success_color, fg="white", 
                         font=self.button_font,
                         relief="flat", 
                         activebackground="#218838", 
                         command=self.open_signup,
                         cursor="hand2",
                         borderwidth=0,
                         padx=30, pady=12)
        cta_btn1.pack(side="left", padx=10)
        cta_btn1.bind("<Enter>", lambda e, b=cta_btn1: b.config(bg="#218838"))
        cta_btn1.bind("<Leave>", lambda e, b=cta_btn1: b.config(bg=self.success_color))
        
        # Fixed: Changed "#3e005c" to self.primary_color
        cta_btn2 = Button(cta_frame, text="Learn More", 
                         bg="#3e005c", fg="white", 
                         font=self.button_font,
                         relief="flat", 
                         activebackground=self.secondary_color, 
                         command=self.show_about,
                         cursor="hand2",
                         borderwidth=2,
                         padx=30, pady=12)
        cta_btn2.pack(side="left", padx=10)
        cta_btn2.bind("<Enter>", lambda e, b=cta_btn2: b.config(bg=self.secondary_color))
        cta_btn2.bind("<Leave>", lambda e, b=cta_btn2: b.config(bg="#3e005c"))
        
        # Statistics section
        stats_frame = Frame(self.content_frame, bg=self.light_bg)
        stats_frame.pack(fill="x", pady=30)
        
        stats_title = Label(stats_frame, text="Trusted by Millions", 
                           font=self.heading_font, 
                           bg=self.light_bg, fg=self.text_color)
        stats_title.pack(pady=(0, 20))
        
        stats_container = Frame(stats_frame, bg=self.light_bg)
        stats_container.pack()
        
        # Create stat cards
        self.create_stat_card(stats_container, "10M+", "Registered Voters", "👥")
        self.create_stat_card(stats_container, "500+", "Elections Conducted", "🗳️")
        self.create_stat_card(stats_container, "99.9%", "System Uptime", "⚡")
        self.create_stat_card(stats_container, "24/7", "Customer Support", "🎧")
        
        # Content cards
        cards_frame = Frame(self.content_frame, bg=self.light_bg)
        cards_frame.pack(fill="both", expand=True, pady=30)
        
        cards_title = Label(cards_frame, text="Why Choose Our System", 
                           font=self.heading_font, 
                           bg=self.light_bg, fg=self.text_color)
        cards_title.pack(pady=(0, 20))
        
        cards_container = Frame(cards_frame, bg=self.light_bg)
        cards_container.pack(fill="both", expand=True)
        
        # Create two columns for cards
        left_column = Frame(cards_container, bg=self.light_bg)
        left_column.pack(side="left", fill="both", expand=True)
        
        right_column = Frame(cards_container, bg=self.light_bg)
        right_column.pack(side="right", fill="both", expand=True)
        
        # Card 1
        self.create_card(
            left_column, 
            "Secure Voting", 
            "Our system uses advanced encryption and authentication methods to ensure your vote is secure and anonymous. Your privacy is our top priority.",
            "Learn More",
            self.show_about,
            "🔒"
        )
        
        # Card 2
        self.create_card(
            right_column, 
            "Easy to Use", 
            "With our intuitive interface, voting has never been easier. No technical knowledge required - just log in and cast your vote in minutes.",
            "Get Started",
            self.open_signup,
            "📱"
        )
    
    def show_about(self):
        """Displays About Page"""
        self.clear_frame()
        
        # Page header with gradient effect
        header_frame = Frame(self.content_frame, bg=self.primary_color)
        header_frame.pack(fill="x")
        
        header_content = Frame(header_frame, bg=self.primary_color)
        header_content.pack(pady=40)
        
        header_title = Label(header_content, text="About Us", 
                            font=self.title_font, 
                            bg=self.primary_color, fg="white")
        header_title.pack()
        
        # Content section
        content_frame = Frame(self.content_frame, bg=self.light_bg)
        content_frame.pack(fill="both", expand=True, pady=40)
        
        # Mission section
        mission_container = Frame(content_frame, bg=self.light_bg)
        mission_container.pack(fill="x", pady=20)
        
        mission_title = Label(mission_container, text="Our Mission", 
                             font=self.heading_font, 
                             bg=self.light_bg, fg=self.text_color)
        mission_title.pack(pady=(0, 20))
        
        mission_text = """We provide a secure and #3e005c voting system that ensures every vote is counted accurately and every voter's privacy is protected.

Our mission is to make voting accessible to everyone while maintaining the highest standards of security and integrity.

With years of experience in developing secure systems, our team has created a platform that combines cutting-edge technology with user-friendly design."""
        
        mission_label = Label(mission_container, text=mission_text, 
                             font=self.body_font, 
                             bg=self.light_bg, 
                             justify="center",
                             fg=self.text_color)
        mission_label.pack(padx=100)
        
        # Values section
        values_container = Frame(content_frame, bg=self.light_bg)
        values_container.pack(fill="both", expand=True, pady=20)
        
        values_title = Label(values_container, text="Our Values", 
                            font=self.heading_font, 
                            bg=self.light_bg, fg=self.text_color)
        values_title.pack(pady=(0, 30))
        
        values_grid = Frame(values_container, bg=self.light_bg)
        values_grid.pack()
        
        # Create value cards
        self.create_card(
            values_grid, 
            "Security", 
            "We prioritize the security and integrity of every vote with advanced encryption and multi-factor authentication.",
            icon="🔒"
        )
        
        self.create_card(
            values_grid, 
            "Accessibility", 
            "Our platform is designed to be accessible to all voters, regardless of technical ability or physical location.",
            icon="♿"
        )
        
        self.create_card(
            values_grid, 
            "Transparency", 
            "We believe in complete transparency in our processes and provide clear audit trails for all elections.",
            icon="🔍"
        )
        
        self.create_card(
            values_grid, 
            "Innovation", 
            "We continuously innovate to improve the voting experience and incorporate the latest security technologies.",
            icon="💡"
        )
    
    def show_contact(self):
        """Displays Contact Page (without form)"""
        self.clear_frame()
        
        # Page header with gradient effect
        header_frame = Frame(self.content_frame, bg=self.primary_color)
        header_frame.pack(fill="x")
        
        header_content = Frame(header_frame, bg=self.primary_color)
        header_content.pack(pady=40)
        
        header_title = Label(header_content, text="Contact Us", 
                            font=self.title_font, 
                            bg=self.primary_color, fg="white")
        header_title.pack()
        
        # Contact information section
        contact_frame = Frame(self.content_frame, bg=self.light_bg)
        contact_frame.pack(fill="both", expand=True, pady=40)
        
        contact_container = Frame(contact_frame, bg=self.light_bg)
        contact_container.pack()
        
        # Create contact cards
        self.create_card(
            contact_container, 
            "Email Us", 
            "support@votingsystem.com\n\nWe typically respond within 24 hours during business days.",
            icon="📧"
        )
        
        self.create_card(
            contact_container, 
            "Call Us", 
            "+1 (234) 567-8900\n\nMon-Fri: 9am-5pm EST\nSat-Sun: Closed",
            icon="📞"
        )
        
        self.create_card(
            contact_container, 
            "Visit Us", 
            "123 Democracy Street\nFreedom City, 12345\nUnited States\n\nBy appointment only",
            icon="📍"
        )
        
        # Additional information
        info_frame = Frame(contact_frame, bg=self.light_bg)
        info_frame.pack(fill="x", pady=40)
        
        info_text = """For technical support or urgent matters, please use our 24/7 helpline.
For general inquiries, email is preferred for faster response times.
Our office is open for scheduled appointments only."""
        
        info_label = Label(info_frame, text=info_text, 
                          font=self.body_font, 
                          bg=self.light_bg, 
                          justify="center",
                          fg=self.text_muted)
        info_label.pack(padx=100)
    
    def show_features(self):
        """Displays Features Page"""
        self.clear_frame()
        
        # Page header with gradient effect
        header_frame = Frame(self.content_frame, bg=self.primary_color)
        header_frame.pack(fill="x")
        
        header_content = Frame(header_frame, bg=self.primary_color)
        header_content.pack(pady=40)
        
        header_title = Label(header_content, text="Our Features", 
                            font=self.title_font, 
                            bg=self.primary_color, fg="white")
        header_title.pack()
        
        # Features section
        features_frame = Frame(self.content_frame, bg=self.light_bg)
        features_frame.pack(fill="both", expand=True, pady=40)
        
        # Create feature cards
        self.create_feature_card(
            features_frame,
            "🔒",
            "Secure & Private",
            "Advanced encryption ensures your vote remains confidential and secure from unauthorized access. Our system meets the highest security standards."
        )
        
        self.create_feature_card(
            features_frame,
            "📱",
            "Accessible Anywhere",
            "Vote from any device, anywhere in the world. No need to visit a physical polling station. Our platform works on desktop, tablet, and mobile devices."
        )
        
        self.create_feature_card(
            features_frame,
            "📊",
            "Real-time Results",
            "Watch the results unfold in real-time with our #3e005c and accurate counting system. Results are available immediately after polls close."
        )
        
        self.create_feature_card(
            features_frame,
            "✅",
            "Verified & Certified",
            "Our system meets all security standards and has been certified by independent auditors. We comply with all election regulations."
        )
        
        self.create_feature_card(
            features_frame,
            "🌐",
            "Multi-language Support",
            "Our platform supports multiple languages to ensure accessibility for diverse voter populations. Language options include English, Spanish, French, and more."
        )
        
        self.create_feature_card(
            features_frame,
            "🔔",
            "Election Notifications",
            "Receive timely notifications about upcoming elections, voting deadlines, and results. Stay informed with customizable notification preferences."
        )
    
    def open_login(self):
        """Opens Login Popup"""
        login_win = Toplevel(self)
        login_win.title("Login")
        login_win.geometry("400x500")
        login_win.resizable(False, False)
        login_win.configure(bg=self.light_bg)
        self.center_window(login_win, 400, 500)
        LoginPage(login_win, self)  # Pass reference to main app
    
    def open_signup(self):
        """Opens Signup Popup"""
        signup_win = Toplevel(self)
        signup_win.title("Sign Up")
        signup_win.geometry("400x800")
        signup_win.resizable(False, False)
        signup_win.configure(bg=self.light_bg)
        self.center_window(signup_win, 400, 800)
        SignupPage(signup_win)
    
    def center_window(self, window, width, height):
        """Centers a popup window on the screen"""
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = VotingApp()
    app.mainloop()

    
