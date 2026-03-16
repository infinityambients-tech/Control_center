from __future__ import annotations


DARK_QSS = """
QWidget { background: #0f1115; color: #e6e6e6; font-size: 12px; }
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
  background: #151923; border: 1px solid #2a2f3a; border-radius: 6px; padding: 6px;
}
QPushButton {
  background: #2563eb; border: 0; border-radius: 6px; padding: 8px 10px; font-weight: 600;
}
QPushButton:hover { background: #1d4ed8; }
QPushButton:disabled { background: #334155; color: #94a3b8; }
QListWidget { background: #0b0d12; border: 1px solid #2a2f3a; border-radius: 8px; }
QListWidget::item { padding: 10px; }
QListWidget::item:selected { background: #1f2937; }
QTableWidget { background: #0b0d12; border: 1px solid #2a2f3a; border-radius: 8px; gridline-color: #2a2f3a; }
QHeaderView::section { background: #0f1115; border: 0; padding: 6px; color: #aab2bf; }
QGroupBox { border: 1px solid #2a2f3a; border-radius: 8px; margin-top: 10px; padding: 10px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; color: #aab2bf; }
"""

