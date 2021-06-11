from sanic_motor import BaseModel


class Movie(BaseModel):
    __coll__ = "movies"


class User(BaseModel):
    __coll__ = "users"

    async def check_email_exists(self):
        pass
