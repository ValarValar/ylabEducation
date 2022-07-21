from pydantic import BaseModel, constr


class PasswordBase(BaseModel):
    password: constr(min_length=3, max_length=40)


class UsernameBase(BaseModel):
    username: constr(min_length=5, max_length=40)


class AuthModel(PasswordBase, UsernameBase):
    pass
