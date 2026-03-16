# Plugins (MVP)

W folderze `control-core/plugins/` możesz dodawać pliki `*.py`, które eksportują funkcję:

```py
def register(app: fastapi.FastAPI) -> None:
    ...
```

Podczas startu backendu pluginy są automatycznie ładowane.

