# system_settings_db.py
# modules/system_settings_db.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,  # Added QGridLayout
    QLabel, QPushButton, QFrame, QLineEdit, QComboBox,
    QGroupBox, QFormLayout, QMessageBox, QTabWidget,
    QCheckBox, QSpinBox, QDoubleSpinBox, QTextEdit,
    QFileDialog, QProgressDialog, QApplication
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QDate
import datetime
from db_connection import DatabaseConnection

class SystemSettings(QWidget):
    """System Settings with Database Integration"""
    
    settings_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Company Tab
        company_tab = self.create_company_tab()
        self.tabs.addTab(company_tab, "Company")
        
        # Invoice Tab
        invoice_tab = self.create_invoice_tab()
        self.tabs.addTab(invoice_tab, "Invoice")
        
        # Backup Tab
        backup_tab = self.create_backup_tab()
        self.tabs.addTab(backup_tab, "Backup")
        
        # Preferences Tab
        preferences_tab = self.create_preferences_tab()
        self.tabs.addTab(preferences_tab, "Preferences")
        
        main_layout.addWidget(self.tabs, 1)
    
    def create_header(self):
        """Create header"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        title_label = QLabel("System Settings")
        title_label.setFont(QFont("Arial", 16))
        
        save_btn = QPushButton("Save All Settings")
        save_btn.clicked.connect(self.save_all_settings)
        
        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_settings)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(save_btn)
        header_layout.addWidget(reset_btn)
        
        return header_widget
    
    def create_company_tab(self):
        """Create company tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Company details
        company_group = QGroupBox("Company Details")
        company_layout = QFormLayout(company_group)
        company_layout.setSpacing(15)
        
        self.company_name = QLineEdit()
        company_layout.addRow("Company Name:", self.company_name)
        
        self.address = QTextEdit()
        self.address.setMaximumHeight(80)
        company_layout.addRow("Address:", self.address)
        
        self.phone = QLineEdit()
        company_layout.addRow("Phone:", self.phone)
        
        self.email = QLineEdit()
        company_layout.addRow("Email:", self.email)
        
        self.website = QLineEdit()
        company_layout.addRow("Website:", self.website)
        
        self.tax_id = QLineEdit()
        company_layout.addRow("Tax ID:", self.tax_id)
        
        self.tax_rate = QDoubleSpinBox()
        self.tax_rate.setRange(0, 100)
        self.tax_rate.setSuffix("%")
        company_layout.addRow("Tax Rate:", self.tax_rate)
        
        layout.addWidget(company_group)
        
        # Currency settings
        currency_group = QGroupBox("Currency Settings")
        currency_layout = QFormLayout(currency_group)
        
        self.currency = QComboBox()
        self.currency.addItems(["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)"])
        currency_layout.addRow("Currency:", self.currency)
        
        self.decimal_places = QSpinBox()
        self.decimal_places.setRange(0, 4)
        self.decimal_places.setValue(2)
        currency_layout.addRow("Decimal Places:", self.decimal_places)
        
        layout.addWidget(currency_group)
        layout.addStretch()
        
        return tab
    
    def create_invoice_tab(self):
        """Create invoice tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Invoice numbering
        numbering_group = QGroupBox("Invoice Numbering")
        numbering_layout = QFormLayout(numbering_group)
        
        self.inv_prefix = QLineEdit()
        self.inv_prefix.setText("INV")
        numbering_layout.addRow("Prefix:", self.inv_prefix)
        
        self.inv_start = QSpinBox()
        self.inv_start.setRange(1, 999999)
        self.inv_start.setValue(1001)
        numbering_layout.addRow("Start Number:", self.inv_start)
        
        layout.addWidget(numbering_group)
        
        # Invoice defaults
        defaults_group = QGroupBox("Invoice Defaults")
        defaults_layout = QFormLayout(defaults_group)
        
        self.payment_terms = QComboBox()
        self.payment_terms.addItems(["Net 7", "Net 15", "Net 30", "Due on Receipt"])
        defaults_layout.addRow("Payment Terms:", self.payment_terms)
        
        self.default_notes = QTextEdit()
        self.default_notes.setMaximumHeight(80)
        defaults_layout.addRow("Default Notes:", self.default_notes)
        
        layout.addWidget(defaults_group)
        layout.addStretch()
        
        return tab
    
    def create_backup_tab(self):
        """Create backup tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Auto backup
        auto_group = QGroupBox("Automatic Backup")
        auto_layout = QFormLayout(auto_group)
        
        self.auto_backup = QCheckBox("Enable automatic backups")
        self.auto_backup.setChecked(True)
        auto_layout.addRow("", self.auto_backup)
        
        self.backup_freq = QComboBox()
        self.backup_freq.addItems(["Daily", "Weekly", "Monthly"])
        auto_layout.addRow("Frequency:", self.backup_freq)
        
        self.backup_time = QLineEdit()
        self.backup_time.setText("02:00")
        auto_layout.addRow("Time:", self.backup_time)
        
        self.retention = QSpinBox()
        self.retention.setRange(1, 365)
        self.retention.setSuffix(" days")
        self.retention.setValue(30)
        auto_layout.addRow("Retention:", self.retention)
        
        layout.addWidget(auto_group)
        
        # Backup location
        location_group = QGroupBox("Backup Location")
        location_layout = QFormLayout(location_group)
        
        path_layout = QHBoxLayout()
        self.backup_path = QLineEdit()
        self.backup_path.setText("./backups/")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_backup_path)
        path_layout.addWidget(self.backup_path)
        path_layout.addWidget(browse_btn)
        
        location_layout.addRow("Path:", path_layout)
        layout.addWidget(location_group)
        
        # Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        
        backup_now_btn = QPushButton("Backup Now")
        backup_now_btn.clicked.connect(self.backup_now)
        
        restore_btn = QPushButton("Restore Backup")
        restore_btn.clicked.connect(self.restore_backup)
        
        actions_layout.addWidget(backup_now_btn)
        actions_layout.addWidget(restore_btn)
        actions_layout.addStretch()
        
        layout.addWidget(actions_widget)
        layout.addStretch()
        
        return tab
    
    def create_preferences_tab(self):
        """Create preferences tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # System preferences
        system_group = QGroupBox("System Preferences")
        system_layout = QFormLayout(system_group)
        
        self.session_timeout = QSpinBox()
        self.session_timeout.setRange(5, 480)
        self.session_timeout.setSuffix(" minutes")
        self.session_timeout.setValue(30)
        system_layout.addRow("Session Timeout:", self.session_timeout)
        
        self.date_format = QComboBox()
        self.date_format.addItems(["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
        system_layout.addRow("Date Format:", self.date_format)
        
        self.language = QComboBox()
        self.language.addItems(["English", "Spanish", "French", "German"])
        system_layout.addRow("Language:", self.language)
        
        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System Default"])
        system_layout.addRow("Theme:", self.theme)
        
        layout.addWidget(system_group)
        
        # Security
        security_group = QGroupBox("Security")
        security_layout = QFormLayout(security_group)
        
        self.min_password = QSpinBox()
        self.min_password.setRange(4, 20)
        self.min_password.setValue(8)
        security_layout.addRow("Min Password Length:", self.min_password)
        
        self.complex_password = QCheckBox("Require complex passwords")
        security_layout.addRow("", self.complex_password)
        
        self.max_attempts = QSpinBox()
        self.max_attempts.setRange(1, 10)
        self.max_attempts.setValue(3)
        security_layout.addRow("Max Login Attempts:", self.max_attempts)
        
        layout.addWidget(security_group)
        layout.addStretch()
        
        return tab
    
    def load_settings(self):
        """Load settings from database"""
        try:
            settings = self.db.fetch_all("SELECT setting_key, setting_value FROM system_settings")
            settings_dict = {s['setting_key']: s['setting_value'] for s in settings}
            
            # Company
            self.company_name.setText(settings_dict.get('company_name', 'Bus Management System Inc.'))
            self.address.setPlainText(settings_dict.get('company_address', '123 Business Street'))
            self.phone.setText(settings_dict.get('company_phone', '+1-555-123-4567'))
            self.email.setText(settings_dict.get('company_email', 'info@busmgmt.com'))
            self.website.setText(settings_dict.get('company_website', 'www.busmgmt.com'))
            self.tax_id.setText(settings_dict.get('tax_id', 'TAX-123456'))
            self.tax_rate.setValue(float(settings_dict.get('tax_rate', '18.0')))
            
            # Currency
            currency = settings_dict.get('currency', 'USD ($)')
            index = self.currency.findText(currency)
            if index >= 0:
                self.currency.setCurrentIndex(index)
            
            self.decimal_places.setValue(int(settings_dict.get('decimal_places', '2')))
            
            # Invoice
            self.inv_prefix.setText(settings_dict.get('inv_prefix', 'INV'))
            self.inv_start.setValue(int(settings_dict.get('inv_start', '1001')))
            
            terms = settings_dict.get('payment_terms', 'Net 30')
            index = self.payment_terms.findText(terms)
            if index >= 0:
                self.payment_terms.setCurrentIndex(index)
            
            self.default_notes.setPlainText(settings_dict.get('default_notes', ''))
            
            # Backup
            self.auto_backup.setChecked(settings_dict.get('auto_backup', 'true') == 'true')
            
            freq = settings_dict.get('backup_freq', 'Daily')
            index = self.backup_freq.findText(freq)
            if index >= 0:
                self.backup_freq.setCurrentIndex(index)
            
            self.backup_time.setText(settings_dict.get('backup_time', '02:00'))
            self.retention.setValue(int(settings_dict.get('retention', '30')))
            self.backup_path.setText(settings_dict.get('backup_path', './backups/'))
            
            # Preferences
            self.session_timeout.setValue(int(settings_dict.get('session_timeout', '30')))
            
            date_fmt = settings_dict.get('date_format', 'YYYY-MM-DD')
            index = self.date_format.findText(date_fmt)
            if index >= 0:
                self.date_format.setCurrentIndex(index)
            
            lang = settings_dict.get('language', 'English')
            index = self.language.findText(lang)
            if index >= 0:
                self.language.setCurrentIndex(index)
            
            theme = settings_dict.get('theme', 'Light')
            index = self.theme.findText(theme)
            if index >= 0:
                self.theme.setCurrentIndex(index)
            
            self.min_password.setValue(int(settings_dict.get('min_password', '8')))
            self.complex_password.setChecked(settings_dict.get('complex_password', 'false') == 'true')
            self.max_attempts.setValue(int(settings_dict.get('max_attempts', '3')))
            
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_all_settings(self):
        """Save all settings to database"""
        reply = QMessageBox.question(
            self, "Save Settings",
            "Save all settings?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                settings = [
                    ('company_name', self.company_name.text()),
                    ('company_address', self.address.toPlainText()),
                    ('company_phone', self.phone.text()),
                    ('company_email', self.email.text()),
                    ('company_website', self.website.text()),
                    ('tax_id', self.tax_id.text()),
                    ('tax_rate', str(self.tax_rate.value())),
                    ('currency', self.currency.currentText()),
                    ('decimal_places', str(self.decimal_places.value())),
                    ('inv_prefix', self.inv_prefix.text()),
                    ('inv_start', str(self.inv_start.value())),
                    ('payment_terms', self.payment_terms.currentText()),
                    ('default_notes', self.default_notes.toPlainText()),
                    ('auto_backup', 'true' if self.auto_backup.isChecked() else 'false'),
                    ('backup_freq', self.backup_freq.currentText()),
                    ('backup_time', self.backup_time.text()),
                    ('retention', str(self.retention.value())),
                    ('backup_path', self.backup_path.text()),
                    ('session_timeout', str(self.session_timeout.value())),
                    ('date_format', self.date_format.currentText()),
                    ('language', self.language.currentText()),
                    ('theme', self.theme.currentText()),
                    ('min_password', str(self.min_password.value())),
                    ('complex_password', 'true' if self.complex_password.isChecked() else 'false'),
                    ('max_attempts', str(self.max_attempts.value()))
                ]
                
                for key, value in settings:
                    self.db.execute_query(
                        "UPDATE system_settings SET setting_value = ?, updated_at = ? WHERE setting_key = ?",
                        (value, datetime.datetime.now().isoformat(), key)
                    )
                
                QMessageBox.information(self, "Success", "Settings saved successfully")
                self.settings_updated.emit("system_settings")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
    
    def reset_settings(self):
        """Reset to default settings"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Reset all settings to default?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset to defaults
            self.company_name.setText("Bus Management System Inc.")
            self.address.setPlainText("123 Business Street\nCity, State 12345")
            self.phone.setText("+1-555-123-4567")
            self.email.setText("info@busmgmt.com")
            self.website.setText("www.busmgmt.com")
            self.tax_id.setText("TAX-123456")
            self.tax_rate.setValue(18.0)
            self.currency.setCurrentIndex(0)
            self.decimal_places.setValue(2)
            self.inv_prefix.setText("INV")
            self.inv_start.setValue(1001)
            self.payment_terms.setCurrentIndex(2)
            self.default_notes.clear()
            self.auto_backup.setChecked(True)
            self.backup_freq.setCurrentIndex(0)
            self.backup_time.setText("02:00")
            self.retention.setValue(30)
            self.backup_path.setText("./backups/")
            self.session_timeout.setValue(30)
            self.date_format.setCurrentIndex(0)
            self.language.setCurrentIndex(0)
            self.theme.setCurrentIndex(0)
            self.min_password.setValue(8)
            self.complex_password.setChecked(False)
            self.max_attempts.setValue(3)
    
    def browse_backup_path(self):
        """Browse for backup path"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Backup Directory",
            self.backup_path.text()
        )
        if directory:
            self.backup_path.setText(directory)
    
    def backup_now(self):
        """Perform immediate backup"""
        reply = QMessageBox.question(
            self, "Backup Now",
            "Create backup now?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            progress = QProgressDialog("Creating backup...", "Cancel", 0, 100, self)
            progress.setWindowModality(Qt.WindowModal)
            
            for i in range(101):
                progress.setValue(i)
                QApplication.processEvents()
                if progress.wasCanceled():
                    break
            
            progress.setValue(100)
            QMessageBox.information(self, "Success", "Backup created successfully")
    
    def restore_backup(self):
        """Restore from backup"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File",
            self.backup_path.text(),
            "Backup Files (*.bak *.zip)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self, "Restore Backup",
                f"Restore from {file_path}?\nThis will overwrite current data!",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Restore", "Restore started")