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
        
        self.ui_handlers = UIHandlers(self)
        
        self.init_ui()
        
        self.setWindowTitle("Class Scheduler")
        self.setMinimumSize(800, 400)
        self.resize(1200, 800)
        self.setMinimumSize(800, 400)
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("assets/logo-white.svg"))

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addStretch(1)
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
        main_layout.addWidget(title)
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
        self.filepicker_label.setStyleSheet("""
            color: #000000
        """)

        main_layout.addWidget(filepicker_button)
        main_layout.addWidget(self.filepicker_label)
        
        algorithm_layout = QVBoxLayout()
        
        algorithm_label = QLabel("Algorithm :")
        algorithm_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 6px;
        """)
        self.algorithm_combo_box = QComboBox()
        algorithm_list = ["Steepest Ascent Hill Climb", "Sideways Hill Climb", "Stochastic Hill Climb", "Simulated Annealing", "Genetic Algorithm"]
        self.algorithm_combo_box.addItems(algorithm_list) 
        # self.algorithm_combo_box.currentIndexChanged.connect()
        self.algorithm_combo_box.setStyleSheet("""
            color: #000000
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
        
        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addWidget(self.algorithm_combo_box)
        algorithm_layout.addWidget(self.keyword_input)
        main_layout.addLayout(algorithm_layout)
        algo_label = QLabel("Search Algorithm:")
        algo_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin: 10px 0 5px 0;
        """)
        
        algo_layout = QHBoxLayout()
        
        
        main_layout.addLayout(algo_layout)
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
        main_layout.addWidget(self.search_btn)
        main_layout.addStretch(1)

        
        self.setLayout(main_layout)

    def start_search_ui(self):
        self.search_btn.setEnabled(False)
        self.search_btn.setText("🔍 Searching...")
        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.keyword_input.setEnabled(False)
        self.match_input.setEnabled(False)
    
    def end_search_ui(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("🔍 Search CVs")
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.keyword_input.setEnabled(True)

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


    def display_search_results(self, cv_results):
        return self.ui_handlers.display_search_results(cv_results)

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
    
    def on_algo_selection_changed(self):
        selected_text = self.algorithm_combo_box.currentText()
        self.algorithm_label.setText(f"Selected Algorithm: {selected_text}")