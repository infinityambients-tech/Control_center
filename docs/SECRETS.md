# Sekrety i dane wrażliwe

Nie trzymaj haseł i tokenów w repo ani w plikach commitowanych.

## Backend (`control-core`)
Najczęstsze sekrety:
- `SECRET_KEY`
- `SMTP_PASSWORD`
- `GITHUB_TOKEN`
- dane do bazy Postgres w `DATABASE_URL`

### Lokalnie (Windows PowerShell)
Przykład ustawienia na czas sesji:
```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="you@example.com"
$env:SMTP_PASSWORD="app-password"
$env:EMAIL_FROM="you@example.com"
$env:GITHUB_TOKEN="ghp_..."
```

### Produkcja / serwer
Ustaw je w:
- systemie (env vars),
- managerze sekretów (np. GitHub Actions Secrets, Azure Key Vault, 1Password, itp.),
- albo w konfiguracji usługi (Docker/Compose/PM2/systemd).

