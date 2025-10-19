import os

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIntValidator, QIcon

from .ui_handlers import UIHandlers


class AlgorithmWorker(QThread):
    finished = pyqtSignal(object, object)  # (algo, result)
    error = pyqtSignal(str)
    
    def __init__(self, algo):
        super().__init__()
        self.algo = algo
    
    def run(self):
        try:
            result = self.algo.search()
            self.finished.emit(self.algo, result)
        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n\n{traceback.format_exc()}"
            self.error.emit(error_msg)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui_handlers = UIHandlers(self)
        self.worker = None  
        self.init_ui()
        self.ui_handlers.load_reports()

        self.setWindowTitle("Class Scheduler")
        self.setMinimumSize(800, 400)
        self.resize(1200, 800)

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                color: #1e293b;
            }
        """)

        main_content_layout = QVBoxLayout()
        main_content_layout.setSpacing(12)
        main_content_layout.setContentsMargins(15, 15, 15, 15)
        
        top_panel = QVBoxLayout()
        
        title = QLabel("Class Scheduler")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #15803d;
            margin: 8px 0;
            padding: 8px;
            letter-spacing: -0.5px;
        """)
        top_panel.addWidget(title)

        input_layout = QHBoxLayout()
        filepicker_button = QPushButton("Select Input File")
        filepicker_button.clicked.connect(self.open_file_picker)
        filepicker_button.setMaximumWidth(200)  
        filepicker_button.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: 2px solid #6b7280;
                border-left: none;
                border-right: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #4b5563;
                border-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #374151;
                border-color: #374151;
            }
        """)
        self.filepicker_label = QLabel("No Selected File")
        self.filepicker_label.setStyleSheet("""
            color: #000000
        """)


        input_layout.addWidget(filepicker_button)
        input_layout.addWidget(self.filepicker_label)
        top_panel.addLayout(input_layout)

        algorithm_layout = QVBoxLayout()
        
        algorithm_label = QLabel("Algorithm :")
        algorithm_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #15803d;
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
                border-color: #16a34a;
            }
            QComboBox:focus {
                border-color: #15803d;
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
                selection-background-color: #16a34a;
                selection-color: #ffffff;
            }
        """)

        algorithm_layout.addWidget(algorithm_label)
        algorithm_layout.addWidget(self.algorithm_combo_box)
        top_panel.addLayout(algorithm_layout)
        algo_label = QLabel("Search Algorithm:")
        algo_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #15803d;
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

        top_panel.addLayout(algorithm_layout)
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.run_algorithm)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #16a34a, stop:1 #22c55e);
                color: white;
                border: none;
                padding: 12px 15px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 22px;
                margin: 8px 0;
            }
            QPushButton:hover {
                background: #15803d;
            }
            QPushButton:pressed {
                background: #15803d;
            }            QPushButton:disabled {
                background: #9ca3af;
                color: #ffffff;
            }
        """)
        top_panel.addWidget(self.search_btn)

        bottom_panel = QVBoxLayout()
        report_title = QLabel("Local Search Report")
        report_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        report_title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 500; 
            color: #15803d;
            margin: 8px 0;
            padding: 8px;
            letter-spacing: -0.5px;
        """)

        bottom_panel.addWidget(report_title)

        report_content_widget = QWidget()
        self.report_cards_layout = QGridLayout(report_content_widget)
        self.report_cards_layout.setSpacing(12)
        self.report_cards_layout.setContentsMargins(12, 12, 12, 12)
        
        bottom_panel.addWidget(report_content_widget)
        
        bottom_panel.addStretch(1)

        main_content_layout.addLayout(top_panel)
        main_content_layout.addLayout(bottom_panel)

        main_content_widget = QWidget()
        main_content_widget.setLayout(main_content_layout)

        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        main_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        main_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll_area.setWidget(main_content_widget)

        main_scroll_area.setStyleSheet("""
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
                background: #16a34a;
                border-radius: 5px;
            }            QScrollBar::handle:vertical:hover {
                background: #15803d;
            }
        """)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(main_scroll_area)


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
                border-color: #16a34a;
            }
            QLineEdit:focus {
                border-color: #15803d;
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

        sa_max_iter_label = QLabel("Max Iterations:")
        sa_max_iter_label.setStyleSheet(label_style)
        self.sa_max_iteration_input = QLineEdit()
        self.sa_max_iteration_input.setPlaceholderText("Enter number (e.g., 150)")
        self.sa_max_iteration_input.setText("150")
        sa_max_iter_validator = QIntValidator(1, 10000, self)
        self.sa_max_iteration_input.setValidator(sa_max_iter_validator)
        self.sa_max_iteration_input.setStyleSheet(input_style)

        sa_note_label = QLabel("Note: Initial temperature and cooling rate are auto-calculated")
        sa_note_label.setStyleSheet(label_style + "font-style: italic; color: #666;")

        simulated_annealing_layout.addWidget(sa_max_iter_label)
        simulated_annealing_layout.addWidget(self.sa_max_iteration_input)
        simulated_annealing_layout.addWidget(sa_note_label)
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
    
    def end_search_ui(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")

    def open_file_picker(self):
        filename = self.ui_handlers.open_file_picker()
        if filename:
            self.filepicker_label.setText(filename)
        else:
            self.filepicker_label.setText(f"No Selected File")
    
    def get_message_box_style(self):
        return """
            QMessageBox {
                background-color: #ffffff;
            }
            QLabel {
                color: #000000;
                font-size: 13px;
            }
            QPushButton {
                background-color: #16a34a;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #15803d;
            }
        """
    
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

    def run_algorithm(self):
        try:
            from src.utils.parse import Parse
            from src.core.state import State
            from src.algorithm.steepest_hill_climbing import SteepestHillClimbing
            from src.algorithm.stochastic_hill_climbing import StochasticHillClimbing
            from src.algorithm.sideways_hill_climbing import SidewaysHillClimbing
            from src.algorithm.random_restart_hill_climbing import RandomRestartHillClimbing
            from src.algorithm.simulated_annealing import SimulatedAnnealing
            from src.algorithm.genetic_algorithm import GeneticAlgorithm
            
            filename = self.filepicker_label.text()
            if filename == "No Selected File":
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("No File Selected")
                msg.setText("Please select an input file first.")
                msg.setStyleSheet(self.get_message_box_style())
                msg.exec()
                return
            filename = filename.replace("Selected File: ", "")

            input_basename = os.path.splitext(os.path.basename(filename))[0]
            self.input_basename = input_basename

            parser = Parse(filename)
            data = parser.loadJson()
            courses, rooms, students = parser.parseAll(data)

            state = State(courses, rooms, students)
            state.initial_state()
            self.initial_objective = state.calculate_objective()
            self.initial_state = state.copy()

            selected_algo = self.algorithm_combo_box.currentText()

            if selected_algo == "Steepest Ascent Hill Climb":
                algo = SteepestHillClimbing(state, input_basename)

            elif selected_algo == "Stochastic Hill Climb":
                max_iter = int(self.max_iteration_input.text())
                algo = StochasticHillClimbing(state, input_basename, max_iteration=max_iter)

            elif selected_algo == "Sideways Hill Climb":
                max_sideways = int(self.max_sideways_input.text())
                algo = SidewaysHillClimbing(state, input_basename, max_sideways=max_sideways)

            elif selected_algo == "Random Restart Hill Climb":
                max_restart = int(self.max_restart_input.text())
                algo = RandomRestartHillClimbing(state, input_basename, max_restart=max_restart)

            elif selected_algo == "Simulated Annealing":
                max_iter = int(self.sa_max_iteration_input.text())
                algo = SimulatedAnnealing(state, input_basename, max_iteration=max_iter)

            elif selected_algo == "Genetic Algorithm":
                pop_size = int(self.population_size_input.text())
                max_iter = int(self.ga_max_iteration_input.text())
                algo = GeneticAlgorithm(state, input_basename, population_size=pop_size,
                                       max_iteration=max_iter)
            
            self.current_algorithm = selected_algo

            self.search_btn.setEnabled(False)
            self.search_btn.setText("Running...")
            self.algorithm_combo_box.setEnabled(False)
            
            self.worker = AlgorithmWorker(algo)
            self.worker.finished.connect(self.on_algorithm_finished)
            self.worker.error.connect(self.on_algorithm_error)
            self.worker.start()
            
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"An error occurred:\n{str(e)}")
            msg.setStyleSheet(self.get_message_box_style())
            msg.exec()
            import traceback
            traceback.print_exc()
    
    def on_algorithm_finished(self, algo, result):
        try:
            from src.utils.pdf_report import generate_pdf_report

            result.visualize()
            algo.print_summary()
            plot_path = algo.plot()

            final_state = result.copy()
            final_objective = result.calculate_objective()
            
            selected_algo = self.algorithm_combo_box.currentText()
            
            extra_image_path = None
            if hasattr(algo, 'extra_plot_filename'):
                extra_image_path = algo.extra_plot_filename
            
            pdf_path = generate_pdf_report(
                algorithm_name=self.current_algorithm,
                initial_state=self.initial_state,
                final_state=final_state,
                initial_objective=self.initial_objective,
                final_objective=final_objective,
                duration=algo.duration,
                iterations=algo.iteration,
                plot_image_path=plot_path,
                extra_image_path=extra_image_path,
                algorithm_instance=algo,
                input_basename=self.input_basename
            )

            self.ui_handlers.load_reports()

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"{selected_algo} completed successfully!\n\nPDF report saved to:\n{pdf_path}")
            msg.setStyleSheet(self.get_message_box_style())
            msg.exec()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Error processing results: {str(e)}")
            msg.setStyleSheet(self.get_message_box_style())
            msg.exec()
        finally:
            self.search_btn.setEnabled(True)
            self.search_btn.setText("Search")
            self.algorithm_combo_box.setEnabled(True)
            self.worker = None
    
    def on_algorithm_error(self, error_msg):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Algorithm Error")
        msg.setText(f"Error occurred:{error_msg}")
        msg.setStyleSheet(self.get_message_box_style())
        msg.exec()
        
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")
        self.algorithm_combo_box.setEnabled(True)
        self.worker = None