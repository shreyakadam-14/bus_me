# main_application.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
    QStatusBar, QMenuBar, QMenu, QToolBar, QAction, QFrame,
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QLineEdit, QComboBox, QDateEdit, QSpinBox,
    QDoubleSpinBox, QTextEdit, QGroupBox, QTabWidget, QApplication,
    QSizePolicy
)
from PyQt5.QtGui import QFont, QColor  # Add QColor here
from PyQt5.QtCore import Qt, QTimer, QDate
import datetime
import sys

# Import integrated modules
# In main_application.py, replace the imports section with:

# Import integrated modules with database
try:
    from modules.bus_management_db import BusManagementPage
    from modules.driver_management_db import DriverManagementPage
    from modules.school_management_db import SchoolManagementPage
    from modules.system_admin_db import UserManagement
    from modules.system_settings_db import SystemSettings
    from modules.reports_dashboard_db import ReportsDashboard
    print("✓ All database-enabled modules imported successfully")
except ImportError as e:
    print(f"Warning: Module import error - {e}")
    # Fallback to mock versions if database versions don't exist
    from modules.bus_management import BusManagementPage
    from modules.driver_management import DriverManagementPage
    from modules.school_management import SchoolManagementPage
    from modules.system_admin import UserManagement
    from modules.system_settings import SystemSettings
    from reports_dashboard import ReportsDashboard
    # Create placeholder classes if imports fail
    class BusManagementPage(QWidget):
        def __init__(self): super().__init__()
    class DriverManagementPage(QWidget):
        def __init__(self): super().__init__()
    class SchoolManagementPage(QWidget):
        def __init__(self): super().__init__()
    class UserManagement(QWidget):
        def __init__(self): super().__init__()
    class SystemSettings(QWidget):
        def __init__(self): super().__init__()
    class ReportsDashboard(QWidget):
        def __init__(self): super().__init__()

class MainApplication(QMainWindow):
    """
    Main Application Window - Shows after successful login
    """
    
    def __init__(self, username="Admin", role="User"):
        super().__init__()
        self.username = username
        self.user_role = role
        
        # Setup window with minimum size
        self.setWindowTitle(f"Bus Management System - Welcome {username}")
        self.setGeometry(100, 50, 1000, 600)
        self.setMinimumSize(1000, 600)
        
        print(f"Initializing MainApplication for {username} ({role})")
        
        # Setup all UI components
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_main_content()
        self.setup_status_bar()
        
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        save_as_action = QAction("Save As...", self)
        print_action = QAction("Print", self)
        logout_action = QAction("Logout", self)
        exit_action = QAction("Exit", self)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(print_action)
        file_menu.addSeparator()
        file_menu.addAction(logout_action)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        
        toolbar_action = QAction("Toolbar", self, checkable=True)
        toolbar_action.setChecked(True)
        statusbar_action = QAction("Status Bar", self, checkable=True)
        statusbar_action.setChecked(True)
        
        view_menu.addAction(toolbar_action)
        view_menu.addAction(statusbar_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        
        calculator_action = QAction("Calculator", self)
        calendar_action = QAction("Calendar", self)
        backup_action = QAction("Backup Database", self)
        restore_action = QAction("Restore Database", self)
        
        tools_menu.addAction(calculator_action)
        tools_menu.addAction(calendar_action)
        tools_menu.addSeparator()
        tools_menu.addAction(backup_action)
        tools_menu.addAction(restore_action)
        
        # Help Menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("User Guide", self)
        about_action = QAction("About", self)
        
        help_menu.addAction(help_action)
        help_menu.addAction(about_action)
        
        # Connect actions
        exit_action.triggered.connect(self.close)
        logout_action.triggered.connect(self.logout)
        about_action.triggered.connect(self.show_about)
        
    def setup_toolbar(self):
        """Setup the toolbar with quick actions"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Dashboard button
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.clicked.connect(lambda: self.switch_module("Dashboard"))
        toolbar.addWidget(dashboard_btn)
        
        toolbar.addSeparator()
        
        # Core module buttons based on user role
        if self.user_role in ["Super Admin", "Admin", "Manager"]:
            # Bus Management
            bus_btn = QPushButton("Buses")
            bus_btn.clicked.connect(lambda: self.switch_module("Buses"))
            toolbar.addWidget(bus_btn)
            
            # Driver Management
            driver_btn = QPushButton("Drivers")
            driver_btn.clicked.connect(lambda: self.switch_module("Drivers"))
            toolbar.addWidget(driver_btn)
            
            # School Management
            school_btn = QPushButton("Schools")
            school_btn.clicked.connect(lambda: self.switch_module("Schools"))
            toolbar.addWidget(school_btn)
            
            toolbar.addSeparator()
        
        # Reports button
        reports_btn = QPushButton("Reports")
        reports_btn.clicked.connect(lambda: self.switch_module("Reports"))
        toolbar.addWidget(reports_btn)
        
        # Admin-only buttons
        if self.user_role in ["Super Admin", "Admin"]:
            users_btn = QPushButton("Users")
            users_btn.clicked.connect(lambda: self.switch_module("User Management"))
            toolbar.addWidget(users_btn)
            
            settings_btn = QPushButton("Settings")
            settings_btn.clicked.connect(lambda: self.switch_module("System Settings"))
            toolbar.addWidget(settings_btn)
        
        toolbar.addSeparator()
        
        # Common buttons
        help_btn = QPushButton("Help")
        help_btn.clicked.connect(lambda: self.switch_module("Help"))
        toolbar.addWidget(help_btn)
        
    def setup_main_content(self):
        """Setup the main content area with sidebar and central widget"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create central work area
        self.central_work_area = self.create_central_work_area()
        main_layout.addWidget(self.central_work_area, 1)
        
    def create_sidebar(self):
        """Create the sidebar navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setFrameStyle(QFrame.Box | QFrame.Raised)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sidebar title with user info
        user_frame = QFrame()
        user_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        user_layout = QVBoxLayout(user_frame)
        
        user_label = QLabel(self.username)
        user_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        user_label.setAlignment(Qt.AlignCenter)
        
        role_label = QLabel(self.user_role)
        role_label.setFont(QFont("Segoe UI", 10))
        role_label.setAlignment(Qt.AlignCenter)
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(role_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setFont(QFont("Segoe UI", 11))
        
        # Add navigation items based on user role
        nav_items = [("Dashboard", "Dashboard")]
        
        # Core modules - available for Manager, Admin, Super Admin
        if self.user_role in ["Super Admin", "Admin", "Manager"]:
            nav_items.extend([
                ("Buses", "Buses"),
                ("Drivers", "Drivers"),
                ("Schools", "Schools"),
            ])
        
        # Reports module
        nav_items.append(("Reports Dashboard", "Reports"))
        
        # Admin-only modules
        if self.user_role in ["Super Admin", "Admin"]:
            nav_items.extend([
                ("User Management", "User Management"),
                ("System Settings", "System Settings"),
            ])
        
        # Common modules
        nav_items.extend([
            ("Help", "Help")
        ])
        
        for text, module in nav_items:
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, module)
            self.nav_list.addItem(item)
        
        # Connect item click
        self.nav_list.itemClicked.connect(self.on_nav_item_clicked)
        
        # Select dashboard by default
        self.nav_list.item(0).setSelected(True)
        
        sidebar_layout.addWidget(user_frame)
        sidebar_layout.addWidget(separator)
        sidebar_layout.addWidget(self.nav_list)
        
        # Logout button at bottom
        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 10))
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)
        
        return sidebar
        
    def create_central_work_area(self):
        """Create the central work area with stacked widgets"""
        # Create stacked widget for different modules
        self.stacked_widget = QStackedWidget()
        
        # Create all module pages
        self.dashboard_page = self.create_dashboard_page()
        self.bus_management_page = BusManagementPage()
        self.driver_management_page = DriverManagementPage()
        self.school_management_page = SchoolManagementPage()
        self.reports_dashboard_page = ReportsDashboard()
        self.user_management_page = UserManagement()
        self.system_settings_page = SystemSettings()
        self.help_page = self.create_help_page()
        self.placeholder_page = self.create_placeholder_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.bus_management_page)
        self.stacked_widget.addWidget(self.driver_management_page)
        self.stacked_widget.addWidget(self.school_management_page)
        self.stacked_widget.addWidget(self.reports_dashboard_page)
        self.stacked_widget.addWidget(self.user_management_page)
        self.stacked_widget.addWidget(self.system_settings_page)
        self.stacked_widget.addWidget(self.help_page)
        self.stacked_widget.addWidget(self.placeholder_page)
        
        # Set minimum size for all pages
        for i in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(i)
            widget.setMinimumSize(1000, 600)
        
        # Set default page
        self.stacked_widget.setCurrentIndex(0)
        
        return self.stacked_widget
        
    def create_dashboard_page(self):
        """Create dashboard page"""
        page = QWidget()
        page.setMinimumSize(1000, 600)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome section
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(welcome_label)
        
        # Statistics section
        stats_label = QLabel("System Overview")
        stats_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(stats_label)
        
        # Statistics cards in grid
        stats_grid = QGridLayout()
        
        stats_data = [
            ("Total Buses", "25", QColor(52, 152, 219)),
            ("Active Drivers", "18", QColor(46, 204, 113)),
            ("Registered Schools", "12", QColor(155, 89, 182)),
            ("Active Contracts", "10", QColor(231, 76, 60)),
            ("Reports Generated", "128", QColor(241, 196, 15)),
            ("System Users", "8", QColor(230, 126, 34))
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = self.create_stat_card(title, value, color)
            stats_grid.addWidget(card, i // 3, i % 3)
        
        layout.addLayout(stats_grid)
        
        # Quick access buttons
        quick_access_label = QLabel("Quick Access")
        quick_access_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(quick_access_label)
        
        quick_access_layout = QHBoxLayout()
        
        quick_actions = [
            ("Add New Bus", "Buses"),
            ("Add Driver", "Drivers"),
            ("Add School", "Schools"),
            ("Generate Report", "Reports")
        ]
        
        for text, module in quick_actions:
            if self.check_access(module):
                btn = QPushButton(text)
                btn.setFont(QFont("Segoe UI", 10))
                btn.setFixedHeight(40)
                btn.clicked.connect(lambda checked, m=module: self.switch_module(m))
                quick_access_layout.addWidget(btn)
        
        layout.addLayout(quick_access_layout)
        
        # Recent activity section
        activity_label = QLabel("Recent Activity")
        activity_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(activity_label)
        
        # Activity table
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["Time", "User", "Activity", "Details"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add sample data
        self.activity_table.setRowCount(5)
        sample_data = [
            ["10:30 AM", self.username, "Login", "Successful login to system"],
            ["11:15 AM", "Manager", "Added Bus", "Bus No: BUS-025 added"],
            ["02:45 PM", "Admin", "Generated Report", "Monthly financial report"],
            ["04:20 PM", "Accountant", "Updated School", "School contract renewed"],
            ["05:10 PM", "Admin", "Updated Settings", "Tax rate updated to 18%"]
        ]
        
        for row, data in enumerate(sample_data):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                self.activity_table.setItem(row, col, item)
        
        layout.addWidget(self.activity_table)
        
        layout.addStretch()
        
        return page
        
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        
        # Set color using stylesheet
        value_label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()});")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
        
    def create_help_page(self):
        """Create help page"""
        page = QWidget()
        page.setMinimumSize(1000, 600)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Page header
        header = QLabel("Help & Support")
        header.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(header)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Help content
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setFont(QFont("Segoe UI", 11))
        help_text.setPlainText(f"""
Welcome to Bus Management System, {self.username}!

Quick Guide:

1. DASHBOARD
   - View system statistics
   - Monitor recent activities
   - Quick access to modules

2. BUS MANAGEMENT
   - Add/Edit/Delete buses
   - Track insurance status
   - Manage bus details

3. DRIVER MANAGEMENT
   - Manage driver information
   - Track license expiry
   - Assign buses to drivers

4. SCHOOL MANAGEMENT
   - Manage school contracts
   - Assign buses to schools
   - Track billing and payments

5. REPORTS DASHBOARD
   - Generate comprehensive reports
   - Financial, Bus, Driver, School, and System reports
   - Export to multiple formats

6. ADMINISTRATION
   - User management (Admin only)
   - System configuration
   - Database management

User Permissions:
- {self.user_role}: {self.get_role_permissions()}

Need Help?
- Check the user guide for detailed instructions
- Contact support for technical issues

Contact Information:
Email: support@busmgmt.com
Phone: +91 9876543210
Hours: 9:00 AM - 6:00 PM (Monday to Friday)
        """)
        
        layout.addWidget(help_text)
        
        layout.addStretch()
        
        return page
        
    def create_placeholder_page(self):
        """Create a placeholder page for modules not implemented"""
        page = QWidget()
        page.setMinimumSize(1000, 600)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Coming soon message
        message = QLabel("Module Under Development")
        message.setFont(QFont("Segoe UI", 24, QFont.Bold))
        message.setAlignment(Qt.AlignCenter)
        
        info = QLabel("This module is currently being developed.\nIt will be available in the next update.")
        info.setFont(QFont("Segoe UI", 14))
        info.setAlignment(Qt.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(message)
        layout.addWidget(info)
        layout.addStretch()
        
        # Back to dashboard button
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setFont(QFont("Segoe UI", 12))
        back_btn.clicked.connect(lambda: self.switch_module("Dashboard"))
        layout.addWidget(back_btn)
        
        return page
        
    def get_role_permissions(self):
        """Get permissions description for current role"""
        permissions = {
            "Super Admin": "Full access to all modules including user management",
            "Admin": "Full access to all management modules",
            "Manager": "Access to bus, driver, school management and reports",
            "User": "View-only access to dashboard and reports"
        }
        return permissions.get(self.user_role, "Limited access")
        
    def check_access(self, module):
        """Check if user has access to a module"""
        # Define access rules
        access_rules = {
            "Dashboard": ["Super Admin", "Admin", "Manager", "User"],
            "Buses": ["Super Admin", "Admin", "Manager"],
            "Drivers": ["Super Admin", "Admin", "Manager"],
            "Schools": ["Super Admin", "Admin", "Manager"],
            "Reports": ["Super Admin", "Admin", "Manager", "User"],
            "User Management": ["Super Admin", "Admin"],
            "System Settings": ["Super Admin", "Admin"],
            "Help": ["Super Admin", "Admin", "Manager", "User"]
        }
        
        return self.user_role in access_rules.get(module, [])
        
    def setup_status_bar(self):
        """Setup the status bar"""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        # Add status labels
        statusbar.showMessage("Ready")
        
        # Add permanent widgets
        user_label = QLabel(f" {self.username} ({self.user_role})")
        user_label.setFont(QFont("Segoe UI", 9))
        
        time_label = QLabel()
        time_label.setFont(QFont("Segoe UI", 9))
        
        # Update time every second
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(lambda: time_label.setText(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.status_timer.start(1000)
        
        statusbar.addPermanentWidget(user_label)
        statusbar.addPermanentWidget(time_label)
        
    def on_nav_item_clicked(self, item):
        """Handle navigation item click"""
        module = item.data(Qt.UserRole)
        self.current_module = module
        
        # Check access
        if not self.check_access(module):
            QMessageBox.warning(self, "Access Denied", 
                              f"You don't have permission to access {module}.")
            return
            
        # Update status bar
        self.statusBar().showMessage(f"Switched to {module}")
        
        # Switch to appropriate page
        module_map = {
            "Dashboard": 0,
            "Buses": 1,
            "Drivers": 2,
            "Schools": 3,
            "Reports": 4,
            "User Management": 5,
            "System Settings": 6,
            "Help": 7
        }
        
        if module in module_map:
            self.stacked_widget.setCurrentIndex(module_map[module])
        else:
            # Show placeholder for other modules
            self.stacked_widget.setCurrentIndex(8)  # Placeholder page
            QMessageBox.information(self, "Coming Soon", 
                                  f"The {module} module is under development.")
            
    def switch_module(self, module_name):
        """Switch to a specific module"""
        # Check access first
        if not self.check_access(module_name):
            QMessageBox.warning(self, "Access Denied", 
                              f"You don't have permission to access {module_name}.")
            return
            
        # Find and select the navigation item
        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            if item.data(Qt.UserRole) == module_name:
                self.nav_list.setCurrentItem(item)
                self.on_nav_item_clicked(item)
                break
                
    def print_current(self):
        """Print current page"""
        QMessageBox.information(self, "Print", 
                              "Print functionality would be implemented here.")
        
    def export_data(self):
        """Export current data"""
        QMessageBox.information(self, "Export", 
                              "Export functionality would be implemented here.")
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Bus Management System",
                         f"Bus Management System v1.0.0\n"
                         f"Logged in as: {self.username} ({self.user_role})\n"
                         f"Developed with PyQt5\n"
                         f"© 2024 All rights reserved")
        
    def show_help(self):
        """Show help"""
        self.switch_module("Help")
        
    def logout(self):
        """Logout from application"""
        reply = QMessageBox.question(self, "Logout", 
                                    "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.close()