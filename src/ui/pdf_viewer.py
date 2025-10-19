from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel, QScrollArea, 
    QSizePolicy, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt, QUrl, QPointF
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView

class PdfViewerDialog(QDialog):
    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Report Viewer")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        file_name = pdf_path.split('/')[-1]
        header_label = QLabel(f"{file_name}")
        header_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 600;
            color: #1e40af;
            padding: 10px;
        """)
        header_layout.addWidget(header_label)
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)
        self.pdf_view = QPdfView(self)
        self.pdf_view.setPageMode(QPdfView.PageMode.SinglePage)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.pdf_doc = QPdfDocument(self)
        self.pdf_doc.load(pdf_path)
        self.pdf_view.setDocument(self.pdf_doc)
        layout.addWidget(self.pdf_view)
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        prev_btn = QPushButton("Previous Page")
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #334155;
                border: none;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 15px;
                margin-right: 5px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        prev_btn.clicked.connect(self.prev_page)
        next_btn = QPushButton("Next Page")
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 15px;
                margin-left: 5px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        next_btn.clicked.connect(self.next_page)
        nav_layout.addWidget(prev_btn)
        nav_layout.addWidget(next_btn)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        self.setLayout(layout)
    
    def prev_page(self):
        current_page = self.pdf_view.pageNavigator().currentPage()
        if current_page > 0:
            self.pdf_view.pageNavigator().jump(current_page - 1, QPointF(0, 0))
    
    def next_page(self):
        current_page = self.pdf_view.pageNavigator().currentPage()
        if current_page < self.pdf_doc.pageCount() - 1:
            self.pdf_view.pageNavigator().jump(current_page + 1, QPointF(0, 0))