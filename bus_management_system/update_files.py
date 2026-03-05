# update_files.py
import os

def write_file(filename, content):
    """Write content to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated: {filename}")

# Database manager content
db_manager_content = '''# database_manager.py
import sqlite3
import os
import datetime
from contextlib import contextmanager

class DatabaseConnection:
    """Database connection manager"""
    
    def __init__(self):
        self.db_path = os.path.join('data', 'bus_management.db')
        os.makedirs('data', exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        finally:
            if conn:
                conn.close()
    
    def fetch_all(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

class DatabaseManager:
    """Main database manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.db_path = os.path.join('data', 'bus_management.db')
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        os.makedirs('data', exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def fetch_all(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def execute_query(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def get_table_names(self):
        tables = self.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [t['name'] for t in tables]
'''

# Application controller content
app_controller_content = '''# application_controller.py
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
'''

# Write the files
write_file('database_manager.py', db_manager_content)
write_file('application_controller.py', app_controller_content)

print("\n" + "=" * 50)
print("Files updated successfully!")
print("=" * 50)
print("\nNow run:")
print("python test_imports.py")