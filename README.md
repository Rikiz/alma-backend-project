# Leads Service (FastAPI with Sync SQLAlchemy)

This service accepts public leads (first name, last name, email, resume), stores them in a DB, saves resume files, and notifies the prospect and an attorney by email. It exposes internal endpoints to list leads and update lead state. Authentication is **not** handled by this service; it should be enforced by a gateway.

## Run (local)

1. Create .env (optional):
```
DATABASE_URL=sqlite:///leads.db
UPLOAD_DIR=./uploads
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=smtp_user
SMTP_PASSWORD=smtp_password
FROM_EMAIL=no-reply@example.com
ATTORNEY_EMAIL=attorney@example.com
```

2. Install dependencies
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start
```
uvicorn app.main:app --reload
```

Public endpoint example (multipart/form-data):

`POST /leads/public` with fields `first_name`, `last_name`, `email` and file field `resume`.

Internal endpoints (protected externally):

- `GET /leads`
- `GET /leads/{id}`
- `PATCH /leads/{id}/state` body `{ "state": "REACHED_OUT" }`
