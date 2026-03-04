from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QFrame, QGroupBox,
    QTabWidget, QTextEdit, QHeaderView, QMessageBox,
    QCheckBox, QFileDialog, QFormLayout, QDialog, QGridLayout,
    QRadioButton, QButtonGroup, QTextEdit, QListWidget, QListWidgetItem,
    QInputDialog, QTimeEdit, QScrollArea
)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QDate
import datetime

# Mock data for schools
MOCK_SCHOOLS = [
    {
        'id': 1,
        'name': 'Delhi Public School',
        'school_code': 'DPS001',
        'type': 'Private',
        'address': '123 Education Lane, Delhi',
        'city': 'Delhi',
        'phone': '011-23456789',
        'email': 'contact@dpsdelhi.edu.in',
        'principal_name': 'Dr. Ramesh Sharma',
        'contact_person': 'Mr. Anil Kumar',
        'contact_person_phone': '9876543210',
        'student_count': 2500,
        'contract_status': 'Active',
        'contract_start': '2023-01-01',
        'contract_end': '2024-12-31',
        'monthly_fee': 150000,
        'payment_status': 'Paid',
        'assigned_buses': ['BUS-001', 'BUS-002'],
        'pickup_time': '07:30',
        'drop_time': '14:30',
        'billing_address': 'Same as school address',
        'gst_number': '07AABCD1234E1Z5'
    },
    {
        'id': 2,
        'name': 'Kendriya Vidyalaya',
        'school_code': 'KV001',
        'type': 'Government',
        'address': '456 Government Road, Delhi',
        'city': 'Delhi',
        'phone': '011-34567890',
        'email': 'kvdelhi@kvs.gov.in',
        'principal_name': 'Dr. Sunita Verma',
        'contact_person': 'Mr. Rajesh Singh',
        'contact_person_phone': '9876543211',
        'student_count': 1800,
        'contract_status': 'Active',
        'contract_start': '2023-03-01',
        'contract_end': '2025-02-28',
        'monthly_fee': 120000,
        'payment_status': 'Pending',
        'assigned_buses': ['BUS-003', 'BUS-004'],
        'pickup_time': '08:00',
        'drop_time': '15:00',
        'billing_address': 'Kendriya Vidyalaya, Delhi',
        'gst_number': '07BABCD1234E1Z6'
    },
    {
        'id': 3,
        'name': 'Modern Public School',
        'school_code': 'MPS001',
        'type': 'Private',
        'address': '789 Modern Road, Gurgaon',
        'city': 'Gurgaon',
        'phone': '0124-4567890',
        'email': 'info@modernschool.edu.in',
        'principal_name': 'Mrs. Priya Kapoor',
        'contact_person': 'Mr. Vikas Gupta',
        'contact_person_phone': '9876543212',
        'student_count': 3000,
        'contract_status': 'Active',
        'contract_start': '2023-06-01',
        'contract_end': '2024-05-31',
        'monthly_fee': 200000,
        'payment_status': 'Paid',
        'assigned_buses': ['BUS-005'],
        'pickup_time': '07:45',
        'drop_time': '14:45',
        'billing_address': 'Modern School Accounts Dept, Gurgaon',
        'gst_number': '06CABCD1234E1Z7'
    },
    {
        'id': 4,
        'name': 'Little Angels School',
        'school_code': 'LAS001',
        'type': 'Private',
        'address': '101 Children Street, Noida',
        'city': 'Noida',
        'phone': '0120-5678901',
        'email': 'contact@littleangels.edu.in',
        'principal_name': 'Mrs. Anjali Mehta',
        'contact_person': 'Mr. Sanjay Patel',
        'contact_person_phone': '9876543213',
        'student_count': 1200,
        'contract_status': 'Expiring Soon',
        'contract_start': '2022-04-01',
        'contract_end': '2023-12-31',
        'monthly_fee': 80000,
        'payment_status': 'Overdue',
        'assigned_buses': ['BUS-006'],
        'pickup_time': '08:15',
        'drop_time': '15:15',
        'billing_address': 'Little Angels School, Noida',
        'gst_number': '09DABCD1234E1Z8'
    },
    {
        'id': 5,
        'name': 'Government Senior Secondary School',
        'school_code': 'GSSS001',
        'type': 'Government',
        'address': '202 Public Sector, Faridabad',
        'city': 'Faridabad',
        'phone': '0129-6789012',
        'email': 'gsss.fbd@edu.gov.in',
        'principal_name': 'Mr. Harish Yadav',
        'contact_person': 'Mr. Rakesh Kumar',
        'contact_person_phone': '9876543214',
        'student_count': 2200,
        'contract_status': 'Inactive',
        'contract_start': '2022-09-01',
        'contract_end': '2023-08-31',
        'monthly_fee': 100000,
        'payment_status': 'Paid',
        'assigned_buses': ['BUS-007', 'BUS-008'],
        'pickup_time': '07:15',
        'drop_time': '14:15',
        'billing_address': 'GSSS Faridabad',
        'gst_number': '06EABCD1234E1Z9'
    }
]

# Available buses for assignment
AVAILABLE_BUSES = ['BUS-001', 'BUS-002', 'BUS-003', 'BUS-004', 'BUS-005', 'BUS-006', 'BUS-007', 'BUS-008', 'BUS-009', 'BUS-010']

# School types
SCHOOL_TYPES = ['Private', 'Government', 'International', 'CBSE', 'ICSE', 'State Board']
CONTRACT_STATUSES = ['Active', 'Inactive', 'Expiring Soon', 'Negotiation', 'Terminated']
PAYMENT_STATUSES = ['Paid', 'Pending', 'Overdue', 'Partially Paid']


class SchoolManagementPage(QWidget):
    """
    Main School Management Page - To be integrated into the main application
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
        header_label = QLabel("School Management")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(header_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Create tab widget for different school management sections
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.school_list_tab = SchoolListTab()
        self.school_form_tab = SchoolFormTab()
        self.school_bus_assignment_tab = SchoolBusAssignmentTab()
        
        # Add tabs
        self.tab_widget.addTab(self.school_list_tab, "School List")
        self.tab_widget.addTab(self.school_form_tab, "Add/Edit School")
        self.tab_widget.addTab(self.school_bus_assignment_tab, "Bus Assignment")
        
        main_layout.addWidget(self.tab_widget)
        
        # Add status label at bottom
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #7f8c8d;")
        main_layout.addWidget(self.status_label)


class SchoolListTab(QWidget):
    """Tab for listing and managing schools"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_schools()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Search and filter section
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, location, code...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.filter_schools)
        filter_layout.addWidget(self.search_input)
        
        # Contract status filter
        filter_layout.addWidget(QLabel("Contract Status:"))
        self.contract_filter = QComboBox()
        self.contract_filter.addItems(["All"] + CONTRACT_STATUSES)
        self.contract_filter.currentTextChanged.connect(self.filter_schools)
        self.contract_filter.setFixedWidth(150)
        filter_layout.addWidget(self.contract_filter)
        
        # School type filter
        filter_layout.addWidget(QLabel("School Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All"] + SCHOOL_TYPES)
        self.type_filter.currentTextChanged.connect(self.filter_schools)
        self.type_filter.setFixedWidth(150)
        filter_layout.addWidget(self.type_filter)
        
        # City filter
        filter_layout.addWidget(QLabel("City:"))
        self.city_filter = QComboBox()
        self.city_filter.addItems(["All", "Delhi", "Gurgaon", "Noida", "Faridabad", "Ghaziabad"])
        self.city_filter.currentTextChanged.connect(self.filter_schools)
        self.city_filter.setFixedWidth(120)
        filter_layout.addWidget(self.city_filter)
        
        filter_layout.addStretch()
        
        # Export buttons
        export_excel_btn = QPushButton("Export to Excel")
        export_excel_btn.clicked.connect(self.export_to_excel)
        filter_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("Export to PDF")
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        filter_layout.addWidget(export_pdf_btn)
        
        layout.addWidget(filter_widget)
        
        # School table
        self.school_table = QTableWidget()
        self.school_table.setColumnCount(10)
        self.school_table.setHorizontalHeaderLabels([
            "School Name", "Code", "Type", "Location", 
            "Contact Person", "Phone", "Contract Status", 
            "Monthly Fee", "Assigned Buses", "Students"
        ])
        self.school_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.school_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.school_table)
        
        # Action buttons section
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        
        # Bulk operations
        bulk_label = QLabel("Bulk Operations:")
        action_layout.addWidget(bulk_label)
        
        self.bulk_action = QComboBox()
        self.bulk_action.addItems(["Update Contract Status", "Generate Invoices", "Export Selected", "Print Contracts"])
        action_layout.addWidget(self.bulk_action)
        
        bulk_apply_btn = QPushButton("Apply")
        bulk_apply_btn.clicked.connect(self.apply_bulk_operation)
        action_layout.addWidget(bulk_apply_btn)
        
        action_layout.addStretch()
        
        # Individual action buttons
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit School")
        edit_btn.clicked.connect(self.edit_school)
        action_layout.addWidget(edit_btn)
        
        assign_bus_btn = QPushButton("Assign Buses")
        assign_bus_btn.clicked.connect(self.assign_buses)
        action_layout.addWidget(assign_bus_btn)
        
        contract_btn = QPushButton("View Contract")
        contract_btn.clicked.connect(self.view_contract)
        action_layout.addWidget(contract_btn)
        
        delete_btn = QPushButton("Delete School")
        delete_btn.clicked.connect(self.delete_school)
        action_layout.addWidget(delete_btn)
        
        layout.addWidget(action_widget)
        
    def load_schools(self):
        """Load schools into the table"""
        self.school_table.setRowCount(len(MOCK_SCHOOLS))
        
        for row, school in enumerate(MOCK_SCHOOLS):
            # School Name
            item = QTableWidgetItem(school['name'])
            self.school_table.setItem(row, 0, item)
            
            # School Code
            item = QTableWidgetItem(school['school_code'])
            self.school_table.setItem(row, 1, item)
            
            # School Type
            item = QTableWidgetItem(school['type'])
            self.school_table.setItem(row, 2, item)
            
            # Location (City)
            item = QTableWidgetItem(school['city'])
            self.school_table.setItem(row, 3, item)
            
            # Contact Person
            item = QTableWidgetItem(school['contact_person'])
            self.school_table.setItem(row, 4, item)
            
            # Phone
            item = QTableWidgetItem(school['phone'])
            self.school_table.setItem(row, 5, item)
            
            # Contract Status with color coding
            contract_item = QTableWidgetItem(school['contract_status'])
            if school['contract_status'] == 'Active':
                contract_item.setBackground(QColor(220, 255, 220))
                contract_item.setForeground(QColor(0, 100, 0))
            elif school['contract_status'] == 'Expiring Soon':
                contract_item.setBackground(QColor(255, 255, 200))
                contract_item.setForeground(QColor(153, 102, 0))
            elif school['contract_status'] == 'Inactive':
                contract_item.setBackground(QColor(255, 220, 220))
                contract_item.setForeground(QColor(139, 0, 0))
            else:
                contract_item.setBackground(QColor(230, 230, 230))
                contract_item.setForeground(QColor(100, 100, 100))
            contract_item.setTextAlignment(Qt.AlignCenter)
            self.school_table.setItem(row, 6, contract_item)
            
            # Monthly Fee
            item = QTableWidgetItem(f"₹ {school['monthly_fee']:,}")
            item.setTextAlignment(Qt.AlignRight)
            self.school_table.setItem(row, 7, item)
            
            # Assigned Buses
            buses_text = ", ".join(school['assigned_buses']) if school['assigned_buses'] else "None"
            item = QTableWidgetItem(buses_text)
            self.school_table.setItem(row, 8, item)
            
            # Students
            item = QTableWidgetItem(f"{school['student_count']:,}")
            item.setTextAlignment(Qt.AlignCenter)
            self.school_table.setItem(row, 9, item)
            
    def filter_schools(self):
        """Filter schools based on search and filter criteria"""
        search_text = self.search_input.text().lower()
        contract_filter = self.contract_filter.currentText()
        type_filter = self.type_filter.currentText()
        city_filter = self.city_filter.currentText()
        
        for row in range(self.school_table.rowCount()):
            show_row = True
            
            # Search filter
            if search_text:
                row_text = ''
                for col in range(self.school_table.columnCount()):
                    item = self.school_table.item(row, col)
                    if item:
                        row_text += item.text().lower() + ' '
                if search_text not in row_text:
                    show_row = False
            
            # Contract status filter
            if contract_filter != 'All':
                contract_item = self.school_table.item(row, 6)
                if contract_item and contract_item.text() != contract_filter:
                    show_row = False
            
            # School type filter
            if type_filter != 'All':
                type_item = self.school_table.item(row, 2)
                if type_item and type_item.text() != type_filter:
                    show_row = False
            
            # City filter
            if city_filter != 'All':
                city_item = self.school_table.item(row, 3)
                if city_item and city_item.text() != city_filter:
                    show_row = False
            
            self.school_table.setRowHidden(row, not show_row)
            
    def get_selected_school(self):
        """Get the currently selected school"""
        selected_items = self.school_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return MOCK_SCHOOLS[row] if row < len(MOCK_SCHOOLS) else None
        return None
        
    def view_details(self):
        """View details of selected school"""
        school = self.get_selected_school()
        if school:
            #dialog = SchoolDetailsDialog(school)
            #dialog.exec_()
            print(f"View details for: {school}") 
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a school first")
            
    def edit_school(self):
        """Edit selected school"""
        school = self.get_selected_school()
        if school:
            # Switch to school form tab with edit mode
            parent = self.parent().parent().parent()  # Get SchoolManagementPage
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(1)  # Switch to form tab
                parent.school_form_tab.load_school_data(school)
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a school first")
            
    def assign_buses(self):
        """Assign buses to selected school"""
        school = self.get_selected_school()
        if school:
            # Switch to bus assignment tab
            parent = self.parent().parent().parent()  # Get SchoolManagementPage
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(2)  # Switch to bus assignment tab
                parent.school_bus_assignment_tab.load_school_data(school)
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a school first")
            
    def view_contract(self):
        """View contract of selected school"""
        school = self.get_selected_school()
        if school:
            #dialog = ContractDetailsDialog(school)
            #dialog.exec_()
            print(f"View details for: {school}") 
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a school first")
            
    def delete_school(self):
        """Delete selected school"""
        school = self.get_selected_school()
        if school:
            reply = QMessageBox.question(self, "Confirm Delete",
                                       f"Delete school {school['name']}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Success", 
                                      f"School {school['name']} deleted (demo mode)")
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a school first")
            
    def apply_bulk_operation(self):
        """Apply bulk operation"""
        operation = self.bulk_action.currentText()
        
        if operation == "Update Contract Status":
            status, ok = QInputDialog.getItem(self, "Update Contract Status", 
                                            "Select new status:", CONTRACT_STATUSES, 0, False)
            if ok and status:
                QMessageBox.information(self, "Bulk Update", 
                                      f"Updated contract status to {status} for selected schools (demo mode)")
        elif operation == "Generate Invoices":
            month, ok = QInputDialog.getItem(self, "Generate Invoices", 
                                           "Select month:", ["January", "February", "March", "April", 
                                                           "May", "June", "July", "August", 
                                                           "September", "October", "November", "December"], 0, False)
            if ok and month:
                QMessageBox.information(self, "Invoice Generation", 
                                      f"Invoices generated for {month} (demo mode)")
        else:
            QMessageBox.information(self, "Bulk Operation", 
                                  f"{operation} applied to selected schools (demo mode)")
        
    def export_to_excel(self):
        """Export to Excel"""
        QMessageBox.information(self, "Export", 
                              "School data exported to Excel (demo mode)")
        
    def export_to_pdf(self):
        """Export to PDF"""
        QMessageBox.information(self, "Export", 
                              "School data exported to PDF (demo mode)")


class SchoolFormTab(QWidget):
    """Tab for adding/editing school details"""
    
    def __init__(self):
        super().__init__()
        self.current_school = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form title
        self.form_title = QLabel("Add New School")
        self.form_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Create scroll area for long form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Create tab widget for form sections
        form_tabs = QTabWidget()
        
        # Basic Information Tab
        basic_tab = self.create_basic_info_tab()
        form_tabs.addTab(basic_tab, "Basic Information")
        
        # Contact Information Tab
        contact_tab = self.create_contact_info_tab()
        form_tabs.addTab(contact_tab, "Contact Information")
        
        # Contract & Billing Tab
        contract_tab = self.create_contract_billing_tab()
        form_tabs.addTab(contract_tab, "Contract & Billing")
        
        # Transportation Details Tab
        transport_tab = self.create_transport_details_tab()
        form_tabs.addTab(transport_tab, "Transportation Details")
        
        scroll_layout.addWidget(form_tabs)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Form buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save School")
        self.save_btn.clicked.connect(self.save_school)
        button_layout.addWidget(self.save_btn)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.status_label)
        
    def create_basic_info_tab(self):
        """Create basic information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # School Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter school name")
        layout.addRow("School Name*:", self.name_input)
        
        # School Code
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter school code")
        layout.addRow("School Code*:", self.code_input)
        
        # School Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(SCHOOL_TYPES)
        layout.addRow("School Type*:", self.type_combo)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(60)
        self.address_input.setPlaceholderText("Enter school address")
        layout.addRow("Address*:", self.address_input)
        
        # City
        self.city_input = QComboBox()
        self.city_input.setEditable(True)
        self.city_input.addItems(["Delhi", "Gurgaon", "Noida", "Faridabad", "Ghaziabad", "Other"])
        layout.addRow("City*:", self.city_input)
        
        # Student Count
        self.student_count = QSpinBox()
        self.student_count.setRange(0, 10000)
        self.student_count.setValue(1000)
        self.student_count.setSingleStep(100)
        layout.addRow("Student Count:", self.student_count)
        
        # Establishment Year
        self.establishment_year = QSpinBox()
        self.establishment_year.setRange(1900, datetime.datetime.now().year)
        self.establishment_year.setValue(2000)
        layout.addRow("Establishment Year:", self.establishment_year)
        
        return tab
        
    def create_contact_info_tab(self):
        """Create contact information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Principal Name
        self.principal_name = QLineEdit()
        self.principal_name.setPlaceholderText("Enter principal name")
        layout.addRow("Principal Name*:", self.principal_name)
        
        # School Phone
        self.school_phone = QLineEdit()
        self.school_phone.setPlaceholderText("Enter school phone number")
        layout.addRow("School Phone*:", self.school_phone)
        
        # School Email
        self.school_email = QLineEdit()
        self.school_email.setPlaceholderText("Enter school email")
        layout.addRow("School Email:", self.school_email)
        
        # Contact Person Name
        self.contact_person = QLineEdit()
        self.contact_person.setPlaceholderText("Enter contact person name")
        layout.addRow("Contact Person*:", self.contact_person)
        
        # Contact Person Phone
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("Enter contact person phone")
        self.contact_phone.setInputMask("9999999999")
        layout.addRow("Contact Person Phone*:", self.contact_phone)
        
        # Contact Person Email
        self.contact_email = QLineEdit()
        self.contact_email.setPlaceholderText("Enter contact person email")
        layout.addRow("Contact Person Email:", self.contact_email)
        
        # Designation
        self.designation = QComboBox()
        self.designation.addItems(["Transport In-charge", "Administrator", "Principal", "Accountant", "Other"])
        layout.addRow("Designation:", self.designation)
        
        return tab
        
    def create_contract_billing_tab(self):
        """Create contract and billing tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Contract Status
        self.contract_status = QComboBox()
        self.contract_status.addItems(CONTRACT_STATUSES)
        layout.addRow("Contract Status:", self.contract_status)
        
        # Contract Start Date
        self.contract_start = QDateEdit()
        self.contract_start.setCalendarPopup(True)
        self.contract_start.setDate(QDate.currentDate())
        layout.addRow("Contract Start Date*:", self.contract_start)
        
        # Contract End Date
        self.contract_end = QDateEdit()
        self.contract_end.setCalendarPopup(True)
        self.contract_end.setDate(QDate.currentDate().addYears(1))
        layout.addRow("Contract End Date*:", self.contract_end)
        
        # Monthly Fee
        self.monthly_fee = QDoubleSpinBox()
        self.monthly_fee.setRange(0, 1000000)
        self.monthly_fee.setPrefix("₹ ")
        self.monthly_fee.setValue(100000)
        self.monthly_fee.setSingleStep(10000)
        layout.addRow("Monthly Fee*:", self.monthly_fee)
        
        # Payment Status
        self.payment_status = QComboBox()
        self.payment_status.addItems(PAYMENT_STATUSES)
        layout.addRow("Payment Status:", self.payment_status)
        
        # Billing Address
        self.billing_address = QTextEdit()
        self.billing_address.setMaximumHeight(60)
        self.billing_address.setPlaceholderText("Enter billing address")
        layout.addRow("Billing Address:", self.billing_address)
        
        # GST Number
        self.gst_number = QLineEdit()
        self.gst_number.setPlaceholderText("Enter GST number")
        layout.addRow("GST Number:", self.gst_number)
        
        # Contract Terms
        self.contract_terms = QTextEdit()
        self.contract_terms.setMaximumHeight(80)
        self.contract_terms.setPlaceholderText("Enter contract terms and conditions")
        layout.addRow("Contract Terms:", self.contract_terms)
        
        return tab
        
    def create_transport_details_tab(self):
        """Create transportation details tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Pickup Time
        self.pickup_time = QTimeEdit()
        self.pickup_time.setTime(datetime.time(7, 30))
        layout.addRow("Morning Pickup Time:", self.pickup_time)
        
        # Drop Time
        self.drop_time = QTimeEdit()
        self.drop_time.setTime(datetime.time(14, 30))
        layout.addRow("Afternoon Drop Time:", self.drop_time)
        
        # Number of Buses Required
        self.buses_required = QSpinBox()
        self.buses_required.setRange(0, 20)
        self.buses_required.setValue(2)
        layout.addRow("Buses Required:", self.buses_required)
        
        # Special Requirements
        self.special_requirements = QTextEdit()
        self.special_requirements.setMaximumHeight(60)
        self.special_requirements.setPlaceholderText("Any special transportation requirements")
        layout.addRow("Special Requirements:", self.special_requirements)
        
        # Route Description
        self.route_description = QTextEdit()
        self.route_description.setMaximumHeight(80)
        self.route_description.setPlaceholderText("Describe pickup/drop routes")
        layout.addRow("Route Description:", self.route_description)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(60)
        self.notes_input.setPlaceholderText("Additional notes")
        layout.addRow("Notes:", self.notes_input)
        
        return tab
        
    def load_school_data(self, school_data):
        """Load existing school data into form"""
        self.current_school = school_data
        self.form_title.setText(f"Edit School: {school_data['name']}")
        
        # Basic information
        self.name_input.setText(school_data['name'])
        self.code_input.setText(school_data['school_code'])
        self.type_combo.setCurrentText(school_data['type'])
        self.address_input.setPlainText(school_data['address'])
        self.city_input.setCurrentText(school_data['city'])
        self.student_count.setValue(school_data['student_count'])
        
        # Contact information
        self.principal_name.setText(school_data['principal_name'])
        self.school_phone.setText(school_data['phone'])
        self.school_email.setText(school_data['email'])
        self.contact_person.setText(school_data['contact_person'])
        self.contact_phone.setText(school_data['contact_person_phone'])
        
        # Contract & billing
        self.contract_status.setCurrentText(school_data['contract_status'])
        contract_start = QDate.fromString(school_data['contract_start'], 'yyyy-MM-dd')
        self.contract_start.setDate(contract_start)
        contract_end = QDate.fromString(school_data['contract_end'], 'yyyy-MM-dd')
        self.contract_end.setDate(contract_end)
        self.monthly_fee.setValue(school_data['monthly_fee'])
        self.payment_status.setCurrentText(school_data['payment_status'])
        self.billing_address.setPlainText(school_data['billing_address'])
        self.gst_number.setText(school_data['gst_number'])
        
        # Transportation details
        pickup_time = datetime.datetime.strptime(school_data['pickup_time'], '%H:%M').time()
        self.pickup_time.setTime(pickup_time)
        drop_time = datetime.datetime.strptime(school_data['drop_time'], '%H:%M').time()
        self.drop_time.setTime(drop_time)
        self.buses_required.setValue(len(school_data['assigned_buses']))
        
    def clear_form(self):
        """Clear the form"""
        self.current_school = None
        self.form_title.setText("Add New School")
        
        # Clear all fields
        self.name_input.clear()
        self.code_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.address_input.clear()
        self.city_input.setCurrentIndex(0)
        self.student_count.setValue(1000)
        self.establishment_year.setValue(2000)
        
        self.principal_name.clear()
        self.school_phone.clear()
        self.school_email.clear()
        self.contact_person.clear()
        self.contact_phone.clear()
        self.contact_email.clear()
        self.designation.setCurrentIndex(0)
        
        self.contract_status.setCurrentIndex(0)
        self.contract_start.setDate(QDate.currentDate())
        self.contract_end.setDate(QDate.currentDate().addYears(1))
        self.monthly_fee.setValue(100000)
        self.payment_status.setCurrentIndex(0)
        self.billing_address.clear()
        self.gst_number.clear()
        self.contract_terms.clear()
        
        self.pickup_time.setTime(datetime.time(7, 30))
        self.drop_time.setTime(datetime.time(14, 30))
        self.buses_required.setValue(2)
        self.special_requirements.clear()
        self.route_description.clear()
        self.notes_input.clear()
        
        self.status_label.setText("Form cleared")
        
    def save_school(self):
        """Save school data"""
        # Basic validation
        if not self.name_input.text().strip():
            self.status_label.setText("Error: School name is required")
            return
            
        if not self.code_input.text().strip():
            self.status_label.setText("Error: School code is required")
            return
            
        if not self.principal_name.text().strip():
            self.status_label.setText("Error: Principal name is required")
            return
            
        if not self.school_phone.text().strip():
            self.status_label.setText("Error: School phone is required")
            return
            
        # Save logic (in real app, this would save to database)
        if self.current_school:
            action = "updated"
        else:
            action = "added"
            
        QMessageBox.information(self, "Success", 
                              f"School {action} successfully!")
        self.status_label.setText(f"School {action} at {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Switch back to school list
        parent = self.parent().parent().parent()  # Get SchoolManagementPage
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)  # Switch to list tab


class SchoolBusAssignmentTab(QWidget):
    """Tab for assigning buses to schools"""
    
    def __init__(self):
        super().__init__()
        self.current_school = None
        self.init_ui()
        self.load_available_buses()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # School info header
        self.school_info_widget = self.create_school_info_widget()
        layout.addWidget(self.school_info_widget)
        
        # Main content split
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        
        # Left side - Available buses
        available_widget = self.create_available_buses_widget()
        main_layout.addWidget(available_widget, 1)
        
        # Right side - Assigned buses
        assigned_widget = self.create_assigned_buses_widget()
        main_layout.addWidget(assigned_widget, 1)
        
        layout.addWidget(main_widget, 1)
        
        # Assignment history
        history_widget = self.create_history_widget()
        layout.addWidget(history_widget)
        
        # Action buttons
        button_widget = self.create_button_widget()
        layout.addWidget(button_widget)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(self.status_label)
        
    def create_school_info_widget(self):
        """Create widget to display current school information"""
        widget = QGroupBox("Selected School")
        widget.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QGridLayout(widget)
        
        # School info labels
        layout.addWidget(QLabel("School:"), 0, 0)
        self.school_name_label = QLabel("No school selected")
        self.school_name_label.setStyleSheet("font-weight: bold; color: #2980b9;")
        layout.addWidget(self.school_name_label, 0, 1)
        
        layout.addWidget(QLabel("Code:"), 0, 2)
        self.school_code_label = QLabel("-")
        layout.addWidget(self.school_code_label, 0, 3)
        
        layout.addWidget(QLabel("Location:"), 0, 4)
        self.school_location_label = QLabel("-")
        layout.addWidget(self.school_location_label, 0, 5)
        
        layout.addWidget(QLabel("Buses Required:"), 0, 6)
        self.buses_required_label = QLabel("-")
        layout.addWidget(self.buses_required_label, 0, 7)
        
        # Add stretch to last column
        layout.setColumnStretch(8, 1)
        
        return widget
        
    def create_available_buses_widget(self):
        """Create widget to display available buses"""
        widget = QGroupBox("Available Buses")
        widget.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QVBoxLayout(widget)
        
        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by:"))
        
        self.bus_type_filter = QComboBox()
        self.bus_type_filter.addItems(["All Types", "Standard", "Mini", "AC", "Non-AC"])
        self.bus_type_filter.currentTextChanged.connect(self.filter_available_buses)
        filter_layout.addWidget(self.bus_type_filter)
        
        self.capacity_filter = QComboBox()
        self.capacity_filter.addItems(["All Capacities", "12 Seater", "20 Seater", "30 Seater", "40+ Seater"])
        self.capacity_filter.currentTextChanged.connect(self.filter_available_buses)
        filter_layout.addWidget(self.capacity_filter)
        
        filter_layout.addStretch()
        
        self.search_available = QLineEdit()
        self.search_available.setPlaceholderText("Search bus number...")
        self.search_available.textChanged.connect(self.filter_available_buses)
        self.search_available.setFixedWidth(180)
        filter_layout.addWidget(self.search_available)
        
        layout.addLayout(filter_layout)
        
        # Available buses table
        self.available_table = QTableWidget()
        self.available_table.setColumnCount(5)
        self.available_table.setHorizontalHeaderLabels([
            "Bus Number", "Type", "Capacity", "Driver", "Status"
        ])
        self.available_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.available_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.available_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.available_table.itemDoubleClicked.connect(self.assign_selected_bus)
        layout.addWidget(self.available_table)
        
        # Quick assign button
        quick_assign_btn = QPushButton("Assign Selected Bus")
        quick_assign_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        quick_assign_btn.clicked.connect(self.assign_selected_bus)
        layout.addWidget(quick_assign_btn)
        
        return widget
        
    def create_assigned_buses_widget(self):
        """Create widget to display assigned buses"""
        widget = QGroupBox("Assigned Buses")
        widget.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QVBoxLayout(widget)
        
        # Assignment summary
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("Total Assigned:"))
        self.total_assigned_label = QLabel("0")
        self.total_assigned_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        summary_layout.addWidget(self.total_assigned_label)
        
        summary_layout.addWidget(QLabel("Required:"))
        self.required_buses_label = QLabel("0")
        self.required_buses_label.setStyleSheet("font-weight: bold; color: #e67e22;")
        summary_layout.addWidget(self.required_buses_label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Assigned buses table
        self.assigned_table = QTableWidget()
        self.assigned_table.setColumnCount(6)
        self.assigned_table.setHorizontalHeaderLabels([
            "Bus Number", "Type", "Capacity", "Driver", "Assigned Date", "Status"
        ])
        self.assigned_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assigned_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.assigned_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.assigned_table.itemDoubleClicked.connect(self.show_bus_details)
        layout.addWidget(self.assigned_table)
        
        # Action buttons for assigned buses
        button_layout = QHBoxLayout()
        
        self.transfer_btn = QPushButton("Transfer Bus")
        self.transfer_btn.setEnabled(False)
        self.transfer_btn.clicked.connect(self.transfer_bus)
        button_layout.addWidget(self.transfer_btn)
        
        self.remove_btn = QPushButton("Remove Assignment")
        self.remove_btn.setEnabled(False)
        self.remove_btn.clicked.connect(self.remove_assignment)
        button_layout.addWidget(self.remove_btn)
        
        self.view_schedule_btn = QPushButton("View Schedule")
        self.view_schedule_btn.setEnabled(False)
        self.view_schedule_btn.clicked.connect(self.view_bus_schedule)
        button_layout.addWidget(self.view_schedule_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Connect selection changed to enable/disable buttons
        self.assigned_table.itemSelectionChanged.connect(self.on_assigned_selection_changed)
        
        return widget
        
    def create_history_widget(self):
        """Create widget to display assignment history"""
        widget = QGroupBox("Assignment History")
        widget.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QVBoxLayout(widget)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Bus Number", "Action", "Assigned By", "Notes"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setMaximumHeight(150)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.history_table)
        
        # View all button
        view_all_btn = QPushButton("View Full History")
        view_all_btn.clicked.connect(self.view_full_history)
        layout.addWidget(view_all_btn, alignment=Qt.AlignRight)
        
        return widget
        
    def create_button_widget(self):
        """Create action buttons widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Bulk operations
        bulk_label = QLabel("Bulk Operations:")
        layout.addWidget(bulk_label)
        
        self.bulk_action = QComboBox()
        self.bulk_action.addItems(["Assign Multiple Buses", "Transfer All", "Generate Assignment Report", "Optimize Assignments"])
        layout.addWidget(self.bulk_action)
        
        bulk_apply_btn = QPushButton("Apply")
        bulk_apply_btn.clicked.connect(self.apply_bulk_operation)
        layout.addWidget(bulk_apply_btn)
        
        layout.addStretch()
        
        # Individual buttons
        check_conflicts_btn = QPushButton("Check Conflicts")
        check_conflicts_btn.clicked.connect(self.check_conflicts)
        layout.addWidget(check_conflicts_btn)
        
        generate_report_btn = QPushButton("Generate Report")
        generate_report_btn.clicked.connect(self.generate_assignment_report)
        layout.addWidget(generate_report_btn)
        
        return widget
        
    def load_school_data(self, school_data):
        """Load school data for bus assignment"""
        self.current_school = school_data
        
        # Update school info
        self.school_name_label.setText(school_data['name'])
        self.school_code_label.setText(school_data['school_code'])
        self.school_location_label.setText(school_data['city'])
        buses_required = len(school_data.get('assigned_buses', []))
        self.buses_required_label.setText(str(buses_required))
        self.required_buses_label.setText(str(buses_required))
        
        # Load assigned buses for this school
        self.load_assigned_buses(school_data.get('assigned_buses', []))
        
        # Update status
        self.status_label.setText(f"Loaded school: {school_data['name']}")
        
    def load_available_buses(self):
        """Load available buses into the table"""
        # Mock data for available buses
        available_buses = [
            {"number": "BUS-001", "type": "AC", "capacity": 40, "driver": "Rajesh Kumar", "status": "Available"},
            {"number": "BUS-002", "type": "Non-AC", "capacity": 30, "driver": "Suresh Singh", "status": "Available"},
            {"number": "BUS-003", "type": "AC", "capacity": 40, "driver": "Amit Sharma", "status": "Available"},
            {"number": "BUS-004", "type": "Mini", "capacity": 20, "driver": "Vikram Patel", "status": "Maintenance"},
            {"number": "BUS-005", "type": "Standard", "capacity": 30, "driver": "Manoj Yadav", "status": "Available"},
            {"number": "BUS-006", "type": "Non-AC", "capacity": 30, "driver": "Prakash Singh", "status": "Assigned"},
            {"number": "BUS-007", "type": "AC", "capacity": 40, "driver": "Ravi Kumar", "status": "Available"},
            {"number": "BUS-008", "type": "Mini", "capacity": 20, "driver": "Dinesh Gupta", "status": "Available"},
            {"number": "BUS-009", "type": "Standard", "capacity": 30, "driver": "Sanjay Mishra", "status": "Available"},
            {"number": "BUS-010", "type": "AC", "capacity": 40, "driver": "Sunil Verma", "status": "Maintenance"},
        ]
        
        self.available_table.setRowCount(len(available_buses))
        
        for row, bus in enumerate(available_buses):
            self.available_table.setItem(row, 0, QTableWidgetItem(bus["number"]))
            self.available_table.setItem(row, 1, QTableWidgetItem(bus["type"]))
            self.available_table.setItem(row, 2, QTableWidgetItem(str(bus["capacity"])))
            self.available_table.setItem(row, 3, QTableWidgetItem(bus["driver"]))
            
            status_item = QTableWidgetItem(bus["status"])
            if bus["status"] == "Available":
                status_item.setBackground(QColor(220, 255, 220))
                status_item.setForeground(QColor(0, 100, 0))
            elif bus["status"] == "Maintenance":
                status_item.setBackground(QColor(255, 220, 220))
                status_item.setForeground(QColor(139, 0, 0))
            elif bus["status"] == "Assigned":
                status_item.setBackground(QColor(255, 255, 200))
                status_item.setForeground(QColor(153, 102, 0))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.available_table.setItem(row, 4, status_item)
            
    def load_assigned_buses(self, assigned_buses):
        """Load assigned buses for current school"""
        # Mock data for assigned buses
        mock_assignments = []
        for bus_number in assigned_buses:
            # Find bus details from available buses
            for row in range(self.available_table.rowCount()):
                if self.available_table.item(row, 0).text() == bus_number:
                    mock_assignments.append({
                        "number": bus_number,
                        "type": self.available_table.item(row, 1).text(),
                        "capacity": self.available_table.item(row, 2).text(),
                        "driver": self.available_table.item(row, 3).text(),
                        "assigned_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "status": "Active"
                    })
                    break
        
        self.assigned_table.setRowCount(len(mock_assignments))
        
        for row, bus in enumerate(mock_assignments):
            self.assigned_table.setItem(row, 0, QTableWidgetItem(bus["number"]))
            self.assigned_table.setItem(row, 1, QTableWidgetItem(bus["type"]))
            self.assigned_table.setItem(row, 2, QTableWidgetItem(str(bus["capacity"])))
            self.assigned_table.setItem(row, 3, QTableWidgetItem(bus["driver"]))
            self.assigned_table.setItem(row, 4, QTableWidgetItem(bus["assigned_date"]))
            
            status_item = QTableWidgetItem(bus["status"])
            status_item.setBackground(QColor(220, 255, 220))
            status_item.setForeground(QColor(0, 100, 0))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.assigned_table.setItem(row, 5, status_item)
        
        # Update total assigned count
        self.total_assigned_label.setText(str(len(mock_assignments)))
        
        # Load history
        self.load_assignment_history()
        
    def load_assignment_history(self):
        """Load assignment history"""
        history_data = [
            {"date": "2026-01-15 10:30", "bus": "BUS-001", "action": "Assigned", "by": "Admin", "notes": "Initial assignment"},
            {"date": "2026-01-20 14:45", "bus": "BUS-002", "action": "Assigned", "by": "Admin", "notes": "Additional bus"},
            {"date": "2026-02-01 09:15", "bus": "BUS-001", "action": "Transferred", "by": "Manager", "notes": "Temporary transfer"},
            {"date": "2026-02-05 11:20", "bus": "BUS-003", "action": "Assigned", "by": "Admin", "notes": "Replacement"},
        ]
        
        self.history_table.setRowCount(len(history_data))
        
        for row, record in enumerate(history_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(record["date"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(record["bus"]))
            
            action_item = QTableWidgetItem(record["action"])
            if record["action"] == "Assigned":
                action_item.setBackground(QColor(220, 255, 220))
            elif record["action"] == "Transferred":
                action_item.setBackground(QColor(255, 255, 200))
            elif record["action"] == "Removed":
                action_item.setBackground(QColor(255, 220, 220))
            self.history_table.setItem(row, 2, action_item)
            
            self.history_table.setItem(row, 3, QTableWidgetItem(record["by"]))
            self.history_table.setItem(row, 4, QTableWidgetItem(record["notes"]))
            
    def filter_available_buses(self):
        """Filter available buses based on search and filters"""
        search_text = self.search_available.text().lower()
        bus_type = self.bus_type_filter.currentText()
        capacity = self.capacity_filter.currentText()
        
        for row in range(self.available_table.rowCount()):
            show_row = True
            
            # Search filter
            if search_text:
                bus_number = self.available_table.item(row, 0).text().lower()
                driver = self.available_table.item(row, 3).text().lower()
                if search_text not in bus_number and search_text not in driver:
                    show_row = False
            
            # Type filter
            if bus_type != "All Types":
                row_type = self.available_table.item(row, 1).text()
                if row_type != bus_type:
                    show_row = False
            
            # Capacity filter
            if capacity != "All Capacities":
                row_capacity = int(self.available_table.item(row, 2).text())
                if capacity == "12 Seater" and row_capacity != 12:
                    show_row = False
                elif capacity == "20 Seater" and row_capacity != 20:
                    show_row = False
                elif capacity == "30 Seater" and row_capacity != 30:
                    show_row = False
                elif capacity == "40+ Seater" and row_capacity < 40:
                    show_row = False
            
            # Only show available buses
            status = self.available_table.item(row, 4).text()
            if status != "Available":
                show_row = False
                
            self.available_table.setRowHidden(row, not show_row)
            
    def assign_selected_bus(self):
        """Assign selected bus to current school"""
        if not self.current_school:
            QMessageBox.warning(self, "No School", "Please select a school first")
            return
            
        selected_items = self.available_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a bus to assign")
            return
            
        row = selected_items[0].row()
        bus_number = self.available_table.item(row, 0).text()
        bus_type = self.available_table.item(row, 1).text()
        bus_capacity = self.available_table.item(row, 2).text()
        bus_driver = self.available_table.item(row, 3).text()
        
        # Check if already assigned
        for assigned_row in range(self.assigned_table.rowCount()):
            if self.assigned_table.item(assigned_row, 0).text() == bus_number:
                QMessageBox.warning(self, "Already Assigned", 
                                  f"Bus {bus_number} is already assigned to this school")
                return
                
        # Check conflict
        conflict = self.check_bus_conflict(bus_number)
        if conflict:
            reply = QMessageBox.question(self, "Conflict Detected", 
                                       f"Bus {bus_number} is currently assigned to another school. "
                                       "Do you want to transfer it?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
        
        # Add to assigned table
        current_row = self.assigned_table.rowCount()
        self.assigned_table.insertRow(current_row)
        
        self.assigned_table.setItem(current_row, 0, QTableWidgetItem(bus_number))
        self.assigned_table.setItem(current_row, 1, QTableWidgetItem(bus_type))
        self.assigned_table.setItem(current_row, 2, QTableWidgetItem(bus_capacity))
        self.assigned_table.setItem(current_row, 3, QTableWidgetItem(bus_driver))
        self.assigned_table.setItem(current_row, 4, QTableWidgetItem(datetime.datetime.now().strftime("%Y-%m-%d")))
        
        status_item = QTableWidgetItem("Active")
        status_item.setBackground(QColor(220, 255, 220))
        status_item.setForeground(QColor(0, 100, 0))
        status_item.setTextAlignment(Qt.AlignCenter)
        self.assigned_table.setItem(current_row, 5, status_item)
        
        # Update bus status in available table
        status_item = QTableWidgetItem("Assigned")
        status_item.setBackground(QColor(255, 255, 200))
        status_item.setForeground(QColor(153, 102, 0))
        status_item.setTextAlignment(Qt.AlignCenter)
        self.available_table.setItem(row, 4, status_item)
        
        # Update counts
        self.total_assigned_label.setText(str(self.assigned_table.rowCount()))
        
        # Add to history
        self.add_to_history(bus_number, "Assigned", "Manual assignment")
        
        QMessageBox.information(self, "Success", f"Bus {bus_number} assigned successfully")
        self.status_label.setText(f"Bus {bus_number} assigned at {datetime.datetime.now().strftime('%H:%M:%S')}")
        
    def transfer_bus(self):
        """Transfer selected bus to another school"""
        selected_items = self.assigned_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a bus to transfer")
            return
            
        row = selected_items[0].row()
        bus_number = self.assigned_table.item(row, 0).text()
        
        # In a real app, this would open a dialog to select target school
        QMessageBox.information(self, "Transfer Bus", 
                              f"Transfer functionality for bus {bus_number} would open a school selection dialog.\n\n"
                              "This is a demo - in the real application, you would select the target school from a list.")
        
        self.add_to_history(bus_number, "Transferred", "Transferred to another school (demo)")
        
    def remove_assignment(self):
        """Remove bus assignment"""
        selected_items = self.assigned_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a bus to remove")
            return
            
        row = selected_items[0].row()
        bus_number = self.assigned_table.item(row, 0).text()
        
        reply = QMessageBox.question(self, "Confirm Removal", 
                                   f"Remove bus {bus_number} from this school?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Remove from assigned table
            self.assigned_table.removeRow(row)
            
            # Update bus status in available table
            for avail_row in range(self.available_table.rowCount()):
                if self.available_table.item(avail_row, 0).text() == bus_number:
                    status_item = QTableWidgetItem("Available")
                    status_item.setBackground(QColor(220, 255, 220))
                    status_item.setForeground(QColor(0, 100, 0))
                    status_item.setTextAlignment(Qt.AlignCenter)
                    self.available_table.setItem(avail_row, 4, status_item)
                    break
            
            # Update counts
            self.total_assigned_label.setText(str(self.assigned_table.rowCount()))
            
            # Add to history
            self.add_to_history(bus_number, "Removed", "Assignment removed")
            
            QMessageBox.information(self, "Success", f"Bus {bus_number} removed from assignment")
            
    def check_bus_conflict(self, bus_number):
        """Check if bus is already assigned to another school"""
        # In a real app, this would query the database
        # Mock conflict detection
        conflict_buses = ["BUS-003", "BUS-006"]  # Example buses already assigned elsewhere
        return bus_number in conflict_buses
        
    def check_conflicts(self):
        """Check for assignment conflicts"""
        conflicts = []
        
        # Check each assigned bus for conflicts
        for row in range(self.assigned_table.rowCount()):
            bus_number = self.assigned_table.item(row, 0).text()
            if self.check_bus_conflict(bus_number):
                conflicts.append(bus_number)
        
        if conflicts:
            conflict_list = ", ".join(conflicts)
            QMessageBox.warning(self, "Conflicts Detected", 
                              f"The following buses have scheduling conflicts: {conflict_list}")
            
            # Highlight conflicting rows
            for row in range(self.assigned_table.rowCount()):
                bus_number = self.assigned_table.item(row, 0).text()
                if bus_number in conflicts:
                    for col in range(self.assigned_table.columnCount()):
                        item = self.assigned_table.item(row, col)
                        if item:
                            item.setBackground(QColor(255, 200, 200))
        else:
            QMessageBox.information(self, "No Conflicts", "No scheduling conflicts detected")
            
    def show_bus_details(self):
        """Show detailed information about selected bus"""
        selected_items = self.assigned_table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        bus_number = self.assigned_table.item(row, 0).text()
        
        # In a real app, this would open a detailed bus information dialog
        QMessageBox.information(self, "Bus Details", 
                              f"Bus Number: {bus_number}\n"
                              f"Type: {self.assigned_table.item(row, 1).text()}\n"
                              f"Capacity: {self.assigned_table.item(row, 2).text()}\n"
                              f"Driver: {self.assigned_table.item(row, 3).text()}\n"
                              f"Assigned Date: {self.assigned_table.item(row, 4).text()}\n"
                              f"Status: {self.assigned_table.item(row, 5).text()}\n\n"
                              "This is a demo - full bus details would be shown here.")
                              
    def view_bus_schedule(self):
        """View schedule for selected bus"""
        selected_items = self.assigned_table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        bus_number = self.assigned_table.item(row, 0).text()
        
        QMessageBox.information(self, "Bus Schedule", 
                              f"Schedule for bus {bus_number} would be displayed here.\n\n"
                              "This is a demo - the full schedule view would include:\n"
                              "• Morning pickup times\n"
                              "• Afternoon drop times\n"
                              "• Route details\n"
                              "• Driver duty hours\n"
                              "• Maintenance schedule")
                              
    def on_assigned_selection_changed(self):
        """Enable/disable buttons based on selection"""
        has_selection = len(self.assigned_table.selectedItems()) > 0
        self.transfer_btn.setEnabled(has_selection)
        self.remove_btn.setEnabled(has_selection)
        self.view_schedule_btn.setEnabled(has_selection)
        
    def add_to_history(self, bus_number, action, notes=""):
        """Add an entry to assignment history"""
        current_row = self.history_table.rowCount()
        self.history_table.insertRow(0)  # Insert at top
        
        self.history_table.setItem(0, 0, QTableWidgetItem(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.history_table.setItem(0, 1, QTableWidgetItem(bus_number))
        
        action_item = QTableWidgetItem(action)
        if action == "Assigned":
            action_item.setBackground(QColor(220, 255, 220))
        elif action == "Transferred":
            action_item.setBackground(QColor(255, 255, 200))
        elif action == "Removed":
            action_item.setBackground(QColor(255, 220, 220))
        self.history_table.setItem(0, 2, action_item)
        
        self.history_table.setItem(0, 3, QTableWidgetItem("Admin"))  # Current user
        self.history_table.setItem(0, 4, QTableWidgetItem(notes))
        
    def view_full_history(self):
        """View complete assignment history"""
        QMessageBox.information(self, "Full History", 
                              "Complete assignment history would be shown in a separate dialog.\n\n"
                              "This would include:\n"
                              "• All assignments (current and past)\n"
                              "• Transfer history\n"
                              "• Driver changes\n"
                              "• Maintenance records\n"
                              "• Billing history")
                              
    def apply_bulk_operation(self):
        """Apply bulk operation"""
        operation = self.bulk_action.currentText()
        
        if operation == "Assign Multiple Buses":
            QMessageBox.information(self, "Bulk Assign", 
                                  "Multiple bus selection dialog would open here.\n\n"
                                  "You could select multiple buses and assign them at once.")
        elif operation == "Transfer All":
            reply = QMessageBox.question(self, "Transfer All", 
                                       "Transfer all assigned buses to another school?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Transfer All", 
                                      "All buses transferred (demo mode)")
        elif operation == "Generate Assignment Report":
            self.generate_assignment_report()
        elif operation == "Optimize Assignments":
            QMessageBox.information(self, "Optimize Assignments", 
                                  "Assignment optimization would:\n"
                                  "• Balance bus loads\n"
                                  "• Minimize travel time\n"
                                  "• Reduce fuel costs\n"
                                  "• Suggest optimal routes")
                                  
    def generate_assignment_report(self):
        """Generate assignment report"""
        QMessageBox.information(self, "Generate Report", 
                              "Assignment report generated successfully!\n\n"
                              "Report includes:\n"
                              f"• School: {self.school_name_label.text()}\n"
                              f"• Total Buses Assigned: {self.total_assigned_label.text()}\n"
                              f"• Buses Required: {self.required_buses_label.text()}\n"
                              "• Assignment History\n"
                              "• Driver Details\n\n"
                              "Report saved as PDF (demo mode)")
        self.status_label.setText("Report generated at " + datetime.datetime.now().strftime("%H:%M:%S"))