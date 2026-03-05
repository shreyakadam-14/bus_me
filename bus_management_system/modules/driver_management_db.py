# driver_management_db.py
# modules/driver_management_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QFrame,
    QGroupBox, QTabWidget, QTextEdit, QHeaderView,
    QMessageBox, QFormLayout, QDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
from db_connection import DatabaseConnection

class DriverManagementPage(QWidget):
    """Driver Management with Database Integration"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        self.load_drivers()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_label = QLabel("Driver Management")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # Tabs
        self.tab_widget = QTabWidget()
        self.driver_list_tab = DriverListTab(self.db)
        self.driver_form_tab = DriverFormTab(self.db)
        
        # Connect signals
        self.driver_list_tab.driver_selected.connect(self.on_driver_selected)
        
        self.tab_widget.addTab(self.driver_list_tab, "Driver List")
        self.tab_widget.addTab(self.driver_form_tab, "Add/Edit Driver")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.status_label)
    
    def load_drivers(self):
        """Load drivers from database"""
        self.driver_list_tab.refresh()
    
    def on_driver_selected(self, driver_id):
        """Handle driver selection"""
        self.tab_widget.setCurrentIndex(1)
        self.driver_form_tab.load_driver(driver_id)


class DriverListTab(QWidget):
    """Driver List Tab with Database"""
    
    driver_selected = pyqtSignal(int)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Filter section
        self.create_filter_section(layout)
        
        # Driver table
        self.create_driver_table(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # Initial load
        self.refresh()
    
    def create_filter_section(self, parent_layout):
        """Create filter controls"""
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search drivers...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive", "On Leave"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        filter_layout.addWidget(refresh_btn)
        
        parent_layout.addWidget(filter_widget)
    
    def create_driver_table(self, parent_layout):
        """Create driver table"""
        self.driver_table = QTableWidget()
        self.driver_table.setColumnCount(7)
        self.driver_table.setHorizontalHeaderLabels([
            "ID", "Name", "Phone", "License No.", "License Expiry", "Status", "Actions"
        ])
        
        header = self.driver_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        self.driver_table.setAlternatingRowColors(True)
        self.driver_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.driver_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        parent_layout.addWidget(self.driver_table)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 10, 0, 0)
        
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_driver)
        action_layout.addWidget(edit_btn)
        
        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(self.add_new_driver)
        action_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_driver)
        action_layout.addWidget(delete_btn)
        
        action_layout.addStretch()
        
        parent_layout.addWidget(action_widget)
    
    def refresh(self):
        """Refresh driver list"""
        try:
            drivers = self.db.fetch_all("SELECT * FROM drivers ORDER BY id DESC")
            self.display_drivers(drivers)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load drivers: {e}")
    
    def display_drivers(self, drivers):
        """Display drivers in table"""
        self.driver_table.setRowCount(len(drivers))
        
        for row, driver in enumerate(drivers):
            # ID
            id_item = QTableWidgetItem(str(driver['id']))
            id_item.setData(Qt.UserRole, driver['id'])
            self.driver_table.setItem(row, 0, id_item)
            
            # Name
            self.driver_table.setItem(row, 1, QTableWidgetItem(driver.get('name', '')))
            
            # Phone
            self.driver_table.setItem(row, 2, QTableWidgetItem(driver.get('phone', '')))
            
            # License
            self.driver_table.setItem(row, 3, QTableWidgetItem(driver.get('license_number', '')))
            
            # License Expiry
            expiry = driver.get('license_expiry', '')
            expiry_item = QTableWidgetItem(expiry)
            self.colorize_expiry(expiry_item, expiry)
            self.driver_table.setItem(row, 4, expiry_item)
            
            # Status
            status_item = QTableWidgetItem(driver.get('status', 'Unknown'))
            self.colorize_status(status_item, driver.get('status'))
            self.driver_table.setItem(row, 5, status_item)
            
            # Actions
            action_widget = self.create_action_widget(row, driver['id'])
            self.driver_table.setCellWidget(row, 6, action_widget)
    
    def create_action_widget(self, row, driver_id):
        """Create action buttons widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        view_btn = QPushButton("View")
        view_btn.setFixedWidth(50)
        view_btn.clicked.connect(lambda: self.view_driver(driver_id))
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedWidth(50)
        edit_btn.clicked.connect(lambda: self.edit_driver_by_id(driver_id))
        
        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addStretch()
        
        return widget
    
    def colorize_expiry(self, item, expiry_date):
        """Colorize expiry date based on days remaining"""
        if not expiry_date:
            return
        
        try:
            expiry = datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date()
            today = datetime.date.today()
            days = (expiry - today).days
            
            if days < 0:
                item.setBackground(QColor(255, 220, 220))
            elif days <= 30:
                item.setBackground(QColor(255, 255, 200))
        except:
            pass
    
    def colorize_status(self, item, status):
        """Colorize status cell"""
        if status == 'Active':
            item.setBackground(QColor(220, 255, 220))
        elif status == 'On Leave':
            item.setBackground(QColor(255, 255, 200))
        elif status == 'Inactive':
            item.setBackground(QColor(255, 220, 220))
    
    def get_selected_driver_id(self):
        """Get selected driver ID"""
        selected = self.driver_table.selectedItems()
        if selected:
            return int(self.driver_table.item(selected[0].row(), 0).text())
        return None
    
    def view_driver(self, driver_id):
        """View driver details"""
        try:
            driver = self.db.fetch_one("SELECT * FROM drivers WHERE id = ?", (driver_id,))
            if driver:
                dialog = DriverDetailsDialog(driver)
                dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load driver details: {e}")
    
    def edit_driver_by_id(self, driver_id):
        """Edit driver by ID"""
        self.driver_selected.emit(driver_id)
    
    def view_details(self):
        """View selected driver details"""
        driver_id = self.get_selected_driver_id()
        if driver_id:
            self.view_driver(driver_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a driver")
    
    def edit_driver(self):
        """Edit selected driver"""
        driver_id = self.get_selected_driver_id()
        if driver_id:
            self.driver_selected.emit(driver_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a driver")
    
    def add_new_driver(self):
        """Add new driver"""
        self.driver_selected.emit(-1)
    
    def delete_driver(self):
        """Delete selected driver"""
        driver_id = self.get_selected_driver_id()
        if not driver_id:
            QMessageBox.warning(self, "No Selection", "Please select a driver")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this driver?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete('drivers', 'id = ?', [driver_id])
                QMessageBox.information(self, "Success", "Driver deleted successfully")
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete driver: {e}")
    
    def apply_filters(self):
        """Apply filters"""
        # Implementation would filter the displayed data
        pass


class DriverFormTab(QWidget):
    """Driver Form Tab with Database"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_driver_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.form_title = QLabel("Add New Driver")
        self.form_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form_layout.addRow("Full Name*:", self.name_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        form_layout.addRow("Phone*:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        form_layout.addRow("Email:", self.email_input)
        
        # License Number
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Enter license number")
        form_layout.addRow("License Number*:", self.license_input)
        
        # License Expiry
        self.license_expiry = QDateEdit()
        self.license_expiry.setCalendarPopup(True)
        self.license_expiry.setDate(QDate.currentDate().addYears(5))
        form_layout.addRow("License Expiry*:", self.license_expiry)
        
        # Joining Date
        self.joining_date = QDateEdit()
        self.joining_date.setCalendarPopup(True)
        self.joining_date.setDate(QDate.currentDate())
        form_layout.addRow("Joining Date*:", self.joining_date)
        
        # Experience
        self.experience_input = QSpinBox()
        self.experience_input.setRange(0, 50)
        self.experience_input.setValue(0)
        form_layout.addRow("Experience (Years):", self.experience_input)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "On Leave"])
        form_layout.addRow("Status:", self.status_combo)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(60)
        self.address_input.setPlaceholderText("Enter address")
        form_layout.addRow("Address:", self.address_input)
        
        layout.addWidget(form_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Driver")
        self.save_btn.clicked.connect(self.save_driver)
        button_layout.addWidget(self.save_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.status_label)
    
    def load_driver(self, driver_id):
        """Load driver data for editing"""
        if driver_id == -1:
            self.clear_form()
            return
        
        try:
            driver = self.db.fetch_one("SELECT * FROM drivers WHERE id = ?", (driver_id,))
            if driver:
                self.current_driver_id = driver_id
                self.form_title.setText(f"Edit Driver: {driver['name']}")
                
                self.name_input.setText(driver.get('name', ''))
                self.phone_input.setText(driver.get('phone', ''))
                self.email_input.setText(driver.get('email', ''))
                self.license_input.setText(driver.get('license_number', ''))
                
                if driver.get('license_expiry'):
                    expiry = QDate.fromString(driver['license_expiry'], 'yyyy-MM-dd')
                    self.license_expiry.setDate(expiry)
                
                if driver.get('joining_date'):
                    joining = QDate.fromString(driver['joining_date'], 'yyyy-MM-dd')
                    self.joining_date.setDate(joining)
                
                self.experience_input.setValue(driver.get('experience_years', 0))
                self.status_combo.setCurrentText(driver.get('status', 'Active'))
                self.address_input.setPlainText(driver.get('address', ''))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load driver: {e}")
    
    def clear_form(self):
        """Clear form"""
        self.current_driver_id = None
        self.form_title.setText("Add New Driver")
        
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.license_input.clear()
        self.license_expiry.setDate(QDate.currentDate().addYears(5))
        self.joining_date.setDate(QDate.currentDate())
        self.experience_input.setValue(0)
        self.status_combo.setCurrentIndex(0)
        self.address_input.clear()
        
        self.status_label.setText("Form cleared")
    
    def cancel(self):
        """Cancel editing"""
        self.clear_form()
        parent = self.parent().parent().parent()
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)
    
    def validate_form(self):
        """Validate form data"""
        if not self.name_input.text().strip():
            self.status_label.setText("Name is required")
            return False
        if not self.phone_input.text().strip():
            self.status_label.setText("Phone is required")
            return False
        if not self.license_input.text().strip():
            self.status_label.setText("License number is required")
            return False
        return True
    
    def save_driver(self):
        """Save driver to database"""
        if not self.validate_form():
            return
        
        driver_data = {
            'name': self.name_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip() or None,
            'license_number': self.license_input.text().strip(),
            'license_expiry': self.license_expiry.date().toString('yyyy-MM-dd'),
            'joining_date': self.joining_date.date().toString('yyyy-MM-dd'),
            'experience_years': self.experience_input.value(),
            'status': self.status_combo.currentText(),
            'address': self.address_input.toPlainText().strip() or None,
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        try:
            if self.current_driver_id:
                self.db.update('drivers', driver_data, 'id = ?', [self.current_driver_id])
                action = "updated"
            else:
                driver_data['created_at'] = datetime.datetime.now().isoformat()
                self.db.insert('drivers', driver_data)
                action = "added"
            
            self.status_label.setText(f"Driver {action} successfully")
            
            parent = self.parent().parent().parent()
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(0)
                parent.load_drivers()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save driver: {e}")


class DriverDetailsDialog(QDialog):
    """Driver Details Dialog"""
    
    def __init__(self, driver_data):
        super().__init__()
        self.driver_data = driver_data
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"Driver Details - {self.driver_data.get('name', 'Unknown')}")
        self.setFixedSize(400, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(self.driver_data.get('name', 'Unknown'))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addWidget(separator)
        
        # Details
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)
        
        details = [
            ("Phone:", self.driver_data.get('phone', 'N/A')),
            ("Email:", self.driver_data.get('email', 'N/A')),
            ("License:", self.driver_data.get('license_number', 'N/A')),
            ("License Expiry:", self.driver_data.get('license_expiry', 'N/A')),
            ("Joined:", self.driver_data.get('joining_date', 'N/A')),
            ("Experience:", f"{self.driver_data.get('experience_years', 0)} years"),
            ("Status:", self.driver_data.get('status', 'N/A')),
            ("Address:", self.driver_data.get('address', 'N/A'))
        ]
        
        for label, value in details:
            value_label = QLabel(str(value))
            value_label.setWordWrap(True)
            form_layout.addRow(label, value_label)
        
        layout.addWidget(form_widget)
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)