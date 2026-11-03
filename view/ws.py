import json

from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from pydantic import ValidationError

from errors import AuthServiceUnavailable,InvalidToken, UserNotFoundAuthService, CommandError, FatalError
from dependencies import AuthClientDep, ConnectionManagerDep, DispatcherDep
from schemas.events import ErrorResponse, ProtocolError, ErrorBody, Response
from schemas.commands import Envelope

router = APIRouter(tags=["websockets"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, auth_service: AuthClientDep, connection_manager: ConnectionManagerDep,
                             dispatcher: DispatcherDep):
    token = websocket.query_params.get("access_token")
    await websocket.accept()
    if not token:
        await websocket.close(InvalidToken.close_code)
        return
    try:
        user = await auth_service.get_current_user(token)
    except (AuthServiceUnavailable, InvalidToken, UserNotFoundAuthService) as exc:
        await websocket.close(exc.close_code)
        return
    user_id = user.get("user_id")
    connection_manager.connect(user_id=user_id, websocket=websocket)
    try:
        while True:
            try:
                data = await websocket.receive_json()
                envelope = Envelope(**data)
                result = await dispatcher.handle(user_id, envelope)
                if result is not None:
                    response = Response(type=result["type"], request_id=envelope.request_id,
                                        payload=result["payload"])
                    await websocket.send_json(response.model_dump(mode="json"))
            except (json.JSONDecodeError, ValueError):
                error = ProtocolError(
                    error=ErrorBody(code="invalid_json", message="invalid json, value error or jsondecodeerror lox")
                )
                await websocket.send_json(error.model_dump(mode="json"))
                continue
            except ValidationError:
                error = ProtocolError(error=ErrorBody(code="invalid_envelope",
                                                      message="invalid envelope from front, снова прислать херь мне"))
                await websocket.send_json(error.model_dump(mode="json"))
                continue
            except CommandError as exc:
                error = ErrorResponse(
                    request_id=envelope.request_id,
                    error=ErrorBody(code=exc.code, message="broooooo xyety prislal")
                )
                await websocket.send_json(error.model_dump(mode="json"))

            except FatalError as exc:
                error = ErrorResponse(
                    request_id=envelope.request_id,
                    error=ErrorBody(code=exc.code, message="Mne poxyi ya zakryl connect bb")
                )
                await websocket.send_json(error.model_dump(mode="json"))
                await websocket.close(exc.close_code)
                return
            except WebSocketDisconnect:
                break
    finally:
        connection_manager.disconnect(user_id, websocket)



    