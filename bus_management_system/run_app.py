# run_app.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Import classes
from login_window import LoginWindow
from main_application import MainApplication
from application_controller import ApplicationController
from database import Database

if __name__ == "__main__":
    # Set application attributes
    QApplication.setStyle("Fusion")
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    # Initialize database
    try:
        db = Database("bus_management.db")
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Show error message but continue - app can still run with mock data
        app_temp = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.warning(None, "Database Warning", 
                           f"Could not initialize database: {e}\n\n"
                           "Application will run with mock data.")
    
    # Start application
    controller = ApplicationController()
    controller.start()