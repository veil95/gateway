from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegistration(BaseModel):
    username: str
    password_plaintext: str
    display_name: str


