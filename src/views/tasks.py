from fastapi import APIRouter, Depends
from ..controllers.tasks_services import fetch_tasks_api,fetch_tasks_per_id_api
from ..middleware.logging import logger
from ..middleware.islogin import oauth2_scheme
from ..schemas.schemas import FetchTasks,FetchTasksPerID
from fastapi.responses import JSONResponse
from typing import List
from ..schemas.responses import API_RESPONSE_MODEL

router = APIRouter(prefix="/tasks")

@router.get("/", responses=API_RESPONSE_MODEL, tags=["Tasks"])
def fetch_tasks(payload: FetchTasks = Depends(),token: List = Depends(oauth2_scheme)) -> JSONResponse:
    """
    ```
    This API will acquire all tasks in Supabase Table
    ```
    """
    logger.info("%s - %s", token[1], "Fetch Tasks API is being called")
    return fetch_tasks_api(auth=token,page=payload.page_no,page_size=payload.page_size)

@router.get("/{id}", responses=API_RESPONSE_MODEL, tags=["Tasks"])
def fetch_tasks_per_id(payload: FetchTasksPerID = Depends(),token: List = Depends(oauth2_scheme)) -> JSONResponse:
    """
    ```
    This API will acquire information of a particular task/job in Supabase Table
    ```
    """
    logger.info("%s - %s", token[1], "Fetch Tasks API is being called")
    return fetch_tasks_per_id_api(auth=token,id=payload.id,choice=payload.choice)
