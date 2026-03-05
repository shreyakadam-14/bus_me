# login_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

# Import database
from database_manager import DatabaseManager
from daos import UserDAO
from session import UserSession

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bus Management System - Login")
        self.setFixedSize(400, 350)
        
        # Initialize database components
        try:
            self.db_manager = DatabaseManager()
            self.user_dao = UserDAO()
            self.session = UserSession()
            print("✓ Login window: Database components initialized")
        except Exception as e:
            print(f"⚠ Login window: Database init warning - {e}")
            self.db_manager = None
            self.user_dao = None
            self.session = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("BUS MANAGEMENT SYSTEM")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Login to access the system")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        # Username
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10))
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(30)
        
        # Password
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(30)
        
        # Remember me
        self.remember_check = QCheckBox("Remember me")
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedHeight(35)
        self.login_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.login_btn.clicked.connect(self.authenticate)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; min-height: 20px;")
        
        # Add all widgets
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(separator)
        layout.addSpacing(10)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember_check)
        layout.addSpacing(5)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Set focus
        self.username_input.setFocus()
        
    def authenticate(self):
        """Authenticate user"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.status_label.setText("Please enter username and password")
            return
        
        # Disable button during authentication
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Authenticating...")
        
        # Try database authentication first
        if self.user_dao:
            try:
                user = self.user_dao.authenticate(username, password)
                if user:
                    # Update last login
                    self.user_dao.update_last_login(user['id'])
                    
                    # Store in session
                    if self.session:
                        self.session.login(user)
                    
                    self.status_label.setStyleSheet("color: green;")
                    self.status_label.setText("Login successful!")
                    
                    # Log activity
                    self.user_dao.log_activity(
                        'LOGIN', 
                        'System', 
                        f"User {username} logged in successfully",
                        username
                    )
                    
                    # Delay before proceeding
                    QTimer.singleShot(1000, lambda: self.login_successful.emit(
                        username, user['role']
                    ))
                    return
            except Exception as e:
                print(f"Database authentication error: {e}")
        
        # Fallback to hardcoded credentials if database fails
        if username == "admin" and password == "admin123":
            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText("Login successful! (Demo mode)")
            QTimer.singleShot(1000, lambda: self.login_successful.emit(username, "Admin"))
        elif username == "manager" and password == "manager123":
            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText("Login successful! (Demo mode)")
            QTimer.singleShot(1000, lambda: self.login_successful.emit(username, "Manager"))
        elif username == "viewer" and password == "viewer123":
            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText("Login successful! (Demo mode)")
            QTimer.singleShot(1000, lambda: self.login_successful.emit(username, "Viewer"))
        else:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText("Invalid username or password")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Login")
    
    def keyPressEvent(self, event):
        """Handle Enter key"""
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.authenticate()
        super().keyPressEvent(event)