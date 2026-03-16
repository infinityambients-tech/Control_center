from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from control_center_desktop.api import ApiClient, ApiError
from control_center_desktop.updater import check_update
from control_center_desktop.version import __version__


class UpdatesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._api: ApiClient | None = None
        self._payload: dict | None = None

        title = QLabel("Updates")
        title.setStyleSheet("font-size: 16px; font-weight: 700;")

        self.status = QLabel("")
        self.status.setWordWrap(True)

        self.check_btn = QPushButton("Sprawdź aktualizacje")
        self.download_btn = QPushButton("Pobierz najnowszą")
        self.download_btn.setEnabled(False)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.check_btn)
        btn_row.addWidget(self.download_btn)
        btn_row.addStretch(1)

        info_box = QGroupBox("Wersja")
        info_layout = QVBoxLayout()
        self.current_ver = QLabel(f"Obecna: {__version__}")
        self.latest_ver = QLabel("Najnowsza: —")
        self.repo = QLabel("Repo: —")
        for w in (self.current_ver, self.latest_ver, self.repo):
            w.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        info_layout.addWidget(self.current_ver)
        info_layout.addWidget(self.latest_ver)
        info_layout.addWidget(self.repo)
        info_box.setLayout(info_layout)

        root = QVBoxLayout()
        root.addWidget(title)
        root.addLayout(btn_row)
        root.addWidget(info_box)
        root.addWidget(self.status)
        root.addStretch(1)
        self.setLayout(root)

        self.check_btn.clicked.connect(self.refresh)
        self.download_btn.clicked.connect(self.download)

    def set_api(self, api: ApiClient) -> None:
        self._api = api

    def refresh(self) -> None:
        if not self._api:
            return
        try:
            payload = check_update(self._api)
        except ApiError as e:
            self._payload = None
            self.download_btn.setEnabled(False)
            self.status.setStyleSheet("color: #fca5a5;")
            self.status.setText(str(e))
            return

        # stash api data for backend-proxy download
        payload["_api_base_url"] = self._api.base_url
        payload["_access_token"] = self._api.access_token
        self._payload = payload

        latest = payload.get("latest_version") or "—"
        self.latest_ver.setText(f"Najnowsza: {latest}")
        self.repo.setText("Repo: (ustawione w backendzie: github_repo / GITHUB_REPO)")

        if payload.get("update_available"):
            self.download_btn.setEnabled(True)
            self.status.setStyleSheet("color: #a7f3d0;")
            self.status.setText("Dostępna jest aktualizacja.")
        else:
            self.download_btn.setEnabled(False)
            self.status.setStyleSheet("color: #a7f3d0;")
            self.status.setText("Brak aktualizacji.")

    def download(self) -> None:
        if not self._payload:
            return
        if not self._api:
            return

        try:
            out_dir = Path.home() / "Downloads" / "control_center_updates"
            from control_center_desktop.updater import download_best_asset

            path = download_best_asset(self._payload, out_dir)
        except Exception as e:
            self.status.setStyleSheet("color: #fca5a5;")
            self.status.setText(f"Pobieranie nieudane: {e}")
            return

        self.status.setStyleSheet("color: #a7f3d0;")
        self.status.setText(f"Pobrano do: {path}")

