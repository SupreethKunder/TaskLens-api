from typing import List
from ..database.connect import redis_client, supabase
from datetime import timedelta
from fastapi.responses import JSONResponse
from ..middleware.logging import logger
from fastapi import status
from redis.exceptions import RedisError

def signup_api(username: str, email: str, password: str) -> JSONResponse:
    """SignUp API to grant access to user"""

    logger.info(f"{email} - SignUp function execution starts")
    try:
        existing_user = supabase.table("authorized_access").select("*").eq("email", email).execute()

        if existing_user.data and len(existing_user.data) > 0:
            logger.warning(f"{email} - User already exists")
            return JSONResponse(
                content={"message": "User already exists"},
                status_code=status.HTTP_409_CONFLICT,
            )
            
        supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        supabase.table("authorized_access").insert({
            "username": username,
            "email": email,
            "password": password
        }).execute()

        
    except Exception as e:
        logger.error(f"{email} - SignUp API failed: {str(e)}")
        return JSONResponse(
            content={"message": "Invalid sign up credentials"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    logger.info(f"{email} - SignUp function execution complete")
    return JSONResponse(content={"message": "User created successfully"})


def login_api(email: str, password: str) -> JSONResponse:
    """Login API to grant access to user"""

    logger.info(f"{email} - Login function execution starts")
    try:
        user_data = supabase.table("authorized_access").select("*").eq("email", email).execute()

        if len(user_data.data) == 0:
            logger.warning(f"{email} - No user exist(s)")
            return JSONResponse(
                content={"message": "User not found"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        if len(user_data.data) > 0 and not user_data.data[0]["isAuthorized"]:
            print(user_data.data[0]["isAuthorized"])
            logger.warning(f"{email} - Unauthorized access attempt")
            return JSONResponse(
                content={"message": "Forbidden access"},
                status_code=status.HTTP_403_FORBIDDEN,
            )
            
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        access_token = response.session.access_token

    except Exception as e:
        logger.error(f"{email} - Login API failed: {str(e)}")
        return JSONResponse(
            content={"message": "Invalid login credentials"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        redis_client.set(access_token, email)
        redis_client.expire(access_token, timedelta(seconds=21600))

    except RedisError as redis_err:
        logger.error(f"{email} - Redis error: {str(redis_err)}")
        return JSONResponse(
            content={"message": "Error storing token in Redis"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = JSONResponse(content={"token": access_token})
    response.set_cookie("Authorization", f"Bearer {access_token}")

    logger.info(f"{email} - Login function execution complete")
    return response


def logout_api(auth: List[str]) -> JSONResponse:
    """Logout API to remove user access"""

    email = auth[1]
    logger.info(f"{email} - Logout function execution starts")
    try:
        redis_client.delete(auth[0])
        logger.info(f"{email} - Logout function execution complete")
        response = JSONResponse(content={"message": "Logged out successfully"})
        response.delete_cookie('Authorization')
        return response

    except RedisError as redis_err:
        logger.error(f"{email} - Redis error: {str(redis_err)}")
        return JSONResponse(
            content={"message": "Error removing token from Redis"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        logger.error(f"{email} - Logout API failed: {str(e)}")
        return JSONResponse(
            content={"message": "An error occurred"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
