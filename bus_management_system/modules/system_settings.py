from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QGroupBox,
    QFormLayout, QMessageBox, QTabWidget, QCheckBox, QDialog, QDialogButtonBox,
    QDateEdit, QTextEdit, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QInputDialog, QSplitter, QScrollArea, QSpinBox, QDoubleSpinBox,
    QFileDialog, QRadioButton, QButtonGroup, QGridLayout, QProgressDialog, QApplication
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QDate, pyqtSignal
import datetime
import json

class SystemSettings(QWidget):
    """
    7.2 System Settings Module
    """
    
    settings_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_sample_settings()
        
    def setup_ui(self):
        """Setup system settings UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # Main tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Company Information
        company_tab = self.create_company_tab()
        self.tabs.addTab(company_tab, "Company")
        
        # Tab 2: Invoice Settings
        invoice_tab = self.create_invoice_tab()
        self.tabs.addTab(invoice_tab, "Invoice")
        
        # Tab 3: Backup Settings
        backup_tab = self.create_backup_tab()
        self.tabs.addTab(backup_tab, "Backup")
        
        # Tab 4: Preferences
        preferences_tab = self.create_preferences_tab()
        self.tabs.addTab(preferences_tab, "Preferences")
        
        main_layout.addWidget(self.tabs, 1)
        
    def create_header(self):
        """Create header for system settings"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Title
        title_label = QLabel("System Settings")
        title_font = QFont("Segoe UI", 16)
        title_label.setFont(title_font)
        
        # Save button
        save_btn = QPushButton("Save All Settings")
        save_btn.setFixedWidth(150)
        save_btn.clicked.connect(self.save_all_settings)
        
        # Reset button
        reset_btn = QPushButton("Reset to Default")
        reset_btn.setFixedWidth(140)
        reset_btn.clicked.connect(self.reset_settings)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(save_btn)
        header_layout.addWidget(reset_btn)
        
        return header_widget
        
    def create_company_tab(self):
        """Create company information tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(20)
        
        # Company details group
        company_group = QGroupBox("Company Details")
        company_group.setFont(QFont("Segoe UI", 10))
        company_layout = QFormLayout(company_group)
        company_layout.setSpacing(15)
        
        # Company name
        self.company_name_input = QLineEdit()
        self.company_name_input.setPlaceholderText("Enter company name")
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("Enter company address")
        
        # Contact information
        contact_widget = QWidget()
        contact_layout = QGridLayout(contact_widget)
        contact_layout.setContentsMargins(1, 1, 1, 1)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone number")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("Website URL")
        
        contact_layout.addWidget(QLabel("Phone:"), 0, 0)
        contact_layout.addWidget(self.phone_input, 0, 1)
        contact_layout.addWidget(QLabel("Email:"), 1, 0)
        contact_layout.addWidget(self.email_input, 1, 1)
        contact_layout.addWidget(QLabel("Website:"), 2, 0)
        contact_layout.addWidget(self.website_input, 2, 1)
        
        # Tax information
        tax_widget = QWidget()
        tax_layout = QHBoxLayout(tax_widget)
        tax_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tax_id_input = QLineEdit()
        self.tax_id_input.setPlaceholderText("Tax ID/VAT Number")
        
        self.tax_rate_input = QDoubleSpinBox()
        self.tax_rate_input.setRange(0, 100)
        self.tax_rate_input.setSuffix("%")
        self.tax_rate_input.setValue(18.0)
        
        tax_layout.addWidget(QLabel("Tax ID:"))
        tax_layout.addWidget(self.tax_id_input)
        tax_layout.addWidget(QLabel("Tax Rate:"))
        tax_layout.addWidget(self.tax_rate_input)
        tax_layout.addStretch()
        
        # Currency settings
        currency_widget = QWidget()
        currency_layout = QHBoxLayout(currency_widget)
        currency_layout.setContentsMargins(0, 0, 0, 0)
        
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)", "Other"])
        
        self.decimal_places_spin = QSpinBox()
        self.decimal_places_spin.setRange(0, 4)
        self.decimal_places_spin.setValue(2)
        
        currency_layout.addWidget(QLabel("Currency:"))
        currency_layout.addWidget(self.currency_combo)
        currency_layout.addWidget(QLabel("Decimal Places:"))
        currency_layout.addWidget(self.decimal_places_spin)
        currency_layout.addStretch()
        
        company_layout.addRow("Company Name:", self.company_name_input)
        company_layout.addRow("Address:", self.address_input)
        company_layout.addRow("Contact:", contact_widget)
        company_layout.addRow("Tax Information:", tax_widget)
        company_layout.addRow("Currency:", currency_widget)
        
        layout.addWidget(company_group)
        
        # Logo upload section
        logo_group = QGroupBox("Company Logo")
        logo_group.setFont(QFont("Segoe UI", 10))
        logo_layout = QHBoxLayout(logo_group)
        
        # Logo preview
        self.logo_preview = QLabel()
        self.logo_preview.setFixedSize(100, 100)
        self.logo_preview.setFrameStyle(QFrame.Box)
        self.logo_preview.setText("Logo Preview\n(100x100 px)")
        self.logo_preview.setAlignment(Qt.AlignCenter)
        
        # Logo actions
        logo_actions = QWidget()
        logo_actions_layout = QVBoxLayout(logo_actions)
        
        upload_btn = QPushButton("Upload Logo")
        upload_btn.clicked.connect(self.upload_logo)
        
        remove_btn = QPushButton("Remove Logo")
        remove_btn.clicked.connect(self.remove_logo)
        
        size_label = QLabel("Recommended: 150x150 px\nMax size: 2 MB")
        size_label.setFont(QFont("Segoe UI", 8))
        
        logo_actions_layout.addWidget(upload_btn)
        logo_actions_layout.addWidget(remove_btn)
        logo_actions_layout.addWidget(size_label)
        logo_actions_layout.addStretch()
        
        logo_layout.addWidget(self.logo_preview)
        logo_layout.addWidget(logo_actions)
        logo_layout.addStretch()
        
        layout.addWidget(logo_group)
        layout.addStretch()
        
        return tab_widget
        
    def create_invoice_tab(self):
        """Create invoice settings tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(20)
        
        # Invoice numbering
        numbering_group = QGroupBox("Invoice Numbering")
        numbering_group.setFont(QFont("Segoe UI", 10))
        numbering_layout = QFormLayout(numbering_group)
        numbering_layout.setSpacing(15)
        
        # Prefix and format
        prefix_widget = QWidget()
        prefix_layout = QHBoxLayout(prefix_widget)
        prefix_layout.setContentsMargins(0, 0, 0, 0)
        
        self.inv_prefix_input = QLineEdit()
        self.inv_prefix_input.setText("INV")
        self.inv_prefix_input.setFixedWidth(80)
        
        self.inv_start_spin = QSpinBox()
        self.inv_start_spin.setRange(1, 999999)
        self.inv_start_spin.setValue(1001)
        
        self.inv_format_combo = QComboBox()
        self.inv_format_combo.addItems([
            "PREFIX-YYYY-MM-NUMBER",
            "PREFIX/NUMBER/YYYY",
            "NUMBER/YYYY/MM",
            "YYYY/PREFIX/NUMBER"
        ])
        
        prefix_layout.addWidget(QLabel("Prefix:"))
        prefix_layout.addWidget(self.inv_prefix_input)
        prefix_layout.addWidget(QLabel("Start #:"))
        prefix_layout.addWidget(self.inv_start_spin)
        prefix_layout.addWidget(QLabel("Format:"))
        prefix_layout.addWidget(self.inv_format_combo)
        prefix_layout.addStretch()
        
        numbering_layout.addRow("Format:", prefix_widget)
        
        layout.addWidget(numbering_group)
        
        # Invoice defaults
        defaults_group = QGroupBox("Invoice Defaults")
        defaults_group.setFont(QFont("Segoe UI", 10))
        defaults_layout = QFormLayout(defaults_group)
        defaults_layout.setSpacing(15)
        
        # Payment terms
        self.payment_terms_combo = QComboBox()
        self.payment_terms_combo.addItems([
            "Net 7 Days",
            "Net 15 Days", 
            "Net 30 Days",
            "Due on Receipt",
            "Custom"
        ])
        
        # Default notes
        self.default_notes_input = QTextEdit()
        self.default_notes_input.setMaximumHeight(80)
        self.default_notes_input.setPlaceholderText("Default terms and conditions...")
        
        # Late fee settings
        late_fee_widget = QWidget()
        late_fee_layout = QHBoxLayout(late_fee_widget)
        late_fee_layout.setContentsMargins(0, 0, 0, 0)
        
        self.late_fee_check = QCheckBox("Apply late fees")
        self.late_fee_check.setChecked(True)
        
        self.late_fee_rate_input = QDoubleSpinBox()
        self.late_fee_rate_input.setRange(0, 50)
        self.late_fee_rate_input.setSuffix("%")
        self.late_fee_rate_input.setValue(5.0)
        
        late_fee_layout.addWidget(self.late_fee_check)
        late_fee_layout.addWidget(QLabel("Late Fee Rate:"))
        late_fee_layout.addWidget(self.late_fee_rate_input)
        late_fee_layout.addStretch()
        
        defaults_layout.addRow("Payment Terms:", self.payment_terms_combo)
        defaults_layout.addRow("Default Notes:", self.default_notes_input)
        defaults_layout.addRow("Late Fees:", late_fee_widget)
        
        layout.addWidget(defaults_group)
        
        # Invoice template
        template_group = QGroupBox("Invoice Template")
        template_group.setFont(QFont("Segoe UI", 10))
        template_layout = QVBoxLayout(template_group)
        
        # Template selection
        template_selection = QWidget()
        template_selection_layout = QHBoxLayout(template_selection)
        
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "Modern (Default)",
            "Classic",
            "Minimal",
            "Professional"
        ])
        
        preview_btn = QPushButton("Preview Template")
        preview_btn.setFixedWidth(120)
        
        template_selection_layout.addWidget(QLabel("Select Template:"))
        template_selection_layout.addWidget(self.template_combo)
        template_selection_layout.addStretch()
        template_selection_layout.addWidget(preview_btn)
        
        # Template options
        template_options = QWidget()
        template_options_layout = QHBoxLayout(template_options)
        
        self.show_logo_check = QCheckBox("Show Company Logo")
        self.show_logo_check.setChecked(True)
        
        self.show_tax_check = QCheckBox("Show Tax Breakdown")
        self.show_tax_check.setChecked(True)
        
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Blue (Default)", "Green", "Red", "Purple", "Custom"])
        
        template_options_layout.addWidget(self.show_logo_check)
        template_options_layout.addWidget(self.show_tax_check)
        template_options_layout.addWidget(QLabel("Color Scheme:"))
        template_options_layout.addWidget(self.color_combo)
        template_options_layout.addStretch()
        
        template_layout.addWidget(template_selection)
        template_layout.addWidget(template_options)
        
        layout.addWidget(template_group)
        layout.addStretch()
        
        return tab_widget
        
    def create_backup_tab(self):
        """Create backup settings tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(20)
        
        # Automatic backup settings
        auto_backup_group = QGroupBox("Automatic Backups")
        auto_backup_group.setFont(QFont("Segoe UI", 10))
        auto_backup_layout = QFormLayout(auto_backup_group)
        auto_backup_layout.setSpacing(15)
        
        # Enable auto backup
        self.auto_backup_check = QCheckBox("Enable automatic backups")
        self.auto_backup_check.setChecked(True)
        
        # Frequency
        frequency_widget = QWidget()
        frequency_layout = QHBoxLayout(frequency_widget)
        frequency_layout.setContentsMargins(0, 0, 0, 0)
        
        self.backup_frequency_combo = QComboBox()
        self.backup_frequency_combo.addItems([
            "Daily",
            "Weekly",
            "Monthly"
        ])
        
        self.backup_time_input = QLineEdit()
        self.backup_time_input.setText("02:00")
        self.backup_time_input.setFixedWidth(80)
        
        frequency_layout.addWidget(QLabel("Frequency:"))
        frequency_layout.addWidget(self.backup_frequency_combo)
        frequency_layout.addWidget(QLabel("Time:"))
        frequency_layout.addWidget(self.backup_time_input)
        frequency_layout.addStretch()
        
        # Retention period
        self.retention_spin = QSpinBox()
        self.retention_spin.setRange(1, 365)
        self.retention_spin.setSuffix(" days")
        self.retention_spin.setValue(30)
        
        auto_backup_layout.addRow("", self.auto_backup_check)
        auto_backup_layout.addRow("Schedule:", frequency_widget)
        auto_backup_layout.addRow("Retention Period:", self.retention_spin)
        
        layout.addWidget(auto_backup_group)
        
        # Backup location
        location_group = QGroupBox("Backup Location")
        location_group.setFont(QFont("Segoe UI", 10))
        location_layout = QFormLayout(location_group)
        location_layout.setSpacing(15)
        
        # Local backup path
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.backup_path_input = QLineEdit()
        self.backup_path_input.setText("./backups/")
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.browse_backup_path)
        
        path_layout.addWidget(self.backup_path_input)
        path_layout.addWidget(browse_btn)
        
        # Cloud backup options
        self.cloud_backup_check = QCheckBox("Enable cloud backup (Google Drive/Dropbox)")
        
        location_layout.addRow("Local Path:", path_widget)
        location_layout.addRow("", self.cloud_backup_check)
        
        layout.addWidget(location_group)
        
        # Backup content selection
        content_group = QGroupBox("Backup Content")
        content_group.setFont(QFont("Segoe UI", 10))
        content_layout = QVBoxLayout(content_group)
        
        # Checkboxes for different data types
        self.backup_database_check = QCheckBox("Database")
        self.backup_database_check.setChecked(True)
        
        self.backup_documents_check = QCheckBox("Documents & Files")
        self.backup_documents_check.setChecked(True)
        
        self.backup_logs_check = QCheckBox("System Logs")
        
        self.backup_config_check = QCheckBox("Configuration Files")
        self.backup_config_check.setChecked(True)
        
        # Compress backup
        self.compress_check = QCheckBox("Compress backups (ZIP)")
        self.compress_check.setChecked(True)
        
        content_layout.addWidget(self.backup_database_check)
        content_layout.addWidget(self.backup_documents_check)
        content_layout.addWidget(self.backup_logs_check)
        content_layout.addWidget(self.backup_config_check)
        content_layout.addWidget(self.compress_check)
        
        layout.addWidget(content_group)
        
        # Quick actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        
        backup_now_btn = QPushButton("🚀 Backup Now")
        backup_now_btn.setFixedWidth(120)
        backup_now_btn.clicked.connect(self.backup_now)
        
        restore_btn = QPushButton("🔄 Restore Backup")
        restore_btn.setFixedWidth(140)
        restore_btn.clicked.connect(self.restore_backup)
        
        view_backups_btn = QPushButton("📁 View Backups")
        view_backups_btn.setFixedWidth(120)
        
        actions_layout.addWidget(backup_now_btn)
        actions_layout.addWidget(restore_btn)
        actions_layout.addWidget(view_backups_btn)
        actions_layout.addStretch()
        
        layout.addWidget(actions_widget)
        layout.addStretch()
        
        return tab_widget
        
    def create_preferences_tab(self):
        """Create system preferences tab"""
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setSpacing(20)
        
        # System preferences
        system_group = QGroupBox("System Preferences")
        system_group.setFont(QFont("Segoe UI", 10))
        system_layout = QFormLayout(system_group)
        system_layout.setSpacing(15)
        
        # Session timeout
        self.session_timeout_spin = QSpinBox()
        self.session_timeout_spin.setRange(5, 480)
        self.session_timeout_spin.setSuffix(" minutes")
        self.session_timeout_spin.setValue(30)
        
        # Date format
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems([
            "YYYY-MM-DD",
            "DD/MM/YYYY",
            "MM/DD/YYYY",
            "DD-MMM-YYYY"
        ])
        
        # Default language
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Spanish",
            "French",
            "German",
            "Hindi"
        ])
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Light Theme",
            "Dark Theme",
            "Blue Theme",
            "Auto (System)"
        ])
        
        system_layout.addRow("Session Timeout:", self.session_timeout_spin)
        system_layout.addRow("Date Format:", self.date_format_combo)
        system_layout.addRow("Language:", self.language_combo)
        system_layout.addRow("Theme:", self.theme_combo)
        
        layout.addWidget(system_group)
        
        """# Email notifications
        email_group = QGroupBox("Email Notifications")
        email_group.setFont(QFont("Segoe UI", 10))
        email_layout = QVBoxLayout(email_group)
        
        # Email settings
        email_settings = QWidget()
        email_settings_layout = QFormLayout(email_settings)
        
        self.smtp_host_input = QLineEdit()
        self.smtp_host_input.setPlaceholderText("smtp.gmail.com")
        
        self.smtp_port_input = QLineEdit()
        self.smtp_port_input.setPlaceholderText("587")
        
        self.smtp_user_input = QLineEdit()
        self.smtp_user_input.setPlaceholderText("your-email@gmail.com")
        
        email_settings_layout.addRow("SMTP Host:", self.smtp_host_input)
        email_settings_layout.addRow("SMTP Port:", self.smtp_port_input)
        email_settings_layout.addRow("Username:", self.smtp_user_input)
        
        email_layout.addWidget(email_settings)
        
        # Notification types
        notification_widget = QWidget()
        notification_layout = QVBoxLayout(notification_widget)
        
        self.notify_login_check = QCheckBox("Notify on user login")
        self.notify_backup_check = QCheckBox("Notify on backup completion")
        self.notify_error_check = QCheckBox("Notify on system errors")
        
        notification_layout.addWidget(self.notify_login_check)
        notification_layout.addWidget(self.notify_backup_check)
        notification_layout.addWidget(self.notify_error_check)
        
        email_layout.addWidget(notification_widget)
        
        layout.addWidget(email_group)
        """
        # Security settings
        security_group = QGroupBox("Security Settings")
        security_group.setFont(QFont("Segoe UI", 10))
        security_layout = QVBoxLayout(security_group)
        
        # Password policy
        policy_widget = QWidget()
        policy_layout = QFormLayout(policy_widget)
        
        self.min_password_spin = QSpinBox()
        self.min_password_spin.setRange(4, 20)
        self.min_password_spin.setValue(8)
        
        self.password_complexity_check = QCheckBox("Require complex passwords")
        
        policy_layout.addRow("Minimum Length:", self.min_password_spin)
        policy_layout.addRow("", self.password_complexity_check)
        
        # Login security
        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        
        self.two_factor_check = QCheckBox("Enable Two-Factor Authentication")
        self.login_attempts_spin = QSpinBox()
        self.login_attempts_spin.setRange(1, 10)
        self.login_attempts_spin.setValue(3)
        
        login_layout.addWidget(self.two_factor_check)
        login_layout.addWidget(QLabel("Max Login Attempts:"))
        login_layout.addWidget(self.login_attempts_spin)
        
        security_layout.addWidget(policy_widget)
        security_layout.addWidget(login_widget)
        
        layout.addWidget(security_group)
        layout.addStretch()
        
        return tab_widget
        
    def load_sample_settings(self):
        """Load sample settings"""
        self.company_name_input.setText("Bus Management System Inc.")
        self.address_input.setText("123 Business Street\nCity, State 12345\nCountry")
        self.phone_input.setText("+1 (555) 123-4567")
        self.email_input.setText("info@busmanagement.com")
        self.website_input.setText("www.busmanagement.com")
        self.tax_id_input.setText("TAX-123456789")
        
    def upload_logo(self):
        """Upload company logo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_preview.setPixmap(scaled_pixmap)
                self.logo_preview.setText("")
                QMessageBox.information(self, "Success", "Logo uploaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to load image!")
                
    def remove_logo(self):
        """Remove company logo"""
        self.logo_preview.clear()
        self.logo_preview.setText("Logo Preview\n(150x150 px)")
        
    def browse_backup_path(self):
        """Browse for backup path"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Backup Directory",
            self.backup_path_input.text()
        )
        
        if directory:
            self.backup_path_input.setText(directory)
            
    def backup_now(self):
        """Perform immediate backup"""
        reply = QMessageBox.question(
            self,
            "Backup Now",
            "Create a backup of the system now?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Simulate backup process
            progress_dialog = QProgressDialog("Creating backup...", "Cancel", 0, 100, self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            
            for i in range(101):
                progress_dialog.setValue(i)
                QApplication.processEvents()
                import time
                time.sleep(0.02)
                
            progress_dialog.setValue(100)
            QMessageBox.information(self, "Backup Complete", "System backup created successfully!")
            
    def restore_backup(self):
        """Restore from backup"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup File",
            self.backup_path_input.text(),
            "Backup Files (*.bak *.zip);;All Files (*.*)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self,
                "Restore Backup",
                f"Restore system from backup?\n\nFile: {file_path}\n\nWarning: This will overwrite current data!",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                QMessageBox.information(self, "Restore Started", "Restoration process has started...")
                
    def save_all_settings(self):
        """Save all settings"""
        reply = QMessageBox.question(
            self,
            "Save Settings",
            "Save all system settings?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Simulate save process
            settings = {
                "company": {
                    "name": self.company_name_input.text(),
                    "tax_id": self.tax_id_input.text(),
                    "tax_rate": self.tax_rate_input.value()
                },
                "invoice": {
                    "prefix": self.inv_prefix_input.text(),
                    "start_number": self.inv_start_spin.value()
                },
                "backup": {
                    "auto_backup": self.auto_backup_check.isChecked(),
                    "frequency": self.backup_frequency_combo.currentText(),
                    "path": self.backup_path_input.text()
                },
                "preferences": {
                    "session_timeout": self.session_timeout_spin.value(),
                    "theme": self.theme_combo.currentText()
                }
            }
            
            QMessageBox.information(self, "Settings Saved", "All settings have been saved successfully!")
            self.settings_updated.emit("system_settings")
            
    def reset_settings(self):
        """Reset all settings to default"""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.load_sample_settings()
            
            # Reset other tabs
            self.auto_backup_check.setChecked(True)
            self.backup_frequency_combo.setCurrentIndex(0)
            self.session_timeout_spin.setValue(30)
            
            QMessageBox.information(self, "Settings Reset", "All settings have been reset to default values!")