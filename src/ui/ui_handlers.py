import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsDropShadowEffect, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class UIHandlers:
    def __init__(self, parent):
        self.parent = parent

    def clear_results_container(self):
        while self.parent.results_container.count():
            child = self.parent.results_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_search_results(self, cv_results):
        self.clear_results_container()
        if self.parent.show_all_checkbox.isChecked():
            results_to_show = cv_results
        else:
            try:
                num_results = int(self.parent.match_input.text())
                num_results = max(1, min(num_results, 20))
            except ValueError:
                num_results = 6
            results_to_show = cv_results[:num_results]
        for index, cv_data in enumerate(results_to_show):
            row = index // 3
            col = index % 3
            card = self.create_search_result_card(cv_data)
            self.parent.results_container.addWidget(card, row, col)

    def create_search_result_card(self, cv_data):
        card = QFrame()
        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(0, 0, 0, 50))
        effect.setBlurRadius(15)
        effect.setOffset(0, 0)
        card.setGraphicsEffect(effect)

        card.setFixedWidth(300)
        card.setStyleSheet("""
            QFrame {                
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 12px;
                margin: 4px;
            }
            QFrame:hover {
                background-color: #f8fafc;                
                border-color: #3b82f6;
            }
        """)
        
        card_layout = QVBoxLayout()

        card_layout.setSpacing(8)  
        card_layout.setContentsMargins(8, 8, 8, 8)  # Add margins
        
        # Header layout (name and role)
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        
        # Candidate name 
        name_label = QLabel(cv_data['name'])
        name_label.setStyleSheet("""
            font-weight: 700;
            font-size: 16px;
            color: #1e40af;
            margin-bottom: 2px;
        """)
        header_layout.addWidget(name_label)
        
        if cv_data.get('role'):
            role_label = QLabel(f"{cv_data['role']}")
            role_label.setWordWrap(True)
            role_label.setStyleSheet("""
                font-weight: 500;
                font-size: 14px;
                color: #4b5563;
                margin-bottom: 2px;
                line-height: 1.2;
            """)
            header_layout.addWidget(role_label)
        
        match_count_label = QLabel(f"{cv_data['total_matches']} matches")
        match_count_label.setStyleSheet("""
            font-weight: 600;
            font-size: 14px;
            color: #2563eb;
            margin-bottom: 8px;
        """)
        header_layout.addWidget(match_count_label)
        
        card_layout.addLayout(header_layout)

        match_text = "Matched keywords:\n"
        for i, (keyword, count) in enumerate(cv_data['matches'], start=1):
            match_text += f"{i}. {keyword}: {count} occurrence(s)\n"
        match_label = QLabel(match_text)
        match_label.setStyleSheet("""
            color: #64748b;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 12px;
        """)
        card_layout.addWidget(match_label)
        btn_layout = QHBoxLayout()
        summary_btn = QPushButton("Summary")
        summary_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e7ff;
                color: #3730a3;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 15px;
                margin-right: 4px;
            }
            QPushButton:hover {
                background-color: #c7d2fe;
            }
        """)
        summary_btn.clicked.connect(lambda: self.open_summary_viewer(cv_data))
        view_btn = QPushButton("View CV")
        view_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 15px;
                margin-left: 4px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        view_btn.clicked.connect(lambda: self.open_pdf_viewer(cv_data['path'], cv_data['name']))
        btn_layout.addWidget(summary_btn)
        btn_layout.addWidget(view_btn)
        card_layout.addLayout(btn_layout)
        card.setLayout(card_layout)
        return card

    def open_pdf_viewer(self, pdf_path, candidate_name):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        data_dir = os.path.join(project_root, 'data')
        os.makedirs(data_dir, exist_ok=True)
        if not os.path.exists(pdf_path):
            pdf_path = os.path.join(data_dir, "sample_cv.pdf")
            if not os.path.exists(pdf_path):
                QMessageBox.warning(
                    self.parent,
                    "File Not Found",
                    f"PDF file not found:\n{pdf_path}\n\nPlease check that the file exists."
                )
                return


    def increment_value(self):
        try:
            current_value = int(self.parent.match_input.text())
            if current_value < 20:
                self.parent.match_input.setText(str(current_value + 1))
        except ValueError:
            self.parent.match_input.setText("1")

    def decrement_value(self):
        try:
            current_value = int(self.parent.match_input.text())
            if current_value > 1:
                self.parent.match_input.setText(str(current_value - 1))
        except ValueError:
            self.parent.match_input.setText("1")

    def toggle_show_all(self, checked):
        self.parent.match_input.setEnabled(not checked)
        self.parent.increment_btn.setEnabled(not checked)
        self.parent.decrement_btn.setEnabled(not checked)
        if checked:
            self.parent.match_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px 15px;
                    font-size: 14px;
                    border: 2px solid #d1d5db;
                    border-radius: 5px;
                    background-color: #f3f4f6;
                    color: #9ca3af;
                    min-width: 100px;
                    max-width: 120px;
                }
            """)
        else:
            self.parent.match_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px 15px;
                    font-size: 14px;
                    border: 2px solid #e5e7eb;
                    border-radius: 5px;
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
    
    def open_file_picker(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open File",
                                       "./input/",
                                       "Text (*.json)")
        
        return filename
