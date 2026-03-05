# reports_dashboard_db.py
# modules/reports_dashboard_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QDateEdit, QComboBox, QLineEdit, QGroupBox, QScrollArea,
    QSplitter, QHeaderView, QMessageBox, QTextEdit,
    QFormLayout, QCheckBox, QSpinBox, QDoubleSpinBox,
    QDialog, QTabWidget, QDialogButtonBox, QFileDialog,
    QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
import json
import csv
from db_connection import DatabaseConnection

class ReportsDashboard(QWidget):
    """Reports Dashboard with Database Integration"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setMinimumSize(1000, 600)
        self.setup_ui()
        self.load_recent_reports()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Report Categories
        left_panel = self.create_categories_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Recent Reports
        right_panel = self.create_recent_reports_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter, 1)
        
        # Footer
        footer_widget = self.create_footer()
        main_layout.addWidget(footer_widget)
    
    def create_header(self):
        """Create header"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Reports Dashboard")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Date range selector
        date_widget = QWidget()
        date_layout = QHBoxLayout(date_widget)
        date_layout.setContentsMargins(0, 0, 0, 0)
        
        date_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        date_layout.addWidget(self.from_date)
        
        date_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.to_date)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(date_widget)
        
        return header
    
    def create_categories_panel(self):
        """Create report categories panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("Report Categories")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Categories
        categories = [
            ("Financial Reports", "Income, expenses, profit/loss", self.open_financial_report),
            ("Bus Reports", "Utilization, maintenance, insurance", self.open_bus_report),
            ("Driver Reports", "Performance, attendance, salary", self.open_driver_report),
            ("School Reports", "Contracts, billing, transport", self.open_school_report),
            ("System Reports", "User activity, logs, audit", self.open_system_report)
        ]
        
        for cat_title, desc, callback in categories:
            card = self.create_category_card(cat_title, desc, callback)
            layout.addWidget(card)
        
        layout.addStretch()
        
        return panel
    
    def create_category_card(self, title, description, callback):
        """Create category card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(callback)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(generate_btn, alignment=Qt.AlignRight)
        
        return card
    
    def create_recent_reports_panel(self):
        """Create recent reports panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Recent Reports")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_recent_reports)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        layout.addWidget(header_widget)
        
        # Reports table
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(5)
        self.reports_table.setHorizontalHeaderLabels([
            "Report Name", "Type", "Generated On", "Format", "Actions"
        ])
        
        header = self.reports_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.reports_table.setAlternatingRowColors(True)
        self.reports_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.reports_table)
        
        return panel
    
    def create_footer(self):
        """Create footer with quick actions"""
        footer = QWidget()
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(0, 0, 0, 0)
        
        quick_label = QLabel("Quick Generate:")
        quick_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(quick_label)
        
        daily_btn = QPushButton("Daily Summary")
        daily_btn.clicked.connect(lambda: self.quick_generate("daily"))
        layout.addWidget(daily_btn)
        
        weekly_btn = QPushButton("Weekly Report")
        weekly_btn.clicked.connect(lambda: self.quick_generate("weekly"))
        layout.addWidget(weekly_btn)
        
        monthly_btn = QPushButton("Monthly Financial")
        monthly_btn.clicked.connect(lambda: self.quick_generate("monthly"))
        layout.addWidget(monthly_btn)
        
        layout.addStretch()
        
        export_all_btn = QPushButton("Export All")
        export_all_btn.clicked.connect(self.export_all_reports)
        layout.addWidget(export_all_btn)
        
        return footer
    
    def load_recent_reports(self):
        """Load recent reports from database"""
        try:
            # Check if reports table exists
            tables = self.db.fetch_all(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='saved_reports'"
            )
            
            if not tables:
                # Create table if it doesn't exist
                self.db.execute_query("""
                    CREATE TABLE IF NOT EXISTS saved_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_name TEXT NOT NULL,
                        report_type TEXT NOT NULL,
                        generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        report_data TEXT,
                        format TEXT,
                        created_by TEXT
                    )
                """)
            
            # Load reports
            reports = self.db.fetch_all("""
                SELECT * FROM saved_reports 
                ORDER BY generated_date DESC 
                LIMIT 20
            """)
            
            self.reports_table.setRowCount(len(reports))
            
            for row, report in enumerate(reports):
                self.reports_table.setItem(row, 0, QTableWidgetItem(report.get('report_name', '')))
                self.reports_table.setItem(row, 1, QTableWidgetItem(report.get('report_type', '')))
                self.reports_table.setItem(row, 2, QTableWidgetItem(report.get('generated_date', '')[:16]))
                self.reports_table.setItem(row, 3, QTableWidgetItem(report.get('format', 'PDF')))
                
                # Actions
                action_widget = self.create_report_actions(row, report['id'])
                self.reports_table.setCellWidget(row, 4, action_widget)
                
        except Exception as e:
            print(f"Error loading reports: {e}")
    
    def create_report_actions(self, row, report_id):
        """Create action buttons for report"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        view_btn = QPushButton("View")
        view_btn.setFixedWidth(50)
        view_btn.clicked.connect(lambda: self.view_report(report_id))
        
        export_btn = QPushButton("Export")
        export_btn.setFixedWidth(50)
        export_btn.clicked.connect(lambda: self.export_report(report_id))
        
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedWidth(50)
        delete_btn.clicked.connect(lambda: self.delete_report(report_id))
        
        layout.addWidget(view_btn)
        layout.addWidget(export_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()
        
        return widget
    
    def open_financial_report(self):
        """Open financial report generator"""
        dialog = ReportGeneratorDialog(self.db, "financial", self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_recent_reports()
    
    def open_bus_report(self):
        """Open bus report generator"""
        dialog = ReportGeneratorDialog(self.db, "bus", self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_recent_reports()
    
    def open_driver_report(self):
        """Open driver report generator"""
        dialog = ReportGeneratorDialog(self.db, "driver", self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_recent_reports()
    
    def open_school_report(self):
        """Open school report generator"""
        dialog = ReportGeneratorDialog(self.db, "school", self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_recent_reports()
    
    def open_system_report(self):
        """Open system report generator"""
        dialog = ReportGeneratorDialog(self.db, "system", self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_recent_reports()
    
    def quick_generate(self, report_type):
        """Generate quick report"""
        if report_type == "daily":
            name = f"Daily Summary - {QDate.currentDate().toString('yyyy-MM-dd')}"
        elif report_type == "weekly":
            name = f"Weekly Report - Week {datetime.date.today().isocalendar()[1]}"
        else:
            name = f"Monthly Financial - {QDate.currentDate().toString('MMMM yyyy')}"
        
        self.save_report(name, "quick", "PDF", {"type": report_type})
        QMessageBox.information(self, "Success", f"Generated: {name}")
    
    def save_report(self, name, report_type, format, data):
        """Save report to database"""
        try:
            report_data = {
                'report_name': name,
                'report_type': report_type,
                'format': format,
                'report_data': json.dumps(data),
                'created_by': 'admin',  # Get from session
                'generated_date': datetime.datetime.now().isoformat()
            }
            
            self.db.insert('saved_reports', report_data)
            self.load_recent_reports()
            
        except Exception as e:
            print(f"Error saving report: {e}")
    
    def view_report(self, report_id):
        """View report details"""
        try:
            report = self.db.fetch_one("SELECT * FROM saved_reports WHERE id = ?", (report_id,))
            if report:
                dialog = ReportViewDialog(report)
                dialog.exec_()
        except Exception as e:
            QMessage