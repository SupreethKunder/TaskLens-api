from typing import List,Union
from ..database.connect import supabase
from fastapi.responses import JSONResponse,StreamingResponse
from ..middleware.logging import logger
from fastapi.exceptions import HTTPException
from math import ceil
import requests
from ..core.config import settings
from io import StringIO
from os.path import basename

def fetch_tasks_api(auth: List[str], page: int, page_size: int) -> JSONResponse:
    logger.info("%s - %s", auth[1], "Fetch Tasks API function execution starts")
    try:
        total_count = supabase.table("cronjobs").select("id", count="exact").execute()
    except Exception as e:
        print(e)
        logger.error("%s - %s", auth[1], "Error in acquiring total count from Supabase")
        raise HTTPException(status_code=500, detail="Exception Occured")
    start = (page - 1) * page_size
    end = start + page_size - 1
    try:
        items = supabase.table("cronjobs").select("*,systems(systemType,systemName)").range(start, end).execute()
    except Exception as e:
        print(e)
        logger.error("%s - %s", auth[1], "Error in acquiring items from Supabase")
        raise HTTPException(status_code=500, detail="Exception Occured")

    total_items = total_count.count
    total_pages = ceil(total_items / page_size)
    logger.info("%s - %s", auth[1], "Fetch Tasks API function execution completed")
    return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "items": items.data,
    }


def fetch_tasks_per_id_api(auth: List[str], id: str, choice: str) -> Union[JSONResponse,StreamingResponse]:
    logger.info("%s - %s", auth[1], "Fetch Tasks Per ID API function execution starts")
    if choice == "metadata":
        try:
            metadata = supabase.table("cronjobs").select("*,systems(systemType,systemName)").eq("id", id).execute()
            return metadata.data
        except Exception as e:
            print(e)
            logger.error("%s - %s", auth[1], f"Error in acquiring metadata for taskID {id} from Supabase")
            raise HTTPException(status_code=500, detail="Exception Occured")        
    else:
        try:
            logs_path = supabase.table("cronjobs").select("logs_path").eq("id", id).execute().data[0]["logs_path"]         
        except Exception as e:
            print(e)
            logger.error("%s - %s", auth[1], "Error in acquiring total count from Supabase")
            raise HTTPException(status_code=500, detail="Exception Occured")
        if logs_path:
            presigned_url_headers = {
                "Authorization": f"Bearer {settings.SUPABASE_KEY}"
            }
            presigned_url = requests.post(f"{settings.SUPABASE_URL}/storage/v1/object/sign/{settings.SUPABASE_BUCKET}/{logs_path}",headers=presigned_url_headers,json={"expiresIn":600})
            if presigned_url.status_code == 200:
                log_data = requests.get(f"{settings.SUPABASE_URL}/storage/v1{presigned_url.json()["signedURL"]}&download=raw.txt")
                if log_data.status_code == 200:
                    response = StreamingResponse(StringIO(log_data.text), media_type="text/plain")
                    response.headers["Content-Disposition"] = f"attachment; filename={basename(logs_path)}"
                    return response
            else:
                print(presigned_url.json())
                logger.error("%s - %s", auth[1], "Error in acquiring presigned url from Supabase")
                raise HTTPException(status_code=500, detail="Exception Occured")
        else:
            raise HTTPException(status_code=400, detail="No logs found for this taskID")         

