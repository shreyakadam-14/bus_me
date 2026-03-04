from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QFrame, QGroupBox,
    QTabWidget, QTextEdit, QHeaderView, QMessageBox,
    QCheckBox, QFileDialog, QFormLayout, QDialog, QGridLayout,
    QRadioButton, QButtonGroup, QTextEdit, QListWidget, QListWidgetItem,
    QInputDialog
)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QDate
import datetime

# Mock data for drivers
MOCK_DRIVERS = [
    {
        'id': 1,
        'name': 'Rajesh Kumar',
        'phone': '9876543210',
        'license_number': 'DL-0420150001234',
        'license_expiry': '2024-12-31',
        'status': 'Active',
        'salary': 25000,
        'salary_status': 'Paid',
        'bus_assigned': 'BUS-001',
        'joining_date': '2020-05-15',
        'bank_account': '123456789012',
        'ifsc_code': 'SBIN0000123',
        'address': '123 Main Street, Mumbai',
        'emergency_contact': '9876543211',
        'experience_years': 5,
        'rating': 4.5
    },
    {
        'id': 2,
        'name': 'Suresh Patel',
        'phone': '9876543211',
        'license_number': 'MH-0120150005678',
        'license_expiry': '2023-11-30',
        'status': 'Active',
        'salary': 28000,
        'salary_status': 'Pending',
        'bus_assigned': 'BUS-002',
        'joining_date': '2019-08-22',
        'bank_account': '234567890123',
        'ifsc_code': 'HDFC0000456',
        'address': '456 Park Avenue, Delhi',
        'emergency_contact': '9876543212',
        'experience_years': 7,
        'rating': 4.2
    },
    {
        'id': 3,
        'name': 'Amit Sharma',
        'phone': '9876543212',
        'license_number': 'GJ-0120160009012',
        'license_expiry': '2025-06-15',
        'status': 'Active',
        'salary': 23000,
        'salary_status': 'Paid',
        'bus_assigned': 'BUS-003',
        'joining_date': '2021-03-10',
        'bank_account': '345678901234',
        'ifsc_code': 'ICIC0000789',
        'address': '789 Lake Road, Ahmedabad',
        'emergency_contact': '9876543213',
        'experience_years': 3,
        'rating': 4.7
    },
    {
        'id': 4,
        'name': 'Vikram Singh',
        'phone': '9876543213',
        'license_number': 'UP-0120170003456',
        'license_expiry': '2023-09-30',
        'status': 'Inactive',
        'salary': 27000,
        'salary_status': 'Overdue',
        'bus_assigned': 'BUS-004',
        'joining_date': '2018-11-05',
        'bank_account': '456789012345',
        'ifsc_code': 'AXIS0000912',
        'address': '101 Hill View, Lucknow',
        'emergency_contact': '9876543214',
        'experience_years': 6,
        'rating': 4.0
    },
    {
        'id': 5,
        'name': 'Anil Gupta',
        'phone': '9876543214',
        'license_number': 'RJ-0120180007890',
        'license_expiry': '2024-08-20',
        'status': 'Active',
        'salary': 26000,
        'salary_status': 'Pending',
        'bus_assigned': 'BUS-005',
        'joining_date': '2022-01-18',
        'bank_account': '567890123456',
        'ifsc_code': 'PNB0000345',
        'address': '202 Green Park, Jaipur',
        'emergency_contact': '9876543215',
        'experience_years': 2,
        'rating': 4.3
    }
]

# Available buses for assignment
AVAILABLE_BUSES = ['BUS-001', 'BUS-002', 'BUS-003', 'BUS-004', 'BUS-005', 'BUS-006', 'BUS-007', 'BUS-008']


class DriverManagementPage(QWidget):
    """
    Main Driver Management Page - To be integrated into the main application
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Page header
        header_label = QLabel("Driver Management")
        header_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(header_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Create tab widget for different driver management sections
        self.tab_widget = QTabWidget()
        
        # Create tabs (EXCLUDING SALARY TABS)
        self.driver_list_tab = DriverListTab()
        self.driver_form_tab = DriverFormTab()
        
        # Add only driver-related tabs
        self.tab_widget.addTab(self.driver_list_tab, "Driver List")
        self.tab_widget.addTab(self.driver_form_tab, "Add/Edit Driver")
        
        main_layout.addWidget(self.tab_widget)
        
        # Add status label at bottom
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #7f8c8d;")
        main_layout.addWidget(self.status_label)


class DriverListTab(QWidget):
    """Tab for listing and managing drivers"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_drivers()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Search and filter section
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, license...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.filter_drivers)
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive"])
        self.status_filter.currentTextChanged.connect(self.filter_drivers)
        self.status_filter.setFixedWidth(120)
        filter_layout.addWidget(self.status_filter)
        
        # Salary status filter (removing this since we're excluding salary module)
        # filter_layout.addWidget(QLabel("Salary Status:"))
        # self.salary_filter = QComboBox()
        # self.salary_filter.addItems(["All", "Paid", "Pending", "Overdue"])
        # self.salary_filter.currentTextChanged.connect(self.filter_drivers)
        # self.salary_filter.setFixedWidth(120)
        # filter_layout.addWidget(self.salary_filter)
        
        # Bus assignment filter
        filter_layout.addWidget(QLabel("Bus Assigned:"))
        self.bus_filter = QComboBox()
        self.bus_filter.addItems(["All"] + AVAILABLE_BUSES)
        self.bus_filter.currentTextChanged.connect(self.filter_drivers)
        self.bus_filter.setFixedWidth(120)
        filter_layout.addWidget(self.bus_filter)
        
        filter_layout.addStretch()
        
        # Export buttons
        export_excel_btn = QPushButton("Export to Excel")
        export_excel_btn.clicked.connect(self.export_to_excel)
        filter_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("Export to PDF")
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        filter_layout.addWidget(export_pdf_btn)
        
        layout.addWidget(filter_widget)
        
        # Driver table - remove salary-related columns
        self.driver_table = QTableWidget()
        self.driver_table.setColumnCount(8)  # Reduced from 10
        self.driver_table.setHorizontalHeaderLabels([
            "Name", "Phone", "License No.", "License Expiry", 
            "Status", "Bus Assigned", "Joining Date", "Experience"
        ])
        self.driver_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.driver_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.driver_table)
        
        # Action buttons section
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        
        # Bulk operations
        bulk_label = QLabel("Bulk Operations:")
        action_layout.addWidget(bulk_label)
        
        self.bulk_action = QComboBox()
        self.bulk_action.addItems(["Update Status", "Assign Bus", "Export Selected", "Print Details"])
        action_layout.addWidget(self.bulk_action)
        
        bulk_apply_btn = QPushButton("Apply")
        bulk_apply_btn.clicked.connect(self.apply_bulk_operation)
        action_layout.addWidget(bulk_apply_btn)
        
        action_layout.addStretch()
        
        # Individual action buttons
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit Driver")
        edit_btn.clicked.connect(self.edit_driver)
        action_layout.addWidget(edit_btn)
        
        assign_btn = QPushButton("Assign/Reassign Bus")
        assign_btn.clicked.connect(self.assign_bus)
        action_layout.addWidget(assign_btn)
        
        # Remove salary button
        # pay_salary_btn = QPushButton("Pay Salary")
        # pay_salary_btn.clicked.connect(self.pay_salary)
        # action_layout.addWidget(pay_salary_btn)
        
        delete_btn = QPushButton("Delete Driver")
        delete_btn.clicked.connect(self.delete_driver)
        action_layout.addWidget(delete_btn)
        
        layout.addWidget(action_widget)
        
    def load_drivers(self):
        """Load drivers into the table (without salary columns)"""
        self.driver_table.setRowCount(len(MOCK_DRIVERS))
        
        for row, driver in enumerate(MOCK_DRIVERS):
            # Name
            item = QTableWidgetItem(driver['name'])
            self.driver_table.setItem(row, 0, item)
            
            # Phone
            item = QTableWidgetItem(driver['phone'])
            self.driver_table.setItem(row, 1, item)
            
            # License Number
            item = QTableWidgetItem(driver['license_number'])
            self.driver_table.setItem(row, 2, item)
            
            # License Expiry with color coding
            expiry_date = driver['license_expiry']
            expiry_item = QTableWidgetItem(expiry_date)
            
            # Check if license is expired or expiring soon
            expiry_qdate = QDate.fromString(expiry_date, 'yyyy-MM-dd')
            days_to_expiry = QDate.currentDate().daysTo(expiry_qdate)
            
            if days_to_expiry < 0:
                expiry_item.setBackground(QColor(255, 220, 220))  # Red for expired
                expiry_item.setForeground(QColor(139, 0, 0))
            elif days_to_expiry <= 30:
                expiry_item.setBackground(QColor(255, 255, 200))  # Yellow for expiring soon
                expiry_item.setForeground(QColor(153, 102, 0))
            
            self.driver_table.setItem(row, 3, expiry_item)
            
            # Status with color coding
            status_item = QTableWidgetItem(driver['status'])
            if driver['status'] == 'Active':
                status_item.setBackground(QColor(220, 255, 220))
                status_item.setForeground(QColor(0, 100, 0))
            else:
                status_item.setBackground(QColor(255, 220, 220))
                status_item.setForeground(QColor(139, 0, 0))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.driver_table.setItem(row, 4, status_item)
            
            # Bus Assigned
            item = QTableWidgetItem(driver['bus_assigned'])
            self.driver_table.setItem(row, 5, item)
            
            # Joining Date
            item = QTableWidgetItem(driver['joining_date'])
            self.driver_table.setItem(row, 6, item)
            
            # Experience
            item = QTableWidgetItem(f"{driver['experience_years']} years")
            self.driver_table.setItem(row, 7, item)
            
    def filter_drivers(self):
        """Filter drivers based on search and filter criteria"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()
        bus_filter = self.bus_filter.currentText()
        
        for row in range(self.driver_table.rowCount()):
            show_row = True
            
            # Search filter
            if search_text:
                row_text = ''
                for col in range(self.driver_table.columnCount()):
                    item = self.driver_table.item(row, col)
                    if item:
                        row_text += item.text().lower() + ' '
                if search_text not in row_text:
                    show_row = False
            
            # Status filter
            if status_filter != 'All':
                status_item = self.driver_table.item(row, 4)
                if status_item and status_item.text() != status_filter:
                    show_row = False
            
            # Bus filter
            if bus_filter != 'All':
                bus_item = self.driver_table.item(row, 5)
                if bus_item and bus_item.text() != bus_filter:
                    show_row = False
            
            self.driver_table.setRowHidden(row, not show_row)
            
    def get_selected_driver(self):
        """Get the currently selected driver"""
        selected_items = self.driver_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return MOCK_DRIVERS[row] if row < len(MOCK_DRIVERS) else None
        return None
        
    def view_details(self):
        """View details of selected driver"""
        driver = self.get_selected_driver()
        if driver:
            dialog = DriverDetailsDialog(driver)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a driver first")
            
    def edit_driver(self):
        """Edit selected driver"""
        driver = self.get_selected_driver()
        if driver:
            # Switch to driver form tab with edit mode
            parent = self.parent().parent().parent()  # Get DriverManagementPage
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(1)  # Switch to form tab
                parent.driver_form_tab.load_driver_data(driver)
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a driver first")
            
    def assign_bus(self):
        """Assign/reassign bus to selected driver"""
        driver = self.get_selected_driver()
        if driver:
            dialog = AssignBusDialog(driver, AVAILABLE_BUSES)
            if dialog.exec_() == QDialog.Accepted:
                QMessageBox.information(self, "Success", 
                                      f"Bus assigned to {driver['name']} (demo mode)")
                self.load_drivers()
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a driver first")
            
    def delete_driver(self):
        """Delete selected driver"""
        driver = self.get_selected_driver()
        if driver:
            reply = QMessageBox.question(self, "Confirm Delete",
                                       f"Delete driver {driver['name']}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Success", 
                                      f"Driver {driver['name']} deleted (demo mode)")
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a driver first")
            
    def apply_bulk_operation(self):
        """Apply bulk operation"""
        operation = self.bulk_action.currentText()
        
        if operation == "Update Status":
            status, ok = QInputDialog.getItem(self, "Update Status", 
                                            "Select new status:", ["Active", "Inactive"], 0, False)
            if ok and status:
                QMessageBox.information(self, "Bulk Update", 
                                      f"Updated status to {status} for selected drivers (demo mode)")
        elif operation == "Assign Bus":
            bus, ok = QInputDialog.getItem(self, "Assign Bus", 
                                         "Select bus:", AVAILABLE_BUSES, 0, False)
            if ok and bus:
                QMessageBox.information(self, "Bulk Assignment", 
                                      f"Assigned {bus} to selected drivers (demo mode)")
        else:
            QMessageBox.information(self, "Bulk Operation", 
                                  f"{operation} applied to selected drivers (demo mode)")
        
    def export_to_excel(self):
        """Export to Excel"""
        QMessageBox.information(self, "Export", 
                              "Driver data exported to Excel (demo mode)")
        
    def export_to_pdf(self):
        """Export to PDF"""
        QMessageBox.information(self, "Export", 
                              "Driver data exported to PDF (demo mode)")


class DriverFormTab(QWidget):
    """Tab for adding/editing driver details"""
    
    def __init__(self):
        super().__init__()
        self.current_driver = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form title
        self.form_title = QLabel("Add New Driver")
        self.form_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Create tab widget for form sections
        form_tabs = QTabWidget()
        
        # Personal Information Tab
        personal_tab = self.create_personal_info_tab()
        form_tabs.addTab(personal_tab, "Personal Information")
        
        # License & Employment Tab
        license_tab = self.create_license_employment_tab()
        form_tabs.addTab(license_tab, "License & Employment")
        
        # Bank & Salary Tab (keeping but will simplify)
        bank_tab = self.create_bank_info_tab()
        form_tabs.addTab(bank_tab, "Bank Information")
        
        # Emergency Contacts Tab
        emergency_tab = self.create_emergency_contacts_tab()
        form_tabs.addTab(emergency_tab, "Emergency Contacts")
        
        layout.addWidget(form_tabs)
        
        # Form buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Driver")
        self.save_btn.clicked.connect(self.save_driver)
        button_layout.addWidget(self.save_btn)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.status_label)
        
    def create_personal_info_tab(self):
        """Create personal information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        layout.addRow("Full Name*:", self.name_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter 10-digit mobile number")
        self.phone_input.setInputMask("9999999999")
        layout.addRow("Phone Number*:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        layout.addRow("Email:", self.email_input)
        
        # Date of Birth
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate(1985, 1, 1))
        self.dob_input.setMaximumDate(QDate.currentDate().addYears(-18))
        layout.addRow("Date of Birth:", self.dob_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("Enter complete address")
        layout.addRow("Address:", self.address_input)
        
        # Gender
        gender_widget = QWidget()
        gender_layout = QHBoxLayout(gender_widget)
        gender_layout.setContentsMargins(0, 0, 0, 0)
        
        self.gender_group = QButtonGroup()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.other_radio = QRadioButton("Other")
        
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.other_radio)
        
        self.male_radio.setChecked(True)
        
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.other_radio)
        
        layout.addRow("Gender:", gender_widget)
        
        return tab
        
    def create_license_employment_tab(self):
        """Create license and employment tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # License Number
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Enter driving license number")
        layout.addRow("License Number*:", self.license_input)
        
        # License Expiry
        self.license_expiry = QDateEdit()
        self.license_expiry.setCalendarPopup(True)
        self.license_expiry.setDate(QDate.currentDate().addYears(5))
        layout.addRow("License Expiry Date*:", self.license_expiry)
        
        # License Type
        self.license_type = QComboBox()
        self.license_type.addItems(["LMV", "HMV", "MCWG", "MCWOG", "International"])
        layout.addRow("License Type:", self.license_type)
        
        # Experience Years
        self.experience_input = QSpinBox()
        self.experience_input.setRange(0, 50)
        self.experience_input.setValue(5)
        layout.addRow("Experience (Years):", self.experience_input)
        
        # Joining Date
        self.joining_date = QDateEdit()
        self.joining_date.setCalendarPopup(True)
        self.joining_date.setDate(QDate.currentDate())
        layout.addRow("Joining Date*:", self.joining_date)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "On Leave", "Suspended"])
        layout.addRow("Employment Status:", self.status_combo)
        
        # Assigned Bus
        self.bus_assigned = QComboBox()
        self.bus_assigned.addItems([""] + AVAILABLE_BUSES)
        layout.addRow("Assigned Bus:", self.bus_assigned)
        
        return tab
        
    def create_bank_info_tab(self):
        """Create simplified bank information tab (without salary)"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Bank Name
        self.bank_name = QComboBox()
        self.bank_name.setEditable(True)
        self.bank_name.addItems(["State Bank of India", "HDFC Bank", "ICICI Bank", 
                                "Axis Bank", "Punjab National Bank", "Other"])
        layout.addRow("Bank Name:", self.bank_name)
        
        # Account Number
        self.account_number = QLineEdit()
        self.account_number.setPlaceholderText("Enter account number")
        layout.addRow("Account Number*:", self.account_number)
        
        # IFSC Code
        self.ifsc_code = QLineEdit()
        self.ifsc_code.setPlaceholderText("Enter IFSC code")
        layout.addRow("IFSC Code*:", self.ifsc_code)
        
        # Account Holder Name
        self.account_holder = QLineEdit()
        self.account_holder.setPlaceholderText("Enter account holder name")
        layout.addRow("Account Holder Name:", self.account_holder)
        
        # PAN Number
        self.pan_number = QLineEdit()
        self.pan_number.setPlaceholderText("Enter PAN number")
        layout.addRow("PAN Number:", self.pan_number)
        
        return tab
        
    def create_emergency_contacts_tab(self):
        """Create emergency contacts tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Emergency Contact Name
        self.emergency_name = QLineEdit()
        self.emergency_name.setPlaceholderText("Enter emergency contact name")
        layout.addRow("Emergency Contact Name*:", self.emergency_name)
        
        # Emergency Phone
        self.emergency_phone = QLineEdit()
        self.emergency_phone.setPlaceholderText("Enter emergency contact number")
        self.emergency_phone.setInputMask("9999999999")
        layout.addRow("Emergency Phone*:", self.emergency_phone)
        
        # Relationship
        self.emergency_relation = QComboBox()
        self.emergency_relation.addItems(["Spouse", "Father", "Mother", "Son", 
                                         "Daughter", "Sibling", "Relative", "Friend"])
        layout.addRow("Relationship:", self.emergency_relation)
        
        # Medical Information
        self.medical_info = QTextEdit()
        self.medical_info.setMaximumHeight(60)
        self.medical_info.setPlaceholderText("Any medical conditions or allergies")
        layout.addRow("Medical Information:", self.medical_info)
        
        # Additional Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Additional notes or information")
        layout.addRow("Additional Notes:", self.notes_input)
        
        return tab
        
    def load_driver_data(self, driver_data):
        """Load existing driver data into form"""
        self.current_driver = driver_data
        self.form_title.setText(f"Edit Driver: {driver_data['name']}")
        
        # Personal information
        self.name_input.setText(driver_data['name'])
        self.phone_input.setText(driver_data['phone'])
        self.address_input.setPlainText(driver_data['address'])
        
        # License & employment
        self.license_input.setText(driver_data['license_number'])
        expiry_date = QDate.fromString(driver_data['license_expiry'], 'yyyy-MM-dd')
        self.license_expiry.setDate(expiry_date)
        
        joining_date = QDate.fromString(driver_data['joining_date'], 'yyyy-MM-dd')
        self.joining_date.setDate(joining_date)
        
        self.experience_input.setValue(driver_data['experience_years'])
        self.status_combo.setCurrentText(driver_data['status'])
        self.bus_assigned.setCurrentText(driver_data['bus_assigned'])
        
        # Bank information
        self.account_number.setText(driver_data['bank_account'])
        self.ifsc_code.setText(driver_data['ifsc_code'])
        
        # Emergency contacts
        self.emergency_phone.setText(driver_data['emergency_contact'])
        
    def browse_document(self):
        """Browse for documents"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Document", "",
            "All Files (*);;PDF Files (*.pdf);;Image Files (*.png *.jpg)"
        )
        if file_path:
            QMessageBox.information(self, "Document Selected", 
                                  f"Selected: {file_path}")
            
    def clear_form(self):
        """Clear the form"""
        self.current_driver = None
        self.form_title.setText("Add New Driver")
        
        # Clear all fields
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.dob_input.setDate(QDate(1985, 1, 1))
        self.address_input.clear()
        
        self.license_input.clear()
        self.license_expiry.setDate(QDate.currentDate().addYears(5))
        self.license_type.setCurrentIndex(0)
        self.experience_input.setValue(5)
        self.joining_date.setDate(QDate.currentDate())
        self.status_combo.setCurrentIndex(0)
        self.bus_assigned.setCurrentIndex(0)
        
        self.bank_name.setCurrentIndex(0)
        self.account_number.clear()
        self.ifsc_code.clear()
        self.account_holder.clear()
        self.pan_number.clear()
        
        self.emergency_name.clear()
        self.emergency_phone.clear()
        self.emergency_relation.setCurrentIndex(0)
        self.medical_info.clear()
        self.notes_input.clear()
        
        self.status_label.setText("Form cleared")
        
    def save_driver(self):
        """Save driver data"""
        # Basic validation
        if not self.name_input.text().strip():
            self.status_label.setText("Error: Full name is required")
            return
            
        if not self.phone_input.text().strip() or len(self.phone_input.text()) != 10:
            self.status_label.setText("Error: Valid 10-digit phone number is required")
            return
            
        if not self.license_input.text().strip():
            self.status_label.setText("Error: License number is required")
            return
            
        if not self.account_number.text().strip():
            self.status_label.setText("Error: Account number is required")
            return
            
        # Save logic (in real app, this would save to database)
        if self.current_driver:
            action = "updated"
        else:
            action = "added"
            
        QMessageBox.information(self, "Success", 
                              f"Driver {action} successfully!")
        self.status_label.setText(f"Driver {action} at {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Switch back to driver list
        parent = self.parent().parent().parent()  # Get DriverManagementPage
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)  # Switch to list tab


# Placeholder dialog classes to prevent errors
class DriverDetailsDialog(QDialog):
    """Dialog for showing driver details"""
    def __init__(self, driver_data):
        super().__init__()
        self.setWindowTitle(f"Driver Details: {driver_data['name']}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Details for {driver_data['name']}"))
        layout.addWidget(QLabel(f"Phone: {driver_data['phone']}"))
        layout.addWidget(QLabel(f"License: {driver_data['license_number']}"))
        layout.addWidget(QLabel(f"Status: {driver_data['status']}"))
        layout.addWidget(QLabel(f"Bus Assigned: {driver_data['bus_assigned']}"))
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class AssignBusDialog(QDialog):
    """Dialog for assigning bus to driver"""
    def __init__(self, driver_data, available_buses):
        super().__init__()
        self.setWindowTitle(f"Assign Bus to {driver_data['name']}")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"Current Bus: {driver_data['bus_assigned']}"))
        
        self.bus_combo = QComboBox()
        self.bus_combo.addItems(available_buses)
        layout.addWidget(QLabel("Select New Bus:"))
        layout.addWidget(self.bus_combo)
        
        button_layout = QHBoxLayout()
        assign_btn = QPushButton("Assign")
        assign_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(assign_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)