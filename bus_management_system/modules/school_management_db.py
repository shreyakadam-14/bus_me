# school_management_db.py
# modules/school_management_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, 
    QFrame, QGroupBox, QTabWidget, QTextEdit, QHeaderView, 
    QMessageBox, QCheckBox, QFormLayout, QDialog, QTimeEdit, 
    QScrollArea
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal
import datetime
from db_connection import DatabaseConnection

class SchoolManagementPage(QWidget):
    """School Management with Database Integration"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        self.load_schools()
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_label = QLabel("School Management")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(header_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        self.school_list_tab = SchoolListTab(self.db)
        self.school_form_tab = SchoolFormTab(self.db)
        self.bus_assignment_tab = SchoolBusAssignmentTab(self.db)
        
        # Connect signals
        self.school_list_tab.school_selected.connect(self.on_school_selected)
        self.school_list_tab.assign_buses_requested.connect(self.on_assign_buses)
        self.school_form_tab.school_saved.connect(self.on_school_saved)
        
        self.tab_widget.addTab(self.school_list_tab, "School List")
        self.tab_widget.addTab(self.school_form_tab, "Add/Edit School")
        self.tab_widget.addTab(self.bus_assignment_tab, "Bus Assignment")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 9))
        main_layout.addWidget(self.status_label)
    
    def load_schools(self):
        """Load schools from database"""
        self.school_list_tab.refresh()
    
    def on_school_selected(self, school_id):
        """Handle school selection for editing"""
        self.tab_widget.setCurrentIndex(1)
        self.school_form_tab.load_school(school_id)
    
    def on_assign_buses(self, school_id):
        """Handle bus assignment request"""
        self.tab_widget.setCurrentIndex(2)
        self.bus_assignment_tab.load_school(school_id)
    
    def on_school_saved(self, school_id):
        """Handle school saved"""
        self.status_label.setText(f"School saved at {datetime.datetime.now().strftime('%H:%M:%S')}")
        self.tab_widget.setCurrentIndex(0)
        self.load_schools()


class SchoolListTab(QWidget):
    """School List Tab with Database"""
    
    school_selected = pyqtSignal(int)
    assign_buses_requested = pyqtSignal(int)
    
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
        
        # School table
        self.create_school_table(layout)
        
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
        self.search_input.setPlaceholderText("Search by name, code, city...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input)
        
        # Contract status filter
        filter_layout.addWidget(QLabel("Contract:"))
        self.contract_filter = QComboBox()
        self.contract_filter.addItems(["All", "Active", "Inactive", "Expiring Soon"])
        self.contract_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.contract_filter)
        
        # City filter
        filter_layout.addWidget(QLabel("City:"))
        self.city_filter = QComboBox()
        self.city_filter.addItems(["All", "Delhi", "Mumbai", "Bangalore", "Chennai"])
        self.city_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.city_filter)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        filter_layout.addWidget(refresh_btn)
        
        parent_layout.addWidget(filter_widget)
    
    def create_school_table(self, parent_layout):
        """Create school table"""
        self.school_table = QTableWidget()
        self.school_table.setColumnCount(9)
        self.school_table.setHorizontalHeaderLabels([
            "ID", "School Name", "Code", "City", "Contact Person",
            "Phone", "Contract Status", "Monthly Fee", "Actions"
        ])
        
        header = self.school_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        
        self.school_table.setAlternatingRowColors(True)
        self.school_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.school_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        parent_layout.addWidget(self.school_table)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 10, 0, 0)
        
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(self.view_details)
        action_layout.addWidget(view_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_school)
        action_layout.addWidget(edit_btn)
        
        assign_btn = QPushButton("Assign Buses")
        assign_btn.clicked.connect(self.assign_buses)
        action_layout.addWidget(assign_btn)
        
        add_btn = QPushButton("Add New")
        add_btn.clicked.connect(self.add_new_school)
        action_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_school)
        action_layout.addWidget(delete_btn)
        
        action_layout.addStretch()
        
        parent_layout.addWidget(action_widget)
    
    def refresh(self):
        """Refresh school list"""
        try:
            query = """
                SELECT s.*, 
                       COUNT(ba.id) as bus_count
                FROM schools s
                LEFT JOIN bus_assignments ba ON s.id = ba.school_id AND ba.status = 'Active'
                GROUP BY s.id
                ORDER BY s.id DESC
            """
            schools = self.db.fetch_all(query)
            self.display_schools(schools)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load schools: {e}")
    
    def display_schools(self, schools):
        """Display schools in table"""
        self.school_table.setRowCount(len(schools))
        
        for row, school in enumerate(schools):
            # ID
            id_item = QTableWidgetItem(str(school['id']))
            id_item.setData(Qt.UserRole, school['id'])
            self.school_table.setItem(row, 0, id_item)
            
            # Name
            self.school_table.setItem(row, 1, QTableWidgetItem(school.get('name', '')))
            
            # Code
            self.school_table.setItem(row, 2, QTableWidgetItem(school.get('school_code', '')))
            
            # City
            self.school_table.setItem(row, 3, QTableWidgetItem(school.get('city', '')))
            
            # Contact Person
            self.school_table.setItem(row, 4, QTableWidgetItem(school.get('contact_person', '')))
            
            # Phone
            self.school_table.setItem(row, 5, QTableWidgetItem(school.get('phone', '')))
            
            # Contract Status
            status_item = QTableWidgetItem(school.get('contract_status', 'Unknown'))
            self.colorize_status(status_item, school.get('contract_status'))
            self.school_table.setItem(row, 6, status_item)
            
            # Monthly Fee
            fee = school.get('monthly_fee', 0)
            fee_item = QTableWidgetItem(f"₹ {fee:,.0f}" if fee else "0")
            fee_item.setTextAlignment(Qt.AlignRight)
            self.school_table.setItem(row, 7, fee_item)
            
            # Actions
            action_widget = self.create_action_widget(row, school['id'])
            self.school_table.setCellWidget(row, 8, action_widget)
    
    def create_action_widget(self, row, school_id):
        """Create action buttons widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        view_btn = QPushButton("View")
        view_btn.setFixedWidth(50)
        view_btn.clicked.connect(lambda: self.view_school(school_id))
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedWidth(50)
        edit_btn.clicked.connect(lambda: self.edit_school_by_id(school_id))
        
        assign_btn = QPushButton("Buses")
        assign_btn.setFixedWidth(50)
        assign_btn.clicked.connect(lambda: self.assign_buses_to_school(school_id))
        
        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(assign_btn)
        layout.addStretch()
        
        return widget
    
    def colorize_status(self, item, status):
        """Colorize contract status"""
        if status == 'Active':
            item.setBackground(QColor(220, 255, 220))
            item.setForeground(QColor(0, 100, 0))
        elif status == 'Expiring Soon':
            item.setBackground(QColor(255, 255, 200))
            item.setForeground(QColor(153, 102, 0))
        elif status == 'Inactive':
            item.setBackground(QColor(255, 220, 220))
            item.setForeground(QColor(139, 0, 0))
    
    def get_selected_school_id(self):
        """Get selected school ID"""
        selected = self.school_table.selectedItems()
        if selected:
            return int(self.school_table.item(selected[0].row(), 0).text())
        return None
    
    def view_school(self, school_id):
        """View school details"""
        try:
            school = self.db.fetch_one("SELECT * FROM schools WHERE id = ?", (school_id,))
            if school:
                # Get bus assignments
                buses = self.db.fetch_all("""
                    SELECT b.bus_number, ba.pickup_time, ba.drop_time
                    FROM bus_assignments ba
                    JOIN buses b ON ba.bus_id = b.id
                    WHERE ba.school_id = ? AND ba.status = 'Active'
                """, (school_id,))
                
                dialog = SchoolDetailsDialog(school, buses)
                dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load school details: {e}")
    
    def edit_school_by_id(self, school_id):
        """Edit school by ID"""
        self.school_selected.emit(school_id)
    
    def assign_buses_to_school(self, school_id):
        """Assign buses to school"""
        self.assign_buses_requested.emit(school_id)
    
    def view_details(self):
        """View selected school details"""
        school_id = self.get_selected_school_id()
        if school_id:
            self.view_school(school_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a school")
    
    def edit_school(self):
        """Edit selected school"""
        school_id = self.get_selected_school_id()
        if school_id:
            self.school_selected.emit(school_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a school")
    
    def assign_buses(self):
        """Assign buses to selected school"""
        school_id = self.get_selected_school_id()
        if school_id:
            self.assign_buses_requested.emit(school_id)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a school")
    
    def add_new_school(self):
        """Add new school"""
        self.school_selected.emit(-1)
    
    def delete_school(self):
        """Delete selected school"""
        school_id = self.get_selected_school_id()
        if not school_id:
            QMessageBox.warning(self, "No Selection", "Please select a school")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this school?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete('schools', 'id = ?', [school_id])
                QMessageBox.information(self, "Success", "School deleted successfully")
                self.refresh()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete school: {e}")
    
    def apply_filters(self):
        """Apply filters"""
        search = self.search_input.text().lower()
        contract = self.contract_filter.currentText()
        city = self.city_filter.currentText()
        
        for row in range(self.school_table.rowCount()):
            show = True
            
            if search:
                row_text = ''
                for col in range(5):  # Check first 5 columns
                    item = self.school_table.item(row, col)
                    if item:
                        row_text += item.text().lower() + ' '
                if search not in row_text:
                    show = False
            
            if show and contract != 'All':
                contract_item = self.school_table.item(row, 6)
                if contract_item and contract_item.text() != contract:
                    show = False
            
            if show and city != 'All':
                city_item = self.school_table.item(row, 3)
                if city_item and city_item.text() != city:
                    show = False
            
            self.school_table.setRowHidden(row, not show)


class SchoolFormTab(QWidget):
    """School Form Tab with Database"""
    
    school_saved = pyqtSignal(int)
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_school_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        self.form_title = QLabel("Add New School")
        self.form_title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.form_title)
        
        # Scroll area for long form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Form tabs
        tabs = QTabWidget()
        
        # Basic Info Tab
        basic_tab = self.create_basic_info_tab()
        tabs.addTab(basic_tab, "Basic Information")
        
        # Contact Tab
        contact_tab = self.create_contact_tab()
        tabs.addTab(contact_tab, "Contact Information")
        
        # Contract Tab
        contract_tab = self.create_contract_tab()
        tabs.addTab(contract_tab, "Contract & Billing")
        
        scroll_layout.addWidget(tabs)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save School")
        self.save_btn.clicked.connect(self.save_school)
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
        self.type_combo.addItems(["Private", "Government", "International", "CBSE", "ICSE"])
        layout.addRow("School Type:", self.type_combo)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(60)
        self.address_input.setPlaceholderText("Enter school address")
        layout.addRow("Address*:", self.address_input)
        
        # City
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city")
        layout.addRow("City*:", self.city_input)
        
        # Student Count
        self.student_count = QSpinBox()
        self.student_count.setRange(0, 10000)
        self.student_count.setValue(0)
        layout.addRow("Student Count:", self.student_count)
        
        return tab
    
    def create_contact_tab(self):
        """Create contact information tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Principal Name
        self.principal_input = QLineEdit()
        self.principal_input.setPlaceholderText("Enter principal name")
        layout.addRow("Principal Name:", self.principal_input)
        
        # School Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter school phone")
        layout.addRow("Phone*:", self.phone_input)
        
        # School Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter school email")
        layout.addRow("Email:", self.email_input)
        
        # Contact Person
        self.contact_person = QLineEdit()
        self.contact_person.setPlaceholderText("Enter contact person name")
        layout.addRow("Contact Person*:", self.contact_person)
        
        # Contact Phone
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("Enter contact person phone")
        layout.addRow("Contact Phone*:", self.contact_phone)
        
        return tab
    
    def create_contract_tab(self):
        """Create contract and billing tab"""
        tab = QWidget()
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # Contract Status
        self.contract_status = QComboBox()
        self.contract_status.addItems(["Active", "Inactive", "Expiring Soon", "Negotiation"])
        layout.addRow("Contract Status:", self.contract_status)
        
        # Contract Dates
        dates_widget = QWidget()
        dates_layout = QHBoxLayout(dates_widget)
        dates_layout.setContentsMargins(0, 0, 0, 0)
        
        self.contract_start = QDateEdit()
        self.contract_start.setCalendarPopup(True)
        self.contract_start.setDate(QDate.currentDate())
        
        self.contract_end = QDateEdit()
        self.contract_end.setCalendarPopup(True)
        self.contract_end.setDate(QDate.currentDate().addYears(1))
        
        dates_layout.addWidget(QLabel("Start:"))
        dates_layout.addWidget(self.contract_start)
        dates_layout.addWidget(QLabel("End:"))
        dates_layout.addWidget(self.contract_end)
        
        layout.addRow("Contract Period:", dates_widget)
        
        # Monthly Fee
        self.monthly_fee = QDoubleSpinBox()
        self.monthly_fee.setRange(0, 1000000)
        self.monthly_fee.setPrefix("₹ ")
        self.monthly_fee.setValue(0)
        layout.addRow("Monthly Fee:", self.monthly_fee)
        
        # Payment Status
        self.payment_status = QComboBox()
        self.payment_status.addItems(["Paid", "Pending", "Overdue", "Partially Paid"])
        layout.addRow("Payment Status:", self.payment_status)
        
        # GST Number
        self.gst_input = QLineEdit()
        self.gst_input.setPlaceholderText("Enter GST number")
        layout.addRow("GST Number:", self.gst_input)
        
        return tab
    
    def load_school(self, school_id):
        """Load school data for editing"""
        if school_id == -1:
            self.clear_form()
            return
        
        try:
            school = self.db.fetch_one("SELECT * FROM schools WHERE id = ?", (school_id,))
            if school:
                self.current_school_id = school_id
                self.form_title.setText(f"Edit School: {school['name']}")
                
                # Basic info
                self.name_input.setText(school.get('name', ''))
                self.code_input.setText(school.get('school_code', ''))
                self.type_combo.setCurrentText(school.get('type', 'Private'))
                self.address_input.setPlainText(school.get('address', ''))
                self.city_input.setText(school.get('city', ''))
                self.student_count.setValue(school.get('student_count', 0))
                
                # Contact info
                self.principal_input.setText(school.get('principal_name', ''))
                self.phone_input.setText(school.get('phone', ''))
                self.email_input.setText(school.get('email', ''))
                self.contact_person.setText(school.get('contact_person', ''))
                self.contact_phone.setText(school.get('contact_person_phone', ''))
                
                # Contract info
                self.contract_status.setCurrentText(school.get('contract_status', 'Active'))
                
                if school.get('contract_start'):
                    start = QDate.fromString(school['contract_start'], 'yyyy-MM-dd')
                    self.contract_start.setDate(start)
                
                if school.get('contract_end'):
                    end = QDate.fromString(school['contract_end'], 'yyyy-MM-dd')
                    self.contract_end.setDate(end)
                
                self.monthly_fee.setValue(school.get('monthly_fee', 0))
                self.payment_status.setCurrentText(school.get('payment_status', 'Pending'))
                self.gst_input.setText(school.get('gst_number', ''))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load school: {e}")
    
    def clear_form(self):
        """Clear form"""
        self.current_school_id = None
        self.form_title.setText("Add New School")
        
        self.name_input.clear()
        self.code_input.clear()
        self.type_combo.setCurrentIndex(0)
        self.address_input.clear()
        self.city_input.clear()
        self.student_count.setValue(0)
        
        self.principal_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.contact_person.clear()
        self.contact_phone.clear()
        
        self.contract_status.setCurrentIndex(0)
        self.contract_start.setDate(QDate.currentDate())
        self.contract_end.setDate(QDate.currentDate().addYears(1))
        self.monthly_fee.setValue(0)
        self.payment_status.setCurrentIndex(0)
        self.gst_input.clear()
        
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
            self.status_label.setText("School name is required")
            return False
        if not self.code_input.text().strip():
            self.status_label.setText("School code is required")
            return False
        if not self.address_input.toPlainText().strip():
            self.status_label.setText("Address is required")
            return False
        if not self.city_input.text().strip():
            self.status_label.setText("City is required")
            return False
        if not self.phone_input.text().strip():
            self.status_label.setText("Phone is required")
            return False
        if not self.contact_person.text().strip():
            self.status_label.setText("Contact person is required")
            return False
        if not self.contact_phone.text().strip():
            self.status_label.setText("Contact phone is required")
            return False
        if self.contract_start.date() >= self.contract_end.date():
            self.status_label.setText("Contract end must be after start")
            return False
        return True
    
    def save_school(self):
        """Save school to database"""
        if not self.validate_form():
            return
        
        school_data = {
            'name': self.name_input.text().strip(),
            'school_code': self.code_input.text().strip(),
            'type': self.type_combo.currentText(),
            'address': self.address_input.toPlainText().strip(),
            'city': self.city_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip() or None,
            'principal_name': self.principal_input.text().strip() or None,
            'contact_person': self.contact_person.text().strip(),
            'contact_person_phone': self.contact_phone.text().strip(),
            'student_count': self.student_count.value(),
            'contract_status': self.contract_status.currentText(),
            'contract_start': self.contract_start.date().toString('yyyy-MM-dd'),
            'contract_end': self.contract_end.date().toString('yyyy-MM-dd'),
            'monthly_fee': self.monthly_fee.value(),
            'payment_status': self.payment_status.currentText(),
            'gst_number': self.gst_input.text().strip() or None,
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        try:
            if self.current_school_id:
                self.db.update('schools', school_data, 'id = ?', [self.current_school_id])
                action = "updated"
            else:
                school_data['created_at'] = datetime.datetime.now().isoformat()
                school_id = self.db.insert('schools', school_data)
                action = "added"
            
            self.status_label.setText(f"School {action} successfully")
            self.school_saved.emit(self.current_school_id or school_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save school: {e}")


class SchoolBusAssignmentTab(QWidget):
    """Bus Assignment Tab with Database"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_school_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # School info header
        self.create_school_info(layout)
        
        # Main content
        content_layout = QHBoxLayout()
        
        # Available buses
        self.create_available_buses(content_layout)
        
        # Assigned buses
        self.create_assigned_buses(content_layout)
        
        layout.addLayout(content_layout, 1)
        
        # Action buttons
        self.create_action_buttons(layout)
    
    def create_school_info(self, parent_layout):
        """Create school info header"""
        info_group = QGroupBox("Selected School")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("School:"), 0, 0)
        self.school_name_label = QLabel("No school selected")
        self.school_name_label.setStyleSheet("font-weight: bold; color: #2980b9;")
        info_layout.addWidget(self.school_name_label, 0, 1)
        
        info_layout.addWidget(QLabel("Code:"), 0, 2)
        self.school_code_label = QLabel("-")
        info_layout.addWidget(self.school_code_label, 0, 3)
        
        info_layout.addWidget(QLabel("City:"), 0, 4)
        self.school_city_label = QLabel("-")
        info_layout.addWidget(self.school_city_label, 0, 5)
        
        info_layout.setColumnStretch(6, 1)
        
        parent_layout.addWidget(info_group)
    
    def create_available_buses(self, parent_layout):
        """Create available buses section"""
        group = QGroupBox("Available Buses")
        layout = QVBoxLayout(group)
        
        # Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Bus number...")
        self.search_input.textChanged.connect(self.filter_available)
        filter_layout.addWidget(self.search_input)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.available_table = QTableWidget()
        self.available_table.setColumnCount(4)
        self.available_table.setHorizontalHeaderLabels(["Bus Number", "Model", "Capacity", "Status"])
        self.available_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.available_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.available_table)
        
        # Assign button
        assign_btn = QPushButton("Assign Selected Bus")
        assign_btn.clicked.connect(self.assign_bus)
        layout.addWidget(assign_btn)
        
        parent_layout.addWidget(group)
    
    def create_assigned_buses(self, parent_layout):
        """Create assigned buses section"""
        group = QGroupBox("Assigned Buses")
        layout = QVBoxLayout(group)
        
        # Summary
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("Assigned:"))
        self.assigned_count = QLabel("0")
        self.assigned_count.setStyleSheet("font-weight: bold; color: #27ae60;")
        summary_layout.addWidget(self.assigned_count)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        # Table
        self.assigned_table = QTableWidget()
        self.assigned_table.setColumnCount(5)
        self.assigned_table.setHorizontalHeaderLabels(["Bus Number", "Model", "Pickup", "Drop", "Status"])
        self.assigned_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.assigned_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.assigned_table)
        
        # Remove button
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_assignment)
        layout.addWidget(remove_btn)
        
        parent_layout.addWidget(group)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        save_btn = QPushButton("Save Assignments")
        save_btn.clicked.connect(self.save_assignments)
        layout.addWidget(save_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        back_btn = QPushButton("Back to School List")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        
        parent_layout.addWidget(widget)
    
    def load_school(self, school_id):
        """Load school for assignment"""
        self.current_school_id = school_id
        
        try:
            # Load school info
            school = self.db.fetch_one("SELECT * FROM schools WHERE id = ?", (school_id,))
            if school:
                self.school_name_label.setText(school.get('name', ''))
                self.school_code_label.setText(school.get('school_code', ''))
                self.school_city_label.setText(school.get('city', ''))
            
            # Load available buses
            self.load_available_buses()
            
            # Load assigned buses
            self.load_assigned_buses()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load school: {e}")
    
    def load_available_buses(self):
        """Load available buses"""
        try:
            query = """
                SELECT * FROM buses 
                WHERE status = 'Active' 
                AND id NOT IN (
                    SELECT bus_id FROM bus_assignments 
                    WHERE school_id = ? AND status = 'Active'
                )
                ORDER BY bus_number
            """
            buses = self.db.fetch_all(query, (self.current_school_id,))
            
            self.available_table.setRowCount(len(buses))
            
            for row, bus in enumerate(buses):
                self.available_table.setItem(row, 0, QTableWidgetItem(bus.get('bus_number', '')))
                self.available_table.setItem(row, 1, QTableWidgetItem(bus.get('model', '')))
                self.available_table.setItem(row, 2, QTableWidgetItem(str(bus.get('capacity', ''))))
                
                status_item = QTableWidgetItem(bus.get('status', ''))
                status_item.setBackground(QColor(220, 255, 220))
                self.available_table.setItem(row, 3, status_item)
                
                # Store bus ID
                self.available_table.item(row, 0).setData(Qt.UserRole, bus['id'])
                
        except Exception as e:
            print(f"Error loading available buses: {e}")
    
    def load_assigned_buses(self):
        """Load assigned buses"""
        try:
            query = """
                SELECT ba.*, b.bus_number, b.model, b.capacity
                FROM bus_assignments ba
                JOIN buses b ON ba.bus_id = b.id
                WHERE ba.school_id = ? AND ba.status = 'Active'
                ORDER BY b.bus_number
            """
            assignments = self.db.fetch_all(query, (self.current_school_id,))
            
            self.assigned_table.setRowCount(len(assignments))
            self.assigned_count.setText(str(len(assignments)))
            
            for row, assign in enumerate(assignments):
                self.assigned_table.setItem(row, 0, QTableWidgetItem(assign.get('bus_number', '')))
                self.assigned_table.setItem(row, 1, QTableWidgetItem(assign.get('model', '')))
                self.assigned_table.setItem(row, 2, QTableWidgetItem(assign.get('pickup_time', '')[:5]))
                self.assigned_table.setItem(row, 3, QTableWidgetItem(assign.get('drop_time', '')[:5]))
                
                status_item = QTableWidgetItem('Active')
                status_item.setBackground(QColor(220, 255, 220))
                self.assigned_table.setItem(row, 4, status_item)
                
                # Store assignment ID
                self.assigned_table.item(row, 0).setData(Qt.UserRole, assign['id'])
                
        except Exception as e:
            print(f"Error loading assigned buses: {e}")
    
    def filter_available(self):
        """Filter available buses"""
        search = self.search_input.text().lower()
        
        for row in range(self.available_table.rowCount()):
            show = True
            if search:
                bus_number = self.available_table.item(row, 0).text().lower()
                if search not in bus_number:
                    show = False
            self.available_table.setRowHidden(row, not show)
    
    def assign_bus(self):
        """Assign selected bus to school"""
        selected = self.available_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select a bus")
            return
        
        bus_id = self.available_table.item(selected, 0).data(Qt.UserRole)
        bus_number = self.available_table.item(selected, 0).text()
        
        # Show dialog for pickup/drop times
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Assign Bus {bus_number}")
        layout = QVBoxLayout(dialog)
        
        form = QFormLayout()
        
        pickup = QTimeEdit()
        pickup.setTime(QTime(7, 30))
        form.addRow("Pickup Time:", pickup)
        
        drop = QTimeEdit()
        drop.setTime(QTime(14, 30))
        form.addRow("Drop Time:", drop)
        
        layout.addLayout(form)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("Assign")
        cancel_btn = QPushButton("Cancel")
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Create assignment
                assign_data = {
                    'bus_id': bus_id,
                    'school_id': self.current_school_id,
                    'pickup_time': pickup.time().toString('HH:mm'),
                    'drop_time': drop.time().toString('HH:mm'),
                    'assigned_date': datetime.date.today().isoformat(),
                    'status': 'Active',
                    'created_at': datetime.datetime.now().isoformat()
                }
                
                self.db.insert('bus_assignments', assign_data)
                
                # Refresh lists
                self.load_available_buses()
                self.load_assigned_buses()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to assign bus: {e}")
    
    def remove_assignment(self):
        """Remove selected assignment"""
        selected = self.assigned_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select an assignment")
            return
        
        assign_id = self.assigned_table.item(selected, 0).data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirm Remove",
            "Remove this bus assignment?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.update('bus_assignments', {'status': 'Completed'}, 'id = ?', [assign_id])
                self.load_available_buses()
                self.load_assigned_buses()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove assignment: {e}")
    
    def save_assignments(self):
        """Save assignments"""
        QMessageBox.information(self, "Success", "Assignments saved successfully")
    
    def refresh(self):
        """Refresh data"""
        self.load_available_buses()
        self.load_assigned_buses()
    
    def go_back(self):
        """Go back to school list"""
        parent = self.parent().parent().parent()
        if hasattr(parent, 'tab_widget'):
            parent.tab_widget.setCurrentIndex(0)


class SchoolDetailsDialog(QDialog):
    """School Details Dialog"""
    
    def __init__(self, school_data, buses):
        super().__init__()
        self.school_data = school_data
        self.buses = buses
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"School Details - {self.school_data.get('name', 'Unknown')}")
        self.setFixedSize(500, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(self.school_data.get('name', 'Unknown'))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel(f"Code: {self.school_data.get('school_code', '')}")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addWidget(separator)
        
        # Details
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(8)
        
        details = [
            ("Address:", self.school_data.get('address', 'N/A')),
            ("City:", self.school_data.get('city', 'N/A')),
            ("Phone:", self.school_data.get('phone', 'N/A')),
            ("Email:", self.school_data.get('email', 'N/A')),
            ("Principal:", self.school_data.get('principal_name', 'N/A')),
            ("Contact Person:", self.school_data.get('contact_person', 'N/A')),
            ("Contact Phone:", self.school_data.get('contact_person_phone', 'N/A')),
            ("Student Count:", str(self.school_data.get('student_count', 0))),
            ("Contract Status:", self.school_data.get('contract_status', 'N/A')),
            ("Contract Period:", f"{self.school_data.get('contract_start', '')} to {self.school_data.get('contract_end', '')}"),
            ("Monthly Fee:", f"₹ {self.school_data.get('monthly_fee', 0):,.0f}"),
            ("Payment Status:", self.school_data.get('payment_status', 'N/A')),
            ("GST:", self.school_data.get('gst_number', 'N/A'))
        ]
        
        for label, value in details:
            value_label = QLabel(str(value))
            value_label.setWordWrap(True)
            form_layout.addRow(label, value_label)
        
        layout.addWidget(form_widget)
        
        # Assigned Buses
        if self.buses:
            buses_label = QLabel("Assigned Buses:")
            buses_label.setFont(QFont("Arial", 10, QFont.Bold))
            layout.addWidget(buses_label)
            
            for bus in self.buses:
                bus_text = f"• {bus['bus_number']} (Pickup: {bus.get('pickup_time', '')}, Drop: {bus.get('drop_time', '')})"
                layout.addWidget(QLabel(bus_text))
        
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)