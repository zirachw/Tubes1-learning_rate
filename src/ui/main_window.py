from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
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
        algorithm_list = ["Steepest Ascent Hill Climb", "Sideways Hill Climb", "Stochastic Hill Climb", "Random Restart Hill Climb", "Simulated Annealing", "Genetic Algorithm"]
        self.algorithm_combo_box.addItems(algorithm_list) 
        self.algorithm_combo_box.currentIndexChanged.connect(self.on_algo_selection_changed)
        self.algorithm_combo_box.setStyleSheet("""
            QComboBox {
                color: #000000;
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                min-height: 20px;
            }
            QComboBox:hover {
                border-color: #3b82f6;
            }
            QComboBox:focus {
                border-color: #2563eb;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6b7280;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 4px;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
            }
        """)

        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addWidget(self.algorithm_combo_box)
        main_layout.addLayout(algorithm_layout)
        algo_label = QLabel("Search Algorithm:")
        algo_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #1e40af;
            margin: 10px 0 5px 0;
        """)
        self.params_layout = QVBoxLayout()
        self.algorithm_params()
        self.params_layout.addWidget(self.stochastic_params)
        self.params_layout.addWidget(self.sideways_hill_climb_params)
        self.params_layout.addWidget(self.random_restart_hill_climb_params)
        self.params_layout.addWidget(self.simulated_annealing_params)
        self.params_layout.addWidget(self.genetic_algorithm_params)
        
        algorithm_layout.addLayout(self.params_layout)

        main_layout.addLayout(algorithm_layout)
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


    def algorithm_params(self):
        input_style = """
            QLineEdit{
            color: #000000;
            padding: 8px 12px;
            font-size: 13px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background-color: #ffffff;
            }
            QLineEdit:hover {
                border-color: #3b82f6;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
        """
        
        label_style = "font-size: 13px; color: #000000;"
        
        # Common Paramater
        self.max_iteration_input = QLineEdit()
        self.max_iteration_input.setPlaceholderText("Enter number (e.g., 5)")
        self.max_iteration_input.setText("6")
        max_iteration_validator = QIntValidator(1, 10000, self)
        self.max_iteration_input.setValidator(max_iteration_validator)
        self.max_iteration_input.setStyleSheet(input_style)

        # Stochastic Hill Climbing
        self.stochastic_params = QWidget()
        stochastic_layout = QVBoxLayout()
        stochastic_label = QLabel("Max Iteration:")
        stochastic_label.setStyleSheet(label_style)
        stochastic_layout.addWidget(stochastic_label)
        stochastic_layout.addWidget(self.max_iteration_input)
        self.stochastic_params.setLayout(stochastic_layout)
        self.stochastic_params.hide()

        # Sideways Hill Climbing
        self.sideways_hill_climb_params = QWidget()
        sideways_hill_climb_layout = QVBoxLayout()
        sideways_hill_climb_label = QLabel("Max Sideways Moves:")
        sideways_hill_climb_label.setStyleSheet(label_style)
        self.max_sideways_input = QLineEdit()
        self.max_sideways_input.setPlaceholderText("Enter number (e.g., 5)")
        self.max_sideways_input.setText("6")
        max_sideways_validator = QIntValidator(1, 100, self)
        self.max_sideways_input.setValidator(max_sideways_validator)
        self.max_sideways_input.setStyleSheet(input_style)
        sideways_hill_climb_layout.addWidget(sideways_hill_climb_label)
        sideways_hill_climb_layout.addWidget(self.max_sideways_input)
        self.sideways_hill_climb_params.setLayout(sideways_hill_climb_layout)
        self.sideways_hill_climb_params.hide()


        # Random Restart Hill Climbing
        self.random_restart_hill_climb_params = QWidget()
        random_restart_hill_climb_layout = QVBoxLayout()
        random_restart_hill_climb_label = QLabel("Max Restarts:")
        random_restart_hill_climb_label.setStyleSheet(label_style)
        self.max_restart_input = QLineEdit()
        self.max_restart_input.setPlaceholderText("Enter number (e.g., 5)")
        self.max_restart_input.setText("6")
        max_restart_validator = QIntValidator(1, 100, self)
        self.max_restart_input.setValidator(max_restart_validator)
        self.max_restart_input.setStyleSheet(input_style)
        random_restart_hill_climb_layout.addWidget(random_restart_hill_climb_label)
        random_restart_hill_climb_layout.addWidget(self.max_restart_input)
        self.random_restart_hill_climb_params.setLayout(random_restart_hill_climb_layout)
        self.random_restart_hill_climb_params.hide()


        # Simulated Annealing
        self.simulated_annealing_params = QWidget()
        simulated_annealing_layout = QVBoxLayout()
        
        initial_temp_label = QLabel("Initial Temperature:")
        initial_temp_label.setStyleSheet(label_style)
        self.initial_temp_input = QLineEdit()
        self.initial_temp_input.setPlaceholderText("Enter number (e.g., 1000)")
        self.initial_temp_input.setText("1000")
        initial_temp_validator = QIntValidator(1, 100000, self)
        self.initial_temp_input.setValidator(initial_temp_validator)
        self.initial_temp_input.setStyleSheet(input_style)
        
        cooling_rate_label = QLabel("Cooling Rate:")
        cooling_rate_label.setStyleSheet(label_style)
        self.cooling_rate_input = QLineEdit()
        self.cooling_rate_input.setPlaceholderText("Enter number (e.g., 0.95)")
        self.cooling_rate_input.setText("0.95")
        self.cooling_rate_input.setStyleSheet(input_style)
        
        sa_max_iter_label = QLabel("Max Iterations:")
        sa_max_iter_label.setStyleSheet(label_style)
        self.sa_max_iteration_input = QLineEdit()
        self.sa_max_iteration_input.setPlaceholderText("Enter number (e.g., 150)")
        self.sa_max_iteration_input.setText("150")
        sa_max_iter_validator = QIntValidator(1, 10000, self)
        self.sa_max_iteration_input.setValidator(sa_max_iter_validator)
        self.sa_max_iteration_input.setStyleSheet(input_style)
        
        simulated_annealing_layout.addWidget(initial_temp_label)
        simulated_annealing_layout.addWidget(self.initial_temp_input)
        simulated_annealing_layout.addWidget(cooling_rate_label)
        simulated_annealing_layout.addWidget(self.cooling_rate_input)
        simulated_annealing_layout.addWidget(sa_max_iter_label)
        simulated_annealing_layout.addWidget(self.sa_max_iteration_input)
        self.simulated_annealing_params.setLayout(simulated_annealing_layout)
        self.simulated_annealing_params.hide()

        # Genetic Algorithm
        self.genetic_algorithm_params = QWidget()
        genetic_algorithm_layout = QVBoxLayout()
        
        pop_size_label = QLabel("Population Size:")
        pop_size_label.setStyleSheet(label_style)
        self.population_size_input = QLineEdit()
        self.population_size_input.setPlaceholderText("Enter number (e.g., 8)")
        self.population_size_input.setText("8")
        population_size_validator = QIntValidator(2, 100, self)
        self.population_size_input.setValidator(population_size_validator)
        self.population_size_input.setStyleSheet(input_style)
        
        ga_max_iter_label = QLabel("Max Iterations:")
        ga_max_iter_label.setStyleSheet(label_style)
        self.ga_max_iteration_input = QLineEdit()
        self.ga_max_iteration_input.setPlaceholderText("Enter number (e.g., 150)")
        self.ga_max_iteration_input.setText("150")
        ga_max_iter_validator = QIntValidator(1, 10000, self)
        self.ga_max_iteration_input.setValidator(ga_max_iter_validator)
        self.ga_max_iteration_input.setStyleSheet(input_style)
        
        genetic_algorithm_layout.addWidget(pop_size_label)
        genetic_algorithm_layout.addWidget(self.population_size_input)
        genetic_algorithm_layout.addWidget(ga_max_iter_label)
        genetic_algorithm_layout.addWidget(self.ga_max_iteration_input)
        self.genetic_algorithm_params.setLayout(genetic_algorithm_layout)
        self.genetic_algorithm_params.hide()

    def start_search_ui(self):
        self.search_btn.setEnabled(False)
        self.search_btn.setText("🔍 Searching...")
        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.match_input.setEnabled(False)
    
    def end_search_ui(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("🔍 Search CVs")
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)

    def on_search_completed(self, cv_results):
        try:
            self.end_search_ui()
            print(f"\n=== SEARCH COMPLETED ===")
            print(f"Total CV results: {len(cv_results) if cv_results else 0}")
            if cv_results:
                print(f"Top result: {cv_results[0]['name']} with {cv_results[0]['total_matches']} matches")
            else:
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

        self.stochastic_params.hide()
        self.sideways_hill_climb_params.hide()
        self.random_restart_hill_climb_params.hide()
        self.simulated_annealing_params.hide()
        self.genetic_algorithm_params.hide()

        if selected_text == "Stochastic Hill Climb":
            self.stochastic_params.show()
        elif selected_text == "Random Restart Hill Climb":
            self.random_restart_hill_climb_params.show()
        elif selected_text == "Sideways Hill Climb":
            self.sideways_hill_climb_params.show()
        elif selected_text == "Simulated Annealing":
            self.simulated_annealing_params.show()
        elif selected_text == "Genetic Algorithm":
            self.genetic_algorithm_params.show()