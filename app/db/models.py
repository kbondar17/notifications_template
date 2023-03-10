from pydantic import BaseModel, EmailStr, validator


class RegisterForm(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def pass_validator(cls, v):
        assert len(v) > 8
        return v
