from clients.chat_client import ChatClient
from services.connection_manager import ConnectionManager
from schemas.events import Event
from errors import ChatServiceUnavailable, ChatNotFound
import logging

logger = logging.getLogger(__name__)


class Broadcast:
    def __init__(self, chat_client: ChatClient, connection_manager: ConnectionManager):
        self.chat_client = chat_client
        self.connection_manager = connection_manager

    async def broadcast_exclude_author(self, user_id: str, event: Event, chat_id: int):
        try:
            response = await self.chat_client.get_chat_members(chat_id=chat_id)
            recipients = [uid for uid in response["members"] if uid != user_id]
            offline_users = await self.connection_manager.send_to_users(user_ids=recipients,
                                                                        data=event.model_dump(mode="json"))
            return offline_users
        except ChatNotFound:
            logger.warning("Не удалось найти чат с таким chat_id %s", chat_id)
        except ChatServiceUnavailable:
            logger.warning("Чат сервис не работает для chat_id %s", chat_id)
        except Exception:
            logger.exception("Непредвиденная ошибка для chat_id %s", chat_id)
        return set()
    