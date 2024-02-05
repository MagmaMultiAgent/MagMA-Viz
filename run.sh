# #!/usr/bin/env bash

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
