from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .views import home, tasks,auth
from .schemas.requests import get_code_samples
from .core.config import settings

description = """
Task Monitoring APIs
"""
tags_metadata = [
    {
        "name": "API HTTP Responses",
        "description": "Apart from the response codes specified in each API, the API server may respond with certain 4xx and 5xx error codes which are related to common API Gateway behaviours. The application should address them accordingly.",
    },
    {
        "name": "Miscellaneous",
        "description": "Utility APIs",
    },
]


app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://task-monitoring-dashboard.netlify.app"
]

# cross origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

################
# MISCELLANEOUS
################

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(tasks.router)


@app.exception_handler(RequestValidationError)
def custom_form_validation_error(request, exc):
    error_list = []
    for pydantic_error in exc.errors():
        error_list.append(
            {pydantic_error["loc"][1]: pydantic_error["msg"].capitalize()}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"errors": error_list}),
    )


def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        description=description,
        routes=app.routes,
        tags=tags_metadata,
        contact={
            "name": "For support contact SIRPI Team at:",
            "email": "sirpi@sirpi.io",
        },
    )

    for route in app.routes:
        if (
            ".json" not in route.path
            and "/docs/oauth2-redirect" not in route.path
            and "/docs" not in route.path
            and "/redoc" not in route.path
        ):
            for method in route.methods:
                if method.lower() in openapi_schema["paths"][route.path]:
                    code_samples = get_code_samples(route=route, method=method)
                    openapi_schema["paths"][route.path][method.lower()][
                        "x-codeSamples"
                    ] = code_samples

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# assign the customized OpenAPI schema
app.openapi = custom_openapi
