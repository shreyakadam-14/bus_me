# bus_report_generator.py
from report_generator import ReportGenerator

class BusReportGenerator(ReportGenerator):
    """Bus Report Generator"""
    
    def __init__(self):
        super().__init__("bus")
        self.init_bus_ui()
        
    def init_bus_ui(self):
        """Initialize bus-specific UI"""
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
        
        self.layout.addWidget(tabs)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.on_generate)
        action_layout.addWidget(generate_btn)
        
        self.layout.addLayout(action_layout)
    
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

METRICS INCLUDED:
{chr(10).join(f"- {cb.text()}" for cb in self.metrics.values() if cb.isChecked())}

DETAIL LEVEL: {self.detail_level.currentText()}
OUTPUT FORMAT: {self.format_combo.currentText()}
"""
        self.preview_text.setText(preview_text)
    
    def on_generate(self):
        """Handle generate button click"""
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
        
        report = self.generate_report()
        self.report_generated.emit(report)
        
        QMessageBox.information(self, "Success", 
                              f"Bus report generated!\n\n"
                              f"Name: {report['name']}\n"
                              f"Type: {report['subtype']}\n"
                              f"Format: {report['format']}")