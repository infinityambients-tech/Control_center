# Auto-update (GitHub Releases)

## Co dokładnie działa w MVP
- Desktop sprawdza dostępność nowszej wersji przez backend (`/api/v1/updates/check`).
- Jeśli jest aktualizacja, desktop pobiera wybrany asset przez backend‑proxy (`/api/v1/updates/download?asset=...`) do lokalnego folderu.

Instalacja “na żywo” (podmiana działającej aplikacji) zależy od platformy i sposobu dystrybucji — w tym MVP pobieramy plik instalacyjny/zip i zostawiamy go użytkownikowi.

## GitHub — konfiguracja repozytorium i Releases
1. Utwórz repo na GitHub i wypchnij kod.
2. Upewnij się, że GitHub Actions jest włączone.
3. Release’y budujemy automatycznie po tagu `vX.Y.Z` workflow: `.github/workflows/release-desktop.yml`.
4. Zrób release:
   - `git tag v0.1.0`
   - `git push origin v0.1.0`
5. Workflow doda assety do GitHub Release:
   - Windows: `control_center.exe`
   - macOS: `Control_Center-macos.zip` (zip zawiera `Control_Center.app`)

Ważne:
- Tag powinien być semver: `v1.2.3` (backend akceptuje też bez `v`).
- Assety muszą kończyć się `.exe` (Windows) lub `.zip` (macOS), bo po tym desktop wybiera plik do pobrania.

## Backend — konfiguracja repo
Mechanizm sprawdza GitHub Releases na podstawie ustawienia w DB (priorytet) lub ENV:

- klucz: `github_repo`
- wartość: `owner/repo`

Alternatywnie ENV:
- `GITHUB_REPO=owner/repo` w `control-core/.env`

## Token (zalecane)
Bez tokenu GitHub API ma niski limit (rate limit). Dla prywatnych repo token jest wymagany.

Możesz ustawić:
- DB: `github_token`
- albo ENV: `GITHUB_TOKEN`

Rekomendacja: w środowiskach produkcyjnych ustaw `GITHUB_TOKEN` w sekretach (np. systemu, który uruchamia backend), a nie w DB.

Możesz ustawić przez API (wymaga roli `admin`):
1. zaloguj się i pobierz token JWT
2. wykonaj `PUT /api/v1/settings/github_repo` z body `{"value":"owner/repo"}`
3. (opcjonalnie) wykonaj `PUT /api/v1/settings/github_token` z body `{"value":"<PAT>"}`

## Desktop
Zakładka `Updates` wywołuje endpoint:
- `GET /api/v1/updates/check?current_version=...`

Pobieranie assetu odbywa się przez backend‑proxy:
- `GET /api/v1/updates/download?asset=<asset_name>`
