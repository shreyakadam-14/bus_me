# main.py
#!/usr/bin/env python3
"""
Bus Management System - Main Entry Point
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application_controller import ApplicationController
from database import Database

def setup_database():
    """Initialize the database"""
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Initialize database
        db = Database('data/bus_management.db')
        print("✓ Database initialized successfully")
        
        # Test connection
        result = db.fetch_one("SELECT COUNT(*) as count FROM users")
        if result:
            print(f"✓ Database contains data")
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def main():
    """Main entry point"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application name
    app.setApplicationName("Bus Management System")
    app.setApplicationVersion("1.0.0")
    
    # Show splash message
    print("=" * 50)
    print("Bus Management System v1.0.0")
    print("=" * 50)
    
    # Setup database
    db_ok = setup_database()
    
    if not db_ok:
        reply = QMessageBox.warning(
            None,
            "Database Warning",
            "Could not initialize database. The application will run with limited functionality.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            sys.exit(1)
    
    # Start application
    print("\nStarting application...")
    controller = ApplicationController()
    controller.start()

if __name__ == "__main__":
    main()