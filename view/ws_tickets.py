from fastapi import APIRouter, HTTPException
from dependencies import AuthClientDep, HTTPBearerDep, TicketStoreDep
from errors import FatalError


ticket_router = APIRouter(tags=["ticket"])


@ticket_router.post("/ws-ticket")
async def create_ticket(auth_service: AuthClientDep, credentials: HTTPBearerDep, ticket_store: TicketStoreDep):
    token = credentials.credentials
    try:
        user = await auth_service.get_current_user(token)
        ticket = await ticket_store.issue(user["user_id"])
        return {"ticket": ticket, "expires_in": ticket_store.TTL_SECONDS}
    except FatalError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.code)



