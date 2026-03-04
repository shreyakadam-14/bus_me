from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QFrame, QGroupBox,
    QTabWidget, QTextEdit, QHeaderView, QMessageBox,
    QCheckBox, QFileDialog, QStackedWidget, QListWidget,
    QListWidgetItem, QFormLayout, QDialog, QGridLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate
import datetime

# Mock data for buses
MOCK_BUSES = [
    {
        'id': 1,
        'registration_number': 'MH-01-AB-1234',
        'bus_number': 'BUS-001',
        'model': 'Tata Starbus',
        'capacity': 40,
        'year': 2020,
        'color': 'White',
        'status': 'Active',
        'policy_number': 'INS-2023-001',
        'provider': 'ICICI Lombard',
        'coverage_amount': 5000000,
        'premium_amount': 75000,
        'start_date': '2023-01-15',
        'expiry_date': '2024-01-14',
        'insurance_status': 'Active',
        'days_remaining': 45
    },
    {
        'id': 2,
        'registration_number': 'MH-01-CD-5678',
        'bus_number': 'BUS-002',
        'model': 'Ashok Leyland',
        'capacity': 45,
        'year': 2019,
        'color': 'Blue',
        'status': 'Active',
        'policy_number': 'INS-2023-002',
        'provider': 'New India Assurance',
        'coverage_amount': 4500000,
        'premium_amount': 68000,
        'start_date': '2023-03-10',
        'expiry_date': '2024-03-09',
        'insurance_status': 'Expiring Soon',
        'days_remaining': 10
    },
    {
        'id': 3,
        'registration_number': 'MH-01-EF-9012',
        'bus_number': 'BUS-003',
        'model': 'Volvo B7R',
        'capacity': 50,
        'year': 2021,
        'color': 'Red',
        'status': 'Maintenance',
        'policy_number': 'INS-2022-015',
        'provider': 'Bajaj Allianz',
        'coverage_amount': 6000000,
        'premium_amount': 85000,
        'start_date': '2022-06-20',
        'expiry_date': '2023-06-19',
        'insurance_status': 'Expired',
        'days_remaining': -200
    },
    {
        'id': 4,
        'registration_number': 'MH-01-GH-3456',
        'bus_number': 'BUS-004',
        'model': 'Force Traveller',
        'capacity': 26,
        'year': 2022,
        'color': 'Yellow',
        'status': 'Active',
        'policy_number': 'INS-2023-045',
        'provider': 'HDFC Ergo',
        'coverage_amount': 3500000,
        'premium_amount': 52000,
        'start_date': '2023-11-01',
        'expiry_date': '2024-10-31',
        'insurance_status': 'Active',
        'days_remaining': 280
    }
]


class BusManagementPage(QWidget):
    """
    Main Bus Management Page - To be integrated into the main application
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
        header_label = QLabel("Bus Management")
        header_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(header_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Create tab widget for different bus management sections
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.bus_list_tab = BusListTab()
        self.bus_form_tab = BusFormTab()
        self.insurance_tracker_tab = InsuranceTrackerTab()
        self.insurance_renewal_tab = InsuranceRenewalTab()
        
        # Add tabs
        self.tab_widget.addTab(self.bus_list_tab, "Bus List")
        self.tab_widget.addTab(self.bus_form_tab, "Add/Edit Bus")
        self.tab_widget.addTab(self.insurance_tracker_tab, "Insurance Tracker")
        self.tab_widget.addTab(self.insurance_renewal_tab, "Renew Insurance")
        
        main_layout.addWidget(self.tab_widget)
        
        # Add status label at bottom
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #7f8c8d;")
        main_layout.addWidget(self.status_label)


class BusListTab(QWidget):
    """Tab for listing and managing buses"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_buses()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Search and filter section
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search buses...")
        self.search_input.setFixedWidth(250)
        filter_layout.addWidget(self.search_input)
        
        # Status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Inactive", "Maintenance"])
        self.status_filter.setFixedWidth(120)
        filter_layout.addWidget(self.status_filter)
        
        # Insurance filter
        filter_layout.addWidget(QLabel("Insurance:"))
        self.insurance_filter = QComboBox()
        self.insurance_filter.addItems(["All", "Active", "Expiring Soon", "Expired"])
        self.insurance_filter.setFixedWidth(120)
        filter_layout.addWidget(self.insurance_filter)
        
        # Apply filter button
        filter_btn = QPushButton("Apply Filters")
        filter_btn.clicked.connect(self.apply_filters)
        filter_layout.addWidget(filter_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_filters)
        filter_layout.addWidget(clear_btn)
        
        filter_layout.addStretch()
        
        # Export buttons
        export_excel_btn = QPushButton("Export to Excel")
        export_excel_btn.clicked.connect(self.export_to_excel)
        filter_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("Export to PDF")
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        filter_layout.addWidget(export_pdf_btn)
        
        layout.addWidget(filter_widget)
        
        # Bus table
        self.bus_table = QTableWidget()
        self.bus_table.setColumnCount(10)
        self.bus_table.setHorizontalHeaderLabels([
            "Registration", "Bus No.", "Model", "Capacity", 
            "Year", "Status", "Policy No.", "Provider", "Expiry Date", "Ins. Status"
        ])
        self.bus_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bus_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.bus_table)
        
        # Action buttons section
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        
        # Bulk operations
        bulk_label = QLabel("Bulk Operations:")
        action_layout.addWidget(bulk_label)
        
        self.bulk_action = QComboBox()
        self.bulk_action.addItems(["Update Status", "Export Selected", "Print Details"])
        action_layout.addWidget(self.bulk_action)
        
        bulk_apply_btn = QPushButton("Apply")
        bulk_apply_btn.clicked.connect(self.apply_bulk_operation)
        action_layout.addWidget(bulk_apply_btn)
        
        action_layout.addStretch()
        
        # Individual action buttons
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit Bus")
        edit_btn.clicked.connect(self.edit_bus)
        action_layout.addWidget(edit_btn)
        
        renew_btn = QPushButton("Renew Insurance")
        renew_btn.clicked.connect(self.renew_insurance)
        action_layout.addWidget(renew_btn)
        
        delete_btn = QPushButton("Delete Bus")
        delete_btn.clicked.connect(self.delete_bus)
        action_layout.addWidget(delete_btn)
        
        layout.addWidget(action_widget)
        
    def load_buses(self):
        """Load buses into the table"""
        self.bus_table.setRowCount(len(MOCK_BUSES))
        
        for row, bus in enumerate(MOCK_BUSES):
            # Registration
            item = QTableWidgetItem(bus['registration_number'])
            self.bus_table.setItem(row, 0, item)
            
            # Bus Number
            item = QTableWidgetItem(bus['bus_number'])
            self.bus_table.setItem(row, 1, item)
            
            # Model
            item = QTableWidgetItem(bus['model'])
            self.bus_table.setItem(row, 2, item)
            
            # Capacity
            item = QTableWidgetItem(str(bus['capacity']))
            item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 3, item)
            
            # Year
            item = QTableWidgetItem(str(bus['year']))
            item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 4, item)
            
            # Status with color coding
            status_item = QTableWidgetItem(bus['status'])
            if bus['status'] == 'Active':
                status_item.setBackground(QColor(220, 255, 220))
                status_item.setForeground(QColor(0, 100, 0))
            elif bus['status'] == 'Maintenance':
                status_item.setBackground(QColor(255, 255, 200))
                status_item.setForeground(QColor(153, 102, 0))
            else:
                status_item.setBackground(QColor(255, 220, 220))
                status_item.setForeground(QColor(139, 0, 0))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 5, status_item)
            
            # Policy Number
            item = QTableWidgetItem(bus['policy_number'])
            self.bus_table.setItem(row, 6, item)
            
            # Provider
            item = QTableWidgetItem(bus['provider'])
            self.bus_table.setItem(row, 7, item)
            
            # Expiry Date
            item = QTableWidgetItem(bus['expiry_date'])
            self.bus_table.setItem(row, 8, item)
            
            # Insurance Status with color coding
            ins_item = QTableWidgetItem(bus['insurance_status'])
            if bus['insurance_status'] == 'Active':
                ins_item.setBackground(QColor(220, 255, 220))
                ins_item.setForeground(QColor(0, 100, 0))
            elif bus['insurance_status'] == 'Expiring Soon':
                ins_item.setBackground(QColor(255, 255, 200))
                ins_item.setForeground(QColor(153, 102, 0))
            else:
                ins_item.setBackground(QColor(255, 220, 220))
                ins_item.setForeground(QColor(139, 0, 0))
            ins_item.setTextAlignment(Qt.AlignCenter)
            self.bus_table.setItem(row, 9, ins_item)
            
    def apply_filters(self):
        """Apply filters to the table"""
        QMessageBox.information(self, "Filters Applied", 
                              "Filters have been applied (demo mode)")
        
    def clear_filters(self):
        """Clear all filters"""
        self.search_input.clear()
        self.status_filter.setCurrentIndex(0)
        self.insurance_filter.setCurrentIndex(0)
        
    def get_selected_bus(self):
        """Get the currently selected bus"""
        selected_items = self.bus_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return MOCK_BUSES[row] if row < len(MOCK_BUSES) else None
        return None
        
    def view_details(self):
        """View details of selected bus"""
        bus = self.get_selected_bus()
        if bus:
            dialog = BusDetailsDialog(bus)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a bus first")
            
    def edit_bus(self):
        """Edit selected bus"""
        bus = self.get_selected_bus()
        if bus:
            # Switch to bus form tab with edit mode
            parent = self.parent().parent().parent()  # Get BusManagementPage
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(1)  # Switch to form tab
                parent.bus_form_tab.load_bus_data(bus)
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a bus first")
            
    def renew_insurance(self):
        """Renew insurance for selected bus"""
        bus = self.get_selected_bus()
        if bus:
            # Switch to insurance renewal tab
            parent = self.parent().parent().parent()  # Get BusManagementPage
            if hasattr(parent, 'tab_widget'):
                parent.tab_widget.setCurrentIndex(3)  # Switch to renewal tab
                parent.insurance_renewal_tab.load_bus_data(bus)
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a bus first")
            
    def delete_bus(self):
        """Delete selected bus"""
        bus = self.get_selected_bus()
        if bus:
            reply = QMessageBox.question(self, "Confirm Delete",
                                       f"Delete bus {bus['registration_number']}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Success", 
                                      f"Bus {bus['registration_number']} deleted (demo mode)")
        else:
            QMessageBox.warning(self, "No Selection", 
                              "Please select a bus first")
            
    def apply_bulk_operation(self):
        """Apply bulk operation"""
        operation = self.bulk_action.currentText()
        QMessageBox.information(self, "Bulk Operation", 
                              f"{operation} applied to selected buses (demo mode)")
        
    def export_to_excel(self):
        """Export to Excel"""
        QMessageBox.information(self, "Export", 
                              "Data exported to Excel (demo mode)")
        
    def export_to_pdf(self):
        """Export to PDF"""
        QMessageBox.information(self, "Export", 
                              "Data exported to PDF (demo mode)")


class BusFormTab(QWidget):
    """Tab for adding/editing bus details"""
    
    def __init__(self):
        super().__init__()
        self.current_bus = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form title
        self.form_title = QLabel("Add New Bus")
        self.form_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Create tab widget for form sections
        form_tabs = QTabWidget()
        
        # Basic Information Tab
        basic_tab = self.create_basic_info_tab()
        form_tabs.addTab(basic_tab, "Basic Information")
        
        # Insurance Information Tab
        insurance_tab = self.create_insurance_tab()
        form_tabs.addTab(insurance_tab, "Insurance Information")
        
        layout.addWidget(form_tabs)
        
        # Form buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Bus")
        self.save_btn.clicked.connect(self.save_bus)
        button_layout.addWidget(self.save_btn)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.status_label)
        
    def create_basic_info_tab(self):
        """Create basic information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Registration Number
        self.reg_number = QLineEdit()
        self.reg_number.setPlaceholderText("e.g., MH-01-AB-1234")
        layout.addRow("Registration Number*:", self.reg_number)
        
        # Bus Number
        self.bus_number = QLineEdit()
        self.bus_number.setPlaceholderText("e.g., BUS-001")
        layout.addRow("Bus Number:", self.bus_number)
        
        # Model
        self.model = QLineEdit()
        self.model.setPlaceholderText("e.g., Tata Starbus")
        layout.addRow("Model:", self.model)
        
        # Capacity and Year in one row
        capacity_year_widget = QWidget()
        capacity_year_layout = QHBoxLayout(capacity_year_widget)
        capacity_year_layout.setContentsMargins(0, 0, 0, 0)
        
        self.capacity = QSpinBox()
        self.capacity.setRange(1, 100)
        self.capacity.setValue(40)
        capacity_year_layout.addWidget(QLabel("Capacity:"))
        capacity_year_layout.addWidget(self.capacity)
        
        self.year = QSpinBox()
        self.year.setRange(2000, 2024)
        self.year.setValue(2020)
        capacity_year_layout.addWidget(QLabel("Year:"))
        capacity_year_layout.addWidget(self.year)
        
        layout.addRow("", capacity_year_widget)
        
        # Color
        self.color = QComboBox()
        self.color.setEditable(True)
        self.color.addItems(["White", "Blue", "Red", "Yellow", "Green", "Black", "Silver"])
        layout.addRow("Color:", self.color)
        
        # Status
        self.status = QComboBox()
        self.status.addItems(["Active", "Inactive", "Maintenance"])
        layout.addRow("Status:", self.status)
        
        return tab
        
    def create_insurance_tab(self):
        """Create insurance information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Policy Number
        self.policy_number = QLineEdit()
        self.policy_number.setPlaceholderText("e.g., INS-2024-001")
        layout.addRow("Policy Number:", self.policy_number)
        
        # Provider
        self.provider = QComboBox()
        self.provider.setEditable(True)
        self.provider.addItems([
            "ICICI Lombard", "New India Assurance", "Bajaj Allianz",
            "HDFC Ergo", "Tata AIG", "Reliance General", "Other"
        ])
        layout.addRow("Provider:", self.provider)
        
        # Coverage Amount
        self.coverage = QDoubleSpinBox()
        self.coverage.setRange(0, 10000000)
        self.coverage.setPrefix("₹ ")
        self.coverage.setValue(5000000)
        layout.addRow("Coverage Amount:", self.coverage)
        
        # Premium Amount
        self.premium = QDoubleSpinBox()
        self.premium.setRange(0, 500000)
        self.premium.setPrefix("₹ ")
        self.premium.setValue(75000)
        layout.addRow("Premium Amount:", self.premium)
        
        # Dates
        dates_widget = QWidget()
        dates_layout = QHBoxLayout(dates_widget)
        dates_layout.setContentsMargins(0, 0, 0, 0)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        dates_layout.addWidget(QLabel("Start Date:"))
        dates_layout.addWidget(self.start_date)
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addYears(1))
        dates_layout.addWidget(QLabel("Expiry Date:"))
        dates_layout.addWidget(self.expiry_date)
        
        layout.addRow("", dates_widget)
        
        # Document upload
        doc_widget = QWidget()
        doc_layout = QHBoxLayout(doc_widget)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        
        self.doc_path = QLineEdit()
        self.doc_path.setReadOnly(True)
        self.doc_path.setPlaceholderText("No file selected")
        doc_layout.addWidget(self.doc_path)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_document)
        doc_layout.addWidget(browse_btn)
        
        layout.addRow("Insurance Document:", doc_widget)
        
        return tab
        
    def load_bus_data(self, bus_data):
        """Load existing bus data into form"""
        self.current_bus = bus_data
        self.form_title.setText(f"Edit Bus: {bus_data['registration_number']}")
        
        # Basic information
        self.reg_number.setText(bus_data['registration_number'])
        self.bus_number.setText(bus_data['bus_number'])
        self.model.setText(bus_data['model'])
        self.capacity.setValue(bus_data['capacity'])
        self.year.setValue(bus_data['year'])
        self.color.setCurrentText(bus_data['color'])
        self.status.setCurrentText(bus_data['status'])
        
        # Insurance information
        self.policy_number.setText(bus_data['policy_number'])
        self.provider.setCurrentText(bus_data['provider'])
        self.coverage.setValue(bus_data['coverage_amount'])
        self.premium.setValue(bus_data['premium_amount'])
        
        start_date = QDate.fromString(bus_data['start_date'], 'yyyy-MM-dd')
        expiry_date = QDate.fromString(bus_data['expiry_date'], 'yyyy-MM-dd')
        self.start_date.setDate(start_date)
        self.expiry_date.setDate(expiry_date)
        
    def browse_document(self):
        """Browse for insurance document"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Insurance Document", "",
            "PDF Files (*.pdf);;Image Files (*.png *.jpg);;All Files (*)"
        )
        if file_path:
            self.doc_path.setText(file_path)
            
    def clear_form(self):
        """Clear the form"""
        self.current_bus = None
        self.form_title.setText("Add New Bus")
        
        # Clear all fields
        self.reg_number.clear()
        self.bus_number.clear()
        self.model.clear()
        self.capacity.setValue(40)
        self.year.setValue(2020)
        self.color.setCurrentIndex(0)
        self.status.setCurrentIndex(0)
        
        self.policy_number.clear()
        self.provider.setCurrentIndex(0)
        self.coverage.setValue(5000000)
        self.premium.setValue(75000)
        self.start_date.setDate(QDate.currentDate())
        self.expiry_date.setDate(QDate.currentDate().addYears(1))
        self.doc_path.clear()
        
        self.status_label.setText("Form cleared")
        
    def save_bus(self):
        """Save bus data"""
        # Basic validation
        if not self.reg_number.text().strip():
            self.status_label.setText("Error: Registration number is required")
            return
            
        if self.start_date.date() >= self.expiry_date.date():
            self.status_label.setText("Error: Expiry date must be after start date")
            return
            
        # Save logic (in real app, this would save to database)
        if self.current_bus:
            action = "updated"
        else:
            action = "added"
            
        QMessageBox.information(self, "Success", 
                              f"Bus {action} successfully!")
        self.status_label.setText(f"Bus {action} at {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Switch back to bus list
        parent = self.parent().parent().parent()  # Get BusManagementPage
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)  # Switch to list tab


class InsuranceTrackerTab(QWidget):
    """Tab for tracking insurance status"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Statistics cards
        stats_widget = self.create_stats_cards()
        layout.addWidget(stats_widget)
        
        # Filter controls
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        filter_layout.addWidget(QLabel("Filter by Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Active", "Expiring Soon (30 days)", "Expired"])
        self.status_filter.currentTextChanged.connect(self.filter_table)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addWidget(QLabel("Expiry Range:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())
        filter_layout.addWidget(self.date_from)
        
        filter_layout.addWidget(QLabel("to"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate().addMonths(6))
        filter_layout.addWidget(self.date_to)
        
        apply_date_btn = QPushButton("Apply Date Filter")
        apply_date_btn.clicked.connect(self.filter_by_date)
        filter_layout.addWidget(apply_date_btn)
        
        filter_layout.addStretch()
        
        # Bulk renew button
        bulk_renew_btn = QPushButton("Bulk Renew Selected")
        bulk_renew_btn.clicked.connect(self.bulk_renew)
        filter_layout.addWidget(bulk_renew_btn)
        
        layout.addWidget(filter_widget)
        
        # Insurance table
        self.insurance_table = QTableWidget()
        self.insurance_table.setColumnCount(9)
        self.insurance_table.setHorizontalHeaderLabels([
            "Select", "Bus Registration", "Policy Number", "Provider",
            "Coverage Amount", "Premium", "Start Date", "Expiry Date", "Days Remaining"
        ])
        self.insurance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Load data
        self.load_insurance_data()
        layout.addWidget(self.insurance_table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        report_btn = QPushButton("Generate Insurance Report")
        report_btn.clicked.connect(self.generate_report)
        action_layout.addWidget(report_btn)
        
        calendar_btn = QPushButton("Calendar View")
        calendar_btn.clicked.connect(self.show_calendar_view)
        action_layout.addWidget(calendar_btn)
        
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self.export_data)
        action_layout.addWidget(export_btn)
        
        layout.addLayout(action_layout)
        
    def create_stats_cards(self):
        """Create statistics cards"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Calculate stats
        total = len(MOCK_BUSES)
        active = len([b for b in MOCK_BUSES if b['insurance_status'] == 'Active'])
        expiring = len([b for b in MOCK_BUSES if b['insurance_status'] == 'Expiring Soon'])
        expired = len([b for b in MOCK_BUSES if b['insurance_status'] == 'Expired'])
        
        # Create stat cards
        cards = [
            ("Total Insured", total, QColor(52, 152, 219)),
            ("Active", active, QColor(46, 204, 113)),
            ("Expiring Soon", expiring, QColor(241, 196, 15)),
            ("Expired", expired, QColor(231, 76, 60))
        ]
        
        for title, value, color in cards:
            card = self.create_stat_card(title, value, color)
            layout.addWidget(card)
        
        return widget
        
    def create_stat_card(self, title, value, color):
        """Create a single stat card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        card.setFixedWidth(180)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()});")
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
        
    def load_insurance_data(self):
        """Load insurance data into table"""
        self.insurance_table.setRowCount(len(MOCK_BUSES))
        
        for row, bus in enumerate(MOCK_BUSES):
            # Checkbox for selection
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            self.insurance_table.setCellWidget(row, 0, checkbox_widget)
            
            # Bus Registration
            item = QTableWidgetItem(bus['registration_number'])
            self.insurance_table.setItem(row, 1, item)
            
            # Policy Number
            item = QTableWidgetItem(bus['policy_number'])
            self.insurance_table.setItem(row, 2, item)
            
            # Provider
            item = QTableWidgetItem(bus['provider'])
            self.insurance_table.setItem(row, 3, item)
            
            # Coverage Amount
            item = QTableWidgetItem(f"₹ {bus['coverage_amount']:,}")
            self.insurance_table.setItem(row, 4, item)
            
            # Premium
            item = QTableWidgetItem(f"₹ {bus['premium_amount']:,}")
            self.insurance_table.setItem(row, 5, item)
            
            # Start Date
            item = QTableWidgetItem(bus['start_date'])
            self.insurance_table.setItem(row, 6, item)
            
            # Expiry Date
            item = QTableWidgetItem(bus['expiry_date'])
            self.insurance_table.setItem(row, 7, item)
            
            # Days Remaining with color coding
            days = bus['days_remaining']
            days_item = QTableWidgetItem(str(days))
            
            if days < 0:
                days_item.setText("Expired")
                days_item.setBackground(QColor(255, 220, 220))
                days_item.setForeground(QColor(139, 0, 0))
            elif days <= 30:
                days_item.setText(f"{days} days")
                days_item.setBackground(QColor(255, 255, 200))
                days_item.setForeground(QColor(153, 102, 0))
            else:
                days_item.setText(f"{days} days")
                days_item.setBackground(QColor(220, 255, 220))
                days_item.setForeground(QColor(0, 100, 0))
            
            days_item.setTextAlignment(Qt.AlignCenter)
            self.insurance_table.setItem(row, 8, days_item)
            
    def filter_table(self):
        """Filter table by status"""
        QMessageBox.information(self, "Filter Applied", 
                              f"Showing {self.status_filter.currentText()} policies")
        
    def filter_by_date(self):
        """Filter by date range"""
        from_date = self.date_from.date().toString("yyyy-MM-dd")
        to_date = self.date_to.date().toString("yyyy-MM-dd")
        QMessageBox.information(self, "Date Filter", 
                              f"Showing policies expiring between {from_date} and {to_date}")
        
    def bulk_renew(self):
        """Bulk renew selected policies"""
        QMessageBox.information(self, "Bulk Renew", 
                              "Selected policies will be renewed (demo mode)")
        
    def generate_report(self):
        """Generate insurance report"""
        QMessageBox.information(self, "Report", 
                              "Insurance report generated (demo mode)")
        
    def show_calendar_view(self):
        """Show calendar view"""
        QMessageBox.information(self, "Calendar View", 
                              "Calendar view would show here (demo mode)")
        
    def export_data(self):
        """Export data"""
        QMessageBox.information(self, "Export", 
                              "Data exported (demo mode)")


class InsuranceRenewalTab(QWidget):
    """Tab for renewing insurance"""
    
    def __init__(self):
        super().__init__()
        self.current_bus = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.renewal_title = QLabel("Renew Insurance")
        self.renewal_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(self.renewal_title)
        
        # Bus selection (if not loaded from list)
        select_widget = QWidget()
        select_layout = QHBoxLayout(select_widget)
        
        select_layout.addWidget(QLabel("Select Bus:"))
        self.bus_combo = QComboBox()
        for bus in MOCK_BUSES:
            self.bus_combo.addItem(f"{bus['registration_number']} - {bus['bus_number']}", bus)
        self.bus_combo.currentIndexChanged.connect(self.bus_selected)
        select_layout.addWidget(self.bus_combo)
        
        layout.addWidget(select_widget)
        
        # Create two-column layout
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        
        # Left column - Previous insurance
        left_column = QGroupBox("Previous Insurance Details")
        left_layout = QFormLayout(left_column)
        
        self.prev_policy = QLineEdit()
        self.prev_policy.setReadOnly(True)
        left_layout.addRow("Policy Number:", self.prev_policy)
        
        self.prev_provider = QLineEdit()
        self.prev_provider.setReadOnly(True)
        left_layout.addRow("Provider:", self.prev_provider)
        
        self.prev_coverage = QLineEdit()
        self.prev_coverage.setReadOnly(True)
        left_layout.addRow("Coverage Amount:", self.prev_coverage)
        
        self.prev_expiry = QLineEdit()
        self.prev_expiry.setReadOnly(True)
        left_layout.addRow("Expiry Date:", self.prev_expiry)
        
        columns_layout.addWidget(left_column)
        
        # Right column - New insurance
        right_column = QGroupBox("New Insurance Details")
        right_layout = QFormLayout(right_column)
        
        self.new_policy = QLineEdit()
        self.new_policy.setPlaceholderText("Enter new policy number")
        right_layout.addRow("New Policy Number*:", self.new_policy)
        
        self.new_provider = QComboBox()
        self.new_provider.setEditable(True)
        self.new_provider.addItems(["ABC Insurance Co.", "XYZ Insurance Ltd.", 
                                   "PQR Insurance Corp.", "Other"])
        right_layout.addRow("Provider:", self.new_provider)
        
        self.new_coverage = QDoubleSpinBox()
        self.new_coverage.setRange(0, 1000000)
        self.new_coverage.setPrefix("₹ ")
        right_layout.addRow("Coverage Amount:", self.new_coverage)
        
        self.new_premium = QDoubleSpinBox()
        self.new_premium.setRange(0, 100000)
        self.new_premium.setPrefix("₹ ")
        right_layout.addRow("Premium Amount*:", self.new_premium)
        
        # Dates
        dates_widget = QWidget()
        dates_layout = QHBoxLayout(dates_widget)
        dates_layout.setContentsMargins(0, 0, 0, 0)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        dates_layout.addWidget(QLabel("Start Date:"))
        dates_layout.addWidget(self.start_date)
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addYears(1))
        dates_layout.addWidget(QLabel("Expiry Date:"))
        dates_layout.addWidget(self.expiry_date)
        
        right_layout.addRow("", dates_widget)
        
        columns_layout.addWidget(right_column)
        
        layout.addWidget(columns_widget)
        
        # Payment information
        payment_group = QGroupBox("Payment Information")
        payment_layout = QFormLayout(payment_group)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Bank Transfer", "Cash", "Cheque", "Credit Card", "Online Payment"])
        payment_layout.addRow("Payment Method:", self.payment_method)
        
        self.receipt_number = QLineEdit()
        self.receipt_number.setPlaceholderText("Receipt/Transaction number")
        payment_layout.addRow("Receipt Number:", self.receipt_number)
        
        layout.addWidget(payment_group)
        
        # Renew button
        renew_btn = QPushButton("Renew Insurance")
        renew_btn.clicked.connect(self.process_renewal)
        layout.addWidget(renew_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.status_label)
        
        # Load first bus by default
        if MOCK_BUSES:
            self.load_bus_data(MOCK_BUSES[0])
            
    def load_bus_data(self, bus_data):
        """Load bus data into form"""
        self.current_bus = bus_data
        self.renewal_title.setText(f"Renew Insurance - {bus_data['registration_number']}")
        
        # Previous insurance
        self.prev_policy.setText(bus_data['policy_number'])
        self.prev_provider.setText(bus_data['provider'])
        self.prev_coverage.setText(f"₹ {bus_data['coverage_amount']:,}")
        self.prev_expiry.setText(bus_data['expiry_date'])
        
        # Auto-fill new form
        self.new_provider.setCurrentText(bus_data['provider'])
        self.new_coverage.setValue(bus_data['coverage_amount'])
        self.new_premium.setValue(bus_data['premium_amount'])
        
        # Set start date as day after expiry
        expiry_date = QDate.fromString(bus_data['expiry_date'], 'yyyy-MM-dd')
        self.start_date.setDate(expiry_date.addDays(1))
        
    def bus_selected(self):
        """Handle bus selection from combo box"""
        index = self.bus_combo.currentIndex()
        if index >= 0:
            bus_data = self.bus_combo.itemData(index)
            if bus_data:
                self.load_bus_data(bus_data)
                
    def process_renewal(self):
        """Process insurance renewal"""
        if not self.new_policy.text().strip():
            self.status_label.setText("Error: New policy number is required")
            return
            
        if self.new_premium.value() <= 0:
            self.status_label.setText("Error: Premium amount must be greater than 0")
            return
            
        reply = QMessageBox.question(self, "Confirm Renewal",
                                   f"Renew insurance for {self.current_bus['registration_number']}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Success", 
                                  f"Insurance renewed for {self.current_bus['registration_number']}!")
            self.status_label.setText(f"Insurance renewed at {datetime.datetime.now().strftime('%H:%M:%S')}")


class BusDetailsDialog(QDialog):
    """Dialog for displaying bus details"""
    
    def __init__(self, bus_data):
        super().__init__()
        self.bus_data = bus_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle(f"Bus Details - {self.bus_data['registration_number']}")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(f"🚌 {self.bus_data['registration_number']}")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel(f"{self.bus_data['bus_number']} - {self.bus_data['model']}")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Details in read-only form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(8)
        
        # Basic details
        details = [
            ("Registration Number", self.bus_data['registration_number']),
            ("Bus Number", self.bus_data['bus_number']),
            ("Model", self.bus_data['model']),
            ("Capacity", str(self.bus_data['capacity'])),
            ("Year", str(self.bus_data['year'])),
            ("Color", self.bus_data['color']),
            ("Status", self.bus_data['status']),
            ("", ""),  # Empty row for spacing
            ("Insurance Policy", self.bus_data['policy_number']),
            ("Provider", self.bus_data['provider']),
            ("Coverage Amount", f"₹ {self.bus_data['coverage_amount']:,}"),
            ("Premium Amount", f"₹ {self.bus_data['premium_amount']:,}"),
            ("Start Date", self.bus_data['start_date']),
            ("Expiry Date", self.bus_data['expiry_date']),
            ("Insurance Status", self.bus_data['insurance_status']),
            ("Days Remaining", str(self.bus_data['days_remaining']))
        ]
        
        for label, value in details:
            if label:  # Skip empty rows
                value_label = QLabel(value)
                value_label.setFont(QFont("Segoe UI", 10))
                form_layout.addRow(f"{label}:", value_label)
            else:
                form_layout.addRow(QLabel(""), QLabel(""))
        
        layout.addWidget(form_widget)
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)