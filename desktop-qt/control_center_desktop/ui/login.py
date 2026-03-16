from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginView(QWidget):
    logged_in = Signal(str)  # access_token

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Control Center — Login")

        self.api_base_url = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.status = QLabel("")
        self.status.setWordWrap(True)

        self.login_btn = QPushButton("Zaloguj")
        self.login_btn.setDefault(True)

        form = QFormLayout()
        form.addRow("API URL", self.api_base_url)
        form.addRow("Email", self.email)
        form.addRow("Hasło", self.password)

        top = QLabel("Control Center")
        top.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top.setStyleSheet("font-size: 20px; font-weight: 700;")

        footer = QHBoxLayout()
        footer.addStretch(1)
        footer.addWidget(self.login_btn)

        root = QVBoxLayout()
        root.addWidget(top)
        root.addSpacing(6)
        root.addLayout(form)
        root.addWidget(self.status)
        root.addLayout(footer)
        root.addStretch(1)

        self.setLayout(root)

    def set_error(self, message: str) -> None:
        self.status.setStyleSheet("color: #fca5a5;")
        self.status.setText(message)

    def set_info(self, message: str) -> None:
        self.status.setStyleSheet("color: #a7f3d0;")
        self.status.setText(message)

