import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsDropShadowEffect, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from datetime import datetime

from .pdf_viewer import PdfViewerDialog

class UIHandlers:
    def __init__(self, parent):
        self.parent = parent

    def clear_results_container(self):
        while self.parent.results_container.count():
            child = self.parent.results_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_reports(self):
        report_dir = "output/report"

        if not os.path.exists(report_dir):
            return

        pdf_files = [pdf for pdf in os.listdir(report_dir) if pdf.endswith(".pdf")]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(report_dir, pdf_file)
            card = self.create_report_card(pdf_path)

            row = self.parent.report_cards_layout.count() // 3
            col = self.parent.report_cards_layout.count() % 3
            self.parent.report_cards_layout.addWidget(card, row, col)

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

    def create_report_card(self, pdf_path):
        filename = os.path.basename(pdf_path).replace('.pdf', '')

        parts = filename.split('_report_')
        if len(parts) == 2:
            algo_name = parts[0].replace('_', ' ').title()
            timestamp = parts[1]
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                time_format = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_format = timestamp
        else:
            algo_name = "Unknown Algorithm"
            time_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   

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
                padding: 8px;
                border-radius: 8px;
            }
            QFrame:hover {
                background-color: #f8fafc;                
                border-color: #3b82f6;
            }
        """)
        
        card_layout = QVBoxLayout()

        card_layout.setSpacing(8)  
        card_layout.setContentsMargins(8, 8, 8, 8)  # Add margins
        
        algo_label = QLabel(algo_name)
        algo_label.setStyleSheet("""
            font-weight: 700;
            font-size: 16px;
            color: #1e40af;
            margin-bottom: 2px;
        """)
        
        timestamp_label = QLabel(time_format)
        timestamp_label.setStyleSheet("""
        font-weight: 400;
        font-size: 12px;
        """)
        
        path_label = QLabel(f"{os.path.basename(pdf_path)}")
        path_label.setStyleSheet("""
        font-weight: 400;
        font-size: 12px;
        """)

        card_layout.addWidget(algo_label)
        card_layout.addWidget(timestamp_label)
        card_layout.addWidget(path_label)

        btn_layout = QHBoxLayout()
        view_btn = QPushButton("View Report")
        view_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 12px;
                margin-left: 4px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        view_btn.clicked.connect(lambda: self.open_pdf_dialog(pdf_path))
        
        open_btn = QPushButton("Open File")
        open_btn.setStyleSheet("""
            QPushButton {
                background: #D3D3D3;
                color: black;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 12px;
                margin-left: 4px;
            }
            QPushButton:hover {
                background: #808080;
            }
        """)
        open_btn.clicked.connect(lambda: self.open_pdf_viewer(pdf_path))

        btn_layout.addWidget(view_btn)
        btn_layout.addWidget(open_btn)

        card_layout.addLayout(btn_layout)
        card.setLayout(card_layout)
        return card

    def open_pdf_dialog(self, pdf_path):
        try:
            dialog = PdfViewerDialog(pdf_path, self.parent)
            dialog.show()
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Failed")
            msg.setText(f"Failed to open PDF")
            msg.setStyleSheet(self.parent.get_message_box_style())
            msg.exec()
    
    def open_pdf_viewer(self, pdf_path):
        try:
            os.startfile(pdf_path) #Only on windows
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Failed")
            msg.setText(f"Failed to open PDF")
            msg.setStyleSheet(self.parent.get_message_box_style())
            msg.exec()

    def open_file_picker(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open File",
                                       "./input/",
                                       "Text (*.json)")
        
        return filename
