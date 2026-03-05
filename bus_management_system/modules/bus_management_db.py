# bus_management_db.py
# modules/bus_management_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox,
    QFrame, QGroupBox, QTabWidget, QTextEdit, QHeaderView,
    QMessageBox, QCheckBox, QFileDialog, QFormLayout, QDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
from db_connection import DatabaseConnection

class BusManagementPage(QWidget):
    """Bus Management with Database Integration"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        self.load_buses()
        
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_label = QLabel("Bus Management")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.bus_list_tab = BusListTab(self.db)
        self.bus_form_tab = BusFormTab(self.db)
        self.insurance_tracker_tab = InsuranceTrackerTab(self.db)
        self.insurance_renewal_tab = InsuranceRenewalTab(self.db)
        
        # Connect signals
        self.bus_list_tab.bus_selected.connect(self.on_bus_selected)
        self.bus_list_tab.refresh_requested.connect(self.load_buses)
        self.bus_form_tab.bus_saved.connect(self.on_bus_saved)
        
        # Add tabs
        self.tab_widget.addTab(self.bus_list_tab, "Bus List")
        self.tab_widget.addTab(self.bus_form_tab, "Add/Edit Bus")
        self.tab_widget.addTab(self.insurance_tracker_tab, "Insurance Tracker")
        self.tab_widget.addTab(self.insurance_renewal_tab, "Renew Insurance")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.status_label)
    
    def load_buses(self):
        """Load buses from database"""
        self.bus_list_tab.refresh()
        self.insurance_tracker_tab.refresh_stats()
    
    def on_bus_selected(self, bus_id):
        """Handle bus selection"""
        self.tab_widget.setCurrentIndex(1)
        self.bus_form_tab.load_bus(bus_id)
    
    def on_bus_saved(self, bus_id):
        """Handle bus saved"""
        self.status_label.setText(f"Bus saved at {datetime.datetime.now().strftime('%H:%M:%S')}")
        self.tab_widget.setCurrentIndex(0)
        self.load_buses()


class BusListTab(QWidget):
    """Bus List Tab with Database"""
    
    bus_selected = pyqtSignal(int)
    refresh_requested = pyqtSignal()
    
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
        
        # Bus table
        self.create_bus_table(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # Initial load
        self.refresh()
    
    def create_filter_section(self, parent_layout):
        """Create filter controls"""
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search buses...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive", "Maintenance"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)
        self.status_filter.setFixedWidth(120)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        filter_layout.addWidget(refresh_btn)
        
        parent_layout.addWidget(filter_widget)
    
    def create_bus_table(self, parent_layout):
        """Create bus table"""
        self.bus_table = QTableWidget()
        self.bus_table.setColumnCount(9)
        self.bus_table.setHorizontalHeaderLabels([
            "ID", "Registration", "Bus No.", "Model", "Capacity",
            "Year", "Status", "Insurance", "Actions"
        ])
        
        header = self.bus_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        
        self.bus_table.setAlternatingRowColors(True)
        self.bus_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bus_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bus_table.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        parent_layout.addWidget(self.bus_table)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 10, 0, 0)
        
        # Action buttons
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_bus)
        action_layout.addWidget(edit_btn)
        
        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(self.add_new_bus)
        action_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_bus)
        action_layout.addWidget(delete_btn)
        
        action_layout.addStretch()
        
        parent_layout.addWidget(action_widget)
    
    def refresh(self):
        """Refresh bus list"""
        try:
            query = """
                SELECT b.*, 
                       COUNT(i.id) as has_insurance,
                       MAX(i.expiry_date) as latest_insurance
                FROM buses b
                LEFT JOIN insurance i ON b.id = i.bus_id
                GROUP BY b.id
                ORDER BY b.id DESC
            """
            buses = self.db.fetch_all(query)
            self.display_buses(buses)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load buses: {e}")
    
    def display_buses(self, buses):
        """Display buses in table"""
        self.bus_table.setRowCount(len(buses))
        
        for row, bus in enumerate(buses):
            # ID
            id_item = QTableWidgetItem(str(bus['id']))
            id_item.setData(Qt.UserRole, bus['id'])
            self.bus_table.setItem(row, 0, id_item)
            
            # Registration
            self.bus_table.setItem(row, 1, QTableWidgetItem(bus.get('registration_number', '')))
            
            # Bus Number
            self.bus_table.setItem(row, 2, QTableWidgetItem(bus.get('bus_number', '')))
            
            # Model
            self.bus_table.setItem(row, 3, QTableWidgetItem(bus.get('model', '')))
            
            # Capacity
            cap_item = QTableWidgetItem(str(bus.get('capacity', '')))
            cap_item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 4, cap_item)
            
            # Year
            year_item = QTableWidgetItem(str(bus.get('year', '')))
            year_item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 5, year_item)
            
            # Status
            status_item = QTableWidgetItem(bus.get('status', 'Unknown'))
            self.colorize_status(status_item, bus.get('status'))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 6, status_item)
            
            # Insurance Status
            insurance_status = "Active" if bus.get('has_insurance', 0) > 0 else "No Insurance"
            ins_item = QTableWidgetItem(insurance_status)
            if bus.get('has_insurance', 0) > 0:
                ins_item.setBackground(QColor(220, 255, 220))
            self.bus_table.setItem(row, 7, ins_item)
            
            # Actions
            action_widget = self.create_action_widget(row, bus['id'])
            self.bus_table.setCellWidget(row, 8, action_widget)
    
    def create_action_widget(self, row, bus_id):
        """Create action buttons widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        view_btn = QPushButton("View")
        view_btn.setFixedWidth(50)
        view_btn.clicked.connect(lambda: self.view_bus(bus_id))
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedWidth(50)
        edit_btn.clicked.connect(lambda: self.edit_bus_by_id(bus_id))
        
        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addStretch()
        
        return widget
    
    def colorize_status(self, item, status):
        """Colorize status cell"""
        if status == 'Active':
            item.setBackground(QColor(220, 255, 220))
            item.setForeground(QColor(0, 100, 0))
        elif status == 'Maintenance':
            item.setBackground(QColor(255, 255, 200))
            item.setForeground(QColor(153, 102, 0))
        elif status == 'Inactive':
            item.setBackground(QColor(255, 220, 220))
            item.setForeground(QColor(139, 0, 0))
    
    def get_selected_bus_id(self):
        """Get selected bus ID"""
        selected = self.bus_table.selectedItems()
        if selected:
            return int(self.bus_table.item(selected[0].row(), 0).text())
        return None
    
    def on_item_double_clicked(self, item):
        """Handle double click"""
        bus_id = self.get_selected_bus_id()
        if bus_id:
            self.view_bus(bus_id)
    
    def view_bus(self, bus_id):
        """View bus details"""
        try:
            bus = self.db.fetch_one("SELECT * FROM buses WHERE id = ?", (bus_id,))
            if bus:
                dialog = BusDetailsDialog(bus)
                dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load bus details: {e}")
    
    def edit_bus_by_id(self, bus_id):
        """Edit bus by ID"""
        self.bus_selected.emit(bus_id)
    
    def view_details(self):
        """View selected bus details"""
        bus_id = self.get_selected_bus_id()
        if bus_id:
            self.view_bus(bus_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a bus")
    
    def edit_bus(self):
        """Edit selected bus"""
        bus_id = self.get_selected_bus_id()
        if bus_id:
            self.bus_selected.emit(bus_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a bus")
    
    def add_new_bus(self):
        """Add new bus"""
        self.bus_selected.emit(-1)  # -1 indicates new bus
    
    def delete_bus(self):
        """Delete selected bus"""
        bus_id = self.get_selected_bus_id()
        if not bus_id:
            QMessageBox.warning(self, "No Selection", "Please select a bus")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this bus?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete('buses', 'id = ?', [bus_id])
                QMessageBox.information(self, "Success", "Bus deleted successfully")
                self.refresh()
                self.refresh_requested.emit()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete bus: {e}")
    
    def apply_filters(self):
        """Apply filters"""
        # Implementation would filter the displayed data
        pass


class BusFormTab(QWidget):
    """Bus Form Tab with Database"""
    
    bus_saved = pyqtSignal(int)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_bus_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.form_title = QLabel("Add New Bus")
        self.form_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)
        
        # Registration Number
        self.reg_number = QLineEdit()
        self.reg_number.setPlaceholderText("e.g., MH-01-AB-1234")
        form_layout.addRow("Registration Number*:", self.reg_number)
        
        # Bus Number
        self.bus_number = QLineEdit()
        self.bus_number.setPlaceholderText("e.g., BUS-001")
        form_layout.addRow("Bus Number*:", self.bus_number)
        
        # Model
        self.model = QLineEdit()
        self.model.setPlaceholderText("e.g., Tata Starbus")
        form_layout.addRow("Model:", self.model)
        
        # Capacity
        self.capacity = QSpinBox()
        self.capacity.setRange(1, 100)
        self.capacity.setValue(40)
        form_layout.addRow("Capacity:", self.capacity)
        
        # Year
        self.year = QSpinBox()
        self.year.setRange(2000, 2025)
        self.year.setValue(2023)
        form_layout.addRow("Year:", self.year)
        
        # Color
        self.color = QLineEdit()
        self.color.setPlaceholderText("e.g., White")
        form_layout.addRow("Color:", self.color)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "Maintenance"])
        form_layout.addRow("Status:", self.status_combo)
        
        layout.addWidget(form_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Bus")
        self.save_btn.clicked.connect(self.save_bus)
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
    
    def load_bus(self, bus_id):
        """Load bus data for editing"""
        if bus_id == -1:  # New bus
            self.clear_form()
            return
        
        try:
            bus = self.db.fetch_one("SELECT * FROM buses WHERE id = ?", (bus_id,))
            if bus:
                self.current_bus_id = bus_id
                self.form_title.setText(f"Edit Bus: {bus['registration_number']}")
                
                self.reg_number.setText(bus['registration_number'] or '')
                self.bus_number.setText(bus['bus_number'] or '')
                self.model.setText(bus['model'] or '')
                self.capacity.setValue(bus['capacity'] or 40)
                self.year.setValue(bus['year'] or 2023)
                self.color.setText(bus['color'] or '')
                self.status_combo.setCurrentText(bus['status'] or 'Active')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load bus: {e}")
    
    def clear_form(self):
        """Clear form"""
        self.current_bus_id = None
        self.form_title.setText("Add New Bus")
        
        self.reg_number.clear()
        self.bus_number.clear()
        self.model.clear()
        self.capacity.setValue(40)
        self.year.setValue(2023)
        self.color.clear()
        self.status_combo.setCurrentIndex(0)
        
        self.status_label.setText("Form cleared")
    
    def cancel(self):
        """Cancel editing"""
        self.clear_form()
        parent = self.parent().parent().parent()
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)
    
    def validate_form(self):
        """Validate form data"""
        if not self.reg_number.text().strip():
            self.status_label.setText("Registration number is required")
            return False
        if not self.bus_number.text().strip():
            self.status_label.setText("Bus number is required")
            return False
        return True
    
    def save_bus(self):
        """Save bus to database"""
        if not self.validate_form():
            return
        
        bus_data = {
            'registration_number': self.reg_number.text().strip(),
            'bus_number': self.bus_number.text().strip(),
            'model': self.model.text().strip() or None,
            'capacity': self.capacity.value(),
            'year': self.year.value(),
            'color': self.color.text().strip() or None,
            'status': self.status_combo.currentText(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        try:
            if self.current_bus_id:
                # Update
                self.db.update('buses', bus_data, 'id = ?', [self.current_bus_id])
                bus_id = self.current_bus_id
                action = "updated"
            else:
                # Insert
                bus_data['created_at'] = datetime.datetime.now().isoformat()
                bus_id = self.db.insert('buses', bus_data)
                action = "added"
            
            self.status_label.setText(f"Bus {action} successfully")
            self.bus_saved.emit(bus_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save bus: {e}")


class InsuranceTrackerTab(QWidget):
    """Insurance Tracker with Database"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Stats
        self.create_stats(layout)
        
        # Insurance table
        self.create_insurance_table(layout)
        
        # Refresh
        self.refresh_stats()
    
    def create_stats(self, parent_layout):
        """Create statistics"""
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        self.total_label = QLabel("Total: 0")
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.active_label = QLabel("Active: 0")
        self.active_label.setFont(QFont("Arial", 12))
        
        self.expiring_label = QLabel("Expiring Soon: 0")
        self.expiring_label.setFont(QFont("Arial", 12))
        
        self.expired_label = QLabel("Expired: 0")
        self.expired_label.setFont(QFont("Arial", 12))
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.active_label)
        stats_layout.addWidget(self.expiring_label)
        stats_layout.addWidget(self.expired_label)
        stats_layout.addStretch()
        
        parent_layout.addWidget(stats_widget)
    
    def create_insurance_table(self, parent_layout):
        """Create insurance table"""
        self.insurance_table = QTableWidget()
        self.insurance_table.setColumnCount(7)
        self.insurance_table.setHorizontalHeaderLabels([
            "Bus", "Policy Number", "Provider", "Coverage",
            "Premium", "Expiry Date", "Status"
        ])
        
        header = self.insurance_table.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        self.insurance_table.setAlternatingRowColors(True)
        self.insurance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        parent_layout.addWidget(self.insurance_table)
    
    def refresh_stats(self):
        """Refresh insurance statistics"""
        try:
            # Get stats
            query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN expiry_date > date('now') THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN expiry_date BETWEEN date('now') AND date('now', '+30 days') THEN 1 ELSE 0 END) as expiring,
                    SUM(CASE WHEN expiry_date < date('now') THEN 1 ELSE 0 END) as expired
                FROM insurance
                WHERE status = 'Active'
            """
            stats = self.db.fetch_one(query) or {}
            
            self.total_label.setText(f"Total: {stats.get('total', 0)}")
            self.active_label.setText(f"Active: {stats.get('active', 0)}")
            self.expiring_label.setText(f"Expiring Soon: {stats.get('expiring', 0)}")
            self.expired_label.setText(f"Expired: {stats.get('expired', 0)}")
            
            # Load insurance data
            self.load_insurance_data()
            
        except Exception as e:
            print(f"Error loading stats: {e}")
    
    def load_insurance_data(self):
        """Load insurance data"""
        try:
            query = """
                SELECT b.registration_number, i.*
                FROM insurance i
                JOIN buses b ON i.bus_id = b.id
                ORDER BY i.expiry_date
            """
            policies = self.db.fetch_all(query)
            
            self.insurance_table.setRowCount(len(policies))
            
            for row, policy in enumerate(policies):
                self.insurance_table.setItem(row, 0, QTableWidgetItem(policy.get('registration_number', '')))
                self.insurance_table.setItem(row, 1, QTableWidgetItem(policy.get('policy_number', '')))
                self.insurance_table.setItem(row, 2, QTableWidgetItem(policy.get('provider', '')))
                self.insurance_table.setItem(row, 3, QTableWidgetItem(f"₹ {policy.get('coverage_amount', 0):,.0f}"))
                self.insurance_table.setItem(row, 4, QTableWidgetItem(f"₹ {policy.get('premium_amount', 0):,.0f}"))
                self.insurance_table.setItem(row, 5, QTableWidgetItem(policy.get('expiry_date', '')))
                
                status = self.get_insurance_status(policy)
                status_item = QTableWidgetItem(status)
                self.colorize_insurance(status_item, status)
                self.insurance_table.setItem(row, 6, status_item)
                
        except Exception as e:
            print(f"Error loading insurance: {e}")
    
    def get_insurance_status(self, policy):
        """Get insurance status"""
        if not policy.get('expiry_date'):
            return 'No Data'
        
        try:
            expiry = datetime.datetime.strptime(policy['expiry_date'], '%Y-%m-%d').date()
            today = datetime.date.today()
            days = (expiry - today).days
            
            if days < 0:
                return 'Expired'
            elif days <= 30:
                return 'Expiring Soon'
            else:
                return 'Active'
        except:
            return 'Unknown'
    
    def colorize_insurance(self, item, status):
        """Colorize insurance status"""
        if status == 'Active':
            item.setBackground(QColor(220, 255, 220))
        elif status == 'Expiring Soon':
            item.setBackground(QColor(255, 255, 200))
        elif status == 'Expired':
            item.setBackground(QColor(255, 220, 220))


class InsuranceRenewalTab(QWidget):
    """Insurance Renewal with Database"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_bus_id = None
        self.init_ui()
        self.load_buses()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.title = QLabel("Renew Insurance")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.title)
        
        # Bus selection
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Select Bus:"))
        self.bus_combo = QComboBox()
        self.bus_combo.currentIndexChanged.connect(self.bus_selected)
        select_layout.addWidget(self.bus_combo)
        select_layout.addStretch()
        layout.addLayout(select_layout)
        
        # Current Insurance
        current_group = QGroupBox("Current Insurance")
        current_layout = QFormLayout(current_group)
        
        self.current_policy = QLineEdit()
        self.current_policy.setReadOnly(True)
        current_layout.addRow("Policy:", self.current_policy)
        
        self.current_provider = QLineEdit()
        self.current_provider.setReadOnly(True)
        current_layout.addRow("Provider:", self.current_provider)
        
        self.current_expiry = QLineEdit()
        self.current_expiry.setReadOnly(True)
        current_layout.addRow("Expires:", self.current_expiry)
        
        layout.addWidget(current_group)
        
        # New Insurance
        new_group = QGroupBox("New Insurance")
        new_layout = QFormLayout(new_group)
        
        self.new_policy = QLineEdit()
        self.new_policy.setPlaceholderText("Enter new policy number")
        new_layout.addRow("Policy Number*:", self.new_policy)
        
        self.new_provider = QLineEdit()
        self.new_provider.setPlaceholderText("Enter provider name")
        new_layout.addRow("Provider:", self.new_provider)
        
        self.new_coverage = QDoubleSpinBox()
        self.new_coverage.setRange(0, 10000000)
        self.new_coverage.setPrefix("₹ ")
        self.new_coverage.setValue(5000000)
        new_layout.addRow("Coverage:", self.new_coverage)
        
        self.new_premium = QDoubleSpinBox()
        self.new_premium.setRange(0, 500000)
        self.new_premium.setPrefix("₹ ")
        self.new_premium.setValue(75000)
        new_layout.addRow("Premium:", self.new_premium)
        
        # Dates
        dates_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addYears(1))
        
        dates_layout.addWidget(QLabel("Start:"))
        dates_layout.addWidget(self.start_date)
        dates_layout.addWidget(QLabel("Expiry:"))
        dates_layout.addWidget(self.expiry_date)
        dates_layout.addStretch()
        
        new_layout.addRow("", dates_layout)
        
        layout.addWidget(new_group)
        
        # Renew button
        renew_btn = QPushButton("Renew Insurance")
        renew_btn.clicked.connect(self.process_renewal)
        renew_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        layout.addWidget(renew_btn)
        
        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
    
    def load_buses(self):
        """Load buses into combo box"""
        try:
            buses = self.db.fetch_all("SELECT id, registration_number, bus_number FROM buses ORDER BY registration_number")
            self.bus_combo.clear()
            self.bus_combo.addItem("Select a bus", None)
            for bus in buses:
                text = f"{bus['registration_number']} - {bus['bus_number']}"
                self.bus_combo.addItem(text, bus['id'])
        except Exception as e:
            print(f"Error loading buses: {e}")
    
    def bus_selected(self):
        """Handle bus selection"""
        bus_id = self.bus_combo.currentData()
        if not bus_id:
            self.clear_current()
            return
        
        try:
            # Get current insurance
            query = """
                SELECT * FROM insurance 
                WHERE bus_id = ? AND status = 'Active'
                ORDER BY id DESC LIMIT 1
            """
            insurance = self.db.fetch_one(query, (bus_id,))
            
            if insurance:
                self.current_policy.setText(insurance.get('policy_number', ''))
                self.current_provider.setText(insurance.get('provider', ''))
                self.current_expiry.setText(insurance.get('expiry_date', ''))
                
                # Auto-fill new form
                self.new_provider.setText(insurance.get('provider', ''))
                self.new_coverage.setValue(insurance.get('coverage_amount', 5000000))
                self.new_premium.setValue(insurance.get('premium_amount', 75000))
                
                # Set start date after expiry
                if insurance.get('expiry_date'):
                    expiry = QDate.fromString(insurance['expiry_date'], 'yyyy-MM-dd')
                    self.start_date.setDate(expiry.addDays(1))
            else:
                self.clear_current()
            
            self.current_bus_id = bus_id
            
        except Exception as e:
            print(f"Error loading insurance: {e}")
    
    def clear_current(self):
        """Clear current insurance display"""
        self.current_policy.clear()
        self.current_provider.clear()
        self.current_expiry.clear()
    
    def process_renewal(self):
        """Process insurance renewal"""
        if not self.current_bus_id:
            QMessageBox.warning(self, "No Selection", "Please select a bus")
            return
        
        if not self.new_policy.text().strip():
            self.status_label.setText("Policy number is required")
            return
        
        if self.start_date.date() >= self.expiry_date.date():
            self.status_label.setText("Expiry date must be after start date")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Renewal",
            "Renew insurance for this bus?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Mark old insurance as expired
                self.db.update('insurance', {'status': 'Expired'}, 
                              'bus_id = ? AND status = "Active"', [self.current_bus_id])
                
                # Add new insurance
                insurance_data = {
                    'bus_id': self.current_bus_id,
                    'policy_number': self.new_policy.text().strip(),
                    'provider': self.new_provider.text().strip(),
                    'coverage_amount': self.new_coverage.value(),
                    'premium_amount': self.new_premium.value(),
                    'start_date': self.start_date.date().toString('yyyy-MM-dd'),
                    'expiry_date': self.expiry_date.date().toString('yyyy-MM-dd'),
                    'status': 'Active',
                    'created_at': datetime.datetime.now().isoformat()
                }
                
                self.db.insert('insurance', insurance_data)
                
                QMessageBox.information(self, "Success", "Insurance renewed successfully")
                self.status_label.setText(f"Renewed at {datetime.datetime.now().strftime('%H:%M:%S')}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to renew insurance: {e}")


class BusDetailsDialog(QDialog):
    """Bus Details Dialog"""
    
    def __init__(self, bus_data):
        super().__init__()
        self.bus_data = bus_data
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"Bus Details - {self.bus_data.get('registration_number', 'Unknown')}")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(self.bus_data.get('registration_number', 'Unknown'))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel(f"{self.bus_data.get('bus_number', '')} - {self.bus_data.get('model', '')}")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addWidget(separator)
        
        # Details
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)
        
        details = [
            ("Registration:", self.bus_data.get('registration_number', 'N/A')),
            ("Bus Number:", self.bus_data.get('bus_number', 'N/A')),
            ("Model:", self.bus_data.get('model', 'N/A')),
            ("Capacity:", str(self.bus_data.get('capacity', 'N/A'))),
            ("Year:", str(self.bus_data.get('year', 'N/A'))),
            ("Color:", self.bus_data.get('color', 'N/A')),
            ("Status:", self.bus_data.get('status', 'N/A')),
            ("Created:", self.bus_data.get('created_at', 'N/A')[:10] if self.bus_data.get('created_at') else 'N/A')
        ]
        
        for label, value in details:
            value_label = QLabel(value)
            form_layout.addRow(label, value_label)
        
        layout.addWidget(form_widget)
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)