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

    def clear_report_cards(self):
        from PyQt6.QtCore import QCoreApplication

        while self.parent.report_cards_layout.count():
            child = self.parent.report_cards_layout.takeAt(0)
            if child.widget():
                widget = child.widget()
                widget.setParent(None)
                widget.deleteLater()

        QCoreApplication.processEvents()

    def show_no_reports_message(self):
        from PyQt6.QtWidgets import QLabel
        from PyQt6.QtCore import Qt

        message = QLabel("No reports generated yet.\nRun an algorithm to generate reports.")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 14px;
                padding: 40px;
            }
        """)
        self.parent.report_cards_layout.addWidget(message, 0, 1)

    def load_reports(self):
        self.clear_report_cards()

        report_dir = "output/report"

        if not os.path.exists(report_dir):
            self.show_no_reports_message()
            return

        pdf_files = []
        for root, dirs, files in os.walk(report_dir):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    pdf_files.append(pdf_path)

        if not pdf_files:
            self.show_no_reports_message()
            return

        # sort (newest first)
        pdf_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        for pdf_path in pdf_files:
            card = self.create_report_card(pdf_path)

            row = self.parent.report_cards_layout.count() // 3
            col = self.parent.report_cards_layout.count() % 3
            self.parent.report_cards_layout.addWidget(card, row, col)

    def create_report_card(self, pdf_path):
        filename = os.path.basename(pdf_path).replace('.pdf', '')

        parent_folder = os.path.basename(os.path.dirname(pdf_path))

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
                border-color: #16a34a;
            }
        """)
        
        card_layout = QVBoxLayout()

        card_layout.setSpacing(8)  
        card_layout.setContentsMargins(8, 8, 8, 8)
        
        algo_label = QLabel(algo_name)
        algo_label.setStyleSheet("""
            font-weight: 700;
            font-size: 16px;
            color: #15803d;
            margin-bottom: 2px;
        """)

        input_time_label = QLabel(f"{parent_folder}, {time_format}")
        input_time_label.setStyleSheet("""
        font-weight: 400;
        font-size: 12px;
        color: #666;
        """)

        report_label = QLabel(f"{os.path.basename(pdf_path)}")
        report_label.setStyleSheet("""
        font-weight: 400;
        font-size: 11px;
        color: #888;
        """)

        card_layout.addWidget(algo_label)
        card_layout.addWidget(input_time_label)
        card_layout.addWidget(report_label)

        btn_layout = QHBoxLayout()
        view_btn = QPushButton("View Report")
        view_btn.setStyleSheet("""
            QPushButton {
                background: #16a34a;
                color: white;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 12px;
                margin-left: 4px;
            }
            QPushButton:hover {
                background: #15803d;
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
        except Exception as e:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Failed")
            msg.setText(f"Failed to open PDF:\n{str(e)}")
            msg.setStyleSheet(self.parent.get_message_box_style())
            msg.exec()
    
    def open_pdf_viewer(self, pdf_path):
        try:
            abs_path = os.path.abspath(pdf_path)
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"File not found: {abs_path}")
            os.startfile(abs_path)  # only on Windows
        except Exception as e:
            msg = QMessageBox(self.parent)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Failed to Open PDF")
            msg.setText(f"Failed to open PDF:\n{str(e)}")
            msg.setStyleSheet(self.parent.get_message_box_style())
            msg.exec()

    def open_file_picker(self):
        filename, _ = QFileDialog.getOpenFileName(self.parent, "Open File",
                                       "./input/",
                                       "Text (*.json)")
        
        return filename