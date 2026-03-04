# financial_report_generator.py
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QGridLayout
from report_generator import ReportGenerator

class FinancialReportGenerator(ReportGenerator):
    """Financial Report Generator"""
    
    def __init__(self):
        super().__init__("financial")
        self.init_financial_ui()
        
    def init_financial_ui(self):
        """Initialize financial-specific UI"""
        # Remove default layout and create tabs
        self.layout.removeWidget(self.layout.itemAt(0).widget() if self.layout.count() > 0 else None)
        
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
        
        self.layout.addWidget(tabs)
        
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
        
        self.layout.addLayout(action_layout)
        
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
        # This would connect to your actual database
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