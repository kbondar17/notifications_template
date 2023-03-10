from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey

from app.db.db_config import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    confirmed = Column(Boolean, default=False)


class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    url_value = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    valid_untill = Column(DateTime)
    was_visited = Column(Boolean, default=False)
    redirectUrl = Column(String)
