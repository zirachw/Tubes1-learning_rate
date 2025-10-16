from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QRadioButton, QButtonGroup, QScrollArea, QFrame,
    QCompleter, QCheckBox, QMessageBox, QProgressBar, QGraphicsDropShadowEffect,
    QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QThreadPool, QRunnable, QObject, QTimer
from PyQt6.QtGui import QIntValidator, QIcon

from .ui_handlers import UIHandlers

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.search_worker = None
        self.db_worker = None
        
        self.ui_handlers = UIHandlers(self)
        
        self.init_ui()
        
        self.setWindowTitle("Class Scheduler")
        self.setMinimumSize(800, 400)
        self.resize(1200, 800)
        self.setMinimumSize(800, 400)
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("assets/logo-white.svg"))

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)
        left_panel = QVBoxLayout()
        right_panel = QVBoxLayout()
        title = QLabel("Class Scheduler")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #1e40af;
            margin: 8px 0;
            padding: 8px;
            letter-spacing: -0.5px;
        """)
        left_panel.addWidget(title)
        filepicker_button = QPushButton("Select Input File")
        filepicker_button.clicked.connect(self.open_file_picker)
        filepicker_button.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: 2px solid #6b7280;
                border-left: none;
                border-right: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #4b5563;
                border-color: #4b5563;
                border-left: none;
                border-right: none;
            }
            QPushButton:pressed {
                background-color: #374151;
                border-color: #374151;
                border-left: none;
                border-right: none;
            }
        """)
        self.filepicker_label = QLabel("No Selected File")


        left_panel.addWidget(filepicker_button)
        left_panel.addWidget(self.filepicker_label)
        
        keyword_layout = QVBoxLayout()
        
        keyword_label = QLabel("Keywords :")
        keyword_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 6px;
        """)
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("React, Express, HTML")
        self.keyword_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 20px;
                font-size: 14px;
                border: 2px solid #e5e7eb;
                border-radius: 20px;
                background-color: #ffffff;
                color: #374151;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                background-color: #ffffff;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #93c5fd;
            }
        """)
        
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        left_panel.addLayout(keyword_layout)
        algo_label = QLabel("Search Algorithm:")
        algo_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin: 10px 0 5px 0;
        """)
        
        algo_layout = QHBoxLayout()
        self.kmp_radio = QRadioButton("KMP")
        self.bm_radio = QRadioButton("BM")
        self.ao_radio = QRadioButton("AO")
        self.kmp_radio.setChecked(True)
        
        radio_style = """
            QRadioButton {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #d1d5db;
                border-radius: 9px;
                background-color: #ffffff;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #3b82f6;
                border-radius: 9px;
                background-color: #3b82f6;
            }
        """
        
        self.kmp_radio.setStyleSheet(radio_style)
        self.bm_radio.setStyleSheet(radio_style)
        self.ao_radio.setStyleSheet(radio_style)
        
        algo_group = QButtonGroup()
        algo_group.addButton(self.kmp_radio)
        algo_group.addButton(self.bm_radio)
        algo_group.addButton(self.ao_radio)
        algo_layout.addWidget(self.kmp_radio)
        algo_layout.addWidget(self.bm_radio)
        algo_layout.addWidget(self.ao_radio)
        left_panel.addWidget(algo_label)
        left_panel.addLayout(algo_layout)
        match_label = QLabel("Number of Results to Show:")
        match_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin: 10px 0 5px 0;
        """)
        match_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_container = QHBoxLayout()
        input_container.setSpacing(0)
        self.match_input = QLineEdit()
        self.match_input.setPlaceholderText("Enter number (e.g., 5)")
        self.match_input.setText("6")
        validator = QIntValidator(1, 99, self)
        self.match_input.setValidator(validator)
        self.match_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                font-size: 14px;
                border: 2px ridge #e5e7eb;
                border-radius: 10px;
                background-color: #ffffff;
                color: #374151;
                min-width: 100px;
                max-width: 120px;
            }
            QLineEdit:hover {
                border-color: #93c5fd;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
                outline: none;
            }
        """)
        self.decrement_btn = QPushButton("-")
        self.decrement_btn.setFixedSize(32, 39)
        self.decrement_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: 2px solid #6b7280;
                border-left: none;
                border-right: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #4b5563;
                border-color: #4b5563;
                border-left: none;
                border-right: none;
            }
            QPushButton:pressed {
                background-color: #374151;
                border-color: #374151;
                border-left: none;
                border-right: none;
            }
        """)
        self.increment_btn = QPushButton("+")
        self.increment_btn.setFixedSize(32, 39)
        self.increment_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: 2px solid #3b82f6;
                border-left: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #2563eb;
                border-color: #2563eb;
                border-left: none;
            }
            QPushButton:pressed {
                background-color: #1e40af;
                border-color: #1e40af;
                border-left: none;
            }
        """)
        self.decrement_btn.clicked.connect(self.ui_handlers.decrement_value)
        self.increment_btn.clicked.connect(self.ui_handlers.increment_value)
        input_container.addWidget(self.match_input)
        input_container.addWidget(self.increment_btn)
        input_container.addWidget(self.decrement_btn)
        self.show_all_checkbox = QCheckBox("Show All")
        self.show_all_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #1e40af;
                spacing: 8px;
                margin-left: 8px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #d1d5db;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #3b82f6;
                border-radius: 4px;
                background-color: #3b82f6;
                image: none;
            }
            QCheckBox::indicator:hover {
                border-color: #2563eb;
            }
        """)
        self.show_all_checkbox.toggled.connect(self.ui_handlers.toggle_show_all)
        match_layout = QHBoxLayout()
        match_layout.setSpacing(4)
        match_layout.addWidget(match_label)
        match_layout.addLayout(input_container)
        match_layout.addWidget(self.show_all_checkbox)
        left_panel.addLayout(match_layout)
        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #3b82f6, stop:1 #5b95f5);
                color: white;
                border: none;
                padding: 12px 15px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 22px;
                margin: 8px 0;
            }
            QPushButton:hover {
                background: #2563eb;
            }
            QPushButton:pressed {
                background: #1e40af;
            }            QPushButton:disabled {
                background: #9ca3af;
                color: #ffffff;
            }
        """)
        left_panel.addWidget(self.search_btn)
        
        encryption_layout = QHBoxLayout()
        encrypt_btn = QPushButton("Encrypt Database")
        encrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #f59e0b, stop:1 #d97706);
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 16px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background: #d97706;
            }
            QPushButton:pressed {
                background: #b45309;
            }
        """)
        encryption_layout.addWidget(encrypt_btn)
        decrypt_btn = QPushButton("Decrypt Database")
        decrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #8b5cf6, stop:1 #7c3aed);
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 16px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background: #7c3aed;
            }
            QPushButton:pressed {
                background: #6d28d9;
            }
        """)
        encryption_layout.addWidget(decrypt_btn)
        left_panel.addLayout(encryption_layout)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                text-align: center;
                font-size: 12px;
                font-weight: 600;
                color: #374151;
                background-color: #f9fafb;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #3b82f6, stop: 1 #2563eb);
                border-radius: 8px;
                margin: 2px;
            }
        """)
        left_panel.addWidget(self.progress_bar)
        self.cancel_btn = QPushButton("Cancel Search")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #ef4444, stop:1 #dc2626);
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #dc2626, stop: 1 #b91c1c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #b91c1c, stop: 1 #991b1b);
            }
        """)
        left_panel.addWidget(self.cancel_btn)
        left_panel.addStretch()
        self.runtime_label = QLabel("Total Real Processing Time: -- s")
        self.runtime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.runtime_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #0f172a;
            padding: 10px 12px;
            background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            margin-bottom: 8px;
        """)
        right_panel.addWidget(self.runtime_label)
        self.subtime_container = QWidget()
        self.subtime_layout = QVBoxLayout()
        self.subtime_layout.setContentsMargins(12, 6, 12, 6)
        self.subtime_layout.setSpacing(6)
        self.subtime_container.setLayout(self.subtime_layout)
        self.subtime_container.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 6px;
        """)
        self.runtime_fuzzy_label = QLabel("Fuzzy Search Time: -- s")
        self.runtime_fuzzy_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.runtime_fuzzy_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 500;
            color: #000000;
        """)
        self.subtime_layout.addWidget(self.runtime_fuzzy_label)
        self.runtime_exact_label = QLabel("Exact Search Time: -- s")
        self.runtime_exact_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.runtime_exact_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 500;
            color: #000000;
        """)
        self.subtime_layout.addWidget(self.runtime_exact_label)
        right_panel.addWidget(self.subtime_container)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }            QScrollBar:vertical {
                border: none;
                width: 10px;
                background: #f1f5f9;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                border-radius: 5px;
            }            QScrollBar::handle:vertical:hover {
                background: #2563eb;
            }
        """)
        scroll_content = QWidget()
        self.results_container = QGridLayout(scroll_content)
        self.results_container.setSpacing(12)
        self.results_container.setContentsMargins(12, 12, 12, 12)
        scroll_area.setWidget(scroll_content)
        right_panel.addWidget(scroll_area)
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 4)
        self.setLayout(main_layout)        
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                color: #1e293b;
            }
        """)

    def start_search_ui(self):
        self.search_btn.setEnabled(False)
        self.search_btn.setText("🔍 Searching...")
        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.keyword_input.setEnabled(False)
        self.kmp_radio.setEnabled(False)
        self.bm_radio.setEnabled(False)
        self.ao_radio.setEnabled(False)
        self.match_input.setEnabled(False)
        self.increment_btn.setEnabled(False)
        self.decrement_btn.setEnabled(False)
        self.show_all_checkbox.setEnabled(False)
    
    def end_search_ui(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("🔍 Search CVs")
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.keyword_input.setEnabled(True)
        self.kmp_radio.setEnabled(True)
        self.bm_radio.setEnabled(True)
        self.ao_radio.setEnabled(True)
        checkbox_checked = self.show_all_checkbox.isChecked()
        self.match_input.setEnabled(not checkbox_checked)
        self.increment_btn.setEnabled(not checkbox_checked)
        self.decrement_btn.setEnabled(not checkbox_checked)
        self.show_all_checkbox.setEnabled(True)

    def update_progress(self, current, total, filename):
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"Processing {current}/{total}: {filename}")

    def update_runtime_label(self, seconds):
        self.runtime_label.setText(f"Total Real Processing Time: {seconds:.2f} s")

    def update_fuzzy_runtime_label(self, seconds):
        self.runtime_fuzzy_label.setText(f"Fuzzy Search Time: {seconds:.2f} s")

    def update_exact_runtime_label(self, seconds):
        self.runtime_exact_label.setText(f"Exact Search Time: {seconds:.2f} s")

    def on_search_completed(self, cv_results):
        try:
            self.end_search_ui()
            print(f"\n=== SEARCH COMPLETED ===")
            print(f"Total CV results: {len(cv_results) if cv_results else 0}")
            if cv_results:
                print(f"Top result: {cv_results[0]['name']} with {cv_results[0]['total_matches']} matches")
            else:
                print("No CVs found with matching keywords")
                self.ui_handlers.clear_results_container()
                
        except Exception as e:
            print(f"Error in search completion handler: {e}")
            self.end_search_ui()
            QMessageBox.critical(self, "Search Completion Error", 
                               f"An error occurred while displaying results:\n{str(e)}")
        finally:
            self.cleanup_search_worker()

    def on_search_error(self, error_message):
        try:
            self.end_search_ui()
            if not error_message or error_message.strip() == "":
                error_message = "An unknown error occurred during search"
            print(f"Search error: {error_message}")
            QMessageBox.critical(self, "Search Error", f"An error occurred during search:\n{error_message}")
            self.ui_handlers.clear_results_container()
            error_label = QLabel(f"Search error: {error_message}")
            error_label.setStyleSheet("""
                font-size: 16px;
                color: #ef4444;
                font-weight: 500;
                text-align: center;
                padding: 40px;
            """)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_container.addWidget(error_label, 0, 0, 1, 3)
            
        except Exception as e:
            print(f"Error in search error handler: {e}")
            QMessageBox.critical(self, "Search Error", f"A critical error occurred:\n{str(e)}")
        finally:
            self.cleanup_search_worker()

    def cleanup_search_worker(self):
        if self.search_worker:
            try:
                if self.search_worker.isRunning():
                    self.search_worker.quit()
                    self.search_worker.wait(2000)
                self.search_worker = None
            except Exception as e:
                print(f"Error cleaning up search worker: {e}")

    def on_database_names_updated(self, updated_cv_results):
        print(f"DEBUG: Database worker completed, displaying {len(updated_cv_results)} results")
        self.ui_handlers.display_search_results(updated_cv_results)
        self.cleanup_database_worker()

    def on_database_error(self, error_message):
        print(f"Database worker error: {error_message}")
        print("DEBUG: Continuing with filename-based names")
        
    def on_database_progress(self, progress_message):
        print(f"Database progress: {progress_message}")
        
    def cleanup_database_worker(self):
        if self.db_worker:
            try:
                if self.db_worker.isRunning():
                    self.db_worker.quit()
                    self.db_worker.wait(2000)
                self.db_worker = None
            except Exception as e:
                print(f"Error cleaning up database worker: {e}")

    def clear_results_container(self):
        return self.ui_handlers.clear_results_container()

    def display_search_results(self, cv_results):
        return self.ui_handlers.display_search_results(cv_results)

    def create_search_result_card(self, cv_data):
        return self.ui_handlers.create_search_result_card(cv_data)

    def open_pdf_viewer(self, pdf_path, candidate_name):
        return self.ui_handlers.open_pdf_viewer(pdf_path, candidate_name)

    def open_summary_viewer(self, cv_data):
        return self.ui_handlers.open_summary_viewer(cv_data)

    def open_file_picker(self):
        filename = self.ui_handlers.open_file_picker()
        if filename:
            self.filepicker_label.setText(f"Selected File: {filename}")
        else:
            self.filepicker_label.setText(f"No Selected File")