# test_imports.py
print("Testing imports...")

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QColor
    print("✓ PyQt5 imports successful")
except ImportError as e:
    print(f"✗ PyQt5 import error: {e}")

try:
    from modules.bus_management import BusManagementPage
    print("✓ BusManagementPage import successful")
except ImportError as e:
    print(f"✗ BusManagementPage import error: {e}")

try:
    from modules.driver_management import DriverManagementPage
    print("✓ DriverManagementPage import successful")
except ImportError as e:
    print(f"✗ DriverManagementPage import error: {e}")

try:
    from modules.school_management import SchoolManagementPage
    print("✓ SchoolManagementPage import successful")
except ImportError as e:
    print(f"✗ SchoolManagementPage import error: {e}")

try:
    from reports_dashboard import ReportsDashboard
    print("✓ ReportsDashboard import successful")
except ImportError as e:
    print(f"✗ ReportsDashboard import error: {e}")

print("\nTest complete!")