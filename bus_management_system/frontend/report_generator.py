# report_generator.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QLineEdit,
    QDateEdit, QComboBox, QCheckBox, QGroupBox, QFormLayout,
    QSpinBox, QDoubleSpinBox, QScrollArea, QSplitter,
    QHeaderView, QMessageBox, QFileDialog, QDialog, QDialogButtonBox,
    QTabWidget, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
import json

class ReportGenerator(QWidget):
    """Base class for report generation"""
    
    report_generated = pyqtSignal(dict)  # Signal emitted when report is generated
    
    def __init__(self, report_type="generic"):
        super().__init__()
        self.report_type = report_type
        self.report_data = {}
        self.filters = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
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
    
    def create_filter_section(self):
        """Create filter section - to be overridden by subclasses"""
        filter_group = QGroupBox("Filters")
        filter_layout = QVBoxLayout(filter_group)
        
        filter_label = QLabel(f"No specific filters for {self.report_type} report")
        filter_label.setAlignment(Qt.AlignCenter)
        filter_layout.addWidget(filter_label)
        
        return filter_group
    
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
        
    def generate_report(self):
        """Generate the actual report - to be overridden"""
        return {
            'name': self.report_name.text() or f"{self.report_type.capitalize()} Report",
            'type': self.report_type,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'filters': self.filters,
            'data': {}
        }
    
    def validate_filters(self):
        """Validate filters - to be overridden"""
        return True
    
    def get_report_data(self):
        """Get report data from database/mock data - to be overridden"""
        return []