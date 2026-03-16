from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from control_center_desktop.api import ApiClient, ApiError
from control_center_desktop.config import DesktopConfig
from control_center_desktop.theme import DARK_QSS
from control_center_desktop.ui.login import LoginView
from control_center_desktop.ui.main_window import MainView


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_QSS)

    cfg = DesktopConfig.load()
    api = ApiClient(base_url=cfg.api_base_url, access_token=cfg.access_token)

    login = LoginView()
    login.api_base_url.setText(cfg.api_base_url)

    main_view = MainView()

    def do_login() -> None:
        api.base_url = login.api_base_url.text().strip() or "http://127.0.0.1:8000"
        email = login.email.text().strip()
        password = login.password.text()
        if not email or not password:
            login.set_error("Podaj email i hasło.")
            return
        try:
            token = api.login(email=email, password=password)
        except ApiError as e:
            login.set_error(str(e))
            return

        cfg.api_base_url = api.base_url
        cfg.access_token = token
        cfg.save()

        main_view.set_api(api)
        main_view.show()
        login.close()

    login.login_btn.clicked.connect(do_login)

    if cfg.access_token:
        # best-effort: try to open main view directly
        try:
            api.get("/api/v1/auth/me")
            main_view.set_api(api)
            main_view.show()
        except Exception:
            login.show()
    else:
        login.show()

    try:
        return app.exec()
    except Exception as e:
        QMessageBox.critical(None, "Control Center", f"Unhandled error: {e}")
        return 1

