from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from fastapi.responses import JSONResponse

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def init_middlewares(app: FastAPI):
    
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def verify_jwt_middleware(request: Request, call_next):
        if request.url.path not in ["/users/login", "/users"]:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                try:
                    token = auth_header.split(" ")[1]
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    request.state.user = payload
                except (JWTError, IndexError):
                    return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "status": 403,
                        "detail": "Could not validate credentials"
                        },
                )
            else:
                return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                        "status": 403,
                        "detail": "Authorization header missing"
                        },
                )
        response = await call_next(request)
        return response
    
export = init_middlewares