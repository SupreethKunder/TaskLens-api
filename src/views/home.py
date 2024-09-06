from fastapi import APIRouter
from fastapi.requests import Request
from ..middleware.logging import logger
from ..schemas.responses import (
    API_RESPONSE_MODEL,
)
from ..controllers.home_services import home

router = APIRouter(responses=API_RESPONSE_MODEL)


@router.get("/")
def default(request: Request):
    """
    ```
    Miscellaneous APIs

    The miscellaneous APIs are the APIs that do not logically fall
    in a specific part of the Varanasi SWM API
    ```
    """
    logger.info(
        "%s - %s - %s",
        request.method,
        "public",
        "Default API is being called",
    )
    return home()
