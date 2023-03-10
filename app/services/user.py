from datetime import datetime, timedelta
import secrets
from string import ascii_letters, digits

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from app.db.schemas import Users, Urls


async def register(email: str, password: str, db: AsyncSession) -> int | None:
    try:
        user = Users(email=email, password=password)
        db.add(user)
        await db.commit()
        return user.id
    except IntegrityError:
        ...


async def make_uuid_for_confirmation_link(user_id: int, db: AsyncSession) -> str:
    url_exists = True
    while url_exists:
        personal_url = "".join(secrets.choice(ascii_letters + digits) for _ in range(9))
        url_exists = await db.execute(
            select(Urls).filter(Urls.url_value == personal_url)
        )
        url_exists = url_exists.fetchone()

    valid_until = datetime.now() + timedelta(days=1)
    user_url = Urls(
        url_value=personal_url,
        user_id=int(user_id),
        valid_untill=valid_until,
        was_visited=False,
        redirectUrl="/success",
    )
    db.add(user_url)
    await db.commit()
    return user_url.url_value
