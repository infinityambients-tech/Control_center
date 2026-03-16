from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QWidget,
)

from control_center_desktop.api import ApiClient
from control_center_desktop.ui.pages import (
    SimpleTablePage,
    companies_fetch,
    dashboard_fetch,
    deployments_fetch,
    invoices_fetch,
    logs_fetch,
    plans_fetch,
    projects_fetch,
    settings_fetch,
    subscriptions_fetch,
    users_fetch,
)
from control_center_desktop.ui.updates_page import UpdatesPage


class MainView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Control Center")
        self.resize(1100, 700)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)

        self.stack = QStackedWidget()

        self.pages: list[tuple[str, QWidget]] = [
            ("Dashboard", SimpleTablePage("Dashboard", dashboard_fetch)),
            ("Projects", SimpleTablePage("Projects", projects_fetch)),
            ("Companies", SimpleTablePage("Companies", companies_fetch)),
            ("Users", SimpleTablePage("Users", users_fetch)),
            ("Plans", SimpleTablePage("Plans", plans_fetch)),
            ("Subscriptions", SimpleTablePage("Subscriptions", subscriptions_fetch)),
            ("Invoices", SimpleTablePage("Invoices", invoices_fetch)),
            ("Deployments", SimpleTablePage("Deployments", deployments_fetch)),
            ("Settings", SimpleTablePage("Settings", settings_fetch)),
            ("System Logs", SimpleTablePage("System Logs", logs_fetch)),
            ("Updates", UpdatesPage()),
        ]

        for name, page in self.pages:
            self.sidebar.addItem(QListWidgetItem(name))
            self.stack.addWidget(page)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        layout = QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setLayout(layout)

    def set_api(self, api: ApiClient) -> None:
        for _, page in self.pages:
            if hasattr(page, "set_api"):
                page.set_api(api)  # type: ignore[attr-defined]
        first = self.pages[0][1]
        if hasattr(first, "refresh"):
            first.refresh()  # type: ignore[attr-defined]
