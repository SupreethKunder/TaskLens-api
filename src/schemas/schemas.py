from pydantic import EmailStr, SecretStr, BaseModel
from enum import Enum
from fastapi import Form, Query,Path


class Forbidden(str, Enum):
    a = "Authorization cookies must start with Bearer"
    b = "Authorization cookies must be a Bearer token"
    c = "Forbidden Access"


class Unauthorized(str, Enum):
    a = "Token expired"
    b = "Unauthorized"


class Exception500(BaseModel):
    message: str


class NotFound404(BaseModel):
    message: str = "Not Found"


class Forbidden403(BaseModel):
    detail: Forbidden = "Forbidden Access"


class Unauthorized401(BaseModel):
    message: Unauthorized = "Unauthorized"


class Login200(BaseModel):
    token: str


class Default(BaseModel):
    message: str


class Home200(BaseModel):
    message: str = "This is initial route of Task Monitoring APIs"


class Login403(BaseModel):
    message: str = "Wrong email or password"


class Login401(BaseModel):
    message: str = "Invalid Client ID or Secret"


class Logout200(BaseModel):
    message: str = "Logged out successfully"

class FetchTasksPerIDParams(str, Enum):
    a = "metadata"
    b = "download"



class Login:
    def __init__(
        self,
        email: EmailStr = Form(..., description="Registered Email ID"),
        password: SecretStr = Form(..., description="Password"),
    ):
        self.email = email
        self.password = password

class SignUp:
    def __init__(
        self,
        name: str = Form(..., description="Username"),
        email: EmailStr = Form(..., description="Email ID"),
        password: SecretStr = Form(..., description="Password"),
    ):
        self.name = name
        self.email = email
        self.password = password


class FetchTasks:
    def __init__(
        self,
        page_no: int = Query(..., description="Page Number",ge=1),
        page_size: int = Query(..., description="Page Size"),
    ):
        self.page_no = page_no
        self.page_size = page_size
        

class FetchTasksPerID:
    def __init__(
        self,
        id: str = Path(..., description="Existing Task ID"),
        choice: FetchTasksPerIDParams = Query(..., description="Choice based metadata or download"),
    ):
        self.id = id
        self.choice = choice

        