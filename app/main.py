import json

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from sqlalchemy.orm import Session

from app.db import RegisterForm, models
from app.db.db_config import engine, get_db, Base
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user as user_service
from app.services.email import queue


app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.post("/register")
async def register(
    user_data: RegisterForm = Depends(RegisterForm), db: AsyncSession = Depends(get_db)
):
    user_id = await user_service.register(user_data.email, user_data.password, db)

    if user_id:
        user_link = await user_service.make_uuid_for_confirmation_link(user_id, db)
        body = json.dumps({"dest_email": user_data.email, "text": user_link})
        # TODO: make async
        queue.add_task(body)
        return "Registered successfully"
    return "Registration error"


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    # TODO: тут примерно накидал, не реализовано
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.get("/success")
def success():
    return "Emailed confirmed!"
