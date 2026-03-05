# application_controller.py
import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from main_application import MainApplication
from database_manager import DatabaseManager, DatabaseConnection
from session import UserSession
from daos import UserDAO

class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        self.login_window = None
        self.main_window = None
        self.db_manager = None
        self.db_connection = None
        self.user_session = None
        self.user_dao = None
        
    def start(self):
        """Start the application"""
        self.initialize_database()
        self.user_session = UserSession()
        self.user_dao = UserDAO()
        self.show_login()
        return self.app.exec_()
    
    def initialize_database(self):
        """Initialize database connection"""
        try:
            self.db_manager = DatabaseManager()
            self.db_connection = DatabaseConnection()
            print("✓ Database initialized")
        except Exception as e:
            print(f"Database warning: {e}")
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.show_main_app)
        self.center_window(self.login_window)
        self.login_window.show()
    
    def show_main_app(self, username, role):
        """Show main application"""
        self.login_window.close()
        self.main_window = MainApplication(username, role)
        self.center_window(self.main_window)
        self.main_window.show()
    
    def center_window(self, window):
        """Center window on screen"""
        screen = self.app.primaryScreen().availableGeometry()
        window.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )
