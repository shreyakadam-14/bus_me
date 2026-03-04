# application_controller.py
import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from main_application import MainApplication

class ApplicationController:
    """Controls the flow between Login and Main Application"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.main_window = None
        
    def start(self):
        """Start the application"""
        self.show_login()
        sys.exit(self.app.exec_())
        
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.show_main_app)
        self.login_window.show()
        
    def show_main_app(self, username, role):
        """Show main application after successful login"""
        self.login_window.close()
        self.main_window = MainApplication(username, role)
        self.main_window.show()