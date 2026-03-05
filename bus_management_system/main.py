# main.py
#!/usr/bin/env python3
"""
Bus Management System - Main Entry Point
"""

import sys
import os
import traceback

# Add the current directory to path FIRST
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"Added {current_dir} to Python path")

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
    print("✓ PyQt5 imported successfully")
except ImportError as e:
    print(f"✗ PyQt5 import error: {e}")
    print("\nPlease install PyQt5: pip install PyQt5")
    input("Press Enter to exit...")
    sys.exit(1)

# Import application modules with error handling
try:
    from application_controller import ApplicationController
    print("✓ ApplicationController imported")
except ImportError as e:
    print(f"✗ Failed to import ApplicationController: {e}")
    print("Make sure application_controller.py exists")
    input("Press Enter to exit...")
    sys.exit(1)

try:
    from database import Database
    print("✓ Database imported")
except ImportError as e:
    print(f"✗ Failed to import Database: {e}")
    print("Make sure database.py exists")
    Database = None

try:
    from db_connection import DatabaseConnection
    print("✓ DatabaseConnection imported")
except ImportError as e:
    print(f"✗ Failed to import DatabaseConnection: {e}")
    print("Make sure db_connection.py exists")
    DatabaseConnection = None

def setup_database():
    """Initialize the database"""
    if Database is None:
        print("✗ Database module not available")
        return False
        
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
            print("✓ Created data directory")
        
        # Initialize database
        db_path = os.path.join('data', 'bus_management.db')
        db = Database(db_path)
        print("✓ Database initialized successfully")
        
        # Test connection
        try:
            result = db.fetch_one("SELECT COUNT(*) as count FROM users")
            if result:
                print(f"✓ Database contains {result['count']} users")
            else:
                print("✓ Database connected but no users found")
        except Exception as e:
            print(f"Note: Could not query users table: {e}")
        
        # Test connection manager if available
        if DatabaseConnection:
            conn_manager = DatabaseConnection()
            print("✓ Database connection manager ready")
        
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        traceback.print_exc()
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\n" + "-" * 30)
    print("CHECKING REQUIRED FILES")
    print("-" * 30)
    
    required_files = [
        'application_controller.py',
        'login_window.py',
        'main_application.py',
        'database.py',
        'db_connection.py',
    ]
    
    module_files = [
        'modules/__init__.py',
        'modules/bus_management_db.py',
        'modules/driver_management_db.py',
        'modules/school_management_db.py',
        'modules/system_admin_db.py',
        'modules/system_settings_db.py',
        'modules/reports_dashboard_db.py',
    ]
    
    all_files = required_files + module_files
    missing_files = []
    
    for file in all_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (MISSING)")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def main():
    """Main entry point"""
    print("=" * 60)
    print("           BUS MANAGEMENT SYSTEM v1.0.0")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check required files first
    files_ok, missing = check_required_files()
    
    if not files_ok:
        print("\n" + "!" * 60)
        print("WARNING: Some files are missing!")
        print("!" * 60)
        print("\nMissing files:")
        for f in missing:
            print(f"  • {f}")
        print("\nThe application may not work correctly.")
        print("Please create these files first.")
        
        reply = input("\nContinue anyway? (y/n): ").lower()
        if reply != 'y':
            print("Exiting...")
            sys.exit(1)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application name
    app.setApplicationName("Bus Management System")
    app.setApplicationVersion("1.0.0")
    
    # Setup database
    print("\n" + "-" * 30)
    print("DATABASE INITIALIZATION")
    print("-" * 30)
    
    db_ok = setup_database()
    
    if not db_ok:
        print("\n⚠ Database initialization failed!")
        reply = QMessageBox.warning(
            None,
            "Database Warning",
            "Could not initialize database properly.\n\n"
            "The application will run with limited functionality.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.No:
            print("Exiting...")
            sys.exit(1)
    
    # Print login information
    print("\n" + "-" * 30)
    print("DEFAULT LOGIN CREDENTIALS:")
    print("-" * 30)
    print("Admin  : admin / admin123")
    print("Manager: manager / manager123")
    print("Viewer : viewer / viewer123")
    print("-" * 30)
    
    # Start application
    print("\n🚀 Starting application...")
    print("   (The login window will appear shortly)\n")
    
    try:
        controller = ApplicationController()
        controller.start()
    except Exception as e:
        print(f"\n✗ Application error: {e}")
        traceback.print_exc()
        
        QMessageBox.critical(
            None,
            "Application Error",
            f"Failed to start application:\n\n{str(e)}\n\nPlease check the console for details."
        )
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)