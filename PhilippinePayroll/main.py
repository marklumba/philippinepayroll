import customtkinter as ctk
from views.main_window import MainWindow
from models.database import init_db

def main():
    # Initialize database
    init_db()

    # Set the appearance mode and default color theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create and run the main application window
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()