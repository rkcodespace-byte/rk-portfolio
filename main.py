
from pathlib import Path
import json
import re
from datetime import datetime, timezone

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
MESSAGES_FILE = DATA_DIR / "messages.jsonl"

app = FastAPI(title="RK Portfolio", version="2.0.0")

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "message": "RK Portfolio API is running!"
    }


@app.post("/api/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    website: str = Form(""),
):
    if website.strip():
        return {
            "ok": True,
            "message": "Thanks! Your message was received."
        }

    name = name.strip()
    email = email.strip()
    subject = subject.strip()
    message = message.strip()

    if not 2 <= len(name) <= 80:
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "message": "Name must be between 2 and 80 characters."
            },
        )

    if len(email) > 254 or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "message": "Please enter a valid email address."
            },
        )

    if not 3 <= len(subject) <= 120:
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "message": "Subject must be between 3 and 120 characters."
            },
        )

    if not 10 <= len(message) <= 3000:
        return JSONResponse(
            status_code=422,
            content={
                "ok": False,
                "message": "Message must be between 10 and 3,000 characters."
            },
        )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }

    with MESSAGES_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "ok": True,
        "message": "Thanks! Your message was saved successfully."
    }
