from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from control_center_desktop.api import ApiClient, ApiError


class SimpleTablePage(QWidget):
    def __init__(self, title: str, fetch_fn) -> None:
        super().__init__()
        self._fetch_fn = fetch_fn
        self._api: ApiClient | None = None

        self.title = QLabel(title)
        self.title.setStyleSheet("font-size: 16px; font-weight: 700;")

        self.refresh_btn = QPushButton("Odśwież")
        self.refresh_btn.clicked.connect(self.refresh)

        self.status = QLabel("")
        self.status.setWordWrap(True)

        self.table = QTableWidget(0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.status)
        layout.addWidget(self.table, 1)
        self.setLayout(layout)

    def set_api(self, api: ApiClient) -> None:
        self._api = api

    def refresh(self) -> None:
        if not self._api:
            return
        try:
            rows = self._fetch_fn(self._api)
        except ApiError as e:
            self.status.setStyleSheet("color: #fca5a5;")
            self.status.setText(str(e))
            return

        if not isinstance(rows, list):
            rows = [rows]

        columns = []
        for r in rows:
            if isinstance(r, dict):
                for k in r.keys():
                    if k not in columns:
                        columns.append(k)

        self.table.setColumnCount(len(columns))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(columns)

        for i, r in enumerate(rows):
            if not isinstance(r, dict):
                r = {"value": str(r)}
            for j, key in enumerate(columns):
                v = r.get(key)
                self.table.setItem(i, j, QTableWidgetItem("" if v is None else str(v)))

        self.status.setStyleSheet("color: #a7f3d0;")
        self.status.setText(f"Załadowano: {len(rows)}")


def dashboard_fetch(api: ApiClient):
    return api.get("/api/v1/dashboard/summary")


def projects_fetch(api: ApiClient):
    return api.get("/api/v1/projects/")


def companies_fetch(api: ApiClient):
    return api.get("/api/v1/companies/")


def users_fetch(api: ApiClient):
    return api.get("/api/v1/users/")


def plans_fetch(api: ApiClient):
    return api.get("/api/v1/plans/")


def subscriptions_fetch(api: ApiClient):
    return api.get("/api/v1/subscriptions/active")


def invoices_fetch(api: ApiClient):
    return api.get("/api/v1/invoices/")


def deployments_fetch(api: ApiClient):
    return api.get("/api/v1/deployments/")


def settings_fetch(api: ApiClient):
    return api.get("/api/v1/settings/")


def logs_fetch(api: ApiClient):
    return api.get("/api/v1/logs/")


def updates_fetch(api: ApiClient):
    return api.get("/api/v1/updates/check")

