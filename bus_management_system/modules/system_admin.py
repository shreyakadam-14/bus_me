from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QGroupBox,
    QFormLayout, QMessageBox, QTabWidget, QCheckBox, QDialog, QDialogButtonBox,
    QDateEdit, QTextEdit, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QInputDialog, QSplitter, QScrollArea, QToolBar, QAction, QMenu, QGridLayout
)
from PyQt5.QtGui import QFont, QIcon, QColor, QBrush
from PyQt5.QtCore import Qt, QDate, QSize, pyqtSignal  # ← QSize is here!
import datetime

class UserManagement(QWidget):
    """
    7.1 User Management Module
    """
    
    user_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 600)  # Add this line
        self.setup_ui()
        self.load_sample_users()
        
    def setup_ui(self):
        """Setup user management UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Main tabs
        self.tabs = QTabWidget()
        
        # Tab 1: User List
        user_list_tab = self.create_user_list_tab()
        self.tabs.addTab(user_list_tab, "User List")
        
        """# Tab 2: Permissions
        permissions_tab = self.create_permissions_tab()
        self.tabs.addTab(permissions_tab, "Permissions")"""
        
        # Tab 3: Activity Logs
        activity_tab = self.create_activity_logs_tab()
        self.tabs.addTab(activity_tab, "Activity Logs")
        
        main_layout.addWidget(self.tabs, 1)
        
    def create_header(self):
        """Create header for user management"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Title
        title_label = QLabel("User Management")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        
        # Quick actions toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(20, 20))
        
        # Add user action
        add_action = QAction("➕ Add User", self)
        add_action.triggered.connect(self.add_user)
        
        # Refresh action
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.load_sample_users)
        
        # Export action
        export_action = QAction("💾 Export", self)
        export_action.triggered.connect(self.export_users)
        
        toolbar.addAction(add_action)
        toolbar.addAction(refresh_action)
        toolbar.addAction(export_action)
        toolbar.addSeparator()
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(toolbar)
        
        return header_widget
        
    def create_user_list_tab(self):
        """Create user list tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(10)
        
        # Search and filter
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search users by name, email, or role...")
        search_input.setFixedWidth(300)
        
        role_combo = QComboBox()
        role_combo.addItems(["All Roles", "Admin", "Manager", "Accountant", "Driver", "Viewer"])
        
        status_combo = QComboBox()
        status_combo.addItems(["All Status", "Active", "Inactive", "Locked"])
        
        search_btn = QPushButton("Search")
        clear_btn = QPushButton("Clear")
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(search_input)
        filter_layout.addWidget(QLabel("Role:"))
        filter_layout.addWidget(role_combo)
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(status_combo)
        filter_layout.addWidget(search_btn)
        filter_layout.addWidget(clear_btn)
        filter_layout.addStretch()
        
        layout.addWidget(filter_widget)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(8)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Username", "Full Name", "Email", "Role", "Status", "Last Login", "Actions"
        ])
        
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.users_table, 1)
        
        # Statistics
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        total_label = QLabel("Total Users: 0")
        active_label = QLabel("Active: 0")
        admin_label = QLabel("Admins: 0")
        
        for label in [total_label, active_label, admin_label]:
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            stats_layout.addWidget(label)
            
        stats_layout.addStretch()
        layout.addWidget(stats_widget)
        
        return tab_widget
        
    def create_activity_logs_tab(self):
        """Create user activity logs tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Filter controls
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        user_combo = QComboBox()
        user_combo.addItems(["All Users", "admin", "manager1", "accountant1"])
        
        action_combo = QComboBox()
        action_combo.addItems(["All Actions", "Login", "Logout", "Create", "Edit", "Delete", "Export"])
        
        date_from = QDateEdit()
        date_from.setCalendarPopup(True)
        date_from.setDate(QDate.currentDate().addDays(-7))
        
        date_to = QDateEdit()
        date_to.setCalendarPopup(True)
        date_to.setDate(QDate.currentDate())
        
        filter_btn = QPushButton("Filter")
        export_logs_btn = QPushButton("Export Logs")
        
        filter_layout.addWidget(QLabel("User:"))
        filter_layout.addWidget(user_combo)
        filter_layout.addWidget(QLabel("Action:"))
        filter_layout.addWidget(action_combo)
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(date_to)
        filter_layout.addWidget(filter_btn)
        filter_layout.addWidget(export_logs_btn)
        filter_layout.addStretch()
        
        layout.addWidget(filter_widget)
        
        # Activity logs table
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(6)
        self.activity_table.setHorizontalHeaderLabels([
            "Timestamp", "User", "IP Address", "Action", "Module", "Details"
        ])
        
        header = self.activity_table.horizontalHeader()
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        
        layout.addWidget(self.activity_table, 1)
        
        # Load sample logs
        self.load_sample_activity_logs()
        
        return tab_widget
        
    def load_sample_users(self):
        """Load sample users data"""
        users = [
            [1, "admin", "System Administrator", "admin@company.com", "Admin", "Active", "2024-01-20 10:30", ""],
            [2, "manager1", "John Manager", "john@company.com", "Manager", "Active", "2024-01-19 14:15", ""],
            [3, "accountant1", "Sarah Accountant", "sarah@company.com", "Accountant", "Active", "2024-01-18 11:45", ""],
            [4, "driver1", "Michael Driver", "michael@company.com", "Driver", "Active", "2024-01-17 09:20", ""],
            [5, "viewer1", "Lisa Viewer", "lisa@company.com", "Viewer", "Inactive", "2024-01-10 16:40", ""],
            [6, "manager2", "Robert Manager", "robert@company.com", "Manager", "Active", "2024-01-15 13:10", ""]
        ]
        
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            for col, data in enumerate(user[:7]):  # Skip actions column
                item = QTableWidgetItem(str(data))
                
                # Style based on status
                if col == 5:  # Status column
                    if data == "Active":
                        item.setForeground(QColor("#4CAF50"))
                    elif data == "Inactive":
                        item.setForeground(QColor("#FF9800"))
                    elif data == "Locked":
                        item.setForeground(QColor("#F44336"))
                        
                # Style admin users
                if col == 4 and data == "Admin":
                    item.setFont(QFont("Segoe UI", 9, QFont.Bold))
                    item.setForeground(QColor("#2196F3"))
                    
                self.users_table.setItem(row, col, item)
                
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setFixedWidth(60)
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_user(r))
            
            reset_btn = QPushButton("Reset PW")
            reset_btn.setFixedWidth(70)
            reset_btn.clicked.connect(lambda checked, r=row: self.reset_password(r))
            
            toggle_btn = QPushButton("Toggle")
            toggle_btn.setFixedWidth(60)
            toggle_btn.clicked.connect(lambda checked, r=row: self.toggle_user(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(reset_btn)
            action_layout.addWidget(toggle_btn)
            action_layout.addStretch()
            
            self.users_table.setCellWidget(row, 7, action_widget)
            
    def load_sample_activity_logs(self):
        """Load sample activity logs"""
        logs = [
            ["2024-01-20 10:30:15", "admin", "192.168.1.100", "Login", "System", "Successful login"],
            ["2024-01-20 10:35:22", "admin", "192.168.1.100", "Create", "User Management", "Created new user: manager2"],
            ["2024-01-20 11:15:45", "manager1", "192.168.1.101", "Login", "System", "Successful login"],
            ["2024-01-20 11:20:30", "manager1", "192.168.1.101", "View", "Financial Reports", "Viewed monthly report"],
            ["2024-01-20 12:05:18", "accountant1", "192.168.1.102", "Login", "System", "Successful login"],
            ["2024-01-20 12:10:45", "accountant1", "192.168.1.102", "Export", "Salary Reports", "Exported salary register"],
            ["2024-01-20 13:45:22", "admin", "192.168.1.100", "Edit", "System Settings", "Updated company information"],
            ["2024-01-20 14:30:15", "driver1", "192.168.1.103", "Login", "System", "Successful login"],
            ["2024-01-20 15:20:33", "manager1", "192.168.1.101", "Logout", "System", "User logged out"],
            ["2024-01-20 16:45:12", "admin", "192.168.1.100", "Backup", "Database", "Created system backup"]
        ]
        
        self.activity_table.setRowCount(len(logs))
        
        for row, log in enumerate(logs):
            for col, data in enumerate(log):
                item = QTableWidgetItem(str(data))
                
                # Color code actions
                if col == 3:  # Action column
                    if data == "Login":
                        item.setForeground(QColor("#4CAF50"))
                    elif data == "Logout":
                        item.setForeground(QColor("#FF9800"))
                    elif data == "Create":
                        item.setForeground(QColor("#2196F3"))
                    elif data == "Delete":
                        item.setForeground(QColor("#F44336"))
                        
                self.activity_table.setItem(row, col, item)
                
    def load_role_permissions(self, role):
        """Load permissions for selected role"""
        print(f"Loading permissions for role: {role}")
        
    def add_user(self):
        """Open add user dialog"""
        dialog = AddUserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Success", "New user added successfully!")
            self.load_sample_users()
            
    def edit_user(self, row):
        """Edit user information"""
        username = self.users_table.item(row, 1).text()
        QMessageBox.information(self, "Edit User", f"Editing user: {username}")
        
    def reset_password(self, row):
        """Reset user password"""
        username = self.users_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Reset Password",
            f"Reset password for user '{username}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Password Reset", 
                                  f"Password reset link sent to user '{username}'")
            
    def toggle_user(self, row):
        """Toggle user active/inactive status"""
        username = self.users_table.item(row, 1).text()
        current_status = self.users_table.item(row, 5).text()
        
        new_status = "Inactive" if current_status == "Active" else "Active"
        
        reply = QMessageBox.question(
            self, "Change User Status",
            f"Change user '{username}' status to '{new_status}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.users_table.item(row, 5).setText(new_status)
            
            # Update color
            if new_status == "Active":
                self.users_table.item(row, 5).setForeground(QColor("#4CAF50"))
            else:
                self.users_table.item(row, 5).setForeground(QColor("#FF9800"))
                
            QMessageBox.information(self, "Status Changed", 
                                  f"User '{username}' is now '{new_status}'")
            
    def export_users(self):
        """Export users list"""
        QMessageBox.information(self, "Export", "Users exported to CSV file")


class AddUserDialog(QDialog):
    """Dialog for adding new user"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        # Form layout
        form_group = QGroupBox("User Information")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(10)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        # Full name
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Manager", "Accountant", "Driver", "Viewer"])
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Confirm password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        # Send welcome email
        self.welcome_email_check = QCheckBox("Send welcome email with login instructions")
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Full Name:", self.fullname_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Role:", self.role_combo)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        form_layout.addRow("", self.welcome_email_check)
        
        layout.addWidget(form_group)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        
    def validate_and_accept(self):
        """Validate inputs before accepting"""
        if not self.username_input.text():
            QMessageBox.warning(self, "Validation Error", "Username is required")
            return
            
        if not self.email_input.text():
            QMessageBox.warning(self, "Validation Error", "Email is required")
            return
            
        if not self.password_input.text():
            QMessageBox.warning(self, "Validation Error", "Password is required")
            return
            
        if self.password_input.text() != self.confirm_password_input.text():
            QMessageBox.warning(self, "Validation Error", "Passwords do not match")
            return
            
        self.accept()