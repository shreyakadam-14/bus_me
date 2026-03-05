# system_admin_db.py
# modules/system_admin_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QGroupBox, QFormLayout, 
    QMessageBox, QTabWidget, QHeaderView, QDialog,
    QDialogButtonBox, QDateEdit
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QDate
import datetime
from db_connection import DatabaseConnection

class UserManagement(QWidget):
    """User Management with Database Integration"""
    
    user_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setMinimumSize(1000, 600)
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # User List Tab
        user_list_tab = self.create_user_list_tab()
        self.tabs.addTab(user_list_tab, "User List")
        
        # Activity Logs Tab
        activity_tab = self.create_activity_logs_tab()
        self.tabs.addTab(activity_tab, "Activity Logs")
        
        main_layout.addWidget(self.tabs, 1)
    
    def create_header(self):
        """Create header"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        title_label = QLabel("User Management")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.add_user)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_users)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        header_layout.addWidget(refresh_btn)
        
        return header_widget
    
    def create_user_list_tab(self):
        """Create user list tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filter
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.filter_users)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addWidget(QLabel("Role:"))
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All", "Admin", "Manager", "Accountant", "Driver", "Viewer"])
        self.role_filter.currentTextChanged.connect(self.filter_users)
        filter_layout.addWidget(self.role_filter)
        
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive"])
        self.status_filter.currentTextChanged.connect(self.filter_users)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        layout.addWidget(filter_widget)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(7)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Username", "Full Name", "Email", "Role", "Status", "Actions"
        ])
        
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.users_table, 1)
        
        return tab
    
    def create_activity_logs_tab(self):
        """Create activity logs tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filter
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        date_from = QDateEdit()
        date_from.setCalendarPopup(True)
        date_from.setDate(datetime.date.today() - datetime.timedelta(days=7))
        
        date_to = QDateEdit()
        date_to.setCalendarPopup(True)
        date_to.setDate(datetime.date.today())
        
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(date_to)
        
        filter_btn = QPushButton("Filter")
        filter_btn.clicked.connect(lambda: self.load_activity_logs(
            date_from.date().toString('yyyy-MM-dd'),
            date_to.date().toString('yyyy-MM-dd')
        ))
        filter_layout.addWidget(filter_btn)
        
        filter_layout.addStretch()
        layout.addWidget(filter_widget)
        
        # Activity table
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(5)
        self.activity_table.setHorizontalHeaderLabels([
            "Timestamp", "User", "Action", "Module", "Details"
        ])
        
        header = self.activity_table.horizontalHeader()
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        layout.addWidget(self.activity_table, 1)
        
        # Load initial logs
        self.load_activity_logs()
        
        return tab
    
    def load_users(self):
        """Load users from database"""
        try:
            users = self.db.fetch_all("SELECT * FROM users ORDER BY id")
            self.display_users(users)
            self.update_stats(users)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {e}")
    
    def display_users(self, users):
        """Display users in table"""
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # ID
            id_item = QTableWidgetItem(str(user['id']))
            id_item.setData(Qt.UserRole, user['id'])
            self.users_table.setItem(row, 0, id_item)
            
            # Username
            self.users_table.setItem(row, 1, QTableWidgetItem(user.get('username', '')))
            
            # Full Name
            self.users_table.setItem(row, 2, QTableWidgetItem(user.get('full_name', '')))
            
            # Email
            self.users_table.setItem(row, 3, QTableWidgetItem(user.get('email', '')))
            
            # Role
            role_item = QTableWidgetItem(user.get('role', ''))
            if user.get('role') == 'Admin':
                role_item.setForeground(QColor(33, 150, 243))
                role_item.setFont(QFont("Arial", 9, QFont.Bold))
            self.users_table.setItem(row, 4, role_item)
            
            # Status
            status_item = QTableWidgetItem(user.get('status', ''))
            self.colorize_status(status_item, user.get('status'))
            self.users_table.setItem(row, 5, status_item)
            
            # Actions
            action_widget = self.create_action_widget(row, user['id'])
            self.users_table.setCellWidget(row, 6, action_widget)
    
    def create_action_widget(self, row, user_id):
        """Create action buttons"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedWidth(50)
        edit_btn.clicked.connect(lambda: self.edit_user(user_id))
        
        reset_btn = QPushButton("Reset PW")
        reset_btn.setFixedWidth(70)
        reset_btn.clicked.connect(lambda: self.reset_password(user_id))
        
        toggle_btn = QPushButton("Toggle")
        toggle_btn.setFixedWidth(60)
        toggle_btn.clicked.connect(lambda: self.toggle_user(user_id))
        
        layout.addWidget(edit_btn)
        layout.addWidget(reset_btn)
        layout.addWidget(toggle_btn)
        layout.addStretch()
        
        return widget
    
    def colorize_status(self, item, status):
        """Colorize status"""
        if status == 'Active':
            item.setForeground(QColor(76, 175, 80))
        elif status == 'Inactive':
            item.setForeground(QColor(255, 152, 0))
        elif status == 'Locked':
            item.setForeground(QColor(244, 67, 54))
    
    def update_stats(self, users):
        """Update statistics"""
        total = len(users)
        active = len([u for u in users if u.get('status') == 'Active'])
        admins = len([u for u in users if u.get('role') == 'Admin'])
        
        # You could display these stats somewhere
        print(f"Total: {total}, Active: {active}, Admins: {admins}")
    
    def load_activity_logs(self, from_date=None, to_date=None):
        """Load activity logs"""
        try:
            query = "SELECT * FROM activity_logs"
            params = []
            
            if from_date and to_date:
                query += " WHERE date(timestamp) BETWEEN ? AND ?"
                params = [from_date, to_date]
            
            query += " ORDER BY timestamp DESC LIMIT 100"
            logs = self.db.fetch_all(query, params)
            
            self.activity_table.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                self.activity_table.setItem(row, 0, QTableWidgetItem(log.get('timestamp', '')[:19]))
                self.activity_table.setItem(row, 1, QTableWidgetItem(log.get('username', '')))
                self.activity_table.setItem(row, 2, QTableWidgetItem(log.get('action', '')))
                self.activity_table.setItem(row, 3, QTableWidgetItem(log.get('module', '')))
                self.activity_table.setItem(row, 4, QTableWidgetItem(log.get('details', '')))
                
        except Exception as e:
            print(f"Error loading logs: {e}")
    
    def filter_users(self):
        """Filter users based on search and filters"""
        search = self.search_input.text().lower()
        role = self.role_filter.currentText()
        status = self.status_filter.currentText()
        
        for row in range(self.users_table.rowCount()):
            show = True
            
            if search:
                row_text = ''
                for col in range(5):  # Check first 5 columns
                    item = self.users_table.item(row, col)
                    if item:
                        row_text += item.text().lower() + ' '
                if search not in row_text:
                    show = False
            
            if show and role != 'All':
                role_item = self.users_table.item(row, 4)
                if role_item and role_item.text() != role:
                    show = False
            
            if show and status != 'All':
                status_item = self.users_table.item(row, 5)
                if status_item and status_item.text() != status:
                    show = False
            
            self.users_table.setRowHidden(row, not show)
    
    def add_user(self):
        """Add new user"""
        dialog = AddUserDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
            QMessageBox.information(self, "Success", "User added successfully")
    
    def edit_user(self, user_id):
        """Edit user"""
        dialog = EditUserDialog(self.db, user_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
    
    def reset_password(self, user_id):
        """Reset user password"""
        reply = QMessageBox.question(
            self, "Reset Password",
            "Reset password to default?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update('users', {'password': 'default123'}, 'id = ?', [user_id])
                QMessageBox.information(self, "Success", "Password reset to 'default123'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to reset password: {e}")
    
    def toggle_user(self, user_id):
        """Toggle user status"""
        try:
            user = self.db.fetch_one("SELECT status FROM users WHERE id = ?", (user_id,))
            if user:
                new_status = 'Inactive' if user['status'] == 'Active' else 'Active'
                self.db.update('users', {'status': new_status}, 'id = ?', [user_id])
                self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to toggle user: {e}")


class AddUserDialog(QDialog):
    """Add User Dialog"""
    
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add New User")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # Form
        form_group = QGroupBox("User Information")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Manager", "Accountant", "Driver", "Viewer"])
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("default123")
        
        form_layout.addRow("Username*:", self.username_input)
        form_layout.addRow("Full Name*:", self.fullname_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Role:", self.role_combo)
        form_layout.addRow("Password:", self.password_input)
        
        layout.addWidget(form_group)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def validate_and_accept(self):
        """Validate and accept"""
        if not self.username_input.text().strip():
            QMessageBox.warning(self, "Error", "Username is required")
            return
        
        if not self.fullname_input.text().strip():
            QMessageBox.warning(self, "Error", "Full name is required")
            return
        
        try:
            user_data = {
                'username': self.username_input.text().strip(),
                'password': self.password_input.text().strip(),
                'full_name': self.fullname_input.text().strip(),
                'email': self.email_input.text().strip() or None,
                'role': self.role_combo.currentText(),
                'status': 'Active',
                'created_at': datetime.datetime.now().isoformat()
            }
            
            self.db.insert('users', user_data)
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add user: {e}")


class EditUserDialog(QDialog):
    """Edit User Dialog"""
    
    def __init__(self, db, user_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Edit User")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        self.load_user()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # Form
        form_group = QGroupBox("User Information")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setReadOnly(True)
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Manager", "Accountant", "Driver", "Viewer"])
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive"])
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Full Name*:", self.fullname_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Role:", self.role_combo)
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addWidget(form_group)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def load_user(self):
        """Load user data"""
        try:
            user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (self.user_id,))
            if user:
                self.username_input.setText(user.get('username', ''))
                self.fullname_input.setText(user.get('full_name', ''))
                self.email_input.setText(user.get('email', ''))
                self.role_combo.setCurrentText(user.get('role', ''))
                self.status_combo.setCurrentText(user.get('status', 'Active'))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load user: {e}")
    
    def validate_and_accept(self):
        """Validate and accept"""
        if not self.fullname_input.text().strip():
            QMessageBox.warning(self, "Error", "Full name is required")
            return
        
        try:
            user_data = {
                'full_name': self.fullname_input.text().strip(),
                'email': self.email_input.text().strip() or None,
                'role': self.role_combo.currentText(),
                'status': self.status_combo.currentText(),
                'updated_at': datetime.datetime.now().isoformat()
            }
            
            self.db.update('users', user_data, 'id = ?', [self.user_id])
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update user: {e}")