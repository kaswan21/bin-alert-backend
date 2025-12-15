# Bin Alert Backend (FastAPI)

Backend service for bin monitoring:
- Manage bins (thresholds, location)
- Ingest fill level readings (0–100)
- Create alerts with levels: WARNING / FULL
- Suppress duplicate alerts within a 30-minute cooldown

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## API (basic)

- `POST /bins`
- `GET /bins`
- `POST /readings`
- `GET /alerts`
- `PATCH /alerts/{alert_id}`