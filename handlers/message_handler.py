from clients.chat_client import ChatClient
from schemas.events import Event

class MessageHandler:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    async def send_message(self, user_id: str, payload: dict, chat_client: ChatClient):
        response = await chat_client.save_message(user_id=user_id, payload=payload)
        recipients = [uid for uid in response["members"] if uid != user_id]
        message = response["message"]

        event = Event(type="message_created", payload=message) # ивент для фронта что сообщение создано и само сообщение собсна

        offline_users = await self.connection_manager.send_to_users(user_ids=recipients,
                                                                    data=event.model_dump(mode="json")) # для push уведов в будущем(offline_users)
        return {"type": "message_sent", "payload": message}

    async def edit_message(self, user_id: str, payload: dict, chat_client: ChatClient):
        response = await chat_client.edit_message(user_id=user_id, payload=payload)
        message = response["message"]
        recipients = [uid for uid in response["members"] if uid != user_id]

        event = Event(type="message_edit", payload=message)

        offline_users = await self.connection_manager.send_to_users(user_ids=recipients,
                                                                    data=event.model_dump(mode="json"))
        return {"type": "message_edit_confirmed", "payload": message}

    async def delete_message(self, user_id: str, payload: dict, chat_client: ChatClient):
        response = await chat_client.delete_message(user_id=user_id, payload=payload)
        message_for_front = {
            "message_id": response["message_id"],
            "chat_id": response["chat_id"]
        }
        recipients = [uid for uid in response["members"] if uid != user_id]
        event = Event(type="message_deleted", payload=message_for_front)
        offline_users = await self.connection_manager.send_to_users(user_ids=recipients,
                                                                    data=event.model_dump(mode="json")) # отправка того что сообщения удалено всем юзерам чата
        return {"type": "message_deleted_confirmed", "payload": message_for_front}