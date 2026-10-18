from clients.chat_client import ChatClient
from schemas.events import Event
from services.chat_broadcaster import Broadcast
from services.connection_manager import ConnectionManager


class MessageHandler:
    def __init__(self, connection_manager: ConnectionManager, chat_client: ChatClient, broadcaster: Broadcast):
        self.connection_manager = connection_manager
        self.chat_client = chat_client
        self.broadcaster = broadcaster

    async def send_message(self, user_id: str, payload: dict):
        response = await self.chat_client.save_message(user_id=user_id, payload=payload)
        message = response
        event = Event(type="message_created", payload=message) # ивент для фронта что сообщение создано и само сообщение собсна
        # для push уведов в будущем(offline_users)
        offline_users = await self.broadcaster.broadcast_exclude_author(user_id=user_id,
                                                                        event=event,
                                                                        chat_id=response["chat_id"])
        return {"type": "message_sent", "payload": message}

    async def edit_message(self, user_id: str, payload: dict):
        response = await self.chat_client.edit_message(user_id=user_id, payload=payload)
        message = response
        event = Event(type="message_edit", payload=message)
        await self.broadcaster.broadcast_exclude_author(user_id=user_id, event=event, chat_id=response["chat_id"])
        return {"type": "message_edit_confirmed", "payload": message}

    async def delete_message(self, user_id: str, payload: dict):
        response = await self.chat_client.delete_message(user_id=user_id, payload=payload)
        message_for_front = {
            "message_id": response["message_id"],
            "chat_id": response["chat_id"]
        }
        event = Event(type="message_deleted", payload=message_for_front)
        # отправка того что сообщения удалено всем юзерам чата

        offline_users = await self.broadcaster.broadcast_exclude_author(user_id=user_id,
                                                                        event=event,
                                                                        chat_id=response["chat_id"])
        return {"type": "message_deleted_confirmed", "payload": message_for_front}
