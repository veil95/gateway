from fastapi import APIRouter, HTTPException, Response, Request
from dependencies import AuthClientDep
from schemas.user import UserLogin, UserRegistration
from errors import AuthServiceUnavailable, FatalError
from dependencies import HTTPBearerDep


auth_router = APIRouter(tags=["auth"])


@auth_router.post("/auth/login")
async def login(user: UserLogin, auth_service: AuthClientDep):
    try:
        response = await auth_service.user_login(username=user.username, password=user.password)
    except AuthServiceUnavailable as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)
    headers = {}
    content_type = response.headers.get("Content-Type")

    if content_type is not None:
        headers["Content-Type"] = content_type

    browser_response = Response(status_code=response.status_code, content=response.content, headers=headers)

    for set_cookie in response.headers.get_list("Set-Cookie"):
        browser_response.headers.append("Set-Cookie", set_cookie)

    return browser_response


@auth_router.post("/auth/register")
async def register(user: UserRegistration, auth_service: AuthClientDep):
    try:
        response = await auth_service.user_registration(username=user.username,
                                                        password_plaintext=user.password_plaintext,
                                                        display_name=user.display_name)
    except AuthServiceUnavailable as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    browser_response = Response(status_code=response.status_code, content=response.content)

    return browser_response


@auth_router.get("/auth/me")
async def get_profile(credentials: HTTPBearerDep, auth_service: AuthClientDep):
    token = credentials.credentials
    try:
        user = await auth_service.get_current_user(token)
    except FatalError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    return user


@auth_router.post("/auth/refresh")
async def get_refresh_token(request: Request, auth_service: AuthClientDep):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="no refresh token")
    try:
        response = await auth_service.refresh_token(refresh_token)
    except AuthServiceUnavailable as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)

    headers = {}
    content_type = response.headers.get("Content-Type")

    if content_type is not None:
        headers["Content-Type"] = content_type

    browser_response = Response(status_code=response.status_code, headers=headers, content=response.content)

    for set_cookie in response.headers.get_list("Set-Cookie"):
        browser_response.headers.append("Set-Cookie", set_cookie)

    return browser_response