# login_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bus Management System - Login")
        self.setFixedSize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("BUS MANAGEMENT SYSTEM")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Login")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        
        # Username
        username_label = QLabel("Username:")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        
        # Password
        password_label = QLabel("Password:")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.Password)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.authenticate)
        
        # Status
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        
        # Add all widgets
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(username_label)
        layout.addWidget(self.username)
        layout.addWidget(password_label)
        layout.addWidget(self.password)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.status)
        
        self.setLayout(layout)
        
        # Set focus
        self.username.setFocus()
        
    def authenticate(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            self.status.setText("Please enter username and password")
            return
            
        # Simple authentication
        if username == "admin" and password == "admin123":
            self.status.setText("Login successful!")
            self.login_btn.setEnabled(False)
            # Use QTimer to simulate loading
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self.login_successful.emit(username, "Admin"))
        else:
            self.status.setText("Invalid credentials")
            
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.authenticate()