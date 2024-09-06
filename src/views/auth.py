from fastapi import APIRouter, Depends
from ..controllers.authentication_services import (
    login_api,
    signup_api,
    logout_api
)
from ..middleware.logging import logger
from ..middleware.islogin import oauth2_scheme
from ..schemas.schemas import Login,SignUp
from fastapi.responses import JSONResponse
from typing import List
from ..schemas.responses import LOGIN_RESPONSE_MODEL, LOGOUT_RESPONSE_MODEL

router = APIRouter()


@router.post("/login", responses=LOGIN_RESPONSE_MODEL, tags=["Authentication"])
def login(creds: Login = Depends()) -> JSONResponse:
    """
    ```
    This API will authenticate an user
    ```
    """
    logger.info("%s - %s", creds.email, "Login API is being called")
    return login_api(creds.email, creds.password.get_secret_value())

@router.post("/signup", responses=LOGIN_RESPONSE_MODEL, tags=["Authentication"])
def signup(creds: SignUp = Depends()) -> JSONResponse:
    """
    ```
    This API will create an user
    ```
    """
    logger.info("%s - %s", creds.email, "SignUp API is being called")
    return signup_api(creds.name,creds.email, creds.password.get_secret_value())

@router.get("/logout", responses=LOGOUT_RESPONSE_MODEL, tags=["Authentication"])
def logout(token: List = Depends(oauth2_scheme)) -> JSONResponse:
    """
    ```
    This API will revoke the access of an authenticated user
    ```
    """
    logger.info("%s - %s", token[1], "Logout API is being called")
    return logout_api(token)
