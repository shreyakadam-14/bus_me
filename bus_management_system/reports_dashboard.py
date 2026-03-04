# reports_dashboard.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem,
    QDateEdit, QComboBox, QLineEdit, QGroupBox, QScrollArea,
    QSplitter, QHeaderView, QMessageBox, QProgressBar,
    QSizePolicy, QSpacerItem, QToolButton, QTableWidgetSelectionRange,
    QTextEdit, QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox,
    QDialog, QTabWidget, QDialogButtonBox, QRadioButton,
    QButtonGroup, QFileDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QDate, QSize, pyqtSignal
import datetime
import json

# ============================================================================
# BASE REPORT GENERATOR CLASS
# ============================================================================

class ReportGenerator(QWidget):
    """Base class for report generation"""
    
    report_generated = pyqtSignal(dict)  # Signal emitted when report is generated
    
    def __init__(self, report_type="generic"):
        super().__init__()
        self.report_type = report_type
        self.report_data = {}
        self.filters = {}
        
    def create_basic_controls(self):
        """Create basic report controls"""
        basic_group = QGroupBox("Report Settings")
        basic_layout = QFormLayout(basic_group)
        
        # Report name
        self.report_name = QLineEdit()
        self.report_name.setPlaceholderText(f"Enter {self.report_type.capitalize()} Report Name")
        basic_layout.addRow("Report Name:", self.report_name)
        
        # Date range
        date_widget = QWidget()
        date_layout = QHBoxLayout(date_widget)
        date_layout.setContentsMargins(0, 0, 0, 0)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        
        date_layout.addWidget(QLabel("From:"))
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.end_date)
        
        basic_layout.addRow("Date Range:", date_widget)
        
        # Format selection
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PDF", "Excel", "CSV", "HTML"])
        basic_layout.addRow("Output Format:", self.format_combo)
        
        # Include summary checkbox
        self.include_summary = QCheckBox("Include Summary")
        self.include_summary.setChecked(True)
        basic_layout.addRow("", self.include_summary)
        
        # Include charts checkbox
        self.include_charts = QCheckBox("Include Charts/Graphs")
        self.include_charts.setChecked(True)
        basic_layout.addRow("", self.include_charts)
        
        return basic_group
    
    def create_preview_section(self):
        """Create preview section"""
        preview_group = QGroupBox("Report Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        # Preview text area
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(200)
        preview_layout.addWidget(self.preview_text)
        
        # Update preview button
        update_btn = QPushButton("Update Preview")
        update_btn.clicked.connect(self.update_preview)
        preview_layout.addWidget(update_btn)
        
        return preview_group
    
    def update_preview(self):
        """Update the preview - to be overridden"""
        self.preview_text.setText("Preview not available for this report type.")
    
    def validate_filters(self):
        """Validate filters"""
        if not self.report_name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter a report name.")
            return False
        
        if self.start_date.date() > self.end_date.date():
            QMessageBox.warning(self, "Validation Error", "Start date cannot be after end date.")
            return False
            
        return True

# ============================================================================
# FINANCIAL REPORT GENERATOR
# ============================================================================

class FinancialReportGenerator(ReportGenerator):
    """Financial Report Generator"""
    
    def __init__(self):
        super().__init__("financial")
        self.init_ui()
        
    def init_ui(self):
        """Initialize financial-specific UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        
        # Basic Settings Tab
        basic_tab = self.create_basic_controls()
        tabs.addTab(basic_tab, "Basic Settings")
        
        # Financial Filters Tab
        filters_tab = self.create_financial_filters()
        tabs.addTab(filters_tab, "Financial Filters")
        
        # Customization Tab
        custom_tab = self.create_customization_tab()
        tabs.addTab(custom_tab, "Customization")
        
        # Preview Tab
        preview_tab = self.create_preview_section()
        tabs.addTab(preview_tab, "Preview")
        
        layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        save_template_btn = QPushButton("Save as Template")
        save_template_btn.clicked.connect(self.save_template)
        action_layout.addWidget(save_template_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        action_layout.addWidget(reset_btn)
        
        layout.addLayout(action_layout)
        
    def create_financial_filters(self):
        """Create financial-specific filters"""
        filter_widget = QWidget()
        layout = QFormLayout(filter_widget)
        
        # Report Type
        self.report_subtype = QComboBox()
        self.report_subtype.addItems([
            "Income Statement",
            "Balance Sheet", 
            "Cash Flow",
            "Profit & Loss",
            "Revenue Analysis",
            "Expense Analysis",
            "Budget vs Actual"
        ])
        layout.addRow("Report Type:", self.report_subtype)
        
        # Transaction Type
        self.transaction_type = QComboBox()
        self.transaction_type.addItems(["All", "Income", "Expense", "Investment", "Loan"])
        layout.addRow("Transaction Type:", self.transaction_type)
        
        # Minimum Amount
        self.min_amount = QDoubleSpinBox()
        self.min_amount.setRange(0, 1000000)
        self.min_amount.setPrefix("₹ ")
        self.min_amount.setValue(0)
        layout.addRow("Minimum Amount:", self.min_amount)
        
        # Categories (checkboxes)
        categories_group = QGroupBox("Include Categories:")
        categories_layout = QGridLayout(categories_group)
        
        self.categories = {
            'bus_fares': QCheckBox("Bus Fares"),
            'maintenance': QCheckBox("Maintenance"),
            'fuel': QCheckBox("Fuel"),
            'insurance': QCheckBox("Insurance"),
            'salaries': QCheckBox("Salaries"),
            'taxes': QCheckBox("Taxes"),
            'other': QCheckBox("Other Expenses")
        }
        
        for i, (key, checkbox) in enumerate(self.categories.items()):
            checkbox.setChecked(True)
            categories_layout.addWidget(checkbox, i // 3, i % 3)
        
        layout.addRow(categories_group)
        
        # Group by
        self.group_by = QComboBox()
        self.group_by.addItems(["Day", "Week", "Month", "Quarter", "Year", "Category"])
        layout.addRow("Group By:", self.group_by)
        
        return filter_widget
    
    def create_customization_tab(self):
        """Create customization options"""
        custom_widget = QWidget()
        layout = QFormLayout(custom_widget)
        
        # Currency
        self.currency = QComboBox()
        self.currency.addItems(["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
        layout.addRow("Currency:", self.currency)
        
        # Number format
        self.number_format = QComboBox()
        self.number_format.addItems(["1,000.00", "1.000,00", "1 000.00"])
        layout.addRow("Number Format:", self.number_format)
        
        # Include VAT/GST
        self.include_tax = QCheckBox("Include Tax Calculations")
        self.include_tax.setChecked(True)
        layout.addRow("", self.include_tax)
        
        # Include comparisons
        self.include_comparisons = QCheckBox("Include Year-over-Year Comparisons")
        self.include_comparisons.setChecked(True)
        layout.addRow("", self.include_comparisons)
        
        # Comments/Notes
        self.comments = QTextEdit()
        self.comments.setMaximumHeight(80)
        self.comments.setPlaceholderText("Add comments or notes for this report...")
        layout.addRow("Comments:", self.comments)
        
        return custom_widget
    
    def update_preview(self):
        """Update financial report preview"""
        preview_text = f"""
FINANCIAL REPORT PREVIEW
========================

Report Name: {self.report_name.text() or 'Unnamed Financial Report'}
Report Type: {self.report_subtype.currentText()}
Period: {self.start_date.date().toString("dd-MMM-yyyy")} to {self.end_date.date().toString("dd-MMM-yyyy")}

INCLUDED DATA:
- Transaction Type: {self.transaction_type.currentText()}
- Minimum Amount: ₹ {self.min_amount.value():,.2f}
- Grouped By: {self.group_by.currentText()}
- Currency: {self.currency.currentText()}

SECTIONS:
1. Summary Overview
2. Income Analysis
3. Expense Breakdown
4. Net Profit/Loss
5. Budget vs Actual Comparison
6. Recommendations

FORMAT: {self.format_combo.currentText()}
CHARTS: {'Yes' if self.include_charts.isChecked() else 'No'}
COMMENTS: {self.comments.toPlainText() or 'No comments added'}
"""
        self.preview_text.setText(preview_text)
    
    def generate_report(self):
        """Generate financial report"""
        # Get filters
        categories_selected = [name for name, cb in self.categories.items() if cb.isChecked()]
        
        self.filters = {
            'report_subtype': self.report_subtype.currentText(),
            'transaction_type': self.transaction_type.currentText(),
            'min_amount': self.min_amount.value(),
            'categories': categories_selected,
            'group_by': self.group_by.currentText(),
            'currency': self.currency.currentText(),
            'include_tax': self.include_tax.isChecked(),
            'include_comparisons': self.include_comparisons.isChecked(),
            'comments': self.comments.toPlainText()
        }
        
        # Simulate data fetching
        mock_data = self.get_financial_data()
        
        report = {
            'name': self.report_name.text() or f"Financial Report - {self.report_subtype.currentText()}",
            'type': 'financial',
            'subtype': self.report_subtype.currentText(),
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'period': f"{self.start_date.date().toString('dd-MMM-yyyy')} to {self.end_date.date().toString('dd-MMM-yyyy')}",
            'filters': self.filters,
            'data': mock_data,
            'summary': self.generate_summary(mock_data),
            'format': self.format_combo.currentText()
        }
        
        return report
    
    def get_financial_data(self):
        """Get mock financial data"""
        return [
            {"category": "Bus Fares", "amount": 1250000, "budget": 1200000, "variance": "+4.17%"},
            {"category": "Maintenance", "amount": 185000, "budget": 200000, "variance": "-7.50%"},
            {"category": "Fuel", "amount": 325000, "budget": 300000, "variance": "+8.33%"},
            {"category": "Insurance", "amount": 75000, "budget": 75000, "variance": "0.00%"},
            {"category": "Salaries", "amount": 450000, "budget": 450000, "variance": "0.00%"},
            {"category": "Taxes", "amount": 125000, "budget": 120000, "variance": "+4.17%"},
            {"category": "Other", "amount": 65000, "budget": 60000, "variance": "+8.33%"}
        ]
    
    def generate_summary(self, data):
        """Generate summary from data"""
        total_income = sum(item['amount'] for item in data if item['category'] == 'Bus Fares')
        total_expense = sum(item['amount'] for item in data if item['category'] != 'Bus Fares')
        net_profit = total_income - total_expense
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_profit': net_profit,
            'profit_margin': (net_profit / total_income * 100) if total_income > 0 else 0
        }
    
    def on_generate(self):
        """Handle generate button click"""
        if self.validate_filters():
            report = self.generate_report()
            self.report_generated.emit(report)
            
            # Show success message
            QMessageBox.information(self, "Success", 
                                  f"Financial report generated!\n\n"
                                  f"Name: {report['name']}\n"
                                  f"Type: {report['subtype']}\n"
                                  f"Format: {report['format']}")
    
    def save_template(self):
        """Save report as template"""
        template = {
            'name': self.report_name.text(),
            'type': 'financial',
            'filters': self.filters,
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Template", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(template, f, indent=2)
            QMessageBox.information(self, "Saved", "Template saved successfully!")
    
    def reset_form(self):
        """Reset form to defaults"""
        self.report_name.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.format_combo.setCurrentIndex(0)
        self.report_subtype.setCurrentIndex(0)
        self.transaction_type.setCurrentIndex(0)
        self.min_amount.setValue(0)
        for checkbox in self.categories.values():
            checkbox.setChecked(True)
        self.group_by.setCurrentIndex(0)
        self.currency.setCurrentIndex(0)
        self.number_format.setCurrentIndex(0)
        self.include_tax.setChecked(True)
        self.include_comparisons.setChecked(True)
        self.comments.clear()

# ============================================================================
# BUS REPORT GENERATOR
# ============================================================================

class BusReportGenerator(ReportGenerator):
    """Bus Report Generator"""
    
    def __init__(self):
        super().__init__("bus")
        self.init_ui()
        
    def init_ui(self):
        """Initialize bus-specific UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        
        # Basic Settings Tab
        basic_tab = self.create_basic_controls()
        tabs.addTab(basic_tab, "Basic Settings")
        
        # Bus Filters Tab
        filters_tab = self.create_bus_filters()
        tabs.addTab(filters_tab, "Bus Filters")
        
        # Metrics Tab
        metrics_tab = self.create_metrics_tab()
        tabs.addTab(metrics_tab, "Metrics")
        
        # Preview Tab
        preview_tab = self.create_preview_section()
        tabs.addTab(preview_tab, "Preview")
        
        layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        save_template_btn = QPushButton("Save Template")
        save_template_btn.clicked.connect(self.save_template)
        action_layout.addWidget(save_template_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        action_layout.addWidget(reset_btn)
        
        layout.addLayout(action_layout)
    
    def create_bus_filters(self):
        """Create bus-specific filters"""
        filter_widget = QWidget()
        layout = QFormLayout(filter_widget)
        
        # Report Type
        self.report_subtype = QComboBox()
        self.report_subtype.addItems([
            "Bus Utilization",
            "Maintenance Schedule",
            "Fuel Consumption", 
            "Insurance Status",
            "Bus Assignment",
            "Performance Analysis",
            "Route Efficiency"
        ])
        layout.addRow("Report Type:", self.report_subtype)
        
        # Bus Status
        self.bus_status = QComboBox()
        self.bus_status.addItems(["All", "Active", "Inactive", "Maintenance", "Repair"])
        layout.addRow("Bus Status:", self.bus_status)
        
        # Bus Type/Model
        self.bus_type = QLineEdit()
        self.bus_type.setPlaceholderText("e.g., Tata Starbus, All")
        layout.addRow("Bus Model:", self.bus_type)
        
        # Capacity Range
        capacity_widget = QWidget()
        capacity_layout = QHBoxLayout(capacity_widget)
        
        self.min_capacity = QSpinBox()
        self.min_capacity.setRange(0, 100)
        self.min_capacity.setValue(0)
        
        self.max_capacity = QSpinBox()
        self.max_capacity.setRange(0, 100)
        self.max_capacity.setValue(100)
        
        capacity_layout.addWidget(QLabel("Min:"))
        capacity_layout.addWidget(self.min_capacity)
        capacity_layout.addWidget(QLabel("Max:"))
        capacity_layout.addWidget(self.max_capacity)
        
        layout.addRow("Capacity Range:", capacity_widget)
        
        # Include inactive buses
        self.include_inactive = QCheckBox("Include Inactive Buses")
        self.include_inactive.setChecked(False)
        layout.addRow("", self.include_inactive)
        
        # Sort by
        self.sort_by = QComboBox()
        self.sort_by.addItems(["Registration Number", "Bus Number", "Capacity", "Year", "Status"])
        layout.addRow("Sort By:", self.sort_by)
        
        return filter_widget
    
    def create_metrics_tab(self):
        """Create metrics selection"""
        metrics_widget = QWidget()
        layout = QFormLayout(metrics_widget)
        
        # Metrics to include
        metrics_group = QGroupBox("Include Metrics:")
        metrics_layout = QGridLayout(metrics_group)
        
        self.metrics = {
            'utilization_rate': QCheckBox("Utilization Rate"),
            'fuel_efficiency': QCheckBox("Fuel Efficiency"),
            'maintenance_cost': QCheckBox("Maintenance Cost"),
            'insurance_status': QCheckBox("Insurance Status"),
            'driver_assignment': QCheckBox("Driver Assignment"),
            'school_assignment': QCheckBox("School Assignment"),
            'revenue_generated': QCheckBox("Revenue Generated"),
            'operating_cost': QCheckBox("Operating Cost")
        }
        
        for i, (key, checkbox) in enumerate(self.metrics.items()):
            checkbox.setChecked(True)
            metrics_layout.addWidget(checkbox, i // 3, i % 3)
        
        layout.addRow(metrics_group)
        
        # Show details level
        self.detail_level = QComboBox()
        self.detail_level.addItems(["Summary Only", "Detailed", "Very Detailed"])
        layout.addRow("Detail Level:", self.detail_level)
        
        return metrics_widget
    
    def update_preview(self):
        """Update bus report preview"""
        selected_metrics = [cb.text() for cb in self.metrics.values() if cb.isChecked()]
        
        preview_text = f"""
BUS REPORT PREVIEW
==================

Report Name: {self.report_name.text() or 'Unnamed Bus Report'}
Report Type: {self.report_subtype.currentText()}
Period: {self.start_date.date().toString("dd-MMM-yyyy")} to {self.end_date.date().toString("dd-MMM-yyyy")}

FILTERS:
- Bus Status: {self.bus_status.currentText()}
- Bus Model: {self.bus_type.text() or 'All'}
- Capacity: {self.min_capacity.value()} to {self.max_capacity.value()} seats
- Include Inactive: {'Yes' if self.include_inactive.isChecked() else 'No'}
- Sort By: {self.sort_by.currentText()}

METRICS INCLUDED ({len(selected_metrics)}):
{chr(10).join(f"  • {metric}" for metric in selected_metrics)}

DETAIL LEVEL: {self.detail_level.currentText()}
OUTPUT FORMAT: {self.format_combo.currentText()}
CHARTS INCLUDED: {'Yes' if self.include_charts.isChecked() else 'No'}
"""
        self.preview_text.setText(preview_text)
    
    def generate_report(self):
        """Generate bus report"""
        # Collect metrics
        selected_metrics = [cb.text() for cb in self.metrics.values() if cb.isChecked()]
        
        self.filters = {
            'report_subtype': self.report_subtype.currentText(),
            'bus_status': self.bus_status.currentText(),
            'bus_type': self.bus_type.text(),
            'capacity_range': f"{self.min_capacity.value()}-{self.max_capacity.value()}",
            'include_inactive': self.include_inactive.isChecked(),
            'sort_by': self.sort_by.currentText(),
            'metrics': selected_metrics,
            'detail_level': self.detail_level.currentText()
        }
        
        # Simulate data fetching
        mock_data = self.get_bus_data()
        
        report = {
            'name': self.report_name.text() or f"Bus Report - {self.report_subtype.currentText()}",
            'type': 'bus',
            'subtype': self.report_subtype.currentText(),
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'period': f"{self.start_date.date().toString('dd-MMM-yyyy')} to {self.end_date.date().toString('dd-MMM-yyyy')}",
            'filters': self.filters,
            'data': mock_data,
            'summary': self.generate_bus_summary(mock_data),
            'format': self.format_combo.currentText()
        }
        
        return report
    
    def get_bus_data(self):
        """Get mock bus data"""
        return [
            {"bus_no": "BUS-001", "registration": "MH-01-AB-1234", "status": "Active", 
             "utilization": "85%", "fuel_eff": "8.5 kmpl", "maintenance_cost": 15000},
            {"bus_no": "BUS-002", "registration": "MH-01-CD-5678", "status": "Active",
             "utilization": "92%", "fuel_eff": "7.8 kmpl", "maintenance_cost": 22000},
            {"bus_no": "BUS-003", "registration": "MH-01-EF-9012", "status": "Maintenance",
             "utilization": "65%", "fuel_eff": "9.2 kmpl", "maintenance_cost": 35000},
            {"bus_no": "BUS-004", "registration": "MH-01-GH-3456", "status": "Active",
             "utilization": "78%", "fuel_eff": "8.1 kmpl", "maintenance_cost": 18000}
        ]
    
    def generate_bus_summary(self, data):
        """Generate bus summary"""
        active_buses = len([b for b in data if b['status'] == 'Active'])
        total_buses = len(data)
        avg_utilization = sum(float(b['utilization'].strip('%')) for b in data) / total_buses if total_buses > 0 else 0
        total_maintenance = sum(b['maintenance_cost'] for b in data)
        
        return {
            'total_buses': total_buses,
            'active_buses': active_buses,
            'inactive_buses': total_buses - active_buses,
            'avg_utilization': f"{avg_utilization:.1f}%",
            'total_maintenance_cost': f"₹ {total_maintenance:,}",
            'avg_maintenance_per_bus': f"₹ {total_maintenance/total_buses:,.0f}" if total_buses > 0 else "₹ 0"
        }
    
    def on_generate(self):
        """Handle generate button click"""
        if self.validate_filters():
            report = self.generate_report()
            self.report_generated.emit(report)
            
            QMessageBox.information(self, "Success", 
                                  f"Bus report generated!\n\n"
                                  f"Name: {report['name']}\n"
                                  f"Type: {report['subtype']}\n"
                                  f"Format: {report['format']}")
    
    def save_template(self):
        """Save template"""
        if not self.report_name.text().strip():
            QMessageBox.warning(self, "Error", "Please enter a report name first.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Template", f"{self.report_name.text()}.json", "JSON Files (*.json)"
        )
        
        if file_path:
            template = {
                'name': self.report_name.text(),
                'type': 'bus',
                'filters': self.filters,
                'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(file_path, 'w') as f:
                json.dump(template, f, indent=2)
            QMessageBox.information(self, "Saved", "Template saved successfully!")
    
    def reset_form(self):
        """Reset form"""
        self.report_name.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.format_combo.setCurrentIndex(0)
        self.report_subtype.setCurrentIndex(0)
        self.bus_status.setCurrentIndex(0)
        self.bus_type.clear()
        self.min_capacity.setValue(0)
        self.max_capacity.setValue(100)
        self.include_inactive.setChecked(False)
        self.sort_by.setCurrentIndex(0)
        for checkbox in self.metrics.values():
            checkbox.setChecked(True)
        self.detail_level.setCurrentIndex(0)

# ============================================================================
# SCHOOL REPORT GENERATOR
# ============================================================================

class SchoolReportGenerator(ReportGenerator):
    """School Report Generator"""
    
    def __init__(self):
        super().__init__("school")
        self.init_ui()
        
    def init_ui(self):
        """Initialize school-specific UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        
        # Basic Settings Tab
        basic_tab = self.create_basic_controls()
        tabs.addTab(basic_tab, "Basic Settings")
        
        # School Filters Tab
        filters_tab = self.create_school_filters()
        tabs.addTab(filters_tab, "School Filters")
        
        # Billing Tab
        billing_tab = self.create_billing_tab()
        tabs.addTab(billing_tab, "Billing & Contracts")
        
        # Preview Tab
        preview_tab = self.create_preview_section()
        tabs.addTab(preview_tab, "Preview")
        
        layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        action_layout.addWidget(reset_btn)
        
        layout.addLayout(action_layout)
    
    def create_school_filters(self):
        """Create school-specific filters"""
        filter_widget = QWidget()
        layout = QFormLayout(filter_widget)
        
        # Report Type
        self.report_subtype = QComboBox()
        self.report_subtype.addItems([
            "School Contracts",
            "Student Transport", 
            "Billing & Payments",
            "Route Assignment",
            "Service Performance",
            "Contract Renewals"
        ])
        layout.addRow("Report Type:", self.report_subtype)
        
        # School Type
        self.school_type = QComboBox()
        self.school_type.addItems(["All", "Private", "Government", "International", "CBSE", "ICSE"])
        layout.addRow("School Type:", self.school_type)
        
        # Contract Status
        self.contract_status = QComboBox()
        self.contract_status.addItems(["All", "Active", "Expired", "Expiring Soon", "Under Negotiation"])
        layout.addRow("Contract Status:", self.contract_status)
        
        # City/Location
        self.location = QLineEdit()
        self.location.setPlaceholderText("e.g., Delhi, Gurgaon, All")
        layout.addRow("Location:", self.location)
        
        # Minimum Students
        self.min_students = QSpinBox()
        self.min_students.setRange(0, 10000)
        self.min_students.setValue(0)
        layout.addRow("Minimum Students:", self.min_students)
        
        # Payment Status
        self.payment_status = QComboBox()
        self.payment_status.addItems(["All", "Paid", "Pending", "Overdue", "Partially Paid"])
        layout.addRow("Payment Status:", self.payment_status)
        
        return filter_widget
    
    def create_billing_tab(self):
        """Create billing and contract options"""
        billing_widget = QWidget()
        layout = QFormLayout(billing_widget)
        
        # Billing Period
        self.billing_period = QComboBox()
        self.billing_period.addItems(["Monthly", "Quarterly", "Half-Yearly", "Yearly"])
        layout.addRow("Billing Period:", self.billing_period)
        
        # Include billing details
        self.include_invoices = QCheckBox("Include Invoice Details")
        self.include_invoices.setChecked(True)
        layout.addRow("", self.include_invoices)
        
        self.include_payments = QCheckBox("Include Payment Records")
        self.include_payments.setChecked(True)
        layout.addRow("", self.include_payments)
        
        self.include_outstanding = QCheckBox("Include Outstanding Amounts")
        self.include_outstanding.setChecked(True)
        layout.addRow("", self.include_outstanding)
        
        # Contract details
        self.include_contract_terms = QCheckBox("Include Contract Terms")
        self.include_contract_terms.setChecked(False)
        layout.addRow("", self.include_contract_terms)
        
        return billing_widget
    
    def update_preview(self):
        """Update school report preview"""
        preview_text = f"""
SCHOOL REPORT PREVIEW
=====================

Report Name: {self.report_name.text() or 'Unnamed School Report'}
Report Type: {self.report_subtype.currentText()}
Period: {self.start_date.date().toString("dd-MMM-yyyy")} to {self.end_date.date().toString("dd-MMM-yyyy")}

FILTERS:
- School Type: {self.school_type.currentText()}
- Contract Status: {self.contract_status.currentText()}
- Location: {self.location.text() or 'All'}
- Minimum Students: {self.min_students.value()}
- Payment Status: {self.payment_status.currentText()}

BILLING OPTIONS:
- Billing Period: {self.billing_period.currentText()}
- Include Invoices: {'Yes' if self.include_invoices.isChecked() else 'No'}
- Include Payments: {'Yes' if self.include_payments.isChecked() else 'No'}
- Include Outstanding: {'Yes' if self.include_outstanding.isChecked() else 'No'}

OUTPUT FORMAT: {self.format_combo.currentText()}
CHARTS INCLUDED: {'Yes' if self.include_charts.isChecked() else 'No'}
"""
        self.preview_text.setText(preview_text)
    
    def on_generate(self):
        """Handle generate button click"""
        if self.validate_filters():
            report = self.generate_report()
            self.report_generated.emit(report)
            
            QMessageBox.information(self, "Success", 
                                  f"School report generated!\n\n"
                                  f"Name: {report['name']}\n"
                                  f"Type: {report['subtype']}\n"
                                  f"Format: {report['format']}")
    
    def reset_form(self):
        """Reset form"""
        self.report_name.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.format_combo.setCurrentIndex(0)
        self.report_subtype.setCurrentIndex(0)
        self.school_type.setCurrentIndex(0)
        self.contract_status.setCurrentIndex(0)
        self.location.clear()
        self.min_students.setValue(0)
        self.payment_status.setCurrentIndex(0)
        self.billing_period.setCurrentIndex(0)
        self.include_invoices.setChecked(True)
        self.include_payments.setChecked(True)
        self.include_outstanding.setChecked(True)
        self.include_contract_terms.setChecked(False)

# ============================================================================
# DRIVER REPORT GENERATOR
# ============================================================================

class DriverReportGenerator(ReportGenerator):
    """Driver Report Generator"""
    
    def __init__(self):
        super().__init__("driver")
        self.init_ui()
        
    def init_ui(self):
        """Initialize driver-specific UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        
        # Basic Settings Tab
        basic_tab = self.create_basic_controls()
        tabs.addTab(basic_tab, "Basic Settings")
        
        # Driver Filters Tab
        filters_tab = self.create_driver_filters()
        tabs.addTab(filters_tab, "Driver Filters")
        
        # Performance Tab
        performance_tab = self.create_performance_tab()
        tabs.addTab(performance_tab, "Performance Metrics")
        
        # Preview Tab
        preview_tab = self.create_preview_section()
        tabs.addTab(preview_tab, "Preview")
        
        layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        action_layout.addWidget(reset_btn)
        
        layout.addLayout(action_layout)
    
    def create_driver_filters(self):
        """Create driver-specific filters"""
        filter_widget = QWidget()
        layout = QFormLayout(filter_widget)
        
        # Report Type
        self.report_subtype = QComboBox()
        self.report_subtype.addItems([
            "Driver Performance",
            "Attendance & Schedule", 
            "Salary & Payments",
            "License & Certification",
            "Assignment Details",
            "Incident Reports"
        ])
        layout.addRow("Report Type:", self.report_subtype)
        
        # Driver Status
        self.driver_status = QComboBox()
        self.driver_status.addItems(["All", "Active", "Inactive", "On Leave", "Suspended"])
        layout.addRow("Driver Status:", self.driver_status)
        
        # Experience Range
        experience_widget = QWidget()
        experience_layout = QHBoxLayout(experience_widget)
        
        self.min_experience = QSpinBox()
        self.min_experience.setRange(0, 50)
        self.min_experience.setValue(0)
        
        self.max_experience = QSpinBox()
        self.max_experience.setRange(0, 50)
        self.max_experience.setValue(50)
        
        experience_layout.addWidget(QLabel("Min:"))
        experience_layout.addWidget(self.min_experience)
        experience_layout.addWidget(QLabel("Max:"))
        experience_layout.addWidget(self.max_experience)
        
        layout.addRow("Experience (Years):", experience_widget)
        
        # Assigned Bus
        self.assigned_bus = QLineEdit()
        self.assigned_bus.setPlaceholderText("e.g., BUS-001, All")
        layout.addRow("Assigned Bus:", self.assigned_bus)
        
        # License Status
        self.license_status = QComboBox()
        self.license_status.addItems(["All", "Valid", "Expiring Soon", "Expired"])
        layout.addRow("License Status:", self.license_status)
        
        return filter_widget
    
    def create_performance_tab(self):
        """Create performance metrics options"""
        performance_widget = QWidget()
        layout = QFormLayout(performance_widget)
        
        # Performance metrics
        metrics_group = QGroupBox("Include Performance Metrics:")
        metrics_layout = QGridLayout(metrics_group)
        
        self.metrics = {
            'attendance': QCheckBox("Attendance Rate"),
            'punctuality': QCheckBox("Punctuality"),
            'safety_score': QCheckBox("Safety Score"),
            'fuel_efficiency': QCheckBox("Fuel Efficiency"),
            'incident_count': QCheckBox("Incident Count"),
            'customer_feedback': QCheckBox("Customer Feedback"),
            'training_completion': QCheckBox("Training Completion"),
            'salary_details': QCheckBox("Salary Details")
        }
        
        for i, (key, checkbox) in enumerate(self.metrics.items()):
            checkbox.setChecked(True)
            metrics_layout.addWidget(checkbox, i // 3, i % 3)
        
        layout.addRow(metrics_group)
        
        # Rating filter
        self.min_rating = QDoubleSpinBox()
        self.min_rating.setRange(0, 5)
        self.min_rating.setValue(0)
        self.min_rating.setSingleStep(0.5)
        layout.addRow("Minimum Rating (0-5):", self.min_rating)
        
        return performance_widget
    
    def update_preview(self):
        """Update driver report preview"""
        selected_metrics = [cb.text() for cb in self.metrics.values() if cb.isChecked()]
        
        preview_text = f"""
DRIVER REPORT PREVIEW
=====================

Report Name: {self.report_name.text() or 'Unnamed Driver Report'}
Report Type: {self.report_subtype.currentText()}
Period: {self.start_date.date().toString("dd-MMM-yyyy")} to {self.end_date.date().toString("dd-MMM-yyyy")}

FILTERS:
- Driver Status: {self.driver_status.currentText()}
- Experience: {self.min_experience.value()} to {self.max_experience.value()} years
- Assigned Bus: {self.assigned_bus.text() or 'All'}
- License Status: {self.license_status.currentText()}
- Minimum Rating: {self.min_rating.value()}/5

PERFORMANCE METRICS ({len(selected_metrics)}):
{chr(10).join(f"  • {metric}" for metric in selected_metrics)}

OUTPUT FORMAT: {self.format_combo.currentText()}
CHARTS INCLUDED: {'Yes' if self.include_charts.isChecked() else 'No'}
"""
        self.preview_text.setText(preview_text)
    
    def on_generate(self):
        """Handle generate button click"""
        if self.validate_filters():
            report = self.generate_report()
            self.report_generated.emit(report)
            
            QMessageBox.information(self, "Success", 
                                  f"Driver report generated!\n\n"
                                  f"Name: {report['name']}\n"
                                  f"Type: {report['subtype']}\n"
                                  f"Format: {report['format']}")
    
    def reset_form(self):
        """Reset form"""
        self.report_name.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.format_combo.setCurrentIndex(0)
        self.report_subtype.setCurrentIndex(0)
        self.driver_status.setCurrentIndex(0)
        self.min_experience.setValue(0)
        self.max_experience.setValue(50)
        self.assigned_bus.clear()
        self.license_status.setCurrentIndex(0)
        for checkbox in self.metrics.values():
            checkbox.setChecked(True)
        self.min_rating.setValue(0)

# ============================================================================
# SYSTEM REPORT GENERATOR
# ============================================================================

class SystemReportGenerator(ReportGenerator):
    """System Report Generator"""
    
    def __init__(self):
        super().__init__("system")
        self.init_ui()
        
    def init_ui(self):
        """Initialize system-specific UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        
        # Basic Settings Tab
        basic_tab = self.create_basic_controls()
        tabs.addTab(basic_tab, "Basic Settings")
        
        # System Filters Tab
        filters_tab = self.create_system_filters()
        tabs.addTab(filters_tab, "System Filters")
        
        # Log Details Tab
        log_tab = self.create_log_details_tab()
        tabs.addTab(log_tab, "Log Details")
        
        # Preview Tab
        preview_tab = self.create_preview_section()
        tabs.addTab(preview_tab, "Preview")
        
        layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_form)
        action_layout.addWidget(reset_btn)
        
        layout.addLayout(action_layout)
    
    def create_system_filters(self):
        """Create system-specific filters"""
        filter_widget = QWidget()
        layout = QFormLayout(filter_widget)
        
        # Report Type
        self.report_subtype = QComboBox()
        self.report_subtype.addItems([
            "User Activity Logs",
            "System Error Logs", 
            "Database Audit",
            "Login History",
            "Backup Reports",
            "Performance Metrics",
            "Security Audit"
        ])
        layout.addRow("Report Type:", self.report_subtype)
        
        # Log Level
        self.log_level = QComboBox()
        self.log_level.addItems(["All", "INFO", "WARNING", "ERROR", "CRITICAL"])
        layout.addRow("Log Level:", self.log_level)
        
        # User/Role filter
        self.user_filter = QLineEdit()
        self.user_filter.setPlaceholderText("e.g., admin, manager, All")
        layout.addRow("User/Role:", self.user_filter)
        
        # Module/Component
        self.module_filter = QComboBox()
        self.module_filter.addItems(["All", "Bus Management", "Driver Management", 
                                   "School Management", "Reports", "Billing", "System"])
        layout.addRow("Module:", self.module_filter)
        
        # Minimum severity
        self.min_severity = QComboBox()
        self.min_severity.addItems(["Low", "Medium", "High", "Critical"])
        layout.addRow("Minimum Severity:", self.min_severity)
        
        return filter_widget
    
    def create_log_details_tab(self):
        """Create log details options"""
        log_widget = QWidget()
        layout = QFormLayout(log_widget)
        
        # Log details to include
        details_group = QGroupBox("Include Details:")
        details_layout = QGridLayout(details_group)
        
        self.details = {
            'timestamp': QCheckBox("Timestamp"),
            'user_id': QCheckBox("User ID"),
            'ip_address': QCheckBox("IP Address"),
            'action': QCheckBox("Action Performed"),
            'module': QCheckBox("Module/Component"),
            'status': QCheckBox("Status/Result"),
            'duration': QCheckBox("Duration"),
            'error_message': QCheckBox("Error Message")
        }
        
        for i, (key, checkbox) in enumerate(self.details.items()):
            checkbox.setChecked(True)
            details_layout.addWidget(checkbox, i // 3, i % 3)
        
        layout.addRow(details_group)
        
        # Format options
        self.log_format = QComboBox()
        self.log_format.addItems(["Table", "List", "CSV", "JSON"])
        layout.addRow("Log Format:", self.log_format)
        
        # Include system metrics
        self.include_metrics = QCheckBox("Include System Metrics (CPU, Memory, Disk)")
        self.include_metrics.setChecked(True)
        layout.addRow("", self.include_metrics)
        
        return log_widget
    
    def update_preview(self):
        """Update system report preview"""
        selected_details = [cb.text() for cb in self.details.values() if cb.isChecked()]
        
        preview_text = f"""
SYSTEM REPORT PREVIEW
=====================

Report Name: {self.report_name.text() or 'Unnamed System Report'}
Report Type: {self.report_subtype.currentText()}
Period: {self.start_date.date().toString("dd-MMM-yyyy")} to {self.end_date.date().toString("dd-MMM-yyyy")}

FILTERS:
- Log Level: {self.log_level.currentText()}
- User/Role: {self.user_filter.text() or 'All'}
- Module: {self.module_filter.currentText()}
- Minimum Severity: {self.min_severity.currentText()}

LOG DETAILS INCLUDED ({len(selected_details)}):
{chr(10).join(f"  • {detail}" for detail in selected_details)}

ADDITIONAL OPTIONS:
- Log Format: {self.log_format.currentText()}
- Include System Metrics: {'Yes' if self.include_metrics.isChecked() else 'No'}
- Output Format: {self.format_combo.currentText()}
"""
        self.preview_text.setText(preview_text)
    
    def on_generate(self):
        """Handle generate button click"""
        if self.validate_filters():
            report = self.generate_report()
            self.report_generated.emit(report)
            
            QMessageBox.information(self, "Success", 
                                  f"System report generated!\n\n"
                                  f"Name: {report['name']}\n"
                                  f"Type: {report['subtype']}\n"
                                  f"Format: {report['format']}")
    
    def reset_form(self):
        """Reset form"""
        self.report_name.clear()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.end_date.setDate(QDate.currentDate())
        self.format_combo.setCurrentIndex(0)
        self.report_subtype.setCurrentIndex(0)
        self.log_level.setCurrentIndex(0)
        self.user_filter.clear()
        self.module_filter.setCurrentIndex(0)
        self.min_severity.setCurrentIndex(0)
        for checkbox in self.details.values():
            checkbox.setChecked(True)
        self.log_format.setCurrentIndex(0)
        self.include_metrics.setChecked(True)

# ============================================================================
# MAIN REPORTS DASHBOARD
# ============================================================================

class ReportsDashboard(QWidget):
    """
    Page 1: Reports Dashboard - No CSS Version
    Using only PyQt built-in styling
    """
    
    generate_report = pyqtSignal(str)
    view_report = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 600)
        self.setup_ui()
        self.load_sample_data()

    def setup_ui(self):
        """Setup the UI with no CSS"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 1. Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # 2. Main Content Splitter (Now includes stats on the right)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Report Categories
        left_panel = self.create_report_categories_panel()
        splitter.addWidget(left_panel)
        
        # Right: Vertical splitter for Stats and Recent Reports
        right_splitter = QSplitter(Qt.Vertical)
        
        # Top right: Quick Stats (moved from above)
        stats_widget = self.create_quick_stats()
        right_splitter.addWidget(stats_widget)
        
        # Bottom right: Recent Reports
        right_panel = self.create_recent_reports_panel()
        right_splitter.addWidget(right_panel)
        
        # Set initial sizes for right splitter
        right_splitter.setSizes([200, 400])
        
        splitter.addWidget(right_splitter)
        splitter.setSizes([350, 650])
        main_layout.addWidget(splitter, 1)
        
        # 3. Footer
        footer_widget = self.create_footer_actions()
        main_layout.addWidget(footer_widget)

    def create_header(self):
        """Create header without CSS"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Title
        title_label = QLabel("Reports Dashboard")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        
        # Search area
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search reports...")
        self.search_input.setFixedWidth(200)
        self.search_input.setMinimumHeight(25)
        
        search_btn = QPushButton("Search")
        search_btn.setFixedWidth(80)
        
        search_label = QLabel("Search:")
        search_font = QFont("Segoe UI", 10)
        search_label.setFont(search_font)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(search_widget)
        
        return header_widget

    def create_quick_stats(self):
        """Create quick statistics without CSS"""
        stats_widget = QWidget()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setSpacing(10)
        
        stats_data = [
            ("Reports Generated", "128", "This month"),
            ("Pending Reports", "12", "Awaiting generation"),
            ("Most Popular", "Financial", "25 times this month"),
            ("Scheduled", "8", "Auto-generated reports")
        ]
        
        for i, (title, value, subtitle) in enumerate(stats_data):
            stat_card = self.create_stat_card(title, value, subtitle)
            stats_layout.addWidget(stat_card, i // 2, i % 2)
            
        return stats_widget
        
    def create_stat_card(self, title, value, subtitle):
        """Create a statistic card without CSS"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        card.setLineWidth(2)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Title
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 10, QFont.Bold)
        title_label.setFont(title_font)
        
        # Value
        value_label = QLabel(value)
        value_font = QFont("Segoe UI", 18, QFont.Bold)
        value_label.setFont(value_font)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_font = QFont("Segoe UI", 8)
        subtitle_label.setFont(subtitle_font)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        return card
        
    def create_report_categories_panel(self):
        """Create left panel without CSS"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box | QFrame.Raised)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Panel title
        panel_title = QLabel("Report Categories")
        panel_title_font = QFont("Segoe UI", 12, QFont.Bold)
        panel_title.setFont(panel_title_font)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Categories container
        categories_widget = QWidget()
        categories_layout = QVBoxLayout(categories_widget)
        categories_layout.setSpacing(8)
        
        # Report categories - UPDATED NAMES
        categories = [
            ("Financial Reports", "Generate income, expense, and profit reports", "financial"),
            ("Bus Reports", "Bus utilization, maintenance, and insurance reports", "bus"),
            ("School Reports", "School contracts, billing, and student transport", "school"),
            ("Driver Reports", "Driver performance, salary, and attendance", "driver"),
            ("System Reports", "System logs, user activity, and audit reports", "system"),
        ]
        
        for title, description, report_type in categories:
            category_card = self.create_category_card(title, description, report_type)
            categories_layout.addWidget(category_card)
            
        categories_layout.addStretch()
        scroll.setWidget(categories_widget)
        
        layout.addWidget(panel_title)
        layout.addWidget(scroll)
        
        return panel
        
    def create_category_card(self, title, description, report_type):
        """Create a category card without CSS"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        card.setLineWidth(1)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Title row
        title_row = QHBoxLayout()
        
        title_label = QLabel(title)
        title_font = QFont("Segoe UI", 11, QFont.Bold)
        title_label.setFont(title_font)
        
        arrow_btn = QPushButton(">")
        arrow_btn.setFixedSize(25, 25)
        arrow_btn.clicked.connect(lambda: self.on_category_clicked(report_type))
        
        title_row.addWidget(title_label)
        title_row.addStretch()
        title_row.addWidget(arrow_btn)
        
        # Description
        desc_label = QLabel(description)
        desc_font = QFont("Segoe UI", 9)
        desc_label.setFont(desc_font)
        desc_label.setWordWrap(True)
        
        # Quick actions
        actions_row = QHBoxLayout()
        
        generate_btn = QPushButton("Generate")
        generate_btn.setFixedWidth(80)
        generate_btn.clicked.connect(lambda: self.on_generate_clicked(report_type))
        
        view_btn = QPushButton("View Samples")
        view_btn.setFixedWidth(100)
        view_btn.clicked.connect(lambda: self.view_sample_reports(report_type))
        
        actions_row.addWidget(generate_btn)
        actions_row.addWidget(view_btn)
        actions_row.addStretch()
        
        layout.addLayout(title_row)
        layout.addWidget(desc_label)
        layout.addLayout(actions_row)
        
        return card
        
    def create_recent_reports_panel(self):
        """Create right panel without CSS"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box | QFrame.Raised)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Panel header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        header_title = QLabel("Recent Reports")
        header_font = QFont("Segoe UI", 12, QFont.Bold)
        header_title.setFont(header_font)
        
        # Filter controls
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        
        period_label = QLabel("Period:")
        period_font = QFont("Segoe UI", 9)
        period_label.setFont(period_font)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 7 days", "Last 30 days", "Last 3 months", "This year", "All"])
        self.period_combo.setFixedWidth(120)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFixedWidth(80)
        refresh_btn.clicked.connect(self.load_sample_data)
        
        filter_layout.addWidget(period_label)
        filter_layout.addWidget(self.period_combo)
        filter_layout.addWidget(refresh_btn)
        
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(filter_widget)
        
        # Reports table
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(6)
        self.reports_table.setHorizontalHeaderLabels([
            "Report Name", "Type", "Generated On", "Generated By", "Size", "Actions"
        ])
        
        header = self.reports_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.reports_table.setAlternatingRowColors(True)
        self.reports_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(header_widget)
        layout.addWidget(self.reports_table, 1)
        
        return panel
        
    def create_footer_actions(self):
        """Create footer actions without CSS"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        
        # Quick generate buttons
        quick_widget = QWidget()
        quick_layout = QHBoxLayout(quick_widget)
        
        quick_label = QLabel("Quick Generate:")
        quick_font = QFont("Segoe UI", 10, QFont.Bold)
        quick_label.setFont(quick_font)
        
        quick_buttons = ["Daily Summary", "Weekly Report", "Monthly Financial"]
        
        for text in quick_buttons:
            btn = QPushButton(text)
            btn.setFixedWidth(120)
            quick_layout.addWidget(btn)
            
        quick_layout.addWidget(quick_label)
        for i in range(len(quick_buttons)):
            quick_layout.addWidget(quick_layout.itemAt(i).widget())
            
        # Right side actions
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        
        schedule_btn = QPushButton("Schedule Report")
        schedule_btn.setFixedWidth(120)
        
        export_btn = QPushButton("Export All")
        export_btn.setFixedWidth(100)
        
        clear_btn = QPushButton("Clear History")
        clear_btn.setFixedWidth(100)
        
        right_layout.addWidget(schedule_btn)
        right_layout.addWidget(export_btn)
        right_layout.addWidget(clear_btn)
        
        footer_layout.addWidget(quick_widget)
        footer_layout.addStretch()
        footer_layout.addWidget(right_widget)
        
        return footer_widget
        
    def load_sample_data(self):
        """Load sample data without CSS"""
        sample_reports = [
            ["Monthly Financial Report", "Financial", "2024-01-20 10:30", "admin", "2.4 MB"],
            ["Driver Salary Report", "Driver", "2024-01-19 14:15", "manager", "1.8 MB"],
            ["Bus Utilization Report", "Bus", "2024-01-18 11:45", "admin", "3.1 MB"],
            ["Accounts Receivable", "School", "2024-01-17 16:20", "accountant", "1.2 MB"],
            ["System Activity Log", "System", "2024-01-16 09:30", "admin", "4.2 MB"]
        ]
        
        self.reports_table.setRowCount(len(sample_reports))
        
        for row, report in enumerate(sample_reports):
            for col, data in enumerate(report):
                item = QTableWidgetItem(data)
                
                # Make type column bold
                if col == 1:
                    item_font = QFont("Segoe UI", 9, QFont.Bold)
                    item.setFont(item_font)
                    
                self.reports_table.setItem(row, col, item)
            
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(2, 2, 2, 2)
            
            view_btn = QPushButton("View")
            view_btn.setFixedWidth(50)
            view_btn.clicked.connect(lambda checked, r=row: self.view_report_details(r))
            
            export_btn = QPushButton("Export")
            export_btn.setFixedWidth(50)
            export_btn.clicked.connect(lambda checked, r=row: self.export_report(r))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setFixedWidth(50)
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_report(r))
            
            action_layout.addWidget(view_btn)
            action_layout.addWidget(export_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            self.reports_table.setCellWidget(row, 5, action_widget)
            
    def on_category_clicked(self, report_type):
        """Handle category click"""
        report_names = {
            "financial": "Financial Reports",
            "bus": "Bus Reports", 
            "school": "School Reports",
            "driver": "Driver Reports",
            "system": "System Reports",
        }
        
        QMessageBox.information(self, "Navigate", 
                              f"Opening {report_names.get(report_type, report_type)}")
        self.generate_report.emit(report_type)
        
    def on_generate_clicked(self, report_type):
        """Handle generate click - show appropriate report generator"""
        report_names = {
            "financial": "Financial Report Generator",
            "bus": "Bus Report Generator",
            "school": "School Report Generator",
            "driver": "Driver Report Generator",
            "system": "System Report Generator",
        }
        
        # Create appropriate report generator
        generator = None
        if report_type == "financial":
            generator = FinancialReportGenerator()
        elif report_type == "bus":
            generator = BusReportGenerator()
        elif report_type == "school":
            generator = SchoolReportGenerator()
        elif report_type == "driver":
            generator = DriverReportGenerator()
        elif report_type == "system":
            generator = SystemReportGenerator()
        
        if generator:
            dialog = QDialog(self)
            dialog.setWindowTitle(report_names.get(report_type, "Report Generator"))
            dialog.setMinimumSize(900, 700)
            
            layout = QVBoxLayout(dialog)
            layout.addWidget(generator)
            
            # Connect signals
            generator.report_generated.connect(lambda report: self.on_report_generated(report, dialog))
            
            # Add dialog buttons
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            dialog.exec_()
        else:
            QMessageBox.information(self, "Generate Report", 
                                  f"Generate {report_names.get(report_type, report_type)}?")
    
    def view_sample_reports(self, report_type):
        """View sample reports for a category"""
        report_names = {
            "financial": "Financial Reports",
            "bus": "Bus Reports", 
            "school": "School Reports",
            "driver": "Driver Reports",
            "system": "System Reports",
        }
        
        samples = {
            "financial": [
                "Monthly Income Statement",
                "Quarterly Profit & Loss",
                "Annual Financial Summary"
            ],
            "bus": [
                "Bus Utilization Summary",
                "Maintenance Schedule Report",
                "Fuel Consumption Analysis"
            ],
            "school": [
                "School Contract Status",
                "Monthly Billing Report",
                "Student Transport Analysis"
            ],
            "driver": [
                "Driver Performance Review",
                "Monthly Salary Report",
                "Attendance & Schedule Report"
            ],
            "system": [
                "User Activity Log",
                "System Error Report",
                "Database Backup Report"
            ]
        }
        
        sample_list = samples.get(report_type, ["No samples available"])
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Sample {report_names.get(report_type)}")
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel(f"Sample {report_names.get(report_type)}")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(title)
        
        list_widget = QListWidget()
        for sample in sample_list:
            list_widget.addItem(QListWidgetItem(sample))
        layout.addWidget(list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec_()
    
    def on_report_generated(self, report_data, dialog):
        """Handle when a report is generated"""
        dialog.accept()
        
        # Add to recent reports
        self.add_to_recent_reports(report_data)
        
        # Ask about exporting
        reply = QMessageBox.question(self, "Report Generated",
                                   f"Report '{report_data['name']}' generated successfully!\n\n"
                                   "Would you like to export it now?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.export_generated_report(report_data)
    
    def add_to_recent_reports(self, report_data):
        """Add generated report to recent reports table"""
        row = self.reports_table.rowCount()
        self.reports_table.insertRow(row)
        
        # Add report data
        self.reports_table.setItem(row, 0, QTableWidgetItem(report_data['name']))
        self.reports_table.setItem(row, 1, QTableWidgetItem(report_data['type'].capitalize()))
        self.reports_table.setItem(row, 2, QTableWidgetItem(report_data['date']))
        self.reports_table.setItem(row, 3, QTableWidgetItem("admin"))
        self.reports_table.setItem(row, 4, QTableWidgetItem("1.5 MB"))
        
        # Add action buttons
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(2, 2, 2, 2)
        
        view_btn = QPushButton("View")
        view_btn.setFixedWidth(50)
        view_btn.clicked.connect(lambda: self.view_generated_report(report_data))
        
        export_btn = QPushButton("Export")
        export_btn.setFixedWidth(50)
        export_btn.clicked.connect(lambda: self.export_generated_report(report_data))
        
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedWidth(50)
        delete_btn.clicked.connect(lambda: self.delete_report(row))
        
        action_layout.addWidget(view_btn)
        action_layout.addWidget(export_btn)
        action_layout.addWidget(delete_btn)
        action_layout.addStretch()
        
        self.reports_table.setCellWidget(row, 5, action_widget)
    
    def view_generated_report(self, report_data):
        """View a generated report"""
        # Create a dialog to show report details
        dialog = QDialog(self)
        dialog.setWindowTitle(f"View Report: {report_data['name']}")
        dialog.resize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Report info
        info_text = f"""
REPORT DETAILS
==============

Name: {report_data['name']}
Type: {report_data['type'].capitalize()}
Generated: {report_data['date']}
Period: {report_data.get('period', 'Not specified')}
Format: {report_data.get('format', 'PDF')}

FILTERS APPLIED:
"""
        filters = report_data.get('filters', {})
        if filters:
            for key, value in filters.items():
                info_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        else:
            info_text += "No specific filters applied\n"
        
        if 'summary' in report_data:
            info_text += "\nSUMMARY:\n"
            for key, value in report_data['summary'].items():
                info_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        # Data preview
        if 'data' in report_data and report_data['data']:
            info_text += f"\nDATA PREVIEW ({len(report_data['data'])} records):\n"
            # Show first few records
            for i, record in enumerate(report_data['data'][:3]):
                info_text += f"\nRecord {i+1}:\n"
                for key, value in record.items():
                    info_text += f"  {key.replace('_', ' ').title()}: {value}\n"
            if len(report_data['data']) > 3:
                info_text += f"\n... and {len(report_data['data']) - 3} more records"
        
        text_edit = QTextEdit()
        text_edit.setText(info_text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec_()
    
    def export_generated_report(self, report_data):
        """Export a generated report"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", 
            f"{report_data['name']}.{report_data.get('format', 'pdf').lower()}",
            f"{report_data.get('format', 'PDF')} Files (*.{report_data.get('format', 'pdf').lower()})"
        )
        
        if file_path:
            # In a real app, you would generate the actual file here
            QMessageBox.information(self, "Exported", 
                                  f"Report exported to:\n{file_path}")
            
    def view_report_details(self, row):
        """View report details"""
        report_name = self.reports_table.item(row, 0).text()
        QMessageBox.information(self, "View Report", f"Viewing: {report_name}")
        
    def export_report(self, row):
        """Export a report"""
        report_name = self.reports_table.item(row, 0).text()
        QMessageBox.information(self, "Export", f"Exporting: {report_name}")
        
    def delete_report(self, row):
        """Delete a report"""
        report_name = self.reports_table.item(row, 0).text()
        
        reply = QMessageBox.question(self, "Delete",
                                   f"Delete '{report_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.reports_table.removeRow(row)
            QMessageBox.information(self, "Deleted", "Report deleted")

# ============================================================================
# MAIN TEST FUNCTION
# ============================================================================

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Reports Dashboard Test")
            self.setGeometry(100, 100, 1200, 800)
            
            self.reports_dashboard = ReportsDashboard()
            self.setCentralWidget(self.reports_dashboard)
    
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())